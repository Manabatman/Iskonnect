# ADR-003: Inter body + Russo One display

**Status:** Accepted (retroactive)  
**Date:** 2026-07-31  
**Phase:** 2 — Design system

## Context

Phase 1 loaded fonts from Google CDN (privacy and perf cost). Display typography needed a distinct brand voice without harming body readability.

## Decision

- **Body:** Inter, self-hosted via `@fontsource`
- **Display:** Russo One, display headings and logo wordmark only — never for long paragraphs or form labels

## Consequences

- No external font requests on first paint.
- ESLint/audit rules can flag `font-display` on non-heading elements.
- Filipino diacritics and mixed Latin scripts tested on Inter; Russo One used sparingly.

## References

- Phase 2 task DS-05
- `frontend/src/index.css` `@font-face` blocks
