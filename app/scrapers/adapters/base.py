"""Base adapter interface for scholarship scrapers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseScraperAdapter(ABC):
    """Each source implements listing discovery and optional detail enrichment."""

    source: str = "unknown"
    listing_url: str = ""

    @abstractmethod
    def discover_listing_urls(self, html: str) -> list[str]:
        """Return scholarship post URLs from a listing/sitemap page."""

    @abstractmethod
    def parse_detail_page(self, html: str, url: str) -> dict[str, Any]:
        """Extract fields from a detail page."""

    def row_from_url(self, url: str, title_hint: str | None = None) -> dict[str, Any]:
        slug = url.rstrip("/").split("/")[-1].replace("-", " ").title()
        return {
            "title": title_hint or slug,
            "link": url,
            "provider": None,
            "description": None,
            "source": self.source,
        }

    def is_scholarship_url(self, url: str) -> bool:
        return True
