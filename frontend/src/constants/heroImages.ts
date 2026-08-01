/**
 * Landing hero carousel — SVG placeholders under public/images/hero/.
 * HeroCarousel falls back to the matching SVG if a primary asset fails to load.
 *
 * Alt text for each slide is set in LandingPage `heroAlts` (same order as this array).
 */
export const HERO_CAROUSEL_IMAGES = [
  "/images/hero/hero-1.svg",
  "/images/hero/hero-2.svg",
  "/images/hero/hero-3.svg",
] as const;

/** Same order as HERO_CAROUSEL_IMAGES — used when primary image fails to load. */
export const HERO_CAROUSEL_FALLBACK_SVGS = [
  "/images/hero/hero-1.svg",
  "/images/hero/hero-2.svg",
  "/images/hero/hero-3.svg",
] as const;

/** Milliseconds between slide transitions (white fade happens inside the carousel). */
export const HERO_CAROUSEL_INTERVAL_MS = 5000;

/** Intrinsic dimensions for hero slides (16:9) — prevents CLS while SVG/JPEG loads. */
export const HERO_CAROUSEL_WIDTH = 1920;
export const HERO_CAROUSEL_HEIGHT = 1080;
