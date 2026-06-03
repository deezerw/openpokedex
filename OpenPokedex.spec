# PyInstaller spec for OpenPokedex.
# Build with: pyinstaller OpenPokedex.spec
# Produces a single-file Windows .exe with the Flask backend + native window.
#
# Note: data files are bundled read-only. User-writable data (gen3.db,
# settings.json) lives in %APPDATA%/OpenPokedex/ at runtime — see paths.py.

import os

block_cipher = None

datas = [
    ("templates", "templates"),
    ("static", "static"),
    ("data/seed_gen3.db", "data"),
    ("data/catch_locations.db", "data"),
]

# walkthrough_data is a regular Python package — PyInstaller picks it up by
# import discovery via desktop.py → app.py → models.py. Listed explicitly as
# a hidden import so its submodules aren't pruned.
hiddenimports = [
    "walkthrough_data",
    "walkthrough_data.emerald",
    "walkthrough_data.ruby",
    "walkthrough_data.sapphire",
    "walkthrough_data.firered",
    "walkthrough_data.leafgreen",
    "walkthrough_data.colosseum",
    "walkthrough_data.xd",
]

excludes = [
    # Dev / scraper scripts — never imported at runtime.
    "catch_locations_data",
    "scrape_gen3_locations",
    "scrape_missing_locations",
    "patch_missing_sevii",
    "update_colo_xd",
    "build_sprites",
    "seed_data",
    "seed",
    "guide_order",
    # Heavyweight unused stdlib / third-party modules.
    "tkinter",
    "test",
    "unittest",
]

a = Analysis(
    ["desktop.py"],
    pathex=[os.path.abspath(".")],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=excludes,
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
    name="OpenPokedex",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,        # no console window on Windows
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="build/icon.ico",
)
