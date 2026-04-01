param(
    [string]$AppName = "IT Health AutoFill",
    [string]$SourceDir = ".\dist\IT Health AutoFill",
    [string]$OutputDir = ".\dist",
    [string]$Version = "1.0.0"
)

$ErrorActionPreference = "Stop"

$workspace = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $workspace

$sourcePath = Resolve-Path $SourceDir -ErrorAction Stop
if (-not (Test-Path (Join-Path $sourcePath "$AppName.exe"))) {
    throw "File executable utama tidak ditemukan di $sourcePath"
}

$iexpress = Join-Path $env:WINDIR "System32\iexpress.exe"
if (-not (Test-Path $iexpress)) {
    throw "IExpress tidak ditemukan di $iexpress"
}

$stageRoot = Join-Path $workspace "installer_stage"
$packageDir = Join-Path $stageRoot "package"
$sedPath = Join-Path $stageRoot "installer.sed"
$installCmdPath = Join-Path $packageDir "install.cmd"
$payloadZipPath = Join-Path $packageDir "payload.zip"

if (Test-Path $stageRoot) {
    Remove-Item $stageRoot -Recurse -Force
}
New-Item -ItemType Directory -Path $packageDir | Out-Null

Compress-Archive -Path (Join-Path $sourcePath "*") -DestinationPath $payloadZipPath -Force

$installCmd = @"
@echo off
setlocal EnableExtensions

set "APP_NAME=$AppName"
set "DEST=%LocalAppData%\Programs\%APP_NAME%"
set "SRC=%~dp0"

if not exist "%DEST%" mkdir "%DEST%"

if not exist "%SRC%payload.zip" (
    echo payload.zip tidak ditemukan.
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -Path '%SRC%payload.zip' -DestinationPath '%DEST%' -Force"
if errorlevel 1 (
    echo Gagal mengekstrak payload aplikasi.
    pause
    exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$W=New-Object -ComObject WScript.Shell;" ^
  "$desktop=[Environment]::GetFolderPath('Desktop');" ^
  "$lnk=$W.CreateShortcut((Join-Path $desktop '$AppName.lnk'));" ^
  "$lnk.TargetPath=(Join-Path $env:LocalAppData 'Programs\\$AppName\\$AppName.exe');" ^
  "$lnk.WorkingDirectory=(Join-Path $env:LocalAppData 'Programs\\$AppName');" ^
  "$lnk.IconLocation=(Join-Path $env:LocalAppData 'Programs\\$AppName\\$AppName.exe');" ^
  "$lnk.Save()"

start "" "%DEST%\$AppName.exe"
exit /b 0
"@

Set-Content -Path $installCmdPath -Value $installCmd -Encoding ASCII

$outputPath = Join-Path (Resolve-Path $OutputDir) ("Setup-{0}-{1}.exe" -f $AppName.Replace(' ', '-'), $Version)

$sedContent = @"
[Version]
Class=IEXPRESS
SEDVersion=3

[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=0
HideExtractAnimation=1
UseLongFileName=1
InsideCompressed=0
CAB_FixedSize=0
CAB_ResvCodeSigning=0
RebootMode=N
InstallPrompt=%InstallPrompt%
DisplayLicense=%DisplayLicense%
FinishMessage=%FinishMessage%
TargetName=%TargetName%
FriendlyName=%FriendlyName%
AppLaunched=%AppLaunched%
PostInstallCmd=%PostInstallCmd%
AdminQuietInstCmd=%AdminQuietInstCmd%
UserQuietInstCmd=%UserQuietInstCmd%
SourceFiles=SourceFiles
SelfDelete=0

[Strings]
InstallPrompt=
DisplayLicense=
FinishMessage=Instalasi selesai.
TargetName=$outputPath
FriendlyName=$AppName Installer
AppLaunched=cmd /c install.cmd
PostInstallCmd=<None>
AdminQuietInstCmd=
UserQuietInstCmd=
FILE1=payload.zip
FILE2=install.cmd

[SourceFiles]
SourceFiles0=$packageDir

[SourceFiles0]
%FILE1%=
%FILE2%=
"@

Set-Content -Path $sedPath -Value $sedContent -Encoding ASCII

Write-Host "Membuat installer dengan IExpress..."
& $iexpress /N /Q $sedPath

if (-not (Test-Path $outputPath)) {
    throw "Installer gagal dibuat."
}

Write-Host "Installer selesai:" -ForegroundColor Green
Write-Host $outputPath
