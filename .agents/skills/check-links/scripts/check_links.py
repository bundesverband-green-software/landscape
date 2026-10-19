#!/usr/bin/env python3
"""Check every URL in data.yml for reachability and classify what answers.

Buckets, decided in classify():

- ok        2xx, no redirect.
- redirect  2xx after redirect(s). The final URL is written back to data.yml
            (--write) unless writing it would bake in a wrong URL: a notation
            change, an added locale prefix or an https->http downgrade (see
            redirect_ignore_reason()). An http:// link that redirects to
            https:// is upgraded this way.
- broken    404/410/other 4xx, NXDOMAIN, redirect loop. FAILS the check.
- suspect   401/403/429 without a bot-challenge header, 5xx, timeouts, other
            network errors, and a plain http:// link that serves no upgrade.
            Reported every run, never fails: a denial cannot be told apart from
            bot protection, so it must not block a merge.
- challenge 401/403/429 carrying cf-mitigated / x-vercel-mitigated: challenge.
            Proven bot protection, reported under its own heading.

Only broken sets the exit code. URLs are deduplicated and checked concurrently;
only the matched field lines are rewritten, so YAML formatting is preserved.

Usage:
    python3 check_links.py                 # dry run, report only
    python3 check_links.py --write         # apply redirect rewrites
    python3 check_links.py --write --workers 32 --timeout 20
"""

import argparse
import random
import re
import socket
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlsplit

import requests
import yaml

FIELDS = ("homepage_url", "repo_url", "blog", "documentation_url")
DEFAULT_DATA = "data.yml"
ATTEMPTS = 2
# Headers that prove a 401/403/429 is a challenge, not a verdict on the page.
CHALLENGE_HEADERS = ("cf-mitigated", "x-vercel-mitigated")
# Statuses that may be bot protection; never a failure on their own.
DENIED_STATUSES = (401, 403, 429)
# First path segments that are a language prefix. An explicit list, because
# /go/ and /ai/ are real paths too; region forms ("pt-BR") match on the base.
LOCALES = frozenset(
    ("de", "en", "es", "fr", "it", "ja", "ko", "nl", "pl", "pt", "ru", "sv",
     "tr", "zh")
)

# One session per worker thread; a browser-ish UA avoids 403s from strict sites.
_local = threading.local()


def session() -> requests.Session:
    s = getattr(_local, "session", None)
    if s is None:
        s = requests.Session()
        s.headers["User-Agent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        )
        s.max_redirects = 10
        _local.session = s
    return s


def backoff(r, attempt: int) -> float:
    """Delay before the next attempt: honour Retry-After, else 2**attempt, jittered."""
    delay = 2 ** attempt
    if r is not None:
        try:
            delay = min(30.0, max(0.0, float(r.headers.get("Retry-After", ""))))
        except ValueError:
            pass
    return delay * random.uniform(0.5, 1.5)


def is_challenge(r: requests.Response) -> bool:
    """True when the response headers say a bot challenge was served."""
    if r.status_code not in DENIED_STATUSES:
        return False
    return any(
        "challenge" in (r.headers.get(h) or "").lower() for h in CHALLENGE_HEADERS
    )


def dns_fails(url: str) -> bool:
    """Distinguish a dead host from a connection that was merely blocked."""
    host = urlsplit(url).hostname
    if not host:
        return True
    try:
        socket.getaddrinfo(host, None)
    except OSError:
        return True
    return False


def check(url: str, timeout: int):
    """Return (status|None, final_url|None, error|None, challenge)."""
    for attempt in range(ATTEMPTS):
        last = attempt + 1 == ATTEMPTS
        try:
            with session().get(
                url, timeout=timeout, allow_redirects=True, stream=True
            ) as r:
                r.raw.read(1)  # confirm the body is reachable, then stop
                # Retry throttling and server hiccups; a plain 403 is a
                # verdict, retrying it only wastes time.
                if not last and (r.status_code == 429 or r.status_code >= 500):
                    time.sleep(backoff(r, attempt))
                    continue
                return r.status_code, r.url, None, is_challenge(r)
        except requests.TooManyRedirects:
            return None, None, "too many redirects", False
        except requests.RequestException:
            if not last:
                time.sleep(backoff(None, attempt))
                continue
            return None, None, "dns" if dns_fails(url) else "network error", False
    raise AssertionError("unreachable")  # the last attempt always returns


def path_key(url: str):
    """Host+path+query, ignoring scheme, "www." and a trailing slash."""
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    return host, parts.path.rstrip("/"), parts.query


def classify(url: str, status, final, error, challenge: bool) -> str:
    """Bucket for one URL. See the module docstring."""
    if error:
        return "broken" if error in ("dns", "too many redirects") else "suspect"
    if status is None:
        return "suspect"
    if challenge:
        return "challenge"
    if status in DENIED_STATUSES:
        return "suspect"
    if 400 <= status < 500:
        return "broken"
    if status >= 500:
        return "suspect"
    if final and final != url:
        return "redirect"
    if urlsplit(url).scheme != "https":
        return "suspect"  # plain http:// that offers no upgrade; fix by hand
    return "ok"


def _segments(path: str) -> list[str]:
    return [s for s in path.split("/") if s]


def _strip_locale(segments: list[str]):
    if segments and segments[0].lower().split("-")[0] in LOCALES:
        return segments[1:], True
    return segments, False


def redirect_ignore_reason(old: str, new: str):
    """Why a redirect must not be written to data.yml, or None to write it."""
    a, b = urlsplit(old), urlsplit(new)
    if a.scheme == "https" and b.scheme == "http":
        return "downgrade"
    # Same scheme only: an http->https upgrade is a fix, not notation.
    if a.scheme == b.scheme and path_key(old) == path_key(new):
        return "cosmetic"
    # /solution <-> /en/solution: locale redirects flip direction over time, so
    # writing either end bakes in a wrong URL (see Sopht in #67 and #74).
    segs_a, had_locale_a = _strip_locale(_segments(a.path))
    segs_b, had_locale_b = _strip_locale(_segments(b.path))
    if had_locale_a != had_locale_b and segs_a == segs_b and a.query == b.query:
        return "locale"
    return None


def load_owners(path: Path):
    """Map URL -> sorted list of 'Item name (field)' for reporting."""
    owners: dict[str, list[str]] = {}
    data = yaml.safe_load(path.read_text())
    for cat in data.get("categories", []):
        for sub in cat.get("subcategories", []):
            for item in sub.get("items", []):
                if not isinstance(item, dict):
                    continue
                name = item.get("name", "?")
                extra = item.get("extra") or {}
                for field in FIELDS:
                    value = extra.get(field) if field == "documentation_url" else item.get(field)
                    if isinstance(value, str) and value.startswith(("http://", "https://")):
                        owners.setdefault(value, []).append(f"{name} ({field})")
    return owners


def rewrite(data_text: str, redirects: dict[str, str]):
    """Replace URL values on field lines; returns (new_text, lines_changed)."""
    pattern = re.compile(
        r"^(\s*(?:" + "|".join(FIELDS) + r"):\s*)(\S+)(\s*)$"
    )
    changed = 0

    def sub(m):
        nonlocal changed
        if m.group(2) in redirects:
            changed += 1
            return m.group(1) + redirects[m.group(2)] + m.group(3)
        return m.group(0)

    new_text = "\n".join(pattern.sub(sub, line) for line in data_text.split("\n"))
    return new_text, changed


def report(buckets, writable, ignored, owners):
    """Print the findings; returns the number of failing (broken) URLs."""

    def who(url):
        return "; ".join(owners.get(url, []))

    def show(bucket, headline, detail):
        entries = buckets[bucket]
        if not entries:
            return
        print(f"\n{headline} ({len(entries)}):")
        for url, status, final, error in entries:
            print(f"  {detail(status, final, error)}  {url}")
            if who(url):
                print(f"       {who(url)}")

    show("broken", "Broken (fails the check)",
         lambda status, final, error: status or error)

    if writable:
        print(f"\nRedirects ({len(writable)}):")
        for old, new in writable.items():
            print(f"  {old}\n    -> {new}" + (f"   [{who(old)}]" if who(old) else ""))

    if ignored:
        print(f"\nRedirects ignored ({len(ignored)}) "
              f"[notation, locale prefix or downgrade, not written]:")
        for old, new, reason in ignored:
            print(f"  ({reason})  {old}\n    -> {new}")

    show("suspect", "Suspect (not a failure - verify before editing)",
         lambda status, final, error: status or error)
    show("challenge", "Bot challenge (not a failure - headers prove it)",
         lambda status, final, error: status)

    return len(buckets["broken"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-file", default=DEFAULT_DATA)
    ap.add_argument("--write", action="store_true",
                    help="apply redirect rewrites")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--timeout", type=int, default=15)
    args = ap.parse_args()

    path = Path(args.data_file)
    text = path.read_text()
    owners = load_owners(path)
    urls = sorted(owners)

    print(f"Checking {len(urls)} unique URLs from {path} "
          f"({args.workers} workers, {args.timeout}s timeout)...", flush=True)

    results = {}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(check, u, args.timeout): u for u in urls}
        for fut in as_completed(futures):
            url = futures[fut]
            results[url] = fut.result()

    buckets: dict[str, list] = {
        "ok": [], "redirect": [],
        "broken": [], "suspect": [], "challenge": [],
    }
    writable: dict[str, str] = {}
    ignored: list[tuple[str, str, str]] = []
    for url in urls:
        status, final, error, challenge = results[url]
        bucket = classify(url, status, final, error, challenge)
        buckets[bucket].append((url, status, final, error))
        if bucket == "redirect":
            reason = redirect_ignore_reason(url, final)
            if reason:
                ignored.append((url, final, reason))
            else:
                writable[url] = final

    print("\n" + "=" * 72)
    failing = report(buckets, writable, ignored, owners)

    if args.write and writable:
        new_text, changed = rewrite(text, writable)
        path.write_text(new_text)
        print(f"\nWrote {changed} URL replacement(s) to {path}.")
        print("Now run: landscape2 validate data --data-file data.yml")
    elif writable:
        print("\nNo changes written (dry run). Re-run with --write to apply.")

    print(f"\nSummary: {len(buckets['ok'])} ok, {len(writable)} rewrite(s), "
          f"{len(ignored)} ignored redirect(s), "
          f"{len(buckets['challenge'])} bot challenge, "
          f"{len(buckets['suspect'])} suspect, {len(buckets['broken'])} broken.")
    if failing:
        broken_urls = " ".join(url for url, *_ in buckets["broken"])
        print(f"Exit code 1: {failing} broken URL(s): {broken_urls}")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
