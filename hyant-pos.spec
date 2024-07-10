# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('fonts\\SimHei.ttf', 'fonts')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='hyant-pos',
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
    exe, Tree('C:\\Users\\haifeng\\Documents\\Python Scripts\\pos_app\\'),
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='hyant-pos',
)
