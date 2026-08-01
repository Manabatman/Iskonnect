# ISKONNECT Accessibility Specification

> **Document type:** WCAG 2.2 AA compliance specification  
> **Status:** Approved specification  
> **Version:** 1.0  
> **Last updated:** 2026-08-01  
> **Target:** WCAG 2.2 Level AA on every student-facing route  
> **North star:** [PRODUCT_NARRATIVE.md](./PRODUCT_NARRATIVE.md)

---

## 1. Scope and enforcement

### Automated gates (CI)

| Tool | Scope | Gate |
| --- | --- | --- |
| axe-core (Playwright) | 12 routes | Hard fail on serious/critical |
| eslint-plugin-jsx-a11y | `ui/**` errors; legacy warnings | Errors block merge on `ui/` |
| Contrast unit test | Token values in `index.css` | CI pass |
| Touch-target probe | Core flows | Allowlist-only (242 violations inventoried) |

### Manual gates (required before public launch)

| Tool | Flows | Status |
| --- | --- | --- |
| NVDA + Chrome (Windows) | 5 critical flows | Template only — not executed |
| TalkBack + Chrome (Android) | 5 critical flows | Template only — not executed |
| 200% zoom | All student routes | Unverified |
| 400% zoom | All student routes | Unverified |

Manual pass template: `docs/engineering/a11y-manual-pass.md`

---

## 2. Global requirements

### Skip links and landmarks (A11Y-01, shipped)

- Skip link → `<main id="main-content">` on all three shells
- One `<main>` per page
- `<nav aria-label="Main navigation">` on navbar and bottom nav
- `<header>`, `<footer>` landmarks present

### Focus management (A11Y-02, shipped)

- Uniform focus ring: 2px solid, 2px offset, ≥3:1 contrast against adjacent colors
- Class: `.focus-visible-ring`
- Never `outline: none` without replacement

### Touch targets

- Minimum 44×44px on all interactive elements (`min-h-11 min-w-11`)
- WCAG 2.5.8 (24px) is floor; ISKONNECT standard is 44px (P3)

### Reduced motion

Global CSS override in `index.css`:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**Critical audit finding:** CSS-only reduced motion is insufficient when JavaScript controls motion (intervals, auto-advance). Any JS-driven animation must check `prefers-reduced-motion` and halt entirely — not degrade to hard cuts.

**Action:** Delete `HeroCarousel.tsx` (auto-rotation). Static hero has no JS motion.

### Live regions (A11Y-10, shipped)

- Search result count: polite live region via `LiveRegion` component
- Form errors: `role="alert"` on submission failure
- Toast notifications: Sonner with accessible announcements

### Color and meaning (WCAG 1.4.1)

Status badges use **icon + text label**. Color alone never carries meaning. Three `neutral`-tone lifecycle states differentiated by icon and label.

---

## 3. Per-component checklist

### Hero (static photography)

| Criterion | Requirement | Implementation |
| --- | --- | --- |
| 1.1.1 Non-text Content | Hero image has descriptive `alt` | Art-directed alt per breakpoint: "Filipino students studying together" |
| 1.4.3 Contrast | Text over image ≥4.5:1 | Scrim overlay (`--hero-scrim`); test with contrast checker |
| 1.4.11 Non-text Contrast | UI components on image ≥3:1 | Scrim ensures button contrast |
| 2.3.1 Three Flashes | No flashing content | Static image — no animation |
| 2.2.2 Pause, Stop, Hide | No auto-advancing content | No carousel — compliant by construction |

### Scholarship card (`ScholarshipCardV2`)

| Criterion | Requirement |
| --- | --- |
| 1.3.1 Info and Relationships | Card is `<article>` with labelled title via `id` |
| 2.4.4 Link Purpose | Card click opens detail; action buttons have distinct labels |
| 4.1.2 Name, Role, Value | Score ring: `role="img"` with `aria-label="{pct}% eligibility fit based on your profile"` |
| 1.4.3 Contrast | Badge text meets 4.5:1 on tone backgrounds |

**Redesign note:** Remove ambient disclaimer from card. Score ring aria-label simplified (no trailing "not your chance" clause — explanation lives in modal).

### Match analysis modal

| Criterion | Requirement |
| --- | --- |
| 2.1.2 No Keyboard Trap | Focus trap with Escape to close |
| 2.4.3 Focus Order | Focus moves to modal on open; returns to trigger on close |
| 1.3.1 | Factor breakdown as structured list |
| 1.4.3 | Disclaimer text at `body-sm` minimum (14px), not 11px |

### Search autocomplete

| Criterion | Requirement | Status |
| --- | --- | --- |
| 4.1.2 Combobox | Full ARIA combobox pattern | Shipped |
| 2.4.3 | Arrow key navigation in suggestions | Shipped |
| 1.3.1 | `role="listbox"`, `role="option"`, `aria-selected` | Shipped |

### Filter drawer (redesign)

| Criterion | Requirement |
| --- | --- |
| 2.1.2 | Focus trap in sheet; Escape closes |
| 2.4.3 | Focus moves to first filter on open |
| 1.3.1 | Filter groups use `<fieldset>` + `<legend>` |
| 2.5.8 | All filter controls ≥44px touch target |

### Bottom navigation

| Criterion | Requirement |
| --- | --- |
| 2.4.1 Bypass Blocks | Skip link bypasses bottom nav to main |
| 2.5.8 | Each nav item ≥56px height |
| 4.1.2 | `aria-current="page"` on active item |
| 2.4.11 Focus Not Obscured (AA) | Focused item not hidden by feedback FAB |

### Feedback button (redesign)

| Criterion | Requirement |
| --- | --- |
| 2.4.11 Focus Not Obscured | FAB must not cover focused bottom nav items |
| 2.5.8 | ≥44px touch target |
| 4.1.2 | `aria-label="Share feedback"` |
| Fix | Position above bottom nav: `bottom: var(--feedback-fab-offset)` |

### Notifications panel (redesign)

| Criterion | Requirement |
| --- | --- |
| 1.4.10 Reflow | Panel scrolls within viewport at 320px width |
| 2.1.2 | Focus trap when open; Escape closes |
| 1.3.1 | Notification list as `<ul>` with `<li>` |
| Fix | `max-h-[calc(100dvh-{header}px)]` with internal scroll |

### Forms (profile builder, auth)

| Criterion | Requirement |
| --- | --- |
| 1.3.1 | Every input has visible `<label>` |
| 3.3.1 Error Identification | Inline errors at field level |
| 3.3.2 Labels or Instructions | Purpose + example per field |
| 2.4.7 Focus Visible | Focus ring on all inputs |

### Glossary terms (`GlossaryTerm`)

| Criterion | Requirement |
| --- | --- |
| 4.1.2 | `<button>` with `aria-describedby` popover — not `title` attribute |
| 2.1.1 | Keyboard operable on touch devices |

---

## 4. Per-flow checklist

### Flow 1: Register and verify email

| Step | A11Y requirement |
| --- | --- |
| Register form | Labels, error identification, focus on first error |
| Email verify | Clear success/failure message with next action |
| Redirect | No unexpected focus loss |

### Flow 2: Build profile

| Step | A11Y requirement |
| --- | --- |
| Stepper | Current step announced; progress bar has `aria-valuenow` |
| Field validation | Inline errors; focus moves to first invalid field |
| Save | Success toast announced via live region |

### Flow 3: Search and filter

| Step | A11Y requirement |
| --- | --- |
| Search | Combobox pattern; result count in live region |
| Filter drawer | Focus trap; fieldset grouping |
| Results | Cards keyboard navigable; pagination announced |

### Flow 4: View matches

| Step | A11Y requirement |
| --- | --- |
| Loading | Skeleton preserves layout (no CLS) |
| Results | Score rings have aria-labels |
| Match explanation | Modal focus trap; disclaimer readable size |

### Flow 5: Save scholarship and apply

| Step | A11Y requirement |
| --- | --- |
| Save | Button state change announced |
| Detail page | Apply link is outbound with clear label |
| Official site | Disclaimer banner is `role="note"` |

---

## 5. WCAG 2.2 AA criteria matrix

Student-facing routes must pass all Level A and AA criteria. Key criteria for redesign:

| Criterion | Level | Redesign impact |
| --- | --- | --- |
| 1.4.3 Contrast (Minimum) | AA | Hero scrim; badge tone pairs verified |
| 1.4.4 Resize Text | AA | Usable at 200% zoom — no horizontal scroll |
| 1.4.10 Reflow | AA | No 2D scroll at 320px width |
| 1.4.11 Non-text Contrast | AA | Focus ring, button borders on hero |
| 2.2.2 Pause, Stop, Hide | A | No carousel auto-rotation |
| 2.4.11 Focus Not Obscured (Minimum) | AA | Feedback FAB reposition |
| 2.5.8 Target Size (Minimum) | AA | 44px targets maintained |
| 3.3.1 Error Identification | A | errorCopy.ts on all forms |

---

## 6. Manual screen reader pass (required)

Execute before public launch. Record in `docs/engineering/a11y-manual-pass.md`.

### NVDA + Chrome (Windows)

| # | Flow | Pass criteria |
| --- | --- | --- |
| 1 | Register → verify → dashboard | All steps announced; no silent failures |
| 2 | Profile builder (3 steps) | Stepper progress announced; errors readable |
| 3 | Search → filter → view detail | Combobox works; filters operable |
| 4 | Find matches → view results → open explanation | Score meaning clear; modal navigable |
| 5 | Save scholarship → view in dashboard | Save confirmed; saved list updated |

### TalkBack + Chrome (Android)

Same 5 flows on physical Android device at 360px viewport.

### Zoom verification

| Zoom | Requirement |
| --- | --- |
| 200% | All content readable; no loss of functionality |
| 400% | No horizontal scroll on any student route |

---

## 7. Redesign-specific accessibility actions

| Action | File | WCAG criterion |
| --- | --- | --- |
| Delete `HeroCarousel.tsx` | `components/HeroCarousel.tsx` | 2.2.2 |
| Add hero scrim for contrast | `HeroSection.tsx` | 1.4.3, 1.4.11 |
| Reposition feedback FAB | `FeedbackButton.tsx` | 2.4.11 |
| Add scroll container to notifications | `DashboardTopbar.tsx` | 1.4.10 |
| Unified filter drawer with fieldsets | `ScholarshipSearchFilters.tsx` | 2.1.2, 1.3.1 |
| Increase disclaimer text size in modal | `MatchAnalysisModal.tsx` | 1.4.3 |
| Remove 11px disclaimer from cards | `ScholarshipCardV2.tsx` | 1.4.3, 1.4.4 |

---

## 8. Testing protocol

### Before merge (automated)

```bash
cd frontend
npm run lint
npm run test
npm run build
npx playwright test e2e/a11y.spec.ts
```

### Before launch (manual)

1. Complete NVDA pass (5 flows)
2. Complete TalkBack pass (5 flows)
3. Verify 200% and 400% zoom on landing, search, dashboard
4. Record results in `a11y-manual-pass.md`
5. Fix any findings; re-test

---

## Document history

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-01 | Initial accessibility spec per design blueprint. |
