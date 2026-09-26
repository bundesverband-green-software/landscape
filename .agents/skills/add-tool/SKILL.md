---
name: add-tool
description: Add a tool to data.yml for the green-software-landscape repo, either from a "Tool Proposal" GitHub issue (number or URL) or by researching a bare tool URL/name. Use when asked to add a tool to the landscape.
---

# Add a tool from a proposal issue

Repo: `bundesverband-green-software/landscape`. The proposal author is a
stranger and the issue template is only a guide — **verify everything against
the repository and flag inconsistencies instead of guessing.**

## Step 1 — get the input

The input is one of:

**A proposal issue** (issue number or issue URL):

```sh
gh issue view <NUMBER-OR-URL> --repo bundesverband-green-software/landscape \
  --json number,title,body,url
```

Parse the body by its `### Heading` sections. `_No response_` means empty.

**A bare tool URL or name** (no issue): research the tool instead.

- For a GitHub repo, get metadata:
  `gh repo view <owner/repo> --json name,description,homepageUrl,url,isArchived,licenseInfo`
- Fetch the homepage and the repo README/docs to learn what the tool does.

There are no curated answers (methodology, status), so every field is inferred:
mark it as inferred and surface it in the Step 6 report rather than presenting it
as fact. Also flag that a maintainer should review the entry more carefully.

## Step 2 — resolve categories against the CURRENT tree

The issue template's category options are already written as
`Category / Subcategory (hint)` paths. Strip the ` (hint)` suffix and you have
the path. Still verify every path against `data.yml` at runtime — it is the
source of truth, and the tree can change independently of the template. Read the
tree:

```sh
python3 -c "
import yaml
for c in yaml.safe_load(open('data.yml'))['categories']:
    print(c['name'])
    for s in c['subcategories']:
        print('  /', s['name'])
"
```

Match each proposed path to one in the tree:

- measurement dropdown → the Measurement tree (everything under
  Infrastructure & Cluster Level, Component, Code, Artificial Intelligence,
  Databases, Data Aggregation, Device & Process Level, Website, Measurement
  Utilities)
- optimization dropdown → the Optimization tree

(For a bare URL/name, propose categories from what the tool does and resolve
them the same way. Older issues may use the previous bare option names, e.g.
`Agent` or `Website Profiling` — match those by subcategory name against the
tree and flag any that no longer exist.)

The **first** resolved path is the item's primary location (insert the
`- item:` block there). Every other resolved path becomes a `second_path`
entry (`"Category / Subcategory"`), excluding the primary.

**Flag** any proposed category that:

- does not exist in the tree (the template may have drifted from the tree —
  flag it so the template can be fixed too)
- is ambiguous and cannot be resolved from context
- names a top-level category without a subcategory
- looks wrong for the tool described (e.g. a measurement tool proposed only
  under an optimization category)

## Step 3 — build the item

```yaml
          - item:
            name: <proposal Name, or the tool's name>
            description: <SHORT plain text — see rule below>
            homepage_url: <explicit homepage, else repo URL; required>
            repo_url: <if given>
            logo: <required; from proposal, add-logo, or found logo>
            project: "archived"   # only if deprecated/archived (see rule)
            second_path:
              - "<Category / Subcategory>"
            extra:
              documentation_url: <docs/methodology URL>
```

Field rules:

- **`description`** — Markdown/HTML are **not** supported. Write plain
  sentences, condensed from the proposal's description (mode A) or the
  homepage/repo description (mode B). There is no character limit, but keep it
  concise — shorter reads better on cards. Strip any markup. Keep methodology
  detail out, except for an important point in a short statement (studies and
  factors change, so don't go into detail); full detail belongs in
  `extra.documentation_url` and the PR.
- **`project`** — only ever `"archived"` or `"in-active-use-by-members"`.
  Set `"archived"` when the status is "Deprecated / Archived" (mode A) or the
  repo is archived (mode B). `"in-active-use-by-members"` is **not** derived
  from the proposal's Status dropdown; only set it if explicitly known, and
  flag it. For any other status, omit `project`.
- **`logo`** — **required by the schema**; an entry without it fails
  validation. Use the proposal's logo only if it is a usable file/path in
  `logos/`. Otherwise **do not insert the item**: flag it and hand off to the
  `add-logo` skill (create the logo first, then continue).
- **`license`** — do not set unless the proposal explicitly requires it;
  landscape2 fetches it from GitHub.

## Step 4 — methodology answers

There is **no field** for the methodology answers (metrics, grid intensity
method, scopes, direct/model, source data). `description` is deliberately kept
short, so it is not the right place either. Instead:

- record the methodology documentation URL in `extra.documentation_url`
- keep the methodology answers for the **PR description** (past the item block),
  where maintainers review them

If the proposal has no methodology URL, flag it.

## Step 5 — insert and validate

Insert the block directly into `data.yml` at the resolved primary location,
matching the surrounding 2-space indentation. Then:

```sh
landscape2 validate data --data-file data.yml
```

## Step 6 — report

End with a short **Needs human decision** list covering every flag from above
(unknown categories, missing logo, unclear status, missing methodology URL,
suspicious category choices). If there are none, say so explicitly.
