# ISKONNECT UI Defect Register

> **Document type:** Implementation defect tracker with acceptance criteria  
> **Status:** Active  
> **Version:** 1.0  
> **Last updated:** 2026-08-01  
> **Spec authority:** [PRODUCT_DESIGN_SPEC.md](./PRODUCT_DESIGN_SPEC.md)

Each defect includes: Problem, Evidence, UX Principle, Alternatives, Chosen Solution, Trade-offs, Complexity, Impact, and Decision/Hypothesis/Metric/Rollback where contested.

---

## Summary

| ID | Defect | Priority | Complexity |
| --- | --- | --- | --- |
| D-01 | Hero lacks photography | High | Medium |
| D-02 | Proof strip CSS placeholders | Medium | Low |
| D-03 | Technical landing copy | Medium | Low |
| D-04 | Footer rhythm inconsistent | Low | Low |
| D-05 | FAQ in primary nav | Medium | Low |
| D-06 | Feedback FAB over bottom nav | High | Low |
| D-07 | Notifications panel overflow | Medium | Low |
| D-08 | Ambient disclaimer repetition | High | Medium |
| D-09 | Card header badge overlap | High | Medium |
| D-10 | Search competing primaries | High | Medium |
| D-11 | Duplicate mobile filter UI | High | Low |

---

## D-01: Hero lacks photography

### Problem
Landing hero feels informational rather than aspirational. On-disk version uses CSS product mock; users previously responded well to photographic hero.

### Evidence
- `frontend/src/components/landing/HeroSection.tsx` — gradient + CSS mock (uncommitted)
- `frontend/src/components/HeroCarousel.tsx` — orphaned, zero imports
- `public/images/hero/` — three SVG placeholders (~625 bytes each)

### UX Principle
Trust + Growth — credible, warm first impression.

### Alternatives Considered
1. Restore auto-rotating carousel — rejected (WCAG 2.2.2, LCP cost, reduced-motion hard-cut)
2. CSS-only hero — current state; lacks warmth
3. **Static art-directed photography per breakpoint** — chosen

### Chosen Solution
- Delete `HeroCarousel.tsx` and carousel constants in `heroImages.ts`
- Implement `<picture>` with three compositions: desktop landscape, tablet crop, mobile portrait
- AVIF/WebP + JPEG fallback; ≤120KB per source; preload LCP candidate
- Scrim overlay for text contrast
- Photography brief: real Filipino students, natural light

### Trade-offs
Adds image weight to LCP path. Mitigated by single image (not three rotating) and modern formats.

### Complexity
Medium — asset pipeline, responsive art direction, contrast testing.

### Expected Impact
Landing credibility increases; LCP may improve vs carousel if optimized.

### Decision Record
- **Decision:** Static hero, three breakpoint compositions
- **Hypothesis:** One strong image per device feels premium and loads faster
- **Metric:** LCP ≤ 2.5s; Lighthouse mobile ≥ 90
- **Rollback:** Revert to CSS hero if LCP fails after optimization

### Acceptance Criteria
- [ ] Hero displays photograph on all breakpoints (not CSS mock)
- [ ] Mobile uses portrait composition distinct from desktop
- [ ] Text contrast ≥4.5:1 over image with scrim
- [ ] LCP element is hero image with `fetchpriority="high"`
- [ ] `HeroCarousel.tsx` deleted
- [ ] No auto-rotating content (WCAG 2.2.2)
- [ ] CLS remains 0

---

## D-02: Proof strip CSS placeholders

### Problem
"See the product" section shows CSS skeleton frames instead of product screenshots, failing to demonstrate value.

### Evidence
- `frontend/src/components/landing/ProofStripSection.tsx:5-27` — `ProofFrame` renders colored bars and gray rectangles
- Eyebrow "See the product" at line ~32

### UX Principle
Trust — show, don't claim.

### Alternatives
1. Keep CSS frames — fails "See the product" promise
2. **Device-framed screenshots or labeled placeholders** — chosen

### Chosen Solution
- Remove eyebrow text
- Replace `ProofFrame` with `<img>` in device frame chrome (or labeled "Screenshot coming soon" frame)
- Capture via `docs/engineering/screenshot-capture.md`
- Update copy per CONTENT_VOICE_GUIDE §8

### Complexity
Low (with screenshots) / Medium (if screenshots need staging environment)

### Acceptance Criteria
- [ ] No CSS skeleton bars in proof strip
- [ ] Four frames show recognizable product UI or labeled placeholders
- [ ] Eyebrow "See the product" removed
- [ ] Captions describe student outcomes, not internal mechanics

---

## D-03: Technical landing copy

### Problem
Landing copy references internal product mechanics rather than student outcomes.

### Evidence
- `ProofStripSection.tsx` — "Every screen is built around eligibility fit—not catalog volume"
- Various landing sections in `landingData.ts`

### UX Principle
Clarity beats cleverness (Pillar 1); Grade 11 reading level (P8).

### Chosen Solution
Rewrite all landing section copy per [CONTENT_VOICE_GUIDE.md](./CONTENT_VOICE_GUIDE.md) §7–8.

### Complexity
Low

### Acceptance Criteria
- [ ] No technical jargon in landing copy
- [ ] Hero, proof strip, benefits, FAQ use student-outcome framing
- [ ] `npm run audit:dev-strings` passes

---

## D-04: Footer rhythm inconsistent

### Problem
Footer vertical padding and grid gaps feel disproportionate compared to page sections.

### Evidence
- `frontend/src/components/Footer.tsx:60` — `py-12 sm:py-16`
- Landing sections — `py-12 sm:py-16 lg:py-24 xl:py-32` (`Section.tsx:36`)
- `id="about"` on footer (misleading — About is `/about`)

### UX Principle
Professional over flashy (P5) — consistent rhythm.

### Chosen Solution
- Align footer padding to `py-10 sm:py-12`
- Reduce column gap to `gap-8`
- Remove or rename `id="about"` to `id="site-footer"`

### Complexity
Low

### Acceptance Criteria
- [ ] Footer visual weight proportional to content above
- [ ] No misleading `id="about"`
- [ ] Tablet 2-column grid balanced (brand column span fixed)

---

## D-05: FAQ in primary nav

### Problem
FAQ in primary nav adds a fourth item when FAQ content already exists on landing and in footer.

### Evidence
- `frontend/src/components/Navbar.tsx:56-65` — FAQ nav item to `/faq`
- `frontend/src/components/landing/FaqSection.tsx` — 5 items + "View all FAQs"
- FAQ not in footer currently

### UX Principle
Simplicity (P9) — fewer nav decisions (Hick's Law).

### Chosen Solution
- Remove FAQ from `navItems` array
- Add FAQ link to footer Company column
- Keep `/faq` route and landing FAQ section

### Complexity
Low

### Decision Record
- **Metric:** FAQ page traffic via footer vs nav
- **Rollback:** Restore nav item if FAQ traffic drops >50% without footer offset

### Acceptance Criteria
- [ ] Navbar shows 3 items: Scholarships, How it works, Transparency
- [ ] FAQ link in footer Company column
- [ ] Landing FAQ section unchanged
- [ ] `/faq` route still accessible

---

## D-06: Feedback FAB over bottom nav

### Problem
Floating "Share Feedback" button overlaps mobile bottom navigation, obstructing Settings.

### Evidence
- `frontend/src/components/FeedbackButton.tsx:32` — `fixed bottom-6 right-6 z-50`
- `frontend/src/components/layout/BottomNav.tsx:16` — `fixed bottom-0 z-40`, ~56px + safe-area
- Missing from `AdaptiveSearchLayout` when logged in on search

### UX Principle
Mobile-first (P3); WCAG 2.4.11 Focus Not Obscured.

### Chosen Solution
- Add CSS tokens: `--nav-height-mobile`, `--feedback-fab-offset`
- Position FAB: `bottom: var(--feedback-fab-offset)` on mobile
- Collapse to icon-only on mobile (hide "Share Feedback" text)
- Mount in `AdaptiveSearchLayout` for logged-in search

### Complexity
Low

### Acceptance Criteria
- [ ] FAB never overlaps bottom nav items at 360px viewport
- [ ] FAB visible on authenticated search page
- [ ] Focused bottom nav item not obscured by FAB
- [ ] Safe-area inset respected on notched devices

---

## D-07: Notifications panel overflow

### Problem
Notifications dropdown has no max-height or scroll, causing long lists to extend past viewport.

### Evidence
- `frontend/src/components/layout/DashboardTopbar.tsx:391-392` — `absolute right-0 w-80 max-w-[calc(100vw-2rem)]`, no `max-h`

### UX Principle
Mobile-first (P3); WCAG 1.4.10 Reflow.

### Chosen Solution
- Add `max-h-[min(24rem,calc(100dvh-5rem))]` with `overflow-y-auto`
- Below `sm`: convert to bottom sheet pattern
- Focus trap when open

### Complexity
Low

### Acceptance Criteria
- [ ] Panel scrolls internally when content exceeds viewport
- [ ] Usable at 320px width
- [ ] Escape closes panel
- [ ] Focus trapped within panel when open

---

## D-08: Ambient disclaimer repetition

### Problem
"ISKONNECT estimate — the provider decides who is accepted" appears on every card, badge tooltip, dashboard, and score ring — creating visual noise and habituation.

### Evidence
- `frontend/src/components/MatchConfidenceNote.tsx:4-5` — `MATCH_CONFIDENCE_COMPACT`
- Call sites:
  - `ScholarshipCardV2.tsx:239`
  - `MatchAnalysisModal.tsx:170`
  - `QualificationStatusBadge.tsx:4,44`
  - `ProfileDashboard.tsx:581`
  - `MatchScoreRing.tsx:27` (aria-label clause)

### UX Principle
Transparency over persuasion (Pillar 4) — transparency where sought, not everywhere.

### Alternatives
1. Keep on all surfaces — current; causes noise
2. Delete entirely — loses in-product uncertainty signal
3. **Relocate to match-explanation surfaces only** — chosen

### Chosen Solution
- Remove from: card hero, badge tooltip, dashboard rings, score ring aria trailing clause
- Redesign in `MatchAnalysisModal.tsx` as calm two-sentence copy after factor breakdown
- Optional one-line link on `MatchResultsPage.tsx` header
- Refactor `MatchConfidenceNote` to single `explanation` variant
- Delete `MATCH_CONFIDENCE_COMPACT` string
- Retain on legal/explainer pages: `/terms`, `/how-matching-works`, `/how-we-verify`, `/scholarship-status`, `TrustSection`

### Complexity
Medium — 6 call sites + copy rewrite + test update

### Decision Record
- **Hypothesis:** Students who seek explanations read it; ambient repetition causes habituation
- **Metric:** Support tickets citing score-as-acceptance; modal open rate
- **Rollback:** Restore one instance at Apply on detail page if confusion rises

### Acceptance Criteria
- [ ] No disclaimer text on scholarship cards
- [ ] No disclaimer in badge tooltips
- [ ] Match analysis modal shows two-sentence non-guarantee copy at readable size (≥14px)
- [ ] Legal/explainer pages unchanged
- [ ] `trustRoutes.test.tsx` still passes

---

## D-09: Card header badge overlap

### Problem
Badges, eligibility labels, and match percentage compete for space in card header overlay.

### Evidence
- `frontend/src/components/ScholarshipCardV2.tsx:233-241` — score block `max-w-[9.5rem]` with ring + label + disclaimer
- Badge row `flex-wrap` at lines 245-252 with no priority ordering

### UX Principle
Clarity beats cleverness — readable hierarchy.

### Chosen Solution
Implement three-zone card grammar (DESIGN_SYSTEM §10):
- Zone 1: Media with score ring (no disclaimer text)
- Zone 2: Badges with priority (Lifecycle > Verification > Qualification > Type)
- Zone 3: Metadata + actions
- Max 3 visible badges; overflow to "+N more"

### Complexity
Medium

### Acceptance Criteria
- [ ] Score ring, badges, and title never overlap at 360px
- [ ] Badge priority documented and enforced
- [ ] No text below 12px on card
- [ ] Hover state does not cause layout shift

---

## D-10: Search competing primaries

### Problem
"Find My Matches" and "Complete Your Profile" are equally weighted solid buttons before any search results appear.

### Evidence
- `frontend/src/pages/ScholarshipSearchPage.tsx:254-268` — accent + primary solid buttons
- Helper text at lines 296-300 explains difference — users shouldn't need to read helper text

### UX Principle
One primary action per view (P9); progressive disclosure.

### Chosen Solution
- Search input is the visual primary
- "Find My Matches" — single contextual solid button (hidden if no profile)
- "Complete Your Profile" — inline text link
- Add sort control
- Simplify helper text

### Complexity
Medium

### Acceptance Criteria
- [ ] Only one solid button in search header at a time
- [ ] Search input visible above fold on 360px mobile
- [ ] Sort control present
- [ ] Helper text ≤1 line or removed

---

## D-11: Duplicate mobile filter UI

### Problem
Tapping "Filters" on mobile opens a full-screen overlay that contains another "Filters" sheet trigger.

### Evidence
- `ScholarshipSearchPage.tsx:302-328` — page-level full-screen overlay
- `ScholarshipSearchFilters.tsx:380-401` — inner Sheet trigger (also `lg:hidden`)

### UX Principle
Simplicity — one path to filters.

### Chosen Solution
- Delete page-level overlay (`mobileFiltersOpen` state and JSX)
- Add `variant="sidebar" | "drawer"` prop to `ScholarshipSearchFilters`
- Mobile: expose drawer trigger at page level OR let component own trigger (not both)
- Desktop: unchanged sidebar

### Complexity
Low

### Acceptance Criteria
- [ ] One tap from search page to filter drawer on mobile
- [ ] No nested "Filters" button inside filter overlay
- [ ] Desktop sidebar unchanged
- [ ] Active filter count visible on trigger button
- [ ] Focus trapped in drawer; Escape closes

---

## Implementation order

Recommended sequence (dependencies noted):

```
D-11 (filters) ──┐
D-10 (search CTAs) ──┤
D-08 (disclaimer) ──┼── D-09 (card header) ── parallel after D-08
D-06 (FAB) ─────────┤
D-07 (notifications) ┤
D-05 (nav) ──────────┤
D-01 (hero) ─────────┤── independent
D-02 (proof strip) ──┤── after D-01 (needs product screenshots)
D-03 (copy) ─────────┤
D-04 (footer) ───────┘
```

---

## Document history

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-01 | Initial defect register with 11 named issues. |
