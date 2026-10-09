#!/usr/bin/env python3
"""Check every URL in data.yml for reachability.

- 2xx                     -> OK
- 2xx after redirect(s)   -> redirect: final URL is written back to data.yml (--write)
- 403/429 from a listed host -> tolerated false positive (see false-positive-hosts.txt)
- any other 4xx / 5xx / network err -> reported, never written

URLs are deduplicated and checked concurrently. Only the matched field lines
are rewritten, so YAML formatting is preserved.

Usage:
    python3 check_links.py                 # dry run, report only
    python3 check_links.py --write         # apply redirect rewrites
    python3 check_links.py --write --workers 32 --timeout 20
"""

import argparse
import re
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
FALSE_POSITIVES_FILE = Path(__file__).resolve().parent.parent / "false-positive-hosts.txt"
# Only bot-protection statuses are excused for listed hosts; never 5xx/DNS.
TOLERATED_STATUSES = (403, 429)

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


def retry_delay(r: requests.Response, attempt: int) -> float:
    """Seconds to wait after a 429: honor Retry-After, else 1s, 2s, ..."""
    value = r.headers.get("Retry-After", "")
    try:
        return min(30.0, max(0.0, float(value)))  # ponytail: 30s cap, raise if GitHub asks for more and it matters
    except ValueError:
        return 2 ** attempt


def check(url: str, timeout: int):
    """Return (status_code|None, final_url|None, error|None)."""
    for attempt in range(2):  # one retry for transient errors and 429
        try:
            with session().get(
                url, timeout=timeout, allow_redirects=True, stream=True
            ) as r:
                r.raw.read(1)  # confirm the body is reachable, then stop
                if r.status_code == 429 and attempt == 0:
                    time.sleep(retry_delay(r, attempt))
                    continue
                return r.status_code, r.url, None
        except requests.TooManyRedirects:
            return None, None, "too many redirects"
        except requests.RequestException as e:
            if attempt == 1:
                return None, None, type(e).__name__
            time.sleep(1)
    return None, None, "unknown error"


def load_false_positive_hosts(path: Path) -> list[str]:
    """Host suffixes whose 403/429 answers are treated as bot protection."""
    if not path.is_file():
        return []
    hosts = []
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip().lower()
        if line:
            hosts.append(line)
    return hosts


def is_tolerated(url: str, status: int, hosts: list[str]) -> bool:
    if status not in TOLERATED_STATUSES:
        return False
    host = (urlsplit(url).hostname or "").lower()
    return any(host == h or host.endswith("." + h) for h in hosts)


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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-file", default=DEFAULT_DATA)
    ap.add_argument("--write", action="store_true", help="apply redirect rewrites")
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

    false_positive_hosts = load_false_positive_hosts(FALSE_POSITIVES_FILE)
    redirects = {}
    client_errors, server_errors, network_errors, tolerated = [], [], [], []
    for url in urls:
        status, final, error = results[url]
        if error or status is None:
            network_errors.append((url, error))
        elif is_tolerated(url, status, false_positive_hosts):
            tolerated.append((url, status))
        elif 400 <= status < 500:
            client_errors.append((url, status))
        elif status >= 500:
            server_errors.append((url, status))
        elif final and final != url:
            redirects[url] = final

    print("\n" + "=" * 72)

    if redirects:
        print(f"\nRedirects ({len(redirects)}) -> "
              f"{'written to ' + str(path) if args.write else 'dry run, use --write'}:")
        for old, new in redirects.items():
            who = "; ".join(owners.get(old, []))
            print(f"  {old}\n    -> {new}   [{who}]")

    if client_errors:
        print(f"\n4xx client errors ({len(client_errors)}):")
        for url, st in client_errors:
            print(f"  {st}  {url}\n       {', '.join(owners.get(url, []))}")

    if server_errors:
        print(f"\n5xx server errors ({len(server_errors)}):")
        for url, st in server_errors:
            print(f"  {st}  {url}\n       {', '.join(owners.get(url, []))}")

    if network_errors:
        print(f"\nNetwork errors ({len(network_errors)}):")
        for url, err in network_errors:
            print(f"  {err}  {url}\n       {', '.join(owners.get(url, []))}")

    if tolerated:
        print(f"\nTolerated false positives ({len(tolerated)}) "
              f"[{FALSE_POSITIVES_FILE.name}: known 403/429 hosts]:")
        for url, st in tolerated:
            print(f"  {st}  {url}\n       {', '.join(owners.get(url, []))}")

    if args.write and redirects:
        new_text, changed = rewrite(text, redirects)
        path.write_text(new_text)
        print(f"\nWrote {changed} URL replacement(s) to {path}.")
        print("Now run: landscape2 validate data --data-file data.yml")
    elif redirects:
        print("\nNo changes written (dry run). Re-run with --write to apply.")

    problems = len(client_errors) + len(server_errors) + len(network_errors)
    print(f"\nSummary: {len(urls) - len(redirects) - problems - len(tolerated)} ok, "
          f"{len(redirects)} redirect(s), {len(tolerated)} tolerated, "
          f"{problems} problem(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
