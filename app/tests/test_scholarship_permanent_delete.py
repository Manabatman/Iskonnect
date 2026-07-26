"""Tests for permanent scholarship deletion."""

from app import models
from app.auth import create_access_token
from app.services.scholarship_catalog_admin import permanently_delete_scholarship
from app.utils.dedupe import scholarship_dedupe_key


def _admin_headers(client, Session):
    db = Session()
    try:
        user = models.User(email="admin_del@example.com", password_hash="x", role="admin")
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"Authorization": f"Bearer {create_access_token(user.id, role='admin')}"}
    finally:
        db.close()


def _inactive_scholarship(db, *, title="Inactive Test", suffix="a"):
    s = models.Scholarship(
        title=title,
        provider="Test Provider",
        link=f"https://example.com/{suffix}",
        dedupe_key=scholarship_dedupe_key(title, "Test Provider", f"https://example.com/{suffix}"),
        is_active=False,
        application_status="archived",
        editorial_state="archived",
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


def test_permanent_delete_rejects_active(api_with_db):
    client, Session = api_with_db
    headers = _admin_headers(client, Session)
    db = Session()
    try:
        s = models.Scholarship(
            title="Active One",
            provider="Gov",
            link="https://example.com/active",
            dedupe_key=scholarship_dedupe_key("Active One", "Gov", "https://example.com/active"),
            is_active=True,
        )
        db.add(s)
        db.commit()
        db.refresh(s)
        sid = s.id
    finally:
        db.close()

    r = client.delete(f"/api/v1/admin/scholarships/{sid}/permanent", headers=headers)
    assert r.status_code == 400
    assert "Deactivate" in r.json()["detail"]


def test_permanent_delete_inactive(api_with_db):
    client, Session = api_with_db
    headers = _admin_headers(client, Session)
    db = Session()
    try:
        user = models.User(email="saved@test.com", password_hash="x", role="student")
        db.add(user)
        db.commit()
        db.refresh(user)
        s = _inactive_scholarship(db, title="Delete Me", suffix="del1")
        sid = s.id
        db.add(models.SavedScholarship(user_id=user.id, scholarship_id=sid))
        db.commit()
    finally:
        db.close()

    r = client.delete(f"/api/v1/admin/scholarships/{sid}/permanent", headers=headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["status"] == "deleted"
    assert data["scholarship_id"] == sid

    db = Session()
    try:
        assert db.query(models.Scholarship).filter(models.Scholarship.id == sid).first() is None
        assert db.query(models.SavedScholarship).filter(models.SavedScholarship.scholarship_id == sid).count() == 0
    finally:
        db.close()


def test_permanent_delete_service_not_found(db_session):
    import pytest

    from app.services.scholarship_catalog_admin import CatalogAdminError

    with pytest.raises(CatalogAdminError):
        permanently_delete_scholarship(db_session, 99999)
