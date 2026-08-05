# ADR-001: CSS variable design tokens

**Status:** Accepted (retroactive)  
**Date:** 2026-07-31  
**Phase:** 2 — Design system

## Context

Phase 1 used scattered Tailwind literals. Phase 2 needed a single token layer for theming, contrast testing, and CI enforcement.

## Decision

Use **CSS custom properties** in `frontend/src/index.css` as the source of truth for color, spacing, radius, and motion. Tailwind maps to these variables via `tailwind.config.js`.

## Consequences

- Dark mode toggles variables, not duplicated class strings.
- `audit:design-tokens` CI guard can fail on raw hex outside allowlist.
- New surfaces must consume tokens, not ad-hoc `slate-*` for brand colors.

## References

- Phase 2 tasks DS-01, DS-02
- `docs/engineering/benchmarks/` Lighthouse baselines
