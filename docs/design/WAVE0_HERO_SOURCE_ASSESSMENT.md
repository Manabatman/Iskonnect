# Wave 0 — Hero Source Crop Assessment

> **For:** Wave 3 defect D-01 (static hero photography)  
> **Sources:** Extracted from commit `009238c` into `frontend/.hero-sources/`  
> **Target mobile frame:** 768×1024 portrait (3:4) per [DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md) §16

---

## Source inventory

All three committed hero JPGs are high-resolution **3:2 landscape** photographs:

| Source | Dimensions | Megapixels | File size |
| --- | --- | ---: | ---: |
| hero-1 | 5184×3456 | 17.9 MP | 1.84 MB |
| hero-2 | 6720×4480 | 30.1 MP | 1.70 MB |
| hero-3 | 5263×3509 | 18.5 MP | 1.10 MB |

---

## Can landscape crop to mobile portrait?

**Yes — technically feasible for all three sources.**

For a 3:4 portrait crop from a 3:2 landscape image:

- Use full image height.
- Crop width = height × 0.75.
- Center horizontally.

| Source | Height | Max portrait crop width | Source width | Fits? |
| --- | ---: | ---: | ---: | --- |
| hero-1 | 3456 | 2592 | 5184 | Yes (50% width used) |
| hero-2 | 4480 | 3360 | 6720 | Yes (50% width used) |
| hero-3 | 3509 | 2632 | 5263 | Yes (50% width used) |

At export resolution 768×1024, each source provides ample pixels for sharp downscaling.

---

## Composition risk (requires human review)

Technical crop feasibility does not guarantee **subject-safe** portrait crops. Before Wave 3:

1. Open each source in an image editor.
2. Preview a center 3:4 crop at mobile safe zones (faces, text overlay area in hero).
3. Select **one primary source** for desktop/tablet/mobile art direction — not necessarily three different files.
4. Wave 3 may use hero-1 for desktop landscape and a **re-cropped hero-1** for mobile portrait rather than three separate photographs.

**Recommendation:** Use hero-1 as the primary source (smallest file, sufficient resolution). Evaluate hero-2 and hero-3 only if hero-1's subject does not survive portrait crop.

---

## Wave 3 delivery reminder

- Do **not** ship 1.9 MB JPGs to production.
- Target ≤80 KB mobile AVIF, ≤120 KB desktop AVIF per [perf-baseline.md](../engineering/perf-baseline.md).
- Delete `HeroCarousel.tsx`; static `<picture>` only.

---

## Document history

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-01 | Initial assessment at Wave 0 freeze |
