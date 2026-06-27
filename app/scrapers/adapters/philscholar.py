"""
PhilScholar adapter — discovers posts via WordPress sitemap (not the marketing /scholarships/ page).

The /scholarships/ URL is a static landing page; scholarship articles live as blog posts.
"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from app.scrapers.adapters.base import BaseScraperAdapter

SITEMAP_INDEX_URL = "https://philscholar.com/sitemap_index.xml"
LISTING_URL = SITEMAP_INDEX_URL

# Slug keywords suggesting scholarship/program content
_SCHOLARSHIP_SLUG_KEYWORDS = (
    "scholarship",
    "scholar",
    "grant",
    "program",
    "fellowship",
    "stipend",
    "ched",
    "dost",
    "tesda",
    "upcat",
    "merit",
    "financial-aid",
)

_SKIP_PATH_PREFIXES = (
    "/category/",
    "/tag/",
    "/author/",
    "/page/",
    "/wp-",
    "/feed",
    "/sitemap",
    "/courses",
    "/contact",
    "/about",
    "/privacy",
)


class PhilScholarAdapter(BaseScraperAdapter):
    source = "philscholar"
    listing_url = LISTING_URL

    def is_scholarship_url(self, url: str) -> bool:
        parsed = urlparse(url)
        if parsed.netloc and "philscholar.com" not in parsed.netloc:
            return False
        path = (parsed.path or "").lower()
        if not path or path == "/":
            return False
        for prefix in _SKIP_PATH_PREFIXES:
            if prefix in path:
                return False
        slug = path.strip("/").split("/")[-1]
        slug_lower = slug.lower()
        return any(kw in slug_lower for kw in _SCHOLARSHIP_SLUG_KEYWORDS)

    def discover_listing_urls(self, html: str) -> list[str]:
        """Parse sitemap XML and return candidate post URLs."""
        return self._parse_sitemap_locs(html)

    @staticmethod
    def _parse_sitemap_locs(xml: str) -> list[str]:
        soup = BeautifulSoup(xml, "lxml-xml")
        if not soup.find("loc"):
            soup = BeautifulSoup(xml, "lxml")
        locs: list[str] = []
        for loc in soup.find_all("loc"):
            text = loc.get_text(strip=True)
            if text.startswith("http"):
                locs.append(text)
        return locs

    def filter_post_urls(self, urls: list[str], *, limit: int = 50) -> list[str]:
        seen: set[str] = set()
        out: list[str] = []
        for url in urls:
            if url in seen:
                continue
            if not self.is_scholarship_url(url):
                continue
            seen.add(url)
            out.append(url)
            if len(out) >= limit:
                break
        return out

    def title_from_url(self, url: str) -> str:
        slug = url.rstrip("/").split("/")[-1]
        title = re.sub(r"[-_]+", " ", slug).strip()
        return title.title() if title else "Scholarship"

    def parse_detail_page(self, html: str, url: str) -> dict[str, Any]:
        soup = BeautifulSoup(html, "lxml")
        out: dict[str, Any] = {}

        title_el = soup.select_one("h1.entry-title, h1, .entry-title")
        if title_el:
            title = title_el.get_text(strip=True)
            if title:
                out["title"] = title

        content = soup.select_one(".entry-content, article .post-content, .post-content, article")
        if content:
            text = content.get_text(" ", strip=True)
            if text:
                out["description"] = text[:8000]

        provider_el = soup.select_one(".author a, .posted-by a, .provider, meta[property='og:site_name']")
        if provider_el:
            if provider_el.name == "meta":
                out["provider"] = (provider_el.get("content") or "").strip() or None
            else:
                out["provider"] = provider_el.get_text(strip=True) or None

        og_image = soup.select_one("meta[property='og:image']")
        if og_image and og_image.get("content"):
            out["og_image"] = og_image["content"]

        if "title" not in out:
            out["title"] = self.title_from_url(url)
        out["link"] = url
        out["source"] = self.source
        return out
