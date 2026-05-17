# Project Overview

## Purpose

Gardener is an ESPHome-based irrigation controller. It connects a fixed-size
bank of moisture sensors to a fixed-size bank of valves, then exposes telemetry,
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

The current YAML can remain as the first concrete device instance while shared
behavior is extracted into reusable packages.

## Channel Count

The hardware is organized around four-channel MOSFET modules. That means the
natural expansion unit is four channels. The current ESP32 pin budget limits the
active implementation to exactly four moisture sensors and four valves.

The generic project should still describe channel count explicitly instead of
burying it in pin names or LED indexes. Even if the first reusable version is
limited to four channels, the config should make that constraint visible.

## Non-Goals For The First Generic Pass

- Automatically generating arbitrary numbers of ESPHome entities.
- Supporting boards that cannot provide the required ADC and GPIO pins.
- Changing the behavior of the already working `esp32-s3-gardener-01` device.
- Uploading firmware before validation and compile checks pass locally.

