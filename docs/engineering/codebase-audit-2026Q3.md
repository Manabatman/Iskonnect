# Codebase audit — 2026 Q3

**Owner:** Engineering  
**Last verified:** 2026-07-31  
**Task:** SUBTRACT-01  
**Source:** Part II of `ISKONNECT_PHASE_3_MASTER_PLAN.md`

This document records keep / defer / delete decisions for orphan routes, unused API endpoints, and unused database tables. Deletions are executed only after grep evidence and test suite green (SUBTRACT-02 through SUBTRACT-09).

**Legend**

| Column | Meaning |
| --- | --- |
| Planned | Built in codebase |
| Needed | Serves a current student goal today |
| Requested | Users or partners asked for it |
| Decision | keep · defer · delete |

---

## II.1 — Orphan frontend routes (11 unreachable from nav)

| Route | Planned | Needed | Requested | Decision | Rationale |
| --- | --- | --- | --- | --- | --- |
| `/success-stories` | Yes | Low | No | **keep** | Honest empty-state page; no fabricated testimonials. Link from footer in a future pass. |
| `/organizations/:slug` | Yes | Medium | No | **defer** | Provider detail surface; wire from scholarship detail provider name before delete. |
| `/design-system` | Yes | Dev only | No | **keep** | Internal reference; gate to non-production in SUBTRACT-06 follow-up. |
| `/match-methodology` | Yes | Medium | No | **defer** | Route still live (`App.tsx:130`). Consolidate with `/transparency`, `/how-we-verify`, `/why-iskonnect` in Phase 5 `CONT-04`; remove stale redirect claims (A1, 2026-08-01). |
| `/opportunities/:typeSlug` | Yes | Yes | No | **keep** | Honest "coming soon" for unlaunched verticals. |
| `/changelog` | Yes | Low | No | **keep** | Settings-linked; low cost. |
| `/match/:profileId` | Yes | Yes | No | **keep** | Programmatic match results entry. |
| `/match-compare` | Yes | Medium | No | **keep** | Comparison tool; linked from match UI. |
| `/admin/analytics` | Yes | Ops | No | **keep** | Admin sub-route; linked from `/admin`. |
| `/forgot-password`, `/reset-password`, `/verify-email` | Yes | Yes | No | **keep** | Auth flow; correct by design (email/redirect only). |
| `/sponsor`, `/school` | Yes | Unclear | No | **defer** | Built and tested; feature-flag or hide nav until partner onboarded (SUBTRACT-06). |
| `/planner/:profileId` | Yes | Medium | No | **keep** | Calendar/planner for saved opportunities. |

---

## II.2 — Unused API endpoints (~25)

| Cluster | Endpoints | Decision | Rationale |
| --- | --- | --- | --- |
| Admin dashboards | `/admin/dashboard/health`, `/admin/dashboard/import`, `/admin/data-quality`, `/admin/staging/stats`, `/admin/scraper-runs/latest` | **defer** | Wire into Admin UI or document as ops-only CLI. |
| Scoring admin | `GET`/`PUT /admin/scoring/weights` | **keep** | Load-bearing; document as ops-only. |
| Audit | `GET /admin/audit/logs` | **keep** | RA 10173 compliance story. |
| Staging | `POST /scholarships/staging/import`, `GET .../diff` | **defer** | Confirm CLI usage; document in deployment runbook. |
| Search | `GET /scholarships/search/semantic` | **defer** | Phase 4 seam; delete only if confirmed unused. |
| Suggestions | `/suggestions/regions`, `/suggestions/readiness` | **defer** | Replace hardcoded frontend regions (SUBTRACT-05). |
| Profiles | `PUT /profiles/me`, `GET /profiles`, `GET /profiles/{id}` | **defer** | Builder POST-only bug; fix in SUBTRACT-05. |
| Saved | `GET /saved-scholarships/ids` | **delete** | No frontend consumer; safe removal when scheduled. |
| Applications | `GET /applications/{id}`, `POST /applications/{id}/remove` | **delete** | No frontend consumer; safe removal when scheduled. |

---

## II.3 — Unused database tables (SIPP / OJT vertical)

| Table | Migration | Decision | Rationale |
| --- | --- | --- | --- |
| `hte_partners` | `025_sipp_ojt_compliance` | **defer** | Zero API/frontend references; **do not drop** — migration risk and no reversible backup in CI. |
| `internship_opportunities` | `025_sipp_ojt_compliance` | **defer** | Same as above. |
| `ojt_compliance_vault` | `025_sipp_ojt_compliance` | **defer** | Same as above. |

**Note:** SUBTRACT-03 (table removal) is deferred per launch risk. Tables remain in schema with RLS from `027_rls_sipp_tables.py` until a dedicated migration window with backup.

---

## II.4 — Dead code removed (SUBTRACT-02)

| Item | Evidence | Status |
| --- | --- | --- |
| `CareerRoadmapCard.tsx` | Zero imports | **deleted** |
| `ReviewCenterFinderCard.tsx` | Zero imports | **deleted** |
| `SocialProofTicker.tsx` + `marquee` keyframes | Zero imports | **deleted** |
| `lib/motion.ts` | Zero imports | **deleted** |
| `ui/icon.tsx` | Zero consumers outside barrel | **deleted** |
| `formatDate`, `parseDateOnly` exports | Zero call sites | **deleted** |
| `dataStatusToLifecycle` | Deprecated; callers use `resolveApplicationStatus` | **deleted** |

---

## II.5 — Consolidation completed (SUBTRACT-04, SUBTRACT-08, SUBTRACT-09)

| Task | Change | Status |
| --- | --- | --- |
| SUBTRACT-04 | `SavedScholarshipsErrorBanner` → shared `components/layout/SavedScholarshipsErrorBanner.tsx` | **done** |
| SUBTRACT-08 | Legacy helpers `_data_status_passes_for_matching`, `_level_matches`, `_region_matches`, `_income_matches` removed from `hard_filters.py` | **done** |
| SUBTRACT-09 | Trust-page consolidation (`/match-methodology` et al.) | **deferred** — route still live; stale “redirect done” claims removed in A1 (2026-08-01); code consolidation in Phase 5 `CONT-04` |

---

## Scheduled follow-ups (not in this batch)

| ID | Item | Decision |
| --- | --- | --- |
| SUBTRACT-05 | Profile options single source of truth | defer |
| SUBTRACT-06 | Sponsor/school portal launch vs flag-off | defer |
| SUBTRACT-07 | `ScoringEnginePort` justification or inline | defer |
| SUBTRACT-10 | Decompose eight files >400 lines | defer |

---

## What would make this document wrong

- New routes or endpoints added without updating this table
- SIPP tables wired to API without changing decision to **keep**
- Nav links added to previously orphan routes (reclassify reachability)
