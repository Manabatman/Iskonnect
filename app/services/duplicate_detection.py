"""Detect potential duplicate scholarship pairs for admin review."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app import models
from app.utils.duplicate_candidates import find_duplicate_candidates


def _scholarship_catalog(db: Session, *, include_inactive: bool) -> list[dict]:
    q = db.query(models.Scholarship)
    if not include_inactive:
        q = q.filter(models.Scholarship.is_active == True)  # noqa: E712
    rows = q.order_by(models.Scholarship.id).all()
    return [
        {
            "id": s.id,
            "title": s.title,
            "provider": s.provider,
            "link": s.link,
            "dedupe_key": s.dedupe_key,
            "is_active": s.is_active,
        }
        for s in rows
    ]


def _pair_key(a_id: int, b_id: int) -> tuple[int, int]:
    return (min(a_id, b_id), max(a_id, b_id))


def find_duplicate_pairs(
    db: Session,
    *,
    min_confidence: float = 0.85,
    include_inactive: bool = True,
) -> list[dict]:
    """Return deduplicated pairs with match signals for admin review."""
    catalog = _scholarship_catalog(db, include_inactive=include_inactive)
    by_id = {item["id"]: item for item in catalog}
    seen: set[tuple[int, int]] = set()
    pairs: list[dict] = []

    # Exact dedupe_key collisions
    key_groups: dict[str, list[dict]] = {}
    for item in catalog:
        key = item.get("dedupe_key")
        if not key:
            continue
        key_groups.setdefault(key, []).append(item)
    for key, group in key_groups.items():
        if len(group) < 2:
            continue
        for i, a in enumerate(group):
            for b in group[i + 1 :]:
                pk = _pair_key(a["id"], b["id"])
                if pk in seen:
                    continue
                seen.add(pk)
                pairs.append(
                    {
                        "id_a": a["id"],
                        "id_b": b["id"],
                        "title_a": a["title"],
                        "title_b": b["title"],
                        "provider_a": a.get("provider"),
                        "provider_b": b.get("provider"),
                        "link_a": a.get("link"),
                        "link_b": b.get("link"),
                        "confidence": 1.0,
                        "match_reason": "dedupe_key",
                        "dedupe_key": key,
                        "is_active_a": a.get("is_active"),
                        "is_active_b": b.get("is_active"),
                    }
                )

    # Fuzzy title/provider/link matches
    for item in catalog:
        others = [o for o in catalog if o["id"] != item["id"]]
        candidates = find_duplicate_candidates(
            item["title"] or "",
            item.get("provider"),
            item.get("link"),
            known=others,
            threshold=min_confidence,
        )
        for cand in candidates:
            other_id = cand.get("scholarship_id")
            if other_id is None:
                continue
            pk = _pair_key(item["id"], int(other_id))
            if pk in seen:
                continue
            seen.add(pk)
            other = by_id.get(int(other_id), {})
            pairs.append(
                {
                    "id_a": pk[0],
                    "id_b": pk[1],
                    "title_a": by_id[pk[0]]["title"],
                    "title_b": by_id[pk[1]]["title"],
                    "provider_a": by_id[pk[0]].get("provider"),
                    "provider_b": by_id[pk[1]].get("provider"),
                    "link_a": by_id[pk[0]].get("link"),
                    "link_b": by_id[pk[1]].get("link"),
                    "confidence": cand.get("confidence", 0),
                    "match_reason": cand.get("match_reason", "similar_title"),
                    "dedupe_key": None,
                    "is_active_a": by_id[pk[0]].get("is_active"),
                    "is_active_b": by_id[pk[1]].get("is_active"),
                }
            )

    pairs.sort(key=lambda p: (-float(p["confidence"]), p["id_a"], p["id_b"]))
    return pairs


def count_dedupe_key_collisions(db: Session) -> int:
    from sqlalchemy import func

    rows = (
        db.query(models.Scholarship.dedupe_key)
        .filter(models.Scholarship.dedupe_key.isnot(None))
        .group_by(models.Scholarship.dedupe_key)
        .having(func.count(models.Scholarship.id) > 1)
        .all()
    )
    return len(rows)
