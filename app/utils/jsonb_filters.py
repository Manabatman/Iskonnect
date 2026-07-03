"""JSON list containment helpers for scholarship eligibility filters."""

from __future__ import annotations

from sqlalchemy import Text, cast, func, or_

from app import models


def json_list_contains(column, value: str):
    """
    Match a value inside a JSON list column stored as text (SQLite) or jsonb (Postgres).
    Casts to text so ILIKE works on both dialects.
    """
    val = value.strip()
    pattern = f'%"{val}"%'
    return cast(column, Text).ilike(pattern)


def json_list_pattern(column, pattern: str):
    """Substring match anywhere in the JSON list column (text or jsonb)."""
    return cast(column, Text).ilike(pattern)


def json_list_empty(column):
    """True when column is NULL, blank, or JSON empty list []."""
    text_col = cast(column, Text)
    trimmed = func.trim(func.coalesce(text_col, ""))
    return or_(
        column.is_(None),
        trimmed == "",
        trimmed == "[]",
    )


def education_level_filter(query, education_level: str):
    val = education_level.strip()
    return query.filter(
        or_(
            json_list_empty(models.Scholarship.eligible_levels),
            json_list_contains(models.Scholarship.eligible_levels, val),
        )
    )
