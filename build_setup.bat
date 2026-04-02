@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "ISCC=C:\Users\%USERNAME%\AppData\Local\Programs\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=C:\Program Files\Inno Setup 6\ISCC.exe"

echo [1/3] Build aplikasi terbaru...
call .\build_final.bat
if errorlevel 1 (
  echo Build aplikasi gagal.
  exit /b 1
)

if not exist "%ISCC%" (
  echo ISCC.exe Inno Setup tidak ditemukan.
  echo Install Inno Setup 6 agar setup.exe memakai icon installer.
  exit /b 1
)

echo [2/3] Build installer via Inno Setup (dengan icon)...
"%ISCC%" ".\installer.iss"
if errorlevel 1 (
  echo Build installer Inno Setup gagal.
  exit /b 1
)

echo [3/3] Salin output setup.exe ke root project...
if exist ".\dist\setup.exe" (
  copy /Y ".\dist\setup.exe" ".\setup.exe" >nul
)

if not exist ".\setup.exe" (
  echo setup.exe tidak ditemukan setelah build.
  exit /b 1
)

echo Selesai: %CD%\setup.exe
exit /b 0
