"""Load join-table eligibility data onto profile dicts for matching."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app import models
from app.taxonomy.affiliations import profile_affiliation_codes


def enrich_profile_dict(profile: dict, db: Session | None = None) -> dict:
    """Attach affiliation codes and active grant scopes from DB when session available."""
    out = dict(profile)
    codes = profile_affiliation_codes(out)
    if db is not None and out.get("id"):
        rows = (
            db.query(models.AffiliationCode.code)
            .join(
                models.StudentAffiliation,
                models.StudentAffiliation.affiliation_id == models.AffiliationCode.id,
            )
            .filter(models.StudentAffiliation.student_id == out["id"])
            .all()
        )
        codes.update(r[0] for r in rows if r[0])
        scope_rows = (
            db.query(models.ConflictScope.code)
            .join(
                models.StudentActiveGrantScope,
                models.StudentActiveGrantScope.scope_id == models.ConflictScope.id,
            )
            .filter(models.StudentActiveGrantScope.student_id == out["id"])
            .all()
        )
        out["active_grant_scope_codes"] = [r[0] for r in scope_rows if r[0]]
    out["affiliation_codes"] = sorted(codes)
    return out
