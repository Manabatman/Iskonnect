"""Cross-user authorization isolation tests."""

from app.auth import create_access_token, create_profile_read_token, hash_password
from app import models


def _user_token(Session, email: str, password: str = "password123"):
    db = Session()
    try:
        user = models.User(
            email=email,
            password_hash=hash_password(password),
            email_verified=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        token = create_access_token(user.id, role="student")
        return user, {"Authorization": f"Bearer {token}"}
    finally:
        db.close()


def _scholarship(Session):
    db = Session()
    try:
        sch = models.Scholarship(
            title="Authz Test Scholarship",
            provider="Test",
            link="https://example.com/authz-test",
            is_active=True,
        )
        db.add(sch)
        db.commit()
        db.refresh(sch)
        return sch
    finally:
        db.close()


def test_user_cannot_read_other_users_profile(api_with_db):
    client, Session = api_with_db
    user_a, headers_a = _user_token(Session, "authz_a@example.com")
    _user_b, headers_b = _user_token(Session, "authz_b@example.com")

    db = Session()
    try:
        profile_a = models.Student(
            user_id=user_a.id,
            full_name="User A",
            email=user_a.email,
        )
        db.add(profile_a)
        db.commit()
        db.refresh(profile_a)
        pid = profile_a.id
    finally:
        db.close()

    r = client.get(f"/api/v1/profiles/{pid}", headers=headers_a)
    assert r.status_code == 200

    r2 = client.get(f"/api/v1/profiles/{pid}", headers=headers_b)
    assert r2.status_code == 403


def test_user_cannot_access_other_users_application(api_with_db):
    client, Session = api_with_db
    user_a, headers_a = _user_token(Session, "app_a@example.com")
    _user_b, headers_b = _user_token(Session, "app_b@example.com")
    sch = _scholarship(Session)

    reg = client.post(
        "/api/v1/applications",
        json={"scholarship_id": sch.id},
        headers=headers_a,
    )
    assert reg.status_code == 200
    app_id = reg.json()["id"]

    r = client.get(f"/api/v1/applications/{app_id}", headers=headers_b)
    assert r.status_code == 404


def test_user_cannot_access_other_users_match_run(api_with_db):
    client, Session = api_with_db
    user_a, headers_a = _user_token(Session, "match_a@example.com")
    _user_b, headers_b = _user_token(Session, "match_b@example.com")

    db = Session()
    try:
        profile = models.Student(user_id=user_a.id, full_name="Match A", email=user_a.email)
        db.add(profile)
        db.commit()
        db.refresh(profile)
        run = models.MatchRun(user_id=user_a.id, profile_id=profile.id)
        db.add(run)
        db.commit()
        db.refresh(run)
        run_id = run.id
    finally:
        db.close()

    ok = client.get(f"/api/v1/match-runs/{run_id}", headers=headers_a)
    assert ok.status_code == 200

    denied = client.get(f"/api/v1/match-runs/{run_id}", headers=headers_b)
    assert denied.status_code == 404


def test_user_can_delete_own_match_run(api_with_db):
    client, Session = api_with_db
    user_a, headers_a = _user_token(Session, "delete_match_a@example.com")

    db = Session()
    try:
        sch = models.Scholarship(
            title="Delete Run Test",
            provider="Test",
            link="https://example.com/delete-run",
            is_active=True,
        )
        db.add(sch)
        db.commit()
        db.refresh(sch)

        profile = models.Student(user_id=user_a.id, full_name="Delete Match A", email=user_a.email)
        db.add(profile)
        db.commit()
        db.refresh(profile)
        run = models.MatchRun(user_id=user_a.id, profile_id=profile.id)
        db.add(run)
        db.flush()
        db.add(
            models.MatchResult(
                run_id=run.id,
                scholarship_id=sch.id,
                score=0.5,
                final_score=0.5,
            )
        )
        db.commit()
        db.refresh(run)
        run_id = run.id
    finally:
        db.close()

    deleted = client.delete(f"/api/v1/match-runs/{run_id}", headers=headers_a)
    assert deleted.status_code == 200
    assert deleted.json()["status"] == "deleted"

    gone = client.get(f"/api/v1/match-runs/{run_id}", headers=headers_a)
    assert gone.status_code == 404

    db = Session()
    try:
        assert db.query(models.MatchRun).filter(models.MatchRun.id == run_id).first() is None
        assert db.query(models.MatchResult).filter(models.MatchResult.run_id == run_id).count() == 0
    finally:
        db.close()


def test_user_cannot_delete_other_users_match_run(api_with_db):
    client, Session = api_with_db
    user_a, headers_a = _user_token(Session, "delete_match_owner@example.com")
    _user_b, headers_b = _user_token(Session, "delete_match_other@example.com")

    db = Session()
    try:
        profile = models.Student(user_id=user_a.id, full_name="Owner", email=user_a.email)
        db.add(profile)
        db.commit()
        db.refresh(profile)
        run = models.MatchRun(user_id=user_a.id, profile_id=profile.id)
        db.add(run)
        db.commit()
        db.refresh(run)
        run_id = run.id
    finally:
        db.close()

    denied = client.delete(f"/api/v1/match-runs/{run_id}", headers=headers_b)
    assert denied.status_code == 404

    ok = client.get(f"/api/v1/match-runs/{run_id}", headers=headers_a)
    assert ok.status_code == 200


def test_user_b_cannot_remove_user_a_saved_scholarship(api_with_db):
    client, Session = api_with_db
    _user_a, headers_a = _user_token(Session, "saved_a@example.com")
    _user_b, headers_b = _user_token(Session, "saved_b@example.com")
    sch = _scholarship(Session)

    save = client.post(
        "/api/v1/saved-scholarships",
        json={"scholarship_id": sch.id},
        headers=headers_a,
    )
    assert save.status_code == 200

    # Idempotent delete for user B does not remove user A's bookmark
    del_r = client.delete(f"/api/v1/saved-scholarships/{sch.id}", headers=headers_b)
    assert del_r.status_code == 200

    ids = client.get("/api/v1/saved-scholarships/ids", headers=headers_a)
    assert ids.status_code == 200
    assert sch.id in ids.json()["scholarship_ids"]


def test_anonymous_profile_requires_access_token(api_with_db):
    client, Session = api_with_db
    db = Session()
    try:
        profile = models.Student(
            user_id=None,
            full_name="Anon",
            email="anon@example.com",
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        pid = profile.id
        token = create_profile_read_token(pid)
    finally:
        db.close()

    denied = client.get(f"/api/v1/profiles/{pid}")
    assert denied.status_code == 403

    allowed = client.get(
        f"/api/v1/profiles/{pid}",
        headers={"X-Profile-Access-Token": token},
    )
    assert allowed.status_code == 200
