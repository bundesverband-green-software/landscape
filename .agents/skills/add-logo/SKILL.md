---
name: add-logo
description: Ensure a tool in the green-software-landscape repo has a proper logo file in logos/ and a matching logo field in data.yml, by finding a real logo or generating a text-only placeholder. Use when adding a tool without a logo, or when asked to add/fix a tool logo.
---

# Add a logo

Every `data.yml` item needs a `logo:` pointing to an existing file under `logos/`.
Locations: root `logos/` (the tool's own logo), `logos/organization/` (parent
org logo), `logos/unofficial/` (generated placeholder). Raster is accepted
(SVG/PNG/JPG/WebP), but prefer SVG. New filenames **must** be lowercase
kebab-case.

## Step 1 — check what already exists

Read the tool's `data.yml` entry. If `logo:` is set and the file exists, you are
done. Otherwise find the tool's homepage/repo (from the entry or the input).

## Step 2 — try to find a real logo

Look for an official mark before generating one:

- GitHub repo contents:
  `gh api repos/<owner>/<repo>/contents` and the same for likely dirs
  (`assets`, `docs`, `static`, `public`, `website`, `.github`).
- README images:
  `gh api repos/<owner>/<repo>/readme --jq .content | base64 -d` then find image URLs.
- Homepage: `og:image`, `<link rel="icon">` / apple-touch-icon as a last resort.

Download candidates to a temp dir and **inspect each one with the read tool**
(images are rendered, SVG as text). Rules:

- prefer SVG over raster
- prefer a logo with a **white/light background** (matches the rest of the landscape)
- if several look plausible, or you cannot tell which is the official mark,
  **give the user the candidate URLs and stop**

Place the chosen file as `logos/<slug>.<ext>` and set `logo: <slug>.<ext>`.
Slug = lowercase kebab-case of the tool name (see Step 4).

**Always tell the user the fetched logo needs a review** (provenance, quality,
licensing). Mention the source and its license if the repo has one.

## Step 3 — no real logo: organization fallback

Identify the tool's parent organization (repo owner / company behind it). Use a
file in `logos/organization/` **only if that organization has exactly one tool
in the whole landscape** — otherwise several tools would share one logo. Count
by scanning `data.yml` for the same organization. If there is any doubt, do not
reuse it: generate a placeholder instead and flag the ambiguity.

## Step 4 — no real logo and no eligible org logo: generate a placeholder

Name the file from the tool name: lowercase kebab-case, non-ASCII decorations
stripped (`CO2 Scope®` → `co2-scope`). From the repo root, run the bundled
script:

```sh
uv run --with fonttools python .agents/skills/add-logo/scripts/generate_logo.py \
  --name "<Tool Name>" --out logos/unofficial/<slug>.svg
```

It emits black glyph outlines with a tight viewBox using the libre Roboto
Condensed font. If that font is missing, install it
(`apt install fonts-roboto` / `brew install --cask font-roboto-condensed`) or
pass `--font /path/to/Font.ttf`. Never overwrite an existing file silently —
`--force` only when that is intended.

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

End with a **Needs human decision** list: fetched-logo review, undecided
candidate URLs, org-logo ambiguity, or any missing reference.
