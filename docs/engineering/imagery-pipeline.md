# DS-13 — Imagery pipeline

## Hero carousel
- Primary assets: `frontend/public/images/hero/hero-{1,2,3}.svg` (Phase 2 uses SVG until JPEG/WebP supplied)
- Constants: `frontend/src/constants/heroImages.ts`
- Replace files in place; alt text in `LandingPage` `heroAlts`

## Auth panels
- Primary: `frontend/public/images/auth/login-illustration.jpg`
- Fallback: `frontend/public/images/hero/hero-1.svg` via `onError` in auth pages

## Brand logos
- `frontend/public/images/logo-light.png`, `logo-dark.png`
- Resolver: `frontend/src/lib/brandLogo.ts`

## PWA
- Valid JSON manifest: `frontend/public/manifest.webmanifest`
- Icons: 512×512 PNG referenced in manifest

## Performance
- Use `loading="lazy"` / `decoding="async"` on non-LCP images
- Prefer WebP/JPEG &lt; 400 KB for hero when replacing SVGs
