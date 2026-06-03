"""
scrape_missing_locations.py
Scrapes the Sevii Island locations that were missing from the original scraper,
then merges into catch_locations_data.py (replacing entries for these locations only).

Run:  python3 scrape_missing_locations.py
"""

import re, sys, time, os, html as html_module, sqlite3, importlib.util

KANTO_BASE = "https://www.serebii.net/pokearth/kanto/3rd/"

# Locations missing from the original scraper
MISSING_LOCATIONS = [
    ("Water Path",      "waterpath",    KANTO_BASE, None),
    ("Kindle Road",     "kindleroad",   KANTO_BASE, None),
    ("Tanoby Ruins",    "tanobyruins",  KANTO_BASE, None),
    ("Trainer Tower",   "trainertower", KANTO_BASE, None),
    ("One Island",      "oneisland",    KANTO_BASE, None),
    ("Four Island",     "fourisland",   KANTO_BASE, None),
    ("Five Island",     "fiveisland",   KANTO_BASE, None),
    ("Navel Rock",      "navelrock",    KANTO_BASE, None),
    ("Birth Island",    "birthisland",  KANTO_BASE, None),
]

ENC_CLASS_MAP = {
    "grass": "wild",
    "surf":  "surf",
    "fish":  "fish",
    "swarm": "rock-smash",
}
GAME_CLASS_MAP = {
    "firered": "firered", "leafgreen": "leafgreen",
    "ruby": "ruby", "sapphire": "sapphire", "emerald": "emerald",
}
ROD_NOTES = {"Old Rod": "Old Rod", "Good Rod": "Good Rod", "Super Rod": "Super Rod"}
REPLACEABLE_METHODS = {"wild", "surf", "fish", "safari", "rock-smash"}

import urllib.request, urllib.error

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
        "nidoran♀": 29, "nidoran(f)": 29, "nidoran&#9792;": 29,
        "nidoran♂": 32, "nidoran(m)": 32, "nidoran&#9794;": 32,
        "ho-oh": 250, "hooh": 250,
    })
    return m

def parse_page(html, base_location, method_override, name_map):
    results = []
    table_re  = re.compile(r'<table[^>]*class="(?:dextable|extradextable)"[^>]*>(.*?)</table>', re.DOTALL)
    header_re = re.compile(r'colspan="32" class="([^"]+)">(?:<a[^>]*>)?([^<]+)')
    name_re   = re.compile(r'class="name">([^<]+)</td>')
    rate_re   = re.compile(r'class="rate">([^<]+)</td>')

    section_labels, section_pos_map = {}, []
    for m_sec in re.finditer(r'<a name="([^"]+area\d+)[^"]*">', html, re.IGNORECASE):
        anchor = m_sec.group(1)
        after = html[m_sec.start():m_sec.start() + 400]
        area_m = re.search(r'Area\s+(\d+)', after, re.IGNORECASE)
        if area_m:
            section_labels[anchor] = f"Area {area_m.group(1)}"
    for anchor, label in section_labels.items():
        idx = html.find(f'name="{anchor}"')
        if idx != -1:
            section_pos_map.append((idx, label))
    section_pos_map.sort()

    def get_section_label(pos):
        label = None
        for sec_pos, sec_label in section_pos_map:
            if sec_pos <= pos:
                label = sec_label
        return label

    current_enc_class = current_enc_label = None
    for m in table_re.finditer(html):
        table_html, table_pos = m.group(1), m.start()
        headers = header_re.findall(table_html)
        if not headers:
            continue
        enc_class = enc_label = game = None
        for cls, label in headers:
            label = label.strip()
            if cls in ENC_CLASS_MAP:
                enc_class, enc_label = cls, label
            elif cls in GAME_CLASS_MAP:
                game = GAME_CLASS_MAP[cls]
        if enc_class is None:
            if current_enc_class and game:
                enc_class, enc_label = current_enc_class, current_enc_label
            else:
                continue
        else:
            current_enc_class, current_enc_label = enc_class, enc_label
        if game is None:
            continue
        method = ENC_CLASS_MAP[enc_class]
        if method_override and method == "wild":
            method = method_override
        notes = ROD_NOTES.get(enc_label) if method == "fish" else None
        sub_label = get_section_label(table_pos)
        location = f"{base_location} ({sub_label})" if sub_label else base_location
        names, rates = name_re.findall(table_html), rate_re.findall(table_html)
        for name, rate in zip(names[:min(len(names), len(rates))], rates[:min(len(names), len(rates))]):
            name_clean = html_module.unescape(name.strip())
            key = name_clean.lower()
            dex_no = name_map.get(key) or name_map.get(re.sub(r'[^a-z0-9]', '', key))
            if dex_no is None:
                print(f"  [WARN] Unknown: '{name_clean}' @ {location}", file=sys.stderr)
                continue
            results.append({"dex_no": dex_no, "game": game, "location": location,
                             "method": method, "notes": notes, "encounter_rate": rate.strip()})
    return results

def fmt(e):
    notes_r = f'"{e["notes"]}"' if e["notes"] else "None"
    rate_r  = f'"{e["encounter_rate"]}"' if e["encounter_rate"] else "None"
    return (f'    {{"dex_no": {e["dex_no"]}, "game": "{str(e["game"]).strip()}", '
            f'"location": "{str(e["location"]).strip()}", '
            f'"method": "{str(e["method"]).strip()}", '
            f'"notes": {notes_r}, "encounter_rate": {rate_r}}},')

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")
    name_map = build_name_map()

    # Scrape missing locations
    scraped = []
    scraped_location_names = set()
    for display, slug, base, override in MISSING_LOCATIONS:
        url = base + slug + ".shtml"
        print(f"Scraping {display} ...", file=sys.stderr)
        html = fetch(url)
        if html is None:
            print(f"  [SKIP] {url}", file=sys.stderr)
            continue
        entries = parse_page(html, display, override, name_map)
        print(f"  → {len(entries)} entries", file=sys.stderr)
        scraped.extend(entries)
        scraped_location_names.add(display)
        time.sleep(0.5)

    # Deduplicate scraped
    seen, deduped = set(), []
    for e in scraped:
        key = (e["dex_no"], e["game"], e["location"], e["method"], e["notes"], e["encounter_rate"])
        if key not in seen:
            seen.add(key)
            deduped.append(e)

    # Load existing data, remove entries for the locations we just scraped
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "catch_locations_data.py")
    spec = importlib.util.spec_from_file_location("catch_locations_data", data_path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Keep entries whose location is NOT one we just scraped, OR whose method is non-replaceable
    kept = []
    removed = 0
    for e in mod.CATCH_LOCATIONS:
        loc = str(e["location"]).strip()
        mth = str(e["method"]).strip()
        # Remove old encounter entries for locations we re-scraped
        if loc in scraped_location_names and mth in REPLACEABLE_METHODS:
            removed += 1
        else:
            kept.append(e)

    print(f"Removed {removed} old entries for re-scraped locations", file=sys.stderr)
    print(f"Adding {len(deduped)} new scraped entries", file=sys.stderr)

    all_entries = kept + deduped
    all_entries.sort(key=lambda e: (e["dex_no"], e["game"], e["location"],
                                    e["method"] or "", e["notes"] or ""))

    lines = [
        '"""', "catch_locations_data.py",
        "All Gen 3 catch locations for Pokémon 001–386.",
        "Games: firered, leafgreen, ruby, sapphire, emerald, colosseum, xd",
        "Methods: wild, surf, fish, gift, static, starter, safari, event, shadow,",
        "         breed, evolve, trade, trade-evo, rock-smash, palpark",
        "encounter_rate: exact percentage from Serebii per-route tables.",
        '"""', "", "CATCH_LOCATIONS = [",
    ]
    prev_dex = None
    for e in all_entries:
        if e["dex_no"] != prev_dex:
            if prev_dex is not None:
                lines.append("")
            lines.append(f"    # {e['dex_no']:03d}")
            prev_dex = e["dex_no"]
        lines.append(fmt(e))
    lines += ["]", ""]

    with open(data_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nWrote {len(all_entries)} total entries to {data_path}", file=sys.stderr)

if __name__ == "__main__":
    main()
