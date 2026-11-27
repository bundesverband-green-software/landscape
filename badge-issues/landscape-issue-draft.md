# Suggest the landscape badge to the listed repositories

We started providing badges a few days ago, one per sub-category: GitHub-hosted versions in [BADGES.md](https://github.com/bundesverband-green-software/landscape/blob/main/BADGES.md) and shields.io versions in [BADGES_SHIELDS_IO.md](https://github.com/bundesverband-green-software/landscape/blob/main/BADGES_SHIELDS_IO.md). I think it would make sense to open an issue in all open source repositories. This issue is to settle the wording before we do that.

## Scope

- 87 landscape entries link a repository. That leaves 73 distinct GitHub repositories after dropping 11 archived entries, one repository that is not on GitHub (Perf, kernel.org), and after collapsing entries that share a repository (WebNRG → `green-metrics-tool`, Green Algorithms Calculator (AI) → Green Algorithms Calculator).
- 3 repositories already carry the badge and are skipped: `green-metrics-tool`, `eco-ci-energy-estimation`, `cloud-energy`.
- 70 issues remain. Drafts and the repository table: branch [`badge-issue-drafts`](https://github.com/bundesverband-green-software/landscape/tree/badge-issue-drafts/badge-issues), the table is in its `README.md`.
- Every README was fetched and searched for `bundesverband-green-software` and `Green%20Software%20Landscape`. No other repository has it.

## Template

Each issue uses the **primary** sub-category of the landscape entry for the preview and the snippets. The other sub-categories of the entry (from `second_path`) are mentioned in one sentence, since other badges fit as well.

Example: CodeCarbon

````markdown
Hi! CodeCarbon is listed in the [Green Software Landscape](https://landscape.bundesverband-green-software.de), a directory of relevant Green Software tools categorized into a landscape. It is run by the [Bundesverband Green Software](https://www.bundesverband-green-software.de/), a German NGO with currently over 30 member companies. The landscape itself is open source: [bundesverband-green-software/landscape](https://github.com/bundesverband-green-software/landscape).

We recently started to provide badges, one per sub-category of the landscape. CodeCarbon would fit **Code Level Energy Measurement**. It is also listed under **AI Model Training** and **Device Measurement**, so other badges may fit as well.

[![Green Software Landscape: Code Level Energy Measurement](https://raw.githubusercontent.com/bundesverband-green-software/landscape/refs/heads/main/badges/code-level-energy-measurement.svg)](https://landscape.bundesverband-green-software.de)

To show it in your README, copy either line:

Badge hosted in our repo ([list of all badges](https://github.com/bundesverband-green-software/landscape/blob/main/BADGES.md)):

```markdown
[![Green Software Landscape: Code Level Energy Measurement](https://raw.githubusercontent.com/bundesverband-green-software/landscape/refs/heads/main/badges/code-level-energy-measurement.svg)](https://landscape.bundesverband-green-software.de)
```

Via shields.io ([list of all shields.io badges](https://github.com/bundesverband-green-software/landscape/blob/main/BADGES_SHIELDS_IO.md)):

```markdown
[![Green Software Landscape: Code Level Energy Measurement](https://img.shields.io/badge/Green%20Software%20Landscape-Code%20Level%20Energy%20Measurement-grey?labelColor=rgb%283%2C150%2C69%29)](https://landscape.bundesverband-green-software.de)
```

No obligation — close this if you would rather not carry the badge.
````

For member organizations and organizations close to the Bundesverband the introduction is dropped and a simplified template is used: green-coding-solutions, green-kernel, neuland, bluehands, envite-consulting, hitabisgmbh, RETIT. That is 9 of the 70 drafts.

One exception: for `caas-team/GoKubeDownscaler` the badge was already offered in [#80](https://github.com/bundesverband-green-software/landscape/pull/80) and the maintainer agreed to add it, so that issue links the pull request and leaves out the closing "No obligation" line.

## Before posting

- Check each repository's `CONTRIBUTING.md` and issue templates first; hold back where bulk or agent-written issues are unwelcome.
- Post one issue per repository, nothing until this issue is settled.

## Feedback

@ArneTR @KollinFreise @glatzg @saboehme @hagemic

What do you think about this approach? Is it ok to open 70 issues just to propose to add our badge to their repository?
Also let me know, if you have feedback to the template.
