# CP20S clock and voltage policy

No overclock is included in ArchLinux-CP20S. The prior tablet kernel exposed approximately 408–2016 MHz CPU, 300–900 MHz Mali-G52, and 324–920 MHz DMC ranges. These are historical observations and may differ by firmware or board revision.

Release profiles must stay within the exact stock operating points provided by the matching CP20S firmware, kernel, and device tree. Use adaptive CPU/GPU/DMC governors so the system can idle at lower supported rates while retaining supported stock ceilings under load. Do not add guessed operating points, regulator offsets, or unsupported frequencies.

The earlier experimental clock ladder and candidate boot-image artifacts were per-device engineering material. They are not a release configuration or a validated recipe and are intentionally not published here. Any future overclock investigation belongs in a separate, explicitly experimental branch with a verified recovery path and board-specific stability evidence.
