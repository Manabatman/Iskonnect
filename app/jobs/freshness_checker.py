"""
Mark scholarships expired by deadline; flag stale verification (>30 days) as needs_review.

Delegates to run_catalog_maintenance() for a single source of truth.

Run: python -m app.jobs.freshness_checker
"""

from __future__ import annotations

import logging

from app.jobs.catalog_maintenance import run_catalog_maintenance

logger = logging.getLogger(__name__)


def run_freshness_check() -> tuple[int, int]:
    """
    Returns (expired_count, needs_review_count) for backwards compatibility.
    """
    out = run_catalog_maintenance()
    return out.get("expired", 0), out.get("needs_review", 0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    e, r = run_freshness_check()
    print(f"expired={e} needs_review={r}")
