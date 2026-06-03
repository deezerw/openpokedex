GAME_SEQUENCE = ["ruby", "sapphire", "emerald", "firered", "leafgreen", "colosseum", "xd"]

CATCH_QTY_OVERRIDES = {}

STORY_AREAS = [
    # ── Opening ───────────────────────────────────────────────────────────────
    {
        "label": "Wes's Partners",
        "locations": ["Wes's partner"],
        "notes": "Espeon and Umbreon are Wes's two starter Pokémon. They begin with you and cannot be replaced.",
    },
    # ── Part 1: Outskirt Stand ────────────────────────────────────────────────
    {
        "label": "Outskirt Stand",
        "locations": ["Outskirt Stand"],
        "notes": "Snag Togetic from a trainer at the Outskirt Stand diner. First shadow Pokémon of the game.",
    },
    # ── Part 2: Phenac City ───────────────────────────────────────────────────
    {
        "label": "Phenac City",
        "locations": ["Phenac City"],
        "notes": "Snag one of the three Johto starters (Bayleef, Quilava, or Croconaw) and Makuhita from the Pre Gym. You can only snag the starter you're shown — the other two are permanently lost unless traded from another game.",
    },
    # ── Part 3: Pyrite Town ───────────────────────────────────────────────────
    {
        "label": "Pyrite Town",
        "locations": ["Pyrite Town"],
        "notes": "Miror B.'s base. Snag Sudowoodo, Yanma, Remoraid, and Mantine from trainers here.",
    },
    # ── Part 4: Agate Village ─────────────────────────────────────────────────
    {
        "label": "Agate Village — Hitmontop",
        "locations": ["Agate Village"],
        "notes": "Duking gives you Hitmontop as thanks for clearing the shadow Pokémon from Pyrite Town. The other Hitmons (Hitmonlee, Hitmonchan) are available in FireRed/LeafGreen.",
    },
    # ── Part 5: Pyrite City & Pyrite Cave ────────────────────────────────────
    {
        "label": "Pyrite City",
        "locations": ["Pyrite City"],
        "notes": "Multiple trainer battles across the city. Plusle is a gift, not a shadow snag.",
    },
    {
        "label": "Pyrite Cave (Relic Cave)",
        "locations": ["Pyrite Cave"],
    },
    # ── Part 6: The Under ─────────────────────────────────────────────────────
    {
        "label": "The Under",
        "locations": ["The Under"],
        "notes": "Cipher's underground hideout. Contains Suicune as a shadow Pokémon.",
    },
    # ── Part 7: Shadow Pokémon Lab ────────────────────────────────────────────
    {
        "label": "Shadow Pokémon Lab",
        "locations": ["Shadow PKMN Lab"],
        "notes": "Contains Raikou as a shadow Pokémon. Also has Ariados, Aipom, Murkrow, Forretress, Granbull, and Vibrava.",
    },
    # ── Part 8: Realgam Tower ─────────────────────────────────────────────────
    {
        "label": "Realgam Tower",
        "locations": ["Realgam Tower"],
        "notes": "Final story area. Contains the most powerful shadow Pokémon: Tyranitar, Metagross, Absol, Houndoom, Skarmory, and more. Realgam Tower can also be replayed post-game.",
    },
    # ── Post-game ─────────────────────────────────────────────────────────────
    {
        "label": "Mt. Battle",
        "locations": ["Mt. Battle"],
        "notes": "Entei is a shadow Pokémon encountered as the Area 1 boss. Ho-Oh is a gift for completing all 100 consecutive battles.",
    },
    {
        "label": "Snagem Hideout",
        "locations": ["Snagem Hideout"],
        "notes": "Accessible post-game. Contains Ursaring and Smeargle as shadow Pokémon.",
    },
    {
        "label": "Deep Colosseum",
        "locations": ["Deep Colosseum"],
        "notes": "Post-game battle mode. Shuckle is a shadow Pokémon found here.",
    },
    # ── Japan-only E-Reader events ────────────────────────────────────────────
    {
        "label": "Phenac City — E-Reader (Japan only)",
        "locations": ["Phenac City (E-Reader)"],
        "notes": "Togepi, Mareep, and Scizor were distributed via E-Reader cards in Japan only — effectively unobtainable outside Japan.",
        "ecard_only_dex": {175, 179, 212},
    },
    # ── Bonus Disc events ─────────────────────────────────────────────────────
    {
        "label": "Bonus Disc Events",
        "locations": ["Bonus Disc (US)", "Bonus Disc (Japan)"],
        "notes": "Jirachi via the Pokémon Colosseum Bonus Disc (NA/AU). Celebi via the Bonus Disc (Japan only).",
    },
]
