"""
patch_missing_sevii.py
Adds missing Sevii Island entries to catch_locations_data.py:
  - Sevault Canyon wild encounters (Larvitar etc.)
  - Tanoby Ruins Unown
  - Prof. Oak post-game Johto starter gifts (Chikorita, Cyndaquil, Totodile)
"""

import os
import importlib.util

NEW_ENTRIES = [
    # ── Prof. Oak post-game gift (Johto starters) ────────────────────────────
    # After completing Sevii Islands story, Oak gives one Johto starter per save
    {"dex_no": 152, "game": "firered",   "location": "Pallet Town (Prof. Oak)",  "method": "gift",  "notes": "Post-game gift; one per save",  "encounter_rate": None},
    {"dex_no": 152, "game": "leafgreen", "location": "Pallet Town (Prof. Oak)",  "method": "gift",  "notes": "Post-game gift; one per save",  "encounter_rate": None},
    {"dex_no": 155, "game": "firered",   "location": "Pallet Town (Prof. Oak)",  "method": "gift",  "notes": "Post-game gift; one per save",  "encounter_rate": None},
    {"dex_no": 155, "game": "leafgreen", "location": "Pallet Town (Prof. Oak)",  "method": "gift",  "notes": "Post-game gift; one per save",  "encounter_rate": None},
    {"dex_no": 158, "game": "firered",   "location": "Pallet Town (Prof. Oak)",  "method": "gift",  "notes": "Post-game gift; one per save",  "encounter_rate": None},
    {"dex_no": 158, "game": "leafgreen", "location": "Pallet Town (Prof. Oak)",  "method": "gift",  "notes": "Post-game gift; one per save",  "encounter_rate": None},

    # ── Tanoby Ruins (Sevii Island 7) — Unown ───────────────────────────────
    {"dex_no": 201, "game": "firered",   "location": "Tanoby Ruins",             "method": "wild",  "notes": "All 28 forms across 7 chambers", "encounter_rate": "varies"},
    {"dex_no": 201, "game": "leafgreen", "location": "Tanoby Ruins",             "method": "wild",  "notes": "All 28 forms across 7 chambers", "encounter_rate": "varies"},

    # ── Sevault Canyon (Sevii Island 7) ─────────────────────────────────────
    # FireRed
    {"dex_no":  22, "game": "firered",   "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "10%"},
    {"dex_no":  52, "game": "firered",   "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "10%"},
    {"dex_no":  53, "game": "firered",   "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "5%"},
    {"dex_no":  74, "game": "firered",   "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "20%"},
    {"dex_no":  74, "game": "firered",   "location": "Sevault Canyon",           "method": "rock-smash", "notes": None, "encounter_rate": "65%"},
    {"dex_no":  75, "game": "firered",   "location": "Sevault Canyon",           "method": "rock-smash", "notes": None, "encounter_rate": "35%"},
    {"dex_no":  95, "game": "firered",   "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "5%"},
    {"dex_no": 104, "game": "firered",   "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "10%"},
    {"dex_no": 105, "game": "firered",   "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "10%"},
    {"dex_no": 227, "game": "firered",   "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "5%"},
    {"dex_no": 231, "game": "firered",   "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "20%"},
    {"dex_no": 246, "game": "firered",   "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "5%"},
    # LeafGreen (no Skarmory; Fearow 15%)
    {"dex_no":  22, "game": "leafgreen", "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "15%"},
    {"dex_no":  52, "game": "leafgreen", "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "10%"},
    {"dex_no":  53, "game": "leafgreen", "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "5%"},
    {"dex_no":  74, "game": "leafgreen", "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "20%"},
    {"dex_no":  74, "game": "leafgreen", "location": "Sevault Canyon",           "method": "rock-smash", "notes": None, "encounter_rate": "65%"},
    {"dex_no":  75, "game": "leafgreen", "location": "Sevault Canyon",           "method": "rock-smash", "notes": None, "encounter_rate": "35%"},
    {"dex_no":  95, "game": "leafgreen", "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "5%"},
    {"dex_no": 104, "game": "leafgreen", "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "10%"},
    {"dex_no": 105, "game": "leafgreen", "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "10%"},
    {"dex_no": 231, "game": "leafgreen", "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "20%"},
    {"dex_no": 246, "game": "leafgreen", "location": "Sevault Canyon",           "method": "wild",  "notes": None,  "encounter_rate": "5%"},
]


def fmt(e):
    notes_r = f'"{e["notes"]}"' if e["notes"] else "None"
    rate_r  = f'"{e["encounter_rate"]}"' if e["encounter_rate"] else "None"
    return (
        f'    {{"dex_no": {e["dex_no"]}, "game": "{e["game"]}", '
        f'"location": "{e["location"]}", '
        f'"method": "{e["method"]}", '
        f'"notes": {notes_r}, '
        f'"encounter_rate": {rate_r}}},'
    )


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "catch_locations_data.py")

    spec = importlib.util.spec_from_file_location("catch_locations_data", data_path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    existing = list(mod.CATCH_LOCATIONS)

    # Deduplicate: skip any new entry that already exists
    existing_keys = {
        (e["dex_no"], e["game"], e["location"], e["method"])
        for e in existing
    }
    to_add = [e for e in NEW_ENTRIES
              if (e["dex_no"], e["game"], e["location"], e["method"]) not in existing_keys]

    print(f"Adding {len(to_add)} new entries (skipping {len(NEW_ENTRIES)-len(to_add)} duplicates)")

    all_entries = existing + to_add
    all_entries.sort(key=lambda e: (e["dex_no"], e["game"], e["location"],
                                    e["method"] or "", e["notes"] or ""))

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

    with open(data_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Wrote {len(all_entries)} total entries to {data_path}")


if __name__ == "__main__":
    main()
