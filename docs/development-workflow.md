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

The profile for new development is:

```text
profiles\esp32-s3-gardener-01.yaml
```

The generated ESPHome config is:

```text
esp32-s3-gardener-01.generated.yaml
```

Do not edit the generated file directly. Regenerate it from the profile.

The real secrets file is:

```text
secrets.yaml
```

`secrets.yaml` is intentionally ignored by git.

## Common Commands

Validate the config:

```powershell
.\tools\deploy.ps1 -Action config
```

Compile firmware:

```powershell
.\tools\deploy.ps1 -Action compile
```

Upload over OTA to the current device:

```powershell
.\tools\deploy.ps1 -Action upload -Device 192.168.42.141
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

- `Gardener: Generate ESPHome config`
- `ESPHome: Validate generated gardener`
- `ESPHome: Compile generated gardener`
- `ESPHome: Upload generated gardener OTA`
- `ESPHome: Validate original reference`
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

The generated config is intended to validate and compile locally with ESPHome
`2026.4.5`.

Known non-blocking warnings:

- `GPIO3` is a strapping pin.
- `captive_portal` is enabled without a Wi-Fi fallback AP.
