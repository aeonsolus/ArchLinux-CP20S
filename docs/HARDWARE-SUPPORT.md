# CP20S hardware support matrix

This project targets the INCAR CP20S tablet with Rockchip RK3562. Results below are engineering observations from prior development, not a current live-device report. The tablet is not connected as part of this repository work. Re-run and record the tests against a clean build before release.

| Area | Prior evidence | Release status |
|---|---|---|
| Kernel and boot | CP20S previously ran Arch Linux ARM userspace on a vendor-derived Linux 6.1 kernel. The tested Arch root was nested inside userdata and depended on a custom initramfs handoff. | Direct-root boot, matched public build inputs, cold boot, and recovery are not accepted. |
| Internal storage | Development used Android userdata for Linux files. This target contains user data and must be fully backed up before a direct-root install. | Exact target layout and installer manifest are not published or validated. |
| GPU | Prior desktop evidence reported Panfrost/Mali-G52 EGL and Mutter GBM rendering. A small guarded GPL-2.0 compatibility module addresses a device-tree IRQ-name mismatch. | Rebuild against the exact target kernel and confirm Mutter renderer/frame performance on each release. |
| Video decode | Kernel MPP/RKVDEC components were present, but browser hardware decode was not demonstrated. | Unverified. Do not claim Chrome or Electron video decode acceleration. |
| Audio | RK817 routing was adjusted during development; a speaker test was reported audible in one session. | Re-test built-in speakers and headphone jack independently after a clean boot and resume. |
| Wi-Fi/Bluetooth | Wi-Fi connected in prior sessions but throughput and power-save behavior varied. Bluetooth keyboard pairing/input was inconsistent. | Unverified; cold-boot and sustained connection checks required. |
| Volume keys | Debian used the ADC channel `iio:device0/in_voltage1_raw`: volume-up at values ≤120; volume-down from 650–920, 5% steps, 150% cap. | Arch service, ADC channel stability, and duplicate GNOME key handling are unverified. |
| Sensors/rotation | Sensor readings were observed, but rotation/display-manager behavior changed during development. Gyroscope rate was reported too fast at one point. | Unverified. Preserve sensor configuration until rates and orientation are measured. |
| Suspend/resume | Adaptive CPU/GPU/DMC policies and a sleep profile were explored. | Complete suspend/resume, frequency restore, audio, radios, and data integrity are not accepted. |
| GNOME touch profile | GNOME Shell 51, TouchUp, TouchBoard, and other extensions were used or attempted. Mutter hardware rendering was reported in a prior desktop session. | Fresh install, TouchBoard docking/text entry, gesture smoothness, and extension compatibility are release gates. |
| Performance and memory | Prior runs reported adaptive stock governors and Panfrost. A measured GNOME Shell idle snapshot was around 850 MiB RSS; transient CPU spikes were inconsistent. | Publish clean-boot RAM, idle CPU, and frame-time measurements. There is no 750 MB hard cap. |

## Performance policy

Use only operating points exposed by the matching CP20S firmware/kernel. Keep stock thermal and regulator limits. Do not add unsupported CPU, GPU, or DRAM frequencies or voltage offsets to release profiles. Adaptive governors should allow low idle frequencies while keeping supported stock ceilings available under load.

## Release evidence format

For each release, record kernel/config provenance, device tree and module hashes, GNOME/Mutter renderer, separate audio route results, radio throughput/power policy, physical key mapping, sensor rates/orientation, suspend/resume, idle RAM/CPU, and cold-boot/recovery outcomes. Include date, release image hash, and pass/fail result, but exclude personal paths, account names, serial numbers, private network identifiers, and raw userdata/firmware images.
