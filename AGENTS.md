# AGENTS.md — Green Software Landscape

Tool landscape of the Bundesverband Green Software (<https://landscape.bundesverband-green-software.de>). No application code: the CNCF [landscape2](https://github.com/cncf/landscape2) generates the site from three YAML files and `logos/`. Per-task procedures — adding a tool, fixing a logo, checking links — live in `.agents/skills/*/SKILL.md`.

## Source of truth

| File           | Purpose                                                                                    |
|----------------|--------------------------------------------------------------------------------------------|
| `data.yml`     | All tools + the category tree. The file you touch most.                                     |
| `settings.yml` | Site config: colors, `groups:` (which categories count as measurement vs optimization), featured items, header/footer links. |
| `guide.yml`    | In-site guide text, mixed German and English.                                               |
| `logos/`       | Tool logos, see below.                                                                      |

`build/` and `cache/` are generated from these. `.github/workflows/deploy.yaml` builds and deploys to GitHub Pages on push to `main`.

## Tool entries (`data.yml`)

An item is an `- item:` block inside a subcategory's `items:`. Every tool lives in exactly one category; `second_path` lists the other places it appears.

Required fields:

```yaml
- item:
  name: Tool Name
  description: One or two short plain-text sentences. No Markdown/HTML.
  homepage_url: https://example.com/
  logo: toolname.svg
```

- `repo_url`, `blog` — optional links.
- `license` — leave it out; landscape2 fetches it from GitHub. Set it only when fetching fails (no repo, or `repo_url` missing).
- `project` — exactly two values exist. `"archived"` greys the tool out; `"in-active-use-by-members"` means member organizations use it in practice. It is **not** CNCF-style maturity.
- `second_path` — `"Category / Subcategory"` strings; both parts must match names in `data.yml` exactly.
- `extra.documentation_url` — prefer the page that describes the methodology (how metrics are measured/calculated), else the main user docs:
  - current/latest version, not an `archive/` path
  - methodology spread over several pages → the main docs page
  - skip a page that only *claims* a methodology without publishing it

Indentation is 2-space steps matching the neighbouring entry; multi-line descriptions use the `|` block scalar.

Gotcha: a new top-level category also needs a `groups:` entry in `settings.yml`, or it does not render on the site.

## Logos

`logo:` is relative to `logos/` and the file must exist:

- `logos/` — the tool's own logo (SVG preferred; PNG, JPG and WebP accepted)
- `logos/organization/` — the parent organization's logo
- `logos/unofficial/` — generated text-only placeholder

Filenames are lowercase kebab-case, initials and punctuation included (`CO2.js.svg` → `co2-js.svg`).

## Validate before finishing any YAML change

```sh
landscape2 validate data     --data-file data.yml
landscape2 validate settings --settings-file settings.yml
landscape2 validate guide    --guide-file guide.yml
```

Local build and serve: see `## Local usage` in `README.md`.

## Conventions

- `description` fields and docs are English; `guide.yml` mixes German and English — match the file you edit.
- New tools must meet the prerequisites in `README.md`, section `Propose a new tool` — check them before an entry goes in, not after.
- PRs use `.github/pull_request_template.md`; it asks how the tool's methodology is documented.
