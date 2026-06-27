"""Scraper parsing unit tests (no live HTTP)."""

from app.scrapers.adapters.philscholar import PhilScholarAdapter
from app.scrapers.scrape_runner import _validate_entry

adapter = PhilScholarAdapter()

SAMPLE_SITEMAP_HTML = """
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://philscholar.com/ched-merit-scholarship-2026/</loc></url>
  <url><loc>https://philscholar.com/category/news/</loc></url>
</urlset>
"""

SAMPLE_DETAIL_HTML = """
<html><body>
<article class="post">
  <h1 class="entry-title">CHED Merit Scholarship Program 2026</h1>
  <div class="entry-content"><p>Full description of the scholarship program.</p></div>
  <span class="author"><a href="#">CHED</a></span>
</article>
</body></html>
"""

SAMPLE_LANDING_HTML = """
<html><body>
<section><h2>Your Guide to College Scholarships</h2></section>
</body></html>
"""


def test_parse_sitemap_extracts_post_urls():
    locs = adapter.discover_listing_urls(SAMPLE_SITEMAP_HTML)
    assert "https://philscholar.com/ched-merit-scholarship-2026/" in locs


def test_filter_post_urls_excludes_category_pages():
    locs = adapter.discover_listing_urls(SAMPLE_SITEMAP_HTML)
    posts = adapter.filter_post_urls(locs, limit=10)
    assert any("ched-merit" in u for u in posts)
    assert all("/category/" not in u for u in posts)


def test_landing_page_yields_no_scholarship_posts():
    """Regression: /scholarships/ marketing page has no article cards."""
    locs = adapter.discover_listing_urls(SAMPLE_LANDING_HTML)
    posts = adapter.filter_post_urls(locs, limit=10)
    assert posts == []


def test_parse_detail_page_extracts_description_and_provider():
    extra = adapter.parse_detail_page(SAMPLE_DETAIL_HTML, "https://philscholar.com/ched-merit-scholarship-2026/")
    assert "description" in extra
    assert "scholarship program" in extra["description"].lower()
    assert extra.get("provider") == "CHED"
    assert extra.get("title") == "CHED Merit Scholarship Program 2026"


def test_validate_entry_rejects_bad_link():
    assert _validate_entry({"title": "Okay", "link": "ftp://bad"}) is False
    assert _validate_entry({"title": "Okay", "link": "https://example.com/x"}) is True
