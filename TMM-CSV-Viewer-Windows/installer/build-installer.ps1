[CmdletBinding()]
param([string]$InnoCompiler)

$ErrorActionPreference = "Stop"
$installerDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $InnoCompiler) {
    $InnoCompiler = @((Join-Path ${env:ProgramFiles} "Inno Setup 7\ISCC.exe"), (Join-Path ${env:ProgramFiles(x86)} "Inno Setup 7\ISCC.exe")) | Where-Object { Test-Path $_ } | Select-Object -First 1
}
if (-not $InnoCompiler) { throw "Inno Setup 7 compiler not found." }
if (-not (Test-Path (Join-Path $installerDir "staging\app\tmm_csv_viewer.pyw"))) { throw "Application staging missing. Run prepare-app.ps1 first." }
if (-not (Test-Path (Join-Path $installerDir "staging\runtime\pythonw.exe"))) { throw "Runtime staging missing. Run prepare-runtime.ps1 first." }
& $InnoCompiler (Join-Path $installerDir "TMM-CSV-Viewer.iss")
if ($LASTEXITCODE -ne 0) { throw "Inno Setup compilation failed with exit code $LASTEXITCODE." }
Get-FileHash -Algorithm SHA256 (Join-Path $installerDir "output\TMM-CSV-Viewer-Setup-1.1.1.exe") | Format-List
