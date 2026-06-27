"""Scholarship image field and upload endpoint tests."""

from io import BytesIO

from app.auth import create_access_token, hash_password
from app import models


def _student_headers(client, Session):
    db = Session()
    try:
        user = models.User(email="img_student@example.com", password_hash=hash_password("password123"), email_verified=True)
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
            email="img_admin@example.com",
            password_hash=hash_password("password123"),
            role="admin",
            email_verified=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        token = create_access_token(user.id, role="admin")
        return {"Authorization": f"Bearer {token}"}, user
    finally:
        db.close()


def _create_scholarship(client, admin_headers):
    r = client.post(
        "/api/v1/scholarships",
        json={"title": "Image Test Scholarship", "provider": "Test", "link": "https://example.com/img-test"},
        headers=admin_headers,
    )
    assert r.status_code == 200
    return r.json()


def test_scholarship_response_includes_null_image_fields(api_with_db):
    client, Session = api_with_db
    admin_headers, _ = _admin_headers(client, Session)
    data = _create_scholarship(client, admin_headers)
    assert "image_url" in data
    assert data["image_url"] is None
    assert data.get("image_alt") is None


def test_student_cannot_upload_image(api_with_db):
    client, Session = api_with_db
    admin_headers, _ = _admin_headers(client, Session)
    student_headers, _ = _student_headers(client, Session)
    sch = _create_scholarship(client, admin_headers)

    # minimal PNG header bytes
    png = BytesIO(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde"
        b"\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x01\x01\x01\x00\x18\xdd\x8d\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    r = client.post(
        f"/api/v1/scholarships/{sch['id']}/image",
        files={"file": ("test.png", png, "image/png")},
        headers=student_headers,
    )
    assert r.status_code == 403


def test_admin_upload_requires_storage_config(api_with_db, monkeypatch):
    client, Session = api_with_db
    admin_headers, _ = _admin_headers(client, Session)
    sch = _create_scholarship(client, admin_headers)

    monkeypatch.setattr("app.config.settings.supabase_url", None)
    monkeypatch.setattr("app.config.settings.supabase_service_role_key", None)
    monkeypatch.setattr(
        "app.api.v1.scholarships.compress_scholarship_image",
        lambda *a, **k: (b"fake-webp", "abcd1234"),
    )

    png = BytesIO(b"fake")
    r = client.post(
        f"/api/v1/scholarships/{sch['id']}/image",
        files={"file": ("test.png", png, "image/png")},
        headers=admin_headers,
    )
    assert r.status_code == 503
