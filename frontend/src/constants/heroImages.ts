/**
 * Static landing hero photography (AVIF/WebP + PNG fallback in public/images/hero/).
 */
export const HERO_IMAGE_ALT = "Filipino students in graduation caps celebrating achievement";

export type HeroBreakpointAssets = {
  width: number;
  height: number;
  media: string;
  avif: string;
  webp: string;
  png: string;
};

export const HERO_BREAKPOINTS: {
  mobile: HeroBreakpointAssets;
  tablet: HeroBreakpointAssets;
  desktop: HeroBreakpointAssets;
} = {
  mobile: {
    width: 768,
    height: 1024,
    media: "(max-width: 767px)",
    avif: "/images/hero/hero-mobile.avif",
    webp: "/images/hero/hero-mobile.webp",
    png: "/images/hero/hero-mobile.png",
  },
  tablet: {
    width: 1024,
    height: 768,
    media: "(min-width: 768px) and (max-width: 1023px)",
    avif: "/images/hero/hero-tablet.avif",
    webp: "/images/hero/hero-tablet.webp",
    png: "/images/hero/hero-tablet.png",
  },
  desktop: {
    width: 1920,
    height: 1080,
    media: "(min-width: 1024px)",
    avif: "/images/hero/hero-desktop.avif",
    webp: "/images/hero/hero-desktop.webp",
    png: "/images/hero/hero-desktop.png",
  },
};

/** Auth panel fallback when login illustration fails. */
export const HERO_FALLBACK_SVG = "/images/hero/hero-1.svg";
