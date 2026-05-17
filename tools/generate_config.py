#!/usr/bin/env python3
"""Generate an ESPHome YAML file from a small gardener hardware profile."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

DEFAULT_CONTROLLER_PACKAGE = "packages/gardener-controller.yaml"


def require_mapping(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a mapping")
    return value


def require_list(value: Any, name: str) -> list[Any]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{name} must be a non-empty list")
    return value


def as_substitution(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def load_profile(path: Path) -> dict[str, Any]:
    lines: list[tuple[int, str]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.split("#", 1)[0].rstrip()
        if not stripped:
            continue
        lines.append((len(stripped) - len(stripped.lstrip(" ")), stripped.lstrip(" ")))

    if not lines:
        raise ValueError(f"{path} is empty")

    profile, index = parse_block(lines, 0, lines[0][0])
    if index != len(lines):
        raise ValueError(f"Could not parse all of {path}")
    return require_mapping(profile, str(path))


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    if value == "true":
        return True
    if value == "false":
        return False
    if value.isdigit():
        return int(value)
    return value


def parse_key_value(content: str) -> tuple[str, Any]:
    if ":" not in content:
        raise ValueError(f"Expected key/value entry, got: {content}")
    key, value = content.split(":", 1)
    key = key.strip()
    value = value.strip()
    return key, parse_scalar(value) if value else None


def parse_block(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[Any, int]:
    if lines[index][1].startswith("- "):
        return parse_list(lines, index, indent)
    return parse_dict(lines, index, indent)


def parse_dict(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    while index < len(lines):
        line_indent, content = lines[index]
        if line_indent < indent:
            break
        if line_indent > indent:
            raise ValueError(f"Unexpected indentation near: {content}")
        if content.startswith("- "):
            break

        key, value = parse_key_value(content)
        index += 1
        if value is None:
            if index >= len(lines) or lines[index][0] <= indent:
                result[key] = {}
            else:
                value, index = parse_block(lines, index, lines[index][0])
                result[key] = value
        else:
            result[key] = value
    return result, index


def parse_list(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[list[Any], int]:
    result: list[Any] = []
    while index < len(lines):
        line_indent, content = lines[index]
        if line_indent < indent:
            break
        if line_indent > indent:
            raise ValueError(f"Unexpected indentation near: {content}")
        if not content.startswith("- "):
            break

        item_content = content[2:].strip()
        index += 1

        if not item_content:
            if index >= len(lines):
                result.append({})
            else:
                item, index = parse_block(lines, index, lines[index][0])
                result.append(item)
            continue

        if ":" in item_content:
            key, value = parse_key_value(item_content)
            item: dict[str, Any] = {key: value}
            if index < len(lines) and lines[index][0] > indent:
                child, index = parse_dict(lines, index, lines[index][0])
                item.update(child)
            result.append(item)
        else:
            result.append(parse_scalar(item_content))

    return result, index


def build_config(profile: dict[str, Any]) -> dict[str, Any]:
    device = require_mapping(profile.get("device"), "device")
    board = require_mapping(profile.get("board"), "board")
    hardware = require_mapping(profile.get("hardware"), "hardware")
    channels = require_list(profile.get("channels"), "channels")
    defaults = require_mapping(profile.get("defaults", {}), "defaults")

    device_name = device["name"]
    friendly_name = device.get("friendly_name", device_name)
    board_package = board["package"]
    controller_package = profile.get("controller_package", DEFAULT_CONTROLLER_PACKAGE)

    beeper = require_mapping(hardware.get("beeper"), "hardware.beeper")
    leds = require_mapping(hardware.get("leds"), "hardware.leds")
    button = require_mapping(hardware.get("button"), "hardware.button")

    substitutions: dict[str, str] = {
        "device_name": as_substitution(device_name),
        "friendly_name": as_substitution(friendly_name),
        "flash_size": as_substitution(board["flash_size"]),
        "channel_count": as_substitution(len(channels)),
        "led_count": as_substitution(leds["count"]),
        "pin_beeper": as_substitution(beeper["pin"]),
        "beeper_inverted": as_substitution(beeper.get("inverted", False)),
        "pin_leds": as_substitution(leds["pin"]),
        "pin_button": as_substitution(button["pin"]),
        "sensor_voltage_too_high": as_substitution(defaults.get("sensor_voltage_too_high", "3.")),
        "sensor_voltage_too_low": as_substitution(defaults.get("sensor_voltage_too_low", ".1")),
        "sensor_pct_critical": as_substitution(defaults.get("sensor_pct_critical", "15")),
        "main_led_brightness_default": as_substitution(defaults.get("main_led_brightness", "0.5")),
        "sensor_led_brightness_default": as_substitution(defaults.get("sensor_led_brightness", "0.5")),
        "dry_voltage_default": as_substitution(defaults.get("dry_voltage", "2.23")),
        "wet_voltage_default": as_substitution(defaults.get("wet_voltage", "0.86")),
        "breathing_min_brightness_default": as_substitution(defaults.get("breathing_min_brightness", "0.25")),
        "breathing_cycle_default": as_substitution(defaults.get("breathing_cycle", "4000")),
        "blink_cycle_default": as_substitution(defaults.get("blink_cycle", "250")),
        "slow_blink_cycle_default": as_substitution(defaults.get("slow_blink_cycle", "1000")),
    }

    sensor_reads: list[str] = []
    valve_reads: list[str] = []
    switches: list[dict[str, Any]] = []
    sensors: list[dict[str, Any]] = []

    for index, raw_channel in enumerate(channels, start=1):
        channel = require_mapping(raw_channel, f"channels[{index}]")
        sensor_id = f"sensor_{index}_v"
        valve_id = f"valve_{index}"
        sensor_pin_key = f"pin_sensor_{index}"
        valve_pin_key = f"pin_valve_{index}"

        substitutions[sensor_pin_key] = as_substitution(channel["sensor_pin"])
        substitutions[valve_pin_key] = as_substitution(channel["valve_pin"])
        sensor_reads.append(f"id({sensor_id}).state")
        valve_reads.append(f"id({valve_id}).state")

        switches.append(
            {
                "platform": "gpio",
                "id": valve_id,
                "name": f"Valve {index}",
                "pin": f"${{{valve_pin_key}}}",
                "restore_mode": "ALWAYS_OFF",
            }
        )

        sensor = {
            "platform": "adc",
            "id": sensor_id,
            "name": f"Moisture {index} - Voltage",
            "pin": f"${{{sensor_pin_key}}}",
            "attenuation": channel.get("attenuation", "12db"),
            "update_interval": channel.get("update_interval", "2s"),
            "filters": [
                {
                    "sliding_window_moving_average": {
                        "window_size": channel.get("window_size", 10),
                        "send_every": channel.get("send_every", 5),
                    }
                }
            ],
        }
        sensors.append(sensor)

    substitutions["sensor_value_reads"] = ", ".join(sensor_reads)
    substitutions["valve_state_reads"] = ", ".join(valve_reads)

    return {
        "wifi": {
            "ssid": "!secret wifi_ssid",
            "password": "!secret wifi_password",
        },
        "packages": {
            "board": f"!include {board_package}",
            "controller": f"!include {controller_package}",
        },
        "substitutions": substitutions,
        "switch": switches,
        "sensor": sensors,
    }


def write_config(config: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    header = "# Generated by tools/generate_config.py. Edit the profile, not this file.\n\n"
    output_path.write_text(header + render_config(config), encoding="utf-8")


def render_config(config: dict[str, Any]) -> str:
    substitutions = config["substitutions"]
    switches = config["switch"]
    sensors = config["sensor"]
    lines: list[str] = [
        "wifi:",
        "  ssid: !secret wifi_ssid",
        "  password: !secret wifi_password",
        "",
        "packages:",
        f"  board: !include {config['packages']['board'].removeprefix('!include ')}",
        f"  controller: !include {config['packages']['controller'].removeprefix('!include ')}",
        "",
        "substitutions:",
    ]

    for key, value in substitutions.items():
        lines.append(f"  {key}: {quote_substitution(value)}")

    lines.extend(["", "switch:"])
    for switch in switches:
        lines.extend(
            [
                "  - platform: gpio",
                f"    id: {switch['id']}",
                f"    name: {switch['name']}",
                f"    pin: {switch['pin']}",
                f"    restore_mode: {switch['restore_mode']}",
            ]
        )

    lines.extend(["", "sensor:"])
    for sensor in sensors:
        average = sensor["filters"][0]["sliding_window_moving_average"]
        lines.extend(
            [
                "  - platform: adc",
                f"    id: {sensor['id']}",
                f"    name: {sensor['name']}",
                f"    pin: {sensor['pin']}",
                f"    attenuation: {sensor['attenuation']}",
                f"    update_interval: {sensor['update_interval']}",
                "    filters:",
                "      - sliding_window_moving_average:",
                f"          window_size: {average['window_size']}",
                f"          send_every: {average['send_every']}",
            ]
        )

    return "\n".join(lines) + "\n"


def quote_substitution(value: str) -> str:
    if value in {"true", "false"}:
        return f'"{value}"'
    if value.startswith("id(") or ", id(" in value:
        return value
    if value.replace(".", "", 1).isdigit():
        return f'"{value}"'
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path, help="Path to a gardener profile YAML file")
    parser.add_argument("-o", "--output", type=Path, help="Generated ESPHome YAML path")
    args = parser.parse_args()

    profile = load_profile(args.profile)
    config = build_config(profile)
    device_name = config["substitutions"]["device_name"]
    output_path = args.output or Path(f"{device_name}.generated.yaml")
    write_config(config, output_path)
    print(output_path)


if __name__ == "__main__":
    main()
