"""Tests for Gemini/CSV import coercion on schemas.Scholarship."""

from __future__ import annotations

import json

import pytest

from app import models, schemas
from app.utils.staging_promotion import promote_staging_row, verification_source_for


def test_pipe_delimited_lists_coerced():
    sch = schemas.Scholarship.model_validate(
        {
            "title": "Test Scholarship",
            "eligible_levels": "College|Graduate",
            "eligible_school_types": "Public|Private",
            "eligible_courses_psced": "STEM|Engineering",
            "required_documents": "ITR|TOR|GOOD_MORAL",
            "countries": "Philippines",
        }
    )
    assert sch.eligible_levels == ["College", "Graduate"]
    assert sch.eligible_school_types == ["Public", "Private"]
    assert sch.eligible_courses_psced == ["STEM", "Engineering"]
    assert sch.required_documents == ["ITR", "TOR", "GOOD_MORAL"]
    assert sch.countries == ["Philippines"]


def test_empty_string_scalars_become_none():
    sch = schemas.Scholarship.model_validate(
        {
            "title": "Scalar Test",
            "min_age": "",
            "max_age": "",
            "max_income_threshold": "",
            "min_gwa_normalized": "",
            "benefit_allowance_monthly": "",
            "benefit_total_value": "",
            "application_open_date": "",
            "application_deadline": "",
        }
    )
    assert sch.min_age is None
    assert sch.max_age is None
    assert sch.max_income_threshold is None
    assert sch.min_gwa_normalized is None
    assert sch.benefit_allowance_monthly is None
    assert sch.benefit_total_value is None
    assert sch.application_open_date is None
    assert sch.application_deadline is None


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("Merit", "Merit-based"),
        ("merit", "Merit-based"),
        ("Merit-based", "Merit-based"),
        ("Academic", "Merit-based"),
        ("merit based", "Merit-based"),
        ("Need", "Need"),
        ("", None),
    ],
)
def test_scholarship_type_normalized(raw: str, expected: str | None):
    sch = schemas.Scholarship.model_validate({"title": "Type Test", "scholarship_type": raw})
    assert sch.scholarship_type == expected


def test_research_metadata_columns_ignored():
    sch = schemas.Scholarship.model_validate(
        {
            "title": "Research Meta Test",
            "link": "https://example.com/scholarship",
            "application_status": "open",
            "cycle_type": "annual",
            "last_open_date": "2025-02-01",
            "last_close_date": "2025-04-15",
            "research_notes": "Primary: https://example.com Confidence: high",
            "source_urls": "https://example.com|https://example.org",
        }
    )
    assert sch.title == "Research Meta Test"
    assert not hasattr(sch, "application_status")
    assert not hasattr(sch, "research_notes")


def test_gemini_research_maps_to_csv_import_verification_source():
    assert verification_source_for("gemini_research") == "csv_import"
    assert verification_source_for("discovery_verification") == "csv_import"
    assert verification_source_for("csv_import") == "csv_import"
    assert verification_source_for("philscholar") == "team_verified"


def test_staging_round_trip_csv_row(db_session):
    """Simulate csv_to_staging payload_json -> approve validation."""
    raw_row = {
        "title": "CSV Round Trip Scholarship",
        "provider": "DOST-SEI",
        "source": "gemini_research",
        "link": "https://example.com/csv-round-trip",
        "eligible_levels": "College",
        "eligible_school_types": "Public|Private",
        "scholarship_type": "Merit",
        "min_age": "",
        "max_income_threshold": "400000",
        "is_active": "true",
        "research_notes": "ignored on persist",
    }
    sch = schemas.Scholarship.model_validate(raw_row)
    assert sch.eligible_levels == ["College"]
    assert sch.scholarship_type == "Merit-based"
    assert sch.min_age is None
    assert sch.max_income_threshold == 400000

    st = models.ScholarshipStaging(
        title=sch.title,
        provider=sch.provider,
        source=raw_row["source"],
        payload_json=json.dumps(raw_row),
        status="pending",
        dedupe_key="test-csv-round-trip-key",
    )
    db_session.add(st)
    db_session.commit()

    promoted = promote_staging_row(db_session, st)
    assert promoted is not None
    assert promoted.title == "CSV Round Trip Scholarship"
    assert promoted.verification_source == "csv_import"
    assert json.loads(promoted.eligible_levels) == ["College"]
    db_session.commit()
