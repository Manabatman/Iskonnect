"""Load join-table eligibility data onto scholarship dicts for matching."""

from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app import models


def attach_scholarship_join_fields(db: Session, sch_dict: dict[str, Any]) -> dict[str, Any]:
    """Attach required affiliations and conflict scopes from relational tables."""
    sid = sch_dict.get("id")
    if not sid:
        return sch_dict
    aff = (
        db.query(models.AffiliationCode.code)
        .join(
            models.ScholarshipRequiredAffiliation,
            models.ScholarshipRequiredAffiliation.affiliation_id == models.AffiliationCode.id,
        )
        .filter(models.ScholarshipRequiredAffiliation.scholarship_id == sid)
        .all()
    )
    scopes = (
        db.query(models.ConflictScope.code)
        .join(
            models.ScholarshipConflictScope,
            models.ScholarshipConflictScope.scope_id == models.ConflictScope.id,
        )
        .filter(models.ScholarshipConflictScope.scholarship_id == sid)
        .all()
    )
    out = dict(sch_dict)
    if aff:
        out["required_affiliation_codes"] = [r[0] for r in aff if r[0]]
    if scopes:
        out["conflict_scope_codes"] = [r[0] for r in scopes if r[0]]
    return out


def enrich_scholarship_dicts(db: Session, dicts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Batch-enrich scholarship dicts with join-table fields."""
    if not dicts:
        return dicts
    ids = [d["id"] for d in dicts if d.get("id")]
    if not ids:
        return dicts

    aff_map: dict[int, list[str]] = {i: [] for i in ids}
    scope_map: dict[int, list[str]] = {i: [] for i in ids}

    aff_rows = (
        db.query(models.ScholarshipRequiredAffiliation.scholarship_id, models.AffiliationCode.code)
        .join(
            models.AffiliationCode,
            models.AffiliationCode.id == models.ScholarshipRequiredAffiliation.affiliation_id,
        )
        .filter(models.ScholarshipRequiredAffiliation.scholarship_id.in_(ids))
        .all()
    )
    for sid, code in aff_rows:
        if code:
            aff_map.setdefault(sid, []).append(code)

    scope_rows = (
        db.query(models.ScholarshipConflictScope.scholarship_id, models.ConflictScope.code)
        .join(
            models.ConflictScope,
            models.ConflictScope.id == models.ScholarshipConflictScope.scope_id,
        )
        .filter(models.ScholarshipConflictScope.scholarship_id.in_(ids))
        .all()
    )
    for sid, code in scope_rows:
        if code:
            scope_map.setdefault(sid, []).append(code)

    out: list[dict[str, Any]] = []
    for d in dicts:
        row = dict(d)
        sid = row.get("id")
        if sid in aff_map and aff_map[sid]:
            row["required_affiliation_codes"] = aff_map[sid]
        if sid in scope_map and scope_map[sid]:
            row["conflict_scope_codes"] = scope_map[sid]
        out.append(row)
    return out
