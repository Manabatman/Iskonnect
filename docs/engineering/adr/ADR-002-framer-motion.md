# ADR-002: framer-motion over anime.js

**Status:** Accepted (retroactive)  
**Date:** 2026-07-31  
**Phase:** 2 — Design system

## Context

Landing page motion needed a React-friendly animation library with reduced-motion support.

## Decision

Adopt **framer-motion** (`LazyMotion` + `domAnimation` subset) for landing reveals and dialog transitions. Do not add anime.js or CSS-only infinite decorative loops.

## Consequences

- `LandingMotionProvider` wraps public marketing routes only.
- Unused motion utilities (`lib/motion.ts`) were removed in Phase 3 SUBTRACT-02.
- All motion must respect `prefers-reduced-motion`.

## References

- `frontend/src/components/landing/LandingMotionProvider.tsx`
- ADR-001 (motion duration tokens)
