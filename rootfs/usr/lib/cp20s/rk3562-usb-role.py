#!/usr/bin/python3
"""Keep the CP20S USB-C controller in device/peripheral mode.

The service intentionally never requests USB host mode. Review the paths and
confirm the hardware before enabling it on another RK3562 board.
"""
import logging
import os
import time

PHY_MODE = "/sys/devices/platform/ff740000.usb2-phy/otg_mode"
DWC3_MODE = "/sys/kernel/debug/usb/fe500000.usb/mode"

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("rk3562-usb-role")


def enforce(path, expected):
    if not os.path.exists(path):
        return None
    with open(path, encoding="ascii") as control:
        actual = control.read().strip()
    if actual != expected:
        with open(path, "w", encoding="ascii") as control:
            control.write(expected + "\n")
        with open(path, encoding="ascii") as control:
            actual = control.read().strip()
    return actual


def main():
    while not os.path.exists(PHY_MODE):
        time.sleep(1)
    last_state = None
    last_error = None
    while True:
        try:
            state = (enforce(PHY_MODE, "peripheral"),
                     enforce(DWC3_MODE, "device"))
            if state != last_state:
                log.info("USB-C device policy: PHY=%s DWC3=%s", *state)
                last_state = state
            last_error = None
        except OSError as error:
            if error != last_error:
                log.error("Could not enforce USB-C device mode; retrying: %s", error)
                last_error = error
        time.sleep(2)


if __name__ == "__main__":
    main()
