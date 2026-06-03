"""Path resolution for read-only bundled assets vs writable user data.

Bundled assets (seed DBs, catch_locations.db, hotspots JSONs, sprites,
templates) ship inside the .exe and are read-only — resolved via
`bundled_resource_path()`, which works in dev and inside PyInstaller.

User data (gen3.db, gen5.db, settings.json) lives in a writable directory
that survives reinstalls — resolved via `user_data_dir()`:
  Windows: %APPDATA%/OpenPokedex
  Linux:   ~/.openpokedex
  macOS:   ~/Library/Application Support/OpenPokedex
"""
import os
import sys

APP_NAME = "OpenPokedex"


def _is_frozen():
    return getattr(sys, "frozen", False)


def bundled_resource_path(rel_path):
    """Resolve a path to a read-only asset shipped with the app.

    In dev: relative to the repo root.
    In a PyInstaller bundle: relative to sys._MEIPASS (the extracted temp dir).
    """
    if _is_frozen():
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, rel_path)


def user_data_dir():
    """Writable directory for the user's caught/notes DBs and settings."""
    if sys.platform == "win32":
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        # Linux / other — keep it simple, a dotfile dir in $HOME
        base = os.path.expanduser("~")
        return os.path.join(base, ".openpokedex")
    return os.path.join(base, APP_NAME)


def ensure_user_data_dir():
    path = user_data_dir()
    os.makedirs(path, exist_ok=True)
    return path


def user_db_path(filename):
    """Path to a writable per-gen DB inside the user data dir."""
    return os.path.join(ensure_user_data_dir(), filename)


def user_settings_path():
    return os.path.join(ensure_user_data_dir(), "settings.json")
