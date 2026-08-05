"""Phase 2 backend: editorial state, quality, organizations, reports, catalog health."""

from datetime import date, datetime, timedelta

from app import models
from app.auth import create_access_token
from app.matching.eligibility_result import _EVALUATOR_REGISTRY, evaluate_eligibility
from app.taxonomy.organizations import backfill_organizations_from_providers, slugify_org_name
from app.utils.editorial_state import apply_editorial_state, derive_data_status, derive_is_active, NEEDS_REVIEW
from app.utils.opportunity_quality import compute_opportunity_quality, apply_quality_scores


def test_opportunity_alias():
    assert models.Opportunity is models.Scholarship


def test_evaluator_registry_default_scholarship():
    assert "scholarship" in _EVALUATOR_REGISTRY
    assert len(_EVALUATOR_REGISTRY["scholarship"]) >= 8


def test_evaluate_eligibility_uses_opportunity_type(db_session):
    sch = models.Scholarship(
        title="Test",
        provider="DOST",
        link="https://example.com/t",
        opportunity_type="scholarship",
        is_active=True,
        data_status="active",
    )
    db_session.add(sch)
    db_session.commit()
    result = evaluate_eligibility({}, {"id": sch.id, "opportunity_type": "scholarship", "data_status": "active"})
    assert result.status.value in ("qualified", "provisionally_qualified", "almost_qualified", "not_eligible")


def test_editorial_state_shims():
    row = models.Scholarship(
        title="T",
        editorial_state="published",
        is_active=False,
        data_status="needs_review",
    )
    assert derive_is_active(row) is True
    apply_editorial_state(row, NEEDS_REVIEW)
    assert row.editorial_state == NEEDS_REVIEW
    assert row.is_active is True
    assert row.data_status == "needs_review"


def test_editorial_archived_maps_expired():
    row = models.Scholarship(title="T", editorial_state="archived")
    assert derive_data_status(row) == "expired"


def test_opportunity_quality_legacy_fallback(db_session):
    sch = models.Scholarship(
        title="Quality Test",
        provider="Gov",
        link="https://example.com/q",
        description="A" * 60,
        application_deadline=date.today() + timedelta(days=30),
        is_active=True,
        data_status="active",
        last_verified_at=None,
    )
    db_session.add(sch)
    db_session.commit()
    result = compute_opportunity_quality(sch, db_session)
    assert 0 <= result.score <= 100
    assert result.evidence_gated is False


def test_apply_quality_scores_populates_legacy_columns(db_session):
    sch = models.Scholarship(
        title="Score Test",
        provider="Gov",
        link="https://example.com/s",
        is_active=True,
    )
    db_session.add(sch)
    db_session.commit()
    apply_quality_scores(sch, db_session)
    assert sch.data_completeness_score is not None
    assert sch.confidence_score is not None


def test_apply_quality_scores_uses_completeness_not_opportunity(db_session):
    from app.utils.data_completeness import compute_data_completeness_score

    sch = models.Scholarship(
        title="Evidence Gated",
        provider="DOST-SEI",
        link="https://example.com/dost",
        eligible_levels='["College"]',
        eligible_regions='["NCR"]',
        application_deadline=date.today(),
        is_active=True,
        data_status="active",
        last_verified_at=datetime.utcnow(),
        verification_source="manual",
    )
    db_session.add(sch)
    db_session.commit()
    db_session.add(
        models.FieldEvidence(
            scholarship_id=sch.id,
            field_key="title",
            source_url="https://example.com/evidence",
        )
    )
    db_session.commit()
    opp = compute_opportunity_quality(sch, db_session)
    completeness = compute_data_completeness_score(sch)
    assert opp.score != completeness
    apply_quality_scores(sch, db_session)
    assert sch.data_completeness_score == completeness


def test_backfill_organizations(db_session):
    sch = models.Scholarship(
        title="Org Test",
        provider="Department of Science",
        provider_type="Government",
        link="https://example.com/o",
        is_active=True,
    )
    db_session.add(sch)
    db_session.commit()
    stats = backfill_organizations_from_providers(db_session)
    assert stats["organizations_created"] >= 1
    db_session.refresh(sch)
    assert sch.organization_id is not None


def test_slugify_org_name():
    assert slugify_org_name("DOST-SEI") == "dost-sei"


def test_report_field_triage(api_with_db):
    client, Session = api_with_db
    db = Session()
    sch = models.Scholarship(title="Report Me", provider="X", link="https://example.com/r", is_active=True)
    db.add(sch)
    db.commit()
    db.refresh(sch)
    sid = sch.id
    db.close()

    for i in range(3):
        r = client.post(
            "/api/v1/reports",
            json={
                "scholarship_id": sid,
                "issue_type": "wrong_deadline",
                "field_key": "application_deadline",
                "proposed_value": "2026-12-31",
            },
        )
        assert r.status_code == 200, r.text

    db = Session()
    sch = db.query(models.Scholarship).filter(models.Scholarship.id == sid).first()
    assert sch.editorial_state == NEEDS_REVIEW
    db.close()


def test_catalog_health_dashboard(api_with_db):
    client, Session = api_with_db
    db = Session()
    user = models.User(email="admin_ch@example.com", password_hash="x", role="admin")
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user.id, role="admin")
    db.close()

    r = client.get("/api/v1/admin/dashboard/catalog-health", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text
    data = r.json()
    assert "health" in data
    assert "import" in data
    assert "data_quality" in data
    assert "institution_specific_count" in data
    assert "deadline_unknown_count" in data
    assert "avg_quality_score" in data
    assert "verified_this_month" in data


def test_organization_public_endpoint(api_with_db):
    client, Session = api_with_db
    db = Session()
    org = models.Organization(
        slug="dost",
        canonical_name="DOST",
        verification_status="verified",
    )
    db.add(org)
    db.flush()
    db.add(
        models.Scholarship(
            title="DOST Grant",
            provider="DOST",
            organization_id=org.id,
            link="https://example.com/d",
            is_active=True,
        )
    )
    db.commit()
    db.close()

    r = client.get("/api/v1/organizations/dost")
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["slug"] == "dost"
    assert data["opportunity_count"] == 1
