# Manual screen-reader pass — A11Y-13

Template for documenting NVDA and TalkBack passes on five primary student flows. **Do not claim coverage that was not performed** (R-08).

## Pass metadata

| Field | Value |
| --- | --- |
| Date | 2026-08-01 |
| Tester | _pending — requires human operator_ |
| App version / commit | `feature/design-system-v1` (Wave 8) |
| Build environment | local preview + CI e2e |

## Platform availability

| Platform | Available? | Performed? | Notes |
| --- | --- | --- | --- |
| NVDA + Chrome (Windows) | Yes | **No** | Wave 8 automated gates shipped; manual pass still required before public launch |
| TalkBack + Chrome (Android) | Yes | **No** | Requires physical Android device |
| VoiceOver + Safari (macOS) | Yes | No | Optional |
| VoiceOver + Safari (iOS) | Yes | No | Optional |

## Automated Wave 8 coverage (CI)

| Gate | Tool | Status |
| --- | --- | --- |
| axe-core 12 routes | `e2e/a11y.spec.ts` | **PASS** (no serious/critical) |
| Contrast token pairs | `src/lib/contrast.test.ts` | **PASS** |
| 200% / 400% zoom reflow (320px) | `e2e/zoom-reflow.spec.ts` on `/`, `/scholarships/search`, `/dashboard` | **PASS** (no horizontal overflow) |
| Touch targets | `e2e/touch-targets.spec.ts` (allowlist) | Baseline debt — bell/menu bumped to 44px in Wave 8 |
| Modal focus trap | `e2e/modal-focus.spec.ts` | Added — runs when match seed data present |

### Zoom verification (automated partial)

| Zoom | Routes tested | Result |
| --- | --- | --- |
| 200% | Landing, search, dashboard | **PASS** — no horizontal scroll at 320px viewport |
| 400% | Landing, search, dashboard | **PASS** — no horizontal scroll at 320px viewport |

Functional zoom testing (all student routes, all controls operable) still requires manual verification per ACCESSIBILITY_SPEC §6.

---

## Five flows

Each flow: start from a clean session (or documented starting state), complete the task using only the screen reader + keyboard/touch, and note pass/fail plus issues.

### 1. Register

**Route:** `/register`

| # | Check | Pass | Notes |
| --- | --- | --- | --- |
| 1.1 | Skip link announces and moves focus to main content | ☐ | |
| 1.2 | All form fields have accessible names | ☐ | |
| 1.3 | Validation errors are announced (`aria-invalid`, live region, or alert) | ☐ | |
| 1.4 | Submit success navigates with clear announcement | ☐ | |
| 1.5 | Focus is not lost or trapped incorrectly | ☐ | |

**Overall:** ☐ Pass ☐ Fail — _summary_

---

### 2. Build profile

**Route:** `/profile-builder`

| # | Check | Pass | Notes |
| --- | --- | --- | --- |
| 2.1 | Step progress / headings are announced in logical order | ☐ | |
| 2.2 | Combobox fields (`role="combobox"`) expose suggestions and selection | ☐ | |
| 2.3 | Required fields and consent checkbox are discoverable | ☐ | |
| 2.4 | Save / continue actions have clear labels | ☐ | |
| 2.5 | Error states on fields are announced | ☐ | |

**Overall:** ☐ Pass ☐ Fail — _summary_

---

### 3. View matches

**Route:** `/match/{profileId}` (after a match run)

| # | Check | Pass | Notes |
| --- | --- | --- | --- |
| 3.1 | Match score and non-guarantee copy are read without extra interaction | ☐ | Modal disclaimer now `text-body-sm` (14px) |
| 3.2 | “Not calculated yet” vs scored results are distinguishable | ☐ | |
| 3.3 | Match analysis dialog traps focus; Escape closes; focus returns | ☐ | Automated in `modal-focus.spec.ts` when seeded |
| 3.4 | Card actions (Apply, Check match) have accessible names | ☐ | |
| 3.5 | Empty / loading states are announced appropriately | ☐ | |

**Overall:** ☐ Pass ☐ Fail — _summary_

---

### 4. Search and filter

**Route:** `/scholarships/search`

| # | Check | Pass | Notes |
| --- | --- | --- | --- |
| 4.1 | Search input behaves as combobox where applicable | ☐ | |
| 4.2 | Result count live region announces updates (`aria-live="polite"`) | ☐ | |
| 4.3 | Mobile filter sheet is reachable and dismissible | ☐ | Filters grouped in `<fieldset>` + `<legend>` (Wave 8) |
| 4.4 | Pagination controls are labeled | ☐ | |
| 4.5 | Filter chips / active filters are readable | ☐ | |

**Overall:** ☐ Pass ☐ Fail — _summary_

---

### 5. Save a scholarship

**Route:** search or detail → save action

| # | Check | Pass | Notes |
| --- | --- | --- | --- |
| 5.1 | Save / unsave button name reflects current state | ☐ | |
| 5.2 | Confirmation or error feedback is announced | ☐ | |
| 5.3 | Saved state persists after navigation (if applicable) | ☐ | |
| 5.4 | Icon-only controls in dashboard chrome have names when sidebar collapsed | ☐ | |
| 5.5 | No critical information conveyed by color alone | ☐ | |

**Overall:** ☐ Pass ☐ Fail — _summary_

---

## NVDA-specific checklist (Windows + Chrome)

- [ ] NVDA started before page load; browse mode on for static content
- [ ] Tab order matches visual order on each flow
- [ ] `H` / `1`–`6` heading navigation finds one logical `h1` per page
- [ ] `D` landmark navigation reaches `main`, `nav`, and `header`
- [ ] Forms mode activates on inputs; combobox arrow keys work
- [ ] Dialogs: NVDA reads title + description; focus does not escape modal
- [ ] Live regions: result counts and alerts speak without stealing focus

## TalkBack-specific checklist (Android + Chrome)

- [ ] TalkBack enabled; explore-by-touch vs linear navigation both tried
- [ ] Swipe-right linear order matches visual order
- [ ] Double-tap activates controls; no accidental activation on scroll
- [ ] Bottom nav and mobile filter sheet reachable
- [ ] Dialogs: back gesture / escape dismisses; focus returns to trigger
- [ ] Live regions announce search result updates

---

## Issues log

| ID | Flow | Severity | Description | File / component | Fixed? |
| --- | --- | --- | --- | --- | --- |
| SR-001 | Manual | — | NVDA + TalkBack five-flow pass not yet executed | — | ☐ |

---

## Sign-off

- [ ] All mandatory platforms attempted or gaps explicitly recorded
- [ ] All five flows tested on at least one mandatory platform
- [ ] Blocking issues filed or fixed
- [ ] Reviewer signature: __________________ Date: __________

**Related:** [ISKONNECT_PHASE_3_MASTER_PLAN.md](./ISKONNECT_PHASE_3_MASTER_PLAN.md) § XIII.2 (A11Y-13)
