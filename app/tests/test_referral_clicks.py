"""Aggregate outbound referral click instrumentation (C9)."""

import json

from app import models
from app.auth import create_access_token


def _seed_scholarship(Session):
    db = Session()
    try:
        s = models.Scholarship(title="Referral Test", provider="Gov", is_active=True)
        db.add(s)
        db.commit()
        db.refresh(s)
        return s.id
    finally:
        db.close()


def test_referral_click_aggregate_no_pii(api_with_db):
    client, Session = api_with_db
    sid = _seed_scholarship(Session)

    payload = {
        "scholarship_id": sid,
        "surface": "card",
        "link_kind": "apply_official",
    }
    r = client.post("/api/v1/analytics/referral-clicks", json=payload)
    assert r.status_code == 200, r.text
    assert r.json()["recorded"] is True

    forbidden = {"user_id", "email", "ip_address", "session_id", "contact_email"}
    assert forbidden.isdisjoint(payload.keys())

    r2 = client.post("/api/v1/analytics/referral-clicks", json=payload)
    assert r2.status_code == 200

    db = Session()
    try:
        rows = db.query(models.ReferralClickDaily).filter(models.ReferralClickDaily.scholarship_id == sid).all()
        assert len(rows) == 1
        assert rows[0].click_count == 2
        assert rows[0].surface == "card"
        assert rows[0].link_kind == "apply_official"
    finally:
        db.close()


def test_referral_click_unknown_scholarship_404(api_with_db):
    client, _Session = api_with_db
    r = client.post(
        "/api/v1/analytics/referral-clicks",
        json={"scholarship_id": 999999, "surface": "card", "link_kind": "apply_official"},
    )
    assert r.status_code == 404


def test_admin_overview_includes_referral_clicks(api_with_db):
    client, Session = api_with_db
    sid = _seed_scholarship(Session)

    db = Session()
    try:
        admin = models.User(email="admin-ref@test.com", password_hash="x", role="admin")
        db.add(admin)
        db.commit()
        db.refresh(admin)
        token = create_access_token(admin.id, role="admin")
    finally:
        db.close()

    client.post(
        "/api/v1/analytics/referral-clicks",
        json={"scholarship_id": sid, "surface": "trust_source", "link_kind": "view_source"},
    )

    r = client.get("/api/v1/admin/analytics/overview", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text
    data = r.json()
    assert "referral_clicks_last_30_days" in data
    assert data["referral_clicks_last_30_days"] >= 1


def test_feedback_triage_patch(api_with_db):
    client, Session = api_with_db
    db = Session()
    try:
        admin = models.User(email="admin-triage@test.com", password_hash="x", role="admin")
        db.add(admin)
        fb = models.ProductFeedback(category="suggestion", message="Add dark mode")
        db.add(fb)
        db.commit()
        db.refresh(admin)
        db.refresh(fb)
        token = create_access_token(admin.id, role="admin")
        fid = fb.id
    finally:
        db.close()

    r = client.patch(
        f"/api/v1/admin/feedback/{fid}",
        headers={"Authorization": f"Bearer {token}"},
        json={"triage_status": "planned", "triage_note": "Q3 UX pass"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["triage_status"] == "planned"
    assert body["triage_note"] == "Q3 UX pass"
