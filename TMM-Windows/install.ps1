[CmdletBinding()]
param(
    [switch]$NoFirewallRule
)

$ErrorActionPreference = "Stop"
$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    throw "Run this installer from an elevated PowerShell window (Run as administrator)."
}

$source = Split-Path -Parent $MyInvocation.MyCommand.Path
$programDir = Join-Path $env:ProgramFiles "TMM"
$dataDir = Join-Path $env:ProgramData "TMM"
$configPath = Join-Path $dataDir "config.json"
$existingService = Get-Service -Name "TMM" -ErrorAction SilentlyContinue
$applicationFiles = @(
    "tmm_monitor.py", "tmm_profiles.py", "tmm_decode.py", "tmm_web_data.py",
    "tmm_web.py", "tmm_service.py", "tmm_tray.pyw", "tmm_installer_config.py",
    "tmm_verify_install.py",
    "config.example.json", "requirements.txt", "README.md", "VERSION"
)

# Build and verify a complete candidate before touching the running installation.
New-Item -ItemType Directory -Force -Path $dataDir, (Join-Path $dataDir "logs") | Out-Null
$updateStage = Join-Path $dataDir ("update-staging-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $updateStage | Out-Null
foreach ($file in $applicationFiles) {
    $sourceFile = Join-Path $source $file
    if (-not (Test-Path -LiteralPath $sourceFile -PathType Leaf)) {
        throw "Required update file missing: $sourceFile"
    }
    Copy-Item -LiteralPath $sourceFile -Destination (Join-Path $updateStage $file)
}
$staticSource = Join-Path $source "static"
if (-not (Test-Path -LiteralPath $staticSource -PathType Container)) {
    throw "Required static web directory missing: $staticSource"
}
Copy-Item -LiteralPath $staticSource -Destination (Join-Path $updateStage "static") -Recurse

$requiredWebFiles = @("static\index.html", "static\style.css", "static\app.js")
foreach ($file in $requiredWebFiles) {
    if (-not (Test-Path -LiteralPath (Join-Path $updateStage $file) -PathType Leaf)) {
        throw "Required staged web file missing: $file"
    }
}
$stagedFiles = @(Get-ChildItem -LiteralPath $updateStage -File -Recurse)
$stagedHashes = @{}
foreach ($file in $stagedFiles) {
    $relative = $file.FullName.Substring($updateStage.Length + 1)
    $stagedHashes[$relative] = (Get-FileHash -Algorithm SHA256 -LiteralPath $file.FullName).Hash
}

if ($existingService) {
    Stop-Service -Name "TMM" -Force -ErrorAction SilentlyContinue
    # Older development revisions stopped only the Python launcher and could
    # leave its runtime child alive. Remove only processes executing installed
    # TMM modules before replacing files or reopening COM/TCP/SQLite handles.
    Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
        Where-Object {$_.CommandLine -match [regex]::Escape((Join-Path $programDir "tmm_"))} |
        ForEach-Object {Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue}
    Start-Sleep -Seconds 5
}

New-Item -ItemType Directory -Force -Path $programDir | Out-Null
foreach ($relative in $stagedHashes.Keys) {
    $destination = Join-Path $programDir $relative
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $destination) | Out-Null
    Copy-Item -LiteralPath (Join-Path $updateStage $relative) -Destination $destination -Force
}
foreach ($relative in $stagedHashes.Keys) {
    $destination = Join-Path $programDir $relative
    if (-not (Test-Path -LiteralPath $destination -PathType Leaf)) {
        throw "Installed file missing after update: $destination"
    }
    $installedHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $destination).Hash
    if ($installedHash -ne $stagedHashes[$relative]) {
        throw "Installed file verification failed: $destination"
    }
}
Remove-Item -LiteralPath $updateStage -Recurse -Force
Write-Host "Application files copied and verified: $($stagedHashes.Count)"

if (-not (Test-Path $configPath)) {
    Copy-Item (Join-Path $source "config.example.json") $configPath
    Write-Host "Created $configPath. Set the correct COM port before production use."
} else {
    Write-Host "Existing configuration retained: $configPath"
}
# Refuse to start a service with malformed retained configuration.
Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json | Out-Null

$privatePython = Join-Path $programDir "runtime\python.exe"
$privatePythonw = Join-Path $programDir "runtime\pythonw.exe"
$venvRoot = Join-Path $programDir ".venv"
$venvPython = Join-Path $venvRoot "Scripts\python.exe"
$venvPythonw = Join-Path $venvRoot "Scripts\pythonw.exe"
$usingPrivateRuntime = Test-Path -LiteralPath $privatePython -PathType Leaf

if ($usingPrivateRuntime) {
    if (-not (Test-Path -LiteralPath $privatePythonw -PathType Leaf)) {
        throw "Private TMM runtime is incomplete: $privatePythonw is missing."
    }
    $servicePython = $privatePython
    $trayPython = $privatePythonw
    Write-Host "Using existing private TMM runtime: $privatePython"
} else {
    if (-not (Test-Path -LiteralPath $venvPython -PathType Leaf)) {
        $launcher = Get-Command py -ErrorAction SilentlyContinue
        if (-not $launcher) {
            throw "No private TMM runtime or Python launcher was found. Use the compiled installer for a self-contained installation."
        }
        & $launcher.Source -3 -m venv $venvRoot
        if ($LASTEXITCODE -ne 0) { throw "Python virtual environment creation failed." }
    }
    $servicePython = $venvPython
    $trayPython = $venvPythonw
    & $servicePython -m pip install --disable-pip-version-check --upgrade pip
    # TMM requires binary Windows packages. Do not silently attempt a local
    # native build (for example an incompatible Pillow requiring zlib headers).
    & $servicePython -m pip install --disable-pip-version-check --only-binary=:all: -r (Join-Path $programDir "requirements.txt")
    if ($LASTEXITCODE -ne 0) {
        throw "Python dependency installation failed: no compatible Windows wheel is available for this Python version or architecture."
    }

    # pythonservice.exe runs as LocalSystem and cannot rely on the installing
    # user's Python registry or DLL search path.
    $basePrefix = (& $servicePython -c "import sys; print(sys.base_prefix)").Trim()
    $pywin32DllDir = Join-Path $venvRoot "Lib\site-packages\pywin32_system32"
    Get-ChildItem -Path $pywin32DllDir -Filter "*.dll" | Copy-Item -Destination $venvRoot -Force
    Get-ChildItem -Path $basePrefix -Filter "python*.dll" | Copy-Item -Destination $venvRoot -Force
}

if ($existingService) {
    & $servicePython (Join-Path $programDir "tmm_service.py") --startup auto update
} else {
    & $servicePython (Join-Path $programDir "tmm_service.py") --startup auto install
}
if ($LASTEXITCODE -ne 0) {
    throw "Windows Service registration failed."
}
sc.exe failure TMM "reset= 86400" "actions= restart/5000/restart/15000/restart/60000" | Out-Null
sc.exe failureflag TMM 1 | Out-Null

# Run the per-user tray controller at interactive logon. The monitor service
# remains independent and continues to run when no user is signed in.
$startupDir = [Environment]::GetFolderPath("Startup")
$trayShortcut = Join-Path $startupDir "Toshiba Modbus Monitor.lnk"
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($trayShortcut)
$shortcut.TargetPath = $trayPython
$shortcut.Arguments = '"' + (Join-Path $programDir "tmm_tray.pyw") + '"'
$shortcut.WorkingDirectory = $programDir
$shortcut.Description = "Toshiba Modbus Monitor tray controller"
$shortcut.Save()

# Start the tray immediately in the installing user's session.
Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
    Where-Object {$_.CommandLine -match [regex]::Escape((Join-Path $programDir "tmm_tray.pyw"))} |
    ForEach-Object {Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue}
Start-Process -FilePath $trayPython `
    -ArgumentList ('"' + (Join-Path $programDir "tmm_tray.pyw") + '"') `
    -WorkingDirectory $programDir

if (-not $NoFirewallRule) {
    $ruleName = "Toshiba Modbus Monitor Web"
    if (-not (Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue)) {
        New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8080 -Profile Private | Out-Null
    }
}

try {
    Start-Service -Name "TMM"
} catch {
    Write-Host "TMM could not be started. Recent Service Control Manager events:" -ForegroundColor Red
    Get-WinEvent -FilterHashtable @{LogName = "System"; StartTime = (Get-Date).AddMinutes(-5)} -ErrorAction SilentlyContinue |
        Where-Object {$_.ProviderName -eq "Service Control Manager" -and $_.Message -match "TMM|Toshiba Modbus Monitor"} |
        Select-Object TimeCreated, Id, LevelDisplayName, Message |
        Format-List
    throw
}
$webPort = (Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json).web.port
$deadline = (Get-Date).AddSeconds(30)
$verified = $false
do {
    try {
        $health = Invoke-RestMethod -Uri "http://127.0.0.1:$webPort/api/v1/health" -TimeoutSec 3
        $appJs = Invoke-WebRequest -Uri "http://127.0.0.1:$webPort/static/app.js" -UseBasicParsing -TimeoutSec 3
        if ($health.database -and $appJs.StatusCode -eq 200 -and $appJs.Content.Length -gt 1000) {
            $verified = $true
            break
        }
    } catch {
        Start-Sleep -Seconds 1
    }
} while ((Get-Date) -lt $deadline)
if (-not $verified) {
    throw "TMM started, but the API/static-file self-test did not succeed within 30 seconds. Check the service logs."
}
Write-Host "Toshiba Modbus Monitor was installed."
Write-Host "Post-install self-test: API and web assets are available."
Write-Host "Configuration: $configPath"
Write-Host "Service:       Get-Service TMM"
Write-Host "Dashboard:     http://localhost:8080/"
