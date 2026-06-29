"""Regression tests: scholarship card/display fields on every API surface."""

from __future__ import annotations

import json
from datetime import date, timedelta

import pytest

from app import models
from app.api.v1.match_history import _result_to_match_response
from app.auth import create_access_token, hash_password
from app.prediction.cycle_predictor import get_upcoming_scholarships
from app.serialization.scholarship import (
    SCHOLARSHIP_CARD_DISPLAY_KEYS,
    build_match_result_payload,
    missing_card_display_keys,
    scholarship_to_api_payload,
    scholarship_to_catalog_dict,
)


def _assert_card_display_keys(payload: dict, *, endpoint: str) -> None:
    missing = missing_card_display_keys(payload)
    assert not missing, f"{endpoint} missing card display keys: {missing}"


def _sample_scholarship_kwargs(**overrides) -> dict:
    base = {
        "title": "Serialization Test Scholarship",
        "provider": "Test Provider",
        "link": "https://example.com/serialization-test",
        "source": "test",
        "description": "Scholarship for serialization regression tests",
        "image_url": "https://cdn.example.com/scholarships/test.webp",
        "image_alt": "Test scholarship banner",
        "countries": "Philippines",
        "regions": "",
        "needs_tags": json.dumps(["financial_aid"]),
        "level": "College",
        "eligible_levels": json.dumps(["College"]),
        "eligible_regions": json.dumps([]),
        "eligible_cities": json.dumps([]),
        "eligible_school_types": json.dumps(["Public", "Private"]),
        "eligible_courses_psced": json.dumps(["STEM"]),
        "eligible_courses_specific": json.dumps([]),
        "residency_required": False,
        "benefit_tuition": True,
        "benefit_allowance_monthly": 5000,
        "benefit_books": True,
        "benefit_total_value": 120000,
        "required_documents": json.dumps(["Form 137"]),
        "application_deadline": date.today() + timedelta(days=90),
        "application_open_date": date.today() - timedelta(days=7),
        "data_status": "verified",
        "verification_source": "manual",
        "link_status": "ok",
        "is_active": True,
    }
    base.update(overrides)
    return base


def _seed_scholarship(db_session, **overrides) -> models.Scholarship:
    sch = models.Scholarship(**_sample_scholarship_kwargs(**overrides))
    db_session.add(sch)
    db_session.commit()
    db_session.refresh(sch)
    return sch


def _student_with_profile(Session, *, email: str = "serial@example.com"):
    db = Session()
    try:
        user = models.User(
            email=email,
            password_hash=hash_password("password123"),
            email_verified=True,
            role="student",
        )
        db.add(user)
        db.flush()
        profile = models.Student(
            user_id=user.id,
            full_name="Serialization Student",
            email=email,
            education_level="College",
            region="National Capital Region",
            school_type="Public",
            gwa_normalized=92.0,
            field_of_study_broad="STEM",
            household_income_annual=250_000,
        )
        db.add(profile)
        db.commit()
        db.refresh(user)
        db.refresh(profile)
        token = create_access_token(user.id, role="student")
        return user, profile, {"Authorization": f"Bearer {token}"}
    finally:
        db.close()


@pytest.mark.parametrize("serializer", [scholarship_to_api_payload, scholarship_to_catalog_dict])
def test_serializers_include_all_card_display_keys(db_session, serializer):
    sch = _seed_scholarship(db_session)
    payload = serializer(sch)
    _assert_card_display_keys(payload, endpoint=serializer.__name__)


def test_build_match_result_payload_includes_card_fields(db_session):
    sch = _seed_scholarship(db_session)
    catalog = scholarship_to_catalog_dict(sch)
    payload = build_match_result_payload(
        catalog,
        scoring={
            "score": 0.85,
            "final_score": 0.85,
            "eligibility_status": True,
            "deadline_passed": False,
            "explanation": ["Good fit"],
            "breakdown": {"academic": 0.9},
            "confidence": "high",
            "suggestions": [],
            "why_not_higher": [],
            "scoring_policy_version": "v1",
        },
    )
    _assert_card_display_keys(payload, endpoint="build_match_result_payload")


def test_stored_match_response_includes_image_fields(db_session):
    sch = _seed_scholarship(db_session)
    run = models.MatchRun(user_id=1, profile_id=1)
    db_session.add(run)
    db_session.flush()
    result = models.MatchResult(
        run_id=run.id,
        scholarship_id=sch.id,
        score=0.8,
        final_score=0.8,
        explanation=json.dumps(["Eligible"]),
        confidence="high",
    )
    db_session.add(result)
    db_session.commit()

    payload = _result_to_match_response(result, sch)
    assert payload["image_url"] == sch.image_url
    assert payload["image_alt"] == sch.image_alt
    _assert_card_display_keys(payload, endpoint="match_history._result_to_match_response")


def test_upcoming_scholarships_include_card_fields():
    catalog = scholarship_to_catalog_dict(
        {
            "id": 1,
            "title": "Upcoming",
            "provider": "Gov",
            "link": "https://example.com/up",
            "image_url": "https://cdn.example.com/u.webp",
            "image_alt": "Upcoming alt",
            "needs_tags": [],
            "benefit_tuition": True,
            "application_deadline": date.today().isoformat(),
            "application_open_date": None,
        }
    )
    last_open = date.today() - timedelta(days=200)
    rows = get_upcoming_scholarships(
        {
            "age": 20,
            "education_level": "College",
            "region": "National Capital Region",
            "household_income_annual": 200_000,
            "gwa_normalized": 92.0,
            "field_of_study_broad": "STEM",
        },
        [
            {
                **catalog,
                "cycle_type": "annual",
                "last_open_date": last_open.isoformat(),
                "last_close_date": (last_open + timedelta(days=60)).isoformat(),
                "eligible_levels": ["College"],
                "eligible_regions": [],
                "eligible_cities": [],
                "regions": [],
                "min_age": 16,
                "max_age": 30,
                "max_income_threshold": None,
                "min_gwa_normalized": None,
                "eligible_courses_psced": ["STEM"],
                "eligible_school_types": ["Public", "Private"],
                "residency_required": False,
            }
        ],
    )
    assert len(rows) == 1
    _assert_card_display_keys(rows[0], endpoint="get_upcoming_scholarships")


def test_search_endpoint_includes_image_fields(api_with_db):
    client, Session = api_with_db
    sch = _seed_scholarship(Session())
    r = client.get("/api/v1/scholarships/search", params={"query": "Serialization"})
    assert r.status_code == 200
    results = r.json()["results"]
    assert results
    row = next(x for x in results if x["id"] == sch.id)
    for key in ("image_url", "image_alt", "application_open_date", "needs_tags", "benefit_tuition"):
        assert key in row, f"search missing {key}"


def test_get_scholarship_by_id_includes_image_fields(api_with_db):
    client, Session = api_with_db
    sch = _seed_scholarship(Session())
    r = client.get(f"/api/v1/scholarships/{sch.id}")
    assert r.status_code == 200
    data = r.json()
    assert data["image_url"] == sch.image_url
    assert data["image_alt"] == sch.image_alt
    assert "application_open_date" in data
    assert "provider_logo" in data


def test_live_matches_include_card_fields(api_with_db):
    client, Session = api_with_db
    _seed_scholarship(Session())
    _user, profile, headers = _student_with_profile(Session, email="matches_serial@example.com")
    r = client.get(f"/api/v1/plan/{profile.id}", headers=headers)
    assert r.status_code == 200
    matches = r.json()["matches"]
    assert matches
    _assert_card_display_keys(matches[0], endpoint="GET /plan/{profile_id}")


def test_match_run_get_includes_image_fields(api_with_db):
    client, Session = api_with_db
    sch = _seed_scholarship(Session())
    user, profile, headers = _student_with_profile(Session, email="run_serial@example.com")

    db = Session()
    try:
        run = models.MatchRun(user_id=user.id, profile_id=profile.id)
        db.add(run)
        db.flush()
        db.add(
            models.MatchResult(
                run_id=run.id,
                scholarship_id=sch.id,
                score=0.75,
                final_score=0.75,
                explanation=json.dumps(["Match"]),
                confidence="medium",
            )
        )
        db.commit()
        db.refresh(run)
        run_id = run.id
    finally:
        db.close()

    r = client.get(f"/api/v1/match-runs/{run_id}", headers=headers)
    assert r.status_code == 200
    results = r.json()["results"]
    assert len(results) == 1
    assert results[0]["image_url"] == sch.image_url
    _assert_card_display_keys(results[0], endpoint="GET /match-runs/{id}")


def test_saved_scholarships_include_nested_image_fields(api_with_db):
    client, Session = api_with_db
    sch = _seed_scholarship(Session())
    _user, _profile, headers = _student_with_profile(Session, email="saved_serial@example.com")

    save = client.post(
        "/api/v1/saved-scholarships",
        json={"scholarship_id": sch.id},
        headers=headers,
    )
    assert save.status_code == 200
    nested = save.json()["scholarship"]
    assert nested["image_url"] == sch.image_url
    assert nested["image_alt"] == sch.image_alt

    listed = client.get("/api/v1/saved-scholarships", headers=headers)
    assert listed.status_code == 200
    saved = listed.json()["saved"]
    assert len(saved) == 1
    row = saved[0]
    assert row["scholarship_id"] == sch.id
    nested_list = row["scholarship"]
    assert nested_list is not None
    assert nested_list["title"] == sch.title
    assert nested_list["image_url"] == sch.image_url
    assert nested_list["image_alt"] == sch.image_alt
    assert nested_list["application_deadline"] is not None
    _assert_card_display_keys(nested_list, endpoint="GET /saved-scholarships")


def test_application_includes_nested_scholarship_image_fields(api_with_db):
    client, Session = api_with_db
    sch = _seed_scholarship(Session())
    _user, _profile, headers = _student_with_profile(Session, email="app_serial@example.com")

    created = client.post(
        "/api/v1/applications",
        json={"scholarship_id": sch.id},
        headers=headers,
    )
    assert created.status_code == 200
    app_id = created.json()["id"]

    detail = client.get(f"/api/v1/applications/{app_id}", headers=headers)
    assert detail.status_code == 200
    nested = detail.json()["scholarship"]
    assert nested is not None
    assert nested["image_url"] == sch.image_url
    assert nested["image_alt"] == sch.image_alt


def test_card_display_keys_documented():
    """Guardrail: changing SCHOLARSHIP_CARD_DISPLAY_KEYS requires updating serializers."""
    assert "image_url" in SCHOLARSHIP_CARD_DISPLAY_KEYS
    assert "image_alt" in SCHOLARSHIP_CARD_DISPLAY_KEYS
    assert "application_open_date" in SCHOLARSHIP_CARD_DISPLAY_KEYS
    assert "provider_logo" in SCHOLARSHIP_CARD_DISPLAY_KEYS
