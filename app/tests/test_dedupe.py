"""Unified dedupe key tests."""

from app.utils.dedupe import scholarship_dedupe_key


def test_dedupe_key_includes_link():
    k1 = scholarship_dedupe_key("Title", "Provider", "https://a.com")
    k2 = scholarship_dedupe_key("Title", "Provider", "https://b.com")
    assert k1 != k2


def test_dedupe_key_stable():
    k1 = scholarship_dedupe_key(" Title ", " Provider ", "https://x.com")
    k2 = scholarship_dedupe_key("title", "provider", "https://x.com")
    assert k1 == k2
