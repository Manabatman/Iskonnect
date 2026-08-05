"""Tests for eligibility migration v1 — evaluators, publish rules, personas."""

from __future__ import annotations

from datetime import date

import pytest

from app.config import settings
from app.matching.eligibility_gates import (
    evaluate_academic,
    evaluate_conflict_scopes,
    evaluate_prior_tertiary_units,
    evaluate_required_affiliations,
)
from app.matching.eligibility_result import evaluate_eligibility
from app.utils.publishability_rules import validate_scholarship_publish_rules


@pytest.fixture(autouse=True)
def enable_migration_gates(monkeypatch):
    monkeypatch.setattr(settings, "gate_prior_units", True)
    monkeypatch.setattr(settings, "gate_academic_or", True)
    monkeypatch.setattr(settings, "gate_conflicts", True)
    monkeypatch.setattr(settings, "gate_affiliations", True)
    monkeypatch.setattr(settings, "gate_age_as_of", True)
    monkeypatch.setattr(settings, "gate_work_experience", True)
    monkeypatch.setattr(settings, "gate_residency_years", True)
    monkeypatch.setattr(settings, "gate_entry_path", True)
    monkeypatch.setattr(settings, "gate_parent_salary_grade", True)
    monkeypatch.setattr(settings, "gate_marital_status", True)


def test_prior_units_bars_enrolled_student():
    profile = {"prior_tertiary_units": 30, "enrollment_status": "enrolled"}
    sch = {"max_prior_tertiary_units": 0, "title": "DOST UG"}
    check = evaluate_prior_tertiary_units(profile, sch)
    assert check.result.value == "unmet"


def test_prior_units_allows_incoming_freshman():
    profile = {"prior_tertiary_units": 0, "enrollment_status": "incoming_freshman"}
    sch = {"max_prior_tertiary_units": 0}
    check = evaluate_prior_tertiary_units(profile, sch)
    assert check.result.value == "met"


def test_academic_or_rank_satisfies_bpmsp():
    profile = {"gwa_normalized": 88, "class_rank": 3, "class_size": 120}
    sch = {
        "min_gwa_normalized": 95,
        "max_class_rank": 5,
        "academic_gate_mode": "or",
    }
    check = evaluate_academic(profile, sch)
    assert check.result.value == "met"


def test_academic_and_requires_both():
    profile = {"gwa_normalized": 96, "class_rank": 8, "class_size": 120}
    sch = {
        "min_gwa_normalized": 95,
        "max_class_rank": 5,
        "academic_gate_mode": "and",
    }
    check = evaluate_academic(profile, sch)
    assert check.result.value == "unmet"


def test_conflict_scope_excludes_lgu_grant_holder():
    profile = {"active_grant_scope_codes": ["lgu_grant"]}
    sch = {"conflict_scope_codes": ["lgu_grant"], "title": "QCSP"}
    check = evaluate_conflict_scopes(profile, sch)
    assert check.result.value == "unmet"


def test_ncfrs_required_for_coscho():
    profile = {"affiliation_codes": []}
    sch = {"required_affiliation_codes": ["ncfrs"], "title": "CoScho"}
    check = evaluate_required_affiliations(profile, sch)
    assert check.result.value == "unmet"

    profile_ncfrs = {"affiliation_codes": ["ncfrs"], "is_4ps_listahanan": True}
    check2 = evaluate_required_affiliations(profile_ncfrs, sch)
    assert check2.result.value == "met"


def test_consortium_school_lock():
    profile = {"school": "Ateneo de Manila University", "target_school": "Ateneo de Manila University"}
    sch = {
        "eligible_schools": ["university-of-the-philippines-diliman"],
        "title": "ERDT",
    }
    result = evaluate_eligibility(profile, sch)
    school_checks = [r for r in result.requirements if r.key == "school"]
    assert school_checks and any(r.result.value == "unmet" for r in school_checks)


def test_publishability_or_mode_requires_two_predicates():
    errors = validate_scholarship_publish_rules(
        {"id": 1, "academic_gate_mode": "or", "min_gwa_normalized": 95},
    )
    assert any("two academic predicates" in e for e in errors)


def test_publishability_consortium_requires_schools():
    errors = validate_scholarship_publish_rules(
        {
            "id": 2,
            "title": "ASTHRDP Graduate Consortium",
            "description": "consortium universities",
            "eligible_schools": [],
        },
    )
    assert any("eligible_schools" in e for e in errors)


def test_migration_v1_backfill_manifest_exists():
    from pathlib import Path

    path = Path(__file__).resolve().parents[2] / "verification" / "export" / "migration_v1_backfill_manifest.json"
    assert path.exists()


def test_canonical_rule_class_inventory_frozen():
    from pathlib import Path
    import json

    path = Path(__file__).resolve().parents[2] / "verification" / "export" / "canonical_rule_class_inventory.json"
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert len(data) >= 40
