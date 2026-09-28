#!/usr/bin/env python3
"""Generate a text-only logo SVG (glyph outlines) for a landscape tool.

Run via:  uv run --with fonttools python generate_logo.py --name "Tool Name" --out logos/unofficial/tool-name.svg

Uses a local libre condensed font (Roboto Condensed Bold by default) and emits
black glyph <path> outlines with a tight viewBox, matching the style of the
existing logos/unofficial/*.svg placeholders. No network, no permanent deps.
"""

import argparse
import re
import sys
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

# Searched when --font is not given. Covers common Linux/macOS/Windows installs
# of the libre OFL font Roboto Condensed (Debian/Ubuntu: fonts-roboto,
# Fedora: google-roboto-condensed-fonts, macOS: brew install --cask font-roboto-condensed).
FONT_CANDIDATES = [
    "~/.local/share/fonts/RobotoCondensed-Bold.ttf",
    "~/.local/share/fonts/RobotoCondensed[wght].ttf",
    "/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Bold.ttf",
    "/usr/share/fonts/truetype/roboto/RobotoCondensed-Bold.ttf",
    "/usr/share/fonts/TTF/RobotoCondensed-Bold.ttf",
    "/usr/share/fonts/google-roboto-condensed/RobotoCondensed-Bold.ttf",
    "/Library/Fonts/RobotoCondensed-Bold.ttf",
    "~/Library/Fonts/RobotoCondensed-Bold.ttf",
    "C:/Windows/Fonts/RobotoCondensed-Bold.ttf",
]


def find_font(explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit).expanduser()
        if not p.exists():
            sys.exit(f"font not found: {p}")
        return p
    for cand in FONT_CANDIDATES:
        p = Path(cand).expanduser()
        if p.exists():
            return p
    sys.exit(
        "Roboto Condensed not found. Install a libre condensed font "
        "(e.g. `apt install fonts-roboto` / `brew install --cask font-roboto-condensed`) "
        "or pass --font /path/to/Font.ttf"
    )


def load_font(path: Path) -> TTFont:
    font = TTFont(path, fontNumber=0)
    if "fvar" in font:  # variable font -> take the bold instance
        font = instantiateVariableFont(font, {"wght": 700}, inplace=False)
    return font


def slugify(name: str) -> str:
    s = name.encode("ascii", "ignore").decode().strip().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "logo"


def clean_text(name: str) -> str:
    # strip non-ASCII decorations (e.g. ®), keep ASCII punctuation
    return name.encode("ascii", "ignore").decode().strip()


def build_svg(text: str, font: TTFont, size: float = 100.0) -> str:
    upem = font["head"].unitsPerEm
    scale = size / upem
    cmap = font.getBestCmap()
    glyphset = font.getGlyphSet()
    hmtx = font["hmtx"]

    paths: list[str] = []
    bounds = None
    x = 0.0
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            gname = cmap.get(ord(" "))  # fall back to a space advance
        if gname is None:
            continue
        transform = Transform(scale, 0, 0, -scale, x, 0)
        spen = SVGPathPen(glyphset)
        glyphset[gname].draw(TransformPen(spen, transform))
        d = spen.getCommands()
        if d:
            paths.append(d)
        bpen = BoundsPen(glyphset)
        glyphset[gname].draw(TransformPen(bpen, transform))
        if bpen.bounds:
            b = bpen.bounds
            bounds = b if bounds is None else (
                min(bounds[0], b[0]), min(bounds[1], b[1]),
                max(bounds[2], b[2]), max(bounds[3], b[3]),
            )
        x += hmtx[gname][0] * scale

    if bounds is None:
        sys.exit("no drawable glyphs in the provided name")
    x0, y0, x1, y1 = bounds
    w, h = x1 - x0, y1 - y0
    body = "\n".join(f'<path d="{d}"/>' for d in paths)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}">\n'
        f'<g fill="#000000" transform="translate({-x0:.2f},{-y0:.2f})">\n'
        f"{body}\n</g>\n</svg>\n"
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--name", required=True, help="text to render, e.g. the tool name")
    ap.add_argument("--out", required=True, help="output SVG path")
    ap.add_argument("--font", help="path to a TTF font (default: Roboto Condensed)")
    ap.add_argument("--force", action="store_true", help="overwrite an existing file")
    args = ap.parse_args()

    out = Path(args.out).expanduser()
    if out.exists() and not args.force:
        sys.exit(f"{out} already exists (use --force to overwrite)")

    text = clean_text(args.name)
    svg = build_svg(text, load_font(find_font(args.font)))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg)
    print(f"wrote {out}  (slug: {slugify(args.name)})")


if __name__ == "__main__":
    main()
