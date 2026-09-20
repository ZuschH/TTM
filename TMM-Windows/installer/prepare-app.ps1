[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$installerDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Split-Path -Parent $installerDir
$stagingDir = Join-Path $installerDir "staging"
$runtimeDir = Join-Path $stagingDir "runtime"
$appDir = Join-Path $stagingDir "app"
$runtimePython = Join-Path $runtimeDir "python.exe"

if (-not (Test-Path $runtimePython)) {
    throw "Private runtime missing. Run installer\prepare-runtime.ps1 first."
}

$applicationFiles = @(
    "tmm_monitor.py",
    "tmm_profiles.py",
    "tmm_decode.py",
    "tmm_web_data.py",
    "tmm_web.py",
    "tmm_service.py",
    "tmm_tray.pyw",
    "tmm_installer_config.py",
    "tmm_verify_install.py",
    "config.example.json",
    "requirements.txt",
    "README.md",
    "VERSION"
)

$candidateDir = Join-Path $stagingDir ("app.build-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $candidateDir | Out-Null

foreach ($file in $applicationFiles) {
    $source = Join-Path $projectDir $file
    if (-not (Test-Path $source -PathType Leaf)) {
        throw "Required application file missing: $source"
    }
    Copy-Item -LiteralPath $source -Destination (Join-Path $candidateDir $file)
}

$staticSource = Join-Path $projectDir "static"
if (-not (Test-Path $staticSource -PathType Container)) {
    throw "Static web directory missing: $staticSource"
}
Copy-Item -LiteralPath $staticSource -Destination (Join-Path $candidateDir "static") -Recurse

$requiredAssets = @(
    "static\index.html",
    "static\style.css",
    "static\app.js",
    "static\tmm-product-mark.png",
    "static\tmm-tray-16-healthy.png",
    "static\tmm-tray-16-warning.png",
    "static\tmm-tray-16-error.png",
    "static\tmm-tray-16-stopped.png"
)
foreach ($asset in $requiredAssets) {
    if (-not (Test-Path (Join-Path $candidateDir $asset) -PathType Leaf)) {
        throw "Required staged asset missing: $asset"
    }
}

Write-Host "Validating staged application with the private runtime..."
& $runtimePython -m py_compile `
    (Join-Path $candidateDir "tmm_monitor.py") `
    (Join-Path $candidateDir "tmm_profiles.py") `
    (Join-Path $candidateDir "tmm_decode.py") `
    (Join-Path $candidateDir "tmm_web_data.py") `
    (Join-Path $candidateDir "tmm_web.py") `
    (Join-Path $candidateDir "tmm_service.py") `
    (Join-Path $candidateDir "tmm_tray.pyw") `
    (Join-Path $candidateDir "tmm_installer_config.py") `
    (Join-Path $candidateDir "tmm_verify_install.py")
if ($LASTEXITCODE -ne 0) {
    throw "Staged Python application failed compilation."
}

& $runtimePython -c "import json,pathlib,sys; json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))" `
    (Join-Path $candidateDir "config.example.json")
if ($LASTEXITCODE -ne 0) {
    throw "Staged example configuration is invalid."
}

Get-ChildItem -LiteralPath $candidateDir -Filter "__pycache__" -Directory -Recurse |
    Remove-Item -Recurse -Force

$manifestFiles = @(Get-ChildItem -LiteralPath $candidateDir -File -Recurse | Sort-Object FullName | ForEach-Object {
    $relative = $_.FullName.Substring($candidateDir.Length + 1).Replace("\", "/")
    [ordered]@{
        path = $relative
        size = $_.Length
        sha256 = (Get-FileHash -Algorithm SHA256 $_.FullName).Hash.ToLowerInvariant()
    }
})
$manifest = [ordered]@{
    product = "Toshiba Modbus Monitor"
    version = (Get-Content -LiteralPath (Join-Path $candidateDir "VERSION") -Raw).Trim()
    created_at = (Get-Date).ToUniversalTime().ToString("o")
    files = $manifestFiles
}
$manifest | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 `
    (Join-Path $candidateDir "TMM-APP-MANIFEST.json")

if (Test-Path $appDir) {
    $backup = Join-Path $stagingDir ("app.previous-" + (Get-Date -Format "yyyyMMdd-HHmmss"))
    Move-Item -LiteralPath $appDir -Destination $backup
    Write-Host "Previous application staging retained at $backup"
}
Move-Item -LiteralPath $candidateDir -Destination $appDir

Write-Host "TMM application staging prepared: $appDir"
Write-Host "Files in manifest: $($manifestFiles.Count)"
