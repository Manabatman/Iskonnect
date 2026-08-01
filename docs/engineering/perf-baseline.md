# ISKONNECT Performance Baseline

> **Owner:** Engineering  
> **Created:** P1-01 (login waterfall instrumentation)  
> **Updated:** _fill after each measurement run_

This document records **measured** login and dashboard timings. Do not optimize until numbers exist here.

---

## How to capture

### Backend (`Server-Timing` header)

Every API response includes a `wall;dur=…` metric from request middleware. Auth routes add phase breakdowns:

| Endpoint | Phase metrics |
| --- | --- |
| `POST /api/v1/auth/login` | `db-lookup`, `bcrypt`, `token-issue`, `wall` |
| `GET /api/v1/auth/me` | `auth-resolve`, `wall` |
| `GET /api/v1/plan/{profile_id}` | `auth`, `profile-load`, `cache-lookup`, `cache-hit` or `scholarships`, `match`, `cache-store`, `wall` |
| `GET /api/v1/scholarships/search` | `filter-build`, `count`, `fetch`, `serialize`, `wall` |

**DevTools:** Network tab → select request → Response Headers → `Server-Timing`

**curl:**

```bash
curl -s -D - -o /dev/null -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"YOUR_EMAIL","password":"YOUR_PASSWORD"}' | grep -i server-timing
```

### Frontend (`performance.mark` / `performance.measure`)

After P1-01 ships, the login → dashboard path emits marks:

| Mark / measure | Meaning |
| --- | --- |
| `login:submit` | User clicked Sign in |
| `login:login-response` | `POST /login` returned tokens |
| `login:login-request` | measure: submit → login-response |
| `login:auth-me-start` | `GET /auth/me` began |
| `login:auth-me-done` | User object available in AuthContext |
| `login:auth-me` | measure: auth-me-start → auth-me-done |
| `login:navigate-dashboard` | React Router navigated to `/dashboard` |
| `login:dashboard-shell` | Dashboard layout rendered with user |
| `login:dashboard-data` | Profile + match-runs wave complete |
| `login:dashboard-matches` | Latest match results visible |

**Dev console:** After login, run:

```javascript
performance.getEntriesByType("measure")
  .filter((e) => e.name.startsWith("login:"))
  .forEach((e) => console.log(e.name, e.duration.toFixed(1) + "ms"));
```

Or use the helper: `window.__iskonnectLogLoginWaterfall?.()` (dev only, added in P1-01).

### Environment matrix

Record **each** scenario separately — cold vs warm backend changes results dramatically.

| Scenario | Backend | Network | Notes |
| --- | --- | --- | --- |
| Local warm | `uvicorn` already running | localhost | Best-case dev baseline |
| Local cold | Restart uvicorn, first request | localhost | Simulates cold worker |
| Render warm | Instance recently pinged | Production API URL | Typical returning user |
| Render cold | No request ≥15 min | Production API URL | Worst-case first visit |

---

## Login waterfall (target diagram)

```
User clicks Sign in
        ↓
[client] login:submit
        ↓
POST /api/v1/auth/login          ← Server-Timing: db-lookup, bcrypt, token-issue, wall
        ↓
[client] login:login-response
        ↓
GET /api/v1/auth/me              ← Server-Timing: auth-resolve, wall   (removed in P1-03)
        ↓
[client] login:auth-me-done
        ↓
Navigate /dashboard
        ↓
[client] login:dashboard-shell
        ↓
Parallel: GET /profiles/me, GET /match-runs, GET /saved-scholarships
        ↓
[client] login:dashboard-data
        ↓
Serial: GET /plan/{id}, GET /match-runs/{id}
        ↓
[client] login:dashboard-matches
        ↓
First meaningful dashboard content painted
```

---

## Baseline measurements

### Local warm (_date: ___)

| Step | Client (ms) | Server-Timing (ms) | Notes |
| --- | --- | --- | --- |
| submit → login-response | | db-lookup: / bcrypt: / token-issue: / wall: | |
| login-response → auth-me-done | | wall: | |
| submit → dashboard-shell | | | |
| submit → dashboard-data | | | |
| submit → dashboard-matches | | | |
| **Total submit → matches** | | | |

### Render warm (_date: ___)

| Step | Client (ms) | Server-Timing (ms) | Notes |
| --- | --- | --- | --- |
| submit → login-response | | | |
| login-response → auth-me-done | | | |
| **Total submit → matches** | | | |

### Render cold (_date: ___)

| Step | Client (ms) | Server-Timing (ms) | Notes |
| --- | --- | --- | --- |
| submit → login-response | | | First request after spin-down |
| **Total submit → matches** | | | |

---

## After Phase 1 (comparison)

Fill after P1-03…P1-11 complete. Goal: measurable improvement with evidence, not guesses.

| Metric | Before (baseline) | After Phase 1 | Delta |
| --- | --- | --- | --- |
| Login requests (count) | 2 (login + /me) | 1 (P1-03) | |
| submit → dashboard-data p75 warm | | | |
| submit → dashboard-matches p75 warm | | | |
| Render cold first-byte | | | |

---

## Phase 3 (M5) — before/after placeholder

Fill after PERF-11, PERF-18, and PERF-01 land. Compare against Phase 1 baseline above.

### Bundle (gzip, `npm run build` + `audit:bundle-budget`)

| Chunk | Before M5 | After M5 | Delta |
| --- | --- | --- | --- |
| Entry (`index-*.js`) | | | |
| `vendor-*.js` | n/a | | |
| `radix-*.js` | n/a | | |
| `framer-motion-*.js` | n/a | | |
| `sentry-*.js` | n/a | | |
| Largest route chunk | | | |
| **Public static (hero JPGs removed)** | ~4860 KB | ~0 KB | |

### Logo PNGs (PERF-18 follow-up)

| Asset | Size (bytes) | Target | Notes |
| --- | --- | --- | --- |
| `public/images/logo-light.png` | 380393 | ≤ 60 KB | Re-export at 2× nav size; consider WebP/AVIF |
| `public/images/logo-dark.png` | 401227 | ≤ 60 KB | Same treatment as light variant |

### API p75 warm (Server-Timing + client marks)

| Endpoint / flow | Before M5 (ms) | After M5 (ms) | Delta |
| --- | --- | --- | --- |
| `GET /plan/{id}` total `wall` | | | |
| `GET /scholarships/search` total `wall` | | | |
| Login → dashboard-data (client) | | | |
| Login → dashboard-matches (client) | | | |

### `/plan` match core — B13 prefilter benchmark (2026-08-01)

Measured with `python -m app.scripts.measure_plan_prefilter --iterations 25` against Supabase catalog after B12 import.

| Path | Catalog size | p50 (ms) | p95 (ms) | Notes |
| --- | ---: | ---: | ---: | --- |
| Full scan (publishable) | 38 | 3.47 | 3.90 | `get_cached_scholarship_dicts` |
| SQL prefilter (publishable) | 33 | 3.38 | 3.98 | `_prefilter_scholarships_query` |
| Full scan (all active) | 117 | 10.71 | 11.30 | Scale projection input |

Raw JSON: `docs/engineering/reports/b13-plan-prefilter-bench.json`

**ADR-007 gate:** p95 ≤800 ms met for match core at 117 active / 38 publishable. HTTP `/plan` wall time not yet captured at 300-listing scale. **Flag not enabled.**

### Lighthouse mobile landing (target: 67 → 90)

| Metric | Before M5 (2026-07-31) | C6 font-opt (2026-08-01) | C6 root-cause fix (2026-08-01) | C6 gate |
| --- | --- | --- | --- | --- |
| Performance score | 67 | **70** | **88** | **FAIL** (≥ 90) |
| Accessibility score | 96 | **100** | **100** | **PASS** (≥ 95) |
| LCP (ms) | 3333 | **3312** | **3364** | **FAIL** (≤ 2500) |
| CLS | 0.425 | **0.420** | **0** | **PASS** (≤ 0.05) |
| FCP (ms) | — | **2276** | **2280** | informational |
| TBT (ms) | — | **33** | **126** | informational |

**C6 verification (2026-08-01):** Lighthouse **13.4.1** against `http://127.0.0.1:4173/` (vite preview, production build). Chrome at `C:\Program Files\Google\Chrome\Application\chrome.exe` via `CHROME_PATH`. Raw JSON: `docs/engineering/benchmarks/lighthouse-home-mobile-c6.json`.

**Optimizations shipped:**
- Font pass: latin-only `@fontsource` subsets; build-time preload; deferred Inter 700; deferred Sentry.
- Root-cause pass: `AuthContext` `loading` init from token presence (eliminates spinner→landing two-commit CLS); hero stats row height reserved; `registerSW.js` deferred via `injectRegister: "script-defer"`.

**Observed (unthrottled trace):** FCP 312 ms, LCP 312 ms, CLS 0. Simulated scores above use Slow 4G + 4× CPU.

**Post root-cause initial load:** JS transfer **185.6 KB** (5 scripts); fonts **5 latin woff2** (~103 KB). **Bundle budget:** entry 44.5 KB gzip, vendor 108.9 KB gzip — **PASS**.

**C6 status:** **Not complete** — Performance (88) and LCP (3.4 s) gates still fail. CLS and Accessibility pass.

**C4–C5 landing changes:** §11.6 section order; proof strip; single hero primary CTA; navbar 4-link + shrink; footer 4 columns + catalog last-verified; `/roadmap` page; mobile-condensed problem/benefits sections.

---

## Design blueprint — static hero photography (2026-08-01)

> **Spec:** `docs/design/PRODUCT_DESIGN_SPEC.md` (D-01), `docs/design/DESIGN_SYSTEM.md` §16  
> **Decision:** Static art-directed photograph per breakpoint — **not** auto-rotating carousel. `HeroCarousel.tsx` to be deleted.

### Rationale vs carousel

| Factor | Carousel (rejected) | Static `<picture>` (chosen) |
| --- | --- | --- |
| LCP candidates | 3 images; rotation adds JS | 1 preloaded image per viewport |
| Total image weight | ~3× decode cost if all loaded | ≤120 KB per breakpoint source |
| WCAG 2.2.2 | Fails Level A (no pause control) | Compliant (no auto-advance) |
| Reduced motion | Hard-cut between slides (CSS kills transition; JS interval continues) | No JS motion |
| Premium SaaS pattern | Legacy marketing pattern | Stripe, Linear, Notion, Vercel, Apple |

### Image budget (per breakpoint)

| Breakpoint | Format priority | Max transfer | Dimensions (intrinsic) |
| --- | --- | --- | --- |
| Mobile (<768px) | AVIF → WebP → JPEG | ≤80 KB | 768×1024 (portrait) |
| Tablet (768–1023px) | AVIF → WebP → JPEG | ≤100 KB | 1024×768 |
| Desktop (≥1024px) | AVIF → WebP → JPEG | ≤120 KB | 1920×1080 |

**Total landing imagery budget:** ≤500 KB including proof-strip screenshots (DESIGN_SYSTEM §16).

### Delivery requirements

1. `<picture>` with `media` queries per breakpoint — mobile gets portrait composition, not squeezed landscape.
2. LCP candidate: mobile source on mobile; desktop source on desktop.
3. `<link rel="preload" as="image" href="…" type="image/avif">` for LCP candidate only (one per page load).
4. `fetchpriority="high"` on LCP `<img>`; `loading="eager"`; explicit `width` and `height` for CLS = 0.
5. Scrim overlay (`--hero-scrim`) — text contrast ≥4.5:1 without relying on image content.
6. Alt text: descriptive, not decorative — e.g. "Filipino students studying together."

### Performance targets (unchanged — re-measure after hero ships)

| Metric | Target | CI enforced? | Notes |
| --- | ---: | --- | --- |
| Lighthouse mobile Performance (landing) | ≥ 90 | **No** (manual / runbook) | Was 88 with zero hero images |
| LCP (simulated Slow 4G) | ≤ 2.5 s | **No** | Was 3.4 s; static AVIF may improve or regress — measure |
| CLS | ≤ 0.05 | **No** | Was 0; must hold with explicit dimensions |
| Accessibility (landing) | ≥ 95 | **Yes** (axe Playwright) | Was 100 |
| Entry JS gzip | ≤ 120 KB | **Yes** (`audit:bundle-budget`) | 44.5 KB — headroom |
| Vendor JS gzip | ≤ 420 KB | **Yes** | 108.9 KB — headroom |

**Hypothesis:** One optimized AVIF (≤80 KB mobile) improves perceived warmth without exceeding LCP budget, because the current LCP element is hero subtitle text waiting on CSS — adding a preloaded image may shift LCP to the image itself with faster paint if preload wins the race.

**Rollback:** If LCP regresses >500 ms vs C6 baseline (3.4 s) after optimization pass, revert to CSS hero (no raster) and defer photography until render-blocking CSS is addressed (item 1 in C6 remaining contributors).

### Re-measurement protocol

After D-01 implementation:

```bash
cd frontend
npm run build
npx vite preview --port 4173 --host 127.0.0.1
# Second terminal — see docs/engineering/benchmarks/lighthouse-c6-runbook.md
```

Record in the table below and update C6 gate status.

| Metric | C6 baseline (no hero image) | After static hero (_date: ___) | Delta | Gate |
| --- | ---: | ---: | ---: | --- |
| Performance (mobile) | 88 | | | ≥ 90 |
| LCP (ms) | 3364 | | | ≤ 2500 |
| CLS | 0 | | | ≤ 0.05 |
| Hero image transfer (KB) | 0 | | | ≤ 80 (mobile) |
| Bundle budget | PASS | | | PASS |

---

## Related tasks

- **P1-01** — Instrumentation (this document + code)
- **P1-03** — Remove `/auth/me` round trip on login path
- **P1-07** — Skeletons (perceived performance)
- **PERF-07** — SQL prefilter for `/plan`
