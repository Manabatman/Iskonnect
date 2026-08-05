# Product Acceptance Test — Phase 2 sign-off

**Purpose:** Manual walkthrough as a brand-new user. No code changes during this session — only use the app and record findings.

**Environment:** Staging or local with backend + frontend running. Test **360×640 mobile** and **1280+ desktop**.

**Tester:** __________ **Date:** __________

---

## Landing & chrome

| Step | Pass | Notes |
| --- | --- | --- |
| Hero carousel loads (no broken images) | ☐ | |
| Primary CTA visible above fold on mobile | ☐ | |
| Navbar: open sheet menu, all links tappable (44px+) | ☐ | |
| Footer links readable and tappable | ☐ | |
| Dark mode toggle — no flash, tokens readable | ☐ | |
| Theme persists on refresh | ☐ | |

## Registration & auth

| Step | Pass | Notes |
| --- | --- | --- |
| Register — invalid email rejected with clear message | ☐ | |
| Register — loading state during submit | ☐ | |
| Register — server error shown (try duplicate email) | ☐ | |
| Email verification flow (if enabled) | ☐ | |
| Login — valid credentials → correct redirect | ☐ | |
| Login — wrong password → error, no crash | ☐ | |
| Forgot password link works | ☐ | |

## Profile builder

| Step | Pass | Notes |
| --- | --- | --- |
| Every step renders on mobile (no horizontal scroll) | ☐ | |
| Back / Next navigation | ☐ | |
| Autosave indicator or persistence on refresh | ☐ | |
| Mobile keyboard doesn't hide primary action | ☐ | |
| Completion → dashboard redirect + celebration (P1-05) | ☐ | |

## Dashboard

| Step | Pass | Notes |
| --- | --- | --- |
| Cards layout on mobile (priority content first) | ☐ | |
| Saved scholarships section | ☐ | |
| Match history / run matches | ☐ | |
| Planner link | ☐ | |
| Empty states have clear next action | ☐ | |
| Bottom nav: all four tabs, active state correct | ☐ | |

## Search

| Step | Pass | Notes |
| --- | --- | --- |
| Mobile: Filters opens bottom sheet | ☐ | |
| Apply filter → results update | ☐ | |
| Active filter chips visible | ☐ | |
| Scholarship cards tappable, badges readable | ☐ | |
| Detail page from search result | ☐ | |

## Scholarship detail

| Step | Pass | Notes |
| --- | --- | --- |
| Lifecycle + qualification badges legible (light/dark) | ☐ | |
| Official link / bookmark | ☐ | |
| Back navigation | ☐ | |

## Settings

| Step | Pass | Notes |
| --- | --- | --- |
| Theme switch (light / dark / system) | ☐ | |
| Account section loads | ☐ | |
| Profile edits save | ☐ | |

---

## Blockers (must fix before Phase 3)

1. 
2. 

## Polish (can defer)

1. 
2. 

## Sign-off

- [ ] PAT complete — no P0/P1 blockers remaining
- Reviewer: __________
