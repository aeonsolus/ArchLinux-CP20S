# ArchLinux-CP20S

**An unofficial Arch Linux ARM tablet system for the INCAR CP20S (Rockchip RK3562).**

> **Status: engineering preview; not ready to flash.** This repository now contains a public-project structure, board integration sources, and guarded host-side preparation tools. It does not yet contain a complete, reproducibly built, cold-boot-accepted image or a validated installer. Do not flash it to a tablet.

The goal is a direct Arch Linux installation on the CP20S internal Linux root, with GNOME 51, TouchUp gestures, and TouchBoard as the default touch keyboard. A release must preserve the existing partition table and Android boot/vendor/recovery partitions, and must have a tested recovery path. The Linux root target currently corresponds to Android userdata in the engineering layout; installing there erases its contents. A verified user-data backup is mandatory.

## Start here

1. [Project status and build inputs](docs/INSTALL.md)
2. [USB installation and data-loss gates](docs/CLEAN-INSTALL.md)
3. [Hardware support matrix](docs/HARDWARE-SUPPORT.md)
4. [GNOME tablet profile](docs/DESKTOP.md)
5. [License and redistribution policy](docs/LICENSING.md)

## Repository contents

- `rootfs/` — small CP20S integration overlay; not a complete operating system.
- `scripts/host/` — signed Arch ARM rootfs extraction, safe overlay, read-only GPT inspection, and release-tree checks. No current script flashes the tablet.
- `profiles/` — GNOME, performance, and future optional-package profile definitions.
- `packages/` — locally maintained package recipe and patch.
- `src/gpu-irq-compat/` — guarded GPL-2.0 compatibility module source for a device-tree IRQ-name quirk.
- `docs/` — support evidence, installation constraints, recovery notes, and acceptance requirements.

## Build and release policy

The generic Arch Linux ARM rootfs is userspace only. A CP20S release also needs matching, owner-supplied kernel, device tree, modules, firmware, and boot/initramfs artifacts. This repository does not redistribute Android vendor binaries or assume that a generic RK3562 image is interchangeable with CP20S firmware. See [the required inputs](docs/INSTALL.md).

No overclocking, voltage changes, personal credentials, Tailscale configuration, or private system images are part of the release. Performance uses supported stock operating points and adaptive policies. Optional application and appearance packs are kept separate from the base system.

## Contributing and status

This is not an official Arch Linux ARM, GNOME, Rockchip, or INCAR release. Hardware claims are labeled by evidence and date. Failed or untested acceptance checks remain visible; no checkboxes are treated as passed just because a script exists.

See [credits](docs/CREDITS.md) and [licensing](docs/LICENSING.md) before reusing project files.
