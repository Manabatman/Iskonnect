# Eligibility Migration v1 — Production Rollout

## Per-gate feature flags (default: off)

Enable independently after staging soak. Set in environment:

| Flag | Purpose |
|------|---------|
| `GATE_PRIOR_UNITS` | Zero-unit / max prior tertiary units gate |
| `GATE_ACADEMIC_OR` | GWA/rank OR academic gate via `academic_gate_mode` |
| `GATE_CONFLICTS` | Grant exclusivity via `conflict_scope_codes` |
| `GATE_AFFILIATIONS` | Required registry/equity affiliations |
| `GATE_AGE_AS_OF` | Birthdate-relative age rules |
| `GATE_WORK_EXPERIENCE` | Minimum work experience |
| `GATE_MARITAL_STATUS` | Marital status requirements |
| `GATE_RESIDENCY_YEARS` | Municipal residency duration |
| `GATE_ENTRY_PATH` | Transferee/shiftee/first-UG bars |
| `GATE_PARENT_SALARY_GRADE` | Parent salary grade caps |
| `PUBLISHABILITY_RULE_VALIDATION` | SPEC-13 publish guards (default: on) |

## Rollout sequence

1. **Phase 0** — Run audit remediation + migration v1 backfill:
   ```bash
   python -m app.scripts.audit_remediation --apply
   python -m app.scripts.migration_v1_backfill --apply
   ```
2. **Schema** — `alembic upgrade head` (migration `048`)
3. **Staging** — Enable gates one at a time; monitor provisional rate and FP/FN personas in CI
4. **Production** — Enable `GATE_PRIOR_UNITS` and `GATE_ACADEMIC_OR` first (highest FP impact)
5. **Rollback** — Disable gate flag; no schema rollback required

## Monitoring

- Track `provisionally_qualified` share in match runs
- Watch admin publish rejections from `validate_scholarship_publish_rules`
- Persona CI gates in `app/tests/test_eligibility_migration_v1.py`

## Acceptance checklist

Frozen rule-class inventory: `verification/export/canonical_rule_class_inventory.json`
