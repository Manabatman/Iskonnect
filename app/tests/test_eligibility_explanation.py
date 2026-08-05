"""Eligibility explanation object — backend single source of truth for UI."""

import json
from datetime import date, timedelta

from app.matching.eligibility_explanation import (
    STATUS_CURRENTLY_NOT_ELIGIBLE,
    STATUS_ELIGIBLE_NOW,
    STATUS_NOT_ELIGIBLE_YET,
    CATALOG_INCLUDED,
    CATALOG_PENDING,
    CATALOG_UNAVAILABLE,
    build_eligibility_explanation,
)
from app.matching.eligibility_result import evaluate_eligibility


def _explain(profile: dict, sch: dict) -> dict:
    elig = evaluate_eligibility(profile, sch)
    return build_eligibility_explanation(profile, sch, elig)


def test_citizenship_fixed_blocker():
    profile = {"citizenship": "Foreign National", "education_level": "College"}
    sch = {"id": 1, "citizenship_required": "Filipino", "eligible_levels": ["College"]}
    out = _explain(profile, sch)
    assert out["status"] == STATUS_CURRENTLY_NOT_ELIGIBLE
    assert out["primary_blocker"]["key"] == "citizenship"
    cit = next(r for r in out["requirements"] if r["key"] == "citizenship")
    assert "Based on the program rules" in cit["blocker_explanation"]
    assert "Only Filipino citizens are eligible" in cit["blocker_explanation"]


def test_year_level_primary_blocker_over_gwa():
    profile = {
        "education_level": "College",
        "citizenship": "Filipino",
        "current_year_level": 4,
        "gwa_normalized": 90.0,
    }
    sch = {
        "id": 2,
        "eligible_levels": ["College"],
        "eligible_year_levels": [1, 2],
        "min_gwa_normalized": 85.0,
    }
    out = _explain(profile, sch)
    assert out["status"] == STATUS_NOT_ELIGIBLE_YET
    assert out["primary_blocker"]["key"] == "year_level"
    yl = next(r for r in out["requirements"] if r["key"] == "year_level")
    assert yl["changeable"] == "changeable"
    assert "may qualify" in (yl.get("change_hint") or "")


def test_year_level_conditional_hint_not_predictive():
    profile = {
        "education_level": "College",
        "citizenship": "Filipino",
        "current_year_level": 2,
    }
    sch = {"id": 3, "eligible_levels": ["College"], "eligible_year_levels": [3]}
    out = _explain(profile, sch)
    yl = next(r for r in out["requirements"] if r["key"] == "year_level")
    hint = yl.get("change_hint") or ""
    assert "incoming 3rd-year" in hint.lower() or "3rd" in hint
    assert "will qualify" not in hint.lower()
    assert "you will" not in out["summary"].lower()


def test_qualified_and_open():
    profile = {
        "education_level": "College",
        "citizenship": "Filipino",
        "region": "NCR",
        "gwa_normalized": 90.0,
    }
    sch = {
        "id": 4,
        "eligible_levels": ["College"],
        "eligible_regions": ["NCR"],
        "application_open_date": (date.today() - timedelta(days=30)).isoformat(),
        "application_deadline": (date.today() + timedelta(days=60)).isoformat(),
    }
    out = _explain(profile, sch)
    assert out["status"] == STATUS_ELIGIBLE_NOW
    assert "applications are open" in out["summary"].lower()
    assert out["primary_blocker"] is None


def test_qualified_but_closed_window():
    profile = {
        "education_level": "College",
        "citizenship": "Filipino",
        "region": "NCR",
        "gwa_normalized": 90.0,
    }
    sch = {
        "id": 5,
        "eligible_levels": ["College"],
        "eligible_regions": ["NCR"],
        "application_deadline": (date.today() - timedelta(days=10)).isoformat(),
    }
    out = _explain(profile, sch)
    assert out["status"] == STATUS_NOT_ELIGIBLE_YET
    assert "meet the eligibility requirements" in out["summary"]
    assert "closed" in out["summary"].lower()
    assert out["primary_blocker"] is None


def test_rolling_application_window():
    profile = {"education_level": "College", "citizenship": "Filipino", "region": "NCR"}
    sch = {
        "id": 6,
        "eligible_levels": ["College"],
        "eligible_regions": ["NCR"],
        "cycle_type": "rolling",
    }
    out = _explain(profile, sch)
    assert out["application_window"] == "rolling"


def test_eligibility_endpoint_returns_explanation(api_with_db):
    from app import models

    client, Session = api_with_db
    reg = client.post(
        "/api/v1/auth/register",
        json={"email": "explain-user@test.com", "password": "password1234"},
    )
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    db = Session()
    try:
        user = db.query(models.User).filter(models.User.email == "explain-user@test.com").first()
        s = models.Scholarship(
            title="Explain Test",
            provider="Gov",
            eligible_levels=json.dumps(["College"]),
            is_active=True,
        )
        db.add(s)
        student = models.Student(
            user_id=user.id,
            full_name="Test",
            email="explain-user@test.com",
            education_level="College",
            region="NCR",
            citizenship="Filipino",
        )
        db.add(student)
        db.commit()
        db.refresh(s)
        db.refresh(student)
        sid, pid = s.id, student.id
    finally:
        db.close()

    res = client.get(
        f"/api/v1/scholarships/{sid}/eligibility",
        params={"profile_id": pid},
        headers=headers,
    )
    assert res.status_code == 200
    body = res.json()
    assert body["status"] in (STATUS_ELIGIBLE_NOW, STATUS_NOT_ELIGIBLE_YET, STATUS_CURRENTLY_NOT_ELIGIBLE)
    assert body["status_label"]
    assert body["summary"]
    assert body["application_window"]
    assert body["next_action"]
    assert isinstance(body["requirements"], list)


def test_catalog_included_when_publishable():
    profile = {"education_level": "College", "citizenship": "Filipino", "region": "NCR"}
    sch = {
        "id": 10,
        "title": "Full Catalog",
        "provider": "Gov",
        "link": "https://example.com/s",
        "eligible_levels": ["College"],
        "eligible_regions": ["NCR"],
        "application_deadline": (date.today() + timedelta(days=60)).isoformat(),
        "data_status": "active",
    }
    out = _explain(profile, sch)
    assert out["catalog_status"] == CATALOG_INCLUDED
    assert out["catalog_message"] is None


def test_catalog_pending_when_not_publishable():
    profile = {"education_level": "College", "citizenship": "Filipino"}
    sch = {"id": 11, "title": "Sparse", "data_status": "active"}
    out = _explain(profile, sch)
    assert out["catalog_status"] == CATALOG_PENDING
    assert "not yet included in automated recommendations" in (out["catalog_message"] or "").lower()


def test_catalog_unavailable_when_expired():
    profile = {"education_level": "College", "citizenship": "Filipino"}
    sch = {
        "id": 12,
        "title": "Expired",
        "provider": "Gov",
        "link": "https://example.com/x",
        "eligible_levels": ["College"],
        "data_status": "expired",
    }
    out = _explain(profile, sch)
    assert out["catalog_status"] == CATALOG_UNAVAILABLE
    assert "no longer active" in (out["catalog_message"] or "").lower()
