# Gardener ESPHome Workspace

This project contains ESPHome configuration for a Wi-Fi connected irrigation
controller. The current working device is `esp32-s3-gardener-01`, but the goal is
to evolve the configuration into a reusable controller template where device
identity, board type, pins, and LED layout are supplied by each device instance.

Start with these docs:

- [Project Overview](docs/project-overview.md)
- [Hardware Model](docs/hardware-model.md)
- [Configuration Strategy](docs/configuration-strategy.md)
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

The generic/package-based version is:

```text
esp32-s3-gardener-01.packaged.yaml
```

Use the packaged config for new work unless you are comparing against the
original reference.

## Useful commands

Validate a config:

```powershell
.\.venv\Scripts\python.exe -m esphome config .\esp32-s3-gardener-01.packaged.yaml
```

Compile firmware:

```powershell
.\.venv\Scripts\python.exe -m esphome compile .\esp32-s3-gardener-01.packaged.yaml
```

Upload over OTA:

```powershell
.\.venv\Scripts\python.exe -m esphome upload .\esp32-s3-gardener-01.packaged.yaml --device 192.168.42.141
```

Open the local ESPHome dashboard:

```powershell
.\.venv\Scripts\python.exe -m esphome dashboard .
```

Then browse to `http://localhost:6052`.
