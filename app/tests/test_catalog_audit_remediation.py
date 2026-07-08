"""Tests for catalog audit remediation: affiliation equity, region search, priority groups."""

from __future__ import annotations

import json

from app.matching.eligibility_result import evaluate_eligibility
from app.matching.hard_filters import filter_scholarships
from app.taxonomy.priority_groups import normalize_priority_groups, resolve_priority_group
from app.taxonomy.regions import canonical_region_label, region_search_literals
from app.utils.application_status import is_recurring_scholarship


def test_resolve_priority_group_aliases():
    assert resolve_priority_group("4Ps") == "4Ps/Listahanan"
    assert resolve_priority_group("Solo Parent Dependents") == "Solo Parent Dependent"
    assert resolve_priority_group("Indigenous Peoples (Lumad)") == "IP"


def test_normalize_priority_groups_deduplicates():
    out = normalize_priority_groups(["4Ps", "Listahanan", "PWD", "PWD"])
    assert out == ["4Ps/Listahanan", "PWD"]


def test_region_search_literals_ncr_includes_metro_manila():
    literals = region_search_literals("NCR")
    assert "NCR" in literals
    assert "Metro Manila" in literals


def test_canonical_region_label_metro_manila_to_ncr():
    assert canonical_region_label("Metro Manila") == "NCR"
    assert canonical_region_label("National Capital Region") == "NCR"


def test_members_only_uniformed_service_excludes_non_member():
    sch = {
        "id": 62,
        "title": "AFPSLAI Educational Grant Program",
        "members_only": True,
        "priority_groups": ["Uniformed Service Dependents"],
        "eligible_levels": ["College"],
        "data_status": "active",
    }
    generic = {
        "education_level": "College",
        "gwa_normalized": 90.0,
        "is_uniformed_service_dependent": False,
    }
    member = {**generic, "is_uniformed_service_dependent": True}
    assert evaluate_eligibility(generic, sch).status.value == "not_eligible"
    assert evaluate_eligibility(member, sch).passes_for_matching is True


def test_members_only_military_dependents_excludes_non_member():
    sch = {
        "id": 56,
        "title": "AFPEBSO Scholarship",
        "members_only": True,
        "priority_groups": ["Military Dependents"],
        "eligible_levels": ["College"],
        "data_status": "active",
    }
    profile = {"education_level": "College", "is_military_dependent": False}
    out, _ = filter_scholarships(profile, [sch])
    assert out == []


def test_is_recurring_scholarship_from_cycle_type():
    assert is_recurring_scholarship({"cycle_type": "annual"}) is True
    assert is_recurring_scholarship({"cycle_type": "rolling"}) is False
    assert is_recurring_scholarship({"cycle_type": None}) is False


def test_import_contract_includes_members_only():
    from app.utils.import_contract import CANONICAL_IMPORT_COLUMNS

    assert "members_only" in CANONICAL_IMPORT_COLUMNS
