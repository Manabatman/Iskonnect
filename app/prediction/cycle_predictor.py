"""
Scholarship cycle prediction - predicts when closed scholarships will reopen.
"""

import logging
from datetime import date

from app.matching.hard_filters import filter_scholarships
from app.serialization.scholarship import build_upcoming_scholarship_payload

logger = logging.getLogger(__name__)

_MAX_UPCOMING = 6


def _parse_date(val) -> date | None:
    """Parse date from string or date object."""
    if val is None:
        return None
    if isinstance(val, date):
        return val
    if isinstance(val, str):
        try:
            return date.fromisoformat(val.split("T")[0])
        except (ValueError, TypeError):
            return None
    return None


def predict_next_open(last_open_date: date, cycle_type: str) -> date | None:
    """
    Predict the next opening date based on cycle type.
    - annual: last_open + 1 year
    - semester: last_open + 6 months
    - rolling: returns today (always open) - caller should filter these out for upcoming
    """
    if not cycle_type or not last_open_date:
        return None
    ct = (cycle_type or "").strip().lower()
    if ct == "annual":
        return last_open_date.replace(year=last_open_date.year + 1)
    if ct == "semester":
        month = last_open_date.month + 6
        year = last_open_date.year + (month - 1) // 12
        month = ((month - 1) % 12) + 1
        return last_open_date.replace(year=year, month=month)
    if ct == "rolling":
        return date.today()
    return None


def get_upcoming_scholarships(
    profile: dict,
    scholarship_dicts: list[dict],
) -> list[dict]:
    """
    Return scholarships that pass hard filters and have a predicted future opening.
    Sorted by predicted_next_open ascending (soonest first). Limited to _MAX_UPCOMING.
    """
    today = date.today()
    candidates = [
        sch
        for sch in scholarship_dicts
        if sch.get("cycle_type") and _parse_date(sch.get("last_open_date"))
    ]
    if not candidates:
        return []

    filtered, _diag = filter_scholarships(profile, candidates)
    results = []
    for sch in filtered:
        last_open = _parse_date(sch.get("last_open_date"))
        cycle_type = sch.get("cycle_type")
        if not last_open or not cycle_type:
            continue
        predicted = predict_next_open(last_open, cycle_type)
        if predicted is None:
            continue
        if cycle_type.lower() == "rolling":
            continue
        if predicted <= today:
            continue
        last_close = _parse_date(sch.get("last_close_date"))
        last_open_str = last_open.isoformat() if last_open else None
        last_close_str = last_close.isoformat() if last_close else None
        predicted_str = predicted.isoformat() if predicted else None
        results.append(
            build_upcoming_scholarship_payload(
                sch,
                cycle={
                    "cycle_type": cycle_type,
                    "last_open_date": last_open_str,
                    "last_close_date": last_close_str,
                    "predicted_next_open": predicted_str,
                },
            )
        )
    results.sort(key=lambda r: r.get("predicted_next_open") or "")
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("cycle_predictor: upcoming count=%d", len(results[: _MAX_UPCOMING]))
    return results[:_MAX_UPCOMING]
