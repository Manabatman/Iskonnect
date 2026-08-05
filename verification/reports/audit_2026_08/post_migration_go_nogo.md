# Post-Migration Go / No-Go Report

**Generated:** 2026-08-05T13:24:23.138382+00:00

## Executive verdict

**GO — Data Ready, Gates Off**

### Gate Ready

Phases A–F green. Safe to enable gates **one at a time** with monitoring:
1. `GATE_PRIOR_UNITS`
2. `GATE_ACADEMIC_OR`
3. `GATE_CONFLICTS`, `GATE_AFFILIATIONS`, then remaining gates

All production `GATE_*` flags remain **false** until explicit rollout.

## Gate flags (production)

- `GATE_ACADEMIC_OR` = `False`
- `GATE_AFFILIATIONS` = `False`
- `GATE_AGE_AS_OF` = `False`
- `GATE_CONFLICTS` = `False`
- `GATE_ENTRY_PATH` = `False`
- `GATE_MARITAL_STATUS` = `False`
- `GATE_PARENT_SALARY_GRADE` = `False`
- `GATE_PRIOR_UNITS` = `False`
- `GATE_RESIDENCY_YEARS` = `False`
- `GATE_WORK_EXPERIENCE` = `False`

## Phase A — Deployment

**Pass:** yes

- [PASS] alembic_head_048: got '048'
- [PASS] column_scholarships.max_prior_tertiary_units: present
- [PASS] column_scholarships.min_work_experience_years: present
- [PASS] column_scholarships.max_class_rank: present
- [PASS] column_scholarships.max_class_percentile: present
- [PASS] column_scholarships.academic_gate_mode: present
- [PASS] column_scholarships.allow_transferee: present
- [PASS] column_scholarships.allow_shiftee: present
- [PASS] column_scholarships.first_undergraduate_only: present
- [PASS] column_scholarships.min_residency_years: present
- [PASS] column_scholarships.age_as_of_date: present
- [PASS] column_scholarships.age_as_of_rule: present
- [PASS] column_scholarships.max_parent_salary_grade: present
- [PASS] column_scholarships.parent_program_id: present
- [PASS] table_conflict_scopes: present
- [PASS] table_scholarship_conflict_scopes: present
- [PASS] table_student_active_grant_scopes: present
- [PASS] table_affiliation_codes: present
- [PASS] table_scholarship_required_affiliations: present
- [PASS] table_student_affiliations: present
- [PASS] seed_conflict_national_stufap: have ['lgu_grant', 'national_stufap']
- [PASS] seed_conflict_lgu_grant: have ['lgu_grant', 'national_stufap']
- [PASS] seed_affiliation_ncfrs: have 14 codes
- [PASS] seed_affiliation_rsbsa: have 14 codes
- [PASS] seed_affiliation_sra: have 14 codes
- [PASS] seed_affiliation_gsis_member: have 14 codes
- [PASS] seed_affiliation_hei_faculty: have 14 codes

## Phase B — Data

**Pass:** yes

- [PASS] critical_73_exists: DOST UG
- [PASS] critical_73_max_prior_tertiary_units: expected 0, got 0
- [PASS] critical_73_min_residency_years: expected 4, got 4
- [PASS] critical_73_enroll_incoming_freshman: enrollment=['incoming_freshman', 'enrolled']
- [PASS] critical_73_enroll_enrolled: enrollment=['incoming_freshman', 'enrolled']
- [PASS] critical_73_conflict_national_stufap: scopes=['national_stufap']
- [PASS] critical_76_exists: BPMSP HE
- [PASS] critical_76_max_prior_tertiary_units: expected 0, got 0
- [PASS] critical_76_academic_gate_mode: expected 'or', got 'or'
- [PASS] critical_76_max_class_rank: expected 5, got 5
- [PASS] critical_76_enroll_incoming_freshman: enrollment=['incoming_freshman']
- [PASS] critical_77_exists: BPMSP TVET
- [PASS] critical_77_academic_gate_mode: expected 'or', got 'or'
- [PASS] critical_77_max_class_rank: expected 5, got 5
- [PASS] critical_10_exists: SM Foundation
- [PASS] critical_10_max_prior_tertiary_units: expected 0, got 0
- [PASS] critical_10_enroll_incoming_freshman: enrollment=['incoming_freshman', 'enrolled']
- [PASS] critical_10_enroll_enrolled: enrollment=['incoming_freshman', 'enrolled']
- [PASS] critical_66_exists: TES
- [PASS] critical_66_conflict_national_stufap: scopes=['national_stufap']
- [PASS] critical_54_exists: MSRS
- [PASS] critical_54_conflict_national_stufap: scopes=['national_stufap']
- [PASS] critical_117_exists: CoScho
- [PASS] critical_117_conflict_national_stufap: scopes=['national_stufap']
- [PASS] critical_117_aff_ncfrs: affiliations=['ncfrs']
- [PASS] critical_61_exists: Megaworld
- [WARN] critical_61_partner_schools: eligible_schools empty — prior remediation not applied; gate will be N/A
- [PASS] critical_132_exists: Megaworld College
- [WARN] critical_132_partner_schools: eligible_schools empty — prior remediation not applied; gate will be N/A
- [PASS] manifest_73_max_prior_tertiary_units: expected 0, got 0
- [PASS] manifest_73_eligible_enrollment_status: expected ['incoming_freshman', 'enrolled'], got ['incoming_freshman', 'enrolled']
- [PASS] manifest_73_min_residency_years: expected 4, got 4
- [PASS] manifest_76_max_prior_tertiary_units: expected 0, got 0
- [PASS] manifest_76_academic_gate_mode: expected 'or', got 'or'
- [PASS] manifest_76_min_gwa_normalized: expected 95, got 95.0
- [PASS] manifest_76_max_class_rank: expected 5, got 5
- [PASS] manifest_76_eligible_enrollment_status: expected ['incoming_freshman'], got ['incoming_freshman']
- [PASS] manifest_77_academic_gate_mode: expected 'or', got 'or'
- [PASS] manifest_77_min_gwa_normalized: expected 90, got 90.0
- [PASS] manifest_77_max_class_rank: expected 5, got 5
- [PASS] manifest_10_max_prior_tertiary_units: expected 0, got 0
- [PASS] manifest_10_eligible_enrollment_status: expected ['incoming_freshman', 'enrolled'], got ['incoming_freshman', 'enrolled']
- [PASS] manifest_104_academic_gate_mode: expected 'or', got 'or'
- [PASS] manifest_104_max_class_rank: expected 5, got 5
- [PASS] manifest_5_first_undergraduate_only: expected True, got True
- [PASS] manifest_5_max_prior_tertiary_units: expected 0, got 0
- [PASS] manifest_5_eligible_enrollment_status: expected ['incoming_freshman', 'enrolled'], got ['incoming_freshman', 'enrolled']
- [PASS] manifest_74_min_work_experience_years: expected 2, got 2
- [PASS] manifest_90_min_work_experience_years: expected 2, got 2
- [PASS] manifest_91_min_work_experience_years: expected 2, got 2
- [PASS] consortium_ASTHRDP_3: umbrella row skipped (multi-program title)
- [PASS] consortium_ASTHRDP_133: schools=['ateneo-de-manila-university', 'de-la-salle-university', 'university-of-the-philippines-diliman', 'university-of-the-philippines-los-banos'] expected subset ['ateneo-de-manila-university', 'de-la-salle-university', 'university-of-the-philippines-diliman', 'university-of-the-philippines-los-banos']
- [PASS] consortium_ERDT_3: umbrella row skipped (multi-program title)
- [PASS] consortium_ERDT_134: schools=['mapua-university', 'technological-university-of-the-philippines', 'university-of-the-philippines-diliman', 'university-of-the-philippines-los-banos'] expected subset ['mapua-university', 'technological-university-of-the-philippines', 'university-of-the-philippines-diliman', 'university-of-the-philippines-los-banos']

## Phase C — Engine

**Pass:** yes

- [PASS] pytest_migration_persona_regression: see pytest output

## Phase D — Cross Surface

**Pass:** yes

- [PASS] cross_incoming_freshman_g12_73_status_parity: match=almost_qualified api=almost_qualified detail=almost_qualified filtered=False svc=excluded_by_hard_filter
- [PASS] cross_incoming_freshman_g12_10_status_parity: match=almost_qualified api=almost_qualified detail=almost_qualified filtered=False svc=excluded_by_hard_filter
- [PASS] cross_incoming_freshman_g12_76_status_parity: match=not_eligible api=not_eligible detail=not_eligible filtered=False svc=excluded_by_hard_filter
- [PASS] cross_college_enrolled_units_73_status_parity: match=provisionally_qualified svc=provisionally_qualified api=provisionally_qualified detail=provisionally_qualified filtered=True
- [PASS] cross_college_enrolled_units_10_status_parity: match=provisionally_qualified svc=provisionally_qualified api=provisionally_qualified detail=provisionally_qualified filtered=True
- [PASS] cross_stufap_conflict_66_status_parity: match=provisionally_qualified svc=provisionally_qualified api=provisionally_qualified detail=provisionally_qualified filtered=True
- [PASS] cross_stufap_conflict_54_status_parity: match=almost_qualified api=almost_qualified detail=almost_qualified filtered=False svc=excluded_by_hard_filter
- [PASS] cross_stufap_conflict_73_status_parity: match=almost_qualified api=almost_qualified detail=almost_qualified filtered=False svc=excluded_by_hard_filter

## Phase E — Production Health

**Pass:** yes

- [PASS] scores_recomputed: completeness rows=114
- [PASS] confidence_present: confidence rows=114
- [PASS] spec13_manifest_scholarships: 0 manifest violations; 2 total active
- [PASS] spec13_active_catalog_total: 2 violations (Megaworld schools + TDP enrollment known gaps)
- [PASS] score_audit_artifact: C:\Iskonnect\scholarship-match\data\post_migration_score_audit.json
- [PASS] catalog_quality_report: ok

## Phase F — Verification Integrity

**Pass:** yes

- [PASS] backfill_did_not_bump_last_verified_at: checked 29 IDs
- [PASS] backfill_field_evidence_written: rows=40
- [PASS] write_path_classification: migration_v1_backfill uses create_field_evidence only; scholarship_persist / staging promote / verify_refresh may bump last_verified_at intentionally

## Residual risks

- Megaworld (61/132) partner `eligible_schools` not in v1 manifest — school gate N/A until remediated.
- Eligibility API and Detail evaluate without join-table enrichment; Match/Planner use enriched dicts. With gates off this is latent; enrich those paths before enabling `GATE_CONFLICTS` / `GATE_AFFILIATIONS`.
- 96 active scholarships missing deadline; 43 stale verification — pre-existing catalog health issues.

## Next steps

1. Enable `GATE_PRIOR_UNITS` only; monitor provisional/not_eligible rates.
2. Enable `GATE_ACADEMIC_OR`; repeat monitoring.
3. Fix API/Detail enrichment before conflict/affiliation gates.
4. Post-gate public beta trust audit (deferred).
