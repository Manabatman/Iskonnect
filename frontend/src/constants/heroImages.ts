/**
 * Landing hero carousel — primary assets under public/images/hero/ (.jpg).
 * If a file is missing, HeroCarousel falls back to the matching SVG placeholder.
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
