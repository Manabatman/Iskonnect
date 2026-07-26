"""Organization taxonomy: slug generation and provider backfill."""

from __future__ import annotations

import json
import re
from typing import Any

from sqlalchemy.orm import Session

from app import models


def slugify_org_name(name: str) -> str:
    """Produce URL-safe slug from organization name."""
    s = (name or "").strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "unknown"


def _infer_org_type(provider_type: str | None) -> str | None:
    if not provider_type:
        return None
    mapping = {
        "Government": "government",
        "Private": "private",
        "LGU": "lgu",
        "Institutional": "institutional",
    }
    return mapping.get(provider_type.strip(), provider_type.strip().lower())


def backfill_organizations_from_providers(db: Session) -> dict[str, int]:
    """
    Create organizations from distinct scholarship provider strings and link rows.
    Returns counts: organizations_created, scholarships_linked.
    """
    providers = (
        db.query(models.Scholarship.provider, models.Scholarship.provider_type)
        .filter(models.Scholarship.provider.isnot(None), models.Scholarship.provider != "")
        .distinct()
        .all()
    )

    org_by_name: dict[str, models.Organization] = {}
    existing = db.query(models.Organization).all()
    for org in existing:
        org_by_name[org.canonical_name.strip().lower()] = org

    created = 0
    linked = 0
    slug_counts: dict[str, int] = {}

    for provider, provider_type in providers:
        name = (provider or "").strip()
        if not name:
            continue
        key = name.lower()
        org = org_by_name.get(key)
        if not org:
            base_slug = slugify_org_name(name)
            slug_counts[base_slug] = slug_counts.get(base_slug, 0) + 1
            slug = base_slug if slug_counts[base_slug] == 1 else f"{base_slug}-{slug_counts[base_slug]}"
            org = models.Organization(
                slug=slug,
                canonical_name=name,
                aliases=json.dumps([]),
                org_type=_infer_org_type(provider_type),
                official_domains=json.dumps([]),
                verification_status="unverified",
            )
            db.add(org)
            db.flush()
            org_by_name[key] = org
            created += 1

        rows = (
            db.query(models.Scholarship)
            .filter(
                models.Scholarship.provider == name,
                models.Scholarship.organization_id.is_(None),
            )
            .all()
        )
        for row in rows:
            row.organization_id = org.id
            linked += 1

    db.commit()
    return {"organizations_created": created, "scholarships_linked": linked}


def resolve_organization_logo(row: Any, db: Session | None = None) -> str | None:
    """Return logo_url from linked organization, if any."""
    org_id = getattr(row, "organization_id", None) if not isinstance(row, dict) else row.get("organization_id")
    if not org_id or db is None:
        return None
    org = db.query(models.Organization).filter(models.Organization.id == org_id).first()
    return org.logo_url if org else None
