# Configuration Strategy

## Goal

The project should move from a single monolithic YAML file to a small set of
device-specific files plus shared ESPHome packages.

The desired result is:

- Each physical device has a short top-level YAML file.
- Shared controller behavior lives in reusable package files.
- Board-specific pins and capabilities are declared in one place.
- Device identity is easy to rename without touching logic.

## Current File Shape

The project now has a first package-based split:

```text
packages/
  gardener-4ch-controller.yaml
boards/
  esp32-s3-octal-psram.yaml
esp32-s3-gardener-01.packaged.yaml
esp32-s3-gardener-01.yaml
```

`esp32-s3-gardener-01.yaml` is the original reference config.
`esp32-s3-gardener-01.packaged.yaml` is the package-based config to use for new
work.

The package names are intentionally conservative right now:

- `boards/esp32-s3-octal-psram.yaml` owns the board family settings.
- `packages/gardener-4ch-controller.yaml` owns shared four-channel controller
  behavior.
- `esp32-s3-gardener-01.packaged.yaml` owns identity, Wi-Fi secrets, pin map,
  LED count, and tuning defaults.

## Device File Responsibilities

A device YAML should own:

- `esphome.name`
- `esphome.friendly_name`
- Wi-Fi and OTA details that differ per device
- selected board profile
- selected pin map
- selected channel count
- optional per-device calibration defaults

Current direction:

```yaml
substitutions:
  device_name: esp32-s3-gardener-01
  friendly_name: ESP32 S3 Gardener 01
  channel_count: "4"
  led_count: "9"

  pin_beeper: GPIO1
  pin_leds: GPIO2
  pin_sensor_1: GPIO3
  pin_sensor_2: GPIO4
  pin_sensor_3: GPIO5
  pin_sensor_4: GPIO6
  pin_valve_1: GPIO10
  pin_valve_2: GPIO9
  pin_valve_3: GPIO8
  pin_valve_4: GPIO7
  pin_button: GPIO11
```

ESPHome substitutions are string-based, so they are best for values that are
known at compile time: names, pins, counts, and simple defaults.

## Shared Package Responsibilities

Shared packages should own:

- common logger, API, OTA, Wi-Fi conventions
- sensor entity definitions
- valve entity definitions
- LED status behavior
- beeper scripts
- thresholds and calibration controls
- interval logic

The current package refers to substitutions instead of hard-coded pins wherever
ESPHome supports it.

## Channel Count Reality

ESPHome YAML is declarative and does not have a general-purpose loop system for
creating entities. That means a fully dynamic channel count is not as simple as
setting `channel_count: 8`.

For the first generic version, prefer one of these practical approaches:

- Keep a four-channel package and make all names, pins, and LED count
  configurable.
- Later add separate packages for `4ch`, `8ch`, and so on if new hardware needs
  them.
- Avoid clever templating unless it clearly improves maintainability.

This keeps the working device safe while still removing the accidental coupling
to `esp32-s3-gardener-01`.

## Naming Conventions

Use stable internal IDs:

```text
sensor_1_v
sensor_2_v
valve_1
valve_2
status_leds
```

Use device-specific names only at the ESPHome node and friendly-name layer.
Entity names should remain generic unless Home Assistant requires more context.

Good:

```yaml
name: "Valve 1"
id: valve_1
```

Avoid:

```yaml
name: "ESP32 S3 Gardener 01 Valve 1"
id: esp32_s3_gardener_01_valve_1
```

## Migration Plan

1. Keep `esp32-s3-gardener-01.yaml` as the original reference.
2. Use `esp32-s3-gardener-01.packaged.yaml` for the generic implementation.
3. Extend substitutions when more values need to move out of shared logic.
4. Split `gardener-4ch-controller.yaml` into smaller packages when the file
   becomes hard to reason about.
5. Add another top-level device file when another board or pin map exists.
6. Revalidate and recompile before any OTA upload to the live device.
