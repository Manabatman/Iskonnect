"""Tests for student-facing scholarship detail payload (no internal verification metadata)."""

import json

from app import models
from app.auth import create_access_token
from app.utils.field_evidence import create_field_evidence


def test_public_scholarship_detail_strips_internal_verification(api_with_db):
    client, Session = api_with_db
    db = Session()
    try:
        sch = models.Scholarship(
            title="Student UX Test Scholarship",
            provider="Test",
            is_active=True,
            link="https://example.com/official",
            eligible_levels=json.dumps(["College"]),
            data_completeness_score=85,
            verification_source="csv_import",
        )
        db.add(sch)
        db.commit()
        db.refresh(sch)
        create_field_evidence(
            db,
            scholarship_id=sch.id,
            field_key="title",
            value_snapshot=sch.title,
            source_type="manual",
        )
        db.commit()
        scholarship_id = sch.id
    finally:
        db.close()

    r = client.get(f"/api/v1/scholarships/{scholarship_id}")
    assert r.status_code == 200, r.text
    data = r.json()
    assert "field_evidence" not in data
    assert "verification_badge" not in data
    assert "verification_badge_label" not in data
    assert "completeness_label" not in data
    assert data.get("student_verification_status") in ("verified", "needs_review", "archived")
    assert data.get("student_verification_label")
    assert data.get("student_verification_message")
    assert data.get("official_website") == "https://example.com/official"


def test_admin_evidence_endpoint_requires_admin(api_with_db):
    client, Session = api_with_db
    db = Session()
    try:
        student_user = models.User(email="evidence_student@example.com", password_hash="x", role="student")
        admin_user = models.User(email="evidence_admin@example.com", password_hash="x", role="admin")
        db.add_all([student_user, admin_user])
        sch = models.Scholarship(title="Evidence Test", provider="Test", is_active=True, link="https://example.com")
        db.add(sch)
        db.commit()
        db.refresh(student_user)
        db.refresh(admin_user)
        db.refresh(sch)
        create_field_evidence(
            db,
            scholarship_id=sch.id,
            field_key="title",
            value_snapshot=sch.title,
            source_type="manual",
        )
        db.commit()
        student_token = create_access_token(student_user.id, role="student")
        admin_token = create_access_token(admin_user.id, role="admin")
        scholarship_id = sch.id
    finally:
        db.close()

    denied = client.get(
        f"/api/v1/admin/scholarships/{scholarship_id}/evidence",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert denied.status_code == 403

    ok = client.get(
        f"/api/v1/admin/scholarships/{scholarship_id}/evidence",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert ok.status_code == 200, ok.text
    payload = ok.json()
    assert payload["scholarship_id"] == scholarship_id
    assert isinstance(payload.get("field_evidence"), list)
    assert len(payload["field_evidence"]) >= 1
