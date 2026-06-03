"""
update_colo_xd.py
Replaces all game="colosseum" and game="xd" entries in catch_locations_data.py
with the complete, accurate list scraped from Serebii.

Run:  python3 update_colo_xd.py
"""

import os
import importlib.util

REPLACEABLE_GAMES = {"colosseum", "xd"}

# ── Complete Colosseum data ───────────────────────────────────────────────────

COLOSSEUM = [
    # Starters
    {"dex_no": 196, "game": "colosseum", "location": "Wes's partner",         "method": "starter", "notes": "Wes begins with Espeon as partner",         "encounter_rate": None},
    {"dex_no": 197, "game": "colosseum", "location": "Wes's partner",         "method": "starter", "notes": "Wes begins with Umbreon as partner",         "encounter_rate": None},

    # Gifts
    {"dex_no": 311, "game": "colosseum", "location": "Pyrite City",           "method": "gift",    "notes": "From Duking (Plusle gift)",                 "encounter_rate": None},
    {"dex_no": 250, "game": "colosseum", "location": "Mt. Battle",            "method": "gift",    "notes": "Clear all 100 battles; Lv 70",              "encounter_rate": None},

    # Events
    {"dex_no": 251, "game": "colosseum", "location": "Bonus Disc (Japan)",    "method": "event",   "notes": "Japanese Colosseum Bonus Disc only",        "encounter_rate": None},
    {"dex_no": 385, "game": "colosseum", "location": "Bonus Disc (US)",       "method": "event",   "notes": "North American Colosseum Bonus Disc only",  "encounter_rate": None},

    # E-Card (Japan only)
    {"dex_no": 175, "game": "colosseum", "location": "Phenac City (E-Reader)","method": "event",   "notes": "Japan: E-Card Reader only",                 "encounter_rate": None},
    {"dex_no": 179, "game": "colosseum", "location": "Phenac City (E-Reader)","method": "event",   "notes": "Japan: E-Card Reader only",                 "encounter_rate": None},
    {"dex_no": 212, "game": "colosseum", "location": "Phenac City (E-Reader)","method": "event",   "notes": "Japan: E-Card Reader only",                 "encounter_rate": None},

    # Shadow Pokémon (48)
    {"dex_no": 153, "game": "colosseum", "location": "Phenac City",           "method": "shadow",  "notes": "Mystery Troop Verde",                       "encounter_rate": None},
    {"dex_no": 156, "game": "colosseum", "location": "Phenac City",           "method": "shadow",  "notes": "Mystery Troop Rosso",                       "encounter_rate": None},
    {"dex_no": 159, "game": "colosseum", "location": "Phenac City",           "method": "shadow",  "notes": "Mystery Troop Bluno",                       "encounter_rate": None},
    {"dex_no": 162, "game": "colosseum", "location": "Pyrite City",           "method": "shadow",  "notes": "Rogue Cail",                                "encounter_rate": None},
    {"dex_no": 164, "game": "colosseum", "location": "Pyrite City",           "method": "shadow",  "notes": "Rider Nover",                               "encounter_rate": None},
    {"dex_no": 166, "game": "colosseum", "location": "The Under",             "method": "shadow",  "notes": "Cipher Peon Kloak",                         "encounter_rate": None},
    {"dex_no": 168, "game": "colosseum", "location": "Shadow PKMN Lab",       "method": "shadow",  "notes": "Cipher Peon Lesar",                         "encounter_rate": None},
    {"dex_no": 176, "game": "colosseum", "location": "Outskirt Stand",        "method": "shadow",  "notes": "Cipher Peon Grunt (fake)",                  "encounter_rate": None},
    {"dex_no": 180, "game": "colosseum", "location": "Pyrite City",           "method": "shadow",  "notes": "Performer Diogo",                           "encounter_rate": None},
    {"dex_no": 185, "game": "colosseum", "location": "Pyrite Town",           "method": "shadow",  "notes": "Cipher Admin Miror B.",                     "encounter_rate": None},
    {"dex_no": 188, "game": "colosseum", "location": "Pyrite City",           "method": "shadow",  "notes": "Rider Leba",                                "encounter_rate": None},
    {"dex_no": 190, "game": "colosseum", "location": "Shadow PKMN Lab",       "method": "shadow",  "notes": "Cipher Peon Cole",                          "encounter_rate": None},
    {"dex_no": 192, "game": "colosseum", "location": "Realgam Tower",         "method": "shadow",  "notes": "Cipher Peon Baila",                         "encounter_rate": None},
    {"dex_no": 193, "game": "colosseum", "location": "Pyrite Town",           "method": "shadow",  "notes": "Cipher Peon Nore",                          "encounter_rate": None},
    {"dex_no": 195, "game": "colosseum", "location": "Pyrite City",           "method": "shadow",  "notes": "Bandana Guy Divel",                         "encounter_rate": None},
    {"dex_no": 198, "game": "colosseum", "location": "Shadow PKMN Lab",       "method": "shadow",  "notes": "Cipher Peon Lare",                          "encounter_rate": None},
    {"dex_no": 200, "game": "colosseum", "location": "Pyrite City",           "method": "shadow",  "notes": "Rider Vant",                                "encounter_rate": None},
    {"dex_no": 205, "game": "colosseum", "location": "Shadow PKMN Lab",       "method": "shadow",  "notes": "Cipher Peon Vana",                          "encounter_rate": None},
    {"dex_no": 206, "game": "colosseum", "location": "Pyrite Cave",           "method": "shadow",  "notes": "Rider Sosh",                                "encounter_rate": None},
    {"dex_no": 207, "game": "colosseum", "location": "The Under",             "method": "shadow",  "notes": "Hunter Frena",                              "encounter_rate": None},
    {"dex_no": 210, "game": "colosseum", "location": "Shadow PKMN Lab",       "method": "shadow",  "notes": "Cipher Peon Tanie",                         "encounter_rate": None},
    {"dex_no": 211, "game": "colosseum", "location": "Pyrite Cave",           "method": "shadow",  "notes": "Hunter Doken",                              "encounter_rate": None},
    {"dex_no": 213, "game": "colosseum", "location": "Deep Colosseum",        "method": "shadow",  "notes": "Deep King Agnol",                           "encounter_rate": None},
    {"dex_no": 214, "game": "colosseum", "location": "Realgam Tower",         "method": "shadow",  "notes": "Cipher Peon Dioge",                         "encounter_rate": None},
    {"dex_no": 215, "game": "colosseum", "location": "The Under",             "method": "shadow",  "notes": "Rider Nelis",                               "encounter_rate": None},
    {"dex_no": 217, "game": "colosseum", "location": "Snagem Hideout",        "method": "shadow",  "notes": "Snagem Grunt Agrev",                        "encounter_rate": None},
    {"dex_no": 218, "game": "colosseum", "location": "Pyrite City",           "method": "shadow",  "notes": "St. Performer Lon",                         "encounter_rate": None},
    {"dex_no": 221, "game": "colosseum", "location": "The Under",             "method": "shadow",  "notes": "Bodybuilder Lonia",                         "encounter_rate": None},
    {"dex_no": 223, "game": "colosseum", "location": "Pyrite Town",           "method": "shadow",  "notes": "Miror B. Peon Reath",                       "encounter_rate": None},
    {"dex_no": 225, "game": "colosseum", "location": "Realgam Tower",         "method": "shadow",  "notes": "Cipher Peon Arton",                         "encounter_rate": None},
    {"dex_no": 226, "game": "colosseum", "location": "Pyrite Town",           "method": "shadow",  "notes": "Miror B. Peon Ferma",                       "encounter_rate": None},
    {"dex_no": 227, "game": "colosseum", "location": "Realgam Tower",         "method": "shadow",  "notes": "Snagem Leader Gonzap",                      "encounter_rate": None},
    {"dex_no": 229, "game": "colosseum", "location": "Realgam Tower",         "method": "shadow",  "notes": "Cipher Peon Nella",                         "encounter_rate": None},
    {"dex_no": 234, "game": "colosseum", "location": "The Under",             "method": "shadow",  "notes": "Chaser Liaks",                              "encounter_rate": None},
    {"dex_no": 235, "game": "colosseum", "location": "Snagem Hideout",        "method": "shadow",  "notes": "Snagem Grunt Biden",                        "encounter_rate": None},
    {"dex_no": 237, "game": "colosseum", "location": "Agate Village",         "method": "shadow",  "notes": "Cipher Peon Skrub",                         "encounter_rate": None},
    {"dex_no": 241, "game": "colosseum", "location": "Realgam Tower",         "method": "shadow",  "notes": "Bodybuilder Jonas",                         "encounter_rate": None},
    {"dex_no": 243, "game": "colosseum", "location": "Shadow PKMN Lab",       "method": "shadow",  "notes": "Cipher Admin Ein",                          "encounter_rate": None},
    {"dex_no": 244, "game": "colosseum", "location": "Mt. Battle",            "method": "shadow",  "notes": "Cipher Admin Dakim",                        "encounter_rate": None},
    {"dex_no": 245, "game": "colosseum", "location": "The Under",             "method": "shadow",  "notes": "Cipher Admin Venus",                        "encounter_rate": None},
    {"dex_no": 248, "game": "colosseum", "location": "Realgam Tower",         "method": "shadow",  "notes": "Cipher Head Evice",                         "encounter_rate": None},
    {"dex_no": 296, "game": "colosseum", "location": "Phenac City",           "method": "shadow",  "notes": "Miror B. Peon Trudly",                      "encounter_rate": None},
    {"dex_no": 307, "game": "colosseum", "location": "Pyrite Cave",           "method": "shadow",  "notes": "Rider Twan",                                "encounter_rate": None},
    {"dex_no": 329, "game": "colosseum", "location": "Shadow PKMN Lab",       "method": "shadow",  "notes": "Cipher Peon Remil",                         "encounter_rate": None},
    {"dex_no": 333, "game": "colosseum", "location": "Pyrite Cave",           "method": "shadow",  "notes": "Hunter Zalo",                               "encounter_rate": None},
    {"dex_no": 357, "game": "colosseum", "location": "Realgam Tower",         "method": "shadow",  "notes": "Cipher Peon Ston",                          "encounter_rate": None},
    {"dex_no": 359, "game": "colosseum", "location": "Realgam Tower",         "method": "shadow",  "notes": "Rider Delan",                               "encounter_rate": None},
    {"dex_no": 376, "game": "colosseum", "location": "Realgam Tower",         "method": "shadow",  "notes": "Cipher Nascour",                            "encounter_rate": None},
]

# ── Complete XD: Gale of Darkness data ───────────────────────────────────────

XD = [
    # Starter
    {"dex_no": 133, "game": "xd", "location": "Krane's Lab",         "method": "starter", "notes": "Michael's starter",                          "encounter_rate": None},

    # Gift / Trade
    {"dex_no": 175, "game": "xd", "location": "Outskirt Stand",      "method": "gift",    "notes": "From Hordel (Togepi egg)",                   "encounter_rate": None},
    {"dex_no": 239, "game": "xd", "location": "Outskirt Stand",      "method": "trade",   "notes": "Trade Togepi to Hordel",                     "encounter_rate": None},

    # Pokéspot wild encounters
    {"dex_no":  27, "game": "xd", "location": "Rock Pokéspot",       "method": "wild",    "notes": "Common",                                     "encounter_rate": None},
    {"dex_no": 207, "game": "xd", "location": "Rock Pokéspot",       "method": "wild",    "notes": "Uncommon",                                   "encounter_rate": None},
    {"dex_no": 328, "game": "xd", "location": "Rock Pokéspot",       "method": "wild",    "notes": "Rare",                                       "encounter_rate": None},
    {"dex_no": 187, "game": "xd", "location": "Oasis Pokéspot",      "method": "wild",    "notes": "Common",                                     "encounter_rate": None},
    {"dex_no": 231, "game": "xd", "location": "Oasis Pokéspot",      "method": "wild",    "notes": "Uncommon",                                   "encounter_rate": None},
    {"dex_no": 283, "game": "xd", "location": "Oasis Pokéspot",      "method": "wild",    "notes": "Rare",                                       "encounter_rate": None},
    {"dex_no":  41, "game": "xd", "location": "Cave Pokéspot",       "method": "wild",    "notes": "Common",                                     "encounter_rate": None},
    {"dex_no": 304, "game": "xd", "location": "Cave Pokéspot",       "method": "wild",    "notes": "Uncommon",                                   "encounter_rate": None},
    {"dex_no": 194, "game": "xd", "location": "Cave Pokéspot",       "method": "wild",    "notes": "Rare",                                       "encounter_rate": None},

    # Shadow Pokémon (83)
    {"dex_no":  12, "game": "xd", "location": "Cipher Key Lair",     "method": "shadow",  "notes": "Cipher Peon Targ",                           "encounter_rate": None},
    {"dex_no":  15, "game": "xd", "location": "Cipher Key Lair",     "method": "shadow",  "notes": "Cipher Peon Lok",                            "encounter_rate": None},
    {"dex_no":  17, "game": "xd", "location": "Cipher Key Lair",     "method": "shadow",  "notes": "Cipher Peon Lok",                            "encounter_rate": None},
    {"dex_no":  20, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Chaser Furgy",                               "encounter_rate": None},
    {"dex_no":  21, "game": "xd", "location": "Phenac Stadium",      "method": "shadow",  "notes": "Cipher Peon Ezin",                           "encounter_rate": None},
    {"dex_no":  24, "game": "xd", "location": "Cipher Key Lair",     "method": "shadow",  "notes": "Cipher Peon Smarton",                        "encounter_rate": None},
    {"dex_no":  37, "game": "xd", "location": "ONBS Station",        "method": "shadow",  "notes": "Cipher Peon Mesin",                          "encounter_rate": None},
    {"dex_no":  46, "game": "xd", "location": "Cipher Key Lair",     "method": "shadow",  "notes": "Cipher Peon Humah",                          "encounter_rate": None},
    {"dex_no":  49, "game": "xd", "location": "Cipher Key Lair",     "method": "shadow",  "notes": "Cipher Peon Angic",                          "encounter_rate": None},
    {"dex_no":  51, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Peon Stron",                          "encounter_rate": None},
    {"dex_no":  52, "game": "xd", "location": "Phenac City",         "method": "shadow",  "notes": "Cipher Peon Fostin",                         "encounter_rate": None},
    {"dex_no":  55, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Navigator Abson",                            "encounter_rate": None},
    {"dex_no":  57, "game": "xd", "location": "Cipher Key Lair",     "method": "shadow",  "notes": "Cipher Admin Gorigan",                       "encounter_rate": None},
    {"dex_no":  58, "game": "xd", "location": "Cipher Key Lair",     "method": "shadow",  "notes": "Cipher Peon Humah",                          "encounter_rate": None},
    {"dex_no":  62, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Admin Gorigan",                       "encounter_rate": None},
    {"dex_no":  70, "game": "xd", "location": "Cipher Key Lair",     "method": "shadow",  "notes": "Cipher Peon Angic",                          "encounter_rate": None},
    {"dex_no":  78, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Peon Kolest",                         "encounter_rate": None},
    {"dex_no":  82, "game": "xd", "location": "Cipher Key Lair",     "method": "shadow",  "notes": "Cipher Peon Snidle",                         "encounter_rate": None},
    {"dex_no":  83, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Admin Lovrina",                       "encounter_rate": None},
    {"dex_no":  85, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Chaser Furgy",                               "encounter_rate": None},
    {"dex_no":  86, "game": "xd", "location": "Phenac Stadium",      "method": "shadow",  "notes": "Cipher Peon Egrog",                          "encounter_rate": None},
    {"dex_no":  88, "game": "xd", "location": "Phenac Stadium",      "method": "shadow",  "notes": "Cipher Peon Faltly",                         "encounter_rate": None},
    {"dex_no":  90, "game": "xd", "location": "Cipher Key Lair",     "method": "shadow",  "notes": "Cipher Peon Gorog",                          "encounter_rate": None},
    {"dex_no":  97, "game": "xd", "location": "Cipher Key Lair",     "method": "shadow",  "notes": "Cipher Admin Gorigan",                       "encounter_rate": None},
    {"dex_no": 100, "game": "xd", "location": "Cave Pokéspot",       "method": "shadow",  "notes": "Wanderer Miror B. (2nd chance)",              "encounter_rate": None},
    {"dex_no": 103, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Boss Greevil",                        "encounter_rate": None},
    {"dex_no": 105, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Admin Eldes",                         "encounter_rate": None},
    {"dex_no": 106, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Peon Petro",                          "encounter_rate": None},
    {"dex_no": 107, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Peon Karbon",                         "encounter_rate": None},
    {"dex_no": 108, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Peon Gefta",                          "encounter_rate": None},
    {"dex_no": 112, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Boss Greevil",                        "encounter_rate": None},
    {"dex_no": 113, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Peon Leden",                          "encounter_rate": None},
    {"dex_no": 114, "game": "xd", "location": "Cipher Key Lair",     "method": "shadow",  "notes": "Cipher Peon Targ",                           "encounter_rate": None},
    {"dex_no": 115, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Peon Litnar",                         "encounter_rate": None},
    {"dex_no": 121, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Admin Snattle",                       "encounter_rate": None},
    {"dex_no": 122, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Admin Gorigan",                       "encounter_rate": None},
    {"dex_no": 123, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Peon Leden",                          "encounter_rate": None},
    {"dex_no": 125, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Admin Ardos",                         "encounter_rate": None},
    {"dex_no": 126, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Peon Grupel",                         "encounter_rate": None},
    {"dex_no": 127, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Peon Grupel",                         "encounter_rate": None},
    {"dex_no": 128, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Boss Greevil",                        "encounter_rate": None},
    {"dex_no": 131, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Admin Eldes",                         "encounter_rate": None},
    {"dex_no": 143, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Admin Ardos",                         "encounter_rate": None},
    {"dex_no": 144, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Boss Greevil",                        "encounter_rate": None},
    {"dex_no": 145, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Boss Greevil",                        "encounter_rate": None},
    {"dex_no": 146, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Boss Greevil",                        "encounter_rate": None},
    {"dex_no": 149, "game": "xd", "location": "Gateon Port",         "method": "shadow",  "notes": "Wanderer Miror B. (2nd chance)",              "encounter_rate": None},
    {"dex_no": 165, "game": "xd", "location": "Gateon Port",         "method": "shadow",  "notes": "Casual Guy Cyle",                            "encounter_rate": None},
    {"dex_no": 167, "game": "xd", "location": "Cipher Lab",          "method": "shadow",  "notes": "Cipher Peon Nexir",                          "encounter_rate": None},
    {"dex_no": 177, "game": "xd", "location": "Phenac City",         "method": "shadow",  "notes": "Cipher Peon Eloin",                          "encounter_rate": None},
    {"dex_no": 179, "game": "xd", "location": "Cipher Lab",          "method": "shadow",  "notes": "Cipher Peon Yellosix",                       "encounter_rate": None},
    {"dex_no": 204, "game": "xd", "location": "Phenac City",         "method": "shadow",  "notes": "Cipher Peon Gonrag",                         "encounter_rate": None},
    {"dex_no": 216, "game": "xd", "location": "Krane's Lab",         "method": "shadow",  "notes": "Spy Naps",                                   "encounter_rate": None},
    {"dex_no": 219, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Peon Kolest",                         "encounter_rate": None},
    {"dex_no": 220, "game": "xd", "location": "Phenac Stadium",      "method": "shadow",  "notes": "Cipher Peon Greck",                          "encounter_rate": None},
    {"dex_no": 228, "game": "xd", "location": "Cipher Lab",          "method": "shadow",  "notes": "Cipher Peon Resix",                          "encounter_rate": None},
    {"dex_no": 249, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Boss Greevil (XD001)",                 "encounter_rate": None},
    {"dex_no": 261, "game": "xd", "location": "Gateon Port",         "method": "shadow",  "notes": "Bodybuilder Kilen",                          "encounter_rate": None},
    {"dex_no": 273, "game": "xd", "location": "Cipher Lab",          "method": "shadow",  "notes": "Cipher Peon Greesix",                        "encounter_rate": None},
    {"dex_no": 277, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Admin Ardos",                         "encounter_rate": None},
    {"dex_no": 280, "game": "xd", "location": "ONBS Station",        "method": "shadow",  "notes": "Cipher Peon Feldas",                         "encounter_rate": None},
    {"dex_no": 285, "game": "xd", "location": "Cipher Lab",          "method": "shadow",  "notes": "Cipher R&D Klots",                           "encounter_rate": None},
    {"dex_no": 296, "game": "xd", "location": "ONBS Station",        "method": "shadow",  "notes": "Cipher Peon Torkin",                         "encounter_rate": None},
    {"dex_no": 299, "game": "xd", "location": "Phenac Stadium",      "method": "shadow",  "notes": "Wanderer Miror B. (2nd chance)",              "encounter_rate": None},
    {"dex_no": 301, "game": "xd", "location": "Cipher Lab",          "method": "shadow",  "notes": "Cipher Admin Lovrina",                       "encounter_rate": None},
    {"dex_no": 302, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Navigator Abson",                            "encounter_rate": None},
    {"dex_no": 303, "game": "xd", "location": "ONBS Station",        "method": "shadow",  "notes": "Cipher Cmdr. Exol",                          "encounter_rate": None},
    {"dex_no": 310, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Admin Eldes",                         "encounter_rate": None},
    {"dex_no": 315, "game": "xd", "location": "Phenac City",         "method": "shadow",  "notes": "Cipher Peon Fasin",                          "encounter_rate": None},
    {"dex_no": 316, "game": "xd", "location": "Cipher Lab",          "method": "shadow",  "notes": "Cipher Peon Purpsix",                        "encounter_rate": None},
    {"dex_no": 318, "game": "xd", "location": "Cipher Lab",          "method": "shadow",  "notes": "Cipher Peon Cabol",                          "encounter_rate": None},
    {"dex_no": 322, "game": "xd", "location": "Cipher Lab",          "method": "shadow",  "notes": "Cipher Peon Solox",                          "encounter_rate": None},
    {"dex_no": 334, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Admin Lovrina",                       "encounter_rate": None},
    {"dex_no": 335, "game": "xd", "location": "Cipher Key Lair",     "method": "shadow",  "notes": "Thug Zook",                                  "encounter_rate": None},
    {"dex_no": 337, "game": "xd", "location": "Phenac Stadium",      "method": "shadow",  "notes": "Cipher Admin Snattle",                       "encounter_rate": None},
    {"dex_no": 338, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Admin Snattle",                       "encounter_rate": None},
    {"dex_no": 343, "game": "xd", "location": "Cipher Lab",          "method": "shadow",  "notes": "Cipher Peon Browsix",                        "encounter_rate": None},
    {"dex_no": 354, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Peon Litnar",                         "encounter_rate": None},
    {"dex_no": 355, "game": "xd", "location": "ONBS Station",        "method": "shadow",  "notes": "Cipher Peon Labor",                          "encounter_rate": None},
    {"dex_no": 361, "game": "xd", "location": "Phenac City",         "method": "shadow",  "notes": "Cipher Peon Exinn",                          "encounter_rate": None},
    {"dex_no": 363, "game": "xd", "location": "Cipher Lab",          "method": "shadow",  "notes": "Cipher Peon Blusix",                         "encounter_rate": None},
    {"dex_no": 373, "game": "xd", "location": "Citadark Isle",       "method": "shadow",  "notes": "Cipher Admin Eldes",                         "encounter_rate": None},
]


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


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")

    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "catch_locations_data.py")

    # Load existing data, drop all colosseum/xd entries
    spec = importlib.util.spec_from_file_location("catch_locations_data", data_path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    kept = [e for e in mod.CATCH_LOCATIONS
            if str(e["game"]).strip() not in REPLACEABLE_GAMES]
    print(f"Kept {len(kept)} non-Colo/XD entries")

    new_entries = COLOSSEUM + XD
    print(f"Adding {len(new_entries)} Colo/XD entries "
          f"({len(COLOSSEUM)} Colosseum, {len(XD)} XD)")

    all_entries = kept + new_entries
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
