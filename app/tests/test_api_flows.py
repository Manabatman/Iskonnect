"""API-level smoke tests: auth refresh cycle and applications CRUD."""

from app import models


def test_register_login_refresh_logout(api_with_db):
    client, Session = api_with_db
    r = client.post(
        "/api/v1/auth/register",
        json={"email": "flow_user@example.com", "password": "password1"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data and "refresh_token" in data
    rt = data["refresh_token"]

    r2 = client.post("/api/v1/auth/refresh", json={"refresh_token": rt})
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["access_token"]
    rt2 = data2["refresh_token"]

    r3 = client.post("/api/v1/auth/logout", json={"refresh_token": rt2})
    assert r3.status_code == 200

    r4 = client.post("/api/v1/auth/refresh", json={"refresh_token": rt2})
    assert r4.status_code == 401


def test_applications_create_and_patch(api_with_db):
    client, Session = api_with_db
    db = Session()
    try:
        sch = models.Scholarship(
            title="API Test Scholarship",
            provider="Test Provider",
            link="https://example.com/scholarship-api-test",
            source="test",
            is_active=True,
            required_documents='["Form 137", "Good moral"]',
        )
        db.add(sch)
        db.commit()
        db.refresh(sch)
        sid = sch.id
    finally:
        db.close()

    reg = client.post(
        "/api/v1/auth/register",
        json={"email": "app_user@example.com", "password": "password1"},
    )
    assert reg.status_code == 200
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post("/api/v1/applications", json={"scholarship_id": sid}, headers=headers)
    assert r.status_code == 200
    app_row = r.json()
    assert app_row["status"] == "preparing"
    aid = app_row["id"]

    docs = client.get(f"/api/v1/applications/{aid}/documents", headers=headers)
    assert docs.status_code == 200
    doc_list = docs.json()
    assert len(doc_list) == 2

    r2 = client.patch(
        f"/api/v1/applications/{aid}",
        json={"status": "submitted"},
        headers=headers,
    )
    assert r2.status_code == 200
    assert r2.json()["status"] == "submitted"

    ev = client.get(f"/api/v1/applications/{aid}/events", headers=headers)
    assert ev.status_code == 200
    assert len(ev.json()) >= 2


def test_feedback_submission_anonymous_and_auth(api_with_db):
    client, _Session = api_with_db
    r = client.post(
        "/api/v1/feedback",
        json={"category": "suggestion", "message": "More filters please", "contact_email": "x@y.com"},
    )
    assert r.status_code == 200


def test_semantic_search_matches_description(api_with_db):
    client, Session = api_with_db
    db = Session()
    try:
        db.add(
            models.Scholarship(
                title="Hidden Title Xyzzy",
                provider="Gov",
                link="https://example.com/hidden",
                source="test",
                is_active=True,
                description="Unique keyword plugh for semantic search test",
            )
        )
        db.commit()
    finally:
        db.close()

    r = client.get("/api/v1/scholarships/search/semantic", params={"query": "plugh"})
    assert r.status_code == 200
    data = r.json()
    assert data["total"] >= 1
    titles = [x["title"] for x in data["results"]]
    assert "Hidden Title Xyzzy" in titles


def test_readiness_suggestions_authenticated(api_with_db):
    client, Session = api_with_db
    db = Session()
    try:
        u = models.User(email="ready@example.com", password_hash="x", role="student")
        db.add(u)
        db.flush()
        p = models.Student(
            user_id=u.id,
            full_name="Test Student",
            email="ready@example.com",
            region="",
            education_level="",
        )
        db.add(p)
        db.commit()
        db.refresh(u)
        db.refresh(p)
        uid = u.id
        pid = p.id
    finally:
        db.close()

    from app.auth import create_access_token

    token = create_access_token(uid, role="student")
    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/api/v1/suggestions/readiness", params={"profile_id": pid}, headers=headers)
    assert r.status_code == 200
    tips = r.json()["suggestions"]
    assert isinstance(tips, list)
    assert any("region" in t.lower() for t in tips)
