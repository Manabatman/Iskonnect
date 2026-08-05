# Lighthouse baseline — Phase 2 exit (2026-07-31)

Production build served locally via `npm run preview` on `http://127.0.0.1:4173/`.  
Tool: Lighthouse 12.8.2 (Edge headless). Raw JSON in this folder.

## Summary scores (0–100)

| Route | Form factor | Performance | Accessibility | Best Practices | SEO |
| --- | --- | ---: | ---: | ---: | ---: |
| `/` (landing) | Mobile | **67** | 96 | 96 | 83 |
| `/` (landing) | Desktop | **80** | 96 | 96 | 83 |
| `/login` | Mobile | **83** | 96 | 96 | 83 |
| `/login` | Desktop | **97** | 96 | 96 | 83 |
| `/scholarships/search` | Mobile | **67** | 91 | 96 | 83 |
| `/scholarships/search` | Desktop | **97** | 90 | 96 | 83 |

## Observations

- **Accessibility** is strong (90–96) across routes — aligns with Phase 2 touch-target and token work.
- **Best Practices** stable at 96.
- **SEO** flat at 83 — likely meta/description/structured-data gaps; revisit in a dedicated SEO pass.
- **Performance** on mobile landing/search (**67**) is the main regression target for Phase 3 — bundle size (~813 KB main chunk at build) and hero assets are prime suspects.
- Desktop performance on auth/search routes is excellent (**97**); landing desktop moderate (**80**).

## Re-run

```bash
cd frontend
npm run build && npm run preview
# In another terminal (Edge on Windows):
npx lighthouse http://127.0.0.1:4173/ --chrome-path="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --output=json --output-path=../docs/engineering/benchmarks/lighthouse-home-mobile.json
npx lighthouse http://127.0.0.1:4173/ --preset=desktop --chrome-path="..." --output=json --output-path=../docs/engineering/benchmarks/lighthouse-home-desktop.json
```

Compare future runs against this table before declaring Phase 3 complete.

## Raw artifacts

- `lighthouse-home-mobile.json` / `lighthouse-home-desktop.json`
- `lighthouse-login-mobile.json` / `lighthouse-login-desktop.json`
- `lighthouse-search-mobile.json` / `lighthouse-search-desktop.json`
