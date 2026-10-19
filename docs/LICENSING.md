# Licensing and redistribution

The project declares separate licenses for original code and documentation:

- Original project code and configuration: MIT, unless a file has its own SPDX/license notice.
- Documentation: CC BY 4.0.
- `src/gpu-irq-compat/`: GPL-2.0 as identified in its source.
- Third-party packages, GNOME extensions, themes, wallpapers, fonts, firmware, and device images retain their upstream licenses and are not relicensed by this repository.

The public repository must not include Android vendor firmware, proprietary kernel modules, boot images, DTBs, radio/GPU blobs, user data, credential material, raw conversation logs, or private system images unless redistribution rights have been established and documented for the exact file. Build inputs supplied by the tablet owner remain outside Git by default.

Before every public release, review the complete tracked tree and Git history for secrets, personal paths, identifiers, vendor material, and third-party code. The attribution list in [CREDITS.md](CREDITS.md) is not a license grant or endorsement.
