"""Regression tests for hard filters and scholarship serialization used in matching."""

import json

import pytest

from app.matching.hard_filters import filter_scholarships, _region_matches
from app import models
from app.api.v1.scholarships import _scholarship_to_dict


def _profile(**overrides):
    p = {
        "age": 20,
        "education_level": "College",
        "region": "National Capital Region",
        "city_municipality": None,
        "school_type": "Public",
        "household_income_annual": 200_000,
        "income_bracket": None,
        "gwa_normalized": 90.0,
        "field_of_study_broad": "STEM",
        "preferred_courses": [],
    }
    p.update(overrides)
    return p


def _sch_base(**overrides):
    s = {
        "id": 1,
        "min_age": None,
        "max_age": None,
        "eligible_levels": ["College"],
        "level": "College",
        "eligible_regions": ["Region VI - Western Visayas"],
        "eligible_cities": [],
        "regions": [],
        "residency_required": False,
        "eligible_school_types": ["Public", "Private"],
        "eligible_courses_psced": ["STEM"],
        "eligible_courses_specific": [],
        "max_income_threshold": None,
        "min_gwa_normalized": None,
        "needs_tags": [],
        "data_status": None,
    }
    s.update(overrides)
    return s


def test_region_filter_excludes_mismatch():
    profile = _profile(region="National Capital Region")
    sch = _sch_base()
    out = filter_scholarships(profile, [sch])
    assert out == []


def test_nationwide_scholarship_passes():
    profile = _profile(region="National Capital Region")
    sch = _sch_base(eligible_regions=[], regions=[])
    out = filter_scholarships(profile, [sch])
    assert len(out) == 1


def test_residency_required_blocks_without_location():
    assert not _region_matches(
        None,
        None,
        ["Region VI - Western Visayas"],
        [],
        True,
        [],
        scholarship_id=99,
    )


def test_residency_required_allows_with_region():
    assert _region_matches(
        "Region VI - Western Visayas",
        None,
        ["Region VI - Western Visayas"],
        [],
        True,
        [],
        scholarship_id=100,
    )


@pytest.mark.parametrize(
    "specific",
    [
        ["BS Computer Science"],
    ],
)
def test_scholarship_dict_includes_matching_fields(db_session, specific):
    """eligible_courses_specific and related columns must appear in dicts used by MatchService."""
    sch = models.Scholarship(
        title="Test",
        provider="Prov",
        countries="Philippines",
        regions="",
        needs_tags=json.dumps([]),
        level="College",
        link="https://example.com/s",
        description="D",
        eligible_levels=json.dumps(["College"]),
        eligible_regions=json.dumps([]),
        eligible_cities=json.dumps([]),
        residency_required=False,
        eligible_school_types=json.dumps(["Public"]),
        eligible_courses_psced=json.dumps(["STEM"]),
        eligible_courses_specific=json.dumps(specific),
        preferred_extracurriculars=json.dumps(["Debate"]),
        preferred_awards=json.dumps(["Science Fair"]),
        max_income_threshold=None,
        min_gwa_normalized=80.0,
        priority_groups=json.dumps([]),
        required_documents=json.dumps([]),
        is_active=True,
    )
    db_session.add(sch)
    db_session.commit()
    db_session.refresh(sch)

    d = _scholarship_to_dict(sch)
    assert d.get("eligible_courses_specific") == specific
    assert d.get("preferred_extracurriculars") == ["Debate"]
    assert d.get("preferred_awards") == ["Science Fair"]
