"""Per-row import validation and reporting for scholarship CSV/staging."""

from __future__ import annotations

from datetime import date
from typing import Any
from urllib.parse import urlparse

from pydantic import ValidationError

from app import schemas
from app.utils.dedupe import scholarship_dedupe_key
from app.utils.duplicate_candidates import find_duplicate_candidates


def _warn_missing(value: Any, field: str, warnings: list[str]) -> None:
    if value is None or (isinstance(value, str) and not value.strip()):
        warnings.append(f"missing_{field}")


def _warn_url(value: str | None, field: str, warnings: list[str]) -> None:
    if not value or not str(value).strip():
        return
    parsed = urlparse(str(value).strip())
    if parsed.scheme not in ("http", "https"):
        warnings.append(f"invalid_{field}_url")


def validate_import_row(
    row: dict[str, Any],
    *,
    live_dedupe_keys: set[str] | None = None,
    pending_dedupe_keys: set[str] | None = None,
) -> dict[str, Any]:
    """
    Validate one raw import row. Returns structured result for import reports.
    """
    live_dedupe_keys = live_dedupe_keys or set()
    pending_dedupe_keys = pending_dedupe_keys or set()
    warnings: list[str] = []
    title = (row.get("title") or "").strip()

    if not title:
        return {
            "status": "invalid",
            "title": title or None,
            "warnings": ["missing_title"],
            "error": "title is required",
        }

    try:
        sch = schemas.Scholarship.model_validate(row)
    except ValidationError as e:
        return {
            "status": "invalid",
            "title": title,
            "warnings": ["schema_validation_failed"],
            "error": str(e.errors()[0]["msg"]) if e.errors() else str(e),
        }

    _warn_missing(sch.application_deadline, "deadline", warnings)
    _warn_missing(sch.link, "application_link", warnings)
    _warn_missing(sch.provider, "provider", warnings)
    _warn_url(sch.link, "link", warnings)
    if sch.image_url:
        _warn_url(sch.image_url, "image", warnings)

    if sch.application_deadline and sch.application_deadline < date.today():
        warnings.append("deadline_in_past")

    if sch.application_open_date and sch.application_deadline:
        if sch.application_open_date > sch.application_deadline:
            warnings.append("open_date_after_deadline")

    # Normalization notes (informational)
    raw_type = row.get("scholarship_type")
    if isinstance(raw_type, str) and raw_type.strip().lower() in ("merit", "merit based", "academic"):
        warnings.append("normalized_scholarship_type:Merit-based")

    key = scholarship_dedupe_key(sch.title, sch.provider, sch.link)
    dup_candidates = find_duplicate_candidates(sch.title, sch.provider, sch.link)

    if key in pending_dedupe_keys:
        return {
            "status": "skipped",
            "title": sch.title,
            "provider": sch.provider,
            "dedupe_key": key,
            "warnings": warnings + ["duplicate_pending_staging"],
        }

    if key in live_dedupe_keys:
        return {
            "status": "updated_candidate",
            "title": sch.title,
            "provider": sch.provider,
            "dedupe_key": key,
            "warnings": warnings + ["duplicate_live_exact"],
            "duplicate_candidates": dup_candidates,
        }

    if dup_candidates:
        warnings.append("duplicate_candidate_detected")
        return {
            "status": "new",
            "title": sch.title,
            "provider": sch.provider,
            "dedupe_key": key,
            "warnings": warnings,
            "duplicate_candidates": dup_candidates,
        }

    return {
        "status": "new",
        "title": sch.title,
        "provider": sch.provider,
        "dedupe_key": key,
        "warnings": warnings,
    }


def summarize_import_report(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate per-row results into an import report."""
    summary = {
        "new": 0,
        "updated_candidate": 0,
        "skipped": 0,
        "invalid": 0,
    }
    for r in rows:
        status = r.get("status", "invalid")
        if status in summary:
            summary[status] += 1
        elif status == "created":
            summary["new"] += 1
    return {
        "imported": summary,
        "rows": rows,
        "total": len(rows),
    }
