"""Application status authorization tests."""

from app.auth import create_access_token, hash_password
from app import models


def _student_headers(client, Session, email: str = "app_status@example.com"):
    db = Session()
    try:
        user = models.User(email=email, password_hash=hash_password("password123"), email_verified=True)
        db.add(user)
        db.commit()
        db.refresh(user)
        token = create_access_token(user.id, role="student")
        return {"Authorization": f"Bearer {token}"}, user
    finally:
        db.close()


def _admin_headers(client, Session):
    db = Session()
    try:
        user = models.User(
            email="admin_app_status@example.com",
            password_hash=hash_password("password123"),
            role="admin",
            email_verified=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        token = create_access_token(user.id, role="admin")
        return {"Authorization": f"Bearer {token}"}
    finally:
        db.close()


def test_student_cannot_set_accepted_status(api_with_db):
    client, Session = api_with_db
    student_headers, _user = _student_headers(client, Session)
    admin_headers = _admin_headers(client, Session)

    sch_r = client.post(
        "/api/v1/scholarships",
        json={"title": "Status Test Scholarship", "provider": "Test", "link": "https://example.com/s"},
        headers=admin_headers,
    )
    assert sch_r.status_code == 200
    sch_id = sch_r.json()["id"]

    create_r = client.post(
        "/api/v1/applications",
        json={"scholarship_id": sch_id},
        headers=student_headers,
    )
    assert create_r.status_code == 200
    app_id = create_r.json()["id"]

    patch_r = client.patch(
        f"/api/v1/applications/{app_id}",
        json={"status": "accepted"},
        headers=student_headers,
    )
    assert patch_r.status_code == 403

    ok_r = client.patch(
        f"/api/v1/applications/{app_id}",
        json={"status": "submitted"},
        headers=student_headers,
    )
    assert ok_r.status_code == 200
    assert ok_r.json()["status"] == "submitted"
