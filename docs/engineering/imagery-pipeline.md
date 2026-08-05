# DS-13 — Imagery pipeline

## Landing hero (D-01)

- **Source:** `frontend/.hero-sources/hero-1.jpg` (extract from git `009238c` if missing)
- **Generate:** `cd frontend && npm run generate:hero-images`
- **Output:** `frontend/public/images/hero/hero-{mobile,tablet,desktop}.{avif,webp,jpg}`
- **Constants:** `frontend/src/constants/heroImages.ts`
- **Component:** `HeroSection.tsx` — static `<picture>`, no carousel
- **Preload:** `frontend/index.html` — one AVIF per breakpoint via `media` attribute

Budget targets: ≤80 KB mobile AVIF, ≤100 KB tablet, ≤120 KB desktop (see `docs/engineering/perf-baseline.md`).

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
- Hero LCP: `fetchpriority="high"`, explicit `width`/`height`, `loading="eager"`
