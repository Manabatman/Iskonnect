"""Compute public landing statistics from live catalog data."""

from __future__ import annotations

from datetime import timedelta

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from app import models
from app.schemas import PublicStatsResponse
from app.utils.editorial_state import ARCHIVED, PUBLISHED, VERIFIED
from app.utils.json_helpers import parse_json_list
from app.utils.timezone import utc_now_naive
from app.utils.trust_constants import VERIFICATION_FRESH_DAYS

# Include total funding only when this share of active listings have structured amounts.
_BENEFIT_RELIABILITY_THRESHOLD = 0.6

_FORBIDDEN_MARKETING_KEYS = frozenset(
    {
        "user_count",
        "students_served",
        "testimonial",
        "testimonials",
        "endorsement",
        "partner_endorsement",
    }
)


def _active_not_archived():
    return and_(
        models.Scholarship.is_active == True,  # noqa: E712
        or_(
            models.Scholarship.editorial_state.is_(None),
            func.lower(models.Scholarship.editorial_state) != ARCHIVED,
        ),
    )


def _published_fresh_clause(fresh_cutoff):
    return and_(
        _active_not_archived(),
        models.Scholarship.last_verified_at.isnot(None),
        models.Scholarship.last_verified_at >= fresh_cutoff,
        or_(
            func.lower(models.Scholarship.editorial_state) == PUBLISHED,
            func.lower(models.Scholarship.editorial_state) == VERIFIED,
            models.Scholarship.editorial_state.is_(None),
        ),
    )


def _collect_regions_and_levels(db: Session) -> tuple[set[str], set[str]]:
    rows = (
        db.query(
            models.Scholarship.eligible_regions,
            models.Scholarship.eligible_levels,
            models.Scholarship.regions,
            models.Scholarship.level,
        )
        .filter(_active_not_archived())
        .all()
    )
    regions: set[str] = set()
    levels: set[str] = set()
    for eligible_regions, eligible_levels, legacy_regions, legacy_level in rows:
        for region in parse_json_list(eligible_regions) or parse_json_list(legacy_regions):
            if region:
                regions.add(region)
        for level in parse_json_list(eligible_levels):
            if level:
                levels.add(level)
        if legacy_level and str(legacy_level).strip():
            levels.add(str(legacy_level).strip())
    return regions, levels


def _maybe_total_documented_funding(db: Session) -> int | None:
    values = (
        db.query(models.Scholarship.benefit_total_value)
        .filter(_active_not_archived())
        .all()
    )
    if not values:
        return None
    populated = [v[0] for v in values if v[0] is not None and int(v[0]) > 0]
    if len(populated) / len(values) < _BENEFIT_RELIABILITY_THRESHOLD:
        return None
    return int(sum(populated))


def compute_public_stats(db: Session) -> PublicStatsResponse:
    now = utc_now_naive()
    fresh_cutoff = now - timedelta(days=VERIFICATION_FRESH_DAYS)

    verified_listing_count = (
        db.query(func.count(models.Scholarship.id))
        .filter(_published_fresh_clause(fresh_cutoff))
        .scalar()
        or 0
    )
    provider_count = (
        db.query(func.count(func.distinct(models.Scholarship.organization_id)))
        .filter(_active_not_archived(), models.Scholarship.organization_id.isnot(None))
        .scalar()
        or 0
    )
    last_catalog_verification_at = (
        db.query(func.max(models.Scholarship.last_verified_at))
        .filter(_active_not_archived(), models.Scholarship.last_verified_at.isnot(None))
        .scalar()
    )

    regions, levels = _collect_regions_and_levels(db)
    total_documented_funding_php = _maybe_total_documented_funding(db)

    return PublicStatsResponse(
        source="live",
        as_of=now,
        verification_fresh_days=VERIFICATION_FRESH_DAYS,
        verified_listing_count=int(verified_listing_count),
        provider_count=int(provider_count),
        last_catalog_verification_at=last_catalog_verification_at,
        region_count=len(regions),
        regions=sorted(regions),
        education_level_count=len(levels),
        education_levels=sorted(levels),
        total_documented_funding_php=total_documented_funding_php,
    )


def static_fallback_stats() -> PublicStatsResponse:
    """Honest empty fallback — no fabricated marketing figures."""
    return PublicStatsResponse(
        source="fallback",
        as_of=utc_now_naive(),
        verification_fresh_days=VERIFICATION_FRESH_DAYS,
    )


def assert_no_marketing_fabrication(payload: dict) -> None:
    """Guard: response must not carry invented social-proof fields."""
    for key in payload:
        assert key not in _FORBIDDEN_MARKETING_KEYS, f"forbidden marketing field: {key}"
