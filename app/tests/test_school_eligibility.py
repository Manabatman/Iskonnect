"""Tests for school eligibility evaluators and registry."""

from app.matching.eligibility_result import QualificationStatus, RequirementResult, evaluate_eligibility
from app.taxonomy.school_registry import resolve_school_id
from app.taxonomy.schools import PHILIPPINE_SCHOOLS, SCHOOL_REGISTRY


def test_philippine_schools_backward_compat():
    assert isinstance(PHILIPPINE_SCHOOLS, list)
    assert len(PHILIPPINE_SCHOOLS) >= 50
    assert "Polytechnic University of the Philippines" in PHILIPPINE_SCHOOLS


def test_resolve_school_id_aliases():
    assert resolve_school_id("PUP") == "polytechnic-university-of-the-philippines"
    assert resolve_school_id("University of Santo Tomas") == "university-of-santo-tomas"
    assert resolve_school_id("DLSU") == "de-la-salle-university"
    assert resolve_school_id("UP Diliman") == "university-of-the-philippines-diliman"


def test_evaluate_school_met_by_school_id():
    profile = {"school_id": "polytechnic-university-of-the-philippines", "school": "PUP"}
    sch = {"id": 1, "eligible_schools": ["polytechnic-university-of-the-philippines"]}
    result = evaluate_eligibility(profile, sch)
    school_req = next(r for r in result.requirements if r.key == "school")
    assert school_req.result == RequirementResult.MET
    assert result.passes_for_matching


def test_evaluate_school_unmet_wrong_hei():
    profile = {"school_id": "de-la-salle-university", "school": "DLSU"}
    sch = {"id": 2, "eligible_schools": ["polytechnic-university-of-the-philippines"]}
    result = evaluate_eligibility(profile, sch)
    assert result.status == QualificationStatus.NOT_ELIGIBLE


def test_evaluate_school_system_up_campus():
    profile = {"school_id": "university-of-the-philippines-los-banos"}
    sch = {"id": 3, "eligible_school_systems": ["up-system"]}
    result = evaluate_eligibility(profile, sch)
    school_req = next(r for r in result.requirements if r.key == "school")
    assert school_req.result == RequirementResult.MET


def test_evaluate_school_category_suc():
    profile = {"school_id": "polytechnic-university-of-the-philippines"}
    sch = {"id": 4, "eligible_school_categories": ["SUC"]}
    result = evaluate_eligibility(profile, sch)
    cat_req = next(r for r in result.requirements if r.key == "school_category")
    assert cat_req.result == RequirementResult.MET


def test_evaluate_school_unknown_when_missing_profile_school():
    profile = {}
    sch = {"id": 5, "eligible_schools": ["university-of-santo-tomas"]}
    result = evaluate_eligibility(profile, sch)
    school_req = next(r for r in result.requirements if r.key == "school")
    assert school_req.result == RequirementResult.UNKNOWN
    assert result.status == QualificationStatus.PROVISIONALLY_QUALIFIED


def test_registry_has_major_heis():
    for sid in (
        "polytechnic-university-of-the-philippines",
        "university-of-santo-tomas",
        "ateneo-de-manila-university",
        "de-la-salle-university",
        "university-of-the-philippines-diliman",
    ):
        assert sid in SCHOOL_REGISTRY
