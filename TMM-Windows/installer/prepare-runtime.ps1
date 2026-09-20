[CmdletBinding()]
param(
    [string]$PythonVersion = "3.14",
    [string]$RequiredPythonVersion = "3.14.7",
    [string]$PythonExe,
    [switch]$ReuseInstalledPackages,
    [switch]$RefreshWheels
)

$ErrorActionPreference = "Stop"
$installerDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Split-Path -Parent $installerDir
$stagingDir = Join-Path $installerDir "staging"
$runtimeDir = Join-Path $stagingDir "runtime"
$workDir = Join-Path $installerDir "work"
$wheelDir = Join-Path $workDir "wheels"
$requirements = Join-Path $projectDir "requirements.txt"

if (-not (Test-Path $requirements)) {
    throw "Requirements file not found: $requirements"
}

if ($PythonExe) {
    $pythonExe = [IO.Path]::GetFullPath($PythonExe)
    if (-not (Test-Path -LiteralPath $pythonExe -PathType Leaf)) {
        throw "The supplied Python executable does not exist: $pythonExe"
    }
} else {
    $launcher = Get-Command py -ErrorAction SilentlyContinue
    if ($launcher) {
        $pythonExe = (& $launcher.Source "-$PythonVersion" -c "import sys; print(sys.executable)").Trim()
        if ($LASTEXITCODE -ne 0) { $pythonExe = "" }
    }

    if (-not $pythonExe) {
        $candidates = @(
            (Join-Path ${env:ProgramFiles} "Python314\python.exe"),
            (Join-Path ${env:LocalAppData} "Programs\Python\Python314\python.exe"),
            (Join-Path ${env:ProgramFiles} "TMM\runtime\python.exe")
        )
        $commandPython = Get-Command python -ErrorAction SilentlyContinue
        if ($commandPython) { $candidates += $commandPython.Source }
        $pythonExe = $candidates | Where-Object {
            $_ -and (Test-Path -LiteralPath $_ -PathType Leaf)
        } | Select-Object -First 1
    }
}

if (-not $pythonExe -or -not (Test-Path -LiteralPath $pythonExe -PathType Leaf)) {
    throw "Python $RequiredPythonVersion x64 was not found. Install it with the Python launcher, or run .\installer\prepare-runtime.ps1 -PythonExe 'C:\Path\python.exe'."
}
$pythonInfo = & $pythonExe -c "import json,platform,sys; print(json.dumps({'version':platform.python_version(),'machine':platform.machine(),'base_prefix':sys.base_prefix}))"
$info = $pythonInfo | ConvertFrom-Json
if ($info.version -ne $RequiredPythonVersion) {
    throw "Expected Python $RequiredPythonVersion, found $($info.version) at $pythonExe."
}
if ($info.machine -notmatch "AMD64|x86_64") {
    throw "The runtime must be built from 64-bit x64 Python; found $($info.machine)."
}
$basePrefix = [IO.Path]::GetFullPath([string]$info.base_prefix)
if (-not (Test-Path (Join-Path $basePrefix "python.exe"))) {
    throw "Invalid Python base directory: $basePrefix"
}

New-Item -ItemType Directory -Force -Path $stagingDir, $workDir, $wheelDir | Out-Null
if ($RefreshWheels) {
    Get-ChildItem -LiteralPath $wheelDir -File -ErrorAction SilentlyContinue |
        Remove-Item -Force
}

if (-not $ReuseInstalledPackages) {
    Write-Host "Downloading pinned binary wheels..."
    & $pythonExe -m pip download --disable-pip-version-check --only-binary=:all: `
        --dest $wheelDir --requirement $requirements
    if ($LASTEXITCODE -ne 0) {
        throw "Could not create the offline wheel cache. Check internet/proxy access, or use -ReuseInstalledPackages with an already working TMM runtime."
    }
} else {
    Write-Host "Offline mode: reusing packages from $basePrefix"
}

$candidateDir = Join-Path $stagingDir ("runtime.build-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $candidateDir | Out-Null

Write-Host "Copying Python $RequiredPythonVersion runtime..."
if ($ReuseInstalledPackages) {
    & robocopy.exe $basePrefix $candidateDir /E /R:2 /W:1 /NFL /NDL /NJH /NJS /NP `
        /XD (Join-Path $basePrefix "Lib\test") `
        /XF "*.pyc"
} else {
    & robocopy.exe $basePrefix $candidateDir /E /R:2 /W:1 /NFL /NDL /NJH /NJS /NP `
        /XD (Join-Path $basePrefix "Lib\site-packages") (Join-Path $basePrefix "Lib\test") `
        /XF "*.pyc"
}
if ($LASTEXITCODE -gt 7) {
    throw "Python runtime copy failed with robocopy exit code $LASTEXITCODE."
}
if (-not $ReuseInstalledPackages) {
    New-Item -ItemType Directory -Force -Path (Join-Path $candidateDir "Lib\site-packages") | Out-Null
    Write-Host "Installing TMM dependencies from the offline wheel cache..."
    & $pythonExe -m pip install --disable-pip-version-check --no-index --only-binary=:all: `
        --find-links $wheelDir --target (Join-Path $candidateDir "Lib\site-packages") `
        --requirement $requirements
    if ($LASTEXITCODE -ne 0) {
        throw "Could not install dependencies into the private runtime."
    }
}

# pywin32 service DLLs must be resolvable before site initialization when the
# service runs as LocalSystem. Keep them beside python.exe and pythonservice.exe.
$pywin32System = Join-Path $candidateDir "Lib\site-packages\pywin32_system32"
Get-ChildItem -LiteralPath $pywin32System -Filter "*.dll" | Copy-Item -Destination $candidateDir -Force
$pythonServicePath = Join-Path $candidateDir "pythonservice.exe"
if (-not (Test-Path -LiteralPath $pythonServicePath -PathType Leaf)) {
    $pythonService = Get-ChildItem -LiteralPath (Join-Path $candidateDir "Lib\site-packages") `
        -Filter "pythonservice.exe" -Recurse | Select-Object -First 1
    if ($pythonService) {
        Copy-Item -LiteralPath $pythonService.FullName -Destination $pythonServicePath -Force
    }
}
if (-not (Test-Path -LiteralPath $pythonServicePath -PathType Leaf)) {
    throw "pywin32 did not provide pythonservice.exe."
}

$candidatePython = Join-Path $candidateDir "python.exe"
$env:PYTHONNOUSERSITE = "1"
& $candidatePython -c "import tkinter; t=tkinter.Tcl(); import serial,fastapi,uvicorn,psutil,win32service,PIL,pystray; print('runtime-ok', t.eval('info patchlevel'))"
if ($LASTEXITCODE -ne 0) {
    throw "Private runtime import/self-test failed."
}
$requirementsCheck = "import importlib.metadata as m, pathlib, sys; requirements=[line.strip() for line in pathlib.Path(sys.argv[1]).read_text(encoding='utf-8').splitlines() if line.strip() and not line.lstrip().startswith('#')]; mismatches=[item for item in requirements if '==' in item and m.version(item.partition('==')[0]) != item.partition('==')[2]]; print('requirements-ok' if not mismatches else 'version mismatch: ' + '; '.join(mismatches)); sys.exit(bool(mismatches))"
& $candidatePython -c $requirementsCheck $requirements
if ($LASTEXITCODE -ne 0) {
    throw "Private runtime dependency versions do not match requirements.txt."
}

if (Test-Path $runtimeDir) {
    $backup = Join-Path $stagingDir ("runtime.previous-" + (Get-Date -Format "yyyyMMdd-HHmmss"))
    Move-Item -LiteralPath $runtimeDir -Destination $backup
    Write-Host "Previous runtime retained at $backup"
}
Move-Item -LiteralPath $candidateDir -Destination $runtimeDir

$manifest = [ordered]@{
    python_version = $RequiredPythonVersion
    architecture = "x64"
    created_at = (Get-Date).ToUniversalTime().ToString("o")
    requirements_sha256 = (Get-FileHash -Algorithm SHA256 $requirements).Hash.ToLowerInvariant()
    package_source = $(if ($ReuseInstalledPackages) { "existing-runtime" } else { "offline-wheel-cache" })
    wheels = @(Get-ChildItem -LiteralPath $wheelDir -File | Sort-Object Name | ForEach-Object {
        [ordered]@{name=$_.Name; sha256=(Get-FileHash -Algorithm SHA256 $_.FullName).Hash.ToLowerInvariant()}
    })
}
$manifest | ConvertTo-Json -Depth 4 | Set-Content -Encoding UTF8 (Join-Path $runtimeDir "TMM-RUNTIME-MANIFEST.json")

Write-Host "Private TMM runtime prepared: $runtimeDir"
Write-Host "Offline wheels cached:        $wheelDir"
