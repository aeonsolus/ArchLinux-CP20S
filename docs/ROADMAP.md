# Release roadmap

## Source and reproducibility

- [x] Create a public-facing repository structure while keeping the engineering archive private.
- [x] Separate base, GNOME, and optional-pack package intent.
- [x] Add original-code and documentation license declarations while retaining the GPU module's GPL-2.0 identifier.
- [ ] Extract and review only public-safe findings from the session and private archive; never import raw transcripts or vendor blobs.
- [ ] Pin the AArch64 package snapshot and resolve every base/GNOME package against it.
- [ ] Add a reproducible rootfs/image builder consuming checksummed owner-supplied CP20S inputs.
- [ ] Build the Debian-independent initramfs/root handoff from reviewed source and test its boot artifact format.

## Install and recovery

- [ ] Capture a fresh CP20S GPT and boot-partition readback; produce a reviewed partition manifest.
- [ ] Create and verify a complete userdata backup and independent boot-asset rollback set.
- [ ] Add a guided USB installer that validates identity, manifest, backup, and release signatures before any write.
- [ ] Add matching manual instructions; keep all writes limited to the approved Linux root/boot targets.
- [ ] Test readback verification, controlled cold boot, failed-boot recovery, and preservation of Android partitions.

## Desktop and hardware release gates

- [ ] Package GNOME 51, TouchUp, and TouchBoard without silently substituting Squeekboard.
- [ ] Pass TouchBoard docking and text-entry checks in GNOME, Chrome, and Electron.
- [ ] Pass Panfrost/Mutter rendering, speakers and headphone jack as separate routes, Wi-Fi, Bluetooth keyboard, volume keys, rotation, suspend/resume, and cold boot.
- [ ] Measure RAM and idle CPU on a reproducible boot; publish results without a 750 MB hard cap.
- [ ] Publish only after license/provenance review and all required device acceptance checks pass.

All unchecked items are open work. Repository files and prior device notes do not imply that a release or device test has passed.
