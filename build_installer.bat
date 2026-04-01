@echo off
setlocal EnableExtensions

cd /d "%~dp0"

set "ISCC=C:\Users\%USERNAME%\AppData\Local\Programs\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=C:\Program Files\Inno Setup 6\ISCC.exe"

if not exist "%ISCC%" (
  echo Inno Setup Compiler ISCC.exe tidak ditemukan.
  echo Install Inno Setup 6 terlebih dahulu.
  pause
  exit /b 1
)

if not exist ".\installer.iss" (
  echo File installer.iss tidak ditemukan.
  pause
  exit /b 1
)

"%ISCC%" ".\installer.iss"
if errorlevel 1 (
  echo Build installer gagal.
  pause
  exit /b 1
)

echo.
echo Installer selesai. Cek folder dist.
pause
