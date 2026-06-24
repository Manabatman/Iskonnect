"""Unified scholarship deduplication key across ingest, staging, and import paths."""

from __future__ import annotations

import hashlib


def scholarship_dedupe_key(
    title: str,
    provider: str | None,
    link: str | None = None,
) -> str:
    """
    Stable dedupe key: sha256(normalized title | provider | link).
    Link is optional for staging-only title+provider checks.
    """
    parts = [
        (title or "").strip().lower(),
        (provider or "").strip().lower(),
        (link or "").strip().lower(),
    ]
    raw = "|".join(parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:64]
