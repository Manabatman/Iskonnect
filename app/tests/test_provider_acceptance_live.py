"""
Provider acceptance tests — live Supabase scholarship dicts, gates forced on in-process.

These catch production data + engine regressions for trust-critical providers.
Requires DATABASE_URL; skips when scholarship rows are missing.
"""

from __future__ import annotations

import pytest

from app.config import settings
from app.db import SessionLocal
from app import models
from app.serialization.scholarship import scholarship_to_catalog_dict
from app.matching.scholarship_enrichment import attach_scholarship_join_fields
from app.matching.eligibility_result import evaluate_eligibility, QualificationStatus


def _load_sch(db, sid: int) -> dict | None:
    row = db.query(models.Scholarship).filter(models.Scholarship.id == sid).first()
    if not row:
        return None
    return attach_scholarship_join_fields(db, scholarship_to_catalog_dict(row))


def _unmet_keys(result) -> set[str]:
    return {r.key for r in result.requirements if r.result.value == "unmet"}


def _rich_incoming_profile(**overrides) -> dict:
    base = {
        "education_level": "College",
        "enrollment_status": "incoming_freshman",
        "prior_tertiary_units": 0,
        "gwa_normalized": 93,
        "region": "Metro Manila",
        "residency_years_in_locality": 5,
        "citizenship": "Filipino",
        "age": 18,
        "household_income_annual": 200_000,
        "field_of_study_broad": "STEM",
        "school_type": "public",
    }
    base.update(overrides)
    return base


@pytest.fixture(scope="module")
def live_db():
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture(autouse=True)
def enable_all_gates(monkeypatch):
    for gate in (
        "gate_prior_units",
        "gate_academic_or",
        "gate_conflicts",
        "gate_affiliations",
        "gate_age_as_of",
        "gate_work_experience",
        "gate_residency_years",
        "gate_entry_path",
        "gate_parent_salary_grade",
        "gate_marital_status",
    ):
        monkeypatch.setattr(settings, gate, True)


@pytest.fixture(scope="module")
def dost_ug(live_db):
    return _load_sch(live_db, 73)


@pytest.fixture(scope="module")
def bpmsp_he(live_db):
    return _load_sch(live_db, 76)


@pytest.fixture(scope="module")
def sm_foundation(live_db):
    return _load_sch(live_db, 10)


@pytest.fixture(scope="module")
def tes(live_db):
    return _load_sch(live_db, 66)


@pytest.fixture(scope="module")
def coscho(live_db):
    return _load_sch(live_db, 117)


@pytest.fixture(scope="module")
def jlss(live_db):
    return _load_sch(live_db, 130)


def test_dost_incoming_zero_units_eligible_path(dost_ug):
    if not dost_ug:
        pytest.skip("DOST UG (73) not in catalog")
    result = evaluate_eligibility(_rich_incoming_profile(), dost_ug)
    assert "prior_units" not in _unmet_keys(result)
    assert result.status in (
        QualificationStatus.QUALIFIED,
        QualificationStatus.PROVISIONALLY_QUALIFIED,
    )


def test_dost_college_with_prior_units_blocked(dost_ug):
    if not dost_ug:
        pytest.skip("DOST UG (73) not in catalog")
    profile = _rich_incoming_profile(
        enrollment_status="enrolled",
        prior_tertiary_units=24,
    )
    result = evaluate_eligibility(profile, dost_ug)
    assert "prior_units" in _unmet_keys(result)
    assert result.status in (
        QualificationStatus.NOT_ELIGIBLE,
        QualificationStatus.ALMOST_QUALIFIED,
    )


def test_dost_high_prior_units_blocked(dost_ug):
    if not dost_ug:
        pytest.skip("DOST UG (73) not in catalog")
    profile = _rich_incoming_profile(
        enrollment_status="enrolled",
        prior_tertiary_units=90,
        age=20,
    )
    result = evaluate_eligibility(profile, dost_ug)
    assert "prior_units" in _unmet_keys(result)
    assert result.status != QualificationStatus.QUALIFIED


def test_sm_incoming_freshman_eligible_path(sm_foundation):
    if not sm_foundation:
        pytest.skip("SM Foundation (10) not in catalog")
    result = evaluate_eligibility(_rich_incoming_profile(), sm_foundation)
    assert "prior_units" not in _unmet_keys(result)
    assert result.status in (
        QualificationStatus.QUALIFIED,
        QualificationStatus.PROVISIONALLY_QUALIFIED,
        QualificationStatus.ALMOST_QUALIFIED,
    )


def test_sm_enrolled_with_units_blocked(sm_foundation):
    if not sm_foundation:
        pytest.skip("SM Foundation (10) not in catalog")
    profile = _rich_incoming_profile(
        enrollment_status="enrolled",
        prior_tertiary_units=12,
    )
    result = evaluate_eligibility(profile, sm_foundation)
    assert "prior_units" in _unmet_keys(result)
    assert result.status != QualificationStatus.QUALIFIED


def test_tes_active_stufap_conflict_not_eligible(tes):
    if not tes:
        pytest.skip("TES (66) not in catalog")
    profile = {
        "education_level": "College",
        "gwa_normalized": 80,
        "active_grant_scope_codes": ["national_stufap"],
    }
    result = evaluate_eligibility(profile, tes)
    assert "conflict_scope" in _unmet_keys(result)
    assert result.status == QualificationStatus.NOT_ELIGIBLE


def test_coscho_no_ncfrs_not_eligible(coscho):
    if not coscho:
        pytest.skip("CoScho (117) not in catalog")
    profile = {
        "education_level": "College",
        "gwa_normalized": 85,
        "affiliation_codes": [],
    }
    result = evaluate_eligibility(profile, coscho)
    assert "required_affiliation" in _unmet_keys(result)
    assert result.status == QualificationStatus.NOT_ELIGIBLE


def test_coscho_ncfrs_affiliation_met(coscho):
    if not coscho:
        pytest.skip("CoScho (117) not in catalog")
    profile = {
        "education_level": "College",
        "gwa_normalized": 85,
        "affiliation_codes": ["ncfrs"],
        "is_4ps_listahanan": True,
    }
    result = evaluate_eligibility(profile, coscho)
    assert "required_affiliation" not in _unmet_keys(result)


def test_bpmsp_rank_or_gwa_eligible(bpmsp_he):
    if not bpmsp_he:
        pytest.skip("BPMSP HE (76) not in catalog")
    profile = _rich_incoming_profile(
        gwa_normalized=88,
        class_rank=3,
        class_size=120,
    )
    result = evaluate_eligibility(profile, bpmsp_he)
    academic = [r for r in result.requirements if r.key == "academic"]
    assert academic and academic[0].result.value == "met"
    assert result.status in (
        QualificationStatus.QUALIFIED,
        QualificationStatus.PROVISIONALLY_QUALIFIED,
        QualificationStatus.ALMOST_QUALIFIED,
    )


def test_bpmsp_enrolled_with_units_blocked(bpmsp_he):
    if not bpmsp_he:
        pytest.skip("BPMSP HE (76) not in catalog")
    profile = _rich_incoming_profile(
        enrollment_status="enrolled",
        prior_tertiary_units=15,
        gwa_normalized=98,
        class_rank=1,
        class_size=120,
    )
    result = evaluate_eligibility(profile, bpmsp_he)
    assert "prior_units" in _unmet_keys(result)
    assert result.status != QualificationStatus.QUALIFIED


def test_jlss_year_level_gating(jlss):
    if not jlss:
        pytest.skip("JLSS (130) not in catalog")
    if jlss.get("min_year_level") is None and jlss.get("max_year_level") is None:
        pytest.skip("JLSS catalog row lacks structured year_level constraints")

    y1 = _rich_incoming_profile(year_level=1)
    y2 = _rich_incoming_profile(year_level=2, enrollment_status="enrolled")
    y3 = _rich_incoming_profile(year_level=3, enrollment_status="enrolled", prior_tertiary_units=60, age=20)

    s1 = evaluate_eligibility(y1, jlss).status.value
    s2 = evaluate_eligibility(y2, jlss).status.value
    s3 = evaluate_eligibility(y3, jlss).status.value
    assert s1 == QualificationStatus.NOT_ELIGIBLE.value
    assert s2 in (
        QualificationStatus.QUALIFIED.value,
        QualificationStatus.PROVISIONALLY_QUALIFIED.value,
    )
    assert s3 == QualificationStatus.NOT_ELIGIBLE.value


def _grade12_compeng_ph(**overrides) -> dict:
    base = {
        "education_level": "Grade 12",
        "enrollment_status": "incoming_freshman",
        "prior_tertiary_units": 0,
        "gwa_normalized": 93,
        "region": "Metro Manila",
        "residency_years_in_locality": 5,
        "citizenship": "Filipino",
        "age": 18,
        "household_income_annual": 200_000,
        "field_of_study_broad": "Engineering",
        "preferred_courses": ["BS Computer Engineering"],
        "study_destination_preference": "PHILIPPINES_ONLY",
    }
    base.update(overrides)
    return base


@pytest.fixture(scope="module")
def mext_ug(live_db):
    return _load_sch(live_db, 81)


@pytest.fixture(scope="module")
def gks_ug(live_db):
    return _load_sch(live_db, 65)


@pytest.fixture(scope="module")
def gesp(live_db):
    return _load_sch(live_db, 84)


@pytest.fixture(scope="module")
def gabay_guro(live_db):
    return _load_sch(live_db, 16)


@pytest.fixture(scope="module")
def pagpupugay(live_db):
    return _load_sch(live_db, 14)


@pytest.fixture(scope="module")
def gbf_stem(live_db):
    return _load_sch(live_db, 72)


@pytest.mark.parametrize(
    "fixture_name",
    ["mext_ug", "gks_ug", "gesp", "gabay_guro", "pagpupugay"],
)
def test_grade12_compeng_false_positives_blocked(request, fixture_name):
    sch = request.getfixturevalue(fixture_name)
    if not sch:
        pytest.skip(f"{fixture_name} not in catalog")
    result = evaluate_eligibility(_grade12_compeng_ph(), sch)
    assert result.status in (
        QualificationStatus.NOT_ELIGIBLE,
        QualificationStatus.ALMOST_QUALIFIED,
    )
    if result.status == QualificationStatus.ALMOST_QUALIFIED:
        assert _unmet_keys(result)


def test_gbf_stem_may_match_compeng(gbf_stem):
    if not gbf_stem:
        pytest.skip("GBF STEM (72) not in catalog")
    result = evaluate_eligibility(_grade12_compeng_ph(), gbf_stem)
    assert result.status in (
        QualificationStatus.QUALIFIED,
        QualificationStatus.PROVISIONALLY_QUALIFIED,
        QualificationStatus.ALMOST_QUALIFIED,
        QualificationStatus.NOT_ELIGIBLE,
    )


def test_gesp_true_positive_gsis_dependent(gesp):
    if not gesp:
        pytest.skip("GESP (84) not in catalog")
    profile = _rich_incoming_profile(is_gsis_dependent=True, study_destination_preference="PHILIPPINES_ONLY")
    result = evaluate_eligibility(profile, gesp)
    assert "required_affiliation" not in _unmet_keys(result)


def test_pagpupugay_true_positive_frontliner(pagpupugay):
    if not pagpupugay:
        pytest.skip("Pagpupugay (14) not in catalog")
    profile = _grade12_compeng_ph(is_medical_frontliner_dependent=True)
    result = evaluate_eligibility(profile, pagpupugay)
    assert "required_affiliation" not in _unmet_keys(result)


def test_mext_true_positive_abroad_preference(mext_ug):
    if not mext_ug:
        pytest.skip("MEXT (81) not in catalog")
    from app.utils.json_helpers import parse_json_list

    countries = parse_json_list(mext_ug.get("countries"))
    if not countries:
        pytest.skip("MEXT (81) countries not remediated yet")
    profile = _grade12_compeng_ph(study_destination_preference="ABROAD_ONLY")
    result = evaluate_eligibility(profile, mext_ug)
    assert "study_destination" not in _unmet_keys(result)


def test_gks_true_positive_abroad_preference(gks_ug):
    if not gks_ug:
        pytest.skip("GKS (65) not in catalog")
    from app.utils.json_helpers import parse_json_list

    countries = parse_json_list(gks_ug.get("countries"))
    if not countries:
        pytest.skip("GKS (65) countries not remediated yet")
    profile = _grade12_compeng_ph(study_destination_preference="BOTH")
    result = evaluate_eligibility(profile, gks_ug)
    assert "study_destination" not in _unmet_keys(result)


def test_gabay_guro_true_positive_education_major(gabay_guro):
    if not gabay_guro:
        pytest.skip("Gabay Guro (16) not in catalog")
    profile = _grade12_compeng_ph(
        field_of_study_broad="Education",
        preferred_courses=["Bachelor of Elementary Education"],
    )
    result = evaluate_eligibility(profile, gabay_guro)
    assert "field" not in _unmet_keys(result)


def test_megaworld_school_gate_when_partner_list_present(live_db):
    for sid in (61, 132):
        sch = _load_sch(live_db, sid)
        if not sch:
            pytest.skip(f"Megaworld {sid} not in catalog")
        from app.utils.json_helpers import parse_json_list

        schools = parse_json_list(sch.get("eligible_schools"))
        if not schools:
            pytest.skip(f"Megaworld {sid} has no eligible_schools — data gap, not engine test")
        non_partner = _rich_incoming_profile(
            school="University of Santo Tomas",
            target_school="University of Santo Tomas",
        )
        result = evaluate_eligibility(non_partner, sch)
        assert "school" in _unmet_keys(result)
