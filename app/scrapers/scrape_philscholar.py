"""
PhilScholar scraper entry point (delegates to scrape_runner).

Run: python -m app.scrapers.scrape_philscholar
"""

from __future__ import annotations

import logging

from app.scrapers.scrape_runner import run_source

logger = logging.getLogger(__name__)


def run_scrape():
    return run_source("philscholar")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(run_scrape())
