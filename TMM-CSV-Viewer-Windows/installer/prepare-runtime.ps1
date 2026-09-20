[CmdletBinding()]
param(
    [string]$PythonExe = (Join-Path ${env:ProgramFiles} "TMM\runtime\python.exe")
)

$ErrorActionPreference = "Stop"
$installerDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$runtimeDir = Join-Path $installerDir "staging\runtime"

if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
    throw "Python runtime not found: $PythonExe. Pass -PythonExe <path-to-python.exe>."
}
$info = & $PythonExe -c "import json,platform,sys; print(json.dumps({'version':platform.python_version(),'machine':platform.machine(),'base_prefix':sys.base_prefix}))" | ConvertFrom-Json
if ($LASTEXITCODE -ne 0 -or $info.machine -notmatch "AMD64|x86_64") {
    throw "A working 64-bit Python runtime is required."
}
$basePrefix = [IO.Path]::GetFullPath([string]$info.base_prefix)
if (-not (Test-Path -LiteralPath (Join-Path $basePrefix "pythonw.exe") -PathType Leaf)) {
    throw "The selected runtime has no pythonw.exe: $basePrefix"
}

$candidate = Join-Path $installerDir ("staging\runtime.build-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $candidate | Out-Null
& robocopy.exe $basePrefix $candidate /E /R:2 /W:1 /NFL /NDL /NJH /NJS /NP /XD (Join-Path $basePrefix "Lib\test") /XF "*.pyc"
if ($LASTEXITCODE -gt 7) { throw "Python runtime copy failed with robocopy exit code $LASTEXITCODE." }
& (Join-Path $candidate "python.exe") -c "import http.server, pathlib, tkinter; print('viewer-runtime-ok')"
if ($LASTEXITCODE -ne 0) { throw "Copied viewer runtime failed its self-test." }
if (Test-Path $runtimeDir) { Move-Item -LiteralPath $runtimeDir -Destination (Join-Path $installerDir ("staging\runtime.previous-" + (Get-Date -Format "yyyyMMdd-HHmmss"))) }
Move-Item -LiteralPath $candidate -Destination $runtimeDir
Write-Host "Viewer runtime prepared: $runtimeDir ($($info.version), $($info.machine))"
