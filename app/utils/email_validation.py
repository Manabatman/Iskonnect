"""Shared email validation for auth endpoints (P1-06)."""

from __future__ import annotations

import re

EMAIL_RE = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$"
)


def validate_email_format(email: str) -> None:
    trimmed = (email or "").strip()
    if not trimmed or "@" not in trimmed:
        raise ValueError("Enter a valid email address.")
    local, _, domain = trimmed.partition("@")
    if not local or not domain or len(local) > 64 or len(trimmed) > 254:
        raise ValueError("Enter a valid email address.")
    if ".." in local or ".." in domain:
        raise ValueError("Email cannot contain consecutive dots.")
    if not EMAIL_RE.match(trimmed):
        raise ValueError("Enter a valid email address.")
