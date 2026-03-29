"""
Shared JSON list parsing for API/ORM string fields (JSON array or legacy comma-separated).
"""

from __future__ import annotations

import json
from typing import Any


def parse_json_list(val: str | list | None, default: list | None = None) -> list:
    """
    Parse a JSON array from a string, accept list as-is, or split comma-separated strings.
    Returns `default` or [] when empty/invalid (never None for default=[] callers).
    """
    if val is None:
        return list(default) if default is not None else []
    if isinstance(val, list):
        return [str(x).strip() for x in val if x]
    if isinstance(val, str):
        try:
            parsed = json.loads(val)
            return [str(x).strip() for x in parsed if x] if isinstance(parsed, list) else []
        except (json.JSONDecodeError, TypeError):
            return [x.strip() for x in val.split(",") if x.strip()]
    return list(default) if default is not None else []


def parse_json(val: Any, default: list | None = None) -> list:
    """
    Parse JSON list from ORM field; fallback to comma-split. Used for profile list fields.
    """
    if val is None:
        return default if default is not None else []
    if isinstance(val, list):
        return val
    if isinstance(val, str):
        try:
            p = json.loads(val)
            return p if isinstance(p, list) else (default or [])
        except (json.JSONDecodeError, TypeError):
            return [x.strip() for x in val.split(",") if x.strip()] or (default or [])
    return default or []
