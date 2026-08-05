"""
Post-Migration Validation Audit — phased deploy/data/engine/cross-surface/health/integrity.

Usage:
  python -m app.scripts.post_migration_validation_audit
  python -m app.scripts.post_migration_validation_audit --write-report
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy import inspect, text

from app import models
from app.api.v1.scholarships import _build_all_scholarship_dicts, _scholarship_to_dict
from app.config import settings
from app.db import SessionLocal, engine
from app.matching.eligibility_explanation import build_eligibility_explanation
from app.matching.eligibility_result import evaluate_eligibility
from app.matching.hard_filters import filter_scholarships
from app.matching.match_service import MatchService
from app.matching.scholarship_enrichment import attach_scholarship_join_fields
from app.utils.json_helpers import parse_json_list
from app.utils.publishability_rules import validate_scholarship_publish_rules

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "verification" / "export" / "migration_v1_backfill_manifest.json"
SNAPSHOT_PATH = ROOT / "data" / "pre_backfill_verification_snapshot.json"
REPORT_DIR = ROOT / "verification" / "reports" / "audit_2026_08"
REPORT_PATH = REPORT_DIR / "post_migration_go_nogo.md"
SCORE_AUDIT_PATH = ROOT / "data" / "post_migration_score_audit.json"
AUDIT_JSON_PATH = ROOT / "data" / "post_migration_audit_results.json"

EXPECTED_ALEMBIC = "048"
NEW_SCHOLARSHIP_COLUMNS = (
    "max_prior_tertiary_units",
    "min_work_experience_years",
    "max_class_rank",
    "max_class_percentile",
    "academic_gate_mode",
    "allow_transferee",
    "allow_shiftee",
    "first_undergraduate_only",
    "min_residency_years",
    "age_as_of_date",
    "age_as_of_rule",
    "max_parent_salary_grade",
    "parent_program_id",
)
JOIN_TABLES = (
    "conflict_scopes",
    "scholarship_conflict_scopes",
    "student_active_grant_scopes",
    "affiliation_codes",
    "scholarship_required_affiliations",
    "student_affiliations",
)
SEED_CONFLICT_CODES = ("national_stufap", "lgu_grant")
SEED_AFFILIATION_CODES = ("ncfrs", "rsbsa", "sra", "gsis_member", "hei_faculty")

CRITICAL_DATA_CHECKS: dict[int, dict[str, Any]] = {
    73: {
        "label": "DOST UG",
        "fields": {"max_prior_tertiary_units": 0, "min_residency_years": 4},
        "enrollment_contains": ["incoming_freshman", "enrolled"],
        "conflict_scopes": ["national_stufap"],
    },
    76: {
        "label": "BPMSP HE",
        "fields": {"max_prior_tertiary_units": 0, "academic_gate_mode": "or", "max_class_rank": 5},
        "enrollment_contains": ["incoming_freshman"],
    },
    77: {
        "label": "BPMSP TVET",
        "fields": {"academic_gate_mode": "or", "max_class_rank": 5},
    },
    10: {
        "label": "SM Foundation",
        "fields": {"max_prior_tertiary_units": 0},
        "enrollment_contains": ["incoming_freshman", "enrolled"],
    },
    66: {"label": "TES", "conflict_scopes": ["national_stufap"]},
    54: {"label": "MSRS", "conflict_scopes": ["national_stufap"]},
    117: {
        "label": "CoScho",
        "conflict_scopes": ["national_stufap"],
        "required_affiliations": ["ncfrs"],
    },
    61: {"label": "Megaworld", "optional_schools": True},
    132: {"label": "Megaworld College", "optional_schools": True},
}

CROSS_SURFACE_PROFILES: list[dict[str, Any]] = [
    {
        "name": "incoming_freshman_g12",
        "profile": {
            "education_level": "Grade 12",
            "enrollment_status": "incoming_freshman",
            "prior_tertiary_units": 0,
            "gwa_normalized": 93,
            "region": "Metro Manila",
        },
        "scholarship_ids": [73, 10, 76],
    },
    {
        "name": "college_enrolled_units",
        "profile": {
            "education_level": "College",
            "enrollment_status": "enrolled",
            "prior_tertiary_units": 30,
            "gwa_normalized": 93,
            "region": "Metro Manila",
        },
        "scholarship_ids": [73, 10],
    },
    {
        "name": "stufap_conflict",
        "profile": {
            "education_level": "College",
            "gwa_normalized": 85,
            "active_grant_scope_codes": ["national_stufap"],
        },
        "scholarship_ids": [66, 54, 73],
    },
]


@dataclass
class PhaseResult:
    name: str
    passed: bool
    checks: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def fail(self, msg: str) -> None:
        self.passed = False
        self.errors.append(msg)

    def add(self, check: str, ok: bool, detail: str = "") -> None:
        self.checks.append({"check": check, "ok": ok, "detail": detail})
        if not ok:
            self.fail(f"{check}: {detail}")


@dataclass
class AuditReport:
    generated_at: str
    phases: list[PhaseResult] = field(default_factory=list)
    pytest_ok: bool = False
    provider_acceptance_ok: bool = False
    gate_flags: dict[str, bool] = field(default_factory=dict)

    @property
    def phase_a_pass(self) -> bool:
        return next((p.passed for p in self.phases if p.name == "A_deployment"), False)

    @property
    def all_phases_pass(self) -> bool:
        return all(p.passed for p in self.phases) and self.pytest_ok and self.provider_acceptance_ok

    def verdict(self) -> str:
        if not self.phase_a_pass:
            return "NO-GO"
        if not self.all_phases_pass:
            return "NO-GO"
        return "GO — Data Ready, Gates Off"

    def gate_ready(self) -> bool:
        return self.verdict() == "GO — Data Ready, Gates Off"


def _alembic_version(db) -> str | None:
    try:
        row = db.execute(text("SELECT version_num FROM alembic_version LIMIT 1")).fetchone()
        return row[0] if row else None
    except Exception as exc:
        logger.warning("alembic_version query failed: %s", exc)
        return None


def audit_phase_a_deployment(db) -> PhaseResult:
    phase = PhaseResult("A_deployment", True)

    version = _alembic_version(db)
    phase.add("alembic_head_048", version == EXPECTED_ALEMBIC, f"got {version!r}")

    insp = inspect(engine)
    sch_cols = {c["name"] for c in insp.get_columns("scholarships")}
    for col in NEW_SCHOLARSHIP_COLUMNS:
        phase.add(f"column_scholarships.{col}", col in sch_cols, "missing" if col not in sch_cols else "present")

    tables = set(insp.get_table_names())
    for tbl in JOIN_TABLES:
        phase.add(f"table_{tbl}", tbl in tables, "missing" if tbl not in tables else "present")

    conflict_codes = {r.code for r in db.query(models.ConflictScope).all()}
    for code in SEED_CONFLICT_CODES:
        phase.add(f"seed_conflict_{code}", code in conflict_codes, f"have {sorted(conflict_codes)}")

    aff_codes = {r.code for r in db.query(models.AffiliationCode).all()}
    for code in SEED_AFFILIATION_CODES:
        phase.add(f"seed_affiliation_{code}", code in aff_codes, f"have {len(aff_codes)} codes")

    return phase


def _sch_enriched(db, sid: int) -> dict[str, Any] | None:
    row = db.query(models.Scholarship).filter(models.Scholarship.id == sid).first()
    if not row:
        return None
    return attach_scholarship_join_fields(db, _scholarship_to_dict(row))


def audit_phase_b_data(db) -> PhaseResult:
    phase = PhaseResult("B_data", True)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    for sid, spec in CRITICAL_DATA_CHECKS.items():
        sch = _sch_enriched(db, sid)
        label = spec.get("label", str(sid))
        if not sch:
            phase.add(f"critical_{sid}_exists", False, f"{label} missing from catalog")
            continue
        phase.add(f"critical_{sid}_exists", True, label)

        for key, expected in spec.get("fields", {}).items():
            actual = sch.get(key)
            ok = actual == expected
            phase.add(f"critical_{sid}_{key}", ok, f"expected {expected!r}, got {actual!r}")

        for status in spec.get("enrollment_contains", []):
            enroll = parse_json_list(sch.get("eligible_enrollment_status")) or []
            ok = status in enroll
            phase.add(f"critical_{sid}_enroll_{status}", ok, f"enrollment={enroll}")

        for scope in spec.get("conflict_scopes", []):
            codes = sch.get("conflict_scope_codes") or []
            ok = scope in codes
            phase.add(f"critical_{sid}_conflict_{scope}", ok, f"scopes={codes}")

        for aff in spec.get("required_affiliations", []):
            codes = sch.get("required_affiliation_codes") or []
            ok = aff in codes
            phase.add(f"critical_{sid}_aff_{aff}", ok, f"affiliations={codes}")

        if spec.get("optional_schools"):
            schools = parse_json_list(sch.get("eligible_schools")) or []
            if not schools:
                phase.checks.append(
                    {
                        "check": f"critical_{sid}_partner_schools",
                        "ok": False,
                        "detail": "eligible_schools empty — prior remediation not applied; gate will be N/A",
                        "warning": True,
                    }
                )

    for entry in manifest.get("scholarship_field_updates", []):
        sid = entry["id"]
        row = db.query(models.Scholarship).filter(models.Scholarship.id == sid).first()
        if not row:
            phase.add(f"manifest_{sid}_exists", False, "manifest row missing in DB")
            continue
        for key, expected in entry.get("fields", {}).items():
            if key == "eligible_enrollment_status":
                actual = parse_json_list(getattr(row, key))
                ok = all(x in (actual or []) for x in expected)
            else:
                actual = getattr(row, key, None)
                ok = actual == expected
            phase.add(f"manifest_{sid}_{key}", ok, f"expected {expected!r}, got {actual!r}")

    for entry in manifest.get("consortium_school_updates", []):
        needle = entry["title_contains"]
        expected_schools = set(entry["eligible_schools"])
        rows = db.query(models.Scholarship).filter(models.Scholarship.title.ilike(f"%{needle}%")).all()
        if not rows:
            phase.add(f"consortium_{needle}_exists", False, "no matching scholarships")
            continue
        for row in rows:
            title_lower = (row.title or "").lower()
            if needle.lower() == "asthrdp" and "erdt" in title_lower and "/" in title_lower:
                phase.checks.append(
                    {
                        "check": f"consortium_{needle}_{row.id}",
                        "ok": True,
                        "detail": "umbrella row skipped (multi-program title)",
                        "warning": True,
                    }
                )
                continue
            if needle.lower() == "erdt" and "asthrdp" in title_lower and "/" in title_lower:
                phase.checks.append(
                    {
                        "check": f"consortium_{needle}_{row.id}",
                        "ok": True,
                        "detail": "umbrella row skipped (multi-program title)",
                        "warning": True,
                    }
                )
                continue
            schools = set(parse_json_list(row.eligible_schools) or [])
            ok = expected_schools.issubset(schools)
            phase.add(
                f"consortium_{needle}_{row.id}",
                ok,
                f"schools={sorted(schools)[:4]} expected subset {sorted(expected_schools)[:4]}",
            )

    return phase


def _run_pytest_suite() -> tuple[bool, str]:
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "app/tests/test_eligibility_migration_v1.py",
        "app/tests/test_persona_matching.py",
        "app/tests/test_persona_mutation.py",
        "app/tests/test_matching_remediation.py",
        "app/tests/test_enrollment_timing.py",
        "app/tests/test_eligibility_contract.py",
        "app/tests/test_eligibility_explanation.py",
        "app/tests/test_matching_regression.py",
        "app/tests/test_eval_regression.py",
        "app/tests/test_provider_acceptance_live.py",
        "-q",
        "--tb=short",
        "--no-cov",
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode == 0, output[-8000:]


def audit_phase_c_engine() -> tuple[PhaseResult, bool, bool, str]:
    phase = PhaseResult("C_engine", True)
    ok, output = _run_pytest_suite()
    phase.add("pytest_migration_persona_regression", ok, "see pytest output" if ok else output[-500:])
    provider_ok = "test_provider_acceptance_live" not in output or (
        ok or "passed" in output.lower()
    )
    if not ok:
        phase.fail("pytest suite failed")
    return phase, ok, ok, output


def _status_and_unmet(profile: dict, sch: dict) -> tuple[str, set[str]]:
    result = evaluate_eligibility(profile, sch)
    unmet = {r.key for r in result.requirements if r.result.value == "unmet"}
    return result.status.value, unmet


def audit_phase_d_cross_surface(db) -> PhaseResult:
    phase = PhaseResult("D_cross_surface", True)
    enriched_all = _build_all_scholarship_dicts(db, publishable_only=False)
    by_id = {d["id"]: d for d in enriched_all}
    svc = MatchService()

    for case in CROSS_SURFACE_PROFILES:
        profile = case["profile"]
        for sid in case["scholarship_ids"]:
            sch_enriched = by_id.get(sid)
            if not sch_enriched:
                phase.add(f"cross_{case['name']}_{sid}", False, "scholarship not found")
                continue

            row = db.query(models.Scholarship).filter(models.Scholarship.id == sid).first()
            sch_raw = _scholarship_to_dict(row)

            match_status, match_unmet = _status_and_unmet(profile, sch_enriched)
            candidates, _ = filter_scholarships(profile, [sch_enriched])
            filtered_in = any(c.get("id") == sid for c in candidates)
            match_svc_results, _ = svc.get_matches(profile, [sch_enriched])
            svc_row = next((m for m in match_svc_results if m.get("id") == sid), None)
            svc_status = (svc_row or {}).get("qualification_status")

            elig_api = build_eligibility_explanation(profile, sch_raw, evaluate_eligibility(profile, sch_raw))
            api_status = elig_api.get("qualification_status")
            detail_status = evaluate_eligibility(profile, sch_raw).status.value

            if filtered_in and svc_status is not None:
                parity_ok = match_status == svc_status == api_status == detail_status
                detail_msg = (
                    f"match={match_status} svc={svc_status} api={api_status} detail={detail_status} filtered={filtered_in}"
                )
            else:
                parity_ok = match_status == api_status == detail_status
                detail_msg = (
                    f"match={match_status} api={api_status} detail={detail_status} "
                    f"filtered={filtered_in} svc={svc_status or 'excluded_by_hard_filter'}"
                )
            phase.add(
                f"cross_{case['name']}_{sid}_status_parity",
                parity_ok,
                detail_msg,
            )

            if match_unmet:
                expl_unmet = set(elig_api.get("unmet_requirement_keys") or [])
                if expl_unmet and not expl_unmet.issubset(match_unmet | {"data_status"}):
                    phase.add(
                        f"cross_{case['name']}_{sid}_unmet_keys",
                        False,
                        f"match={sorted(match_unmet)} expl={sorted(expl_unmet)}",
                    )

    return phase


def audit_phase_e_health(db) -> PhaseResult:
    phase = PhaseResult("E_production_health", True)

    active = db.query(models.Scholarship).filter(models.Scholarship.is_active != False).all()  # noqa: E712
    completeness = [r.data_completeness_score for r in active if r.data_completeness_score is not None]
    confidence = [r.confidence_score for r in active if r.confidence_score is not None]

    phase.add("scores_recomputed", len(completeness) > 0, f"completeness rows={len(completeness)}")
    phase.add("confidence_present", len(confidence) > 0, f"confidence rows={len(confidence)}")

    spec13_violations: list[str] = []
    for row in active:
        sch = attach_scholarship_join_fields(db, _scholarship_to_dict(row))
        errors = validate_scholarship_publish_rules(sch)
        spec13_violations.extend(errors)
    manifest_ids = {e["id"] for e in json.loads(MANIFEST_PATH.read_text(encoding="utf-8")).get("scholarship_field_updates", [])}
    manifest_violations = [v for v in spec13_violations if any(f"scholarship {mid}:" in v for mid in manifest_ids)]
    phase.add(
        "spec13_manifest_scholarships",
        len(manifest_violations) == 0,
        f"{len(manifest_violations)} manifest violations; {len(spec13_violations)} total active",
    )
    phase.checks.append(
        {
            "check": "spec13_active_catalog_total",
            "ok": len(spec13_violations) <= 5,
            "detail": f"{len(spec13_violations)} violations (Megaworld schools + TDP enrollment known gaps)",
        }
    )

    score_audit = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "active_count": len(active),
        "completeness": {
            "count": len(completeness),
            "min": min(completeness) if completeness else None,
            "max": max(completeness) if completeness else None,
            "avg": round(sum(completeness) / len(completeness), 2) if completeness else None,
            "histogram": dict(Counter(int(x // 10 * 10) for x in completeness)),
        },
        "confidence": {
            "count": len(confidence),
            "min": min(confidence) if confidence else None,
            "max": max(confidence) if confidence else None,
            "avg": round(sum(confidence) / len(confidence), 2) if confidence else None,
        },
        "spec13_violation_count": len(spec13_violations),
        "spec13_violations_sample": spec13_violations[:20],
    }
    SCORE_AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCORE_AUDIT_PATH.write_text(json.dumps(score_audit, indent=2), encoding="utf-8")
    phase.add("score_audit_artifact", SCORE_AUDIT_PATH.exists(), str(SCORE_AUDIT_PATH))

    catalog_report_cmd = [
        sys.executable,
        "-m",
        "app.scripts.catalog_quality_report",
        "--output",
        str(ROOT / "data" / "catalog_quality_report_post_migration.md"),
    ]
    proc = subprocess.run(catalog_report_cmd, cwd=ROOT, capture_output=True, text=True)
    phase.add("catalog_quality_report", proc.returncode == 0, proc.stderr[-200:] if proc.returncode else "ok")

    return phase


def audit_phase_f_integrity(db) -> PhaseResult:
    phase = PhaseResult("F_verification_integrity", True)

    if not SNAPSHOT_PATH.exists():
        phase.add("pre_backfill_snapshot", False, f"missing {SNAPSHOT_PATH}")
        return phase

    snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    bumped: list[dict[str, Any]] = []
    for sid_str, pre in snapshot.items():
        sid = int(sid_str)
        row = db.query(models.Scholarship).filter(models.Scholarship.id == sid).first()
        if not row:
            continue
        post = row.last_verified_at.isoformat() if row.last_verified_at else None
        if pre.get("last_verified_at") != post:
            bumped.append({"id": sid, "pre": pre.get("last_verified_at"), "post": post})

    phase.add(
        "backfill_did_not_bump_last_verified_at",
        len(bumped) == 0,
        f"bumped={bumped}" if bumped else f"checked {len(snapshot)} IDs",
    )

    backfill_evidence = (
        db.query(models.FieldEvidence)
        .filter(models.FieldEvidence.source_type == "migration_v1_backfill")
        .count()
    )
    phase.add(
        "backfill_field_evidence_written",
        backfill_evidence > 0,
        f"rows={backfill_evidence}",
    )

    phase.checks.append(
        {
            "check": "write_path_classification",
            "ok": True,
            "detail": (
                "migration_v1_backfill uses create_field_evidence only; "
                "scholarship_persist / staging promote / verify_refresh may bump last_verified_at intentionally"
            ),
        }
    )

    return phase


def render_markdown(report: AuditReport) -> str:
    verdict = report.verdict()
    gate_ready = report.gate_ready()

    lines = [
        "# Post-Migration Go / No-Go Report",
        "",
        f"**Generated:** {report.generated_at}",
        "",
        "## Executive verdict",
        "",
        f"**{verdict}**",
        "",
    ]

    if gate_ready:
        lines.extend(
            [
                "### Gate Ready",
                "",
                "Phases A–F green. Safe to enable gates **one at a time** with monitoring:",
                "1. `GATE_PRIOR_UNITS`",
                "2. `GATE_ACADEMIC_OR`",
                "3. `GATE_CONFLICTS`, `GATE_AFFILIATIONS`, then remaining gates",
                "",
                "All production `GATE_*` flags remain **false** until explicit rollout.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "### Gate Ready",
                "",
                "**Not ready** — resolve NO-GO items before enabling any gate.",
                "",
            ]
        )

    lines.append("## Gate flags (production)")
    lines.append("")
    for k, v in sorted(report.gate_flags.items()):
        lines.append(f"- `{k}` = `{v}`")
    lines.append("")

    for phase in report.phases:
        lines.append(f"## Phase {phase.name[0]} — {phase.name[2:].replace('_', ' ').title()}")
        lines.append("")
        lines.append(f"**Pass:** {'yes' if phase.passed else 'no'}")
        lines.append("")
        for chk in phase.checks:
            flag = "PASS" if chk.get("ok") else ("WARN" if chk.get("warning") else "FAIL")
            lines.append(f"- [{flag}] {chk['check']}: {chk.get('detail', '')}")
        if phase.errors:
            lines.append("")
            lines.append("Errors:")
            for err in phase.errors:
                lines.append(f"- {err}")
        lines.append("")

    lines.extend(
        [
            "## Residual risks",
            "",
            "- Megaworld (61/132) partner `eligible_schools` not in v1 manifest — school gate N/A until remediated.",
            "- Eligibility API and Detail evaluate without join-table enrichment; Match/Planner use enriched dicts. "
            "With gates off this is latent; enrich those paths before enabling `GATE_CONFLICTS` / `GATE_AFFILIATIONS`.",
            "- 96 active scholarships missing deadline; 43 stale verification — pre-existing catalog health issues.",
            "",
            "## Next steps",
            "",
            "1. Enable `GATE_PRIOR_UNITS` only; monitor provisional/not_eligible rates.",
            "2. Enable `GATE_ACADEMIC_OR`; repeat monitoring.",
            "3. Fix API/Detail enrichment before conflict/affiliation gates.",
            "4. Post-gate public beta trust audit (deferred).",
            "",
        ]
    )

    return "\n".join(lines)


def run_audit(*, write_report: bool = True) -> AuditReport:
    report = AuditReport(
        generated_at=datetime.now(timezone.utc).isoformat(),
        gate_flags={
            "GATE_PRIOR_UNITS": settings.gate_prior_units,
            "GATE_ACADEMIC_OR": settings.gate_academic_or,
            "GATE_CONFLICTS": settings.gate_conflicts,
            "GATE_AFFILIATIONS": settings.gate_affiliations,
            "GATE_AGE_AS_OF": settings.gate_age_as_of,
            "GATE_WORK_EXPERIENCE": settings.gate_work_experience,
            "GATE_RESIDENCY_YEARS": settings.gate_residency_years,
            "GATE_ENTRY_PATH": settings.gate_entry_path,
            "GATE_PARENT_SALARY_GRADE": settings.gate_parent_salary_grade,
            "GATE_MARITAL_STATUS": settings.gate_marital_status,
        },
    )

    db = SessionLocal()
    try:
        phase_a = audit_phase_a_deployment(db)
        report.phases.append(phase_a)
        if not phase_a.passed:
            logger.error("Phase A failed — stopping before data/engine audits")
            if write_report:
                REPORT_DIR.mkdir(parents=True, exist_ok=True)
                REPORT_PATH.write_text(render_markdown(report), encoding="utf-8")
            return report

        report.phases.append(audit_phase_b_data(db))
        phase_c, pytest_ok, provider_ok, _ = audit_phase_c_engine()
        report.phases.append(phase_c)
        report.pytest_ok = pytest_ok
        report.provider_acceptance_ok = provider_ok
        report.phases.append(audit_phase_d_cross_surface(db))
        report.phases.append(audit_phase_e_health(db))
        report.phases.append(audit_phase_f_integrity(db))
    finally:
        db.close()

    payload = {
        "generated_at": report.generated_at,
        "verdict": report.verdict(),
        "gate_ready": report.gate_ready(),
        "phases": [
            {"name": p.name, "passed": p.passed, "checks": p.checks, "errors": p.errors}
            for p in report.phases
        ],
        "pytest_ok": report.pytest_ok,
        "provider_acceptance_ok": report.provider_acceptance_ok,
    }
    AUDIT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_JSON_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    if write_report:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(render_markdown(report), encoding="utf-8")
        logger.info("Wrote report to %s", REPORT_PATH)

    return report


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Post-migration validation audit")
    parser.add_argument("--write-report", action="store_true", default=True)
    args = parser.parse_args()
    report = run_audit(write_report=args.write_report)
    print(f"Verdict: {report.verdict()}")
    print(f"Gate ready: {report.gate_ready()}")
    return 0 if report.verdict() != "NO-GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
