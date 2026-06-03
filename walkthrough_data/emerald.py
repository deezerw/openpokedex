# Game sequence for catch_qty calculation (all games played in order).
# Pokémon directly catchable in any of these games are "covered" and don't
# add to the copy count of earlier-chain members.
GAME_SEQUENCE = ["emerald", "firered", "leafgreen", "colosseum", "xd"]

# Override computed catch_qty for Pokémon with unusual evolution mechanics.
# Used when the algorithm's generic tree-traversal gives the wrong answer.
CATCH_QTY_OVERRIDES = {
    290: 2,  # Nincada: one evolution simultaneously yields BOTH Ninjask AND Shedinja
}

STORY_AREAS = [
    # ── Part 1: Starting Out ─────────────────────────────────────────────────
    {
        "label": "Littleroot Town — Starter",
        "locations": ["Littleroot Town"],
    },
    {
        "label": "Route 101",
        "locations": ["Route 101"],
    },
    {
        "label": "Route 103",
        "locations": ["Route 103"],
    },
    # ── Part 2: Oldale → Petalburg → Rustboro ────────────────────────────────
    {
        "label": "Route 102",
        "locations": ["Route 102"],
    },
    {
        "label": "Route 104 & Petalburg Woods",
        "locations": ["Route 104", "Petalburg Woods"],
    },
    {
        "label": "Route 116",
        "locations": ["Route 116"],
    },
    # ── Part 3: Route 115 (north of Rustboro, no HMs needed for south section)
    {
        "label": "Route 115",
        "locations": ["Route 115"],
    },
    # ── Part 4: Dewford & Granite Cave ───────────────────────────────────────
    {
        "label": "Granite Cave",
        "locations": ["Granite Cave"],
    },
    {
        "label": "Routes 105–106",
        "locations": ["Route 105", "Route 106"],
    },
    # ── Part 5: Slateport & Abandoned Ship ───────────────────────────────────
    {
        "label": "Routes 107–109 & Abandoned Ship",
        "locations": ["Route 107", "Route 108", "Abandoned Ship", "Route 109"],
    },
    # ── Part 6: Mauville & Surroundings ──────────────────────────────────────
    {
        "label": "Route 110",
        "locations": ["Route 110"],
    },
    {
        "label": "Route 117",
        "locations": ["Route 117"],
    },
    {
        "label": "Route 111 & Route 112",
        "locations": ["Route 111", "Route 112"],
        "notes": "The northern desert section of Route 111 requires Go-Goggles, obtained from Lavaridge Town after the 4th gym.",
    },
    {
        "label": "Fiery Path",
        "locations": ["Fiery Path"],
    },
    # ── Part 7: Fallarbor & Meteor Falls ─────────────────────────────────────
    {
        "label": "Route 113",
        "locations": ["Route 113"],
    },
    {
        "label": "Route 114",
        "locations": ["Route 114"],
    },
    {
        "label": "Meteor Falls",
        "locations": ["Meteor Falls"],
        "notes": "Bagon is found in the deeper cave, only reachable with HM Surf. Return here after earning the 5th badge (Petalburg Gym) and obtaining HM03 Surf.",
    },
    # ── Part 8: Lavaridge Town & Magma Hideout ────────────────────────────────
    {
        "label": "Jagged Pass",
        "locations": ["Jagged Pass"],
    },
    {
        "label": "Lavaridge Town — Egg Gift",
        "locations": ["Lavaridge Town (egg gift)"],
    },
    {
        "label": "Magma Hideout",
        "locations": ["Magma Hideout"],
    },
    # ── Part 9: Post-Norman — Surf Unlocked ──────────────────────────────────
    {
        "label": "Route 118",
        "locations": ["Route 118"],
    },
    {
        "label": "Route 119 & Weather Institute",
        "locations": ["Route 119", "Weather Institute (gift)", "Route 119, 120 (static, hidden)"],
    },
    # ── Part 10: Fortree → Lilycove ──────────────────────────────────────────
    {
        "label": "Route 120 & Route 121",
        "locations": ["Route 120", "Route 121"],
    },
    {
        "label": "Safari Zone",
        "locations": ["Safari Zone"],
        "notes": "Located east of Lilycove City. Contains many Johto and cross-region Pokémon unavailable elsewhere in Hoenn.",
    },
    # ── Part 11: Mt. Pyre → Mossdeep ─────────────────────────────────────────
    {
        "label": "Route 122 & Mt. Pyre",
        "locations": ["Route 122", "Mt. Pyre"],
    },
    {
        "label": "Route 123",
        "locations": ["Route 123"],
    },
    {
        "label": "Route 124",
        "locations": ["Route 124"],
    },
    {
        "label": "Mossdeep City — Beldum Gift",
        "locations": ["Mossdeep City (gift from Steven Stone)"],
        "notes": "Visit Steven Stone's house in Mossdeep after defeating the Mossdeep Gym to receive a Beldum.",
    },
    {
        "label": "Shoal Cave",
        "locations": ["Shoal Cave"],
    },
    # ── Part 12: Seafloor → Sootopolis ───────────────────────────────────────
    {
        "label": "Routes 125–128",
        "locations": ["Route 125", "Route 126", "Route 127", "Route 128"],
    },
    {
        "label": "Seafloor Cavern & Sootopolis",
        "locations": ["Seafloor Cavern", "Sootopolis City", "Cave of Origin"],
    },
    # ── Part 13: Pacifidlog & Eastern Routes ─────────────────────────────────
    {
        "label": "Routes 129–134",
        "locations": ["Route 129", "Route 130", "Route 131", "Route 132", "Route 133", "Route 134"],
    },
    # ── Part 14: Victory Road ─────────────────────────────────────────────────
    {
        "label": "Victory Road",
        "locations": ["Victory Road"],
    },
    # ── Post-game ─────────────────────────────────────────────────────────────
    {
        "label": "Devon Corp — Fossil Revival",
        "locations": ["Devon Corp — Claw Fossil revival", "Devon Corp — Root Fossil revival"],
        "notes": "Choose one fossil in the Mirage Tower (Route 111 desert, needs Go-Goggles). The other fossil is found in the Fossil Maniac's Tunnel (Route 114) after the main story.",
    },
    {
        "label": "New Mauville",
        "locations": ["New Mauville"],
        "notes": "Underground power plant south of Mauville. Accessible post-game after Wattson gives you the Generator Key.",
    },
    {
        "label": "Sky Pillar",
        "locations": ["Sky Pillar", "Sky Pillar (static)"],
        "notes": "Located on Route 131. Accessible after obtaining HM Waterfall. Rayquaza is at the summit.",
    },
    {
        "label": "Artisan Cave (Battle Frontier)",
        "locations": ["Artisan Cave", "Battle Frontier (static)"],
        "notes": "Inside the Battle Frontier on the Battle Island. Accessible post-Elite Four. A Sudowoodo can be battled in the Frontier grounds.",
    },
    {
        "label": "Roaming Legendaries",
        "locations": ["Roaming Hoenn (post-game)", "Marine Cave (roaming static)", "Terra Cave (roaming static)"],
        "notes": "Latios roams all of Hoenn post-game (or Latias with the Eon Ticket). Kyogre appears in Marine Cave and Groudon in Terra Cave — each shifts location daily.",
    },
    {
        "label": "Regi Trio",
        "locations": ["Desert Ruins (static)", "Island Cave (static)", "Ancient Tomb (static)"],
        "notes": "Regirock (Desert Ruins, Route 111), Regice (Island Cave, Route 105), Registeel (Ancient Tomb, Route 120). Unlock by solving the braille puzzles on Route 134.",
    },
    {
        "label": "Event Pokémon",
        "locations": [
            "Southern Island (Eon Ticket event)",
            "Birth Island (Aurora Ticket event)",
            "Faraway Island (Old Sea Map event)",
            "Navel Rock (MysticTicket event)",
            "Nintendo event only",
        ],
        "notes": "These Pokémon require official event tickets distributed at Nintendo events.",
    },
]
