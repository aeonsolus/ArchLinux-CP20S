# GNOME tablet profile

## Intended configuration

The target is GNOME Shell 51 on Wayland, with the regular panel and system tray available, TouchUp for edge gestures, and a conventional keyboard-and-pointer desktop when a Bluetooth keyboard is connected. Do not add a persistent navigation bar.

GNOME Shell extensions render through Mutter/Shell; they do not have a separate GPU acceleration switch. Smooth gestures depend on Mutter using Mesa/Panfrost on the CP20S. Validate the live renderer and frame behavior rather than labeling an extension itself “accelerated.”

## Required extensions

- **TouchUp** — primary gesture layer; verify invisible gesture mode and edge conflicts.
- **TouchBoard** — default touchscreen keyboard and a release gate. Do not silently replace it with Squeekboard. If the available GNOME integration cannot provide a docked touch keyboard, the release remains blocked rather than shipping a misleading fallback.
- **Maximize Window Into New Workspace** — optional; test dialogs and transient windows before enabling by default.
- **AppIndicator/KStatusNotifierItem support** — optional tray integration for compatible applications.
- **Dash to Dock** — optional appearance/launcher feature.

Pin extension UUIDs and versions per GNOME release. Enable only the selected profile and check Shell logs after installation or upgrade.

## TouchBoard acceptance

Verify that TouchBoard docks at the bottom and behaves as a tablet keyboard, opens for text fields and can be summoned manually, has a usable tablet-sized footprint, and remains responsive after dismissal/reopen. Test typing in GNOME Settings, Chrome, and an Electron app with both touchscreen and physical keyboard attached. The keyboard must not disappear permanently when a physical keyboard connects, and extensions must not duplicate text input or volume actions.

## Release checks

Test touch gestures, overview and app-grid animation, tray menus, workspace behavior, keyboard popup/docking, rotation, display scaling, lock/suspend/resume, and Shell logs. Confirm Panfrost/Mutter GBM rendering on the running tablet. A working DRM node alone is not proof of hardware rendering.
