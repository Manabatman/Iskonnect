import { type Variants } from "framer-motion";

const reducedMotion =
  typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

export const motionDuration = {
  fast: reducedMotion ? 0 : 0.12,
  base: reducedMotion ? 0 : 0.18,
  overlay: reducedMotion ? 0 : 0.24,
  reveal: reducedMotion ? 0 : 0.32,
} as const;

export const fadeInUp: Variants = {
  hidden: { opacity: 0, y: reducedMotion ? 0 : 12 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: motionDuration.reveal, ease: [0.2, 0, 0, 1] },
  },
};

export const scaleIn: Variants = {
  hidden: { opacity: 0, scale: reducedMotion ? 1 : 0.96 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { duration: motionDuration.overlay, ease: [0, 0, 0.2, 1] },
  },
};

export const staggerContainer: Variants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: reducedMotion ? 0 : 0.06 },
  },
};
