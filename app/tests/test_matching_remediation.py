"""Tests for matching-engine remediation fixes (evidence-based roadmap)."""

import json
from datetime import date, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models
from app.api.v1.matches import _prefilter_scholarships_query
from app.db import Base
from app.matching.hard_filters import filter_scholarships
from app.matching.match_service import MatchService
from app.matching.field_match import psced_code_matches
from app.scoring.engine import WeightedDeterministicScorer
from app.matching.scoring_port import ScoringPayload
from app.scoring.explanation import build_explanation
from app.taxonomy.education_levels import education_levels_compatible, level_search_literals


def _profile(**overrides):
    base = {
        "age": 18,
        "education_level": "Grade 11",
        "region": "NCR",
        "city_municipality": "Quezon City",
        "school_type": "Public",
        "household_income_annual": 200_000,
        "gwa_normalized": 88.0,
        "field_of_study_broad": "Arts",
        "preferred_courses": [],
        "is_pwd": False,
        "is_indigenous_people": False,
        "is_underprivileged": False,
        "is_solo_parent_dependent": False,
        "is_ofw_dependent": False,
        "is_farmer_fisher_dependent": False,
        "is_4ps_listahanan": False,
    }
    base.update(overrides)
    return base


def _sch(**overrides):
    future = (date.today() + timedelta(days=90)).isoformat()
    base = {
        "id": 1,
        "title": "Test Scholarship",
        "eligible_levels": ["Senior High School"],
        "eligible_regions": [],
        "eligible_cities": [],
        "regions": [],
        "residency_required": False,
        "eligible_school_types": [],
        "eligible_courses_psced": [],
        "eligible_courses_specific": [],
        "max_income_threshold": 500_000,
        "min_gwa_normalized": None,
        "priority_groups": [],
        "members_only": False,
        "application_deadline": future,
        "data_status": "active",
    }
    base.update(overrides)
    return base


@pytest.mark.parametrize(
    "profile_level,scholarship_level",
    [
        ("Grade 11", "Senior High School"),
        ("Grade 12", "Senior High"),
        ("High School", "Senior High School"),
        ("Grade 11", "Grade 11"),
        ("College", "College"),
    ],
)
def test_education_level_synonym_matrix(profile_level, scholarship_level):
    assert education_levels_compatible(profile_level, scholarship_level)


def test_senior_high_scholarship_passes_for_grade_11():
    out, _ = filter_scholarships(_profile(education_level="Grade 11"), [_sch()])
    assert len(out) == 1


def test_metro_manila_student_gets_ncr_scholarship_after_sql_prefilter_removed():
    """Region alias: Python filter matches; SQL must not drop NCR-restricted rows."""
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add(
        models.Scholarship(
            title="NCR Grant",
            eligible_regions=json.dumps(["NCR"]),
            eligible_levels=json.dumps(["College"]),
            is_active=True,
            members_only=False,
        )
    )
    db.add(
        models.Scholarship(
            title="Visayas Grant",
            eligible_regions=json.dumps(["Region VI - Western Visayas"]),
            eligible_levels=json.dumps(["College"]),
            is_active=True,
            members_only=False,
        )
    )
    db.commit()

    profile = _profile(education_level="College", region="Metro Manila")
    rows = _prefilter_scholarships_query(db, profile).all()
    titles = {r.title for r in rows}
    assert "NCR Grant" in titles
    assert "Visayas Grant" in titles


def test_level_sql_prefilter_includes_senior_high_synonyms():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add(
        models.Scholarship(
            title="SH Bridge",
            eligible_levels=json.dumps(["Senior High School"]),
            is_active=True,
            members_only=False,
        )
    )
    db.commit()
    profile = _profile(education_level="Grade 11")
    rows = _prefilter_scholarships_query(db, profile).all()
    assert any(r.title == "SH Bridge" for r in rows)
    assert "senior high school" in level_search_literals("Grade 11")


def test_members_only_excludes_non_member():
    sch = _sch(
        title="PWD Exclusive",
        priority_groups=["PWD"],
        members_only=True,
        eligible_levels=["College"],
    )
    non_member = _profile(education_level="College", is_pwd=False)
    member = _profile(education_level="College", is_pwd=True)
    out_nm, _ = filter_scholarships(non_member, [sch])
    out_m, _ = filter_scholarships(member, [sch])
    assert out_nm == []
    assert len(out_m) == 1


def test_preferential_priority_still_shown_to_non_members():
    sch = _sch(
        title="PWD Preferred",
        priority_groups=["PWD"],
        members_only=False,
        eligible_levels=["College"],
    )
    out, _ = filter_scholarships(_profile(education_level="College", is_pwd=False), [sch])
    assert len(out) == 1


def test_engineering_matches_stem_via_hierarchy_not_substring():
    assert not psced_code_matches("architecture", "it")
    assert psced_code_matches("it", "it")
    sch = _sch(eligible_courses_psced=["STEM"], eligible_levels=["College"])
    profile = _profile(education_level="College", field_of_study_broad="Engineering")
    out, _ = filter_scholarships(profile, [sch])
    assert len(out) == 1


def test_medical_broad_matches_nursing_specific_only():
    sch = _sch(
        eligible_courses_specific=["BS Nursing"],
        eligible_courses_psced=[],
        eligible_levels=["College"],
    )
    profile = _profile(
        education_level="College",
        field_of_study_broad="Medical",
        preferred_courses=[],
    )
    out, _ = filter_scholarships(profile, [sch])
    assert len(out) == 1


def test_explanation_never_empty_for_generic_scholarship():
    payload = ScoringPayload(
        gwa_normalized=90.0,
        household_income_annual=200_000,
        income_bracket=None,
        field_match_level="none",
        geographic_match_level="none",
        equity_flags={},
        scholarship_type="Merit-based",
        min_gwa_required=None,
        max_income_threshold=None,
        priority_groups=[],
        has_geographic_restriction=False,
        has_field_restriction=False,
    )
    components = {
        "academic": 0.9,
        "income": 0.5,
        "field_alignment": 0.0,
        "geographic": 0.0,
        "equity_priority": 0.5,
    }
    lines = build_explanation(components, payload)
    assert lines
    assert any("nationwide" in line.lower() or "open" in line.lower() or "meet" in line.lower() for line in lines)


def test_ncr_alias_region_match_in_core_pipeline():
    sch = _sch(
        eligible_regions=["NCR"],
        eligible_levels=["College"],
    )
    profile = _profile(education_level="College", region="Metro Manila")
    svc = MatchService()
    results, _ = svc.get_matches(profile, [sch])
    assert len(results) == 1
