param(
    [string]$Profile = ".\profiles\esp32-s3-gardener-01.yaml",
    [ValidateSet("generate", "config", "compile", "upload")]
    [string]$Action = "config",
    [string]$Device = "192.168.42.141"
)

$ErrorActionPreference = "Stop"

function Test-Python {
    param([string]$Python)
    if (-not (Test-Path $Python)) {
        return $false
    }

    try {
        & $Python --version *> $null
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

$ProjectPython = ".\.venv\Scripts\python.exe"
$GeneratorPython = @($ProjectPython)
if (-not (Test-Python $ProjectPython)) {
    $GeneratorPython = @("py", "-3")
}

$GeneratorArgs = @()
if ($GeneratorPython.Length -gt 1) {
    $GeneratorArgs = $GeneratorPython[1..($GeneratorPython.Length - 1)]
}

$Generated = & $GeneratorPython[0] @GeneratorArgs ".\tools\generate_config.py" $Profile
$Generated = $Generated.Trim()

if ($Action -eq "generate") {
    Write-Host "Generated $Generated"
    exit 0
}

if (-not (Test-Python $ProjectPython)) {
    throw "The project virtual environment Python is missing or broken. Recreate .venv before running ESPHome actions."
}

$EspHomeArgs = @("-m", "esphome", $Action, $Generated)
if ($Action -eq "upload") {
    $EspHomeArgs += @("--device", $Device)
}

& $ProjectPython @EspHomeArgs
