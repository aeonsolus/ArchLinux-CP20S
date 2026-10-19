#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
import importlib.util
import io
import struct
import unittest
import uuid
import zlib
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[2] / "scripts/host/inspect-gpt.py"
SPEC = importlib.util.spec_from_file_location("inspect_gpt", MODULE_PATH)
inspect_gpt = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inspect_gpt)


def make_gpt():
    image = bytearray(100 * 512)
    entry_size = 128
    entries = bytearray(128 * entry_size)
    entry = bytearray(entry_size)
    entry[:16] = uuid.UUID("0fc63daf-8483-4772-8e79-3d69d8477de4").bytes_le
    entry[16:32] = uuid.UUID("11111111-2222-3333-4444-555555555555").bytes_le
    struct.pack_into("<QQQ", entry, 32, 40, 59, 0)
    entry[56:72] = "archroot".encode("utf-16le")
    entries[:entry_size] = entry
    entries_lba = 2
    entries_crc = zlib.crc32(entries) & 0xFFFFFFFF
    image[entries_lba * 512 : entries_lba * 512 + len(entries)] = entries

    header = bytearray(512)
    header[:8] = b"EFI PART"
    struct.pack_into("<IIIIQQQQ", header, 8, 0x00010000, 92, 0, 0, 1, 99, 34, 98)
    header[56:72] = uuid.UUID("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee").bytes_le
    struct.pack_into("<QIII", header, 72, entries_lba, 128, entry_size, entries_crc)
    struct.pack_into("<I", header, 16, zlib.crc32(header[:92]) & 0xFFFFFFFF)
    image[512:1024] = header
    return image


class InspectGptTests(unittest.TestCase):
    def test_reads_partition_map_and_validates_crcs(self):
        result = inspect_gpt.read_gpt(io.BytesIO(make_gpt()), 100 * 512)
        self.assertEqual(result["partitions"][0]["name"], "archroot")
        self.assertEqual(result["partitions"][0]["first_lba"], 40)
        self.assertEqual(result["partitions"][0]["sectors"], 20)

    def test_rejects_header_crc_mismatch(self):
        image = make_gpt()
        image[512 + 80] ^= 0x01
        with self.assertRaisesRegex(ValueError, "header CRC mismatch"):
            inspect_gpt.read_gpt(io.BytesIO(image), len(image))

    def test_rejects_partition_outside_usable_range(self):
        image = make_gpt()
        entry_offset = 2 * 512
        struct.pack_into("<Q", image, entry_offset + 32, 10)
        entries_crc = zlib.crc32(image[entry_offset : entry_offset + 128 * 128]) & 0xFFFFFFFF
        struct.pack_into("<I", image, 512 + 88, entries_crc)
        header = bytearray(image[512:1024])
        struct.pack_into("<I", header, 16, 0)
        struct.pack_into("<I", image, 512 + 16, zlib.crc32(header[:92]) & 0xFFFFFFFF)
        with self.assertRaisesRegex(ValueError, "invalid LBA bounds"):
            inspect_gpt.read_gpt(io.BytesIO(image), len(image))


if __name__ == "__main__":
    unittest.main()
