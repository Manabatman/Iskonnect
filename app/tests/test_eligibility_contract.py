"""Tests for explainable EligibilityResult contract."""

from app.matching.eligibility_result import QualificationStatus, evaluate_eligibility


def test_pasig_resident_not_eligible_for_pasig_only():
    profile = {"city_municipality": "Quezon City", "region": "NCR"}
    sch = {
        "id": 1,
        "eligible_cities": ["Pasig"],
        "residency_required": True,
    }
    result = evaluate_eligibility(profile, sch)
    assert result.status == QualificationStatus.NOT_ELIGIBLE
    assert any("Residency" in m or "Location" in m for m in result.missing_requirements)


def test_pasig_resident_qualified_for_pasig_only():
    profile = {"city_municipality": "Pasig City", "region": "NCR"}
    sch = {
        "id": 2,
        "eligible_cities": ["Pasig"],
        "residency_required": True,
    }
    result = evaluate_eligibility(profile, sch)
    assert result.status in (QualificationStatus.QUALIFIED, QualificationStatus.PROVISIONALLY_QUALIFIED)
    assert result.passes_for_matching


def test_income_bracket_over_ceiling_not_eligible():
    profile = {"income_bracket": "250k_400k"}
    sch = {"id": 3, "max_income_threshold": 250_000}
    result = evaluate_eligibility(profile, sch)
    assert result.status == QualificationStatus.NOT_ELIGIBLE


def test_missing_gwa_provisionally_qualified():
    profile = {"education_level": "College"}
    sch = {"id": 4, "min_gwa_normalized": 90.0, "eligible_levels": ["College"]}
    result = evaluate_eligibility(profile, sch)
    assert result.status == QualificationStatus.PROVISIONALLY_QUALIFIED
    assert result.passes_for_matching
