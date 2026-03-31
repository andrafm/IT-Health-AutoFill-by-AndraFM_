# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_submodules

datas = [('C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python310\\tcl\\tcl8.6', '_tcl_data'), ('C:/Users/Administrator/AppData/Local/Programs/Python/Python310/tcl/tk8.6', '_tk_data')]
hiddenimports = ['tkinter']
datas += collect_data_files('customtkinter')
datas += collect_data_files('tkcalendar')
datas += collect_data_files('babel')
datas += collect_data_files('certifi')
hiddenimports += collect_submodules('babel')


a = Analysis(
    ['teslagi.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas', 'scipy', 'IPython', 'jupyter_client', 'jupyter_core', 'notebook', 'PyQt5', 'PyQt6', 'PySide2', 'PySide6', 'test'],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],
    exclude_binaries=True,
    name='IT Health Auto Fill Form',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='IT Health Auto Fill Form',
)
