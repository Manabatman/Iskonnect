"""Tests for DATA-10 organization auto-link on persist."""

from app import models, schemas
from app.taxonomy.organizations import backfill_organizations_from_providers, ensure_organization_id
from app.utils.scholarship_persist import persist_scholarship_from_schema
from app.serialization.scholarship import scholarship_row_to_payload


def test_ensure_organization_id_creates_and_reuses(db_session):
    first = ensure_organization_id(db_session, "CHED", "Government")
    second = ensure_organization_id(db_session, "CHED", "Government")
    assert first is not None
    assert first == second
    assert db_session.query(models.Organization).count() == 1


def test_persist_links_organization_id(db_session):
    sch = schemas.Scholarship(
        title="Org Link Test",
        provider="Test Agency",
        provider_type="Government",
        link="https://example.com/org-link",
        eligible_levels=["College"],
    )
    result = persist_scholarship_from_schema(db_session, sch)
    assert result.row.organization_id is not None
    org = db_session.query(models.Organization).filter_by(id=result.row.organization_id).first()
    assert org is not None
    assert org.canonical_name == "Test Agency"


def test_backfill_idempotent(db_session):
    sch = schemas.Scholarship(
        title="Backfill One",
        provider="Duplicate Provider",
        link="https://example.com/backfill-1",
        eligible_levels=["College"],
    )
    persist_scholarship_from_schema(db_session, sch)
    first = backfill_organizations_from_providers(db_session)
    second = backfill_organizations_from_providers(db_session)
    assert second["organizations_created"] == 0


def test_serialization_provider_display(db_session):
    org = models.Organization(
        slug="deped",
        canonical_name="Department of Education",
        aliases="[]",
        official_domains="[]",
    )
    db_session.add(org)
    db_session.flush()
    row = models.Scholarship(
        title="Display Test",
        provider="deped raw",
        organization_id=org.id,
        link="https://example.com/display",
    )
    db_session.add(row)
    db_session.flush()
    row.organization = org
    payload = scholarship_row_to_payload(row)
    assert payload["provider"] == "deped raw"
    assert payload["provider_display"] == "Department of Education"
