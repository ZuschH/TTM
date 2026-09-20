[CmdletBinding()]
param(
    [string]$InnoCompiler
)

$ErrorActionPreference = "Stop"
$installerDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Split-Path -Parent $installerDir
$scriptPath = Join-Path $installerDir "TMM.iss"
$stagingDir = Join-Path $installerDir "staging"
$appStage = Join-Path $stagingDir "app"
$runtimeStage = Join-Path $stagingDir "runtime"

if (-not $InnoCompiler) {
    $candidates = @(
        (Join-Path ${env:ProgramFiles} "Inno Setup 7\ISCC.exe"),
        (Join-Path ${env:ProgramFiles(x86)} "Inno Setup 7\ISCC.exe")
    )
    $InnoCompiler = $candidates | Where-Object {Test-Path $_} | Select-Object -First 1
}
if (-not $InnoCompiler -or -not (Test-Path $InnoCompiler)) {
    throw "Inno Setup 7 compiler not found. Install Inno Setup 7 or pass -InnoCompiler <path-to-ISCC.exe>."
}

if (-not (Test-Path $appStage)) {
    throw "Application staging directory missing: $appStage"
}
if (-not (Test-Path (Join-Path $runtimeStage "python.exe"))) {
    throw "Private Python runtime has not been staged yet: $runtimeStage"
}

Write-Host "TMM project:   $projectDir"
Write-Host "Inno compiler: $InnoCompiler"
Write-Host "Setup script:  $scriptPath"
& $InnoCompiler $scriptPath
if ($LASTEXITCODE -ne 0) {
    throw "Inno Setup compilation failed with exit code $LASTEXITCODE."
}

$setup = Join-Path $installerDir "output\TMM-Setup-1.0.0.exe"
if (-not (Test-Path $setup)) {
    throw "Expected setup executable was not created: $setup"
}
Get-FileHash -Algorithm SHA256 $setup | Format-List

