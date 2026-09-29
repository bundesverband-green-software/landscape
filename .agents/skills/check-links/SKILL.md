---
name: check-links
description: Check that every URL in data.yml is still reachable, rewrite http redirects to their final URL, and report 4xx/5xx/network failures. Use when asked to check, validate, or fix links in the landscape.
---

# Check links in `data.yml`

Verifies `homepage_url`, `repo_url`, `blog` and `extra.documentation_url` for
every tool. Deduplicated and concurrent, so the whole file is checked in one go.

- **2xx** — reachable, nothing to do.
- **redirect** — the request was answered by one or more 3xx responses that end
  in a 2xx; the final URL is written back to `data.yml`.
- **4xx / 5xx / network error** — reported only; never rewritten.

## Step 1 — dry run

From the repo root:

```sh
uv run --with requests --with pyyaml python \
  .agents/skills/check-links/scripts/check_links.py
```

Prints a report of redirects and failures, including which tool/field each URL
belongs to (successful URLs are not listed). Exit code is `1` when there is at
least one 4xx/5xx/network problem, `0` otherwise.

## Step 2 — apply redirect rewrites

```sh
uv run --with requests --with pyyaml python \
  .agents/skills/check-links/scripts/check_links.py --write
```

The script edits only the matched field lines, so the YAML formatting is
preserved. Review the diff afterwards, then validate:

```sh
git diff data.yml
landscape2 validate data --data-file data.yml
```

## Step 3 — triage the failures (low effort)

For each reported 4xx/5xx/network URL, make a **quick** attempt to find the
right URL (e.g. search the site or GitHub for the new location). If it is not
found with low effort, stop — leave the field untouched and report the issue to
the user instead. Do not spend a lot of time chasing dead links; a reported
issue is an acceptable outcome.

- **Moved / dead** — update the field to the new URL, or leave it and report.
- **Bot protection (403/429) and timeouts** — often false positives. Open the
  URL in a browser before changing anything.
- **5xx** — usually temporary; re-check before editing.

Do not auto-edit anything the script reported as a failure — the script only
writes redirects it confirmed as 2xx.

## Known false positives

These hosts commonly answer automated clients with 403/429 even though the page
is fine. They live in `false-positive-hosts.txt` (one host suffix per line) so
the list is data, not prose — add an entry only after verifying in a browser.

The script reports them under **Tolerated false positives** and they do **not**
count toward its exit code. Only 403/429 are excused, and only for listed hosts;
DNS failures, timeouts and 5xx are still real problems. Matching is by host
suffix, so `electricitymaps.com` covers `app.` and `portal.`.

## Gotchas

- Redirects are the HTTP kind; JavaScript/meta-refresh redirects are invisible
  to it and look like a normal 2xx.
- A final URL that still redirects on the next run will simply be rewritten
  again; the script is idempotent.
- Report the failures and what you changed in the PR/summary; call out
  false-positive suspects explicitly.
