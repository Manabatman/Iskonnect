"""Fuzzy duplicate candidate detection for scholarship imports."""

from __future__ import annotations

import re
import unicodedata


def _normalize_title(title: str) -> str:
    t = unicodedata.normalize("NFKD", title or "")
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.lower().strip()
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t)
    # Strip common year/cycle suffixes
    t = re.sub(r"\b(20\d{2}|sy\s*20\d{2}[-/]20\d{2}|academic year \d{4})\b", "", t).strip()
    return t


def _token_set_ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    ta = set(a.split())
    tb = set(b.split())
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    return (2.0 * inter) / (len(ta) + len(tb))


def find_duplicate_candidates(
    title: str,
    provider: str | None,
    link: str | None,
    *,
    known: list[dict] | None = None,
    threshold: float = 0.85,
) -> list[dict]:
    """
    Return candidate matches from known scholarships (title, provider, id, link, score).
    known: list of dicts with at least title, provider, id, link keys.
    """
    if not known:
        return []
    norm_title = _normalize_title(title)
    norm_provider = (provider or "").strip().lower()
    norm_link = (link or "").strip().lower()
    candidates: list[dict] = []
    for item in known:
        other_title = _normalize_title(item.get("title") or "")
        other_provider = (item.get("provider") or "").strip().lower()
        other_link = (item.get("link") or "").strip().lower()
        title_score = _token_set_ratio(norm_title, other_title)
        provider_match = bool(norm_provider and other_provider and norm_provider == other_provider)
        link_match = bool(norm_link and other_link and norm_link == other_link)
        score = title_score
        if provider_match:
            score = min(1.0, score + 0.15)
        if link_match:
            score = 1.0
        if score >= threshold or (provider_match and title_score >= 0.7):
            candidates.append(
                {
                    "scholarship_id": item.get("id"),
                    "title": item.get("title"),
                    "provider": item.get("provider"),
                    "link": item.get("link"),
                    "confidence": round(score, 3),
                    "match_reason": "exact_link" if link_match else ("title_provider" if provider_match else "similar_title"),
                }
            )
    candidates.sort(key=lambda x: -x["confidence"])
    return candidates[:5]


def merge_confidence(score: float) -> str:
    """Classify whether auto-merge would be safe."""
    if score >= 0.98:
        return "high"
    if score >= 0.85:
        return "medium"
    return "low"
