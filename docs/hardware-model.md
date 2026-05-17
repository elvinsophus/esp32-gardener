# Hardware Model

## Logical Components

The controller has these logical components:

- Four moisture sensor inputs.
- Four valve outputs.
- One status LED chain.
- One optional beeper output.
- One optional local button.
- Wi-Fi, Home Assistant API, OTA, captive portal, and web server support.

## Current Pin Map

The current working device uses this mapping:

| Function | ESPHome ID | Current Pin | Notes |
| --- | --- | --- | --- |
| Beeper output | `beeper_out` | `GPIO1` | Inverted output, low-active beeper. |
| WS2812 LED chain | `status_leds` | `GPIO2` | 9 LEDs, GRB order. |
| Moisture sensor 1 | `sensor_1_v` | `GPIO3` | ADC input. ESPHome warns this is a strapping pin. |
| Moisture sensor 2 | `sensor_2_v` | `GPIO4` | ADC input. |
| Moisture sensor 3 | `sensor_3_v` | `GPIO5` | ADC input. |
| Moisture sensor 4 | `sensor_4_v` | `GPIO6` | ADC input. |
| Valve 1 | `valve_1` | `GPIO10` | GPIO switch output. |
| Valve 2 | `valve_2` | `GPIO9` | GPIO switch output. |
| Valve 3 | `valve_3` | `GPIO8` | GPIO switch output. |
| Valve 4 | `valve_4` | `GPIO7` | GPIO switch output. |
| Local button | `node_button` | `GPIO11` | Input pull-up, inverted. |

## LED Layout

The current LED chain has 9 LEDs:

| LED Index | Meaning |
| --- | --- |
| 0 | Board status. |
| 1 | Sensor 1 status. |
| 2 | Valve 1 status. |
| 3 | Sensor 2 status. |
| 4 | Valve 2 status. |
| 5 | Sensor 3 status. |
| 6 | Valve 3 status. |
| 7 | Sensor 4 status. |
| 8 | Valve 4 status. |

The pattern is:

```text
board, sensor_1, valve_1, sensor_2, valve_2, sensor_3, valve_3, sensor_4, valve_4
```

For `N` channels, this layout requires `1 + (N * 2)` LEDs. The current
four-channel device therefore needs 9 LEDs.

## Channel Constraints

Because the valve hardware uses four-channel MOSFET modules, channel count
should normally be a multiple of four. The current board has enough usable pins
for one four-channel bank:

```text
4 sensors + 4 valves = 8 channel pins
```

Future board profiles may support 8, 12, or more channels, but the current
device profile should remain explicit about being a four-channel implementation.

## Pin Selection Rules

When adding another device profile, choose pins using these rules:

- Sensor pins must support ADC input on the chosen ESP32 variant.
- Valve pins must be safe GPIO outputs for the attached MOSFET driver.
- Avoid boot strapping pins where possible.
- If a strapping pin is unavoidable, document the external circuitry and verify
  that it does not affect boot mode.
- Keep LED data output separate from noisy valve switching where practical.
- Preserve the logical channel order even if physical pins are routed in reverse.

