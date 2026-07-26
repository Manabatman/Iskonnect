"""Tests for profile completeness warnings (hard-filter field counts)."""

from app.matching.profile_completeness import (
    count_hard_filter_fields_populated,
    profile_completeness_payload,
)


def test_empty_profile_low_warning():
    filled, total = count_hard_filter_fields_populated({"email": "a@b.com"})
    assert total == 7
    assert filled == 0
    p = profile_completeness_payload({"email": "a@b.com"})
    assert p["low_data_warning"] is True
    assert p["quality_percent"] == 0
    assert len(p["missing_fields"]) == 10


def test_full_profile_no_warning():
    profile = {
        "age": 18,
        "education_level": "College",
        "region": "NCR",
        "school_type": "Public",
        "household_income_annual": 200_000,
        "gwa_normalized": 90.0,
        "field_of_study_broad": "Engineering",
    }
    filled, total = count_hard_filter_fields_populated(profile)
    assert filled == 7
    assert total == 7
    p = profile_completeness_payload(profile)
    assert p["low_data_warning"] is False


def test_bracket_instead_of_income():
    profile = {
        "age": 18,
        "education_level": "College",
        "region": "NCR",
        "school_type": "Public",
        "income_bracket": "below_250k",
        "gwa_normalized": 90.0,
        "field_of_study_broad": "STEM",
    }
    assert profile_completeness_payload(profile)["low_data_warning"] is False
