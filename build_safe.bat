@echo off
setlocal EnableExtensions

cd /d D:\PYTHON || (
  echo Folder D:\PYTHON tidak ditemukan.
  pause
  exit /b 1
)

echo [1/4] Update tools...
py -m pip install -U pip
if errorlevel 1 goto :fail

py -m pip install -U pyinstaller customtkinter tkcalendar requests babel certifi
if errorlevel 1 goto :fail

echo [2/4] Deteksi folder Tcl/Tk...
for /f "usebackq delims=" %%I in (`py -c "import tkinter as tk; r=tk.Tk(); r.withdraw(); print(r.tk.globalgetvar('tcl_library')); r.destroy()"`) do set "TCLDIR=%%I"
for /f "usebackq delims=" %%I in (`py -c "import tkinter as tk; r=tk.Tk(); r.withdraw(); print(r.tk.globalgetvar('tk_library')); r.destroy()"`) do set "TKDIR=%%I"

if not defined TCLDIR (
  echo Gagal membaca lokasi Tcl.
  goto :fail
)

if not defined TKDIR (
  echo Gagal membaca lokasi Tk.
  goto :fail
)

echo TCLDIR=%TCLDIR%
echo TKDIR=%TKDIR%

echo [3/4] Bersihkan build lama...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q "IT Health Auto Fill Form.spec" 2>nul

echo [4/4] Build aplikasi...
py -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --windowed ^
  --onedir ^
  --name "IT Health Auto Fill Form" ^
  --hidden-import=tkinter ^
  --collect-all customtkinter ^
  --collect-all tkcalendar ^
  --collect-all babel ^
  --collect-all certifi ^
  --add-data "%TCLDIR%;_tcl_data" ^
  --add-data "%TKDIR%;_tk_data" ^
  teslagi.py

if errorlevel 1 goto :fail

if not exist "dist\IT Health Auto Fill Form\_internal\_tcl_data" (
  echo ERROR: folder _tcl_data tidak ditemukan.
  goto :fail
)

if not exist "dist\IT Health Auto Fill Form\_internal\_tk_data" (
  echo ERROR: folder _tk_data tidak ditemukan.
  goto :fail
)

echo.
echo Build selesai.
echo Copy SELURUH folder ini ke device lain:
echo D:\PYTHON\dist\IT Health Auto Fill Form
echo.
echo Jangan copy .exe saja.
echo Jangan jalankan dari ZIP atau flashdisk.
pause
exit /b 0

:fail
echo.
echo Build gagal. Periksa pesan error di atas.
pause
exit /b 1