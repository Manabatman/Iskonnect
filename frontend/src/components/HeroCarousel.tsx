import { useEffect, useState } from "react";
import { HERO_CAROUSEL_FALLBACK_SVGS, HERO_CAROUSEL_HEIGHT, HERO_CAROUSEL_INTERVAL_MS, HERO_CAROUSEL_WIDTH } from "../constants/heroImages";

interface HeroCarouselProps {
  images: readonly string[];
  /** Alt text per slide (same length as images). */
  alts: readonly string[];
  className?: string;
}

/**
 * Full-bleed background carousel with crossfade between slides.
 * Parent should be `relative` with a defined min-height; this component uses `absolute inset-0`.
 */
export function HeroCarousel({ images, alts, className = "" }: HeroCarouselProps) {
  const [index, setIndex] = useState(0);
  /** 0 = primary image, 1 = SVG fallback, 2+ = omit layer (both failed) */
  const [loadAttemptByIndex, setLoadAttemptByIndex] = useState<Record<number, number>>({});

  useEffect(() => {
    if (images.length <= 1) return undefined;
    const id = window.setInterval(() => {
      setIndex((i) => (i + 1) % images.length);
    }, HERO_CAROUSEL_INTERVAL_MS);
    return () => window.clearInterval(id);
  }, [images.length]);

  return (
    <div className={`absolute inset-0 ${className}`} aria-hidden>
      {images.map((primarySrc, i) => {
        const fallback = HERO_CAROUSEL_FALLBACK_SVGS[i];
        const attempt = loadAttemptByIndex[i] ?? 0;
        const src =
          attempt === 0 ? primarySrc : attempt === 1 && fallback ? fallback : null;

        if (!src) {
          return null;
        }

        return (
          <img
            key={`${i}-${attempt}`}
            src={src}
            alt=""
            width={HERO_CAROUSEL_WIDTH}
            height={HERO_CAROUSEL_HEIGHT}
            decoding="async"
            fetchPriority={i === index ? "high" : undefined}
            loading={i === index ? "eager" : "lazy"}
            onError={() => {
              setLoadAttemptByIndex((prev) => {
                const a = prev[i] ?? 0;
                if (a >= 2) return prev;
                return { ...prev, [i]: a + 1 };
              });
            }}
            className={`absolute inset-0 h-full w-full object-cover object-[50%_35%] transition-opacity duration-1000 ease-in-out md:object-center ${
              i === index ? "opacity-100" : "opacity-0"
            }`}
          />
        );
      })}
      {/* Screen-reader: describe current slide only */}
      <span className="sr-only">{alts[index] ?? ""}</span>
    </div>
  );
}
