---
name: check-links
description: Check that every URL in data.yml is still reachable, rewrite redirect targets (including http:// -> https:// upgrades), and report what it found. Use when asked to check, validate, or fix links in the landscape.
---

# Check links in `data.yml`

Verifies `homepage_url`, `repo_url`, `blog` and `extra.documentation_url` for
every tool. Deduplicated and concurrent, so the whole file is checked in one go.

Every URL lands in exactly one bucket:

| Bucket | Meaning | Fails the check? |
|--------|---------|------------------|
| `ok` | 2xx, no redirect | no |
| `redirect` | 2xx after redirect(s); target is written back with `--write` | no |
| `broken` | 404/410/other 4xx, DNS failure, redirect loop | **yes** |
| `suspect` | 401/403/429 without a bot-challenge header, 5xx, timeout, other network error, plain `http://` with no upgrade | no |
| `challenge` | 401/403/429 with `cf-mitigated` / `x-vercel-mitigated: challenge` | no |

Only `broken` sets the exit code. The rule behind that: a denial cannot be
told apart from bot protection, so it must not block a merge — but it is still
printed on every run, so it stays visible.

## Step 1 — dry run

From the repo root:

```sh
uv run --with requests --with pyyaml python \
  .agents/skills/check-links/scripts/check_links.py
```

Prints every bucket except `ok` (with the tool/field each URL belongs to) plus
a one-line summary. Exit code `1` when something is `broken`, `0` otherwise.

## Step 2 — apply rewrites

```sh
uv run --with requests --with pyyaml python \
  .agents/skills/check-links/scripts/check_links.py --write
```

`--write` edits only the matched field lines, so YAML formatting is preserved.
It writes one kind of change, a redirect target — which is also how a plain
`http://` URL gets upgraded to `https://`. Review the diff afterwards, then
validate:

```sh
git diff data.yml
landscape2 validate data --data-file data.yml
```

## Redirects that are never written

`--write` leaves these alone and lists them under *Redirects ignored*:

- **cosmetic** — same scheme, and the target differs only by a trailing slash
  or a `www.`. This is notation, not a move. An `http://` -> `https://`
  redirect is *not* cosmetic and is written.
- **locale** — one side has a leading language segment the other lacks
  (`/solution` ↔ `/en/solution`). These flip direction over time, so writing
  either end bakes in a wrong URL; see Sopht in issues #67 and #74. Only
  known locale codes count (`en`, `de`, `pt-BR`, …), so `/go/docs` and
  `/ai/docs` are treated as real paths.
- **downgrade** — the target is `http://` while the source is `https://`. Never
  written.

Anything else counts as a real move and is written.

## Gotchas

- A plain `http://` page that serves 200 without redirecting is reported as
  `suspect`: find the `https://` URL of the same page by hand and put it in the
  field.
- Redirects are the HTTP kind; JavaScript/meta-refresh redirects are invisible
  to the checker and look like a normal 2xx.
- A target that still redirects on the next run is simply rewritten again; the
  script is idempotent.
- `suspect` is the noisy bucket on purpose. Before editing anything in it, open
  the URL in a browser — a 403 there is usually bot protection or IP reputation,
  not a dead page. Never rewrite a URL the script only reported.
- `.github/workflows/link-check.yml` runs the dry run weekly and keeps a single
  rolling issue: it edits the body in place and closes the issue once the check
  passes. A body edit sends no notification: the issue stays open and current,
  but nothing pings. `suspect` and `challenge` findings only ever appear in the
  run summary.

## Tests

The classification and rewrite decisions are covered by plain assertions. They
are not run in CI; run them by hand after changing the script:

```sh
uv run --with requests --with pyyaml python \
  .agents/skills/check-links/scripts/test_check_links.py
```
