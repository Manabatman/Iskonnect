# ISKONNECT Design Documentation

> Product design specification suite for the ISKONNECT student opportunity platform redesign.  
> **Status:** Approved — documentation only; implementation tracked in [UI_DEFECT_REGISTER.md](./UI_DEFECT_REGISTER.md).

---

## Read order

1. **[PRODUCT_NARRATIVE.md](./PRODUCT_NARRATIVE.md)** — North star. What ISKONNECT should *feel* like. Experience principles with falsifiable tests. Start here.

2. **[PRODUCT_DESIGN_SPEC.md](./PRODUCT_DESIGN_SPEC.md)** — Master UX spec. Journeys, IA, navigation, per-surface redesigns, prioritized roadmap.

3. **[DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md)** — Typography, color, spacing, components, motion behavior, photography direction.

4. **[CONTENT_VOICE_GUIDE.md](./CONTENT_VOICE_GUIDE.md)** — Microcopy rules, banned language, replacement copy.

5. **[ACCESSIBILITY_SPEC.md](./ACCESSIBILITY_SPEC.md)** — WCAG 2.2 AA per component and per flow.

6. **[UI_DEFECT_REGISTER.md](./UI_DEFECT_REGISTER.md)** — 11 named UI defects with file paths, fixes, and acceptance criteria.

---

## Relationship to engineering docs

| Engineering doc | Design doc connection |
| --- | --- |
| `docs/engineering/ISKONNECT_PRODUCT_REFINEMENT_MASTER_PLAN.md` §10 | Superseded for design tokens by DESIGN_SYSTEM.md |
| `docs/engineering/PROJECT_HANDOFF_PHASE1_TO_PHASE3.md` §6 | Superseded for design system by DESIGN_SYSTEM.md |
| `docs/engineering/perf-baseline.md` | Hero photography budget (§ Design blueprint) |
| `docs/engineering/benchmarks/lighthouse-c6-runbook.md` | Re-measurement protocol after D-01 |
| `docs/engineering/catalog-readiness.md` | Operational catalog targets (not in design docs) |
| ADR-001, ADR-002, ADR-003 | Referenced by DESIGN_SYSTEM.md |

---

## Implementation

Do not implement from this README. Use the defect register:

| Priority | Defect IDs |
| --- | --- |
| High | D-01, D-06, D-08, D-09, D-10, D-11 |
| Medium | D-02, D-03, D-05, D-07 |
| Low | D-04 |

Each defect in [UI_DEFECT_REGISTER.md](./UI_DEFECT_REGISTER.md) maps to exact files and acceptance criteria.

---

## Version

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-01 | Initial design documentation suite. |

---

## Implementation waves

Wave 0 freeze record: [WAVE0_GATE_RESULTS.md](../engineering/WAVE0_GATE_RESULTS.md)

Pre-checkpoint SHA (hero JPG recovery): **`009238c`**

Hero crop assessment: [WAVE0_HERO_SOURCE_ASSESSMENT.md](./WAVE0_HERO_SOURCE_ASSESSMENT.md)

Implementation branch: **`feature/design-system-v1`**
