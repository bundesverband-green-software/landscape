---
name: check-awesome-list
description: Diff the GSF awesome-green-software list against data.yml, judge which of its tools are missing here, and rewrite docs/awesome-green-software-gap.md. Use for a periodic gap check or a "what did the awesome list add this year" question.
---

# Check the awesome list against the landscape

Source: <https://github.com/Green-Software-Foundation/awesome-green-software>, a single `readme.md`. Output: `docs/awesome-green-software-gap.md`, the dated snapshot of the diff and its judgements, rewritten in place each run.

The list orders tools by what they measure, not by our tree, so it is a source of candidates rather than a merge target — and its prose has been wrong before, calling Carbonifer and Carbonara years dead when both had commits in 2024 and 2023. **The repository is the source of truth, the readme's prose is a hint.** Every claim gets checked against the commits.

## Step 1 — clone with full history

```sh
git clone https://github.com/Green-Software-Foundation/awesome-green-software.git ags
```

Clone outside this repo: the clone is a working copy for the run, not part of the landscape. Full clone, not `--filter=blob:none`: the `-S` searches in Step 3 read every historical `readme.md`, which on a partial clone means one network fetch per commit. It is ~30 MB.

Completion: `ags/readme.md` exists and `git -C ags log --oneline | head -1` prints a commit.

## Step 2 — diff both sides

```sh
uv run --with pyyaml python \
  .agents/skills/check-awesome-list/scripts/diff_list.py ags
```

Prints the counts, the matched pairs (`their name => our path`, flagged `[renamed]` where the names differ), the list-only entries as `name · list category · kind · url`, and the landscape-only entries grouped by subcategory.

The readme's shape, for reading around the script: under `## Tooling`, an entry is `- [name](url) - description`; the `### ` heading above it is the list's own category, which says nothing about ours; a trailing `![co]` badge marks a commercial product or vendor page, `![tool]` something you can run.

Completion: the script's `list:` count equals the `- [` count under `## Tooling`:

```sh
awk '/^## Tooling/{f=1;next} /^## /{f=0} f' ags/readme.md | grep -c '^- \['
```

A whole-file `grep -c '^- \[' readme.md` counts the Organizations, Courses, Articles, Books and Research sections too, so it never matches.

## Step 3 — date every entry

Earliest year the URL appeared, and the same for the name:

```sh
git -C ags log -S'<string>' --format=%ad --date=format:%Y -- readme.md | tail -1
```

Take the earlier of the two years. Pitfall: commit `b0fe7c5` (2026-08-04, `Added new reformating`) rewrote names and URLs across the file — `http` to `https`, added trailing slashes, `docs.microsoft.com` to `learn.microsoft.com`, `Eco-CI Continuous Integration Energy Estimation` to `Eco-CI` — so both searches can report 2026 for a tool listed since 2021. When both land on that year, date the entry against the readme from before it:

```sh
sha=$(git -C ags log --until=<YEAR>-01-01 -1 --format=%h -- readme.md) && git -C ags show $sha:readme.md
```

An entry present there is older, so its year comes from that readme; an entry absent from it entered in the reformat year.

Completion: every list-only entry carries a year, and every entry dated to the reformat year is either absent from the pre-reformat readme or names a source that confirms the year.

## Step 4 — eyeball the pairs

The script matches on normalized name (lowercase, non-alphanumerics dropped) and on URL, in both directions, because the list renames tools, links a repo where we link a project page, and lists a successor under the old name. Read the unmatched names by eye for exactly those cases, and expect both directions of error. A shared name is not proof of the same tool: `creedengo-ios` is a separate artefact from `Creedengo`, `ShiftPress Website Carbon Calculator` from `Website Carbon Calculator`. And an exact-match miss is not proof of absence: `oaklean.io` is our `oaklean`, `CO2Scope` our `CO2 Scope® (by EasyVirt)`, `CAST Highlight` our `CAST`, `Customer Carbon Footprint Tool` our `AWS Sustainability Console`, `OVHcloud Carbon Calculator` our `OVHcloud Environmental Impact Tracker` — five pairs no name or URL rule catches, so every run has to find them again.

Completion: every name in the list-only block is either a candidate for Step 5 or pinned to a landscape entry in a "in both, under a different name" row.

## Step 5 — measure each candidate

```sh
gh api repos/<owner>/<repo> --jq '.license.spdx_id, .stargazers_count, .pushed_at, .archived'
```

Plus a liveness check on the homepage and any project page (`curl -sS -L -o /dev/null -w '%{http_code} %{url_effective}'`), the README and docs for user and methodology documentation, and the release archive for non-GitHub projects (FreeIPMI's ftp listing dates every tarball).

Completion: each candidate carries a dated last push, a licence, a follow-checked live URL, and either a methodology link or the reason there is none.

## Step 6 — judge

Fit means the four prerequisites in `README.md`, section `Propose a new tool` — green software relation, public and functional, user docs, methodology docs. Methodology is owed only by a tool that computes a metric: a scheduler, linter or rule pack that outputs no number owes user documentation and the green relation, and is judged on those plus its status instead. A candidate that fails still gets a row and its reason: admitting it stays the maintainer's call.

Reasons that recur:

- **unmaintained**: no upstream commit for about two years, or archived. Name the date, not an age.
- **method, not tool**: coefficients, guidance or a dataset with no calculator.
- **API of a listed entry**: belongs in that entry's `extra.documentation_url`, not as a second item.
- **superseded**: the listed entry is the successor, so propose that one instead.
- **one calculator too many**: another website carbon estimator with nothing to distinguish it from the seven we list.
- **outside IT**: home energy rebates, battery-storage sizing.
- **no published method**: calibration kept server-side, an SEO audit with a green pitch. Only for a tool whose output is a number.
- **doubtful status**: the project labels itself experimental, which is below the beta the prerequisites ask for.

Completion: every candidate has `yes | partial | no` and a reason a maintainer can verify against the named source.

## Step 7 — write the snapshot

Rewrite `docs/awesome-green-software-gap.md`: a header line with the compared commit (`git -C ags rev-parse --short HEAD`), the readme's last commit date (`git -C ags log -1 --format=%ad --date=short -- readme.md`) and the run date; then the candidate tables ordered yes → partial → no, columns Name · In list since · What it is · URLs · Proposed category · Fit, one sentence on what the tool computes and from which data; then the "in both, under a different name" mapping; then the reverse appendix of our entries the list lacks, refreshed from `data.yml` and grouped by subcategory.

The header's counts are the script's, kept consistent: entries = matched + list-only, a name moved into the mapping table moves one from list-only to matched, and the appendix is the script's landscape-only block **minus** the landscape side of every mapping row — the script reports those pairs as two unmatched names, so copying its block wholesale double-counts them.

Proposed categories resolve against the tree as it stands and obey `add-tool` Step 2's limit: one primary plus `second_path`, every path existing in `data.yml`. A `second_path` must also be a subcategory that already holds that kind of tool: `AI Inference` and `Mobile Application` hold measurement tools only, so a scheduler, a factor dataset or a rule pack stays in its primary category.

Completion: `docs/awesome-green-software-gap.md` opens with the current commit, date and counts that add up, and every candidate from Steps 5–6 appears once.

## Step 8 — report

End the run with the list's own errors for upstream — a URL that redirects, a repo renamed, an entry still described as alive — each with the correct value, alongside the candidate verdicts.

Completion: the reply names the snapshot path, every candidate verdict, every upstream error.
