# ISKONNECT Design System

> **Document type:** Visual and interaction specification  
> **Status:** Approved specification  
> **Version:** 1.0  
> **Last updated:** 2026-08-01  
> **North star:** [PRODUCT_NARRATIVE.md](./PRODUCT_NARRATIVE.md)  
> **Source of truth (code):** `frontend/src/index.css`, `frontend/tailwind.config.js`, `frontend/src/components/ui/`

---

## 1. Architecture

### Token strategy (ADR-001)

CSS custom properties in `frontend/src/index.css` are the single source of truth. Tailwind maps to these via `tailwind.config.js`. New surfaces consume tokens — not ad-hoc `slate-*` for brand colors.

**Enforcement:** `npm run audit:design-tokens` runs in CI for palette utilities (DS-17) on guarded paths. Spacing scale violations (DS-10) are **enforced** repo-wide via `SPACING_LINT=enforced` in CI (Wave 9).

**Reference route:** `/design-system` (dev showcase).

### Component strategy (E4)

~21 shadcn-style primitives in `frontend/src/components/ui/`. Import from `@/components/ui/*`. Variants via CVA — never fork per page.

---

## 2. Typography

### Font strategy (ADR-003)

| Role | Family | Weights | Usage |
| --- | --- | --- | --- |
| **Body / UI / headings** | Inter (self-hosted via `@fontsource/inter`) | 400–800 | All application UI |
| **Display / brand** | Russo One (self-hosted, 400 only) | 400 | Wordmark; at most one hero heading per marketing page |

**Russo One constraints (hard rules):**

- Never for: body copy, buttons, inputs, badges, navigation, numbers (GWA, scores, deadlines), text below 20px, runs longer than six words, any authenticated surface.

### Type scale

Semantic utilities with justified sizes. Base: 16px (`1rem`) body.

| Token | Size | Line height | Weight | Usage |
| --- | --- | --- | --- | --- |
| `display` | 3.5rem (56px) | 1.1 | 800 | Landing hero only (Russo One optional) |
| `h1` | 2rem (32px) | 1.2 | 700 | Page titles |
| `h2` | 1.5rem (24px) | 1.3 | 600 | Section headings |
| `h3` | 1.25rem (20px) | 1.4 | 600 | Card titles, panel headers |
| `h4` | 1.125rem (18px) | 1.4 | 600 | Subsection labels |
| `body-lg` | 1.125rem (18px) | 1.6 | 400 | Lead paragraphs, hero subcopy |
| `body` | 1rem (16px) | 1.5 | 400 | Default UI text |
| `body-sm` | 0.875rem (14px) | 1.5 | 400 | Secondary text, metadata |
| `caption` | 0.75rem (12px) | 1.4 | 400 | Timestamps, helper text |
| `overline` | 0.75rem (12px) | 1.4 | 600 | Section labels (uppercase discouraged — use sentence case) |
| `button` | 0.875rem (14px) | 1 | 600 | Button labels |
| `label` | 0.875rem (14px) | 1.4 | 500 | Form labels |

**Responsive headings:** Use `clamp()` for hero H1: `clamp(2rem, 5vw, 3.5rem)`.

**Justification:** 16px body meets WCAG readability at 200% zoom. 14px minimum for secondary UI. 12px only for non-critical metadata — never for disclaimers or eligibility text.

**Implementation:** Encoded in `frontend/tailwind.config.js` as `fontSize` entries — use `text-display`, `text-h1`, … `text-label`. The `/design-system` route renders the full scale.

---

## 3. Spacing system

### Scale (DS-10)

4-based restricted scale. Arbitrary values (`p-[13px]`) prohibited on app routes.

| Token | Value | Tailwind |
| --- | --- | --- |
| space-1 | 4px | `1` |
| space-2 | 8px | `2` |
| space-3 | 12px | `3` |
| space-4 | 16px | `4` |
| space-5 | 20px | `5` |
| space-6 | 24px | `6` |
| space-8 | 32px | `8` |
| space-12 | 48px | `12` |
| space-16 | 64px | `16` |
| space-24 | 96px | `24` |
| space-32 | 128px | `32` |

**Mobile page gutter:** `space-4` (16px) — `px-4 sm:px-6`.

**Section vertical rhythm:** `py-12 sm:py-16 lg:py-20` (landing and content pages).

**Generous whitespace is the primary "professional" signal (P5):** when in doubt, choose the larger step.

### Enforcement (Wave 1)

- Keep Tailwind’s numeric scale (`1`–`32`); do **not** introduce named aliases (`spacing-sm`, etc.).
- `scripts/check-design-tokens.mjs` flags off-scale steps (`p-7`, `gap-10`, `m-11`) and arbitrary values (`p-[13px]`) across `frontend/src`.
- **Enforced in CI (Wave 9)** — off-scale spacing fails `npm run audit:design-tokens` when `SPACING_LINT=enforced`.

---

## 4. Grid and layout

### Container

| Context | Max width | Padding |
| --- | --- | --- |
| Marketing / public | 1200px | `px-4 sm:px-6` |
| Dashboard content | Fluid (sidebar offset) | `px-4 sm:px-6 lg:px-8` |
| Detail page | 960px (prose-friendly) | `px-4 sm:px-6` |

### Grid patterns

| Pattern | Columns | Gap |
| --- | --- | --- |
| Scholarship card grid | 1 (mobile) → 2 (md) → 3 (xl) | `gap-4 sm:gap-6` |
| Landing feature grid | 1 → 2 → 3 | `gap-6 lg:gap-8` |
| Footer | 1 → 2 → 5 | `gap-8 lg:gap-10` |
| Dashboard widgets | 1 → 2 | `gap-4 sm:gap-6` |

### Split layout

Search and profile builder use `SplitLayout`: list left, detail right on `lg+`; full-screen panel on mobile.

---

## 5. Color system

### Semantic tokens (HSL triplets)

Defined in `:root` and `.dark` in `index.css`. Used as `hsl(var(--token))`.

| Token | Light | Purpose |
| --- | --- | --- |
| `--background` | 0 0% 100% | Page background |
| `--foreground` | 222 47% 11% | Primary text |
| `--primary` | 221 83% 53% | Primary actions (#2563eb) |
| `--accent` | 25 95% 53% | Secondary emphasis (orange) |
| `--muted` | 210 40% 96% | Subtle backgrounds |
| `--border` | 214 32% 91% | Dividers, input borders |

### Extended palette

Tailwind `primary`, `accent`, `success`, `danger`, `highlight` ramps (50–950) in `tailwind.config.js`. Use semantic tokens on app routes; extended ramps for charts and illustrations only.

### Status tones

Five semantic tones. Raw palette names prohibited for status UI.

| Tone | Meaning | Examples |
| --- | --- | --- |
| `success` | Actionable now | `open`, `eligible_now`, `qualified` |
| `warning` | Caution / verification needed | `needs_verification`, `prepare_ahead` |
| `danger` | Error / blocked | form errors, `not_eligible` |
| `info` | Informational | `expected_reopen`, `opening_soon` |
| `neutral` | Inactive / reference | `closed`, `archived` |

**Rule:** Three lifecycle states share `neutral` — differentiate by **icon + label**, never color alone (WCAG 1.4.1).

**Utilities:** `.bg-tone-*`, `.text-tone-*`, `.border-tone-*`

### Match score colors

| Range | Color | Meaning |
| --- | --- | --- |
| 80–100 | `success-500` | Strong fit |
| 50–79 | `accent-500` | Moderate fit |
| 0–49 | `slate-500` | Weak fit |

Label always reads **"Eligibility fit"** — never "Match score" or "Win probability."

---

## 6. Elevation and shadows

| Token | Value | Usage |
| --- | --- | --- |
| `--shadow-1` | Subtle | `ui/card` primitive at rest, inputs, chips |
| `--shadow-2` | Default card | Interactive list cards (scholarship cards at rest) |
| `--shadow-3` | Elevated | Dropdowns, popovers |
| `--shadow-4` | Modal | Dialogs, sheets |

**Dark mode:** Elevation via surface lightness (`--card` lighter than `--background`), not shadow intensity.

---

## 7. Border radius

| Token | Value | Usage |
| --- | --- | --- |
| `--radius-sm` | 6px | Chips, badges |
| `--radius-md` | 10px | Inputs, buttons |
| `--radius-lg` | 16px | Cards |
| `--radius-xl` | 20px | Modals, hero elements |

---

## 8. Buttons

### Variants (CVA)

| Variant | Usage | Constraint |
| --- | --- | --- |
| `default` (primary) | One per view | Solid `primary-600` |
| `secondary` | Alternative actions | Outline or muted fill |
| `ghost` | Tertiary, toolbar | No fill |
| `destructive` | Delete, irreversible | `danger` tone |
| `link` | Inline navigation | Underline on hover |

### Sizes

| Size | Min height | Usage |
| --- | --- | --- |
| `sm` | 36px | Dense UI (admin) |
| `default` | 44px | Standard (WCAG touch) |
| `lg` | 48px | Hero CTAs |
| `icon` | 44×44px | Icon-only actions |

**Focus:** `.focus-visible-ring` — 2px ring, 2px offset, ≥3:1 contrast.

---

## 9. Inputs

- Height: 44px minimum (`min-h-11`)
- Border: `border-input`; focus: `ring-2 ring-ring`
- Label: always visible (no placeholder-only labels)
- Error: `tone-danger` border + inline message below field
- Combobox: full ARIA pattern on search autocomplete

---

## 10. Cards

### Scholarship card grammar (three zones)

```
┌─────────────────────────────┐
│ ZONE 1: Media               │  Hero image or gradient
│   [bookmark]    [score ring]│  Score top-right; bookmark top-left
├─────────────────────────────┤
│ ZONE 2: Identity            │  Badges (lifecycle → type → verification)
│   Title (h3, line-clamp-2)  │  Qualification badge if match data
├─────────────────────────────┤
│ ZONE 3: Metadata + actions  │  Provider, deadline, freshness
│   [Check my match] [Apply]  │  Footer actions
└─────────────────────────────┘
```

**Badge priority (overflow):** Lifecycle > Verification > Qualification > Type. Max 3 badges visible; remainder in "+N more" tooltip.

**Hover:** `translate-y-[-1px]` + `shadow-3` (180ms). Disabled when `prefers-reduced-motion`.

### Generic card (`ui/card.tsx`)

Compose with `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`, `CardFooter`.

---

## 11. Navigation

### Public navbar

- Height: 64px (scrolled: 56px)
- Sticky top; backdrop blur on scroll
- Logo: theme-aware via `brandLogoSrc()`
- Links: `body-sm`, semibold, 44px touch target

### Dashboard sidebar

- Width: 256px expanded; 64px collapsed
- Active item: `primary` background tint + left border accent
- Role-gated links at bottom

### Bottom nav (mobile)

- Fixed bottom; `z-40`
- Height: 56px + `env(safe-area-inset-bottom)`
- 4 items max; icon + label
- Active: `primary` color

---

## 12. Modals and sheets

| Pattern | Desktop | Mobile |
| --- | --- | --- |
| Dialog | Centered, max-w-lg | Full-screen or near-full |
| Sheet | Side panel | Bottom sheet, max-h 85vh |
| Match analysis | Centered dialog | Full-screen (`fixed inset-0`) |

**Focus trap:** All dialogs use focus-trapping wrappers (A11Y-07, shipped).

**Animation:** `overlayFade` + `matchDialogIn` (240ms overlay token).

---

## 13. Motion and behavior

### Principle

Animation must communicate **progress, hierarchy, or cause and effect**. If it doesn't answer **"What changed?"**, remove it.

Most student projects animate because they can. Professional products animate because they need to communicate something.

### Duration tokens (canonical)

| Intent | Token | Value | Examples |
| --- | --- | --- | --- |
| Hover, focus, small state | `--duration-fast` | 120ms | Button hover, chip toggle |
| Cards, inline expansion | `--duration-base` | 180ms | Accordion, card hover lift |
| Drawers, modals, sheets | `--duration-overlay` | 240ms | Sheet rise, dialog fade |
| Marketing scroll reveals | `--duration-reveal` | 320ms | Landing `Reveal` component |

**Do not introduce parallel scales** (e.g. hover-100ms alongside fast-120ms).

### Success / celebration

May exceed 200ms on **non-critical paths** (saved scholarship confirmation). Must be non-blocking and interruptible. Documented exception to P2 ("motion ≤200ms on critical paths").

Suggested: `--duration-celebrate: 400ms` for toast entrance only.

### Easing

| Token | Curve |
| --- | --- |
| `--ease-standard` | cubic-bezier(0.2, 0, 0, 1) |
| `--ease-out` | cubic-bezier(0, 0, 0.2, 1) |
| `--ease-in` | cubic-bezier(0.4, 0, 1, 1) |

### Reduced motion

Global override in `index.css` collapses all transitions to 0.01ms. **JavaScript intervals must also halt** — CSS-only reduced motion is insufficient for carousels or auto-advancing content.

### Landing motion (framer-motion)

- `LandingMotionProvider` wraps public marketing routes only
- `LazyMotion` + `domAnimation` subset (code-split)
- `useReducedMotion()` required in all motion components
- Prohibited: infinite decorative loops, parallax, scroll-jacking

### Match loading behavior

- Skeleton within 400ms (Doherty threshold)
- Staged result reveal (progress communication)
- No artificial delay

### Loading shimmer

Linear gradient pulse on skeleton elements. Duration: 1.5s loop. Disabled under `prefers-reduced-motion` (static skeleton).

---

## 14. Loading states

| Context | Pattern |
| --- | --- |
| Page load | Route-level skeleton (`LoadingSkeletons.tsx`) |
| Search results | 6-card skeleton grid |
| Match results | Pulse bar + skeleton cards |
| Button action | Spinner icon + label change ("Opening…") |
| Image | `animate-pulse` placeholder until loaded |

Never: blank screen, spinner-only with no layout shift prevention.

---

## 15. Empty states

Use `StateMessage` component. Required elements:

1. Plain-language headline (what happened)
2. One-sentence explanation (why)
3. One primary action (what to do next)

**Never:** "Something went wrong" alone. Never end without another action (Hope principle test).

---

## 16. Illustration and photography

### Illustration style

- Minimal, geometric when needed (auth panel backgrounds)
- No clip art, no emoji as UI icons
- Lucide React icons only

### Photography direction

**Hero (landing):**

| Breakpoint | Composition |
| --- | --- |
| Desktop | Landscape; real Filipino students; natural light; campus or home study |
| Tablet | Tighter crop; subject repositioned |
| Mobile | Portrait composition — entirely different frame, not squeezed landscape |

**Technical:** AVIF/WebP with JPEG fallback; ≤120KB per breakpoint source; explicit width/height; scrim overlay for text contrast.

**Prohibited:** Stock photo triumphalism, posed graduation caps, fake diversity, text baked into images.

### Screenshots

Device-framed product screenshots for proof strip. ≤80KB each. Captured via `docs/engineering/screenshot-capture.md`.

---

## 17. Iconography

- **Library:** Lucide React exclusively
- **Size:** 16px (inline), 20px (buttons), 24px (nav)
- **Stroke:** Default 2px; 1.5px at 16px
- **Color:** Inherit from text; status icons use tone foreground
- **Accessibility:** Icon-only buttons require `aria-label`

---

## 18. Responsive breakpoints

Tailwind defaults (not overridden):

| Breakpoint | Width | Layout shift |
| --- | --- | --- |
| default | <640px | Single column; bottom nav |
| `sm` | 640px | — |
| `md` | 768px | 2-column grids |
| `lg` | 1024px | Sidebar visible; bottom nav hidden |
| `xl` | 1280px | 3-column card grids |
| `2xl` | 1536px | — |

**Design at 360px first.** Progressive enhancement upward.

---

## 19. Dark mode

- Strategy: `darkMode: "class"` (Tailwind)
- Toggle: Settings page (Light / Dark / System)
- Persistence: `localStorage` + pre-paint script in `index.html`
- Never invert images; re-map surfaces via token swap
- Elevation: surface lightness, not shadow

---

## 20. Design tokens reference

Full token list in `frontend/src/index.css`. Layout and motion additions (Wave 1):

```css
--page-gutter: 1rem;
--section-gap: 3rem;
--card-padding: 1.5rem;
--stack-gap: 0.75rem;
--nav-height-mobile: 3.5rem;        /* 56px bottom nav */
--safe-area-bottom: env(safe-area-inset-bottom, 0px);
--feedback-fab-offset: calc(var(--nav-height-mobile) + var(--safe-area-bottom) + 1rem);
--duration-celebrate: 400ms;
--hero-scrim: linear-gradient(to top, rgb(15 23 42 / 0.7), transparent 60%);
```

Mapped in Tailwind as `spacing.page-gutter`, `spacing.section-gap`, `spacing.nav-mobile`, and `transitionDuration.celebrate`.

---

## 21. Component naming

| Pattern | Convention | Example |
| --- | --- | --- |
| Primitives | lowercase, shadcn | `button.tsx`, `dialog.tsx` |
| Feature components | PascalCase, descriptive | `ScholarshipCardV2.tsx` |
| Landing sections | `{Name}Section.tsx` | `HeroSection.tsx` |
| Layout | `{Name}Layout.tsx` | `DashboardLayout.tsx` |
| Hooks | `use{Name}.ts` | `useScholarshipSearch.ts` |
| Constants | camelCase file, SCREAMING export | `heroImages.ts` → `HERO_IMAGES` |

**Version suffix:** Use `V2` only when replacing an in-use component (`ScholarshipCardV2`). Delete old version after migration.

---

## 22. Accessibility integration

All components must meet [ACCESSIBILITY_SPEC.md](./ACCESSIBILITY_SPEC.md). Non-negotiable:

- 44×44px touch targets
- 2px focus ring with offset
- Icon + text for status (not color alone)
- `prefers-reduced-motion` honored globally
- Grade 11 reading level for user-facing copy

---

## Document history

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-01 | Initial design system spec. Consolidates Product Refinement §10, handoff §6, ADR-001/002/003. |
