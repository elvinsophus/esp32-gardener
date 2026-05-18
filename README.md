# Gardener ESPHome Workspace

This project contains ESPHome configuration for a Wi-Fi connected irrigation
controller. The current working device is `esp32-s3-gardener-01`, but the goal is
to evolve the configuration into a reusable controller template where device
identity, board type, pins, and LED layout are supplied by each device instance.

Start with these docs:

- [Project Overview](docs/project-overview.md)
- [Hardware Model](docs/hardware-model.md)
- [Configuration Strategy](docs/configuration-strategy.md)
- [Beeper Patterns](docs/beeper-patterns.md)
- [Development Workflow](docs/development-workflow.md)

## Local setup

This workspace already uses a local virtual environment at `.venv`. If you need
to recreate it:

```powershell
$python = "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"
& $python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip wheel esphome
.\.venv\Scripts\python.exe -m esphome version
```

If PowerShell blocks activation, run this once for the current user:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Migrating an existing device

Copy the existing ESPHome YAML files into this directory. Common files are:

- `<device-name>.yaml`
- `secrets.yaml`
- any files referenced with `!include`

`secrets.yaml` is ignored by git because it normally contains Wi-Fi credentials, API keys, and OTA passwords.

The original Home Assistant export is kept as the reference config:

```text
esp32-s3-gardener-01.yaml
```

The generic version is generated from the device profile:

```text
profiles/esp32-s3-gardener-01.yaml
esp32-s3-gardener-01.generated.yaml
```

Edit the profile for board-specific values. The generated YAML is a local build
artifact used by ESPHome and is ignored by git.

## Useful commands

Validate a config:

```powershell
.\tools\deploy.ps1 -Action config
```

Compile firmware:

```powershell
.\tools\deploy.ps1 -Action compile
```

Upload over OTA:

```powershell
.\tools\deploy.ps1 -Action upload -Device 192.168.42.141
```

Open the local ESPHome dashboard:

```powershell
.\.venv\Scripts\python.exe -m esphome dashboard .
```

Then browse to `http://localhost:6052`.
