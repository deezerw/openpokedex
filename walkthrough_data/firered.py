GAME_SEQUENCE = ["emerald", "firered", "leafgreen", "colosseum", "xd"]

CATCH_QTY_OVERRIDES = {}

STORY_AREAS = [
    # ── Part 1: Pallet Town & Route 1 ────────────────────────────────────────
    {
        "label": "Pallet Town — Starter",
        "locations": ["Pallet Town"],
    },
    {
        "label": "Route 1",
        "locations": ["Route 1"],
    },
    # ── Part 2: Viridian City & Route 22 ─────────────────────────────────────
    {
        "label": "Route 22",
        "locations": ["Route 22"],
        "notes": "Accessible before the Viridian Gym (8th badge). Worth visiting early for Mankey and Poliwag.",
    },
    # ── Part 3: Viridian Forest & Route 2 ────────────────────────────────────
    {
        "label": "Viridian Forest & Route 2",
        "locations": ["Viridian Forest", "Route 2"],
    },
    # ── Part 4: Route 3, Mt. Moon, Route 4 ───────────────────────────────────
    {
        "label": "Route 3",
        "locations": ["Route 3"],
    },
    {
        "label": "Mt. Moon",
        "locations": ["Mt. Moon"],
        "notes": "Pick up one fossil (Dome Fossil → Kabuto, or Helix Fossil → Omanyte) — you can only take one. The other is permanently lost unless traded.",
    },
    {
        "label": "Route 4",
        "locations": ["Route 4"],
    },
    # ── Part 5: Cerulean City & Routes 24–25 ─────────────────────────────────
    {
        "label": "Route 24 & Route 25",
        "locations": ["Route 24", "Route 25"],
    },
    {
        "label": "Cerulean City — Gifts & Trade",
        "locations": ["Cerulean City (gift)", "Cerulean City (in-game trade)"],
        "notes": "Buy a Magikarp from the house near the Pokémon Center. Trade a Poliwhirl for Jynx at the house in the northeast.",
    },
    # ── Part 6: Routes 5–6, Vermilion City ───────────────────────────────────
    {
        "label": "Route 5 & Route 6",
        "locations": ["Route 5", "Route 6"],
    },
    {
        "label": "Vermilion City — Trade",
        "locations": ["Vermilion City (in-game trade)"],
        "notes": "Trade a Spearow for Farfetch'd at the house south of the Pokémon Center.",
    },
    {
        "label": "Diglett's Cave",
        "locations": ["Diglett's Cave"],
    },
    # ── Part 7: Route 9, Route 10, Rock Tunnel ───────────────────────────────
    {
        "label": "Route 9 & Route 10",
        "locations": ["Route 9", "Route 10"],
    },
    {
        "label": "Rock Tunnel",
        "locations": ["Rock Tunnel"],
    },
    # ── Part 8: Route 7–8, Lavender Town ─────────────────────────────────────
    {
        "label": "Route 7 & Route 8",
        "locations": ["Route 7", "Route 8"],
    },
    {
        "label": "Pokémon Tower",
        "locations": ["Pokémon Tower"],
        "notes": "Requires the Silph Scope from the Rocket Hideout (Celadon City) to interact with the Ghost-type Pokémon.",
    },
    # ── Part 9: Celadon City ──────────────────────────────────────────────────
    {
        "label": "Celadon City — Eevee, Porygon & Electrode",
        "locations": ["Celadon City (gift)", "Celadon Game Corner (9999 coins)", "Celadon Game Corner (static)"],
        "notes": "Eevee is a gift in the building north of the city. Porygon costs 9,999 Game Corner coins. Only one Eevee is available as a gift — breed it for extra copies needed for each Eeveelution (Vaporeon, Jolteon, Flareon). Espeon and Umbreon come from Pokémon Colosseum.",
    },
    # ── Part 10: Silph Co. ────────────────────────────────────────────────────
    {
        "label": "Silph Co. — Lapras Gift",
        "locations": ["Silph Co. (gift)"],
        "notes": "Received from a Silph employee on the 7th floor after defeating Team Rocket.",
    },
    # ── Part 11: Routes 11–15 (east/south of Lavender) ───────────────────────
    {
        "label": "Route 11",
        "locations": ["Route 11"],
    },
    {
        "label": "Routes 12–15",
        "locations": ["Route 12", "Route 12 (static)", "Route 13", "Route 14", "Route 15"],
        "notes": "Two Snorlax block Routes 12 and 16 — both require the Poké Flute to wake.",
    },
    # ── Part 12: Routes 16–18 (Cycling Road) ─────────────────────────────────
    {
        "label": "Routes 16–18",
        "locations": ["Route 16", "Route 16 (static)", "Route 17", "Route 18", "Route 18 (in-game trade)"],
        "notes": "Trade a Golduck for Lickitung on Route 18.",
    },
    # ── Part 13: Safari Zone ──────────────────────────────────────────────────
    {
        "label": "Safari Zone",
        "locations": ["Safari Zone (Area 1)", "Safari Zone (Area 2)", "Safari Zone (Area 3)", "Safari Zone (Area 4)"],
        "notes": "Contains many unique Pokémon including Kangaskhan, Tauros, Scyther, Chansey, and Dratini. Each area has different encounters.",
    },
    # ── Part 14: Fuchsia City → Routes 19–21 ─────────────────────────────────
    {
        "label": "Routes 19–21",
        "locations": ["Route 19", "Route 20", "Route 21", "Route 21 (in-game trade)"],
        "notes": "Trade a Clefairy for Mr. Mime on Route 21. Seadra (fishing) available throughout.",
    },
    {
        "label": "Seafoam Islands",
        "locations": ["Seafoam Islands", "Seafoam Islands (static)"],
        "notes": "Surfed through on the way south from Route 20 to Cinnabar Island. Articuno waits at the bottom.",
    },
    # ── Part 15: Saffron City ─────────────────────────────────────────────────
    {
        "label": "Saffron City — Fighting Dojo",
        "locations": ["Saffron City Fighting Dojo"],
        "notes": "Choose one reward: Hitmonlee OR Hitmonchan. Breed the one you get to raise Tyrogue, which can evolve into the other.",
    },
    # ── Part 16: Pokémon Mansion & Cinnabar Lab Fossils ──────────────────────
    {
        "label": "Pokémon Mansion",
        "locations": ["Pokémon Mansion"],
    },
    {
        "label": "Cinnabar Lab — Fossil Revival",
        "locations": ["Cinnabar Lab (Dome Fossil)", "Cinnabar Lab (Helix Fossil)", "Cinnabar Lab (Old Amber)"],
        "notes": "Revive your Mt. Moon fossil here. Old Amber (→ Aerodactyl) is given by a scientist in Pewter City Museum.",
    },
    # ── Part 17: Power Plant → Route 23 & Victory Road ───────────────────────
    {
        "label": "Power Plant",
        "locations": ["Power Plant", "Power Plant (static)"],
        "notes": "Reached by Surfing up Route 10 once you have HM Surf — a pre-League stop. Zapdos is the static encounter inside.",
    },
    {
        "label": "Route 23",
        "locations": ["Route 23"],
    },
    {
        "label": "Victory Road",
        "locations": ["Victory Road"],
    },
    # ── Sevii Islands (after 7th gym, during/after main story) ───────────────
    {
        "label": "One Island & Kindle Road",
        "locations": ["One Island", "Kindle Road"],
        "notes": "Accessible after defeating Blaine (7th gym) when Bill takes you to One Island.",
    },
    {
        "label": "Mt. Ember",
        "locations": ["Mt. Ember", "Mt. Ember, Sevii Island 1 (static)"],
        "notes": "Moltres is at the summit. Also has unique Pokémon: Ponyta, Slugma, Magcargo.",
    },
    {
        "label": "Sevii Island 1 — Togepi Egg",
        "locations": ["Sevii Island 1 (Lola's egg gift)"],
        "notes": "Lola on One Island gives you a Togepi egg after returning the Ruby.",
    },
    # ── Post-game (after becoming Champion) ──────────────────────────────────
    {
        "label": "Cerulean Cave",
        "locations": ["Cerulean Cave", "Cerulean Cave (static)"],
        "notes": "Unlocked after becoming Champion. Mewtwo is the deepest static encounter. Also contains Wobbuffet.",
    },
    {
        "label": "Four Island",
        "locations": ["Four Island"],
    },
    {
        "label": "Five Island & Water Path",
        "locations": ["Five Island", "Water Path"],
    },
    {
        "label": "Icefall Cave (Four Island area)",
        "locations": ["Icefall Cave"],
        "notes": "Contains Ice-type and Johto Pokémon: Swinub, Delibird, Seel, Shellder, Wooper.",
    },
    {
        "label": "Altering Cave",
        "locations": ["Altering Cave"],
        "notes": "Default encounter is Zubat. Other Pokémon appear via Mystery Gift e-Cards (Japan-only — effectively unobtainable).",
        "ecard_only_dex": {179, 190, 204, 213, 216, 228, 234, 235},
    },
    {
        "label": "Berry Forest (Three Island)",
        "locations": ["Berry Forest"],
    },
    {
        "label": "Lost Cave (Five Island)",
        "locations": ["Lost Cave"],
    },
    {
        "label": "Pattern Bush (Six Island)",
        "locations": ["Pattern Bush"],
        "notes": "Contains Hoenn Bug-types and Heracross.",
    },
    {
        "label": "Sevault Canyon & Water Path (Seven Island)",
        "locations": ["Sevault Canyon"],
        "notes": "Contains rare Pokémon: Larvitar, Skarmory, Phanpy. Requires HM Rock Smash and Strength.",
    },
    {
        "label": "Trainer Tower (Seven Island)",
        "locations": ["Trainer Tower"],
        "notes": "At the far end of Seven Island's Trainer Tower outskirts — surf/fish encounters available post-game.",
    },
    {
        "label": "Tanoby Ruins (Seven Island)",
        "locations": ["Tanoby Ruins"],
        "notes": "Unlock by solving the Tanoby Key in Tanoby Chambers. Different Unown letters in each ruin room.",
    },
    {
        "label": "Roaming Kanto Legendaries",
        "locations": ["Roaming Kanto (post-National Dex)"],
        "notes": "One legendary beast roams Kanto after obtaining the National Pokédex: Entei (if starter was Bulbasaur), Raikou (Charmander), or Suicune (Squirtle).",
    },
    {
        "label": "Pallet Town — Johto Starters (Prof. Oak)",
        "locations": ["Pallet Town (Prof. Oak)"],
        "notes": "Prof. Oak gives one Johto starter (Chikorita, Cyndaquil, or Totodile) after completing the National Pokédex (all 386 Pokémon seen).",
    },
    {
        "label": "Event Pokémon",
        "locations": [
            "Birth Island (Aurora Ticket event)",
            "Navel Rock (MysticTicket event)",
            "Faraway Island (Old Sea Map event)",
        ],
        "notes": "Require official event tickets. Birth Island → Deoxys; Navel Rock → Ho-Oh and Lugia; Faraway Island → Mew.",
    },
]
