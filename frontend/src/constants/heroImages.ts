/**
 * Landing hero carousel — primary assets under public/images/hero/ (.jpg).
 * If a file is missing, HeroCarousel falls back to the matching SVG placeholder.
 *
 * ## Replacing images (no code change required)
 * Swap files in place keeping the same filenames:
 * - hero-1.jpeg — graduates / celebration (recommended 1920×1080 or 16:9, &lt; 400 KB WebP/JPEG)
 * - hero-2.jpg — ceremony / campus wide shot
 * - hero-3.jpg — inspirational campus or student life
 *
 * Alt text for each slide is set in LandingPage `heroAlts` (same order as this array).
 */
export const HERO_CAROUSEL_IMAGES = [
  "/images/hero/hero-1.jpg",
  "/images/hero/hero-2.jpg",
  "/images/hero/hero-3.jpg",
] as const;

/** Same order as HERO_CAROUSEL_IMAGES — used when primary image fails to load. */
export const HERO_CAROUSEL_FALLBACK_SVGS = [
  "/images/hero/hero-1.svg",
  "/images/hero/hero-2.svg",
  "/images/hero/hero-3.svg",
] as const;

/** Milliseconds between slide transitions (white fade happens inside the carousel). */
export const HERO_CAROUSEL_INTERVAL_MS = 5000;
