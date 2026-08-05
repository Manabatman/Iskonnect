"""Trust architecture API endpoints."""

import json

from app import models
from app.utils.scholarship_versioning import record_scholarship_version


def test_scholarship_history_public(api_with_db):
    client, Session = api_with_db
    db = Session()
    try:
        s = models.Scholarship(title="History Test", provider="Test", is_active=True)
        db.add(s)
        db.commit()
        db.refresh(s)
        record_scholarship_version(
            db,
            scholarship_id=s.id,
            changes={"title": {"from": "Old", "to": "History Test"}},
            changed_by=None,
        )
        db.commit()
        sid = s.id
    finally:
        db.close()

    res = client.get(f"/api/v1/scholarships/{sid}/history")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 1
    assert data[0]["version_number"] >= 1
    assert "title" in data[0]["changes"]


def test_scholarship_eligibility_endpoint(api_with_db):
    client, Session = api_with_db
    reg = client.post(
        "/api/v1/auth/register",
        json={"email": "elig-user@test.com", "password": "password1234"},
    )
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    db = Session()
    try:
        user = db.query(models.User).filter(models.User.email == "elig-user@test.com").first()
        s = models.Scholarship(
            title="Elig Test",
            provider="Gov",
            eligible_levels=json.dumps(["College"]),
            eligible_school_types=json.dumps(["Public"]),
            is_active=True,
        )
        db.add(s)
        student = models.Student(
            user_id=user.id,
            full_name="Test",
            email="elig-user@test.com",
            education_level="College",
            school_type="Public",
            region="NCR",
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
    assert body["scholarship_id"] == sid
    assert body["profile_id"] == pid
    assert body["passes_for_matching"] is True


def test_profile_export(api_with_db):
    client, _Session = api_with_db
    reg = client.post(
        "/api/v1/auth/register",
        json={"email": "export-user@test.com", "password": "password1234"},
    )
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/api/v1/profiles",
        json={
            "full_name": "Export Me",
            "email": "export-user@test.com",
            "education_level": "College",
            "region": "NCR",
        },
        headers=headers,
    )

    res = client.get("/api/v1/profiles/me/export", headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["profile"]["full_name"] == "Export Me"
    assert "exported_at" in body
