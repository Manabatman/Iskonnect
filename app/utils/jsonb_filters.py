"""JSONB containment helpers for scholarship eligibility filters (PostgreSQL)."""

from __future__ import annotations

from sqlalchemy import cast, or_
from sqlalchemy.dialects.postgresql import JSONB

from app import models
from app.config import settings


def _db_is_postgres() -> bool:
    return not settings.database_url.strip().lower().startswith("sqlite")


def json_list_contains(column, value: str):
    """
    Match a value inside a JSON list column.
    Uses @> on PostgreSQL jsonb; falls back to ILIKE on SQLite/text.
    """
    val = value.strip()
    if _db_is_postgres():
        return cast(column, JSONB).contains([val])
    pattern = f'%"{val}"%'
    return column.ilike(pattern)


def education_level_filter(query, education_level: str):
    val = education_level.strip()
    return query.filter(
        or_(
            models.Scholarship.eligible_levels.is_(None),
            models.Scholarship.eligible_levels == "",
            models.Scholarship.eligible_levels == "[]",
            json_list_contains(models.Scholarship.eligible_levels, val),
        )
    )
