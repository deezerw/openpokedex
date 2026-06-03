GAME_SEQUENCE = ["ruby", "sapphire", "emerald", "firered", "leafgreen", "colosseum", "xd"]

CATCH_QTY_OVERRIDES = {290: 2}  # Nincada: one level-up yields Ninjask AND Shedinja simultaneously

STORY_AREAS = [
    # ── Part 1: Littleroot Town ───────────────────────────────────────────────
    {
        "label": "Littleroot Town — Starter",
        "locations": ["Littleroot Town"],
    },
    # ── Part 2: Routes 101–103 ────────────────────────────────────────────────
    {
        "label": "Route 101",
        "locations": ["Route 101"],
    },
    {
        "label": "Route 103",
        "locations": ["Route 103"],
    },
    # ── Part 3: Route 102, Route 104 & Petalburg Woods ───────────────────────
    {
        "label": "Route 102",
        "locations": ["Route 102"],
        "notes": "Sapphire gets Lotad here; Ruby gets Seedot.",
    },
    {
        "label": "Route 104 & Petalburg Woods",
        "locations": ["Route 104", "Petalburg Woods"],
    },
    # ── Part 4: Route 116 & Granite Cave ─────────────────────────────────────
    {
        "label": "Route 116",
        "locations": ["Route 116"],
    },
    {
        "label": "Route 115",
        "locations": ["Route 115"],
    },
    {
        "label": "Granite Cave",
        "locations": ["Granite Cave"],
        "notes": "Sapphire gets Sableye here; Ruby gets Mawile.",
    },
    # ── Part 5: Routes 105–109 & Abandoned Ship ──────────────────────────────
    {
        "label": "Routes 105–106",
        "locations": ["Route 105", "Route 106"],
    },
    {
        "label": "Routes 107–109 & Abandoned Ship",
        "locations": ["Route 107", "Route 108", "Route 109", "Abandoned Ship"],
    },
    # ── Part 6: Route 110, Route 117 ─────────────────────────────────────────
    {
        "label": "Route 110",
        "locations": ["Route 110"],
    },
    {
        "label": "Route 117",
        "locations": ["Route 117"],
    },
    # ── Part 7: Route 111, Route 112, Fiery Path ─────────────────────────────
    {
        "label": "Route 111 & Route 112",
        "locations": ["Route 111", "Route 112"],
    },
    {
        "label": "Fiery Path",
        "locations": ["Fiery Path"],
    },
    # ── Part 8: Route 113, Route 114, Meteor Falls ───────────────────────────
    {
        "label": "Route 113",
        "locations": ["Route 113"],
    },
    {
        "label": "Route 114",
        "locations": ["Route 114"],
        "notes": "Sapphire gets Seviper here; Ruby gets Zangoose.",
    },
    {
        "label": "Meteor Falls",
        "locations": ["Meteor Falls"],
        "notes": "Bagon is in the back room and requires Surf. Sapphire gets Lunatone; Ruby gets Solrock.",
    },
    # ── Part 9: Jagged Pass & Lavaridge Town ─────────────────────────────────
    {
        "label": "Jagged Pass",
        "locations": ["Jagged Pass"],
    },
    {
        "label": "Lavaridge Town — Egg",
        "locations": ["Lavaridge Town"],
        "notes": "Old lady by the hot springs gives you a Wynaut egg.",
    },
    # ── Part 10: Route 118, Route 119, Weather Institute ─────────────────────
    {
        "label": "Route 118",
        "locations": ["Route 118"],
    },
    {
        "label": "Route 119 & Weather Institute",
        "locations": ["Route 119", "Route 119, 120 (static, hidden)", "Weather Institute (gift)"],
        "notes": "Castform is a gift from the Weather Institute researcher after rescuing them. Two hidden Kecleon on Routes 119–120 require the Devon Scope (received after Mossdeep Gym).",
    },
    {
        "label": "Route 120 & Route 121",
        "locations": ["Route 120", "Route 121"],
        "notes": "Sapphire gets Shuppet on Routes 121/123; Ruby gets Duskull.",
    },
    # ── Part 11: Safari Zone ──────────────────────────────────────────────────
    {
        "label": "Safari Zone",
        "locations": ["Safari Zone"],
        "notes": "Contains Pikachu, Heracross, Phanpy, Rhyhorn, Wobbuffet, Natu, Girafarig, Doduo, Pinsir, and more.",
    },
    # ── Part 12: Route 122, Mt. Pyre, Route 123 ──────────────────────────────
    {
        "label": "Route 122 & Mt. Pyre",
        "locations": ["Route 122", "Mt. Pyre"],
    },
    {
        "label": "Route 123",
        "locations": ["Route 123"],
    },
    # ── Part 13: Route 124, Mossdeep, Shoal Cave, Seafloor, Cave of Origin ───
    {
        "label": "Route 124",
        "locations": ["Route 124"],
    },
    {
        "label": "Mossdeep City — Beldum Gift",
        "locations": ["Mossdeep City (gift from Steven Stone)"],
        "notes": "Steven Stone leaves a Beldum and a note in his house after you defeat the Mossdeep Gym.",
    },
    {
        "label": "Shoal Cave",
        "locations": ["Shoal Cave"],
    },
    {
        "label": "Routes 125–128",
        "locations": ["Route 125", "Route 126", "Route 127", "Route 128"],
    },
    {
        "label": "Seafloor Cavern",
        "locations": ["Seafloor Cavern"],
    },
    {
        "label": "Cave of Origin — Kyogre (Sapphire) / Groudon (Ruby)",
        "locations": ["Cave of Origin", "Cave of Origin (static)"],
        "notes": "Kyogre is the static encounter in Sapphire; Groudon in Ruby. Sapphire gets Sableye in the wild encounters; Ruby gets Mawile.",
    },
    {
        "label": "Sootopolis City",
        "locations": ["Sootopolis City"],
        "notes": "Home of the 8th Gym. Surf and fish the city water for Tentacool, Magikarp, and Gyarados.",
    },
    {
        "label": "Routes 129–134",
        "locations": ["Route 129", "Route 130", "Route 131", "Route 132", "Route 133", "Route 134"],
    },
    # ── Part 14: Victory Road ─────────────────────────────────────────────────
    {
        "label": "Victory Road",
        "locations": ["Victory Road"],
        "notes": "Sapphire gets Sableye here; Ruby gets Mawile.",
    },
    # ── Post-game ─────────────────────────────────────────────────────────────
    {
        "label": "Devon Corp — Fossil Revival",
        "locations": ["Devon Corp — Root Fossil revival", "Devon Corp — Claw Fossil revival"],
        "notes": "Pick up one fossil during the Team Magma/Aqua conflict in the desert. Root Fossil → Lileep; Claw Fossil → Anorith. Revived at Devon Corp in Rustboro.",
    },
    {
        "label": "New Mauville",
        "locations": ["New Mauville"],
        "notes": "Requires Surf. Voltorb, Electrode, Magnemite, Magneton.",
    },
    {
        "label": "Sky Pillar",
        "locations": ["Sky Pillar", "Sky Pillar (static)"],
        "notes": "Rayquaza is at the summit. Sapphire gets Sableye and Banette here; Ruby gets Mawile and Dusclops.",
    },
    {
        "label": "Regi Trio",
        "locations": ["Desert Ruins (static)", "Island Cave (static)", "Ancient Tomb (static)"],
        "notes": "Regirock (Desert Ruins), Regice (Island Cave), Registeel (Ancient Tomb). Each requires solving the braille puzzles.",
    },
    {
        "label": "Southern Island — Latias",
        "locations": ["Southern Island (static)", "Southern Island (Eon Ticket event)"],
        "notes": "Sapphire: Latias is the static encounter on Southern Island. Latios requires the Eon Ticket event to encounter on Southern Island (or can be found roaming post-game).",
    },
    {
        "label": "Roaming Hoenn — Latios",
        "locations": ["Roaming Hoenn (post-game)"],
        "notes": "Latios roams Hoenn in Sapphire after becoming Champion.",
    },
    {
        "label": "Event Pokémon",
        "locations": [
            "Pokémon Colosseum Bonus Disc EN (event)",
            "Pokémon Channel PAL (event)",
        ],
        "notes": "Jirachi via Pokémon Colosseum Bonus Disc (NA/AU) or Pokémon Channel (PAL).",
    },
]
