"""Tests for scholarship upsert on import/staging approval."""

import json

from app import models, schemas
from app.utils.scholarship_persist import persist_scholarship_from_schema


def test_upsert_preserves_image_on_update(db_session):
    sch = schemas.Scholarship(
        title="Upsert Test Scholarship",
        provider="Test Org",
        source="gemini_research",
        link="https://example.com/upsert-1",
        application_deadline="2026-12-31",
    )
    created = persist_scholarship_from_schema(
        db_session,
        sch,
        auto_commit=True,
        verification_source="manual",
    ).row
    created.image_url = "https://cdn.example.com/manual-image.webp"
    created.image_alt = "Manual banner"
    db_session.commit()

    updated_schema = schemas.Scholarship(
        title="Upsert Test Scholarship",
        provider="Test Org",
        source="gemini_research",
        link="https://example.com/upsert-1",
        application_deadline="2027-06-30",
        description="Updated eligibility text",
    )
    result = persist_scholarship_from_schema(
        db_session,
        updated_schema,
        auto_commit=True,
        verification_source="manual",
        allow_upsert=True,
    ).row
    assert result.id == created.id
    assert result.image_url == "https://cdn.example.com/manual-image.webp"
    assert result.image_alt == "Manual banner"
    assert str(result.application_deadline) == "2027-06-30"
    assert result.description == "Updated eligibility text"


def test_staging_approve_updates_existing(api_with_db):
    client, Session = api_with_db
    db = Session()
    try:
        existing = models.Scholarship(
            title="Staging Update Target",
            provider="Org A",
            source="csv_import",
            link="https://example.com/staging-update",
            dedupe_key="staging-update-key",
            is_active=True,
            data_status="active",
        )
        db.add(existing)
        db.commit()
        db.refresh(existing)

        payload = {
            "title": "Staging Update Target",
            "provider": "Org A",
            "source": "gemini_research",
            "link": "https://example.com/staging-update",
            "application_deadline": "2027-01-15",
        }
        st = models.ScholarshipStaging(
            title=payload["title"],
            provider=payload["provider"],
            source="gemini_research",
            payload_json=json.dumps(payload),
            status="pending",
            dedupe_key="staging-update-key-2",
        )
        db.add(st)
        db.commit()
        db.refresh(st)
        staging_id = st.id

        from app.auth import create_access_token

        admin = models.User(email="upsert_admin@example.com", password_hash="x", role="admin")
        db.add(admin)
        db.commit()
        db.refresh(admin)
        token = create_access_token(admin.id, role="admin")
        headers = {"Authorization": f"Bearer {token}"}
    finally:
        db.close()

    r = client.post(
        f"/api/v1/scholarships/staging/{staging_id}/approve",
        headers=headers,
        json={"action": "update"},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["application_deadline"] == "2027-01-15"
