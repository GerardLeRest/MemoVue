# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ChoixOrganisme.py'],
    pathex=[],
    binaries=[],
    datas=[('fichiers', 'fichiers'), ('deputes.db', 'deputes.db'), ('salaries.db', 'salaries.db'), ('eleves.db', 'eleves.db'), ('ConfigEcole.json', 'ConfigEcole.json'), ('ConfigEntreprise.json', 'ConfigEntreprise.json'), ('ConfigParlement.json', 'ConfigParlement.json')],
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
    a.binaries,
    a.datas,
    [],
    name='ChoixOrganisme',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
