"""Scraper source adapters."""

from app.scrapers.adapters.philscholar import PhilScholarAdapter

SOURCE_REGISTRY: dict[str, type] = {
    "philscholar": PhilScholarAdapter,
}

__all__ = ["SOURCE_REGISTRY", "PhilScholarAdapter"]
