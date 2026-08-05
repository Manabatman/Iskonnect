"""Tests for audit_remediation orchestrator."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_remediation_manifest_exists():
    path = ROOT / "verification" / "reports" / "audit_2026_08" / "remediation_manifest.json"
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert "merge_pairs" in data
    assert data["merge_pairs"]["1"] == 129


def test_audit_remediation_dry_run():
    from app.scripts.audit_remediation import run_remediation

    report = run_remediation(apply=False, phases=["validate"])
    assert "active_count" in report.validation
    assert report.dry_run is True
