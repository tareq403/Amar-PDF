# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller specification file for PDF Editor (Amar PDF)
"""

import sys
import os

block_cipher = None

# Determine icon path based on platform
if sys.platform == 'darwin':
    # macOS uses .icns
    icon_file = 'resources/icons/icon.icns'
elif sys.platform == 'win32':
    # Windows uses .ico
    icon_file = 'resources/icons/icon.ico'
else:
    # Linux uses .png
    icon_file = 'resources/icons/icon.png'

# Check if icon exists, fallback to None if not
if not os.path.exists(icon_file):
    print(f"Warning: Icon file not found: {icon_file}")
    print("Building without icon. See resources/icons/README.md for icon creation guide.")
    icon_file = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],  # No external data files needed anymore
    hiddenimports=[
        'PyQt5.QtPrintSupport',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Amar-PDF',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,  # Platform-specific icon
)

# macOS app bundle
app = BUNDLE(
    exe,
    name='Amar-PDF.app',
    icon=icon_file if sys.platform == 'darwin' else None,
    bundle_identifier='com.amarpdf.app',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'CFBundleName': 'Amar PDF',
        'CFBundleDisplayName': 'Amar PDF',
    },
)
