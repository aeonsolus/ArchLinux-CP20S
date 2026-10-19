# Clean installation design

## Intended user path

Install Arch Linux ARM to the CP20S internal Linux root from a host over USB. The owner should not need Debian, an SD card, Tailscale, or a serial shell. The release must offer both a guided USB installer and a concise manual procedure using the same verified artifacts and target map.

**This installer does not exist yet. Do not flash from this repository.** The available scripts only verify/extract a signed generic userspace archive and apply a small overlay.

## Data and partition behavior

The engineering layout used partition 25 as Android userdata; it later contained both the Debian environment and nested Arch root. Reformatting it as a direct Arch root destroys everything on that partition, including personal files and the nested installation. It is not safe to call this “replacing Debian only.”

A future installer must:

1. Identify the exact CP20S and read the current GPT from the attached device in the supported Rockchip recovery mode.
2. Save a complete host-side readback of the current userdata and every boot partition the procedure might modify; verify sizes and hashes by reading back the saved data.
3. Require the owner to confirm that the userdata partition will be erased and provide a separate backup location for any data they want to keep.
4. Verify the intended Linux-root target by partition GUID/name, start/end sectors, capacity, and a reviewed manifest generated from CP20S evidence. Never infer target offsets from another RK3562 tablet or a stale repository snapshot.
5. Preserve GPT and Android boot/vendor/recovery partitions. Only explicitly listed Linux boot assets and the Linux root target may be written.
6. Verify every write by reading the affected range back and comparing it with the release artifact.

No current public partition manifest, matching boot artifact set, independent full userdata backup, or tested rollback procedure is present. That blocks both a guided writer and safe manual flash instructions.

## Credentials and first boot

No preset password is allowed in a release image. The installer must prompt the owner to create the initial account password locally, set a unique hostname, and keep remote login disabled until setup is complete. It must not enable autologin by default. Recovery access must be documented without shipping reusable credentials.

## Required clean-install acceptance

- Build from documented, owner-supplied CP20S inputs and a pinned AArch64 package snapshot.
- Validate device identity, GPT layout, artifact signatures, and free backup space before writing.
- Install to internal storage without Debian, SD media, Tailscale, or a serial terminal.
- Verify write readback, cold boot to direct Arch root, user setup, and recovery from a deliberately failed test boot.
- Confirm all Android boot/vendor/recovery partitions and the GPT are unchanged unless a release manifest explicitly identifies a boot asset as required.
- Run the hardware and desktop checks in [the support matrix](HARDWARE-SUPPORT.md).

Until every item passes on the CP20S, label the repository and artifacts **engineering preview — not ready to flash**.
