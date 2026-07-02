"""Scholarship detail attaches EligibilityResult when profile_id is provided."""

import json

from app import models
from app.auth import create_access_token


def test_get_scholarship_with_profile_includes_qualification(api_with_db):
    client, Session = api_with_db
    db = Session()
    try:
        user = models.User(email="detail_elig@example.com", password_hash="x", role="student")
        db.add(user)
        db.commit()
        db.refresh(user)
        profile = models.Student(
            user_id=user.id,
            full_name="Test Student",
            email=user.email,
            education_level="College",
            region="NCR",
            gwa_normalized=92.0,
        )
        db.add(profile)
        sch = models.Scholarship(
            title="Detail Eligibility Test",
            provider="Test",
            is_active=True,
            eligible_levels=json.dumps(["College"]),
            eligible_regions=json.dumps(["NCR"]),
            link="https://example.com/detail-elig",
            data_completeness_score=80,
        )
        db.add(sch)
        db.commit()
        db.refresh(profile)
        db.refresh(sch)
        profile_id = profile.id
        scholarship_id = sch.id
        token = create_access_token(user.id, role="student")
    finally:
        db.close()

    r = client.get(
        f"/api/v1/scholarships/{scholarship_id}?profile_id={profile_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data.get("qualification_status") in (
        "qualified",
        "provisionally_qualified",
        "almost_qualified",
        "not_eligible",
    )
    assert "qualifying_requirements" in data
    assert "missing_requirements" in data
