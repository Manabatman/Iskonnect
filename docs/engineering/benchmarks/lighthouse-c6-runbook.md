# Lighthouse C6 runbook (LAND-10)

Run after `npm run build` from `frontend/`.

## Prerequisites

- Chrome or Edge installed (Lighthouse CLI needs a Chromium binary)
- Preview server on port 4173

## Commands

```bash
cd frontend
npm run build
npx vite preview --port 4173 --host 127.0.0.1
```

In a second terminal:

```bash
cd frontend
npx lighthouse http://127.0.0.1:4173/ \
  --only-categories=performance,accessibility \
  --form-factor=mobile \
  --screenEmulation.mobile=true \
  --throttling-method=simulate \
  --output=json \
  --output-path=../docs/engineering/benchmarks/lighthouse-home-mobile-c6.json

node scripts/check-bundle-budget.mjs
```

## Gate (C6)

| Metric | Before (2026-07-31) | Target |
| --- | ---: | ---: |
| Performance (mobile) | 67 | ≥ 90 |
| Accessibility (mobile) | 96 | ≥ 95 |
| LCP | 3.3 s | ≤ 2.5 s |
| CLS | (see baseline JSON) | ≤ 0.05 |

## C4–C5 optimizations shipped (2026-08-01)

- Removed hero image carousel (LCP path is now text + CSS product frame)
- Proof strip uses CSS frames (no raster decode above fold)

## Design blueprint — static hero photography (2026-08-01)

> **Spec:** `docs/design/UI_DEFECT_REGISTER.md` (D-01), `docs/design/DESIGN_SYSTEM.md` §16

**Next landing pass:** Replace CSS hero mock with **one static photograph per breakpoint** via `<picture>`. Do **not** restore `HeroCarousel.tsx`.

### Image delivery checklist (verify before marking D-01 done)

- [ ] AVIF + WebP + JPEG fallback per breakpoint
- [ ] Mobile portrait composition (distinct from desktop — not squeezed landscape)
- [ ] Preload only the LCP candidate for current viewport
- [ ] `fetchpriority="high"` on LCP `<img>`
- [ ] Explicit `width` / `height` — CLS must remain 0
- [ ] Scrim overlay for text contrast ≥4.5:1
- [ ] Mobile source ≤80 KB transfer; desktop ≤120 KB
- [ ] `HeroCarousel.tsx` deleted; no auto-rotating content (WCAG 2.2.2)

### Updated gate interpretation

| Gate | Target | CI? | After static hero |
| --- | ---: | --- | --- |
| Performance | ≥ 90 | No | Re-measure; may pass if LCP improves |
| LCP | ≤ 2.5 s | No | Re-measure; preload + AVIF is critical path |
| CLS | ≤ 0.05 | No | Must hold — explicit dimensions required |
| Accessibility | ≥ 95 | Yes (axe) | Static hero simpler than carousel |
| Bundle budget | see script | **Yes** | Images don't count toward JS budget |

**Rollback trigger:** LCP > 3.9 s (baseline + 500 ms) after one optimization pass → revert to CSS hero; see `perf-baseline.md` § Design blueprint.
- Section spacing aligned to §10.3; framer reveals capped at 240 ms
- Live stats counters fetch `/api/v1/public/stats` after paint
- Bundle budget: entry 44.2 KB gzip, vendor 107.7 KB gzip — **OK**

Record post-change scores in `perf-baseline.md` after running Lighthouse locally.

## C6 verification results (2026-08-01)

**Environment:** Windows; Lighthouse **13.4.1**; Chrome `C:\Program Files\Google\Chrome\Application\chrome.exe` via `CHROME_PATH` (not on PATH). Preview: `npx vite preview --port 4173 --host 127.0.0.1`.

### Before minimal optimizations

| Metric | Measured | Target | Result |
| --- | ---: | ---: | --- |
| Performance (mobile) | **63** | ≥ 90 | **FAIL** |
| Accessibility (mobile) | **100** | ≥ 95 | **PASS** |
| LCP | **3.7 s** (3706 ms) | ≤ 2.5 s | **FAIL** |
| CLS | **0.420** | ≤ 0.05 | **FAIL** |
| FCP | **3.2 s** (3167 ms) | — | — |
| Bundle budget | entry 44.2 KB / vendor 107.7 KB gzip | see `check-bundle-budget.mjs` | **PASS** |
| Initial JS transfer | 221.8 KB (6 scripts incl. Sentry) | — | — |

### After root-cause fixes (auth gate, hero stats reserve, deferred registerSW)

| Metric | Measured | Target | Result | Delta vs font-opt |
| --- | ---: | ---: | --- | ---: |
| Performance (mobile) | **88** | ≥ 90 | **FAIL** | +18 |
| Accessibility (mobile) | **100** | ≥ 95 | **PASS** | — |
| LCP | **3.4 s** (3364 ms) | ≤ 2.5 s | **FAIL** | +52 ms |
| CLS | **0** | ≤ 0.05 | **PASS** | −0.420 |
| FCP | **2.3 s** (2280 ms) | — | — | +4 ms |
| TBT | **126 ms** | — | — | +93 ms |
| Bundle budget | entry 44.5 KB / vendor 108.9 KB gzip | see `check-bundle-budget.mjs` | **PASS** | — |
| Initial JS transfer | 185.6 KB (5 scripts) | — | — | — |
| Observed FCP / LCP / CLS | 312 ms / 312 ms / 0 | — | — | — |

**Artifact:** `lighthouse-home-mobile-c6.json` (root-cause fix run, 2026-08-01T07:37:41Z)

### Optimization → metric attribution (root-cause pass)

| Optimization | Primary effect |
| --- | --- |
| `AuthContext` loading init from token presence | **CLS 0.420 → 0**; eliminates spinner→landing two-commit footer shift; **Performance +18** |
| Hero stats row `min-h-[5.5rem]` reserve | Prevents post-fetch counter insertion shift (no residual CLS) |
| `injectRegister: "script-defer"` | Removes `registerSW.js` from render-blocking list (was 151 ms) |

### Remaining contributors (ranked — await approval before next pass)

1. **Render-blocking CSS (~754 ms)** — `index-u8441PeS.css` blocks first paint; primary LCP lever under simulated throttling.
2. **LCP element render delay (~285 ms observed + CPU scaling)** — hero subtitle `<p>` waits on CSS parse + React paint under 4× CPU.
3. **Nav logo PNG (380 KB)** — wastes simulated bandwidth; does not cause CLS; tracked as PERF-18 follow-up.
4. **Vendor unused JS (~43%)** — secondary; larger scope.

**C6 gate:** **Not met** — Performance 88 and LCP 3.4 s still fail. CLS and Accessibility pass. Do not mark LAND-10 complete.
