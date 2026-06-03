import os, secrets as _secrets

import sqlite3
from urllib.parse import urlparse
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, g
import models
import auth as _auth
import paths


GENERATIONS = {
    3: {
        "label": "Gen III",
        "title": "Pokédex",
        "db": "gen3.db",
        "seed": paths.bundled_resource_path("data/seed_gen3.db"),
        "max_dex": 386,
        "game_order": ["emerald", "firered", "leafgreen", "colosseum", "xd", "ruby", "sapphire"],
        "regions": ["kanto", "johto", "hoenn"],
        "version_groups": [["ruby", "sapphire", "emerald"], ["firered", "leafgreen"], ["colosseum", "xd"]],
    },
}

GAME_ABBR = {
    "ruby": "R", "sapphire": "S", "emerald": "E", "firered": "FR", "leafgreen": "LG",
    "colosseum": "Co", "xd": "XD",
}


def _gen_games_in_order(gen_cfg):
    ordered = [gm for grp in gen_cfg.get("version_groups", []) for gm in grp]
    for gm in gen_cfg["game_order"]:
        if gm not in ordered:
            ordered.append(gm)
    return ordered


_SEEDED_GENS = None
_SEEDED_GENS_LOCK = __import__("threading").Lock()


def _seeded_gens():
    global _SEEDED_GENS
    if _SEEDED_GENS is not None:
        return _SEEDED_GENS
    with _SEEDED_GENS_LOCK:
        if _SEEDED_GENS is not None:
            return _SEEDED_GENS
        seeded = set()
        for gen, cfg in GENERATIONS.items():
            seed = cfg["seed"]
            if not os.path.exists(seed):
                continue
            try:
                con = sqlite3.connect(seed)
                if con.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0] > 0:
                    seeded.add(gen)
                con.close()
            except sqlite3.Error:
                pass
        _SEEDED_GENS = seeded
    return _SEEDED_GENS


app = Flask(__name__)
app.secret_key = _secrets.token_hex(32)

_auth.init()


@app.context_processor
def _inject_globals():
    return {
        "is_admin": True,
        "current_gen": getattr(g, "gen", 3),
        "GENERATIONS": GENERATIONS,
        "seeded_gens": _seeded_gens(),
        "game_name": lambda gm: models._GAME_NAMES.get(gm, gm.title()),
        "csrf_token": "",
    }


@app.before_request
def _set_request_context():
    user = _auth.LOCAL_USER
    gen = session.get("gen", 3)
    if gen not in GENERATIONS or gen not in _seeded_gens():
        gen = 3
    g.gen = gen
    g.gen_cfg = GENERATIONS[gen]
    g.db_path = paths.user_db_path(GENERATIONS[gen]["db"])
    st = _auth.get_settings(user)
    full = set(GENERATIONS[gen]["game_order"])
    owned = st.get("games_owned")
    g.owned_games = full if owned is None else (set(owned) & full)
    g.use_glitches = bool(st.get("use_glitches", False))
    g.show_ready_to_obtain = bool(st.get("show_ready_to_obtain", False))
    extra = set()
    if st.get("bonus_disc_en") or st.get("pokemon_channel_pal"):
        extra.add(385)
    if st.get("bonus_disc_jp"):
        extra.add(251)
    g.extra_obtainable = extra
    g.setup_complete = st.get("setup_complete", True)


_VALID_GAMES = {gm for cfg in GENERATIONS.values() for gm in cfg["game_order"]}


@app.route("/settings", methods=["GET", "POST"])
def settings_view():
    user = _auth.current_user()
    all_games = [gm for cfg in GENERATIONS.values() for gm in cfg["game_order"]]
    welcome = request.args.get("welcome") == "1"
    if request.method == "POST":
        owned = [gm for gm in all_games if request.form.get(f"own_{gm}")]
        _auth.save_settings(
            user, owned,
            use_glitches=request.form.get("use_glitches") == "1",
            bonus_disc_en=request.form.get("bonus_disc_en") == "1",
            bonus_disc_jp=request.form.get("bonus_disc_jp") == "1",
            pokemon_channel_pal=request.form.get("pokemon_channel_pal") == "1",
            show_ready_to_obtain=request.form.get("show_ready_to_obtain") == "1",
        )
        return redirect(url_for("index") if request.form.get("welcome") == "1" else url_for("settings_view"))
    st = _auth.get_settings(user)
    reset_done = request.args.get("reset")
    owned = st.get("games_owned")
    owned_set = set(all_games) if owned is None else set(owned)
    return render_template(
        "settings.html",
        owned_set=owned_set,
        use_glitches=bool(st.get("use_glitches", False)),
        bonus_disc_en=bool(st.get("bonus_disc_en", False)),
        bonus_disc_jp=bool(st.get("bonus_disc_jp", False)),
        pokemon_channel_pal=bool(st.get("pokemon_channel_pal", False)),
        show_ready_to_obtain=bool(st.get("show_ready_to_obtain", False)),
        welcome=welcome,
        reset_done=reset_done,
        stats=models.stats(),
    )


@app.route("/settings/reset", methods=["POST"])
def settings_reset():
    n = models.reset_progress()
    return redirect(url_for("settings_view", reset=n))


@app.route("/switch-gen/<int:gen>")
def switch_gen(gen):
    if gen not in GENERATIONS or gen not in _seeded_gens():
        return redirect("/")
    session["gen"] = gen
    path = urlparse(request.referrer or "/").path or "/"
    if path.startswith("/pokemon/"):
        try:
            dex_no = int(path.split("/")[2])
        except (IndexError, ValueError):
            dex_no = 0
        if dex_no > GENERATIONS[gen]["max_dex"]:
            return redirect("/")
    return redirect(path)


@app.route("/")
def index():
    region = request.args.get("region", "")
    type_filter = request.args.get("type", "")
    tag = request.args.get("tag", "")
    caught_filter = request.args.get("caught", "")
    search = request.args.get("q", "")

    caught_bool = None
    if caught_filter == "yes":
        caught_bool = True
    elif caught_filter == "no":
        caught_bool = False

    pokemon = models.list_pokemon(
        region=region or None,
        type_filter=type_filter or None,
        tag=tag or None,
        caught=caught_bool,
        search=search or None,
    )
    s = models.stats()
    unobtainable = models.unobtainable_dex(owned=g.owned_games, glitches=g.use_glitches)
    derivable = models.derivable_dex() if g.show_ready_to_obtain else set()

    ordered_games = _gen_games_in_order(g.gen_cfg)
    avail = models.catchable_games_by_dex(ordered_games)
    versions = {d: "/".join(GAME_ABBR.get(gm, gm) for gm in gms) for d, gms in avail.items()}
    version_titles = {
        d: ", ".join(models._GAME_NAMES.get(gm, gm.title()) for gm in gms)
        for d, gms in avail.items()
    }
    return render_template(
        "index.html",
        pokemon=pokemon,
        stats=s,
        unobtainable=unobtainable,
        derivable=derivable,
        versions=versions,
        version_titles=version_titles,
        filters={"region": region, "type": type_filter, "tag": tag, "caught": caught_filter, "q": search},
    )


@app.route("/pokemon/<int:dex_no>")
def detail(dex_no):
    mon = models.get_pokemon(dex_no)
    if not mon:
        return "Not found", 404
    max_dex = g.gen_cfg["max_dex"]
    prev_mon = models.get_pokemon(dex_no - 1) if dex_no > 1 else None
    next_mon = models.get_pokemon(dex_no + 1) if dex_no < max_dex else None
    pre_evo = models.get_pokemon(mon["evolves_from"]) if mon["evolves_from"] else None
    s = models.stats()
    game_order = g.gen_cfg["game_order"]
    owned = g.owned_games
    raw_locs = models.get_catch_locations(dex_no)
    catch_locations_by_game = {
        game: [r for r in raw_locs if r["game"] == game]
        for game in game_order
        if (owned is None or game in owned) and any(r["game"] == game for r in raw_locs)
    }
    unobtainable = models.unobtainable_dex(owned=owned, glitches=g.use_glitches)
    return render_template(
        "detail.html",
        mon=mon,
        pre_evo=pre_evo,
        prev_mon=prev_mon,
        next_mon=next_mon,
        stats=s,
        catch_locations_by_game=catch_locations_by_game,
        is_unobtainable=mon["dex_no"] in unobtainable,
    )


@app.route("/pokemon/<int:dex_no>/toggle", methods=["POST"])
def toggle(dex_no):
    raw_game = request.form.get("source_game") or None
    source_game = raw_game if raw_game in _VALID_GAMES else None
    toggled = models.toggle_caught(dex_no, source_game)
    if toggled is None:
        return "Not found", 404
    next_url = request.args.get("next")
    if next_url and next_url.startswith("/") and not next_url.startswith("//"):
        return redirect(next_url)
    return redirect(url_for("detail", dex_no=dex_no))


@app.route("/pokemon/<int:dex_no>/notes", methods=["POST"])
def notes(dex_no):
    user_notes = request.form.get("user_notes", "")[:2000]
    raw_game = request.form.get("source_game") or None
    source_game = raw_game if raw_game in _VALID_GAMES else None
    models.save_notes(dex_no, user_notes, source_game)
    return redirect(url_for("detail", dex_no=dex_no))


@app.route("/stats")
def stats_view():
    user = _auth.current_user()
    st   = _auth.get_settings(user)
    seeded = _seeded_gens()

    gen_stats = []
    orig_db_path  = g.db_path
    orig_owned    = g.owned_games
    try:
        for gen_num in sorted(GENERATIONS):
            if gen_num not in seeded:
                continue
            cfg = GENERATIONS[gen_num]
            g.db_path     = paths.user_db_path(cfg["db"])
            full          = set(cfg["game_order"])
            owned_raw     = st.get("games_owned")
            g.owned_games = full if owned_raw is None else (set(owned_raw) & full)
            s = models.stats(game_order=cfg["game_order"])
            s["gen"]       = gen_num
            s["gen_label"] = cfg["label"]
            gen_stats.append(s)
    finally:
        g.db_path     = orig_db_path
        g.owned_games = orig_owned

    return render_template("stats.html", gen_stats=gen_stats, stats=models.stats())


@app.route("/routes")
def routes_view():
    missing_by_game = models.list_missing_by_game()
    game_counts = {game: sum(len(v) for v in locs.values()) for game, locs in missing_by_game.items()}
    games_sorted = sorted(game_counts.items(), key=lambda x: x[1], reverse=True)
    s = models.stats()
    unobtainable = models.unobtainable_dex(owned=g.owned_games, glitches=g.use_glitches)
    return render_template("routes.html", missing_by_game=missing_by_game, games_sorted=games_sorted,
                           unobtainable=unobtainable, stats=s)


@app.route("/trades")
def trades_view():
    trade_evos = models.list_trade_evos()
    s = models.stats()
    obtainable = models.obtainable_dex(owned=g.owned_games, glitches=g.use_glitches)
    unobtainable = set(range(1, g.gen_cfg["max_dex"] + 1)) - obtainable
    item_summary = models.trade_item_summary(trade_evos, obtainable)
    return render_template("trades.html", trade_evos=trade_evos, stats=s,
                           unobtainable=unobtainable, item_summary=item_summary)


@app.route("/boxes")
def boxes_view():
    mode = request.args.get("mode", "60") if g.gen == 3 else "30"
    if mode == "30":
        boxes = models.list_by_box(box_size=30, cols=6)
        cols = 6
    else:
        boxes = models.list_by_box(box_size=60, cols=12)
        cols = 12
        mode = "60"
    s = models.stats()
    unobtainable = models.unobtainable_dex(owned=g.owned_games, glitches=g.use_glitches)
    derivable = models.derivable_dex() if g.show_ready_to_obtain else set()
    return render_template(
        "boxes.html",
        boxes=boxes,
        unobtainable=unobtainable,
        derivable=derivable,
        stats=s,
        mode=mode,
        cols=cols,
        box_size=int(mode),
        max_dex=g.gen_cfg["max_dex"],
    )


def _walkthrough_order(user):
    from walkthrough_data import GAME_CONFIGS
    all_games = list(GAME_CONFIGS.keys())
    st = _auth.get_settings(user)
    owned_raw = st.get("games_owned")
    owned = set(owned_raw) if owned_raw is not None else None
    games = [gk for gk in all_games if owned is None or gk in owned]
    saved = st.get("walkthrough_order", [])
    ordered = [gk for gk in saved if gk in games]
    for gk in games:
        if gk not in ordered:
            ordered.append(gk)
    return ordered


@app.route("/walkthrough")
def walkthrough_index():
    from walkthrough_data import GAME_CONFIGS
    user = _auth.current_user()
    order = _walkthrough_order(user)
    ordered_configs = [(gk, GAME_CONFIGS[gk]) for gk in order]
    counts = models.walkthrough_mon_counts(order)
    return render_template("walkthrough_index.html", ordered_configs=ordered_configs, counts=counts, stats=models.stats())


@app.route("/walkthrough/order", methods=["POST"])
def walkthrough_order_save():
    user = _auth.current_user()
    from walkthrough_data import GAME_CONFIGS
    data = request.get_json(silent=True) or {}
    order = [gk for gk in data.get("order", []) if gk in GAME_CONFIGS]
    _auth.save_walkthrough_order(user, order)
    counts = models.walkthrough_mon_counts(order)
    return jsonify({"ok": True, "counts": counts})


@app.route("/walkthrough/recommend")
def walkthrough_recommend():
    from walkthrough_data import GAME_CONFIGS
    user = _auth.current_user()
    owned_raw = _auth.get_settings(user).get("games_owned")
    owned = set(owned_raw) if owned_raw is not None else None
    walkthrough_games = set(GAME_CONFIGS.keys())
    if owned is not None:
        walkthrough_games &= owned
    rec = models.recommend_walkthrough_order(walkthrough_games)
    order = [r["game"] for r in rec]
    gains = {r["game"]: r["new"] for r in rec}
    return jsonify({
        "order": order,
        "gains": gains,
        "labels": {gk: GAME_CONFIGS[gk]["label"] for gk in order},
    })


@app.route("/walkthrough/<game>")
def walkthrough_view(game):
    from walkthrough_data import GAME_CONFIGS
    cfg = GAME_CONFIGS.get(game)
    if not cfg:
        return "Not found", 404

    user = _auth.current_user()
    order = _walkthrough_order(user)
    full_seq_configs = [
        {"game": gk, "label": GAME_CONFIGS[gk]["label"], "story_areas": GAME_CONFIGS[gk]["story_areas"]}
        for gk in order
    ]

    gen = cfg["gen"]
    gen_cfg = GENERATIONS[gen]
    owned_raw = _auth.get_settings(user).get("games_owned")
    full_games = set(gen_cfg["game_order"])
    owned_games = full_games if owned_raw is None else (set(owned_raw) & full_games)

    orig_db_path  = g.db_path
    orig_owned    = g.owned_games
    try:
        g.db_path     = paths.user_db_path(gen_cfg["db"])
        g.owned_games = owned_games

        sections = models.walkthrough_sections(
            game, cfg["story_areas"], order,
            catch_qty_overrides=cfg.get("catch_qty_overrides"),
            full_sequence_configs=full_seq_configs,
        )
        total    = sum(len(s["pokemon"]) for s in sections)
        caught   = sum(1 for s in sections for p in s["pokemon"] if p["caught"])
        derivable = models.derivable_dex() if g.show_ready_to_obtain else set()
    finally:
        g.db_path     = orig_db_path
        g.owned_games = orig_owned

    return render_template(
        "walkthrough.html",
        sections=sections,
        game=game,
        game_label=cfg["label"],
        game_gen=cfg["gen"],
        total=total,
        caught=caught,
        derivable=derivable,
        stats=models.stats(),
    )


@app.route("/walkthrough/afterward")
def walkthrough_afterward_view():
    from walkthrough_data import GAME_CONFIGS
    user = _auth.current_user()
    order = _walkthrough_order(user)
    if not order:
        return render_template("walkthrough_afterward.html", data={"evolve": [], "breed": []},
                               game_gen=3, total=0, caught=0, stats=models.stats())

    gen = sorted({GAME_CONFIGS[gk]["gen"] for gk in order})[0]
    gen_cfg = GENERATIONS[gen]
    owned_raw = _auth.get_settings(user).get("games_owned")
    full_games = set(gen_cfg["game_order"])
    owned_games = full_games if owned_raw is None else (set(owned_raw) & full_games)

    orig_db_path = g.db_path
    orig_owned   = g.owned_games
    try:
        g.db_path     = paths.user_db_path(gen_cfg["db"])
        g.owned_games = owned_games
        data = models.walkthrough_optional(set(order))
    finally:
        g.db_path     = orig_db_path
        g.owned_games = orig_owned

    items = data["evolve"] + data["breed"]
    total = len(items)
    caught = sum(1 for it in items if it["caught"])
    return render_template(
        "walkthrough_afterward.html",
        data=data,
        game_gen=gen,
        total=total,
        caught=caught,
        stats=models.stats(),
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=os.environ.get("FLASK_DEBUG") == "1")
