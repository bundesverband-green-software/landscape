---
name: check-links
description: Check that every URL in data.yml is still reachable and rewrite redirect targets (including http:// -> https:// upgrades). Use when asked to check the landscape's links, or to fix a link someone reported dead.
---

# Check links in `data.yml`

Verifies `homepage_url`, `repo_url`, `blog` and `extra.documentation_url` for every tool. Deduplicated and concurrent, so the whole file is checked in one go.

Every URL lands in exactly one bucket:

| Bucket | Meaning | Fails the check? |
|--------|---------|------------------|
| `ok` | 2xx, no redirect | no |
| `redirect` | 2xx after redirect(s); target is written back with `--write` | no |
| `broken` | 404/410/other 4xx, DNS failure, redirect loop | **yes** |
| `suspect` | 401/403/429 without a bot-challenge header, 5xx, timeout, other network error, plain `http://` with no upgrade | no |
| `challenge` | 401/403/429 with `cf-mitigated` / `x-vercel-mitigated: challenge` | no |

Only `broken` sets the exit code: a denial cannot be told apart from bot protection, so it must not block a merge — it still prints on every run, so it stays visible.

## Step 1 — dry run

From the repo root:

```sh
uv run --with requests --with pyyaml python \
  .agents/skills/check-links/scripts/check_links.py
```

Prints every bucket except `ok` (with the tool/field each URL belongs to) plus a one-line summary. Exit code `1` when something is `broken`, `0` otherwise.

## Step 2 — apply rewrites

```sh
uv run --with requests --with pyyaml python \
  .agents/skills/check-links/scripts/check_links.py --write
```

`--write` edits only the matched field lines, so YAML formatting is preserved. It writes one kind of change, a redirect target — which is also how a plain `http://` URL gets upgraded to `https://`. Review the diff afterwards, then validate:

```sh
git diff data.yml
landscape2 validate data --data-file data.yml
```

## Redirects that are never written

`--write` leaves these alone and lists them under *Redirects ignored*:

- **cosmetic** — same scheme, and the target differs only by a trailing slash or a `www.`. This is notation, not a move. An `http://` -> `https://` redirect is *not* cosmetic and is written.
- **locale** — one side has a leading language segment the other lacks (`/solution` ↔ `/en/solution`). These flip direction over time, so writing either end bakes in a wrong URL. Only known locale codes count (`en`, `de`, `pt-BR`, …), so `/go/docs` and `/ai/docs` are treated as real paths.
- **downgrade** — the target is `http://` while the source is `https://`. Never written.

Anything else counts as a real move and is written.

## Gotchas

- A plain `http://` page that serves 200 without redirecting is reported as `suspect`: find the `https://` URL of the same page by hand and put it in the field.
- Redirects are the HTTP kind; JavaScript/meta-refresh redirects are invisible to the checker and look like a normal 2xx.
- `suspect` is the noisy bucket on purpose. Open the URL in a browser before touching it — a 403 there is usually bot protection or IP reputation, not a dead page. Rewrite only redirects the script found.
- `.github/workflows/link-check.yml` runs the dry run weekly against a single rolling issue (body edited in place, closed once the check passes), so an edit sends no notification. `suspect` and `challenge` findings appear only in the run summary.

## Tests

The classification and rewrite decisions are covered by plain assertions. They are not run in CI; run them by hand after changing the script:

```sh
uv run --with requests --with pyyaml python \
  .agents/skills/check-links/scripts/test_check_links.py
```
