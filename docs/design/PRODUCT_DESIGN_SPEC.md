# ISKONNECT Product Design Specification

> **Document type:** Master UX specification  
> **Status:** Approved specification  
> **Version:** 1.0  
> **Last updated:** 2026-08-01  
> **North star:** [PRODUCT_NARRATIVE.md](./PRODUCT_NARRATIVE.md) — read that first.

---

## Executive summary

ISKONNECT is a scholarship discovery and matching platform for Filipino students. This specification defines a product-wide redesign that makes ISKONNECT the most trustworthy, intuitive, and aspirational student opportunity platform in the Philippines — starting with scholarships and expanding into a unified career companion.

**What this redesign solves:** The product is functionally complete but emotionally incomplete. Users report it reads as informative rather than authoritative, navigation buries the primary task, mobile chrome overlaps, match disclaimers create visual noise through repetition, and future opportunity categories feel like absences rather than intentions.

**What this redesign preserves:** Phase 3 trust infrastructure — refresh-token rotation, eligibility fail-closed behavior, RA 10173 export/delete, the `FieldEvidence` provenance model, honest empty states, and the design token layer in `frontend/src/index.css`.

**Catalog quality:** The long-term value of ISKONNECT depends on both experience quality and catalog quality. UX improvements cannot compensate for an insufficient breadth of verified opportunities. Product growth and catalog growth must progress together. Operational targets: `docs/engineering/catalog-readiness.md`.

---

## Decision log

These decisions reverse or revise prior Phase 3 work. Each includes Decision → Hypothesis → Metric → Rollback.

| # | Decision | Hypothesis | Metric | Rollback |
| --- | --- | --- | --- | --- |
| D1 | Static hero photography (3 breakpoint compositions); delete `HeroCarousel.tsx` | One strong art-directed image per device feels premium and loads faster than rotation | LCP ≤ 2.5s; Lighthouse mobile ≥ 90; qualitative "official-looking" in PAT | Restore carousel only if static hero fails LCP gate after optimization |
| D2 | Relocate match disclaimer from cards to match-explanation surfaces | Students who seek explanations read it; ambient repetition causes habituation | Support tickets citing score-as-acceptance; modal open rate on "Why did I match?" | Restore one instance at Apply on detail page if confusion rises |
| D3 | Remove FAQ from primary nav; keep in footer + landing section | Fewer nav items improve task focus (Hick's Law) | Nav click distribution; task completion time to search | Restore if FAQ page traffic drops >50% without footer offset |
| D4 | Landing redesign ahead of Phase 4 sequencing | Design system is stable enough; landing is primary acquisition surface | Lighthouse landing; registration conversion | Defer if token migration incomplete on landing components |
| D5 | Extend motion tokens, do not replace | One timing scale prevents drift | Zero new arbitrary `duration-*` values in PRs | N/A — additive only |

---

## Product vision statement

**Today:** Students find scholarships they are actually eligible for — verified, explained, actionable.

**Tomorrow:** ISKONNECT becomes the career companion that grows with them — from senior high through scholarships, internships, competitions, research, and beyond.

Every interaction reinforces: *you joined early in something meaningful* — through dated roadmap evidence, not hype.

---

## UX critique of current experience

### What works (do not rewrite)

| Area | Evidence |
| --- | --- |
| Match engine transparency | Factor breakdown in `MatchAnalysisModal`; scoring policy link |
| Trust surfaces on detail page | `TrustCard`, freshness chips, field evidence |
| Design token foundation | `index.css` semantic tokens; shadcn/ui primitives |
| Phase 3 honesty | `errorCopy.ts`, `glossary.ts`, fail-closed unknown status |
| Adaptive search layout | Logged-in users get dashboard shell on search |
| Accessibility infrastructure | Skip links, landmarks, axe CI gate on 12 routes |

### Critical gaps

| Gap | User impact | Evidence |
| --- | --- | --- |
| **Competing primaries on search** | User doesn't know whether to search, match, or complete profile first | Two solid buttons before any results (`ScholarshipSearchPage.tsx:255-268`) |
| **Duplicate mobile filters** | Tapping Filters opens a screen with another Filters button | Page overlay + inner Sheet (`ScholarshipSearchFilters.tsx:380-401`) |
| **Card header overlap** | Badges, score ring, and disclaimer compete in 152px overlay | `ScholarshipCardV2.tsx:233-241` |
| **Ambient disclaimer repetition** | 11px text on every card; users stop reading | `MatchConfidenceNote` on 6 surfaces |
| **Feedback FAB over bottom nav** | Obstructs Settings on mobile dashboard | `FeedbackButton.tsx:29-37` vs `BottomNav.tsx:15-18` |
| **"Coming soon" disappointment** | Future opportunities feel unfinished | `OpportunityComingSoonPage.tsx` eyebrow + "Why it's not live yet" |
| **Landing lacks warmth** | On-disk hero uses CSS mock; committed HEAD had carousel (removed for perf) | `HeroSection.tsx` uncommitted state |
| **Proof strip placeholders** | "See the product" shows CSS skeletons, not product | `ProofStripSection.tsx` untracked |
| **No sort on search** | Users cannot reorder results | `useScholarshipSearch.ts` — no sort param |
| **Footer rhythm inconsistent** | Vertical padding half of mid-page sections | `Footer.tsx:60` vs `Section.tsx:36` |

---

## User journey maps

### Journey 1: Guest from Google

**Persona:** Undergraduate, searches "DOST scholarship 2026," lands on ISKONNECT.

```
Google result → Scholarship detail OR Landing
       ↓
Browse search (no account required)
       ↓
See eligibility summary (limited without profile)
       ↓
"Check my match" on card → preview modal
       ↓
Decision: register to save OR apply via official link
```

| Stage | Emotion target | Current friction | Redesign |
| --- | --- | --- | --- |
| Land | Curiosity → Trust | Landing may redirect logged-in users; hero lacks photography | Static hero photo; search CTA above fold |
| Browse | Confidence | Two competing CTAs before results | Search-first; contextual match CTA |
| Understand | Confidence | Disclaimer on every card | Disclaimer only in match explanation |
| Act | Progress | Unclear register value | Show what registration unlocks inline |

### Journey 2: First-time registrant

```
Landing/register → Email verify → Profile builder (41 fields)
       ↓
First match run → Match results
       ↓
Save scholarship → Dashboard
```

| Stage | Emotion target | Current friction | Redesign |
| --- | --- | --- | --- |
| Register | Trust | Tagline may feel generic | Mentor-voice copy; preserve draft across registration (TRUST-01, shipped) |
| Profile | Progress | Long wizard; unclear field purpose | Step validation; each field shows what it unlocks |
| First match | Hope | Loading skeleton only | Staged reveal; optimistic shell |
| Dashboard | Growth | Opportunity journey not visible | Subtle roadmap reminder; next deadline action |

### Journey 3: Returning student

```
Dashboard → Check deadlines / new matches
       ↓
Search with saved filters → Detail → Apply
       ↓
Track application in pipeline
```

| Stage | Emotion target | Current friction | Redesign |
| --- | --- | --- | --- |
| Return | Progress | Dashboard waterfall on cold start | Prefetch; collapsed data loading |
| Search | Confidence | No sort; filter duplication on mobile | Sort control; unified filter drawer |
| Apply | Trust | Official-site disclaimer on detail | Retain; add freshness at decision point |

---

## Information architecture

### Site map (student-facing)

```
Public
├── / (Landing)
├── /scholarships/search (Browse — primary task)
├── /scholarship/:id (Detail)
├── /how-it-works
├── /how-matching-works
├── /how-we-verify
├── /faq (footer + landing; not primary nav)
├── /about, /contact, /success-stories
├── /roadmap, /changelog
├── /opportunities/:typeSlug (Journey timeline — reframed)
├── /terms, /privacy
└── Auth: /login, /register, /forgot-password, /reset-password, /verify-email

Authenticated (Dashboard shell)
├── /dashboard (Home)
├── /scholarships/search (Adaptive shell)
├── /match/:profileId (Results)
├── /profile-builder
├── /applications, /documents
├── /planner/:profileId
├── /settings
└── Role-gated: /admin, /sponsor, /school
```

### Content hierarchy principle

**Scholarships first.** Every IA decision asks: does this help a student find, understand, or apply for a scholarship today? If not, it is secondary navigation, footer content, or roadmap positioning.

---

## Navigation architecture

### Public navbar (logged out and logged in on public shell)

| Current | Proposed | Rationale |
| --- | --- | --- |
| How it works | **Scholarships** (first) | Primary task; Hick's Law |
| Scholarships | How it works | Explainer is secondary to action |
| Transparency | Transparency | Retain — trust differentiator |
| FAQ | *(removed)* | Redundant with landing FAQ section + footer |

**Auth area unchanged:** Sign in / Get started (logged out); Dashboard / Log out (logged in).

### Dashboard sidebar + bottom nav

Retain current structure. Add opportunity journey link in sidebar footer (below Settings) — not in bottom nav (4-item limit).

| Bottom nav | Destination |
| --- | --- |
| Home | `/dashboard` |
| Browse | `/scholarships/search` |
| Profile | `/profile-builder` |
| Settings | `/settings` |

### Footer additions

Move FAQ to Company column. Retain Product, Transparency, Legal groupings.

---

## First-time user experience (FTUE)

### Principles

1. **Value before registration.** Search and detail pages work without an account.
2. **Progressive profile.** Mini profile wizard on landing; full builder after register.
3. **One primary action per screen.** Register page: one CTA. Profile step: one "Continue."

### Landing FTUE flow

```
Hero (photo + "Find scholarships you're eligible for")
  → Search CTA (primary) + "How it works" (secondary link)
  → Proof strip (real product screenshots)
  → Mini profile wizard (3 fields → preview matches)
  → Official sources bar
  → How it works (condensed)
  → FAQ (5 items + "View all")
  → Final CTA
```

### Registration gate

Never block search. Gate only: saved scholarships sync, match history, application tracking, document checklist.

---

## Returning user experience

- **Dashboard** opens to: profile completeness, next deadline, latest match summary, saved scholarships.
- **Prefetch** match data and saved list on dashboard mount (PERF-06, shipped).
- **Notifications** surface deadline reminders and verification updates — not marketing.
- **Search** remembers last filters in session; offers "Resume where you left off" if profile incomplete.

---

## Logged-out experience

| Capability | Available | Gated |
| --- | --- | --- |
| Search scholarships | ✓ | — |
| View detail page | ✓ | — |
| Filter by region, level, field | ✓ | — |
| "Check my match" preview | ✓ (limited) | Full match run |
| Save / bookmark | — | ✓ Register |
| Match history | — | ✓ Register |
| Application tracking | — | ✓ Register |

**Design rule:** Every gated feature shows a one-line explanation of what registration unlocks — never a modal that blocks the current task.

---

## Logged-in experience

- **Adaptive search layout:** Dashboard shell (sidebar + topbar + bottom nav) when authenticated.
- **Contextual CTAs:** "Find My Matches" primary only when profile ≥ minimum threshold; otherwise "Complete your profile to unlock matches" as inline link.
- **Match results** as dedicated page with sort, filter recap, and link to methodology.
- **Feedback button** on all authenticated shells including adaptive search.

---

## Mobile-first considerations

**Primary device:** Android phone, 360px viewport, mobile data.

| Pattern | Desktop | Mobile |
| --- | --- | --- |
| Navigation | Sidebar + topbar | Bottom nav (56px + safe-area) |
| Filters | Left sidebar | Bottom sheet drawer (single trigger) |
| Search detail | Split pane | Full-screen panel or navigate to detail |
| Tables | Responsive table | Card-per-row |
| Modals | Centered dialog | Full-screen or bottom sheet |
| Touch targets | 44×44px minimum | 44×44px minimum (non-negotiable) |

**Safe areas:** All fixed chrome respects `env(safe-area-inset-bottom)`. Feedback FAB positioned above bottom nav, not overlapping it.

---

## Opportunity roadmap experience

### Problem

Users click future opportunity types and encounter "Coming soon" pages that feel like disappointment.

### Solution: Opportunity Journey timeline

Replace deficiency framing with intentional positioning.

**`OpportunityComingSoonPage.tsx` redesign:**

- Remove uppercase "Coming soon" eyebrow
- Title: "{Type} — on your opportunity journey"
- Timeline component showing all verticals; current (Scholarships) highlighted; selected type marked "Planned for {quarter/year}"
- Section: "Why we build in this order" — verification and matching quality bar
- Notify-me form (email capture, stored in feedback system)
- "Explore scholarships now" primary CTA

**`OpportunityRoadmapDialog.tsx` redesign:**

- Rename to "Your opportunity journey"
- Vertical list with timeline dots, not grid of "Soon" badges
- Each item: label, one-line description, status (Live / Planned / Exploring)

### Decision record (D6)

- **Decision:** Reframe coming-soon as journey positioning
- **Hypothesis:** Students feel early-adopter confidence, not disappointment
- **Metric:** Bounce rate on `/opportunities/*`; notify-me signups
- **Rollback:** Revert copy if notify-me < 1% and bounce > 80%

---

## Landing page redesign

### Hero

**Static art-directed photography** — three distinct compositions:

| Breakpoint | Composition |
| --- | --- |
| Desktop (≥1024px) | Landscape photograph; headline left, image right or full-bleed with scrim |
| Tablet (768–1023px) | Tighter crop; subject repositioned |
| Mobile (<768px) | Portrait composition — not squeezed landscape |

**Delete:** `HeroCarousel.tsx`, `heroImages.ts` carousel constants.

**Copy:**

- H1: "Find scholarships you're actually eligible for."
- Sub: "ISKONNECT checks your profile against real program rules — then shows what you can apply for now. Providers make the final decision; we help you focus on fit."
- Primary CTA: "Search scholarships" → `/scholarships/search`
- Secondary: "How it works" → `/how-it-works`

### Proof strip ("See the product")

- Remove "See the product" eyebrow
- Replace CSS skeletons with device-framed screenshots (or labeled placeholders until captured)
- Title: "See what you'll get before you sign up"
- Four frames: match results, factor breakdown, search filters, mobile dashboard

### Section rhythm

Standardize vertical padding: `py-12 sm:py-16 lg:py-20` (reduce from `xl:py-32` except hero).

### Motion

Landing-only framer-motion reveals via `LandingMotionProvider`. Respect `prefers-reduced-motion`. No auto-rotating content.

---

## Search experience redesign

### Progressive disclosure hierarchy

```
1. Search input (immediate, above fold on mobile)
2. Results list (default: all published, paginated)
3. Active filter chips (when filters applied)
4. Filter drawer (on demand — single trigger)
5. Sort control (new)
6. Match actions (contextual — not competing primaries)
```

### CTA hierarchy fix

| Element | Role | Style |
| --- | --- | --- |
| Search input | Primary task | Full width, prominent |
| Find My Matches | Contextual primary | One solid button; hidden if no profile |
| Complete Your Profile | Secondary | Text link or outline button |
| Check my match (card) | Tertiary | Per-card action |

### Filter consolidation

- Delete page-level full-screen overlay in `ScholarshipSearchPage.tsx:312-328`
- Add `variant="sidebar" | "drawer"` to `ScholarshipSearchFilters`
- Mobile: Sheet trigger opens drawer directly
- Desktop: unchanged sidebar

### Sort (new)

Add sort control: Relevance (default), Deadline (soonest), Alphabetical, Recently verified.

---

## Scholarship detail page improvements

Retain Phase 3 trust surface. Enhancements:

1. **Eligibility block** — move above fold on mobile; collapse long requirement lists
2. **Apply section** — sticky action bar on mobile with official link + save
3. **Freshness** — "Last verified {date}" adjacent to Apply button
4. **Related scholarships** — "Similar programs you may qualify for" at bottom (forward momentum)
5. **Non-guarantee copy** — retain official-site disclaimer banner; no inline score disclaimer (per D2)

---

## Match experience redesign

### Loading behavior

- Immediate skeleton on "Find My Matches" (< 400ms, Doherty threshold)
- Staged card reveal as results resolve (progress communication)
- No artificial delay

### Match analysis modal ("Why did I match?")

Primary home for non-guarantee copy:

```
Why did I match?

{score}% Eligibility Fit

Based on
✓ {factor 1}
✓ {factor 2}
...

[Factor breakdown bars]

Learn how matching works →

────────────────────────────
Scholarship providers make the final selection.
Meeting eligibility does not guarantee acceptance.
```

Remove `MATCH_CONFIDENCE_COMPACT` from all ambient surfaces.

### Match results page

- Header: "{n} scholarships matched your profile"
- Optional footer link: "How we calculate eligibility fit →"
- Sort and filter recap

---

## Component inventory

### Shells

| Component | File | Purpose |
| --- | --- | --- |
| PublicShell | `layout/PublicLayout.tsx` | Navbar + main + Footer + Feedback |
| DashboardLayout | `layout/DashboardLayout.tsx` | Sidebar + topbar + bottom nav |
| AdaptiveSearchLayout | `layout/AdaptiveSearchLayout.tsx` | Shell swap by auth |

### Core student components

| Component | File | Redesign notes |
| --- | --- | --- |
| ScholarshipCardV2 | `ScholarshipCardV2.tsx` | Three-zone grammar; remove ambient disclaimer |
| MatchScoreRing | `MatchScoreRing.tsx` | Simplify aria-label |
| MatchAnalysisModal | `MatchAnalysisModal.tsx` | Primary disclaimer home |
| MatchConfidenceNote | `MatchConfidenceNote.tsx` | Refactor to `explanation` variant only |
| ScholarshipSearchFilters | `ScholarshipSearchFilters.tsx` | Add variant prop |
| HeroSection | `landing/HeroSection.tsx` | Static `<picture>` hero |
| ProofStripSection | `landing/ProofStripSection.tsx` | Real screenshots |
| OpportunityTimeline | `OpportunityTimeline.tsx` | Journey timeline (extend) |
| FeedbackButton | `FeedbackButton.tsx` | Reposition above bottom nav |
| BottomNav | `layout/BottomNav.tsx` | Unchanged structure |

### Design system primitives (`components/ui/`)

Retain all 21 shadcn primitives. No new primitives without ADR.

---

## Prioritized implementation roadmap

### High impact (ship first)

| ID | Item | User outcome | Files |
| --- | --- | --- | --- |
| H1 | Search CTA hierarchy + filter consolidation | "I can search immediately" | `ScholarshipSearchPage`, `ScholarshipSearchFilters` |
| H2 | Card header redesign + disclaimer relocation | Cards readable; trust where sought | `ScholarshipCardV2`, `MatchAnalysisModal`, `MatchConfidenceNote` |
| H3 | Hero static photography | Landing feels credible and warm | `HeroSection`, delete `HeroCarousel` |
| H4 | Feedback FAB reposition + adaptive search mount | Mobile chrome usable | `FeedbackButton`, `AdaptiveSearchLayout` |
| H5 | Opportunity journey reframe | Future verticals inspire confidence | `OpportunityComingSoonPage`, `OpportunityRoadmapDialog` |

### Medium impact

| ID | Item | User outcome | Files |
| --- | --- | --- | --- |
| M1 | Proof strip real screenshots | "See the product" delivers | `ProofStripSection` |
| M2 | Nav reduction (remove FAQ) | Clearer task focus | `Navbar`, `Footer` |
| M3 | Notifications panel scroll | Notifications usable on small screens | `DashboardTopbar` |
| M4 | Footer rhythm + id fix | Visual balance | `Footer` |
| M5 | Search sort control | User control over results | `useScholarshipSearch`, search page |
| M6 | Match loading staged reveal | Match feels intelligent | `MatchResultsPage` |
| M7 | Detail page sticky apply bar | Mobile apply friction reduced | `ScholarshipDetailPage` |

### Low impact

| ID | Item | User outcome | Files |
| --- | --- | --- | --- |
| L1 | Landing copy refresh | Student-focused language | `landingData.ts`, landing sections |
| L2 | Dashboard opportunity journey link | Growth principle on major pages | `DashboardSidebar` |
| L3 | Dark mode elevation pass | Consistent depth in dark theme | Token migration on landing |
| L4 | Success animation timing | Non-critical celebration | Design tokens |
| L5 | Related scholarships on detail | Forward momentum | `ScholarshipDetailPage` |

---

## Risks, trade-offs, and engineering considerations

| Risk | Mitigation |
| --- | --- |
| Hero image hurts LCP | Single preloaded AVIF ≤120KB; `<picture>` per breakpoint; measure before merge |
| Disclaimer relocation increases score-as-acceptance confusion | Rollback trigger; monitor support tickets |
| Removing FAQ from nav reduces FAQ traffic | Footer + landing section retain links; monitor analytics |
| Large spec → implementation drift | UI_DEFECT_REGISTER maps every item to file/line |
| Token migration incomplete on landing | ~3,239 raw palette usages remain; landing is priority migration target |
| Bundle budget | No new heavy libraries; framer-motion already code-split |
| Catalog depth limits Hope | Documented in narrative; not a UX fix |

---

## Recommendation template reference

**Full template** (contested decisions): Problem → Evidence → UX Principle → Alternatives → Chosen Solution → Trade-offs → Complexity → Impact → Decision/Hypothesis/Metric/Rollback.

**Compact template** (obvious fixes): Problem → Solution → Principle.

See [UI_DEFECT_REGISTER.md](./UI_DEFECT_REGISTER.md) for file-level implementation of all 11 named defects.

---

## Related documents

| Document | Purpose |
| --- | --- |
| [PRODUCT_NARRATIVE.md](./PRODUCT_NARRATIVE.md) | North star |
| [DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md) | Visual specification |
| [CONTENT_VOICE_GUIDE.md](./CONTENT_VOICE_GUIDE.md) | Copy rules |
| [ACCESSIBILITY_SPEC.md](./ACCESSIBILITY_SPEC.md) | WCAG 2.2 AA |
| [UI_DEFECT_REGISTER.md](./UI_DEFECT_REGISTER.md) | Defect fixes |

---

## Document history

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-01 | Initial master UX specification per design blueprint plan. |
