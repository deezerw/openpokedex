"""Single-user data layer for the desktop build.

There is exactly one user. Their writable data (gen3.db, gen5.db,
settings.json) lives in paths.user_data_dir(). Seed DBs are read-only
bundled resources copied on first run.
"""
import os, sqlite3, shutil, json, tempfile

import paths

LOCAL_USER = "local"  # retained as a label for any caller that wants one

GEN_SEEDS = {
    3: "data/seed_gen3.db",
}
GEN_DBS = {3: "gen3.db"}


def init():
    """Ensure the user data dir + per-gen DBs exist, copying from bundled seeds."""
    paths.ensure_user_data_dir()
    for gen, db_file in GEN_DBS.items():
        user_db = paths.user_db_path(db_file)
        if os.path.exists(user_db):
            continue
        seed = paths.bundled_resource_path(GEN_SEEDS[gen])
        if os.path.exists(seed):
            shutil.copy(seed, user_db)
            con = sqlite3.connect(user_db)
            con.execute("UPDATE pokemon SET caught=0, caught_at=NULL, source_game=NULL, user_notes=NULL")
            con.commit()
            con.close()
        else:
            from models import SCHEMA
            con = sqlite3.connect(user_db)
            con.executescript(SCHEMA)
            con.commit()
            con.close()


def get_settings(username=LOCAL_USER):
    path = paths.user_settings_path()
    if os.path.exists(path):
        try:
            with open(path) as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _write_settings(data):
    dest = paths.user_settings_path()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(dest))
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, dest)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def save_settings(username, games_owned, use_glitches, bonus_disc_en=False, bonus_disc_jp=False, pokemon_channel_pal=False, show_ready_to_obtain=False):
    data = get_settings(username)
    data.update({
        "setup_complete": True,
        "games_owned": list(games_owned),
        "use_glitches": bool(use_glitches),
        "bonus_disc_en": bool(bonus_disc_en),
        "bonus_disc_jp": bool(bonus_disc_jp),
        "pokemon_channel_pal": bool(pokemon_channel_pal),
        "show_ready_to_obtain": bool(show_ready_to_obtain),
    })
    _write_settings(data)


def save_walkthrough_order(username, order):
    data = get_settings(username)
    data["walkthrough_order"] = list(order)
    _write_settings(data)


def current_user():
    return LOCAL_USER


def is_admin():
    return True
