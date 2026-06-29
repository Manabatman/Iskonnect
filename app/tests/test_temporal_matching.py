"""Tests for temporal eligibility and opportunity timeline."""

from datetime import date, timedelta

from app.matching.opportunity_timeline import build_opportunity_timeline
from app.matching.match_service import MatchService
from app.matching.temporal_state import (
    ELIGIBLE_NOW,
    EXPECTED_NEXT_CYCLE,
    PAST_OPPORTUNITY,
    UI_ELIGIBLE_NOW,
    classify_scholarship_temporal,
    map_to_ui_state,
    attach_temporal_fields,
)
from app.matching.preparation import compute_application_readiness, build_document_checklist
from app.utils.freshness_chips import build_freshness_chips


def _sch(**kwargs):
    base = {
        "id": 1,
        "title": "Test Scholarship",
        "provider": "DOST",
        "link": "https://example.com",
        "is_active": True,
        "data_status": "active",
        "application_deadline": (date.today() + timedelta(days=30)).isoformat(),
        "required_documents": '["Birth Certificate", "Form 137"]',
        "last_verified_at": date.today().isoformat(),
        "verification_source": "manual",
    }
    base.update(kwargs)
    return base


def _profile(**kwargs):
    base = {
        "education_level": "College",
        "region": "NCR",
        "age": 20,
        "gwa_normalized": 85.0,
        "household_income_annual": 200000,
        "privacy_consent": True,
    }
    base.update(kwargs)
    return base


def test_classify_eligible_now():
    result = classify_scholarship_temporal(_profile(), _sch())
    assert result["eligibility_state"] in (ELIGIBLE_NOW, "prepare_now")
    assert result.get("next_action")


def test_ui_state_mapping():
    assert map_to_ui_state(ELIGIBLE_NOW) == UI_ELIGIBLE_NOW
    assert map_to_ui_state("requires_future_grade_level") == "future_eligibility"


def test_attach_temporal_includes_ui_state():
    row = attach_temporal_fields(_sch(), _profile())
    assert "ui_state" in row
    assert row["ui_state"] == UI_ELIGIBLE_NOW or row["ui_state"] == "prepare_ahead"


def test_classify_expected_next_cycle_when_expired():
    sch = _sch(
        data_status="expired",
        cycle_type="annual",
        last_open_date=(date.today() - timedelta(days=180)).isoformat(),
        application_deadline=(date.today() - timedelta(days=30)).isoformat(),
    )
    result = classify_scholarship_temporal(_profile(), sch)
    assert result["eligibility_state"] == EXPECTED_NEXT_CYCLE


def test_classify_past_opportunity():
    sch = _sch(
        data_status="expired",
        application_deadline=(date.today() - timedelta(days=60)).isoformat(),
    )
    result = classify_scholarship_temporal(_profile(), sch)
    assert result["eligibility_state"] == PAST_OPPORTUNITY


def test_build_opportunity_timeline_structure():
    profile = _profile()
    scholarships = [_sch(), _sch(id=2, title="Other")]
    svc = MatchService()
    scored, _ = svc.get_matches(profile, scholarships)
    timeline = build_opportunity_timeline(profile, scholarships, scored)
    assert "summary" in timeline
    assert "lanes" in timeline
    assert "headline" in timeline
    assert timeline["summary"]["total_actionable"] >= 0


def test_document_checklist():
    checklist = build_document_checklist(_sch(), _profile(documents=[{"type": "Birth Certificate", "status": "ready"}]))
    assert len(checklist) == 2
    assert checklist[0]["status"] == "ready"
    assert checklist[1]["status"] == "missing"


def test_readiness_score():
    prep = compute_application_readiness(_sch(), _profile())
    assert 0 <= prep["readiness_score"] <= 100
    assert prep["documents_total"] == 2


def test_freshness_chips_transparent():
    chips = build_freshness_chips(_sch(last_verified_at=date.today().isoformat()))
    labels = [c["label"] for c in chips]
    assert any("verified" in l.lower() for l in labels)
    assert not any("confidence" in l.lower() for l in labels)
