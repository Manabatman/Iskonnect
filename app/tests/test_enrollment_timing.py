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
    assert result.status == QualificationStatus.ALMOST_QUALIFIED


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
    assert result.status == QualificationStatus.ALMOST_QUALIFIED


def test_citizenship_missing_is_unknown():
    profile = {"education_level": "College"}
    sch = {"id": 6, "citizenship_required": "Filipino", "eligible_levels": ["College"]}
    result = evaluate_eligibility(profile, sch)
    cit = next(r for r in result.requirements if r.key == "citizenship")
    assert cit.result == RequirementResult.UNKNOWN
    assert result.status == QualificationStatus.PROVISIONALLY_QUALIFIED
    assert "your citizenship" in result.unverified_requirements


def test_citizenship_unmet_foreign():
    profile = {"citizenship": "Foreign National", "education_level": "College"}
    sch = {"id": 7, "citizenship_required": "Filipino", "eligible_levels": ["College"]}
    result = evaluate_eligibility(profile, sch)
    assert result.status == QualificationStatus.NOT_ELIGIBLE


def test_almost_qualified_single_achievable_unmet_gwa():
    profile = {"education_level": "College", "gwa_normalized": 75.0, "citizenship": "Filipino"}
    sch = {"id": 8, "eligible_levels": ["College"], "min_gwa_normalized": 85.0}
    result = evaluate_eligibility(profile, sch)
    assert result.status == QualificationStatus.ALMOST_QUALIFIED


def test_not_eligible_region_unmet_not_almost():
    profile = {"education_level": "College", "region": "NCR", "citizenship": "Filipino"}
    sch = {"id": 9, "eligible_levels": ["College"], "eligible_regions": ["Region VI - Western Visayas"]}
    result = evaluate_eligibility(profile, sch)
    assert result.status == QualificationStatus.NOT_ELIGIBLE
