# OpenPokedex

A self-contained, single-user Pokémon living-dex tracker for Windows. Tracks
your catches, walkthrough progress, PC boxes, trade-evolution requirements,
and per-route completion across the Gen III games (Ruby, Sapphire, Emerald,
FireRed, LeafGreen, Colosseum, XD).

Ships as a single `.exe`. No installer, no Python install, no account, no
cloud — the app runs locally as a native window, stores your progress on
your own machine, and never makes a network call.

## Install (Windows)

1. Download `OpenPokedex.exe` from the latest [Release](../../releases/latest).
2. Double-click. That's it.

Your data lives in `%APPDATA%\OpenPokedex\` (`gen3.db`, `settings.json`) and
survives across upgrades — replace the `.exe` and your progress stays.

## What's in it

- **Dex view** — filter by region, type, tag, caught status, name; jump to any Pokémon's detail.
- **Walkthrough** — per-game catch lists, ordered by your owned games, with cross-game "catchable elsewhere" coverage.
- **Boxes** — visual PC-box layout in 30- or 60-cell modes.
- **Routes** — every game broken down by route, showing what's still missing.
- **Trades** — surfaces every trade-evolution and which trade items you need to gather.
- **Stats** — completion percentage and per-tag breakdowns.
- **Settings** — pick which games you own; the rest of the app respects it.

## Run from source (dev)

```bash
git clone https://github.com/deezerw/openpokedex
cd openpokedex
python3.12 -m venv venv
source venv/bin/activate     # or: venv\Scripts\activate on Windows
pip install -r requirements.txt
python desktop.py
```

This boots Flask in a background thread and opens a pywebview window
pointing at it. On Linux you'll need the GTK/WebKit2 bindings installed
(`python3-gi`, `gir1.2-webkit2-4.1`); on Windows pywebview uses the built-in
Edge WebView2 runtime.

## Build the `.exe` yourself

```bash
pip install pyinstaller pillow
python scripts/make_icon.py
pyinstaller --noconfirm OpenPokedex.spec
# → dist/OpenPokedex.exe
```

The GitHub Actions workflow at `.github/workflows/build.yml` does the same on
`windows-latest` for every push and attaches the artifact to a Release when
you tag `v*`.

## Where your data lives

| What | Where |
|---|---|
| Caught Pokémon, notes | `%APPDATA%\OpenPokedex\gen3.db` |
| Your settings (owned games, etc.) | `%APPDATA%\OpenPokedex\settings.json` |
| Read-only seed data (sprites, locations) | bundled inside `OpenPokedex.exe` |

On Linux dev, replace `%APPDATA%\OpenPokedex` with `~/.openpokedex`. On macOS,
`~/Library/Application Support/OpenPokedex`.

## Tech

- **Python 3.12** + Flask 3 backend
- **pywebview 6** native window (Edge WebView2 on Windows)
- **SQLite** (stdlib) for catch tracking
- **PyInstaller** single-file bundle
- **Pillow** to generate the Poké Ball icon at build time

## License

MIT — see [LICENSE](LICENSE). Use, fork, ship it as your own. Pokémon, Poké
Ball, and related marks are © Nintendo / Game Freak / The Pokémon Company.
This is an unaffiliated fan project.
