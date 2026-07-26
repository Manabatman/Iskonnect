"""Tests for merge-before-delete catalog admin."""

from app import models
from app.auth import create_access_token
from app.services.scholarship_catalog_admin import merge_before_delete
from app.utils.dedupe import scholarship_dedupe_key


def _admin_headers(client, Session):
    db = Session()
    try:
        user = models.User(email="admin_merge@example.com", password_hash="x", role="admin")
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"Authorization": f"Bearer {create_access_token(user.id, role='admin')}"}
    finally:
        db.close()


def test_merge_before_delete_migrates_fields_and_deletes(api_with_db):
    client, Session = api_with_db
    headers = _admin_headers(client, Session)
    db = Session()
    try:
        canonical = models.Scholarship(
            title="Canonical",
            provider="Provider",
            link="https://example.com/c",
            dedupe_key=scholarship_dedupe_key("Canonical", "Provider", "https://example.com/c"),
            is_active=True,
        )
        duplicate = models.Scholarship(
            title="Duplicate",
            provider="Provider",
            link="https://example.com/d",
            description="Rich description from duplicate",
            dedupe_key=scholarship_dedupe_key("Duplicate", "Provider", "https://example.com/d"),
            is_active=False,
            application_status="archived",
        )
        db.add_all([canonical, duplicate])
        db.commit()
        db.refresh(canonical)
        db.refresh(duplicate)
        cid, did = canonical.id, duplicate.id
    finally:
        db.close()

    r = client.post(
        "/api/v1/admin/scholarships/merge-and-delete",
        headers=headers,
        json={"canonical_id": cid, "duplicate_id": did},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["status"] == "merged_and_deleted"
    assert "description" in body["fields_merged"]

    db = Session()
    try:
        kept = db.query(models.Scholarship).filter(models.Scholarship.id == cid).first()
        assert kept is not None
        assert kept.description == "Rich description from duplicate"
        assert db.query(models.Scholarship).filter(models.Scholarship.id == did).first() is None
    finally:
        db.close()


def test_merge_dry_run_no_delete(db_session):
    canonical = models.Scholarship(
        title="Keep",
        provider="P",
        link="https://example.com/k",
        dedupe_key=scholarship_dedupe_key("Keep", "P", "https://example.com/k"),
        is_active=True,
    )
    duplicate = models.Scholarship(
        title="Lose",
        provider="P",
        link="https://example.com/l",
        dedupe_key=scholarship_dedupe_key("Lose", "P", "https://example.com/l"),
        is_active=False,
    )
    db_session.add_all([canonical, duplicate])
    db_session.commit()
    db_session.refresh(canonical)
    db_session.refresh(duplicate)

    result = merge_before_delete(
        db_session,
        canonical.id,
        duplicate.id,
        dry_run=True,
    )
    assert result.deleted is False
    assert db_session.query(models.Scholarship).filter(models.Scholarship.id == duplicate.id).first() is not None
