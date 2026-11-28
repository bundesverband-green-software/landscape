---
name: check-awesome-list
description: Diff the GSF awesome-green-software list against data.yml and judge which of its tools are missing here, with proposed categories and dated maintenance facts. Use for a periodic gap check, a "what did the awesome list add this year" question, or refreshing docs/awesome-green-software-gap.md.
---

# Check the awesome list against the landscape

Source: <https://github.com/Green-Software-Foundation/awesome-green-software>, a single `readme.md`. Output: `docs/awesome-green-software-gap.md`, the dated snapshot of the diff and its judgements, rewritten in place each run.

The list orders tools by what they measure, not by our tree, so it is a source of candidates rather than a merge target — and its prose about maintenance and about what a tool is has been wrong before (it claimed Carbonifer >3 years dead and Carbonara >5; the commits say 2024-07-13 and 2023-03-10). Every claim gets checked against the repository.

## Step 1 — clone with full history

```sh
git clone https://github.com/Green-Software-Foundation/awesome-green-software.git ags
```

Full clone, not `--filter=blob:none`: the `-S` searches in Step 3 read every historical `readme.md`, which on a partial clone means one network fetch per commit. The repo is ~13 MB.

Completion: `git -C ags log --oneline | head -1` prints a commit and the clone holds `readme.md`.

## Step 2 — extract both sides

**Their side.** Under `## Tooling`, entries are `- [name](url) - description`, and the `### ` heading above one is its list category. Note the kind badge at the end of the line — `co` marks a commercial product or vendor page, `tool` something you can run.

**Our side.** Parse `data.yml` with PyYAML: `categories[].subcategories[].items[]`. Each entry is a mapping whose fields sit *beside* the null `item:` key, so read `it.get('name')`, not `it['item']['name']` (the latter raises `'NoneType' object is not subscriptable`).

Completion: both sides are lists of `{name, url, description, category}` with counts matching `grep -c '^- \[' readme.md` under `## Tooling`.

## Step 3 — date every entry

Earliest year the URL appeared, and the same for the name:

```sh
git log -S'<string>' --format=%ad --date=format:%Y -- readme.md | tail -1
```

Pitfall: a mass reformat on 2026-08-04 rewrote URLs across the file, so `-S '<url>'` reports 2026 for tools listed since 2021 (`powercfg`, `codecarbon.io`, `Eco-CI`, `PowerAPI`, `WeDeex`). Take the earlier of the URL year and the name year; when both land on the reformat year, compare against the readme at the last commit before 1 January of it:

```sh
sha=$(git log --until=<YEAR>-01-01 -1 --format=%h -- readme.md) && git show $sha:readme.md
```

Completion: every entry has a year, and every year equal to the reformat year has passed the pre-year comparison.

## Step 4 — diff both directions

Normalize for matching — lowercase, strip `[^a-z0-9]` — and match on name, homepage URL and repo URL. Both directions, because the list renames tools, links repos where we link a project page, and lists the successor of a tool under its old name: ecoCode→Creedengo, ebb-ai→Tidegap, Customer Carbon Footprint Tool→AWS Sustainability Console, OVHcloud Carbon Calculator→our Environmental Impact Tracker, CAST Highlight→our CAST, PowDroid (repo vs. project page).

Then read the unmatched names by eye, because the automaton pairs things that are not the same tool: `creedengo-ios` matches `Creedengo`, `ShiftPress Website Carbon Calculator` matches `Website Carbon Calculator`.

Completion: each of their tooling entries sits in "already here" or "candidate", every candidate eyeballed.

## Step 5 — measure each candidate

```sh
gh api repos/<owner>/<repo> --jq '.license.spdx_id, .stargazers_count, .pushed_at, .archived'
```

Plus a liveness check on the homepage and any project page (`curl -sS -L -o /dev/null -w '%{http_code} %{url_effective}'`), the README and docs for user and methodology documentation, and the release archive for non-GitHub projects (FreeIPMI's ftp listing dates every tarball).

Completion: each candidate carries a dated last push, a licence, a follow-checked live URL, and either a methodology link or the reason there is none.

## Step 6 — judge

Fit means `README.md`'s prerequisites (green software relation, public and functional, user docs, methodology docs); `add-tool` holds how to test them. A candidate that fails still gets a row and its reason — admitting it stays the maintainer's call.

Reasons that recur:

- **unmaintained**: no upstream commit for about two years, or archived. Name the date, not an age — Carbonifer 2024-07-13, Carbonara 2023-03-10, turbostress 2021-03, ipmitool archived 2023-02, the cloudyspells PowerShell modules 2023.
- **method, not tool**: coefficients, guidance, a dataset with no calculator — Cloud Jewels, Well-Architected Framework.
- **API of a listed entry**: belongs in that entry's `extra.documentation_url`, not as a second item (Azure Carbon Service REST API).
- **superseded**: the listed entry is the successor, so propose that one instead (carbon-budget-action → `sci-disclose`).
- **one calculator too many**: another website carbon estimator, with nothing to distinguish it from the seven we list.
- **outside IT**: home energy rebates, battery-storage sizing.
- **no published method**: calibration kept server-side (AXIOMAX), an SEO audit with a green pitch (SEOCheck-AI).

Completion: every candidate has `yes | partial | no` and a reason a maintainer can verify against the named source.

## Step 7 — write the snapshot

Rewrite `docs/awesome-green-software-gap.md`: a header line with the compared commit (`git -C ags rev-parse --short HEAD`), the list's date and the run date; then the candidate tables ordered yes → partial → no, columns Name · In list since · What it is · URLs · Proposed category · Fit; then the "in both, under a different name" mapping; then the reverse appendix of our entries the list lacks, refreshed from `data.yml` and grouped by subcategory.

Proposed categories resolve against the tree as it stands and obey `add-tool` Step 2's limit: one primary plus `second_path`, every path existing in `data.yml`.

Completion: `docs/awesome-green-software-gap.md` opens with the current commit and date, and every candidate from Steps 5–6 appears once.

## Step 8 — report the list's own errors

A URL that redirects, a repo renamed, an entry still priced as alive: say so in the reply, so it can be fixed upstream.
