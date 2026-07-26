# ISKONNECT Catalog Audit — Final Report

**Date:** 2026-07-26  
**Scope:** National scholarship catalog integrity audit (lifecycle, filters, trust, dedupe, UX)

---

## Executive summary

The catalog had a systemic lifecycle bug: **passed deadlines were treated as permanent program discontinuation**, archiving ~78 rows. Combined with a secondary bug where `needs_review` editorial state incorrectly set `is_active=false`, the searchable catalog collapsed to **42 active rows** while "No longer offered" showed **83**.

After repair: **120 active scholarships**, **6 intentionally inactive** (5 merged duplicates + 1 permanently discontinued).

---

## What was fixed

### Lifecycle model
- Rewrote [catalog_maintenance.py](../app/jobs/catalog_maintenance.py) — past deadlines roll into `last_close_date`, clear stale `application_deadline`, stay active
- Added [lifecycle_repair.py](../app/utils/lifecycle_repair.py) and [repair_lifecycle_state.py](../app/scripts/repair_lifecycle_state.py) — **61 rows repaired**
- Fixed [editorial_state.py](../app/utils/editorial_state.py) — `needs_review` no longer hides rows from browse

### Search filters (Part 7)
- Decoupled `timing=archived` from `include_archived` widening in [scholarship_search.py](../app/api/v1/scholarship_search.py)
- Default browse = all `is_active` rows; timing filters narrow without expanding base query
- Fixed `open_now` to exclude future `application_open_date`
- Added `json_list_empty` fallbacks for life stage and course filters

### Trust labeling
- Research imports map to `csv_import`, not `manual` ([staging_promotion.py](../app/utils/staging_promotion.py))
- `verified` badge requires real `field_evidence` ([verification_display.py](../app/utils/verification_display.py))
- Backfilled 35 imported rows (ids ≥92) to honest `imported_unverified`

### Duplicates merged
- Pairs: 1/114, 10/115, 61/116, 75/126, 124/110 via [merge_catalog_duplicates.py](../app/scripts/merge_catalog_duplicates.py)
- Umbrella reframing for TESDA (id 4) and JLSS (id 79)

### UX redesign (Phase 3)
- Replaced 17-chip layout with compact beta badge + [OpportunityRoadmapDialog.tsx](../frontend/src/components/OpportunityRoadmapDialog.tsx)
- Search bar moved ~200px higher on page

### Quality infrastructure
- [catalog_quality_report.py](../app/scripts/catalog_quality_report.py) → [CATALOG_QUALITY.md](./CATALOG_QUALITY.md)
- Admin analytics now exposes `catalog_quality` metrics
- [automated_catalog_validation.py](../app/scripts/automated_catalog_validation.py) for non-tier-1 rows

---

## Current catalog state

| Metric | Value |
|--------|------:|
| Total | 126 |
| Active | 120 |
| Inactive (intentional) | 6 |
| With field evidence | 82 (68%) |
| Broken links (active) | 34 (28%) |
| Badge: needs_review | 75 |
| Badge: partially_verified | 24 |
| Badge: imported_unverified | 21 |

---

## What remains unresolved

1. **Full tier-1 web verification** — government rows have partial bundle CSV coverage; many field_changes skipped due to drift (DB already ahead of CSV)
2. **Broken links (34)** — require URL correction pass; link checker + manual review
3. **LGU rows (34 active)** — automated validation only; queued in `automated_validation_queue.json`
4. **Verified badge at 0%** — intentional until field_evidence exists per row; honesty over false confidence
5. **13 verification bundles** — link audits complete; full ChatGPT field verification still pending

---

## Recommendations

1. Run `python -m app.scripts.fix_broken_links --apply` after updating URLs from bundle reports
2. Complete LGU NCR bundle human verification next (highest student search volume)
3. Set GitHub `RENDER_API_URL` and re-run load test on warmed instance
4. Schedule catalog_maintenance weekly; never reintroduce deadline→archive bulk UPDATE
5. Measure success by quality metrics in CATALOG_QUALITY.md, not raw scholarship count

---

## Scripts reference

```bash
python -m app.scripts.repair_lifecycle_state --apply
python -m app.scripts.reactivate_visible_catalog --apply
python -m app.scripts.merge_catalog_duplicates --apply
python -m app.scripts.backfill_import_trust --apply
python -m app.scripts.catalog_quality_report
python -m app.scripts.automated_catalog_validation --apply
```
