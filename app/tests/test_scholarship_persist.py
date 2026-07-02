"""Regression tests for scholarship persistence and staging approval."""

import json

from app import models
from app.api.v1.scholarships import persist_scholarship_from_schema
from app import schemas


def _admin_headers(client, Session):
    db = Session()
    try:
        user = models.User(
            email="admin_persist@example.com",
            password_hash="x",
            role="admin",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        from app.auth import create_access_token

        token = create_access_token(user.id, role="admin")
        return {"Authorization": f"Bearer {token}"}
    finally:
        db.close()


def test_persist_scholarship_from_schema_sets_verification_source(db_session):
    """Regression: persist_scholarship_from_schema must not raise NameError on verification_source."""
    sch = schemas.Scholarship(
        title="Persist Test Scholarship",
        provider="Test Org",
        source="philscholar",
        link="https://example.com/persist-test",
    )
    row = persist_scholarship_from_schema(
        db_session,
        sch,
        auto_commit=True,
        verification_source="team_verified",
    )
    assert row.id is not None
    assert row.verification_source == "team_verified"
    assert row.title == "Persist Test Scholarship"


def test_create_scholarship_via_api(api_with_db):
    client, Session = api_with_db
    headers = _admin_headers(client, Session)
    r = client.post(
        "/api/v1/scholarships",
        headers=headers,
        json={
            "title": "API Create Scholarship",
            "provider": "API Provider",
            "source": "csv_import",
            "link": "https://example.com/api-create",
        },
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["title"] == "API Create Scholarship"
    assert data.get("verification_source") in (None, "csv_import", "manual", "team_verified")


def test_staging_approve_via_api(api_with_db):
    client, Session = api_with_db
    db = Session()
    try:
        payload = {
            "title": "Staging Approve Scholarship",
            "provider": "Staging Org",
            "source": "philscholar",
            "link": "https://example.com/staging-approve",
        }
        st = models.ScholarshipStaging(
            title=payload["title"],
            provider=payload["provider"],
            source="philscholar",
            payload_json=json.dumps(payload),
            status="pending",
            dedupe_key="test-dedupe-staging-approve",
        )
        db.add(st)
        db.commit()
        db.refresh(st)
        staging_id = st.id
    finally:
        db.close()

    headers = _admin_headers(client, Session)
    r = client.post(f"/api/v1/scholarships/staging/{staging_id}/approve", headers=headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["title"] == "Staging Approve Scholarship"
    assert data.get("verification_source") == "team_verified"
