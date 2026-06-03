"""
scrape_gen3_locations.py
Scrapes Serebii's Gen III route pages, then merges with the existing
catch_locations_data.py (preserving gift/static/evolve/breed/shadow/event
entries which have no encounter rate).

Run:  python3 scrape_gen3_locations.py
This overwrites catch_locations_data.py in place.
"""

import re
import sys
import time
import sqlite3
import urllib.request
import urllib.error
import os
import html as html_module

# ── Serebii URL bases ─────────────────────────────────────────────────────────
KANTO_BASE = "https://www.serebii.net/pokearth/kanto/3rd/"
HOENN_BASE = "https://www.serebii.net/pokearth/hoenn/3rd/"

# ── Location definitions ──────────────────────────────────────────────────────
# (display_name, slug, base_url, method_override)
# method_override=None  → use normal grass/surf/fish/rock-smash mapping
# method_override="safari" → force all grass encounters to safari method

KANTO_LOCATIONS = [
    *[(f"Route {i}", f"route{i}", KANTO_BASE, None) for i in range(1, 26)],
    ("Viridian Forest",  "viridianforest", KANTO_BASE, None),
    ("Mt. Moon",         "mt.moon",        KANTO_BASE, None),
    ("Diglett's Cave",   "diglett'scave",  KANTO_BASE, None),
    ("Rock Tunnel",      "rocktunnel",     KANTO_BASE, None),
    ("Pokémon Tower",    "pokemontower",   KANTO_BASE, None),
    ("Safari Zone",      "safarizone",     KANTO_BASE, "safari"),
    ("Pokémon Mansion",  "pokemonmansion", KANTO_BASE, None),
    ("Seafoam Islands",  "seafoamislands", KANTO_BASE, None),
    ("Power Plant",      "powerplant",     KANTO_BASE, None),
    ("Cerulean Cave",    "ceruleancave",   KANTO_BASE, None),
    ("Victory Road",     "victoryroad",    KANTO_BASE, None),
    ("Mt. Ember",        "mt.ember",       KANTO_BASE, None),
    ("Berry Forest",     "berryforest",    KANTO_BASE, None),
    ("Icefall Cave",     "icefallcave",    KANTO_BASE, None),
    ("Dotted Hole",      "dottedhole",     KANTO_BASE, None),
    ("Lost Cave",        "lostcave",       KANTO_BASE, None),
    ("Pattern Bush",     "patternbush",    KANTO_BASE, None),
    ("Altering Cave",    "alteringcave",   KANTO_BASE, None),
]

HOENN_LOCATIONS = [
    *[(f"Route {i}", f"route{i}", HOENN_BASE, None) for i in range(101, 135)],
    ("Petalburg Woods",  "petalburgwoods", HOENN_BASE, None),
    ("Granite Cave",     "granitecave",    HOENN_BASE, None),
    ("Fiery Path",       "fierypath",      HOENN_BASE, None),
    ("Mt. Chimney",      "mt.chimney",     HOENN_BASE, None),
    ("Jagged Pass",      "jaggedpass",     HOENN_BASE, None),
    ("Meteor Falls",     "meteorfalls",    HOENN_BASE, None),
    ("New Mauville",     "newmauville",    HOENN_BASE, None),
    ("Safari Zone",      "safarizone",     HOENN_BASE, "safari"),
    ("Mt. Pyre",         "mt.pyre",        HOENN_BASE, None),
    ("Abandoned Ship",   "abandonedship",  HOENN_BASE, None),
    ("Shoal Cave",       "shoalcave",      HOENN_BASE, None),
    ("Seafloor Cavern",  "seafloorcavern", HOENN_BASE, None),
    ("Cave of Origin",   "caveoforigin",   HOENN_BASE, None),
    ("Victory Road",     "victoryroad",    HOENN_BASE, None),
    ("Sky Pillar",       "skypillar",      HOENN_BASE, None),
    ("Scorched Slab",    "scorchedslab",   HOENN_BASE, None),
    ("Magma Hideout",    "magmahideout",   HOENN_BASE, None),
    ("Artisan Cave",     "artisancave",    HOENN_BASE, None),
    ("Mirage Cave",      "miragecave",     HOENN_BASE, None),
    ("Sootopolis City",  "sootopoliscity", HOENN_BASE, None),
]

# ── CSS class → encounter method ──────────────────────────────────────────────
ENC_CLASS_MAP = {
    "grass":  "wild",
    "surf":   "surf",
    "fish":   "fish",
    "swarm":  "rock-smash",   # Serebii uses "swarm" for rock-smash in Gen 3
}

GAME_CLASS_MAP = {
    "firered":  "firered",
    "leafgreen": "leafgreen",
    "ruby":     "ruby",
    "sapphire": "sapphire",
    "emerald":  "emerald",
}

ROD_NOTES = {
    "Old Rod":   "Old Rod",
    "Good Rod":  "Good Rod",
    "Super Rod": "Super Rod",
}

# Methods whose entries we will REPLACE with scraped data
REPLACEABLE_METHODS = {"wild", "surf", "fish", "safari", "rock-smash"}

# ── Name → dex_no mapping ─────────────────────────────────────────────────────
def build_name_map():
    con = sqlite3.connect("data/seed_gen3.db")
    rows = con.execute("SELECT dex_no, name FROM pokemon").fetchall()
    con.close()
    m = {}
    for dex_no, name in rows:
        m[name.lower()] = dex_no
        m[re.sub(r'[^a-z0-9]', '', name.lower())] = dex_no
    m.update({
        "mr. mime": 122, "mr.mime": 122, "mrmime": 122,
        "farfetch'd": 83, "farfetchd": 83,
        # HTML entity forms (&#9794; = ♂, &#9792; = ♀)
        "nidoran♀": 29, "nidoran(f)": 29, "nidoran&#9792;": 29,
        "nidoran♂": 32, "nidoran(m)": 32, "nidoran&#9794;": 32,
        "ho-oh": 250, "hooh": 250,
    })
    return m

# ── HTTP fetch ────────────────────────────────────────────────────────────────
def fetch(url, retries=3):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; pokedex-tracker/1.0)"}
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.read().decode("latin-1")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
        except Exception as ex:
            print(f"  [ERR] {ex}", file=sys.stderr)
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    return None

# ── Parse a Serebii route page ────────────────────────────────────────────────
def parse_page(html, base_location, method_override, name_map):
    """
    Returns list of dicts: {dex_no, game, location, method, notes, encounter_rate}.
    base_location: human-readable name (e.g. "Route 1", "Safari Zone")
    method_override: if "safari", all grass encounters become safari method.
    """
    results = []

    table_re = re.compile(
        r'<table[^>]*class="(?:dextable|extradextable)"[^>]*>(.*?)</table>',
        re.DOTALL
    )
    header_re = re.compile(r'colspan="32" class="([^"]+)">(?:<a[^>]*>)?([^<]+)')
    name_re   = re.compile(r'class="name">([^<]+)</td>')
    rate_re   = re.compile(r'class="rate">([^<]+)</td>')

    # Detect multi-section pages (e.g. Safari Zone areas)
    # Serebii uses anchors like <a name="joh-area1"> followed by "Area 1" text nearby
    section_labels = {}
    for m_sec in re.finditer(r'<a name="([^"]+area\d+)[^"]*">', html, re.IGNORECASE):
        anchor = m_sec.group(1)
        # Look for "Area N" text within the next 400 chars
        after = html[m_sec.start():m_sec.start() + 400]
        area_m = re.search(r'Area\s+(\d+)', after, re.IGNORECASE)
        if area_m:
            section_labels[anchor] = f"Area {area_m.group(1)}"

    # If multi-section, build a map of character-position → section label
    # so we can tag each table with the right sub-location
    section_pos_map = []
    for anchor, label in section_labels.items():
        idx = html.find(f'name="{anchor}"')
        if idx != -1:
            section_pos_map.append((idx, label))
    section_pos_map.sort()

    def get_section_label(pos):
        """Return sub-section label for a table at this string position."""
        label = None
        for sec_pos, sec_label in section_pos_map:
            if sec_pos <= pos:
                label = sec_label
        return label

    current_enc_class = None
    current_enc_label = None

    for m in table_re.finditer(html):
        table_html = m.group(1)
        table_pos  = m.start()

        headers = header_re.findall(table_html)
        if not headers:
            continue

        enc_class  = None
        enc_label  = None
        game       = None

        for cls, label in headers:
            label = label.strip()
            if cls in ENC_CLASS_MAP:
                enc_class = cls
                enc_label = label
            elif cls in GAME_CLASS_MAP:
                game = GAME_CLASS_MAP[cls]

        # If this table has no encounter type header, inherit from previous
        if enc_class is None:
            if current_enc_class and game:
                enc_class = current_enc_class
                enc_label = current_enc_label
            else:
                continue
        else:
            current_enc_class = enc_class
            current_enc_label = enc_label

        if game is None:
            continue

        method = ENC_CLASS_MAP[enc_class]
        if method_override and method == "wild":
            method = method_override

        # Notes: rod label for fishing
        notes = ROD_NOTES.get(enc_label) if method == "fish" else None

        # Determine location string
        sub_label = get_section_label(table_pos)
        location  = f"{base_location} ({sub_label})" if sub_label else base_location

        names = name_re.findall(table_html)
        rates = rate_re.findall(table_html)

        pairs = min(len(names), len(rates))
        for name, rate in zip(names[:pairs], rates[:pairs]):
            name_clean = html_module.unescape(name.strip())
            key = name_clean.lower()
            dex_no = (name_map.get(key)
                      or name_map.get(re.sub(r'[^a-z0-9]', '', key)))
            if dex_no is None:
                print(f"  [WARN] Unknown: '{name_clean}' @ {location}", file=sys.stderr)
                continue
            results.append({
                "dex_no":         dex_no,
                "game":           game,
                "location":       location,
                "method":         method,
                "notes":          notes,
                "encounter_rate": rate.strip(),
            })

    return results

# ── Load existing non-replaceable entries ─────────────────────────────────────
def load_existing_non_encounter():
    """
    Import current catch_locations_data.CATCH_LOCATIONS and return only the
    entries whose method is NOT in REPLACEABLE_METHODS (i.e. gift, starter,
    static, evolve, breed, trade, trade-evo, event, shadow, palpark).
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "catch_locations_data",
        os.path.join(os.path.dirname(__file__), "catch_locations_data.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return [e for e in mod.CATCH_LOCATIONS
            if str(e["method"]).strip() not in REPLACEABLE_METHODS]

# ── Format a single entry ─────────────────────────────────────────────────────
def fmt(e):
    notes_r = f'"{e["notes"]}"' if e["notes"] else "None"
    rate_r  = f'"{e["encounter_rate"]}"' if e["encounter_rate"] else "None"
    game    = str(e["game"]).strip()
    loc     = str(e["location"]).strip()
    method  = str(e["method"]).strip()
    return (
        f'    {{"dex_no": {e["dex_no"]}, "game": "{game}", '
        f'"location": "{loc}", '
        f'"method": "{method}", '
        f'"notes": {notes_r}, '
        f'"encounter_rate": {rate_r}}},'
    )

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")

    name_map = build_name_map()

    # ── 1. Scrape encounter data from Serebii ──────────────────────────────
    scraped = []
    skipped = []
    all_locs = KANTO_LOCATIONS + HOENN_LOCATIONS
    total    = len(all_locs)

    for i, (display, slug, base, override) in enumerate(all_locs, 1):
        url = base + slug + ".shtml"
        print(f"[{i:3}/{total}] {display} ...", file=sys.stderr)
        html = fetch(url)
        if html is None:
            print(f"  [SKIP] {url}", file=sys.stderr)
            skipped.append(display)
            continue
        entries = parse_page(html, display, override, name_map)
        print(f"  → {len(entries)} encounter entries", file=sys.stderr)
        scraped.extend(entries)
        time.sleep(0.4)

    # ── 2. Deduplicate scraped entries ─────────────────────────────────────
    seen = set()
    deduped_scraped = []
    for e in scraped:
        key = (e["dex_no"], e["game"], e["location"], e["method"],
               e["notes"], e["encounter_rate"])
        if key not in seen:
            seen.add(key)
            deduped_scraped.append(e)

    # ── 3. Load preserved non-encounter entries ────────────────────────────
    print("Loading existing non-encounter entries ...", file=sys.stderr)
    preserved = load_existing_non_encounter()
    print(f"  → {len(preserved)} preserved entries", file=sys.stderr)

    # ── 4. Merge and sort by dex_no ────────────────────────────────────────
    all_entries = deduped_scraped + preserved
    all_entries.sort(key=lambda e: (e["dex_no"], e["game"], e["location"],
                                     e["method"] or "", e["notes"] or ""))

    # ── 5. Write output file ───────────────────────────────────────────────
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "catch_locations_data.py")

    lines = [
        '"""',
        "catch_locations_data.py",
        "All Gen 3 catch locations for Pokémon 001–386.",
        "Games: firered, leafgreen, ruby, sapphire, emerald, colosseum, xd",
        "Methods: wild, surf, fish, gift, static, starter, safari, event, shadow,",
        "         breed, evolve, trade, trade-evo, rock-smash, palpark",
        "encounter_rate: exact percentage from Serebii per-route tables.",
        '"""',
        "",
        "CATCH_LOCATIONS = [",
    ]

    prev_dex = None
    for e in all_entries:
        if e["dex_no"] != prev_dex:
            if prev_dex is not None:
                lines.append("")
            lines.append(f"    # {e['dex_no']:03d}")
            prev_dex = e["dex_no"]
        lines.append(fmt(e))

    lines.append("]")
    lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nWrote {len(all_entries)} total entries to {out_path}", file=sys.stderr)
    print(f"  Scraped (encounter):  {len(deduped_scraped)}", file=sys.stderr)
    print(f"  Preserved (non-enc):  {len(preserved)}", file=sys.stderr)
    if skipped:
        print(f"  Skipped ({len(skipped)}): {', '.join(skipped)}", file=sys.stderr)

if __name__ == "__main__":
    main()
