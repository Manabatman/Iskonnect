# Manual screen-reader pass — A11Y-13

Template for documenting NVDA and TalkBack passes on five primary student flows. **Do not claim coverage that was not performed** (R-08).

## Pass metadata

| Field | Value |
| --- | --- |
| Date | _YYYY-MM-DD_ |
| Tester | _name_ |
| App version / commit | _hash or tag_ |
| Build environment | _local / staging / production_ |

## Platform availability

| Platform | Available? | Performed? | Notes |
| --- | --- | --- | --- |
| NVDA + Chrome (Windows) | Yes / No | Yes / No | Mandatory when available |
| TalkBack + Chrome (Android) | Yes / No | Yes / No | Mandatory — target device class |
| VoiceOver + Safari (macOS) | Yes / No | Yes / No | Perform if available; record gap if not |
| VoiceOver + Safari (iOS) | Yes / No | Yes / No | Perform if available; record gap if not |

If a mandatory platform was unavailable, record **why** and treat the gap as a finding — not as passed coverage.

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
| 3.1 | Match score and non-guarantee copy are read without extra interaction | ☐ | |
| 3.2 | “Not calculated yet” vs scored results are distinguishable | ☐ | |
| 3.3 | Match analysis dialog traps focus; Escape closes; focus returns | ☐ | |
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
| 4.3 | Mobile filter sheet is reachable and dismissible | ☐ | |
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
| SR-001 | | Critical / Serious / Moderate / Minor | | | ☐ |

---

## Sign-off

- [ ] All mandatory platforms attempted or gaps explicitly recorded
- [ ] All five flows tested on at least one mandatory platform
- [ ] Blocking issues filed or fixed
- [ ] Reviewer signature: __________________ Date: __________

**Related:** [ISKONNECT_PHASE_3_MASTER_PLAN.md](./ISKONNECT_PHASE_3_MASTER_PLAN.md) § XIII.2 (A11Y-13)
