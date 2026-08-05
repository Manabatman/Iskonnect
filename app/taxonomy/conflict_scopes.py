"""Conflict scope catalog — grant exclusivity rules."""

from __future__ import annotations

NATIONAL_STUFAP = "national_stufap"
LGU_GRANT = "lgu_grant"

DEFAULT_CONFLICT_SCOPES: tuple[tuple[str, str, str], ...] = (
    (NATIONAL_STUFAP, "National StuFAP / government grant", "Cannot hold another national government scholarship"),
    (LGU_GRANT, "LGU scholarship", "Cannot hold another LGU scholarship from a different locality"),
)
