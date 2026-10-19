#!/usr/bin/env python3
"""Assert-based checks for the pass/fail and rewrite decisions in check_links.py.

Run from the repo root:
    uv run --with requests --with pyyaml python \
      .agents/skills/check-links/scripts/test_check_links.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_links as cl  # noqa: E402


def test_classify():
    """(url, status, final, error, challenge) -> bucket."""
    cases = [
        (("https://example.test/a", 200, "https://example.test/a", None, False), "ok"),
        (("https://example.test/a", 200, "https://other.test/b", None, False), "redirect"),
        (("http://example.test", 200, "https://example.test/", None, False), "redirect"),
        (("http://example.test/a", 200, "http://example.test/a", None, False), "suspect"),
        (("https://example.test/a", 404, "https://example.test/a", None, False), "broken"),
        (("https://example.test/a", 410, "https://example.test/a", None, False), "broken"),
        (("https://example.test/a", 403, "https://example.test/a", None, False), "suspect"),
        (("https://example.test/a", 503, "https://example.test/a", None, False), "suspect"),
        (("https://example.test/a", 403, "https://example.test/a", None, True), "challenge"),
        (("https://example.test/a", None, None, "dns", False), "broken"),
        (("https://example.test/a", None, None, "too many redirects", False), "broken"),
        (("https://example.test/a", None, None, "network error", False), "suspect"),
    ]
    for args, expected in cases:
        got = cl.classify(*args)
        assert got == expected, f"{args} -> {got}, expected {expected}"


def test_redirect_ignore_reason():
    """None means the redirect is written, a string means it is ignored."""
    cases = [
        (("https://example.test/a", "https://example.test/a/"), "cosmetic"),
        (("https://example.test/a", "https://www.example.test/a"), "cosmetic"),
        (("https://example.test/en/docs", "https://example.test/docs"), "locale"),
        (("https://example.test/solution", "https://example.test/pt-BR/solution"), "locale"),
        (("https://example.test/a", "http://example.test/a"), "downgrade"),
        (("http://example.test", "https://example.test/"), None),
        (("http://example.test/a", "https://example.test/a"), None),
        (("https://example.test/go/docs", "https://example.test/docs"), None),
        (("https://example.test/old", "https://other.test/new"), None),
    ]
    for args, expected in cases:
        got = cl.redirect_ignore_reason(*args)
        assert got == expected, f"{args} -> {got}, expected {expected}"


def test_rewrite():
    text = "    homepage_url: https://old\n    blog: https://keep\n"
    new, changed = cl.rewrite(text, {"https://old": "https://new"})
    assert changed == 1, changed
    assert "homepage_url: https://new" in new, new
    assert "blog: https://keep" in new, new


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
    print("all checks passed")
