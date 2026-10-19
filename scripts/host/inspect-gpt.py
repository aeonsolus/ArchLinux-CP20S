#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only GPT inspector for an image or block-device readback."""

import argparse
import fcntl
import json
import os
import stat
import struct
import sys
import uuid
import zlib

SECTOR = 512


def read_gpt(stream, byte_size):
    if byte_size < 3 * SECTOR or byte_size % SECTOR:
        raise ValueError("input size must be a whole number of sectors and at least 3 sectors")
    stream.seek(SECTOR)
    sector = stream.read(SECTOR)
    if len(sector) != SECTOR or sector[:8] != b"EFI PART":
        raise ValueError("primary GPT signature not found at LBA 1")

    revision, header_size, header_crc, reserved, my_lba, backup_lba, first_usable, last_usable = struct.unpack_from(
        "<IIIIQQQQ", sector, 8
    )
    if not 92 <= header_size <= SECTOR or my_lba != 1:
        raise ValueError("invalid primary GPT header size or current LBA")
    header_copy = bytearray(sector[:header_size])
    struct.pack_into("<I", header_copy, 16, 0)
    if zlib.crc32(header_copy) & 0xFFFFFFFF != header_crc:
        raise ValueError("primary GPT header CRC mismatch")
    if backup_lba >= byte_size // SECTOR or backup_lba == 1:
        raise ValueError("backup GPT LBA is outside the input or invalid")

    disk_guid = uuid.UUID(bytes_le=sector[56:72])
    entry_lba, entry_count, entry_size, entries_crc = struct.unpack_from("<QIII", sector, 72)
    if entry_count == 0 or entry_count > 16384 or entry_size < 128 or entry_size % 8:
        raise ValueError("invalid GPT partition entry geometry")
    entries_bytes = entry_count * entry_size
    entries_offset = entry_lba * SECTOR
    if entries_offset < 2 * SECTOR or entries_offset + entries_bytes > byte_size:
        raise ValueError("GPT partition entries extend outside the input")
    stream.seek(entries_offset)
    raw_entries = stream.read(entries_bytes)
    if len(raw_entries) != entries_bytes or zlib.crc32(raw_entries) & 0xFFFFFFFF != entries_crc:
        raise ValueError("GPT partition array CRC mismatch")

    partitions = []
    total_sectors = byte_size // SECTOR
    for number in range(entry_count):
        entry = raw_entries[number * entry_size : (number + 1) * entry_size]
        type_bytes = entry[:16]
        if type_bytes == bytes(16):
            continue
        type_guid = uuid.UUID(bytes_le=type_bytes)
        unique_guid = uuid.UUID(bytes_le=entry[16:32])
        first_lba, last_lba, attributes = struct.unpack_from("<QQQ", entry, 32)
        if first_lba > last_lba or first_lba < first_usable or last_lba > last_usable or last_lba >= total_sectors:
            raise ValueError(f"partition {number + 1} has invalid LBA bounds")
        name = entry[56 : min(128, entry_size)].decode("utf-16le", errors="strict").split("\0", 1)[0]
        partitions.append(
            {
                "number": number + 1,
                "name": name,
                "type_guid": str(type_guid),
                "partition_guid": str(unique_guid),
                "first_lba": first_lba,
                "last_lba": last_lba,
                "sectors": last_lba - first_lba + 1,
                "bytes": (last_lba - first_lba + 1) * SECTOR,
                "attributes": f"0x{attributes:016x}",
            }
        )

    return {
        "sector_size": SECTOR,
        "total_sectors": total_sectors,
        "gpt_revision": f"{revision >> 16}.{revision & 0xffff:04x}",
        "disk_guid": str(disk_guid),
        "backup_gpt_lba": backup_lba,
        "first_usable_lba": first_usable,
        "last_usable_lba": last_usable,
        "partitions": partitions,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="GPT image or block-device readback (opened read-only)")
    args = parser.parse_args()
    try:
        with open(args.input, "rb", buffering=0) as stream:
            info = os.fstat(stream.fileno())
            if stat.S_ISBLK(info.st_mode):
                size = struct.unpack("Q", fcntl.ioctl(stream.fileno(), 0x80081272, b"\0" * 8))[0]
            else:
                size = info.st_size
            if not size:
                raise ValueError("input has zero apparent size")
            result = read_gpt(stream, size)
        print(json.dumps(result, indent=2, sort_keys=True))
    except (OSError, ValueError, struct.error) as exc:
        print(f"inspect-gpt: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
