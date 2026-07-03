"""Regression tests for production failures (route shadowing, timeline, admin tz)."""

from __future__ import annotations

import json
from datetime import date, timedelta

from app import models
from app.auth import create_access_token, hash_password
from app.matching.opportunity_timeline import build_opportunity_timeline
from app.utils.timezone import utc_now_naive


def _seed_publishable_scholarship(db, **overrides) -> models.Scholarship:
    base = {
        "title": "Regression Test Scholarship",
        "provider": "Test Provider",
        "link": "https://example.com/regression-test",
        "source": "test",
        "description": "Scholarship for production regression tests with enough detail.",
        "level": "College",
        "eligible_levels": json.dumps(["College"]),
        "eligible_regions": json.dumps(["NCR"]),
        "eligible_cities": json.dumps([]),
        "regions": "NCR",
        "eligible_courses_psced": json.dumps(["Engineering"]),
        "residency_required": False,
        "application_deadline": date.today() + timedelta(days=90),
        "application_open_date": date.today() - timedelta(days=7),
        "data_status": "verified",
        "verification_source": "manual",
        "last_verified_at": utc_now_naive(),
        "data_completeness_score": 80,
        "is_active": True,
    }
    base.update(overrides)
    sch = models.Scholarship(**base)
    db.add(sch)
    db.commit()
    db.refresh(sch)
    return sch


def _student_with_profile(Session, *, email: str = "regression@example.com"):
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
            full_name="Regression Student",
            email=email,
            education_level="College",
            region="NCR",
            school_type="Public",
            gwa_normalized=92.0,
            field_of_study_broad="Engineering",
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


def test_sample_matches_not_shadowed_by_profile_id_route(api_with_db):
    """GET /profiles/sample-matches must not hit /profiles/{profile_id} (422)."""
    client, Session = api_with_db
    _seed_publishable_scholarship(Session())
    r = client.get(
        "/api/v1/profiles/sample-matches",
        params={
            "education_level": "College",
            "region": "NCR",
            "field_of_study_broad": "Engineering",
            "limit": 4,
        },
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert "sample_matches" in data
    assert isinstance(data["sample_matches"], list)


def test_build_opportunity_timeline_non_scored_catalog_branch():
    """Catalog scholarships outside scored set must not raise NameError."""
    profile = {
        "education_level": "College",
        "region": "NCR",
        "field_of_study_broad": "Engineering",
        "gwa_normalized": 90.0,
        "privacy_consent": True,
    }
    scored = [
        {
            "id": 1,
            "title": "Scored Match",
            "eligibility_state": "eligible_now",
            "final_score": 85,
        }
    ]
    catalog = [
        {
            "id": 1,
            "title": "Scored Match",
            "provider": "A",
            "link": "https://example.com/a",
            "eligible_levels": ["College"],
            "eligible_regions": ["NCR"],
            "application_deadline": (date.today() + timedelta(days=30)).isoformat(),
        },
        {
            "id": 2,
            "title": "Graduate Only",
            "provider": "B",
            "link": "https://example.com/b",
            "eligible_levels": ["Graduate"],
            "eligible_regions": ["NCR"],
            "application_deadline": (date.today() + timedelta(days=30)).isoformat(),
        },
    ]
    result = build_opportunity_timeline(profile, catalog, scored)
    assert "lanes" in result
    assert "summary" in result


def test_plan_endpoint_with_mixed_catalog(api_with_db):
    """GET /plan/{id} succeeds when catalog has scholarships outside scored matches."""
    client, Session = api_with_db
    _seed_publishable_scholarship(Session())
    _seed_publishable_scholarship(
        Session(),
        title="Graduate Only Program",
        link="https://example.com/graduate-only",
        eligible_levels=json.dumps(["Graduate"]),
        level="Graduate",
    )
    _user, profile, headers = _student_with_profile(Session)
    r = client.get(f"/api/v1/plan/{profile.id}", headers=headers)
    assert r.status_code == 200, r.text
    body = r.json()
    assert "matches" in body
    assert "timeline" in body


def test_admin_data_quality_with_last_verified_at(api_with_db):
    """Admin dashboard must not 500 when comparing naive last_verified_at to cutoff."""
    client, Session = api_with_db
    db = Session()
    try:
        admin = models.User(email="admin_regression@example.com", password_hash="x", role="admin")
        db.add(admin)
        db.commit()
        db.refresh(admin)
        headers = {"Authorization": f"Bearer {create_access_token(admin.id, role='admin')}"}
    finally:
        db.close()

    _seed_publishable_scholarship(Session(), last_verified_at=utc_now_naive())
    r = client.get("/api/v1/admin/data-quality", headers=headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["total_active"] >= 1
