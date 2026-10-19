# Build and installation status

## Status

This repository is an engineering preview, not a ready-to-flash distro. It has a signed Arch Linux ARM userspace extraction helper and a small rootfs overlay. It does not yet build a complete root filesystem image, build the CP20S initramfs/boot container, or write the tablet over USB.

Prior work recorded a vendor-derived Linux 6.1.172 kernel, Arch ARM userspace, a nested Arch root on Android userdata, and one long-running post-fix boot. That layout depended on a custom initramfs and userdata contents. It is not the direct-root design proposed here, and the device is not currently being checked as part of this repository change. Treat all live-device state and previous test results as historical until revalidated.

## Required build inputs

An actual CP20S release needs a documented and checksummed set of owner-supplied files:

- A signed AArch64 Arch Linux ARM rootfs and trusted keyring.
- The exact CP20S kernel image, matching modules, and matching kernel configuration/source provenance.
- The exact CP20S device tree and any required board configuration.
- Matching radio, GPU, and other firmware, retained outside Git unless redistribution is explicitly cleared.
- A source-built CP20S initramfs and a verified method to place it in the CP20S boot chain.
- A fresh GPT/readback manifest, verified userdata backup, and matching rollback images.
- A pinned Arch Linux ARM AArch64 package repository snapshot for reproducible GNOME 51/profile package resolution.

The `scripts/host/extract-archarm-rootfs.sh` helper verifies a detached signature with `gpgv` before extracting a generic rootfs. `scripts/host/apply-overlay.sh` copies only files that are absent or byte-identical. Neither script installs packages, creates an image, prepares boot assets, partitions storage, nor modifies a tablet.

## Why no flash command is included

The prior userdata layout and boot chain are device-specific, and current eMMC offsets cannot safely be inferred from old notes or another RK3562 board. The project still lacks a public, independently reviewed partition manifest and complete matching boot source/artifacts. A script that writes based on guessed offsets would risk destroying Android recovery or the only bootable copy of the device.

The installer will remain absent until a fresh CP20S GPT/readback, explicit root-target validation, full data backup, recovery test, and cold-boot test are complete. The manual instructions will use the same validated manifest and will not provide an alternate unguarded path.

## Current host preparation helper

Run `scripts/host/extract-archarm-rootfs.sh ARCHIVE SIGNATURE KEYRING EMPTY_DESTINATION` on a Linux host with `gpgv`, GNU tar, `sha256sum`, and sufficient storage. It requires root to preserve ownership and refuses non-empty/system destinations. Use only the upstream AArch64 archive whose signature matches the supplied trusted keyring.

The extracted tree is generic AArch64 userspace only. It does not contain CP20S kernel/DT support by virtue of being Arch Linux ARM.

## Read-only GPT inspection

`scripts/host/inspect-gpt.py IMAGE_OR_BLOCK_READBACK` parses the primary GPT header and entry-array CRCs and prints the partition names, GUIDs, LBA ranges, and byte sizes as JSON. It opens its input read-only. Use it only on a host-side readback or image and review the complete result; this tool does not identify a device as CP20S or authorize a write.
