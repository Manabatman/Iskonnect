"""Tests for verification export bundle assignment and field coverage."""

from __future__ import annotations

import json
from datetime import date, timedelta

import pytest

from app import models
from app.verification.bundles import assign_verification_bundle
from app.verification.export_schema import (
    VERIFICATION_EXPORT_COLUMNS,
    compute_verification_priority,
    row_to_verification_export,
    verification_record_to_csv_row,
)
from app.verification.report_schema import (
    CHANGE_REASONS,
    CLOSURE_TYPES,
    FIELD_CHANGES_COLUMNS,
)


def _sch(**overrides) -> models.Scholarship:
    base = {
        "title": "Test Scholarship",
        "provider": "Test Provider",
        "link": "https://example.com/test",
        "source": "test",
        "description": "Test description",
        "countries": "Philippines",
        "regions": "",
        "needs_tags": json.dumps([]),
        "level": "College",
        "eligible_levels": json.dumps(["College"]),
        "eligible_regions": json.dumps(["NCR"]),
        "eligible_cities": json.dumps([]),
        "eligible_school_types": json.dumps(["Public"]),
        "eligible_courses_psced": json.dumps([]),
        "eligible_courses_specific": json.dumps([]),
        "residency_required": False,
        "benefit_tuition": True,
        "benefit_books": False,
        "application_deadline": date.today() + timedelta(days=30),
        "data_status": "verified",
        "verification_source": "manual",
        "link_status": "ok",
        "is_active": True,
    }
    base.update(overrides)
    return models.Scholarship(**base)


@pytest.mark.parametrize(
    ("provider", "provider_type", "title", "expected"),
    [
        ("Commission on Higher Education", "government", "CHED Merit", "ched_unifast"),
        ("Department of Science and Technology", "government", "DOST Merit", "dost"),
        ("TESDA", "government", "TESDA Scholarship", "tesda"),
        ("GSIS", "government", "GESP", "gsis_sss"),
        ("Social Security System", "government", "SSS Education", "gsis_sss"),
        ("OWWA", "government", "EDSP", "owwa_dswd_ncip"),
        ("SM Foundation", "private", "College Scholarship", "sm_foundation"),
        ("Megaworld Foundation", "private", "Partner Grant", "megaworld_foundation"),
        ("Aboitiz Foundation", "private", "Future Leaders", "private_foundations"),
        ("City Government of Pasig", "lgu", "Pasig Scholarship", "lgu_ncr"),
        ("City Government of Cebu", "lgu", "Cebu Scholarship", "lgu_provincial"),
        ("University of the Philippines", "institutional", "UP Grant", "universities"),
        ("European Union", "government", "Erasmus+", "international"),
        ("AFPSLAI", "private", "Educational Grant", "military_affiliation"),
    ],
)
def test_assign_verification_bundle_by_provider(provider, provider_type, title, expected):
    row = _sch(provider=provider, provider_type=provider_type, title=title)
    assert assign_verification_bundle(row) == expected


def test_assign_verification_bundle_archived():
    row = _sch(is_active=False, provider="DOST", title="Old Program")
    assert assign_verification_bundle(row) == "archived_reference"


def test_assign_verification_bundle_id_override():
    row = _sch(id=91, provider="UK Government", title="Chevening")
    assert assign_verification_bundle(row) == "international"


def test_assign_verification_bundle_military_before_ched_title():
    row = _sch(
        id=56,
        provider="Armed Forces of the Philippines (AFPEBSO)",
        title="AFPEBSO DND CHED PASUC Scholarship",
        provider_type="government",
    )
    assert assign_verification_bundle(row) == "military_affiliation"


def test_compute_verification_priority_high():
    assert compute_verification_priority({"link_status": "broken", "data_status": "verified"}) == "high"
    assert compute_verification_priority({"link_status": "ok", "data_status": "needs_review"}) == "high"
    assert compute_verification_priority({"link_status": "ok", "data_status": "verified"}) == "normal"


def test_row_to_verification_export_covers_columns():
    row = _sch(
        id=1,
        provider="Commission on Higher Education",
        title="CHED Merit",
        link_status="broken",
        data_status="broken_link",
        members_only=False,
        citizenship_required="Filipino",
    )
    record = row_to_verification_export(row, verification_bundle="ched_unifast")
    for col in VERIFICATION_EXPORT_COLUMNS:
        assert col in record, f"missing export column: {col}"
    assert record["primary_link"] == row.link
    assert record["verification_bundle"] == "ched_unifast"
    assert record["verification_priority"] == "high"
    assert isinstance(record["eligible_levels"], list)


def test_verification_record_to_csv_row_formats_lists_and_bools():
    record = {
        "id": 1,
        "verification_bundle": "dost",
        "verification_priority": "normal",
        "eligible_levels": ["College", "Graduate"],
        "members_only": True,
        "is_active": True,
        "application_deadline": date(2026, 3, 15),
        "last_verified_at": None,
    }
    for col in VERIFICATION_EXPORT_COLUMNS:
        record.setdefault(col, None if col not in ("eligible_levels",) else [])
    csv_row = verification_record_to_csv_row(record)
    assert csv_row["eligible_levels"] == "College|Graduate"
    assert csv_row["members_only"] == "true"
    assert csv_row["application_deadline"] == "2026-03-15"


def test_report_schema_columns_non_empty():
    assert len(FIELD_CHANGES_COLUMNS) >= 10
    assert "source_url" in FIELD_CHANGES_COLUMNS
    assert "change_reason" in FIELD_CHANGES_COLUMNS
    assert len(CHANGE_REASONS) >= 5
    assert len(CLOSURE_TYPES) >= 3
