# CP20S Panfrost IRQ-name compatibility module

The CP20S kernel's GPU node has been observed with `interrupt-names` spelled `GPU`, `MMU`, and `JOB`, while the matching Panfrost driver expects lowercase names. This module checks the exact device, compatible string, current property, and three distinct IRQ mappings, then changes only the property names through the kernel OF APIs. It does not change IRQ assignments or clock/voltage policy.

The code is GPL-2.0, as marked in the source. Build only against the exact kernel source/build tree and toolchain for the CP20S image. The `Makefile` is a Kbuild fragment; it is not a standalone kernel build system. Confirm the device-tree property and driver probing order before use. The module is intentionally not unloadable because the allocated OF property must stay valid until shutdown.

**Status:** Prior Panfrost operation was observed, but this module is not proof of Mutter acceleration and has not been accepted after the latest boot changes. Do not package a prebuilt `.ko`; kernel ABI matching is mandatory.
