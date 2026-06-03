import os
import sqlite3
import threading
from collections import deque, Counter
from contextlib import contextmanager
from datetime import datetime, timezone

import paths

_CATCH_LOCATIONS_DB = paths.bundled_resource_path("data/catch_locations.db")
_catch_db_initialized = False
_catch_db_lock = threading.Lock()


@contextmanager
def _catch_db():
    uri = f"file:{_CATCH_LOCATIONS_DB}?mode=ro&immutable=1"
    con = sqlite3.connect(uri, uri=True)
    con.row_factory = sqlite3.Row
    try:
        yield con
    finally:
        con.close()


def _ensure_catch_db():
    # catch_locations.db is a bundled read-only asset, populated at build time.
    return


def get_catch_locations(dex_no):
    _ensure_catch_db()
    with _catch_db() as con:
        rows = con.execute(
            "SELECT game, location, method, notes, encounter_rate, levels FROM catch_locations WHERE dex_no = ? ORDER BY game, method, location",
            (dex_no,),
        ).fetchall()
    return [dict(r) for r in rows]

_CATCH_LOC_METHODS = {'wild', 'surf', 'fish', 'gift', 'static', 'starter', 'safari', 'event', 'shadow', 'rock-smash', 'trade', 'breed'}
_catch_locations_cache = None
_catch_locations_lock = threading.Lock()


def _all_catch_locations():
    """dex_no → [{game, location, method}] for catch-method rows only (no evolve/trade/breed)."""
    global _catch_locations_cache
    if _catch_locations_cache is not None:
        return _catch_locations_cache
    with _catch_locations_lock:
        if _catch_locations_cache is not None:
            return _catch_locations_cache
        _ensure_catch_db()
        with _catch_db() as con:
            rows = con.execute("SELECT dex_no, game, location, method FROM catch_locations").fetchall()
        by_dex = {}
        for r in rows:
            if r["method"] in _CATCH_LOC_METHODS:
                by_dex.setdefault(r["dex_no"], []).append({"game": r["game"], "location": r["location"], "method": r["method"]})
        _catch_locations_cache = by_dex
    return _catch_locations_cache


def _db_path():
    fallback = paths.bundled_resource_path("data/seed_gen3.db")
    try:
        from flask import g
        return getattr(g, "db_path", None) or fallback
    except RuntimeError:
        return fallback


SCHEMA = """
CREATE TABLE IF NOT EXISTS pokemon (
    dex_no          INTEGER PRIMARY KEY,
    name            TEXT NOT NULL,
    type1           TEXT NOT NULL,
    type2           TEXT,
    region          TEXT NOT NULL,
    easiest_game    TEXT NOT NULL,
    location        TEXT NOT NULL,
    method          TEXT NOT NULL,
    evolves_from    INTEGER,
    tags            TEXT NOT NULL,
    seed_notes      TEXT,
    caught          INTEGER NOT NULL DEFAULT 0,
    caught_at       TEXT,
    source_game     TEXT,
    user_notes      TEXT
);
"""


@contextmanager
def get_db():
    con = sqlite3.connect(_db_path())
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    try:
        yield con
        if con.in_transaction:
            con.commit()
    finally:
        con.close()


def init_db():
    with get_db() as con:
        con.executescript(SCHEMA)


def get_pokemon(dex_no):
    with get_db() as con:
        row = con.execute("SELECT * FROM pokemon WHERE dex_no = ?", (dex_no,)).fetchone()
    return dict(row) if row else None


def list_pokemon(region=None, type_filter=None, tag=None, caught=None, search=None):
    clauses = []
    params = []
    if region:
        clauses.append("region = ?")
        params.append(region)
    if type_filter:
        clauses.append("(type1 = ? OR type2 = ?)")
        params.extend([type_filter, type_filter])
    if tag:
        clauses.append("(',' || tags || ',' LIKE '%,' || ? || ',%')")
        params.append(tag)
    if caught is not None:
        clauses.append("caught = ?")
        params.append(1 if caught else 0)
    if search:
        clauses.append("name LIKE ?")
        params.append(f"%{search}%")
    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    with get_db() as con:
        rows = con.execute(
            f"SELECT * FROM pokemon {where} ORDER BY dex_no", params
        ).fetchall()
    return [dict(r) for r in rows]


def catchable_games_by_dex(games_in_order):
    """{dex_no: [game_key, ...]} — for each Pokémon, the subset of games_in_order where
    it can be directly caught (wild/surf/fish/gift/static/starter/safari/shadow/rock-smash;
    NOT trade-evo or breed), preserving the given display order. Surfaces version
    exclusivity: a single game means it's exclusive to that version.
    """
    catch_by_dex = _all_catch_locations()
    games_set = set(games_in_order)
    out = {}
    for dex_no, rows in catch_by_dex.items():
        present = {r["game"] for r in rows if r["game"] in games_set and r["method"] in _DIRECT_CATCH}
        if present:
            out[dex_no] = [gm for gm in games_in_order if gm in present]
    return out


def toggle_caught(dex_no, source_game=None):
    """Read current caught state and flip it in one transaction. Returns new state or None if not found."""
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as con:
        row = con.execute("SELECT caught, easiest_game FROM pokemon WHERE dex_no=?", (dex_no,)).fetchone()
        if not row:
            return None
        new_state = not bool(row["caught"])
        game = (source_game or row["easiest_game"]) if new_state else None
        caught_at = now if new_state else None
        con.execute(
            "UPDATE pokemon SET caught=?, caught_at=?, source_game=? WHERE dex_no=?",
            (1 if new_state else 0, caught_at, game, dex_no),
        )
    return new_state


def mark_caught(dex_no, caught: bool, source_game=None):
    now = datetime.now(timezone.utc).isoformat() if caught else None
    with get_db() as con:
        if caught and not source_game:
            row = con.execute("SELECT easiest_game FROM pokemon WHERE dex_no=?", (dex_no,)).fetchone()
            if row:
                source_game = row["easiest_game"]
        con.execute(
            "UPDATE pokemon SET caught=?, caught_at=?, source_game=? WHERE dex_no=?",
            (1 if caught else 0, now, source_game if caught else None, dex_no),
        )


def reset_progress():
    """Clear all caught state in the current generation's DB (caught flag, timestamp,
    and source game). Preserves user notes. Returns how many Pokémon were reset."""
    with get_db() as con:
        n = con.execute("SELECT COUNT(*) FROM pokemon WHERE caught=1").fetchone()[0]
        con.execute("UPDATE pokemon SET caught=0, caught_at=NULL, source_game=NULL WHERE caught=1")
    return n


def save_notes(dex_no, user_notes, source_game=None):
    with get_db() as con:
        con.execute(
            "UPDATE pokemon SET user_notes=?, source_game=COALESCE(?,source_game) WHERE dex_no=?",
            (user_notes, source_game, dex_no),
        )


def list_missing_by_game():
    owned = _owned_games()
    with get_db() as con:
        rows = con.execute(
            """
            SELECT easiest_game, location, dex_no, name
            FROM pokemon
            WHERE caught = 0
            ORDER BY easiest_game, location, dex_no
            """
        ).fetchall()
    grouped = {}
    for r in rows:
        game = r["easiest_game"]
        if owned is not None and game not in owned:
            continue
        loc = r["location"]
        grouped.setdefault(game, {}).setdefault(loc, []).append(
            {"dex_no": r["dex_no"], "name": r["name"]}
        )
    return grouped


_CATCH_METHODS = {'wild', 'gift', 'safari', 'static', 'event', 'shadow', 'starter'}


def _build_evo_maps(mons):
    """Return forward_map where forward_map[parent_dex] = [child_dex, ...]."""
    fwd = {}
    for m in mons.values():
        if m.get("evolves_from"):
            fwd.setdefault(m["evolves_from"], []).append(m["dex_no"])
    return fwd


def _caught_descendant(dex_no, fwd, mons):
    """BFS: return name of first caught descendant, or None."""
    queue = deque(fwd.get(dex_no, []))
    while queue:
        cur = queue.popleft()
        if mons[cur]["caught"]:
            return mons[cur]["name"]
        queue.extend(fwd.get(cur, []))
    return None


def list_evolve_by_game():
    """Evolve + trade-evo Pokémon still missing, with pre-evo context."""
    with get_db() as con:
        rows = con.execute(
            """SELECT p.easiest_game, p.dex_no, p.name, p.method, p.location,
                      pre.name AS pre_name, pre.caught AS pre_caught
               FROM pokemon p
               LEFT JOIN pokemon pre ON pre.dex_no = p.evolves_from
               WHERE p.method IN ('evolve','trade-evo') AND p.caught = 0
               ORDER BY p.easiest_game, p.dex_no"""
        ).fetchall()
    result = {}
    for r in rows:
        result.setdefault(r["easiest_game"], []).append({
            "dex_no": r["dex_no"],
            "name": r["name"],
            "method": r["method"],
            "location": r["location"],
            "pre_name": r["pre_name"],
            "pre_caught": bool(r["pre_caught"]) if r["pre_caught"] is not None else False,
        })
    return result


def _load_all_mons():
    with get_db() as con:
        rows = con.execute(
            "SELECT dex_no, name, easiest_game, method, location, caught, evolves_from, tags FROM pokemon ORDER BY dex_no"
        ).fetchall()
    return {r["dex_no"]: dict(r) for r in rows}


def list_breed_by_game(mons=None):
    """
    Pokémon obtainable by breeding:
    1. Static breed-method entries (Pichu, Cleffa, etc.)
    2. Dynamically detected: uncaught base forms whose descendant is caught.
    Returns ({game: [entry]}, set_of_dynamic_dex_nos).
    Pass mons to reuse an already-loaded dict and avoid a redundant DB read.
    """
    if mons is None:
        mons = _load_all_mons()
    fwd = _build_evo_maps(mons)

    result = {}
    dynamic_dex = set()

    for m in mons.values():
        if m["caught"]:
            continue
        if m["method"] == "breed":
            result.setdefault(m["easiest_game"], []).append({
                "dex_no": m["dex_no"],
                "name": m["name"],
                "location": m["location"],
                "breed_from": None,
            })
        elif m["evolves_from"] is None:
            # Base form — check if a caught descendant can be bred
            source = _caught_descendant(m["dex_no"], fwd, mons)
            if source:
                dynamic_dex.add(m["dex_no"])
                result.setdefault(m["easiest_game"], []).append({
                    "dex_no": m["dex_no"],
                    "name": m["name"],
                    "location": m["location"],
                    "breed_from": source,
                })

    for game in result:
        result[game].sort(key=lambda x: x["dex_no"])
    return result, dynamic_dex


def _owned_games():
    """Set of games the current user owns (for this gen), or None for no filter."""
    try:
        from flask import g
        return getattr(g, "owned_games", None)
    except RuntimeError:
        return None


def _use_glitches():
    try:
        from flask import g
        return bool(getattr(g, "use_glitches", False))
    except RuntimeError:
        return False


def _extra_obtainable():
    try:
        from flask import g
        return getattr(g, "extra_obtainable", set()) or set()
    except RuntimeError:
        return set()


# Games that can perform link trades (for self trade-evolving). GameCube spin-offs excluded.
_NON_TRADEABLE = {"colosseum", "xd"}
_NORMAL_CATCH = {"wild", "surf", "fish", "gift", "static", "starter", "safari", "shadow", "rock-smash", "trade", "breed"}
# Methods that count as self-contained (no trading, no events, no Pal Park)
_DIRECT_CATCH = {"wild", "surf", "fish", "gift", "static", "starter", "safari", "shadow", "rock-smash"}
_GAME_ORDER = ["firered", "leafgreen", "ruby", "sapphire", "emerald", "colosseum", "xd"]

# Genderless gen-3 base forms (Mineral/genderless egg behaviour): they cannot be
# bred, so a pre-evolution here is NOT obtainable just because a later stage is.
_UNBREEDABLE_BASE = {81, 100, 120, 137, 343, 374}  # Magnemite, Voltorb, Staryu, Porygon, Baltoy, Beldum


def _per_game_completable(mons, catch_by_dex):
    """Return {game: set(dex_no)} — all Pokémon obtainable using only that single game
    (no trading, no events, no Pal Park), with full evo and breed propagation."""
    game_direct = {}
    game_breed  = {}
    for dex_no, rows in catch_by_dex.items():
        if dex_no not in mons:
            continue
        for r in rows:
            gm = r["game"]
            if r["method"] in _DIRECT_CATCH:
                game_direct.setdefault(gm, set()).add(dex_no)
            elif r["method"] == "breed":
                game_breed.setdefault(gm, set()).add(dex_no)

    fwd = {}
    for d, m in mons.items():
        if m.get("evolves_from"):
            fwd.setdefault(m["evolves_from"], []).append(d)

    def descendants(d):
        out, q = [], list(fwd.get(d, []))
        while q:
            c = q.pop(); out.append(c); q.extend(fwd.get(c, []))
        return out

    result = {}
    for game in sorted(set(game_direct) | set(game_breed)):
        obtain = set(game_direct.get(game, set()))
        breed_cands = game_breed.get(game, set())
        changed = True
        while changed:
            changed = False
            for d, m in mons.items():
                if d in obtain:
                    continue
                mth, pre = m.get("method", ""), m.get("evolves_from")
                if pre and pre in obtain and mth != "trade-evo":
                    obtain.add(d); changed = True
                elif (mth == "breed" or d in breed_cands) and any(c in obtain for c in descendants(d)):
                    obtain.add(d); changed = True
        result[game] = obtain
    return result


def obtainable_dex(mons=None, owned=None, glitches=None, catch_by_dex=None, extra_obtainable=None):
    """Set of dex_no obtainable given owned games + the self-trade model.

    A Pokémon is obtainable if it can be caught in an owned game, evolved/bred up
    from something obtainable, or trade-evolved (needs ≥2 owned tradeable carts).
    Event-only Pokémon (Mew, etc.) are obtainable only when glitches are enabled.
    extra_obtainable is a set of dex_nos for event distributions the user has access to.
    """
    if mons is None:
        mons = _load_all_mons()
    if owned is None:
        owned = _owned_games()
    if glitches is None:
        glitches = _use_glitches()
    if extra_obtainable is None:
        extra_obtainable = _extra_obtainable()
    if catch_by_dex is None:
        catch_by_dex = _all_catch_locations()
    if owned is None:  # no ownership filter → treat every game as owned
        owned = {r["game"] for rows in catch_by_dex.values() for r in rows} | {m["easiest_game"] for m in mons.values()}

    can_trade = len([gm for gm in owned if gm not in _NON_TRADEABLE]) >= 2

    fwd = {}
    for d, m in mons.items():
        if m.get("evolves_from"):
            fwd.setdefault(m["evolves_from"], []).append(d)

    def descendants(d):
        out, q = [], list(fwd.get(d, []))
        while q:
            c = q.pop()
            out.append(c)
            q.extend(fwd.get(c, []))
        return out

    obtain = {}
    for d, m in mons.items():
        rows = catch_by_dex.get(d, [])
        direct = any(r["game"] in owned and r["method"] in _NORMAL_CATCH for r in rows)
        if not direct and not rows and m["method"] in _CATCH_METHODS and m["easiest_game"] in owned:
            direct = True  # fallback when detailed catch data is missing
        obtain[d] = direct
    if glitches:
        for d, m in mons.items():
            if m["method"] == "event":
                obtain[d] = True
    for d in extra_obtainable:
        if d in obtain:
            obtain[d] = True

    changed = True
    while changed:
        changed = False
        for d, m in mons.items():
            if obtain[d]:
                continue
            mth, pre = m["method"], m.get("evolves_from")
            if mth == "trade-evo" and pre and obtain.get(pre) and can_trade:
                obtain[d] = True; changed = True
            elif mth != "trade-evo" and pre and obtain.get(pre):
                obtain[d] = True; changed = True
            # Breed back to a base form from any obtainable descendant — explicit
            # breed entries (babies) or any non-genderless base (e.g. Cyndaquil
            # from a Quilava you only got as a shadow).
            elif (mth == "breed" or (pre is None and d not in _UNBREEDABLE_BASE)) \
                    and any(obtain.get(c) for c in descendants(d)):
                obtain[d] = True; changed = True
    return {d for d, v in obtain.items() if v}


def unobtainable_dex(mons=None, owned=None, glitches=None, extra_obtainable=None):
    if mons is None:
        mons = _load_all_mons()
    return set(mons) - obtainable_dex(mons=mons, owned=owned, glitches=glitches, extra_obtainable=extra_obtainable)


_GAME_NAMES = {
    "firered": "FireRed", "leafgreen": "LeafGreen",
    "ruby": "Ruby", "sapphire": "Sapphire", "emerald": "Emerald",
    "colosseum": "Colosseum", "xd": "XD",
    "black": "Black", "white": "White", "black2": "Black 2", "white2": "White 2",
}


def derivable_dex(mons=None):
    """Uncaught Pokémon obtainable right now by evolving or breeding caught Pokémon.

    Covers three cases:
    - Evolutions (level/stone/trade): pre-evo is caught
    - Explicit breed entries: a descendant is caught
    - Base forms with no evolves_from: a descendant is caught (breed-back)
    """
    if mons is None:
        mons = _load_all_mons()
    fwd = {}
    for d, m in mons.items():
        if m.get("evolves_from"):
            fwd.setdefault(m["evolves_from"], []).append(d)
    result = set()
    for dex_no, m in mons.items():
        if m["caught"]:
            continue
        pre = m.get("evolves_from")
        if pre and mons.get(pre, {}).get("caught"):
            result.add(dex_no)
        elif not pre and dex_no not in _UNBREEDABLE_BASE and _caught_descendant(dex_no, fwd, mons):
            result.add(dex_no)
        elif m["method"] == "breed" and _caught_descendant(dex_no, fwd, mons):
            result.add(dex_no)

    # Propagate: if a pre-evo is derivable, the next evolution is also derivable
    changed = True
    while changed:
        changed = False
        for dex_no, m in mons.items():
            if m["caught"] or dex_no in result:
                continue
            if m.get("evolves_from") in result:
                result.add(dex_no)
                changed = True

    return result


def list_by_box(box_size=60, cols=12):
    rows_per_box = box_size // cols
    with get_db() as con:
        rows = con.execute("SELECT dex_no, name, caught FROM pokemon ORDER BY dex_no").fetchall()
    boxes = {}
    for r in rows:
        box_num = (r["dex_no"] - 1) // box_size + 1
        slot    = (r["dex_no"] - 1) % box_size
        row     = slot // cols
        col     = slot % cols
        if box_num not in boxes:
            boxes[box_num] = [[None] * cols for _ in range(rows_per_box)]
        boxes[box_num][row][col] = {
            "dex_no": r["dex_no"],
            "name":   r["name"],
            "caught": bool(r["caught"]),
        }
    return boxes


def _trade_item_for(dex_no, catch_by_dex):
    """Held item a trade-evo needs, parsed from its catch-location text
    (e.g. "Trade Onix holding Metal Coat" → "Metal Coat"). None = plain link trade."""
    for r in catch_by_dex.get(dex_no, []):
        loc = r["location"]
        if "holding " in loc:
            return loc.split("holding ", 1)[1].strip()
    return None


def list_trade_evos():
    with get_db() as con:
        rows = con.execute(
            """
            SELECT t.dex_no, t.name, t.type1, t.type2, t.caught, t.evolves_from,
                   p.name AS pre_name, p.caught AS pre_caught,
                   p.dex_no AS pre_dex_no
            FROM pokemon t
            LEFT JOIN pokemon p ON p.dex_no = t.evolves_from
            WHERE t.method = 'trade-evo'
            ORDER BY t.dex_no
            """
        ).fetchall()
    catch_by_dex = _all_catch_locations()
    result = []
    for r in rows:
        d = dict(r)
        d["trade_item"] = _trade_item_for(d["dex_no"], catch_by_dex)
        result.append(d)
    return result


def trade_item_summary(trade_evos, obtainable):
    """Aggregate held items needed across trade-evos. The held item is consumed on
    trade-evolution, so each trade-evo needing an item costs one of that item.

    Returns a list of {item, total, remaining, mons} sorted by remaining desc, where
    `total` = trade-evos using the item, `remaining` = those still uncaught and
    obtainable with the user's games. Trade-evos needing no item are excluded.
    """
    items = {}
    for t in trade_evos:
        item = t.get("trade_item")
        if not item:
            continue
        bucket = items.setdefault(item, {"item": item, "total": 0, "remaining": 0, "mons": []})
        bucket["total"] += 1
        needed = (not t["caught"]) and (t["dex_no"] in obtainable)
        if needed:
            bucket["remaining"] += 1
        bucket["mons"].append({"dex_no": t["dex_no"], "name": t["name"],
                               "caught": bool(t["caught"]), "needed": needed})
    return sorted(items.values(), key=lambda b: (-b["remaining"], -b["total"], b["item"]))


def stats(owned=None, glitches=None, mons=None, game_order=None):
    if mons is None:
        mons = _load_all_mons()
    if game_order is None:
        game_order = _GAME_ORDER
    with get_db() as con:
        by_region = con.execute(
            "SELECT region, COUNT(*) as total, SUM(caught) as done FROM pokemon GROUP BY region"
        ).fetchall()
        by_game = con.execute(
            "SELECT easiest_game, COUNT(*) as total, SUM(caught) as done FROM pokemon GROUP BY easiest_game ORDER BY easiest_game"
        ).fetchall()
    total = len(mons)
    caught = sum(1 for m in mons.values() if m["caught"])
    catch_by_dex = _all_catch_locations()
    obtainable = obtainable_dex(mons=mons, owned=owned, glitches=glitches, catch_by_dex=catch_by_dex)
    obt_caught = sum(1 for d in obtainable if mons[d]["caught"])

    per_game_raw = _per_game_completable(mons, catch_by_dex)
    by_game_completable = []
    for game in game_order:
        if game not in per_game_raw:
            continue
        completable = per_game_raw[game]
        game_caught = sum(1 for d in completable if mons[d]["caught"])
        by_game_completable.append({
            "game": _GAME_NAMES.get(game, game),
            "completable": len(completable),
            "caught": game_caught,
        })

    return {
        "total": total,
        "caught": caught,
        "missing": total - caught,
        "obtainable": len(obtainable),
        "unobtainable": total - len(obtainable),
        "obtainable_caught": obt_caught,
        "obtainable_missing": len(obtainable) - obt_caught,
        "by_region": [dict(r) for r in by_region],
        "by_game": [dict(r) for r in by_game],
        "by_game_completable": by_game_completable,
    }


_WALKTHROUGH_METHODS = {'wild', 'surf', 'fish', 'gift', 'static', 'starter', 'safari', 'shadow', 'rock-smash', 'trade'}
# Methods where you can obtain multiple via grinding; others are one-time-only
_REPEATABLE_METHODS = {'wild', 'surf', 'fish', 'safari', 'rock-smash'}


def walkthrough_mon_counts(ordered_game_keys):
    """Return {game_key: int} — Pokémon assigned to each game via most-locations algorithm.

    A mon is assigned to whichever game in the list has the most distinct locations
    where it's acquirable (catch/in-game-trade/gift); earliest game wins ties. All
    acquirable locations count, whether or not they're placed on the curated route.
    """
    from walkthrough_data import GAME_CONFIGS
    catch_by_dex = _all_catch_locations()
    mons = _load_all_mons()
    trade_evo = {d for d, m in mons.items() if m.get("method") == "trade-evo"}

    games = [gk for gk in ordered_game_keys if gk in GAME_CONFIGS]
    counts = {gk: 0 for gk in games}
    for dex_no, rows in catch_by_dex.items():
        best_game = None
        best_count = 0
        for gk in games:
            count = len({
                r["location"] for r in rows
                if r["game"] == gk and r["method"] in _WALKTHROUGH_METHODS
                and not (r["method"] == "trade" and dex_no in trade_evo)
            })
            if count > best_count:
                best_count = count
                best_game = gk
        if best_count > 0 and best_game:
            counts[best_game] += 1
    return counts


def recommend_walkthrough_order(owned_game_keys):
    """Greedy maximum-coverage order for completing the living dex with the fewest games.

    At each step pick the game that adds the most newly *obtainable* Pokémon — counting
    full catch + evolve + breed + trade-evo closure (via obtainable_dex), not just direct
    catches — on top of the games already chosen. This front-loads the highest-value games
    and pushes games whose entire offering is already covered to the end with new == 0
    ("skippable"), so the user can see which games they don't actually need to play.

    owned_game_keys: collection of game keys to consider (from GAME_CONFIGS).
    Returns an ordered list of {game, new, essential}, where `new` is the marginal count
    of dex entries that game unlocks and `essential` is True when new > 0.
    """
    from walkthrough_data import GAME_CONFIGS
    mons = _load_all_mons()
    catch_by_dex = _all_catch_locations()
    candidates = [gk for gk in GAME_CONFIGS if gk in owned_game_keys]
    selected, covered, result = [], set(), []
    while candidates:
        best_gk, best_gain, best_obt = None, -1, set()
        for gk in candidates:
            obt = obtainable_dex(mons=mons, owned=set(selected + [gk]), catch_by_dex=catch_by_dex)
            gain = len(obt - covered)
            if gain > best_gain:  # first candidate in GAME_CONFIGS order wins ties
                best_gk, best_gain, best_obt = gk, gain, obt
        selected.append(best_gk)
        result.append({"game": best_gk, "new": best_gain, "essential": best_gain > 0})
        covered = best_obt
        candidates.remove(best_gk)
    return result





def walkthrough_sections(game, story_areas, game_sequence=None, catch_qty_overrides=None, full_sequence_configs=None):
    """Story-ordered sections for a game walkthrough.

    Returns list of {label, notes, pokemon: [{dex_no, name, caught, method, catch_qty}]}.
    Each Pokémon appears in the FIRST area where it can be caught; catch_qty indicates
    how many copies to catch to complete the living dex (accounting for evolutions and
    whether later games in game_sequence cover the evolved forms directly).

    full_sequence_configs: ordered list of {game, label, story_areas} for ALL games in
    the user's play order. Each Pokémon is assigned to whichever game has the most
    distinct catchable locations for it; tiebreak goes to the earliest game in the list.
    Mons not assigned to the current game are hidden entirely.
    """
    if game_sequence is None:
        game_sequence = [game]

    mons = _load_all_mons()
    catch_by_dex = _all_catch_locations()
    # A 'trade' catch row on a trade-evo species means the player self trade-evolves
    # their own mon — that's an afterward task, not something acquired during play.
    trade_evo = {d for d, m in mons.items() if m.get("method") == "trade-evo"}

    fwd = {}
    for d, m in mons.items():
        if m.get("evolves_from"):
            fwd.setdefault(m["evolves_from"], []).append(d)

    # Pokémon catchable directly anywhere in the full game sequence
    seq_set = set(game_sequence)
    seq_direct = set()
    for dex_no, rows in catch_by_dex.items():
        for r in rows:
            if r["game"] in seq_set and r["method"] in _DIRECT_CATCH:
                seq_direct.add(dex_no)
                break

    def needed_depth(node):
        """Min copies of node to get node + all evolution-only descendants."""
        needed = [c for c in fwd.get(node, []) if c not in seq_direct]
        if not needed:
            return 1
        return 1 + sum(needed_depth(c) for c in needed)

    # Map each location string to its first story-area index
    loc_to_idx = {}
    for idx, area in enumerate(story_areas):
        for loc in area.get("locations", []):
            if loc not in loc_to_idx:
                loc_to_idx[loc] = idx

    # Collect ecard_only dex sets across all areas
    area_ecard_sets = [area.get("ecard_only_dex", set()) for area in story_areas]
    all_ecard = set().union(*area_ecard_sets)

    # Assign each Pokémon to the game in the sequence with the most distinct catchable
    # locations for it. Iterating in order means the first game wins ties.
    mon_assigned_game = {}
    if full_sequence_configs:
        seq_games = [cfg["game"] for cfg in full_sequence_configs]
        for dex_no, rows in catch_by_dex.items():
            if dex_no not in mons:
                continue
            best_game = None
            best_count = 0
            for cfg_game in seq_games:
                count = len({
                    r["location"] for r in rows
                    if r["game"] == cfg_game and r["method"] in _WALKTHROUGH_METHODS
                    and not (r["method"] == "trade" and dex_no in trade_evo)
                })
                if count > best_count:
                    best_count = count
                    best_game = cfg_game
            if best_count > 0:
                mon_assigned_game[dex_no] = best_game

    # Assign each Pokémon to the earliest story area where it appears in this game.
    # Acquirable locations not matched to any story area land in a trailing
    # "Other / late-game" bucket (index = len(story_areas)) so nothing is dropped.
    other_idx = len(story_areas)
    first_area = {}  # dex_no -> (area_idx, method)
    for dex_no, rows in catch_by_dex.items():
        if dex_no not in mons:
            continue
        for r in rows:
            if r["game"] != game or r["method"] not in _WALKTHROUGH_METHODS:
                continue
            if r["method"] == "trade" and dex_no in trade_evo:
                continue
            idx = loc_to_idx.get(r["location"], other_idx)
            if dex_no not in first_area or first_area[dex_no][0] > idx:
                first_area[dex_no] = (idx, r["method"])

    buckets = [[] for _ in range(len(story_areas) + 1)]
    overrides = catch_qty_overrides or {}
    for dex_no, (idx, method) in first_area.items():
        if full_sequence_configs and mon_assigned_game.get(dex_no) != game:
            continue
        qty = overrides.get(dex_no, needed_depth(dex_no)) if method in _REPEATABLE_METHODS else 1
        buckets[idx].append({
            "dex_no": dex_no,
            "name": mons[dex_no]["name"],
            "caught": bool(mons[dex_no]["caught"]),
            "method": method,
            "catch_qty": qty,
            "ecard_only": dex_no in all_ecard,
        })

    for bucket in buckets:
        bucket.sort(key=lambda m: m["dex_no"])

    sections = [
        {
            "label": area["label"],
            "notes": area.get("notes"),
            "has_ecard": bool(area_ecard_sets[i]),
            "pokemon": buckets[i],
        }
        for i, area in enumerate(story_areas)
    ]
    if buckets[other_idx]:
        sections.append({
            "label": "Other / Late-game Locations",
            "notes": "Acquirable here but not yet placed on the route — usually post-game, optional, or trade-in areas.",
            "has_ecard": False,
            "pokemon": buckets[other_idx],
        })
    return sections


def walkthrough_optional(owned_game_keys, mons=None):
    """Comprehensive "from your catches" map: every living-dex form you don't
    directly acquire during owned playthroughs but can reach from one you do.

    Returns {"breed": [...], "evolve": [...]}; each item is
    {dex_no, name, caught, source_dex, source_name, kind, ready}.
      breed  — an un-acquired pre-evolution you breed down to from a caught later
               stage (genderless lines excluded — they can't be bred).
      evolve — an un-acquired later stage you evolve up to from a caught form
               (kind "trade-evolve" when it needs a trade).
    """
    if mons is None:
        mons = _load_all_mons()
    catch_by_dex = _all_catch_locations()
    owned = set(owned_game_keys)
    trade_evo = {d for d, m in mons.items() if m.get("method") == "trade-evo"}

    acquired = set()
    for d, rows in catch_by_dex.items():
        if d not in mons:
            continue
        for r in rows:
            if r["game"] in owned and r["method"] in _WALKTHROUGH_METHODS:
                if r["method"] == "trade" and d in trade_evo:
                    continue
                acquired.add(d)
                break

    ready = derivable_dex(mons=mons)
    fwd = {}
    for d, m in mons.items():
        if m.get("evolves_from"):
            fwd.setdefault(m["evolves_from"], []).append(d)

    def nearest_acquired_ancestor(d):
        cur = mons[d].get("evolves_from")
        while cur:
            if cur in acquired:
                return cur
            cur = mons.get(cur, {}).get("evolves_from")
        return None

    def nearest_acquired_descendant(d):
        q = list(fwd.get(d, []))
        seen = set(q)
        while q:
            c = q.pop(0)
            if c in acquired:
                return c
            for n in fwd.get(c, []):
                if n not in seen:
                    seen.add(n)
                    q.append(n)
        return None

    def base_of(d):
        while mons.get(d, {}).get("evolves_from"):
            d = mons[d]["evolves_from"]
        return d

    breed, evolve = [], []
    for d in sorted(mons):
        if d in acquired:
            continue
        m = mons[d]
        anc = nearest_acquired_ancestor(d)
        if anc is not None:
            kind = "trade-evolve" if m.get("method") == "trade-evo" else "evolve"
            evolve.append({
                "dex_no": d, "name": m["name"], "caught": bool(m["caught"]),
                "source_dex": anc, "source_name": mons[anc]["name"],
                "kind": kind, "ready": d in ready,
            })
            continue
        if base_of(d) in _UNBREEDABLE_BASE:
            continue
        des = nearest_acquired_descendant(d)
        if des is not None:
            breed.append({
                "dex_no": d, "name": m["name"], "caught": bool(m["caught"]),
                "source_dex": des, "source_name": mons[des]["name"],
                "kind": "breed", "ready": d in ready,
            })

    return {"breed": breed, "evolve": evolve}
