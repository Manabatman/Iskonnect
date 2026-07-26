"""Tests for enrollment timing eligibility evaluators."""

from app.matching.eligibility_result import QualificationStatus, RequirementResult, evaluate_eligibility


def test_year_level_met_current():
    profile = {"current_year_level": 2, "education_level": "College"}
    sch = {"id": 1, "eligible_year_levels": [2, 3]}
    result = evaluate_eligibility(profile, sch)
    yl = next(r for r in result.requirements if r.key == "year_level")
    assert yl.result == RequirementResult.MET


def test_year_level_unmet():
    profile = {"current_year_level": 4, "education_level": "College"}
    sch = {"id": 2, "eligible_year_levels": [1, 2]}
    result = evaluate_eligibility(profile, sch)
    assert result.status == QualificationStatus.NOT_ELIGIBLE


def test_year_level_unknown_when_missing():
    profile = {"education_level": "College"}
    sch = {"id": 3, "eligible_year_levels": [1]}
    result = evaluate_eligibility(profile, sch)
    yl = next(r for r in result.requirements if r.key == "year_level")
    assert yl.result == RequirementResult.UNKNOWN
    assert result.status == QualificationStatus.PROVISIONALLY_QUALIFIED


def test_enrollment_status_met():
    profile = {"enrollment_status": "incoming_freshman", "education_level": "College"}
    sch = {"id": 4, "eligible_enrollment_status": ["incoming_freshman", "transferee"]}
    result = evaluate_eligibility(profile, sch)
    es = next(r for r in result.requirements if r.key == "enrollment_status")
    assert es.result == RequirementResult.MET


def test_enrollment_status_unmet():
    profile = {"enrollment_status": "enrolled", "education_level": "College"}
    sch = {"id": 5, "eligible_enrollment_status": ["incoming_freshman"]}
    result = evaluate_eligibility(profile, sch)
    assert result.status == QualificationStatus.NOT_ELIGIBLE


def test_citizenship_default_filipino_met():
    profile = {"education_level": "College"}
    sch = {"id": 6, "citizenship_required": "Filipino", "eligible_levels": ["College"]}
    result = evaluate_eligibility(profile, sch)
    cit = next(r for r in result.requirements if r.key == "citizenship")
    assert cit.result == RequirementResult.MET


def test_citizenship_unmet_foreign():
    profile = {"citizenship": "Foreign National", "education_level": "College"}
    sch = {"id": 7, "citizenship_required": "Filipino", "eligible_levels": ["College"]}
    result = evaluate_eligibility(profile, sch)
    assert result.status == QualificationStatus.NOT_ELIGIBLE
