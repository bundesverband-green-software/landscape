#!/usr/bin/env python3
"""Generate a text-only logo SVG (glyph outlines) for a landscape tool.

Run via:  uv run --with fonttools python generate_logo.py --name "Tool Name" --out logos/unofficial/tool-name.svg

Uses a local libre condensed font (Roboto Condensed Bold by default) and emits
black glyph <path> outlines with a small margin around the glyphs, matching the
style of the existing logos/unofficial/*.svg placeholders. No network, no
permanent deps.
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


def build_svg(text: str, font: TTFont, size: float = 100.0,
              line_gap: float = 1.25, align: str = "left",
              margin: float = 0.08) -> str:
    upem = font["head"].unitsPerEm
    scale = size / upem
    cmap = font.getBestCmap()
    glyphset = font.getGlyphSet()
    hmtx = font["hmtx"]

    def render_line(line: str, y_baseline: float) -> tuple[list[str], tuple | None, float]:
        paths: list[str] = []
        bounds = None
        x = 0.0
        for ch in line:
            gname = cmap.get(ord(ch))
            if gname is None:
                gname = cmap.get(ord(" "))  # fall back to a space advance
            if gname is None:
                continue
            transform = Transform(scale, 0, 0, -scale, x, y_baseline)
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
        return paths, bounds, x

    lines = text.splitlines() or [text]
    line_height = size * line_gap

    rendered: list[tuple[list[str], tuple | None, float]] = []
    for i, line in enumerate(lines):
        rendered.append(render_line(line, i * line_height))

    # Centre lines within the widest line. Use the advance width rather than the
    # ink width: otherwise a line can shift past the bounding box and get clipped
    # at the viewBox edge.
    max_advance = max((advance for _, _, advance in rendered), default=0.0)

    shifts: list[float] = []
    all_bounds = None
    for _, b, advance in rendered:
        dx = (max_advance - advance) / 2.0 if align == "center" else 0.0
        shifts.append(dx)
        if b is None:
            continue
        shifted = (b[0] + dx, b[1], b[2] + dx, b[3])
        all_bounds = shifted if all_bounds is None else (
            min(all_bounds[0], shifted[0]), min(all_bounds[1], shifted[1]),
            max(all_bounds[2], shifted[2]), max(all_bounds[3], shifted[3]),
        )
    if all_bounds is None:
        sys.exit("no drawable glyphs in the provided name")

    x0, y0, x1, y1 = all_bounds
    w, h = x1 - x0, y1 - y0
    # Breathing room so glyphs never touch the viewBox border.
    pad = margin * size

    body_parts: list[str] = []
    for (paths, _, _), dx in zip(rendered, shifts):
        for d in paths:
            if dx:
                body_parts.append(f'<path transform="translate({dx:.2f},0)" d="{d}"/>')
            else:
                body_parts.append(f'<path d="{d}"/>')
    body = "\n".join(body_parts)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w + 2 * pad:.2f} {h + 2 * pad:.2f}">\n'
        f'<g fill="#000000" transform="translate({pad - x0:.2f},{pad - y0:.2f})">\n'
        f"{body}\n</g>\n</svg>\n"
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--name", required=True, help="text to render, e.g. the tool name")
    ap.add_argument("--out", required=True, help="output SVG path")
    ap.add_argument("--font", help="path to a TTF font (default: Roboto Condensed)")
    ap.add_argument("--line-gap", type=float, default=1.25,
                    help="line height as a multiple of the font size (default: 1.25)")
    ap.add_argument("--align", choices=("left", "center"), default="left",
                    help="horizontal alignment of lines (default: left)")
    ap.add_argument("--margin", type=float, default=0.08,
                    help="padding around the glyphs as a fraction of the font size (default: 0.08)")
    ap.add_argument("--force", action="store_true", help="overwrite an existing file")
    args = ap.parse_args()

    out = Path(args.out).expanduser()
    if out.exists() and not args.force:
        sys.exit(f"{out} already exists (use --force to overwrite)")

    text = clean_text(args.name)
    svg = build_svg(text, load_font(find_font(args.font)),
                    line_gap=args.line_gap, align=args.align, margin=args.margin)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg)
    print(f"wrote {out}  (slug: {slugify(args.name)})")


if __name__ == "__main__":
    main()
