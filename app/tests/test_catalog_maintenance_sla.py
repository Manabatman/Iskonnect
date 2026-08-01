"""Catalog maintenance 90-day verification SLA metrics."""

from datetime import datetime, timedelta, timezone

from app import models
from app.jobs.catalog_maintenance import run_catalog_maintenance
from app.utils.trust_constants import VERIFICATION_FRESH_DAYS


def test_catalog_maintenance_reports_expired_90d(db_session, monkeypatch):
    cutoff = datetime.now(timezone.utc) - timedelta(days=VERIFICATION_FRESH_DAYS + 5)
    row = models.Scholarship(
        title="Stale Verify",
        provider="Fixture",
        link="https://example.com/stale-verify",
        is_active=True,
        data_status="active",
        last_verified_at=cutoff.replace(tzinfo=None),
    )
    db_session.add(row)
    db_session.commit()

    monkeypatch.setattr("app.jobs.catalog_maintenance.SessionLocal", lambda: db_session)
    monkeypatch.setattr("app.jobs.catalog_maintenance.invalidate_scholarship_cache", lambda: None)
    monkeypatch.setattr("app.jobs.catalog_maintenance.run_data_quality_checks", lambda: {})
    monkeypatch.setattr("app.jobs.data_quality.recompute_completeness_scores", lambda: 0)
    monkeypatch.setattr("app.jobs.data_quality.count_structured_eligibility_gaps", lambda: 0)
    monkeypatch.setattr("app.jobs.catalog_maintenance.log_job_run", lambda *a, **k: None)
    monkeypatch.setattr("app.utils.opportunity_quality.apply_quality_scores", lambda *a, **k: None)

    out = run_catalog_maintenance()
    assert out["expired_verification_90d"] >= 1
    assert out["verification_sla_days"] == VERIFICATION_FRESH_DAYS
