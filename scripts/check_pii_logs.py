#!/usr/bin/env python3
"""SEC-05 — fail CI when logger calls reference PII fields without a # pii-safe: escape."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "app"
EXCLUDE_DIRS = {"tests", "__pycache__", ".pytest_cache"}

LOGGER_START = re.compile(r"\blogger\.(?:info|warning|error|debug|exception)\s*\(")
PII_SAFE = re.compile(r"#\s*pii-safe:")

# Argument expressions that must not appear in logger calls (after stripping string literals).
UNSAFE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bto=%s\b"),
    re.compile(r",\s*to\s*,"),
    re.compile(r",\s*to\s*\)"),
    re.compile(r"\b(?:email|password|full_name|household_income|birth_date|refresh_token|reset_token)\s*="),
    re.compile(r"f[\"'][^\"']*\{(?:email|password|full_name|household_income|birth_date|refresh_token|reset_token)\}"),
)

PII_ATTR = re.compile(
    r"\.(?:email|password|full_name|household_income|birth_date|refresh_token|reset_token)\b"
)


def _inside_hash_call(text_before: str) -> bool:
    pos = text_before.rfind("hash(")
    if pos == -1:
        return False
    segment = text_before[pos:]
    return segment.count("(") > segment.count(")")


def _strip_string_literals(source: str) -> str:
    return re.sub(r'(["\'])(?:\\.|(?!\1).)*\1', '""', source)


def _iter_logger_statements(lines: list[str]):
    i = 0
    while i < len(lines):
        if LOGGER_START.search(lines[i]):
            start = i + 1
            chunk = [lines[i]]
            balance = lines[i].count("(") - lines[i].count(")")
            i += 1
            while balance > 0 and i < len(lines):
                chunk.append(lines[i])
                balance += lines[i].count("(") - lines[i].count(")")
                i += 1
            yield start, "\n".join(chunk)
        else:
            i += 1


def statement_has_pii_violation(statement: str) -> bool:
    if PII_SAFE.search(statement):
        return False

    stripped = _strip_string_literals(statement)

    for pattern in UNSAFE_PATTERNS:
        if pattern.search(stripped):
            return True

    for match in PII_ATTR.finditer(stripped):
        if match.group(0) == ".password" and "hash_password(" in stripped:
            continue
        if _inside_hash_call(stripped[: match.start()]):
            continue
        return True

    return False


def scan_file(path: Path) -> list[tuple[int, str]]:
    text = path.read_text(encoding="utf-8")
    violations: list[tuple[int, str]] = []
    for line_no, statement in _iter_logger_statements(text.splitlines()):
        if statement_has_pii_violation(statement):
            violations.append((line_no, statement.strip().replace("\n", " ")[:160]))
    return violations


def scan_tree(root: Path = APP_DIR) -> list[tuple[Path, int, str]]:
    findings: list[tuple[Path, int, str]] = []
    for path in sorted(root.rglob("*.py")):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        for line_no, snippet in scan_file(path):
            findings.append((path, line_no, snippet))
    return findings


def main() -> int:
    findings = scan_tree()
    if not findings:
        print("SEC-05: no PII references in logger calls.")
        return 0

    for path, line_no, snippet in findings:
        rel = path.relative_to(ROOT)
        print(f"{rel}:{line_no}: {snippet}")
    print(
        f"\nSEC-05: {len(findings)} logger call(s) reference PII fields. "
        "Redact values or add `# pii-safe:` with justification."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
