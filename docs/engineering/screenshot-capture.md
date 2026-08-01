# Screenshot capture procedure (LAND-02 / LAND-03)

**Owner:** Engineering / Design  
**Task:** C1 prep for C4 landing proof strip  
**Last updated:** 2026-08-01

## Purpose

Capture real product screenshots for the landing page proof strip. Assets must reflect the current UI after the Phase 2 design-system migration — not mockups or stock imagery.

## When to capture

- After Phase 4 UI changes that affect match cards, search, or dashboard
- Before each major landing release (C6 Lighthouse gate)
- After theme token changes that affect contrast or layout

## Environment

1. Run locally with seeded demo data: `python -m app.scripts.seed_data` (or CI E2E seed).
2. Use **no real user data** — demo personas only.
3. API and frontend both running (`uvicorn` + `npm run dev`).

## Viewports

| Asset | Viewport | DPR | Themes |
| --- | --- | ---: | --- |
| Match results with score + badge | 1280 × 800 | 2× | light + dark |
| Score breakdown modal | 1280 × 800 | 2× | light + dark |
| Search with filters applied | 1280 × 800 | 2× | light + dark |
| Mobile dashboard (device frame) | 390 × 844 | 2× | light + dark |

Record intrinsic dimensions in the filename (e.g. `match-results-1280x800@2x-light.webp`).

## Capture steps

1. Log in as a seeded student with a complete profile (e.g. CI E2E user).
2. Navigate to each target screen; wait for data to load (no spinners).
3. Hide dev-only banners (`ApiWarmupBanner`, debug overlays) if visible.
4. Capture full viewport — crop in design tool if needed, not in-browser zoom.
5. Export **AVIF + WebP** with explicit width/height metadata; keep PNG source in repo only if required for editing.
6. Place assets under `frontend/public/landing/screenshots/` (create directory on first C4 PR).

## Content rules

- Show real match scores with non-guarantee copy visible where applicable.
- Use listings with `last_verified_at` populated so freshness chips appear.
- Do not blur or redact provider names — they are public catalog data.
- No fabricated statistics in screenshot chrome; live stats come from `GET /api/v1/public/stats`.

## Verification checklist

- [ ] Both light and dark variants captured
- [ ] 2× DPR, no upscaled low-res captures
- [ ] Dimensions documented in PR
- [ ] Captions written as user benefits (one line each), not feature names
- [ ] Assets lazy-loaded below fold in landing implementation (C4)

## Recapture trigger

Add to release checklist when any of these change: `ScholarshipCardV2`, match analysis modal, search filter sheet, dashboard layout, or design tokens affecting landing-adjacent surfaces.
