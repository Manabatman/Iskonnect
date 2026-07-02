"""JSON list containment helpers for scholarship eligibility filters."""

from __future__ import annotations

from sqlalchemy import or_

from app import models

def json_list_contains(column, value: str):
    """
    Match a value inside a JSON list column stored as text/jsonb.
    Uses ILIKE for cross-dialect portability (SQLite tests + Postgres text/jsonb).
    """
    val = value.strip()
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
