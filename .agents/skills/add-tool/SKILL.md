---
name: add-tool
description: Add a tool to the landscape's data.yml, either from a "Tool Proposal" GitHub issue (number or URL) or by researching a bare tool URL/name.
---

# Add a tool from a proposal issue

Repo: `bundesverband-green-software/landscape`. The proposal author is a stranger and the issue template is only a guide — **verify everything against the repository and flag inconsistencies instead of guessing.**

Fit comes before fields. The landscape admits a tool only if it is Green Software related, publicly available and functional (minimum beta), and ships user docs plus methodology docs (`README.md`, section `Propose a new tool`). A candidate missing one still gets its item built, but the gap goes into the Step 6 report: admitting it is the maintainer's call, not yours. The item block's field rules live in `AGENTS.md`, section `Tool entries`.

## Step 1 — get the input

**A proposal issue** (number or URL):

```sh
gh issue view <NUMBER-OR-URL> --repo bundesverband-green-software/landscape \
  --json number,title,body,url
```

Parse the body by its `### Heading` sections. `_No response_` means empty.

**A bare tool URL or name** (no issue): research the tool instead.

- GitHub repo: `gh repo view <owner/repo> --json name,description,homepageUrl,url,isArchived,licenseInfo`
- Fetch the homepage and the repo README/docs to learn what the tool does.

Nothing is curated in this mode (methodology, status), so every field is inferred: mark it as inferred in the Step 6 report, and say a maintainer should review the entry more carefully.

## Step 2 — resolve categories against the current tree

The template's category options are written as `Category / Subcategory (hint)` paths: strip the ` (hint)` suffix and you have the path. Its two dropdowns map to the two `groups:` in `settings.yml` (measurement, optimization).

Read the tree from `data.yml`, the source of truth — it changes independently of the template:

```sh
python3 -c "
import yaml
for c in yaml.safe_load(open('data.yml'))['categories']:
    print(c['name'])
    for s in c['subcategories']:
        print('  /', s['name'])
"
```

Match every proposed path to one in the tree. Pick the one that fits the tool **semantically best** as its primary location — that is where the `- item:` block is inserted. Every other resolved path becomes a `second_path` entry (`"Category / Subcategory"`), excluding the primary.

A tool appears in **at most 2 categories in total** (primary plus its `second_path` entries). If the proposal selects more, keep the best-fitting ones and flag the rest for the user to decide.

**Flag** any proposed category that:

- does not exist in the tree (the template drifts from the tree — flag it so the template can be fixed too)
- is ambiguous and cannot be resolved from context
- names a top-level category without a subcategory
- looks wrong for the tool described (e.g. a measurement tool proposed only under an optimization category)

## Step 3 — build the item

```yaml
          - item:
            name: <proposal Name, or the tool's name>
            description: <SHORT plain text — see below>
            homepage_url: <explicit homepage, else repo URL; required>
            repo_url: <if given>
            logo: <required; from proposal, add-logo, or found logo>
            project: "archived"   # only if deprecated/archived
            second_path:
              - "<Category / Subcategory>"
            extra:
              documentation_url: <docs/methodology URL>
```

What a proposal changes:

- **`description`** — condense it from the proposal's description (issue) or the homepage/repo description (bare URL), stripping the markup. Methodology detail belongs in `extra.documentation_url` and the PR: studies and factors change, so a short statement at most.
- **`project`** — `"archived"` when the status is "Deprecated / Archived" or the repo is archived. Nothing in a proposal derives `"in-active-use-by-members"`: set it only if explicitly known, and flag it.
- **`logo`** — required by the schema, so an entry without it fails validation. Use the proposal's logo only if it is a usable file in `logos/`. Otherwise **do not insert the item**: run the `add-logo` skill first, then continue.

## Step 4 — methodology answers

There is **no field** for the methodology answers (metrics, grid intensity method, scopes, direct/model, source data), and `description` is deliberately short. Instead:

- record the methodology documentation URL in `extra.documentation_url`
- carry the methodology answers into the **PR description**, past the item block, where maintainers review them

A proposal with no methodology URL gets flagged.

## Step 5 — insert and validate

Insert the block at the resolved primary location, matching the surrounding 2-space indentation, then:

```sh
landscape2 validate data --data-file data.yml
```

## Step 6 — report

End with a short **Needs human decision** list covering every flag from above (unknown categories, missing logo, unclear status, missing methodology URL, suspicious category choices), and say explicitly when there are none.
