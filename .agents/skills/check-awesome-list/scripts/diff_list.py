#!/usr/bin/env python3
"""Extract both tool lists and diff them by name and URL, in both directions.

Usage, from the repo root: python .agents/skills/check-awesome-list/scripts/diff_list.py <awesome-clone>

Prints three blocks: matched pairs, list-only entries (the candidates), and landscape-only entries grouped by subcategory.
"""

import re
import sys
from pathlib import Path

import yaml


def norm(text):
    return re.sub(r"[^a-z0-9]", "", (text or "").lower())


def norm_url(url):
    url = (url or "").strip().lower()
    url = re.sub(r"^[a-z]+://", "", url)
    url = re.sub(r"^www\.", "", url)
    url = url.split("#")[0].split("?")[0].rstrip("/")
    url = re.sub(r"^github\.com/([^/]+)/([^/]+?)(?:\.git)?(?:/.*)?$", r"github.com/\1/\2", url)
    return url


ENTRY = re.compile(r"^- \[([^\]]+)\]\(([^)\s]+)\)\s*(.*)$")
KIND = re.compile(r"!\[(tool|co)\]")


def read_readme(path):
    """Return the readme's `## Tooling` entries: name, url, description, list category, kind."""
    entries, heading, inside = [], None, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Tooling"
            continue
        if not inside:
            continue
        if line.startswith("### "):
            heading = line[4:].strip()
            continue
        m = ENTRY.match(line)
        if not m:
            continue
        kind = KIND.search(line)
        body = m.group(3).strip()
        entries.append(
            {
                "name": m.group(1).strip(),
                "url": m.group(2),
                "description": re.sub(r"!\[[^\]]*\]\([^)]*\)", "", body).strip(" -"),
                "category": heading,
                "kind": kind.group(1) if kind else "",
            }
        )
    return entries


def read_data(path):
    """Return the landscape's items: name, urls, subcategory path.

    Fields sit beside the null `item:` key, so the name is `it['name']`, never `it['item']['name']`.
    """
    items = []
    for category in yaml.safe_load(path.read_text(encoding="utf-8"))["categories"]:
        for sub in category["subcategories"]:
            for it in sub.get("items") or []:
                urls = [it.get(k) for k in ("homepage_url", "repo_url", "blog")]
                urls += [(it.get("extra") or {}).get("documentation_url")]
                items.append(
                    {
                        "name": it.get("name") or "",
                        "urls": [u for u in urls if u],
                        "path": f"{category['name']} / {sub['name']}",
                    }
                )
    return items


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    clone = Path(sys.argv[1])
    theirs = read_readme(clone / "readme.md")
    ours = read_data(Path("data.yml"))

    by_name = {norm(i["name"]): i for i in ours}
    by_url = {}
    for item in ours:
        for url in item["urls"]:
            by_url.setdefault(norm_url(url), item)

    matched, candidates = [], []
    for entry in theirs:
        hit = by_name.get(norm(entry["name"])) or by_url.get(norm_url(entry["url"]))
        (matched if hit else candidates).append((entry, hit))

    used = {id(hit) for _, hit in matched}
    leftovers = [i for i in ours if id(i) not in used]

    print(f"list: {len(theirs)} entries · landscape: {len(ours)} items")
    print(f"matched: {len(matched)} · list-only: {len(candidates)} · landscape-only: {len(leftovers)}\n")

    print("== matched (their name => ours)")
    for entry, hit in matched:
        same = "" if norm(entry["name"]) == norm(hit["name"]) else f"  [renamed: {hit['name']}]"
        print(f"{entry['name']} => {hit['path']}{same}")

    print("\n== list-only (candidates for Steps 5-6)")
    for entry, _ in candidates:
        print(f"{entry['name']}\t{entry['category']}\t{entry['kind']}\t{entry['url']}")

    print("\n== landscape-only, by subcategory")
    for item in sorted(leftovers, key=lambda i: i["path"]):
        print(f"{item['path']}: {item['name']}")

    print("\nUnmatched names on both sides still need an eyeball: the same tool under two names or two URLs.")


if __name__ == "__main__":
    main()
