# Project Overview

## Purpose

Gardener is an ESPHome-based irrigation controller. It connects a profiled bank
of moisture sensors to a profiled bank of valves, then exposes telemetry,
controls, and status indicators to Home Assistant.

The current deployed device is working and should be treated as the reference
implementation while the project is made more generic.

## Current Device

The current device is named:

```yaml
esphome:
  name: esp32-s3-gardener-01
  friendly_name: ESP32 S3 Gardener 01
```

It is reachable on the local network at:

```text
192.168.42.141
```

The web server is enabled on port `80`, and OTA is configured through ESPHome.

## Design Direction

The controller logic should not be tied to one ESP32 model, one board revision,
or one deployed device name. The long-term shape should separate:

- Device identity: ESPHome node name, friendly name, network address.
- Board capabilities: ESP32 variant, flash, PSRAM, framework, available pins.
- Hardware mapping: sensor pins, valve pins, beeper pin, button pin, LED pin.
- Controller behavior: moisture thresholds, valve control, status display,
  beeper alerts, Home Assistant entities.

The original YAML remains as the first concrete reference device while shared
behavior is extracted into reusable packages. Channel count belongs to the
device profile, not the shared controller package.

## Channel Count

The current hardware uses four moisture sensors and four valves. Future boards
can describe a different channel count by changing the `channels:` list in their
profile.

## Non-Goals For The First Generic Pass

- Supporting boards that cannot provide the required ADC and GPIO pins.
- Changing the behavior of the already working `esp32-s3-gardener-01` device.
- Uploading firmware before validation and compile checks pass locally.
