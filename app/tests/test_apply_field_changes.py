"""Tests for app.scripts.apply_field_changes."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from app import models
from app.scripts.apply_field_changes import (
    apply_field_changes,
    load_field_changes_csv,
    map_application_status,
    normalize_for_compare,
)
from app.utils.field_evidence import list_public_field_evidence


def _sch(**kwargs) -> models.Scholarship:
    defaults = {
        "title": "Test Scholarship",
        "provider": "Test",
        "is_active": True,
    }
    defaults.update(kwargs)
    return models.Scholarship(**defaults)


def test_map_closed_for_this_cycle_to_expected_reopen():
    assert map_application_status("closed_for_this_cycle") == "expected_reopen"
    assert map_application_status("open") == "open"


def test_blocks_dost_id2_2024_carry_forward(db_session):
    s = _sch(
        id=2,
        application_open_date=date(2026, 2, 1),
        application_deadline=date(2026, 4, 15),
    )
    db_session.add(s)
    db_session.commit()

    rows = [
        {
            "id": "2",
            "field": "application_open_date",
            "iskconnect_value": "2026-02-01",
            "official_value": "2024-10-13",
            "action": "update",
            "change_reason": "annual_cycle_update",
            "closure_type": "closed_for_this_cycle",
            "confidence": "verified",
            "source_url": "https://example.com",
            "evidence_snippet": "blocked",
            "official_last_updated": "",
            "announcement_date": "",
            "verified_at": "2026-07-09",
        }
    ]
    summary = apply_field_changes(db_session, rows, dry_run=False)
    db_session.refresh(s)
    assert summary.skipped_blocked == 1
    assert s.application_open_date == date(2026, 2, 1)


def test_drift_guard_skips_when_db_differs(db_session):
    s = _sch(id=5, link="https://old.example.com")
    db_session.add(s)
    db_session.commit()

    rows = [
        {
            "id": "5",
            "field": "primary_link",
            "iskconnect_value": "https://expected.example.com",
            "official_value": "https://new.example.com",
            "action": "update",
            "change_reason": "website_redesign",
            "closure_type": "",
            "confidence": "verified",
            "source_url": "https://example.com",
            "evidence_snippet": "",
            "official_last_updated": "",
            "announcement_date": "",
            "verified_at": "2026-07-09",
        }
    ]
    summary = apply_field_changes(db_session, rows, dry_run=True)
    assert summary.skipped_drift == 1
    assert summary.applied == 0


def test_apply_update_with_evidence_and_version(db_session):
    s = _sch(
        id=10,
        link="https://old.example.com",
        application_status="open",
    )
    db_session.add(s)
    db_session.commit()

    rows = [
        {
            "id": "10",
            "field": "primary_link",
            "iskconnect_value": "https://old.example.com",
            "official_value": "https://new.example.com",
            "action": "update",
            "change_reason": "website_redesign",
            "closure_type": "",
            "confidence": "verified",
            "source_url": "https://official.example.com",
            "evidence_snippet": "Portal migrated",
            "official_last_updated": "",
            "announcement_date": "",
            "verified_at": "2026-07-09",
        },
        {
            "id": "10",
            "field": "application_status",
            "iskconnect_value": "open",
            "official_value": "expected_reopen",
            "action": "update",
            "change_reason": "annual_cycle_update",
            "closure_type": "closed_for_this_cycle",
            "confidence": "partially_verified",
            "source_url": "https://official.example.com",
            "evidence_snippet": "Cycle closed",
            "official_last_updated": "",
            "announcement_date": "",
            "verified_at": "2026-07-09",
        },
    ]
    summary = apply_field_changes(db_session, rows, dry_run=False)
    db_session.refresh(s)

    assert summary.applied == 2
    assert s.link == "https://new.example.com"
    assert s.application_status == "expected_reopen"

    evidence = list_public_field_evidence(db_session, s.id)
    assert len(evidence) == 2
    field_keys = {e["field_key"] for e in evidence}
    assert field_keys == {"link", "application_status"}

    versions = (
        db_session.query(models.ScholarshipVersion)
        .filter(models.ScholarshipVersion.scholarship_id == s.id)
        .all()
    )
    assert len(versions) == 1
    assert "link" in versions[0].changes


def test_idempotent_rerun_applies_nothing(db_session):
    s = _sch(id=11, link="https://stable.example.com")
    db_session.add(s)
    db_session.commit()

    row = {
        "id": "11",
        "field": "primary_link",
        "iskconnect_value": "https://stable.example.com",
        "official_value": "https://updated.example.com",
        "action": "update",
        "change_reason": "website_redesign",
        "closure_type": "",
        "confidence": "verified",
        "source_url": "https://official.example.com",
        "evidence_snippet": "",
        "official_last_updated": "",
        "announcement_date": "",
        "verified_at": "2026-07-09",
    }
    first = apply_field_changes(db_session, [row], dry_run=False)
    assert first.applied == 1

    second = apply_field_changes(db_session, [row], dry_run=False)
    assert second.applied == 0
    assert second.skipped_drift == 1


def test_flag_review_does_not_overwrite_field(db_session):
    s = _sch(id=12, min_gwa_normalized=92.0, editorial_state="verified")
    db_session.add(s)
    db_session.commit()

    rows = [
        {
            "id": "12",
            "field": "min_gwa_normalized",
            "iskconnect_value": "92",
            "official_value": "",
            "action": "flag_review",
            "change_reason": "unknown",
            "closure_type": "",
            "confidence": "cannot_verify",
            "source_url": "https://example.com",
            "evidence_snippet": "No cutoff published",
            "official_last_updated": "",
            "announcement_date": "",
            "verified_at": "2026-07-09",
        }
    ]
    summary = apply_field_changes(db_session, rows, dry_run=False)
    db_session.refresh(s)

    assert summary.flag_review == 1
    assert s.editorial_state == "needs_review"
    assert s.min_gwa_normalized == 92.0


def test_archive_sets_inactive_and_discontinued(db_session):
    s = _sch(id=19, is_active=True, editorial_state="verified", application_status="previous_cycle")
    db_session.add(s)
    db_session.commit()

    rows = [
        {
            "id": "19",
            "field": "is_active",
            "iskconnect_value": "true",
            "official_value": "false",
            "action": "archive",
            "change_reason": "program_discontinued",
            "closure_type": "permanently_discontinued",
            "confidence": "verified",
            "source_url": "https://example.com",
            "evidence_snippet": "Program ended",
            "official_last_updated": "",
            "announcement_date": "",
            "verified_at": "2026-07-09",
        }
    ]
    summary = apply_field_changes(db_session, rows, dry_run=False)
    db_session.refresh(s)

    assert summary.archived == 1
    assert s.is_active is False
    assert s.editorial_state == "archived"
    assert s.application_status == "permanently_discontinued"


def test_skips_cannot_verify_official_value_and_low_confidence(db_session):
    s = _sch(id=20, application_open_date=date(2026, 3, 1))
    db_session.add(s)
    db_session.commit()

    rows = [
        {
            "id": "20",
            "field": "application_open_date",
            "iskconnect_value": "2026-03-01",
            "official_value": "cannot_verify",
            "action": "update",
            "change_reason": "annual_cycle_update",
            "closure_type": "",
            "confidence": "verified",
            "source_url": "",
            "evidence_snippet": "",
            "official_last_updated": "",
            "announcement_date": "",
            "verified_at": "",
        },
        {
            "id": "20",
            "field": "application_deadline",
            "iskconnect_value": "2026-06-30",
            "official_value": "",
            "action": "update",
            "change_reason": "annual_cycle_update",
            "closure_type": "",
            "confidence": "cannot_verify",
            "source_url": "",
            "evidence_snippet": "",
            "official_last_updated": "",
            "announcement_date": "",
            "verified_at": "",
        },
    ]
    summary = apply_field_changes(db_session, rows, dry_run=True)
    assert summary.skipped_cannot_verify_value == 1
    assert summary.skipped_low_confidence == 1


def test_confirm_unchanged_skipped(db_session):
    s = _sch(id=21)
    db_session.add(s)
    db_session.commit()

    rows = [
        {
            "id": "21",
            "field": "title",
            "iskconnect_value": "Test Scholarship",
            "official_value": "Test Scholarship",
            "action": "confirm_unchanged",
            "change_reason": "",
            "closure_type": "",
            "confidence": "verified",
            "source_url": "",
            "evidence_snippet": "",
            "official_last_updated": "",
            "announcement_date": "",
            "verified_at": "",
        }
    ]
    summary = apply_field_changes(db_session, rows, dry_run=True)
    assert summary.skipped_confirm_unchanged == 1


def test_application_cycle_reverification_csv_loads():
    path = (
        Path(__file__).resolve().parents[2]
        / "verification"
        / "reports"
        / "application_cycle_reverification.csv"
    )
    rows = load_field_changes_csv(path)
    ids = {int(r["id"]) for r in rows}
    assert ids == {1, 2, 3, 5, 6, 19, 76, 79}
    assert any(
        r["field"] == "deadline_precision" and r["official_value"] == "institution_dependent"
        for r in rows
    )


def test_clear_date_on_verified_update(db_session):
    s = _sch(id=22, application_open_date=date(2026, 3, 1))
    db_session.add(s)
    db_session.commit()

    rows = [
        {
            "id": "22",
            "field": "application_open_date",
            "iskconnect_value": "2026-03-01",
            "official_value": "",
            "action": "update",
            "change_reason": "annual_cycle_update",
            "closure_type": "",
            "confidence": "verified",
            "source_url": "https://example.com",
            "evidence_snippet": "Clear placeholder",
            "official_last_updated": "",
            "announcement_date": "",
            "verified_at": "2026-07-09",
        }
    ]
    summary = apply_field_changes(db_session, rows, dry_run=False)
    db_session.refresh(s)
    assert summary.applied == 1
    assert s.application_open_date is None


def test_normalize_date_compare():
    assert normalize_for_compare("application_open_date", date(2026, 3, 1)) == "2026-03-01"
    assert normalize_for_compare("application_open_date", "2026-03-01") == "2026-03-01"
