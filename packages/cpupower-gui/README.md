# CP20S cpupower-gui package patch

This package is based on upstream cpupower-gui 1.0.0 and adds a small parser fix for Python 3.14-compatible startup. The upstream parser declares `apply` as a positional argument with `action="store_true"`; `argparse` rejects that during module initialization, preventing both the command-line tool and the GTK application from launching. The patch keeps the documented `cpupower-gui config` behavior and also accepts `cpupower-gui config apply`.

The package install hook enables the privileged helper but leaves `cpupower-gui.service` disabled. The CP20S `cp20s-adaptive-governors.service` owns the CPU/GPU/DMC policy at boot; enabling the generic GUI service would introduce a second CPU policy owner. The GUI remains available for viewing and applying user-selected CPU profiles.

Build with `makepkg -si` from this directory on an Arch Linux host. The recipe fetches the upstream source archive and verifies its SHA-256 before applying the local patch. Keep the upstream GPL license and notices with the resulting package.

The Extreme Performance entry is a CPU frequency/governor profile. It uses the live selector-3 stock OPP table and does not expose a voltage offset or create new CPU, GPU, or DRAM operating points. See [`../../profiles/power/README.md`](../../profiles/power/README.md).
