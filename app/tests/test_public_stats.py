"""Public stats endpoint (C1 / LAND-03a)."""

from datetime import datetime, timedelta
from unittest.mock import patch

from app import models
from app.public_stats_cache import TTL_SECONDS, get_cached_public_stats, invalidate_public_stats_cache
from app.services.public_stats import assert_no_marketing_fabrication, compute_public_stats


def test_public_stats_empty(api_with_db):
    client, _Session = api_with_db
    r = client.get("/api/v1/public/stats")
    assert r.status_code == 200
    data = r.json()
    assert data["source"] == "live"
    assert data["verified_listing_count"] == 0
    assert data["provider_count"] == 0
    assert data["region_count"] == 0
    assert data["education_level_count"] == 0
    assert data["total_documented_funding_php"] is None
    assert data["verification_fresh_days"] == 90
    assert_no_marketing_fabrication(data)


def test_public_stats_aggregates(api_with_db):
    client, Session = api_with_db
    db = Session()
    now = datetime.utcnow()
    org = models.Organization(slug="dost-sei", canonical_name="DOST-SEI")
    db.add(org)
    db.flush()
    try:
        db.add(
            models.Scholarship(
                title="Fresh Grant",
                provider="DOST-SEI",
                organization_id=org.id,
                is_active=True,
                editorial_state="published",
                last_verified_at=now - timedelta(days=5),
                eligible_regions='["National Capital Region", "Region IV-A"]',
                eligible_levels='["College", "Graduate"]',
                benefit_total_value=50000,
                data_completeness_score=80,
            )
        )
        db.add(
            models.Scholarship(
                title="Stale Grant",
                provider="Other",
                is_active=True,
                editorial_state="published",
                last_verified_at=now - timedelta(days=120),
                eligible_levels='["College"]',
                data_completeness_score=80,
            )
        )
        db.commit()
    finally:
        db.close()

    invalidate_public_stats_cache()
    r = client.get("/api/v1/public/stats")
    assert r.status_code == 200
    data = r.json()
    assert data["verified_listing_count"] == 1
    assert data["provider_count"] == 1
    assert data["region_count"] == 2
    assert "National Capital Region" in data["regions"]
    assert data["education_level_count"] == 2
    assert "College" in data["education_levels"]
    assert data["last_catalog_verification_at"] is not None
    assert_no_marketing_fabrication(data)


def test_public_stats_funding_omitted_when_unreliable(api_with_db):
    client, Session = api_with_db
    db = Session()
    now = datetime.utcnow()
    try:
        for i in range(4):
            db.add(
                models.Scholarship(
                    title=f"Grant {i}",
                    provider="Prov",
                    is_active=True,
                    editorial_state="published",
                    last_verified_at=now,
                    benefit_total_value=None,
                    data_completeness_score=80,
                )
            )
        db.add(
            models.Scholarship(
                title="One valued",
                provider="Prov",
                is_active=True,
                editorial_state="published",
                last_verified_at=now,
                benefit_total_value=10000,
                data_completeness_score=80,
            )
        )
        db.commit()
    finally:
        db.close()

    invalidate_public_stats_cache()
    data = client.get("/api/v1/public/stats").json()
    assert data["total_documented_funding_php"] is None


def test_public_stats_funding_included_when_reliable(api_with_db):
    client, Session = api_with_db
    db = Session()
    now = datetime.utcnow()
    try:
        for amount in (10000, 20000, 30000):
            db.add(
                models.Scholarship(
                    title=f"Grant {amount}",
                    provider="Prov",
                    is_active=True,
                    editorial_state="published",
                    last_verified_at=now,
                    benefit_total_value=amount,
                    data_completeness_score=80,
                )
            )
        db.commit()
    finally:
        db.close()

    invalidate_public_stats_cache()
    data = client.get("/api/v1/public/stats").json()
    assert data["total_documented_funding_php"] == 60000


def test_public_stats_fallback_on_db_failure(api_with_db):
    client, _Session = api_with_db
    invalidate_public_stats_cache()
    with patch("app.api.v1.public_stats.compute_public_stats", side_effect=RuntimeError("db down")):
        r = client.get("/api/v1/public/stats")
    assert r.status_code == 200
    data = r.json()
    assert data["source"] == "fallback"
    assert data["verified_listing_count"] is None
    assert data["provider_count"] is None
    assert_no_marketing_fabrication(data)


def test_public_stats_cache_reuses_payload():
    invalidate_public_stats_cache()
    calls = {"n": 0}

    def build():
        calls["n"] += 1
        return {"source": "live", "verified_listing_count": 3}

    first = get_cached_public_stats(build)
    second = get_cached_public_stats(build)
    assert first == second
    assert calls["n"] == 1


def test_public_stats_cache_respects_ttl(monkeypatch):
    invalidate_public_stats_cache()
    calls = {"n": 0}
    times = iter([0.0, float(TTL_SECONDS + 1)])

    monkeypatch.setattr("app.public_stats_cache.time.monotonic", lambda: next(times))

    def build():
        calls["n"] += 1
        return {"source": "live", "verified_listing_count": 1}

    get_cached_public_stats(build)
    get_cached_public_stats(build)
    assert calls["n"] == 2


def test_public_stats_schema_excludes_marketing_fields():
    from app.schemas import PublicStatsResponse

    fields = set(PublicStatsResponse.model_fields)
    forbidden = {
        "user_count",
        "students_served",
        "testimonial",
        "testimonials",
        "endorsement",
        "partner_endorsement",
    }
    assert forbidden.isdisjoint(fields)
