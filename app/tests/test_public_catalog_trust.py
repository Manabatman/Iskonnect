"""Public catalog trust endpoint (A7)."""

from datetime import datetime, timedelta

from app import models


def test_catalog_trust_empty(api_with_db):
    client, _Session = api_with_db
    r = client.get("/api/v1/public/catalog-trust")
    assert r.status_code == 200
    data = r.json()
    assert data["published_count"] == 0
    assert data["last_catalog_verification_at"] is None
    assert data["verified_within_90d_count"] == 0
    assert data["verification_fresh_days"] == 90


def test_catalog_trust_aggregates(api_with_db):
    client, Session = api_with_db
    db = Session()
    now = datetime.utcnow()
    try:
        for title, verified_at, is_active in [
            ("Fresh", now - timedelta(days=10), True),
            ("Stale", now - timedelta(days=120), True),
            ("Unverified", None, True),
            ("Inactive", now, False),
        ]:
            db.add(
                models.Scholarship(
                    title=title,
                    provider="Test Provider",
                    is_active=is_active,
                    last_verified_at=verified_at,
                    data_completeness_score=80,
                )
            )
        db.commit()
    finally:
        db.close()

    r = client.get("/api/v1/public/catalog-trust")
    assert r.status_code == 200
    data = r.json()
    assert data["published_count"] == 3
    assert data["verified_within_90d_count"] == 1
    assert data["last_catalog_verification_at"] is not None
