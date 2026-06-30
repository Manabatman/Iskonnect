"""Tests for app.utils.import_contract."""

from __future__ import annotations

import pytest

from app.utils.import_contract import (
    CANONICAL_IMPORT_COLUMNS,
    CANONICAL_SCHEMA_COLUMNS,
    KNOWN_METADATA_COLUMNS,
    normalize_header,
    validate_header,
)
from app import schemas


def test_canonical_schema_columns_exist_on_pydantic_model():
    for col in CANONICAL_SCHEMA_COLUMNS:
        assert col in schemas.Scholarship.model_fields, f"missing schema field: {col}"


def test_canonical_import_column_count():
    assert len(CANONICAL_IMPORT_COLUMNS) == len(CANONICAL_SCHEMA_COLUMNS) + len(KNOWN_METADATA_COLUMNS)
    assert len(CANONICAL_IMPORT_COLUMNS) == 39


def test_normalize_header_url_alias():
    assert normalize_header("URL") == "link"
    assert normalize_header(" link ") == "link"
    assert normalize_header("Eligible Levels") == "eligible_levels"


def test_validate_header_accepts_canonical_columns():
    result = validate_header(list(CANONICAL_IMPORT_COLUMNS))
    assert result["unknown"] == []
    assert result["missing_required"] == []
    assert result["duplicate"] == []


def test_validate_header_unknown_column():
    headers = ["title", "provider", "not_a_real_column"]
    result = validate_header(headers)
    assert "not_a_real_column" in result["unknown"]


def test_validate_header_missing_required_title():
    result = validate_header(["provider", "link"])
    assert "title" in result["missing_required"]


def test_validate_header_missing_recommended_warned_not_fatal():
    result = validate_header(["title"])
    assert result["missing_recommended"]
    assert "provider" in result["missing_recommended"]


def test_validate_header_duplicate_normalized_keys():
    result = validate_header(["title", "Title", "provider"])
    assert "title" in result["duplicate"]
