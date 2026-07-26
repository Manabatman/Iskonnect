"""Tests for Phase 2 catalog growth tooling scripts."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from app import models
from app.scripts.discovery_to_csv import convert_discovery_json, discovery_row_to_csv
from app.scripts.fix_broken_links import _extract_csv_fixes, _rewrite_link
from app.scripts.gemini_triage import (
    build_catalog_index,
    strip_unsupported_2026_dates,
    triage_row,
)
from app.scripts.resolve_duplicate_scholarships import (
    _build_duplicate_updates,
    _load_duplicate_candidates,
    resolve_duplicates,
)
from app.utils.dedupe import scholarship_dedupe_key
from app.utils.import_contract import CANONICAL_IMPORT_COLUMNS


FIXTURES = Path(__file__).resolve().parents[2] / "verification"


def test_build_duplicate_updates_maps_generic_parents():
    candidates = _load_duplicate_candidates(FIXTURES / "discovery" / "duplicate_candidates.json")
    updates = _build_duplicate_updates(candidates)
    assert 11 in updates
    assert updates[11]["fields"]["title"] == "Ayala Foundation U-Go Scholar Grant"
    assert updates[13]["fields"]["title"] == "Metrobank Foundation ACCESS Program"
    assert 54 not in updates
    assert 3 not in updates


def test_discovery_row_to_csv_has_40_columns():
    entry = {
        "title": "Test Scholarship",
        "provider": "Test Provider",
        "provider_type": "Government",
        "scholarship_type": "Need",
        "primary_link": "https://example.gov.ph/program",
        "description": "Desc",
        "eligible_levels": ["College"],
        "eligible_regions": [],
        "priority_groups": ["4Ps"],
        "members_only": False,
        "benefit_summary": "PHP 10,000 stipend",
        "benefits": "PHP 10,000/AY stipend",
        "required_documents": ["ITR"],
        "has_return_service": True,
        "application_status": "open",
        "verification_confidence": "verified",
        "discovery_classification": "add_immediately",
        "research_candidate_id": "test_slug",
        "source_urls": ["https://example.gov.ph/program"],
        "evidence_snippet": "Evidence",
    }
    row = discovery_row_to_csv(entry)
    assert list(row.keys()) == list(CANONICAL_IMPORT_COLUMNS)
    assert row["title"] == "Test Scholarship"
    assert row["link"] == "https://example.gov.ph/program"
    assert row["is_active"] == "true"


def test_convert_discovery_json_skips_partial_by_default(tmp_path):
    payload = [
        {"title": "Verified One", "verification_confidence": "verified", "provider": "A", "provider_type": "Government", "scholarship_type": "Need", "primary_link": "https://a", "description": "d", "eligible_levels": ["College"], "benefit_summary": "b", "source_urls": ["https://a"], "evidence_snippet": "e", "discovery_classification": "add_immediately"},
        {"title": "Partial One", "verification_confidence": "partially_verified", "provider": "B", "provider_type": "Government", "scholarship_type": "Need", "primary_link": "https://b", "description": "d", "eligible_levels": ["College"], "benefit_summary": "b", "source_urls": ["https://b"], "evidence_snippet": "e", "discovery_classification": "add_immediately"},
    ]
    src = tmp_path / "validated.json"
    src.write_text(json.dumps(payload), encoding="utf-8")
    rows, stats = convert_discovery_json(src, include_partial=False)
    assert stats["exported"] == 1
    assert stats["skipped_partial"] == 1
    assert rows[0]["title"] == "Verified One"


def test_strip_unsupported_2026_dates():
    row = {
        "application_open_date": "2026-07-01",
        "application_deadline": "2026-08-15",
        "research_notes": "application_status=opening_soon | confidence=high",
    }
    cleaned = strip_unsupported_2026_dates(row)
    assert cleaned["application_open_date"] == ""
    assert cleaned["application_deadline"] == ""

    open_row = {
        "application_open_date": "2026-07-01",
        "research_notes": "application_status=open | confidence=high",
    }
    kept = strip_unsupported_2026_dates(open_row)
    assert kept["application_open_date"] == "2026-07-01"


def test_rewrite_link_common_patterns():
    assert _rewrite_link("https://ugs.science-scholarships.ph") == "https://ugrad.science-scholarships.ph"
    assert _rewrite_link("https://science-scholarships.ph/grad") == "https://www.science-scholarships.ph/grad"


def test_extract_csv_fixes_filters_link_fields():
    fixes = _extract_csv_fixes([FIXTURES / "reports" / "dost" / "field_changes.csv"])
    fields = {f"{row['id']}:{row['field']}" for row in fixes}
    assert "2:primary_link" in fields
    assert "2:link_status" in fields
    assert all(row["field"] in {"primary_link", "link", "link_status", "data_status"} for row in fixes)


def test_triage_row_new_vs_skip(db_session):
    existing = models.Scholarship(
        title="Exact Match",
        provider="Provider A",
        link="https://example.com/a",
        dedupe_key=scholarship_dedupe_key("Exact Match", "Provider A", "https://example.com/a"),
    )
    db_session.add(existing)
    db_session.commit()

    catalog = build_catalog_index(db_session)
    action, matched_id, _ = triage_row(
        {
            "title": "Exact Match",
            "provider": "Provider A",
            "link": "https://example.com/a",
        },
        catalog,
    )
    assert action == "skip"
    assert matched_id == str(existing.id)

    action2, _, _ = triage_row(
        {
            "title": "Brand New Program",
            "provider": "Provider B",
            "link": "https://example.com/new",
        },
        catalog,
    )
    assert action2 == "new"


def test_resolve_duplicates_dry_run(db_session, tmp_path):
    candidates_path = FIXTURES / "discovery" / "duplicate_candidates.json"
    dost_csv = FIXTURES / "reports" / "dost" / "field_changes.csv"

    s11 = models.Scholarship(
        id=11,
        title="Ayala Foundation Scholarship Program",
        provider="Ayala Foundation",
        link="https://old.example.com",
    )
    s54 = models.Scholarship(
        id=54,
        title="DOH Medical Scholarship and Return Service Program",
        provider="Department of Health",
        link="https://doh.example.com",
        is_active=False,
        editorial_state="archived",
    )
    s3 = models.Scholarship(
        id=3,
        title="DOST-SEI Graduate Scholarship",
        provider="DOST-SEI",
        description="Old umbrella description",
    )
    db_session.add_all([s11, s54, s3])
    db_session.commit()

    summary = resolve_duplicates(
        db_session,
        duplicate_json=candidates_path,
        dost_csv=dost_csv,
        dry_run=True,
    )
    db_session.refresh(s11)
    db_session.refresh(s54)
    db_session.refresh(s3)

    assert summary.applied > 0
    assert s11.title == "Ayala Foundation Scholarship Program"
    assert s54.is_active is False
    assert s3.editorial_state != "needs_review"

    applied_fields = {o.field for o in summary.outcomes if o.result == "dry_run"}
    assert "title" in applied_fields


def test_discovery_to_csv_real_file():
    src = FIXTURES / "discovery" / "validated_new_scholarships.json"
    if not src.exists():
        pytest.skip("validated_new_scholarships.json missing")
    rows, stats = convert_discovery_json(src, include_partial=False)
    assert stats["exported"] == 8
    assert len(rows[0]) == len(CANONICAL_IMPORT_COLUMNS)
