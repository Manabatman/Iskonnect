# Verification capacity statement

**Owner:** Engineering (solo maintainer)  
**Last verified:** 2026-08-01  
**Task:** OPS-02

## Adopted public posture (2026-08-01)

ISKONNECT does **not** promise a 30-day re-verification SLA for the whole catalog. Student-facing copy and the public catalog-trust endpoint reflect:

1. **Per-listing transparency** — every card and detail page shows `last_verified_at` or an honest **"Not yet verified"** label.
2. **Launch gate (internal)** — public launch requires **≥300 published listings** with **median verification age under 90 days** (`catalog-readiness.md`; Phase 3 plan §19.2). This is an ops measurement, not a student guarantee.
3. **Internal flagging unchanged** — `STALE_VERIFICATION_DAYS = 30` in `app/utils/trust_constants.py` still drives maintainer `needs_verification` / review queues (TRUST-02). It is **not** advertised as a student SLA.
4. **Public aggregate** — `GET /api/v1/public/catalog-trust` exposes the latest verification date among active listings plus a count verified within 90 days. Landing stats: `GET /api/v1/public/stats` (C1 / LAND-03a, 1-hour cache).

This posture **unblocks catalog import (B12)**: scale-up may proceed without implying solo capacity can re-verify every listing every 30 days.

## Throughput estimate (honest)

ISKONNECT is maintained by **one student developer** (`ContactPage.tsx`). Verification is manual: confirm official link, deadline, eligibility fields, and lifecycle status against provider sources.

| Activity | Realistic solo throughput |
| --- | ---: |
| Full verification (new listing) | **8–12 listings / week** |
| Re-verification (staleness refresh) | **15–25 listings / week** |
| Mixed week (growth + refresh) | **~20 net listing-updates / week** |

Assumptions: ~20–30 minutes per new listing (research + data entry + admin publish); ~8–12 minutes per re-check; no dedicated QA team; catalog maintenance competes with engineering and coursework.

## Why a 30-day *public* SLA was retired

If the product **promised** re-verification of every listing within **30 days**:

| Catalog size | Re-verifications / month (all listings) | Solo capacity @ 20/week | Achievable? |
| ---: | ---: | ---: | --- |
| 24 (seed) | 24 | ~80 | Yes |
| 100 | 100 | ~80 | Marginal — backlog grows |
| 300 (launch gate) | 300 | ~80 | **No** — 220+ backlog/month |
| 500 | 500 | ~80 | **No** |

At **10 new listings/week** net growth and **~20 listing-updates/week** total capacity, steady state on a 30-day refresh cycle is roughly **80 listings** before backlog grows. Growing to 300 while maintaining 30-day freshness requires **~4× current throughput** or additional verifiers.

## Maintainer playbook (unchanged)

1. Show **`last_verified_at`** on every detail page and card — do not imply fresher than shown.
2. Do not auto-hide listings at 30 days if they cannot be re-verified — flag as `needs_verification` instead (TRUST-02).
3. Run the production SQL in `catalog-readiness.md` before any launch decision; target **90-day median**, not 30-day universal refresh.
4. Recruit partner verifiers or defer public launch until catalog size matches sustainable refresh load.

## What would make this document wrong

- Additional maintainers or paid verification staff onboarded (revise throughput table)
- Automated link-check + field extraction reduces manual time per listing (re-measure)
- Product reintroduces a fixed public re-verification SLA without capacity to match (requires new decision log entry)
