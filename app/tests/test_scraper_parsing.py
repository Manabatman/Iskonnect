"""Scraper parsing unit tests (no live HTTP)."""

from app.scrapers.scrape_philscholar import _parse_detail_page, _parse_listing, _validate_entry


SAMPLE_LISTING_HTML = """
<html><body>
<article>
  <h2><a href="https://philscholar.com/example-scholarship/">Test Scholarship</a></h2>
</article>
</body></html>
"""

SAMPLE_DETAIL_HTML = """
<html><body>
<article class="post">
  <div class="entry-content"><p>Full description of the scholarship program.</p></div>
  <span class="author"><a href="#">CHED</a></span>
</article>
</body></html>
"""


def test_parse_listing_extracts_title_and_link():
    rows = _parse_listing(SAMPLE_LISTING_HTML)
    assert len(rows) == 1
    assert rows[0]["title"] == "Test Scholarship"
    assert rows[0]["link"].startswith("https://")


def test_parse_detail_page_extracts_description_and_provider():
    extra = _parse_detail_page(SAMPLE_DETAIL_HTML)
    assert "description" in extra
    assert "scholarship program" in extra["description"].lower()
    assert extra.get("provider") == "CHED"


def test_validate_entry_rejects_bad_link():
    assert _validate_entry({"title": "Okay", "link": "ftp://bad"}) is False
    assert _validate_entry({"title": "Okay", "link": "https://example.com/x"}) is True
