@echo off
setlocal EnableExtensions
cd /d "%~dp0"

py -m pip install -U pip
py -m pip install -U pyinstaller customtkinter tkcalendar requests babel certifi

rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q "IT Health AutoFill.spec" 2>nul

py -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --windowed ^
  --onedir ^
  --icon "icon.ico" ^
  --name "IT Health AutoFill" ^
  --add-data "icon.ico;." ^
  --add-data "app.ico;." ^
  --collect-all customtkinter ^
  --collect-all tkcalendar ^
  --collect-all babel ^
  --collect-all certifi ^
  main.py

echo.
echo Build selesai.
echo Ambil seluruh folder ini:
echo %CD%\dist\IT Health AutoFill
pause