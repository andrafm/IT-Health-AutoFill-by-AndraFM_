@echo off
cd /d D:\PYTHON

py -m pip install -U pip
py -m pip install -U pyinstaller customtkinter tkcalendar requests babel certifi

rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q "IT Health Auto Fill Form.spec" 2>nul

py -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --windowed ^
  --onedir ^
  --name "IT Health Auto Fill Form" ^
  --collect-all customtkinter ^
  --collect-all tkcalendar ^
  --collect-all babel ^
  --collect-all certifi ^
  teslagi.py

echo.
echo Build selesai.
echo Ambil seluruh folder ini:
echo D:\PYTHON\dist\IT Health Auto Fill Form
pause