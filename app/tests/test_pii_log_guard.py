"""SEC-05: static guard for PII in logger calls."""

from __future__ import annotations

from pathlib import Path

from scripts.check_pii_logs import scan_file, scan_tree, statement_has_pii_violation

ROOT = Path(__file__).resolve().parents[2]


def test_statement_flags_raw_recipient_email():
    stmt = 'logger.info("email_sent to=%s subject=%s", to, subject)'
    assert statement_has_pii_violation(stmt) is True


def test_statement_allows_hashed_email():
    stmt = 'logger.warning("auth_login_failed user_hash=%s", hash(req.email) % 10_000)'
    assert statement_has_pii_violation(stmt) is False


def test_statement_allows_pii_safe_escape_hatch():
    stmt = 'logger.info("debug email=%s", email)  # pii-safe: local-only fixture'
    assert statement_has_pii_violation(stmt) is False


def test_scan_file_detects_violation_in_temp_content(tmp_path: Path):
    path = tmp_path / "sample.py"
    path.write_text(
        'import logging\nlogger = logging.getLogger(__name__)\n'
        'logger.info("leak to=%s", user.email)\n',
        encoding="utf-8",
    )
    hits = scan_file(path)
    assert len(hits) == 1
    assert hits[0][0] == 3


def test_app_tree_has_no_pii_logger_violations():
    findings = scan_tree(ROOT / "app")
    assert findings == [], "\n".join(
        f"{path.relative_to(ROOT)}:{line}: {snippet}" for path, line, snippet in findings
    )
