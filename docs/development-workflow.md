# Development Workflow

## VS Code

Open this folder in VS Code:

```text
D:\elvin\Workspace\ESP32\Gardener
```

The workspace recommends and uses:

- ESPHome extension: `esphome.esphome-vscode`
- YAML extension: `redhat.vscode-yaml`
- Python extension: `ms-python.python`

The project selects:

```text
.venv\Scripts\python.exe
```

as the workspace Python interpreter.

## Device Config

The original reference config is:

```text
esp32-s3-gardener-01.yaml
```

The package-based config for new development is:

```text
esp32-s3-gardener-01.packaged.yaml
```

The real secrets file is:

```text
secrets.yaml
```

`secrets.yaml` is intentionally ignored by git.

## Common Commands

Validate the config:

```powershell
.\.venv\Scripts\python.exe -m esphome config .\esp32-s3-gardener-01.yaml
```

Validate the package-based config:

```powershell
.\.venv\Scripts\python.exe -m esphome config .\esp32-s3-gardener-01.packaged.yaml
```

Compile firmware:

```powershell
.\.venv\Scripts\python.exe -m esphome compile .\esp32-s3-gardener-01.yaml
```

Compile the package-based firmware:

```powershell
.\.venv\Scripts\python.exe -m esphome compile .\esp32-s3-gardener-01.packaged.yaml
```

Upload over OTA to the current device:

```powershell
.\.venv\Scripts\python.exe -m esphome upload .\esp32-s3-gardener-01.packaged.yaml --device 192.168.42.141
```

Start the local ESPHome dashboard:

```powershell
.\.venv\Scripts\python.exe -m esphome dashboard .
```

Then open:

```text
http://localhost:6052
```

## VS Code Tasks

Use `Terminal > Run Task...` for:

- `ESPHome: Validate gardener`
- `ESPHome: Validate gardener packaged`
- `ESPHome: Compile gardener`
- `ESPHome: Compile gardener packaged`
- `ESPHome: Upload gardener OTA`
- `ESPHome: Upload gardener packaged OTA`
- `ESPHome: Dashboard`

## Verification Rules

Before uploading to a functioning device:

1. Run validation.
2. Run compile.
3. Review the exact YAML changes.
4. Confirm the target IP.
5. Upload OTA only when the change is intentional.

The current known device IP is:

```text
192.168.42.141
```

The web server should answer on:

```text
http://192.168.42.141/
```

## Current Validation Notes

Both the original config and the package-based config validate and compile
locally with ESPHome `2026.4.5`.

Known non-blocking warnings:

- `GPIO3` is a strapping pin.
- `captive_portal` is enabled without a Wi-Fi fallback AP.
