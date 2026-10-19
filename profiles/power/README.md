# CP20S power profiles

Incremental overclock work is tracked separately in [the overclock lab chart](overclock-lab.md). The Extreme Performance profile remains on stock limits until each new frequency and voltage pair has been tested on this tablet.

The `rootfs/etc/cpupower_gui.d/extreme-performance.profile` overlay adds a separate **Extreme Performance** entry to cpupower-gui. It does not change the existing **Performance** profile or the configured default. It allows CPU0–CPU3 to use the full stock 2016 MHz ceiling with `schedutil`, selecting lower stock OPPs and their validated voltage entries when demand is low. The boot services keep CPU/GPU/DMC limits at their stock ceilings, use adaptive `schedutil` / `simple_ondemand` / `dmc_ondemand` governors, and enable Panfrost runtime power management so the GPU can suspend between render work. This reduces idle/light-load clocks and power; it is not a voltage offset or a CPU/GPU undervolt.

The live CP20S exposed these GPU/DMC operating points. Before adaptive governors were selected, both devices were at their maximum with the `performance` governor:

| Domain | Live supported range | Requested target | Difference above live maximum |
| --- | ---: | ---: | ---: |
| CPU | 408–2016 MHz | 2200 MHz | +184 MHz / +9.13% |
| Mali-G52 GPU | 300–900 MHz | 1000 MHz | +100 MHz / +11.11% |
| DMC (memory controller) | 324–920 MHz | 1056–1064 MHz | +136–144 MHz / +14.78–15.65% |

Those overclock targets are **not applied** by this profile. They exceed live operating points by 184 MHz / 9.13% for CPU, 100 MHz / 11.11% for GPU, and 136–144 MHz / 14.78–15.65% for DMC. The running kernel does not expose 2200 MHz CPU, 1000 MHz GPU, or 1056–1064 MHz DMC points. The active device tree puts the GPU's table through 900 MHz; its separate NPU table contains a 1000 MHz point. The DMC device tree has a 1560 MHz OPP entry, but live devfreq reports only 324, 528, 780, and 920 MHz. Live driver logs set the DMC `performance_rate` to 920 MHz. The active `uboot_a` image also matches the captured Android-stock `uboot_a` byte-for-byte. Rockchip's DMC driver obtains the usable DDR frequency list from firmware, so adding a GUI limit or changing only that device-tree entry cannot make a new DDR rate usable.

## Research and validation status

Rockchip's RK3562 product specification states Cortex-A53 operation up to 2.0 GHz and identifies the GPU as Mali-G52 2EE. The remembered combination of **2.2 GHz CPU + Mali-G52 MC3** matches Rockchip's official RK3576 specification instead: that part has Cortex-A72 plus Cortex-A53 cores and a G52 MC3. This is likely where the remembered values came from; they do not establish an RK3562/CP20S overclock. The CP20S device tree and live frequency tables identify the RK3562 CPU and a Mali-G52 2EE, with current ceilings of 2016 MHz CPU and 900 MHz GPU. A “G52 MP2 at 1 GHz” claim is not board-specific validation. The upstream RK3562 device tree's 2016 MHz CPU OPP allows up to 1.15 V depending on silicon bin, while the Mali table tops out at 900 MHz. The RK3562 clock driver lists a 2208 MHz PLL rate, but a PLL rate is not a CPU OPP or evidence of stable CPU operation at that speed. The live CP20S kernel logged CPU PVTM 1423 with voltage selector 3; without a characterized higher-OPP table for this board and bin, that reading does not provide a safe 2.2 GHz voltage. The 1 GHz point elsewhere in the captured device tree belongs to the NPU, not Mali. Searching for RK3562/CP20S community reports did not produce a reproducible 2.2 GHz CPU or 1.0 GHz GPU result with board-specific voltage, temperature, and sustained-load data.

The live CPU boot log reports PVTM voltage selector 3, and the live loaded device tree exposes the corresponding CPU `L3` voltage entries: 408/600/816/1008 MHz at 825 mV, 1200 MHz at 850 mV, 1416 MHz at 925 mV, 1608 MHz at 962.5 mV, 1800 MHz at 1.05 V, and 2016 MHz at 1.10 V. These are the board's bin-selected stock OPP targets, not experimentally discovered undervolt values. The live GPU table's `L3` row is 300–700 MHz at 825 mV, 800 MHz at 875 mV, and 900 MHz at 925 mV. Its PVTM selector was not present in the boot log, so retain the shipped GPU OPP selection rather than assuming that its selector matches the CPU. Linux exposes no writable CPU/GPU voltage-offset control on this kernel.

The adaptive governors use the lower-frequency OPPs and their associated stock voltages when demand is low, while retaining the full stock frequency ceilings. This is the lowest voltage behavior supported by the captured, silicon-bin-selected tables. It is not an undervolt: lowering voltage below the selected table requires changing the OPP data, then validating each frequency under sustained load and thermal conditions. Do not substitute the lower `L4` CPU table for this selector-3 chip or write a guessed regulator voltage; that could cause calculation errors, freezes, or boot failure.

As a rough comparison, the table below estimates the CPU's dynamic switching component using `Pdyn ∝ V² × f`, normalized to the 2016 MHz / 1.10 V OPP. It assumes the same activity factor at every point. It is not total CPU power, whole-device power, energy per task, or a temperature prediction; leakage, workload duration, regulator loss, and thermal throttling are not included.

| CPU OPP | Selector-3 voltage | Estimated dynamic component vs. 2016 MHz / 1.10 V |
| ---: | ---: | ---: |
| 408 MHz | 825 mV | 11.4% |
| 600 MHz | 825 mV | 16.7% |
| 816 MHz | 825 mV | 22.8% |
| 1008 MHz | 825 mV | 28.1% |
| 1200 MHz | 850 mV | 35.5% |
| 1416 MHz | 925 mV | 49.7% |
| 1608 MHz | 962.5 mV | 61.1% |
| 1800 MHz | 1.05 V | 81.4% |
| 2016 MHz | 1.10 V | 100.0% |

This supports the adaptive profile's thermal behavior at low and moderate demand, but `schedutil` can still select the maximum OPP when workload needs it. A hard sustained-load thermal cap would need a lower maximum frequency; it cannot be achieved by claiming an unvalidated lower voltage.

After enabling the adaptive service on the CP20S, readback showed CPU `schedutil` with the original 408–2016 MHz limits, GPU `simple_ondemand` at 300 MHz with about 0.824 V on `vdd_gpu`, and DMC `dmc_ondemand` at 324 MHz. The live GPU-preparation service had separately forced `power/control=on` and `performance`, while the later adaptive service changed only its governor; this conflict left runtime PM forbidden. The project now has the GPU-preparation helper set `power/control=auto` and leave governor/frequency ownership to the adaptive service. In one five-second light-load sample, CPU frequency moved to 1416 MHz; an instantaneous later sample reached 2016 MHz, which is expected under `schedutil`. The **Performance** preset definition and configured profile key remain unchanged.

### Arithmetic estimates only — not profile values

The following is useful for sizing the experiment, but it is **not** a safe voltage table. For the live CPU silicon selector 3, the last two stock points observed were 1800 MHz at 1.05 V and 2016 MHz at 1.10 V. Extending that last voltage slope linearly gives 1.1426 V at 2200 MHz, or 1.1444 V at the nearest listed RK3562 PLL rate, 2208 MHz. That extrapolation is outside every validated CPU OPP; regulators' voltage ceilings and PLL programming support do not certify it. On the GPU, extending the observed 800 MHz/0.95 V to 900 MHz/1.00 V step gives an arithmetic estimate of 1.05 V at 1000 MHz. That too is outside the GPU OPP table and has no board-specific validation.

Using the approximate dynamic-power relation `Pdyn ∝ V² × f` gives:

| Domain and estimate | Clock uplift from live maximum | Estimated voltage | Dynamic-power component vs live maximum |
| --- | ---: | ---: | ---: |
| CPU, 2200 MHz | +9.13% | 1.1426 V, linearly extrapolated | about +17.7% |
| CPU, nearest PLL point 2208 MHz | +9.52% | 1.1444 V, linearly extrapolated | about +18.6% |
| Mali GPU, 1000 MHz | +11.11% | 1.05 V, linearly extrapolated | about +22.5% |
| DMC, 1056 MHz | +14.78% | Not derivable from these data | Not derivable from these data |
| DMC, 1064 MHz | +15.65% | Not derivable from these data | Not derivable from these data |

These are first-order estimates of the switching component only. They omit leakage, regulator losses, temperature dependence, thermal throttling, and load-dependent voltage droop. They cannot establish stability, safe temperature, or total-system performance. In particular, adding CPU and GPU percentages does not produce a meaningful total-power figure without measured baseline power for each rail. Do not copy the extrapolated voltages into a device tree or set the profile to report unsupported clocks.

The requested targets require CPU +184 MHz (+9.13% over the live 2016 MHz maximum), GPU +100 MHz (+11.11% over 900 MHz), and DMC +136–144 MHz (+14.78–15.65% over 920 MHz). The table above estimates the effect if voltage were raised along a simplistic extrapolation of the last stock steps; it does not turn these targets into validated operating points. The available evidence provides no validated higher-voltage OPPs, so arithmetic cannot derive safe voltage values or prove stability.

Rockchip publishes an RK3562 `rk3562_ddr_1056MHz_ultra_v1.06.bin`, so 1056 MHz is a vendor DDR-bin target for some configurations. Rockchip's RK3562 configuration table lists distinct LP4 PCB templates, some rated 800 MHz and others 1333 MHz, and says the corresponding DDR-bin/configuration must match the board and memory package. The live CP20S model string only identifies LP4, not its DRAM part or a matching template. This makes a 1056 MHz candidate technically plausible, but does not prove that this CP20S memory and PCB can run it stably. No CP20S-specific 1056 MHz result or named 1064 MHz configuration was found. Rockchip's release history also records a suspend/wake data-corruption fix for an earlier 1056 MHz ultra binary; that is a reason to test suspend/resume and memory integrity on the exact board, not evidence that the current CP20S firmware is validated.

A read-only capture of the first 4 MiB of the CP20S eMMC user area contains a Rockchip DDR V1.04 build tag dated 2023-05-26 and a U-Boot SPL 2017.09 build dated 2023-09-11. It does not identify the LP4 package or its validated speed. The capture is retained at `work/cp20s-live-backup/oc-research/emmc-user-first-4m-20261018.bin`; it has not been modified or written back.

Before enabling any of these overclock targets, the project needs the exact CP20S DRAM part and PCB revision, a matching Rockchip DDR-bin configuration, maximum-frequency/eye-margin results, sustained memory testing including suspend/resume, and tested CPU/GPU voltage-frequency OPPs on this board. A regulator's allowable voltage range is not an OPP validation. The Extreme Performance entry retains stock CPU/GPU/DMC ceilings and uses adaptive stock OPPs; the requested overclock limits must not be presented as working just because the vendor tool can describe them.

Rollback: disable `cp20s-adaptive-governors.service`, restore `/etc/cpupower_gui.d/extreme-performance.profile` from `/var/lib/cp20s-adaptive-governors/backups/20261018/extreme-performance.profile.before`, and set CPU/GPU/DMC governors back to the values recorded in that backup directory's `live-settings.before` file.

Sources: [Rockchip RK3562 specification](https://www.rock-chips.com/a/en/products/RK35_Series/2024/0626/1983.html); [Rockchip Linux RK3562 device tree](https://github.com/rockchip-linux/kernel/blob/develop-6.1/arch/arm64/boot/dts/rockchip/rk3562.dtsi); [RK3562 clock driver](https://codebrowser.dev/linux/linux/drivers/clk/rockchip/clk-rk3562.c.html); [Rockchip RK3562 DDR firmware release notes](https://github.com/rockchip-linux/rkbin/blob/master/doc/release/RK3562_EN.md); [Rockchip PCB and DDR-bin configuration table](https://github.com/rockchip-linux/rkbin/blob/master/specific/Rockchip_Specific_PCB_Template_and_DDR_bin_Configuration_Table.md); [Rockchip DDR-bin tool guide](https://github.com/rockchip-linux/rkbin/blob/master/tools/ddrbin_tool_user_guide.txt); [Rockchip DMC driver](https://github.com/rockchip-linux/kernel/blob/develop-6.1/drivers/devfreq/rockchip_dmc.c).

All live ceilings above were read from this CP20S on Linux 6.1.172; other RK3562 boards can have different firmware, memory packages, and device-tree OPPs.
