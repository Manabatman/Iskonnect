# Documentation audit manifest

**Date:** 2026-07-26  
**Purpose:** Record every documentation file removed from the public repository during the recruiter-facing cleanup pass. Archive copies locally or in a private repo before deleting if you need them.

## Summary

| Action | Count |
|--------|------:|
| Removed (internal / personal / audit) | 105 |
| Consolidated into new public docs | 8 superseded sources |
| Added (public contributor docs) | 9 |
| Kept unchanged | 2 |

## New public documentation

| File | Purpose |
|------|---------|
| `docs/architecture.md` | System design, matching engine, troubleshooting |
| `docs/api.md` | API endpoint overview + link to FastAPI `/docs` |
| `docs/deployment.md` | Vercel + Render + Supabase + backups + observability |
| `docs/verification.md` | Catalog pipeline, staging, maintainer scripts |
| `docs/import_csv_contract.md` | CSV import format (restored) |
| `CONTRIBUTING.md` | Contributor setup and PR guidelines |
| `SECURITY.md` | Vulnerability reporting |
| `LICENSE` | MIT license |
| `docs/DOCS_AUDIT_MANIFEST.md` | This file |

## Kept in repository

| Path | Purpose | Recommendation |
|------|---------|----------------|
| `README.md` | Project overview | Keep (updated links) |
| `scripts/loadtest/README.md` | Load test instructions | Keep |
| `docs/supabase_rls_blueprint.sql` | RLS reference SQL | Keep |
| `verification/export/**` | Bundle CSV/JSON exports | Keep (operational data) |
| `verification/discovery/*.json`, `*.csv` | Discovery artifacts | Keep |
| `verification/reports/**/field_changes.csv`, `*.json` | Field corrections + queues | Keep |
| `verification/templates/**` | Report templates | Keep |

## Removed by category

| Category | Count | Recommendation |
|----------|------:|----------------|
| Personal learning (`docs/learning/**`, `notes/`) | 32 | Move to private |
| Operations handbook (`docs/operations-handbook/**`) | 11 | Move to private |
| Superseded docs (merged into new `docs/*.md`) | 10 | Delete |
| Engineering / audit root docs | 2 | Move to private |
| Internal status guides | 2 | Move to private |
| Verification prompts (`verification/prompts/**`) | 16 | Move to private |
| Verification planning (`verification/*.md`) | 5 | Move to private |
| Verification audit reports (`verification/reports/**/*.md`) | 22 | Move to private |
| Verification discovery notes (`verification/discovery/*.md`) | 2 | Move to private |
| One-off run artifacts (`data/*report*.json`, logs) | 6 | Delete |

## Full removal list

```
data/approve_staging_report.json
data/automated_validation.log
data/bundle_audit_log.txt
data/discovery_import_report.json
data/gemini_staging_report.json
data/repair_lifecycle_report.json
docs/BACKUP_ROLLBACK.md
docs/BACKUPS.md
docs/DEPLOYMENT.md
docs/DEPLOYMENT_CHECKLIST.md
docs/ENGINEERING_HANDBOOK.md
docs/HANDBOOK.md
docs/learning/ACTIVE_LEARNING_PATH.md
docs/learning/apprenticeship/00-index.md
docs/learning/apprenticeship/01-how-engineers-think.md
docs/learning/apprenticeship/02-terminal-and-os.md
docs/learning/apprenticeship/03-git-and-version-control.md
docs/learning/apprenticeship/04-python-env-and-deps.md
docs/learning/apprenticeship/05-project-genesis-day0.md
docs/learning/apprenticeship/06-fastapi-and-request-lifecycle.md
docs/learning/apprenticeship/07-sqlalchemy-data-modeling.md
docs/learning/apprenticeship/08-pydantic-validation-and-schemas.md
docs/learning/apprenticeship/09-alembic-migrations.md
docs/learning/apprenticeship/10-auth-jwt-bcrypt.md
docs/learning/apprenticeship/11-matching-engine-architecture.md
docs/learning/apprenticeship/12-scoring-engine-internals.md
docs/learning/apprenticeship/13-domain-taxonomies.md
docs/learning/apprenticeship/14-redis-cache-and-rate-limiting.md
docs/learning/apprenticeship/15-middleware-observability-sentry.md
docs/learning/apprenticeship/16-background-jobs-and-data-ingest.md
docs/learning/apprenticeship/17-backend-testing-philosophy.md
docs/learning/apprenticeship/18-react-vite-typescript.md
docs/learning/apprenticeship/19-frontend-architecture-routing-state.md
docs/learning/apprenticeship/20-frontend-auth-and-data-flow.md
docs/learning/apprenticeship/21-tailwind-pwa-virtualization-perf.md
docs/learning/apprenticeship/22-frontend-testing.md
docs/learning/apprenticeship/23-ci-cd-and-docker.md
docs/learning/apprenticeship/24-production-deployment.md
docs/learning/apprenticeship/25-operations-and-incident-response.md
docs/learning/apprenticeship/26-maintenance-and-rebuild-capstone.md
docs/learning/LEARNING_GUIDE.md
docs/learning/learning-log.md
docs/learning/TEACHING.md
docs/MONITORING_GUIDE.md
docs/OBSERVABILITY.md
docs/operations-handbook/00-index.md
docs/operations-handbook/01-architecture.md
docs/operations-handbook/02-deployment.md
docs/operations-handbook/03-verification.md
docs/operations-handbook/04-domains-and-dns.md
docs/operations-handbook/05-testing-production.md
docs/operations-handbook/06-data-pipeline.md
docs/operations-handbook/07-operations.md
docs/operations-handbook/08-observability.md
docs/operations-handbook/09-scaling.md
docs/operations-handbook/10-founder-operator-handbook.md
docs/OPPORTUNITY_ARCHITECTURE.md
docs/status-guide-journey-validation.md
docs/status-guide-phase0-decisions.md
notes/learning-log.md
PRODUCTION_AUDIT.md
SCORING_ENGINE.md
verification/CHANGE_REASONS.md
verification/CHECKLIST.md
verification/CLOSURE_TYPES.md
verification/DEFINITION_OF_DONE.md
verification/discovery/discovery_summary.md
verification/discovery/SCHEMA.md
verification/MISSING_SCHOLARSHIP_TARGETS.md
verification/prompts/00_MASTER_INSTRUCTIONS.md
verification/prompts/archived_reference_prompt.md
verification/prompts/ched_unifast_prompt.md
verification/prompts/dost_prompt.md
verification/prompts/gsis_sss_prompt.md
verification/prompts/international_prompt.md
verification/prompts/lgu_ncr_prompt.md
verification/prompts/lgu_provincial_prompt.md
verification/prompts/megaworld_foundation_prompt.md
verification/prompts/military_affiliation_prompt.md
verification/prompts/other_government_prompt.md
verification/prompts/owwa_dswd_ncip_prompt.md
verification/prompts/private_foundations_prompt.md
verification/prompts/sm_foundation_prompt.md
verification/prompts/tesda_prompt.md
verification/prompts/universities_prompt.md
verification/reports/_db_quality_audit.md
verification/reports/application_cycle_reverification.md
verification/reports/archived_reference/human_report.md
verification/reports/BUNDLE_STATUS.md
verification/reports/CATALOG_AUDIT_FINAL.md
verification/reports/CATALOG_QUALITY.md
verification/reports/ched_unifast/human_report.md
verification/reports/dost/human_report.md
verification/reports/gsis_sss/human_report.md
verification/reports/international/human_report.md
verification/reports/lgu_ncr/human_report.md
verification/reports/lgu_provincial/human_report.md
verification/reports/megaworld_foundation/human_report.md
verification/reports/military_affiliation/human_report.md
verification/reports/other_government/human_report.md
verification/reports/owwa_dswd_ncip/human_report.md
verification/reports/private_foundations/human_report.md
verification/reports/sm_foundation/human_report.md
verification/reports/tesda/human_report.md
verification/reports/universities/human_report.md
```
