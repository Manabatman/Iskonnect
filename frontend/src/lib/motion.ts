/** Seconds — mirrors CSS `--duration-*` tokens in index.css */
export const MOTION_DURATION_S = {
  fast: 0.12,
  base: 0.18,
  overlay: 0.24,
  reveal: 0.32,
  celebrate: 0.4,
} as const;

/** Milliseconds — for requestAnimationFrame / setInterval timing */
export const MOTION_DURATION_MS = {
  fast: 120,
  base: 180,
  overlay: 240,
  reveal: 320,
  celebrate: 400,
} as const;
