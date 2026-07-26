# Catalog verification and data pipeline

How scholarship data enters the catalog, gets verified, and stays accurate.

## Pipeline overview

```
CSV / research import  →  scholarships_staging  →  admin approve  →  scholarships (live)
                                                              ↓
                                         catalog maintenance (nightly)
                                                              ↓
                                         search + matching cache
```

**Policy:** All external imports land in **staging** first. Every row requires explicit admin approval before going live.

## Ingestion paths

| Path | Entry point | Destination |
|------|-------------|-------------|
| CSV → staging | `python -m app.scripts.csv_to_staging` | `scholarships_staging` |
| Staging approve | Admin UI or `POST /api/v1/scholarships/staging/{id}/approve` | `scholarships` |
| Field corrections | `python -m app.scripts.apply_field_changes` | `scholarships` + `field_evidence` |
| Admin create/edit | `POST /api/v1/scholarships` | `scholarships` |

CSV format is defined in [import_csv_contract.md](import_csv_contract.md).

## Completeness and publishability

- **Score:** `app/utils/data_completeness.py` — weighted 0–100, recomputed on write and nightly
- **Gate:** Search and matching exclude rows below the publishability threshold (40)
- **Admin:** `GET /api/v1/admin/data-quality` — tier distribution and gap views

## Trust labels

Verification badges require real `field_evidence` rows — completeness alone does not produce a “verified” badge.

| Source | Meaning |
|--------|---------|
| `team_verified` | Human-reviewed against official source |
| `csv_import` | Imported from CSV/research, not yet fully verified |
| `imported_unverified` | Automated validation only |

## Catalog maintenance

Runs via GitHub Actions **Scholarship deadline maintenance**:

```bash
python -m app.jobs.catalog_maintenance
```

What it does:

1. Past deadlines → cycle rollover (`last_close_date`, clear stale deadline) — stays active
2. Stale verification → `needs_review` editorial flag
3. Recompute completeness scores
4. Invalidate scholarship list cache

Permanently discontinued programs are set `is_active=false` by human verification — not by deadline expiry alone.

## Maintainer scripts

| Script | Purpose |
|--------|---------|
| `python -m app.scripts.apply_field_changes --csv path/to/field_changes.csv` | Preview field corrections |
| `python -m app.scripts.apply_field_changes --csv … --apply` | Apply corrections + evidence |
| `python -m app.scripts.run_verification_bundle --all-pending` | Automated link audit for pending bundles |
| `python -m app.scripts.fix_broken_links` | Bulk link status updates |
| `python -m app.scripts.catalog_quality_report` | Emit catalog quality metrics |
| `python -m app.scripts.automated_catalog_validation --apply` | Label unverified rows, update link status |

Field correction CSVs live under `verification/reports/{bundle_id}/field_changes.csv`. Bundle exports live under `verification/export/`.

## Matching path

1. Student profile → `GET /api/v1/plan/{profile_id}` or `POST /api/v1/match-runs`
2. `match_service.py` loads publishable catalog from cache
3. `hard_filters.py` → `evaluate_eligibility()`
4. Passing rows scored and ranked with verification badges attached

## Troubleshooting

| Symptom | Check |
|---------|--------|
| Scholarship missing from search | `is_active`, `data_completeness_score`, `data_status` |
| Staging not clearing | Admin approve queue; `dedupe_key` conflicts |
| Stale badges | Run catalog maintenance; review `needs_review` queue |
| Wrong timing filter counts | `application_status`, cycle fields, not `is_active` alone |

## Key files

| File | Role |
|------|------|
| `app/utils/staging_promotion.py` | Staging → live promotion rules |
| `app/utils/scholarship_persist.py` | Persist + completeness on write |
| `app/matching/eligibility_result.py` | Eligibility contract |
| `app/jobs/catalog_maintenance.py` | Nightly lifecycle + quality |
| `app/jobs/link_checker.py` | HTTP link health checks |
