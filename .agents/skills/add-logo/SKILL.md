---
name: add-logo
description: Add or fix a tool's logo in the landscape — find the official mark or generate a text-only placeholder, place the file under logos/ and set `logo:` in data.yml.
---

# Add a logo

Every `data.yml` item needs a `logo:` pointing to a file that exists under `logos/` (`AGENTS.md`, section `Logos`, covers the three locations, the naming and the accepted formats).

## Step 1 — check what already exists

Read the tool's `data.yml` entry. If `logo:` is set and the file exists, report that and stop. Otherwise find the tool's homepage/repo (from the entry or the input).

## Step 2 — try to find a real logo

Look for an official mark before generating one:

- GitHub repo contents: `gh api repos/<owner>/<repo>/contents` and the same for likely dirs (`assets`, `docs`, `static`, `public`, `website`, `.github`).
- README images: `gh api repos/<owner>/<repo>/readme --jq .content | base64 -d`, then find the image URLs.
- Homepage: `og:image`, `<link rel="icon">` / apple-touch-icon as a last resort.

Download the candidates to a temp dir and **inspect each with the read tool** (images render, SVG as text):

- prefer SVG over raster
- prefer a logo with a **white/light background** (matches the rest of the landscape)
- if several look plausible, or you cannot tell which is the official mark, **give the user the candidate URLs and stop**

Place the chosen file as `logos/<slug>.<ext>` and set `logo: <slug>.<ext>`.

**Always tell the user the fetched logo needs a review** — provenance, quality, licensing — naming the source, and its license if the repo has one.

## Step 3 — no real logo: organization fallback

Identify the tool's parent organization (repo owner / company behind it). Use a file in `logos/organization/` **only if that organization has exactly one tool in the whole landscape** — otherwise several tools would share one logo. Count by scanning `data.yml` for the same organization. With any doubt, generate a placeholder instead and flag the ambiguity.

## Step 4 — no real logo and no eligible org logo: generate a placeholder

Name the file from the tool name: lowercase kebab-case, non-ASCII decorations stripped (`CO2 Scope®` → `co2-scope`). From the repo root:

```sh
uv run --with fonttools python .agents/skills/add-logo/scripts/generate_logo.py \
  --name "<Tool Name>" --out logos/unofficial/<slug>.svg
```

It emits black glyph outlines with a small margin around them, in the libre Roboto Condensed font. Font missing: install it (`apt install fonts-roboto` / `brew install --cask font-roboto-condensed`) or pass `--font /path/to/Font.ttf`. `--margin` (default `0.08` of the font size) controls the padding around the glyphs. `--force` overwrites an existing file; use it only when that is intended.

### Sizing and line breaks

Cards are ~70 px wide (explore card `70×90`, mobile `55×55`; grid cards vary with zoom), so a wide logo is width-limited: it renders about `70 / ratio` px tall, and a single long line becomes an unreadable strip.

- Keep the aspect ratio **≤ 5:1**; **~6:1 is the practical maximum** (the script warns above it, and at 6:1 the logo renders only ~12 px tall).
- Break at spaces and hyphens, keeping the hyphen at the end of the line (`grid-` / `intensity-go`), matching the existing placeholders.
- Nothing short alone on a line (`UK`, `go`): rebalance so every line has at least a few characters, roughly even. 2 lines is usually enough, 3 for long names. A single word with no break opportunity stays wide.
- Multi-line output is centred by default (`--align center`); single-line output is unaffected.

Then set `logo: unofficial/<slug>.svg` in `data.yml`.

## Step 5 — validate

```sh
landscape2 validate data --data-file data.yml
```

`validate` does not check that logo files exist, so also verify every reference:

```sh
python3 -c "
import yaml, pathlib
for c in yaml.safe_load(open('data.yml'))['categories']:
    for s in c['subcategories']:
        for i in s.get('items', []):
            logo = i.get('logo')
            if logo and not (pathlib.Path('logos') / logo).exists():
                print('MISSING', logo)
"
```

## Step 6 — report

End with a **Needs human decision** list: fetched-logo review, undecided candidate URLs, org-logo ambiguity, missing references. Say so when it is empty.
