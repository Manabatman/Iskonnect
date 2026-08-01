# B12 catalog import batch — 2026-08-01

**Milestone:** Track B B12 (catalog import toward 300)  
**Workflow:** CSV → staging → admin approve (E15 — no direct production writes)

## Batch summary

| Step | Source | Rows staged | Approved | Net-new scholarship IDs |
| --- | --- | ---: | ---: | --- |
| Gemini triage | `data/gemini_staging_ready.csv` | 6 | 6 | 127–132 |
| Discovery | `data/discovery_import.csv` | 8 | 8 | Updates to 117–124 (existing rows) |

**Total staging rows processed:** 14 (0 errors, 0 rejected)

## Import reports

- `docs/engineering/reports/b12-staging-gemini.json`
- `docs/engineering/reports/b12-staging-discovery.json`
- `docs/engineering/reports/b12-approve-summary.json`

## Post-batch production metrics (Supabase, 2026-08-01)

| Metric | Before | After |
| --- | ---: | ---: |
| Published (`is_active`) | 114 | **117** |
| Verified within 90 days | 66 | **77** |
| Distinct providers | 63 | 63 |
| Median verification age (days) | — | **~6.3** |

## Quality follow-up

- `docs/engineering/reports/b12-catalog-quality.md` — 117 active, 70.1% with field evidence, 37.6% broken links (link checker backlog)
- `automated_catalog_validation` dry-run — 56 tier-2+ rows checked, 25 queued for review

## Gap to launch gate

- Target: **≥300** published listings
- Current: **117** (**~183 short**)
- Next batches: additional Gemini research CSVs + verification bundle corrections; re-run `gemini_triage` after each batch

## Commands (repeatable)

```bash
python -m app.scripts.gemini_triage
python -m app.scripts.csv_to_staging --csv data/gemini_staging_ready.csv --report docs/engineering/reports/b12-staging-gemini.json
python -m app.scripts.approve_staging_batch --apply --report docs/engineering/reports/b12-approve-summary.json
python -m app.scripts.catalog_quality_report --output docs/engineering/reports/b12-catalog-quality.md
python -m app.scripts.automated_catalog_validation
```
