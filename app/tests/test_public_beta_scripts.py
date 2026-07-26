"""Tests for approve_staging_batch and run_verification_bundle helpers."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def test_master_index_lists_pending_bundles():
    from app.scripts.run_verification_bundle import _load_pending_bundle_ids

    pending = _load_pending_bundle_ids()
    assert "tesda" in pending
    assert "ched_unifast" not in pending
    assert "dost" not in pending
    assert len(pending) == 13


def test_bundle_scholarship_ids_from_export():
    from app.scripts.run_verification_bundle import _bundle_scholarship_ids

    ids = _bundle_scholarship_ids("tesda")
    assert ids == [4, 77]


def test_tesda_field_changes_report_exists():
    path = ROOT / "verification" / "reports" / "tesda" / "field_changes.csv"
    assert path.exists()
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert rows
    assert all(r["field"] == "link_status" for r in rows)


def test_approve_staging_batch_dry_run():
    from app.scripts.approve_staging_batch import run

    summary = run(apply=False)
    assert "pending" in summary
    assert "approved" in summary
