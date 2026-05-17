# Configuration Strategy

## Goal

The project should move from a single monolithic YAML file to a small
device-specific profile plus shared ESPHome packages.

The desired result is:

- Each physical device has a short profile YAML file.
- A preparation step generates the ESPHome YAML used for validation, compile,
  and upload.
- Shared controller behavior lives in reusable package files.
- Board-specific pins and capabilities are declared in one place.
- Device identity is easy to rename without touching logic.

## Current File Shape

The project now has a first package-based split:

```text
packages/
  gardener-controller.yaml
boards/
  esp32-s3-octal-psram.yaml
profiles/
  esp32-s3-gardener-01.yaml
tools/
  generate_config.py
  deploy.ps1
esp32-s3-gardener-01.generated.yaml
esp32-s3-gardener-01.yaml
```

`esp32-s3-gardener-01.yaml` is the original reference config.
`profiles/esp32-s3-gardener-01.yaml` is the human-authored device profile.
`esp32-s3-gardener-01.generated.yaml` is generated and used by ESPHome.

The package names are intentionally conservative right now:

- `profiles/esp32-s3-gardener-01.yaml` owns only specific values for the
  current board: identity, board package, pins, channel mappings, LED count, and
  defaults.
- `boards/esp32-s3-octal-psram.yaml` owns the board family settings.
- `packages/gardener-controller.yaml` owns shared controller behavior.
- `tools/generate_config.py` expands the profile into ESPHome component YAML.
- `tools/deploy.ps1` runs generation before ESPHome validation, compile, or
  upload.

## Device File Responsibilities

A device profile should own:

- ESPHome node name
- friendly name
- selected board profile
- selected pin map
- selected channel count
- optional per-device calibration defaults

Current direction:

```yaml
device:
  name: esp32-s3-gardener-01
  friendly_name: ESP32 S3 Gardener 01

board:
  package: boards/esp32-s3-octal-psram.yaml
  flash_size: 8MB

hardware:
  leds:
    pin: GPIO2
    count: 9

channels:
  - sensor_pin: GPIO3
    valve_pin: GPIO10
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
creating entities. That means the preparation step generates the repeated
`switch:` and `sensor:` declarations from `channels:`.

The shared package does not declare channel-specific sensors or valve switches.
Those entities live in the generated YAML. The generator also supplies C++ read
lists for the shared status and alert logic:

```yaml
substitutions:
  channel_count: "4"
  sensor_value_reads: "id(sensor_1_v).state, id(sensor_2_v).state, id(sensor_3_v).state, id(sensor_4_v).state"
  valve_state_reads: "id(valve_1).state, id(valve_2).state, id(valve_3).state, id(valve_4).state"
```

This keeps the shared package independent of a specific channel count while the
authored profile stays small.

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
2. Edit `profiles/esp32-s3-gardener-01.yaml` for the current board profile.
3. Run `.\tools\deploy.ps1 -Action config` before compile or upload.
4. Split `gardener-controller.yaml` into smaller packages when the file
   becomes hard to reason about.
5. Add another top-level device file when another board or pin map exists.
6. Revalidate and recompile before any OTA upload to the live device.
