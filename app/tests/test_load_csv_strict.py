"""Tests for strict CSV structural validation (load_csv_strict)."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from app.scripts.import_scholarships import load_csv_strict
from app.utils.import_contract import CANONICAL_IMPORT_COLUMNS
from app.utils.import_validation import summarize_import_report


def _write_csv(tmp_path: Path, content: str) -> str:
    path = tmp_path / "test.csv"
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
    return str(path)


def _minimal_valid_row(**overrides: str) -> str:
    """One valid data row with all 39 canonical columns (mostly empty)."""
    values = {col: "" for col in CANONICAL_IMPORT_COLUMNS}
    values["title"] = "Test Scholarship"
    values.update(overrides)
    return ",".join(values[col] for col in CANONICAL_IMPORT_COLUMNS)


def test_load_csv_strict_valid_minimal_row(tmp_path):
    header = ",".join(CANONICAL_IMPORT_COLUMNS)
    row = _minimal_valid_row(provider="Test Provider")
    path = _write_csv(tmp_path, f"{header}\n{row}")
    rows, structural = load_csv_strict(path)
    assert structural["header_valid"] is True
    assert len(rows) == 1
    assert rows[0]["title"] == "Test Scholarship"
    assert rows[0]["provider"] == "Test Provider"
    assert structural["valid_row_count"] == 1
    assert structural["rejected_rows"] == []


def test_load_csv_strict_rejects_short_row_column_count_mismatch(tmp_path):
    header = "title,provider,eligible_cities,residency_required"
    # Missing empty eligible_cities field — would left-shift residency_required
    row = "Test Scholarship,Pasig City,true"
    path = _write_csv(tmp_path, f"{header}\n{row}")
    rows, structural = load_csv_strict(path)
    assert rows == []
    assert len(structural["rejected_rows"]) == 1
    rejection = structural["rejected_rows"][0]
    assert rejection["status"] == "rejected_structural"
    assert rejection["line"] == 2
    assert "column_count_mismatch" in rejection["reason"]
    assert "expected 4, got 3" in rejection["reason"]


def test_load_csv_strict_accepts_row_with_empty_middle_field(tmp_path):
    header = "title,provider,eligible_cities,residency_required"
    row = "Test Scholarship,Pasig City,,true"
    path = _write_csv(tmp_path, f"{header}\n{row}")
    rows, structural = load_csv_strict(path)
    assert len(rows) == 1
    assert rows[0]["eligible_cities"] is None
    assert rows[0]["residency_required"] == "true"
    assert structural["rejected_rows"] == []


def test_load_csv_strict_rejects_long_row(tmp_path):
    header = "title,provider"
    row = "Test,Provider,extra"
    path = _write_csv(tmp_path, f"{header}\n{row}")
    rows, structural = load_csv_strict(path)
    assert rows == []
    assert "column_count_mismatch" in structural["rejected_rows"][0]["reason"]
    assert "expected 2, got 3" in structural["rejected_rows"][0]["reason"]


def test_load_csv_strict_unknown_column_aborts(tmp_path):
    header = "title,provider,unknown_column_xyz"
    row = "Test,Provider,x"
    path = _write_csv(tmp_path, f"{header}\n{row}")
    rows, structural = load_csv_strict(path)
    assert rows == []
    assert structural["header_valid"] is False
    assert "unknown_column_xyz" in structural["unknown_columns"]


def test_load_csv_strict_missing_required_title_aborts(tmp_path):
    header = "provider,link"
    row = "Provider,https://example.com"
    path = _write_csv(tmp_path, f"{header}\n{row}")
    rows, structural = load_csv_strict(path)
    assert rows == []
    assert structural["header_valid"] is False
    assert "title" in structural["missing_columns"]


def test_load_csv_strict_empty_file(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")
    rows, structural = load_csv_strict(str(path))
    assert rows == []
    assert structural["header_valid"] is False
    assert any("empty_file" in e for e in structural["header_errors"])


def test_summarize_import_report_includes_structural_metadata():
    rows = [
        {"status": "rejected_structural", "line": 2, "reason": "column_count_mismatch (expected 39, got 38)"},
        {"status": "created", "warnings": ["normalized_scholarship_type:Merit-based", "invalid_link_url"]},
    ]
    structural = {
        "header_valid": True,
        "rejected_rows": [rows[0]],
        "unknown_columns": [],
        "missing_columns": [],
        "missing_recommended": ["provider"],
    }
    report = summarize_import_report(rows, structural=structural)
    assert report["rejected_structural"] == 1
    assert report["missing_recommended"] == ["provider"]
    assert report["invalid_urls"] == 1
    assert "normalized_scholarship_type:Merit-based" in report["auto_normalizations"]
    assert report["imported"]["rejected_structural"] == 1
