@echo off
setlocal EnableExtensions

cd /d "%~dp0" || (
  echo Folder project tidak ditemukan.
  pause
  exit /b 1
)

set "VENV_DIR=.venv_small"
set "APP_NAME=IT Health AutoFill"
set "UPX_DIR=C:\upx"

echo [1/5] Menyiapkan virtual environment ringan...
if not exist "%VENV_DIR%\Scripts\python.exe" (
  py -m venv "%VENV_DIR%"
  if errorlevel 1 goto :fail
)

call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 goto :fail

python -m pip install -U pip setuptools wheel
if errorlevel 1 goto :fail

python -m pip install -U pyinstaller customtkinter requests tkcalendar babel certifi
if errorlevel 1 goto :fail

echo [2/5] Deteksi folder Tcl/Tk...
for /f "usebackq delims=" %%I in (`python -c "import tkinter as tk; r=tk.Tk(); r.withdraw(); print(r.tk.globalgetvar('tcl_library')); r.destroy()"`) do set "TCLDIR=%%I"
for /f "usebackq delims=" %%I in (`python -c "import tkinter as tk; r=tk.Tk(); r.withdraw(); print(r.tk.globalgetvar('tk_library')); r.destroy()"`) do set "TKDIR=%%I"

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

echo [3/5] Membersihkan hasil build lama...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q "%APP_NAME%.spec" 2>nul

echo [4/5] Build EXE ringan...
if exist "%UPX_DIR%\upx.exe" (
  echo UPX ditemukan. Kompresi aktif.
  python -m PyInstaller ^
    --noconfirm ^
    --clean ^
    --windowed ^
    --onedir ^
    --optimize 2 ^
    --name "%APP_NAME%" ^
    --upx-dir "%UPX_DIR%" ^
    --hidden-import=tkinter ^
    --collect-data customtkinter ^
    --collect-data tkcalendar ^
    --collect-data babel ^
    --collect-submodules babel ^
    --collect-data certifi ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    --exclude-module scipy ^
    --exclude-module IPython ^
    --exclude-module jupyter_client ^
    --exclude-module jupyter_core ^
    --exclude-module notebook ^
    --exclude-module PyQt5 ^
    --exclude-module PyQt6 ^
    --exclude-module PySide2 ^
    --exclude-module PySide6 ^
    --exclude-module test ^
    --add-data "%TCLDIR%;_tcl_data" ^
    --add-data "%TKDIR%;_tk_data" ^
    main.py
) else (
  echo UPX tidak ditemukan. Build tetap jalan tanpa kompresi tambahan.
  python -m PyInstaller ^
    --noconfirm ^
    --clean ^
    --windowed ^
    --onedir ^
    --optimize 2 ^
    --name "%APP_NAME%" ^
    --hidden-import=tkinter ^
    --collect-data customtkinter ^
    --collect-data tkcalendar ^
    --collect-data babel ^
    --collect-submodules babel ^
    --collect-data certifi ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    --exclude-module scipy ^
    --exclude-module IPython ^
    --exclude-module jupyter_client ^
    --exclude-module jupyter_core ^
    --exclude-module notebook ^
    --exclude-module PyQt5 ^
    --exclude-module PyQt6 ^
    --exclude-module PySide2 ^
    --exclude-module PySide6 ^
    --exclude-module test ^
    --add-data "%TCLDIR%;_tcl_data" ^
    --add-data "%TKDIR%;_tk_data" ^
    main.py
)

if errorlevel 1 goto :fail

echo [5/5] Validasi hasil build...
if not exist "dist\%APP_NAME%\%APP_NAME%.exe" goto :fail
if not exist "dist\%APP_NAME%\_internal\_tcl_data" goto :fail
if not exist "dist\%APP_NAME%\_internal\_tk_data" goto :fail

echo.
echo Build selesai.
echo Ambil seluruh folder ini:
echo %CD%\dist\%APP_NAME%
echo.
echo Catatan:
echo - Jangan copy .exe saja
echo - Pindahkan seluruh folder ke device lain
echo - Jika ingin lebih kecil lagi, install UPX ke: C:\upx
pause
exit /b 0

:fail
echo.
echo Build gagal. Periksa pesan error di atas.
pause
exit /b 1