"""Dry-run script tests (DATA-05 / B8)."""

from __future__ import annotations

from app.scripts.taxonomy_migration_dryrun import analyze_values
from app.taxonomy.psced_fields import taxonomy_value_resolves
from collections import Counter


def test_taxonomy_value_resolves_broad_and_field():
    assert taxonomy_value_resolves("STEM")
    assert taxonomy_value_resolves("Development Communication")
    assert taxonomy_value_resolves("BSDevCom")
    assert not taxonomy_value_resolves("Not A Real Field XYZ")


def test_analyze_values_flags_unresolved():
    counters = {
        "profile_field_of_study_broad": Counter({"STEM": 2, "Mystery": 1}),
        "profile_field_of_study_specific": Counter(),
        "scholarship_eligible_courses_psced": Counter({"Business": 1}),
        "scholarship_eligible_courses_specific": Counter(),
    }
    result = analyze_values(counters)
    assert not result["ok"]
    assert "Mystery" in result["unresolved"]["profile_field_of_study_broad"]


def test_analyze_values_passes_when_all_resolve():
    counters = {
        "profile_field_of_study_broad": Counter({"STEM": 1, "Nursing": 1}),
        "profile_field_of_study_specific": Counter({"BS Nursing": 1}),
        "scholarship_eligible_courses_psced": Counter({"Arts": 1}),
        "scholarship_eligible_courses_specific": Counter({"BS Accountancy": 1}),
    }
    result = analyze_values(counters)
    assert result["ok"]
