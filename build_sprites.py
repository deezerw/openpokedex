#!/usr/bin/env python3
"""
build_sprites.py
Builds sprite sheet PNGs and a CSS file so the box page makes 1 image request
instead of 386/493 individual ones.

Run once after adding or changing sprites:
    python3 build_sprites.py
"""
import os
import subprocess
import sys

BASE   = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(BASE, "static")
COLS   = 20

GENS = [
    ("gen3", 386, 64),
]


def build_sheet(gen_slug, max_dex, size):
    src_dir  = os.path.join(STATIC, "sprites", gen_slug)
    out_path = os.path.join(STATIC, "sprites", f"sheet_{gen_slug}.png")

    files = [os.path.join(src_dir, f"{i}.png") for i in range(1, max_dex + 1)]
    missing = [f for f in files if not os.path.exists(f)]
    if missing:
        print(f"  [WARN] {len(missing)} missing sprites: {missing[:3]}…", file=sys.stderr)

    cmd = (
        ["montage"]
        + ["-geometry", f"{size}x{size}+0+0"]
        + ["-tile", f"{COLS}x"]
        + ["-background", "none"]
        + files
        + [out_path]
    )
    print(f"Building sheet_{gen_slug}.png  ({max_dex} sprites, {COLS} cols × {size}px)…")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"ERROR:\n{r.stderr}", file=sys.stderr)
        sys.exit(1)
    size_kb = os.path.getsize(out_path) // 1024
    print(f"  → {out_path}  ({size_kb} KB)")


def build_css():
    """
    Uses percentage-based background-position so the sprite scales correctly
    when the element is resized (e.g. via a mobile media query).

    background-size: {COLS*100}% auto  → image is always COLS× the element width,
    so one sprite slot = one element width.

    background-position: X% Y% where
      X = col / (COLS-1) * 100
      Y = row / (ROWS-1) * 100
    These percentages are scale-invariant: they stay correct at any element size.
    """
    import math
    out_css = os.path.join(STATIC, "sprites.css")
    lines = []
    for gen_slug, max_dex, size in GENS:
        rows = math.ceil(max_dex / COLS)
        lines += [
            f".sprite-{gen_slug} {{",
            f"  background-image: url('/static/sprites/sheet_{gen_slug}.png');",
            f"  background-size: {COLS * 100}% auto;",
            f"  width: {size}px; height: {size}px;",
            f"  display: inline-block; flex-shrink: 0;",
            f"}}",
        ]
        for dex in range(1, max_dex + 1):
            col = (dex - 1) % COLS
            row = (dex - 1) // COLS
            x = round(col / (COLS - 1) * 100, 4) if COLS > 1 else 0
            y = round(row / (rows - 1) * 100, 4) if rows > 1 else 0
            lines.append(f".sprite-{gen_slug}-{dex}{{background-position:{x}% {y}%}}")
        lines.append("")
    with open(out_css, "w") as f:
        f.write("\n".join(lines))
    size_kb = os.path.getsize(out_css) // 1024
    print(f"CSS → {out_css}  ({size_kb} KB)")


if __name__ == "__main__":
    css_only = "--css-only" in sys.argv
    if not css_only:
        for args in GENS:
            build_sheet(*args)
    build_css()
    print("Done. Restart the server if it's running.")
