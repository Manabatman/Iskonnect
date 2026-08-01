# ISKONNECT Content Voice Guide

> **Document type:** Microcopy and tone specification  
> **Status:** Approved specification  
> **Version:** 1.0  
> **Last updated:** 2026-08-01  
> **North star:** [PRODUCT_NARRATIVE.md](./PRODUCT_NARRATIVE.md) — voice summary lives there; rules live here.

---

## 1. Voice definition

ISKONNECT speaks like a **helpful mentor** — someone who knows how scholarships work in the Philippines and explains it without talking down.

| Attribute | We are | We are not |
| --- | --- | --- |
| **Encouraging** | "You have options worth exploring." | "Revolutionary AI finds your dream scholarship!" |
| **Transparent** | "We last verified this on March 12." | "Verified ✓" (with no date) |
| **Credible** | "Providers make the final decision." | "Guaranteed match!" |
| **Plain** | "Your grade average (GWA)" | "Academic performance metric" |
| **Calm** | "3 scholarships match your profile." | "ONLY 3 LEFT — APPLY NOW!" |

**Reading level:** Grade 11 English. Filipino terms used where they are the actual terms (GWA, 4Ps, barangay, PSCED).

---

## 2. Banned language

### Startup buzzwords (never use)

- Revolutionary, disruptive, game-changing, cutting-edge
- AI-powered (say "checks your profile against program rules" instead)
- Dream scholarship, life-changing, unlock your future
- Exclusive early access, join the movement
- Leverage, synergy, ecosystem (in user-facing copy)

### Manipulation (never use)

- Countdown timers on open deadlines
- Fake scarcity ("Only 2 spots left")
- Dark patterns toward registration
- "Click here" (link text must make sense out of context)

### Technical jargon (never use in student UI)

- API, endpoint, token, cache, prefetch
- Lifecycle status (use "application status" or the plain label)
- Prefilter, oracle, serialization
- VITE_, localhost, any dev environment string

### Exaggeration (never use)

- "All scholarships in the Philippines"
- "100% accurate"
- Implied endorsement by CHED, DOST, or any provider
- Fabricated testimonials or outcome statistics

---

## 3. Term consistency

| Use this | Not this | Notes |
| --- | --- | --- |
| **scholarship** | listing, opportunity (unless referring to platform-wide) | Default term |
| **match** / **eligible fit** | recommendation, prediction | Score = fit, not odds |
| **profile** | application (until user actually applies) | Profile is input; application is output |
| **provider** | sponsor, organization (unless specific) | The entity offering the scholarship |
| **verify on the official site** | apply through ISKONNECT | We link out; we don't process applications |
| **eligibility fit** | match score, win probability | Always |

First use of abbreviations: expand with `GlossaryTerm` component (GWA, TVET, PSCED, 4Ps, ALS, LOA).

---

## 4. Empty states

**Pattern:** Headline + explanation + one action.

| Context | Headline | Action |
| --- | --- | --- |
| No search results | "No scholarships match these filters." | "Clear filters" or "Broaden your search" |
| No matches (profile) | "No scholarships matched your profile yet." | "Complete your profile" or "Adjust your region" |
| No saved scholarships | "You haven't saved any scholarships." | "Browse scholarships" |
| No applications | "No applications tracked yet." | "Save a scholarship to start tracking" |
| No notifications | "You're all caught up." | "Browse new scholarships" |
| Success stories (empty) | "We're collecting real student stories." | "Share your experience" (when ready) |

**Never:** "Something went wrong" without explanation and recovery.

---

## 5. Error states

Use `errorCopy.ts` mappings. Every error includes exactly one recovery action.

| Error class | Copy pattern |
| --- | --- |
| Network | "We couldn't reach the server. Check your connection and try again." + [Retry] |
| Auth expired | "Your session expired. Sign in again to continue." + [Sign in] |
| Not found | "We couldn't find that scholarship. It may have been removed." + [Browse scholarships] |
| Validation | "{Field} needs to be {requirement}." (inline, at the field) |
| Server | "Something went wrong on our end. Try again in a moment." + [Retry] |

**Never expose:** stack traces, HTTP status codes, variable names, environment strings.

---

## 6. Loading states

| Context | Copy |
| --- | --- |
| Search | "Searching…" |
| Match run | "Finding your matches…" / "Running…" |
| Navigation | "Opening…" |
| Save | "Saving…" |
| General | "Loading…" |

Prefer skeleton layouts over spinner-only screens. Label changes on buttons, not separate loading pages.

---

## 7. Replacement copy — landing hero

**H1:** Find scholarships you're actually eligible for.

**Subcopy:** ISKONNECT checks your profile against real program rules — then shows what you can apply for now, prepare for, or watch for next cycle. Providers make the final decision; we help you focus on fit.

**Primary CTA:** Search scholarships

**Secondary link:** How it works

**Trust chips (below CTA):**

- Verified against official sources
- Free for students
- No account needed to browse

---

## 8. Replacement copy — "See the product" section

**Remove eyebrow** ("See the product").

**Title:** See what you'll get before you sign up

**Description:** Browse real programs, understand your fit, and decide where to spend your time — without creating an account first.

**Frame captions:**

1. "See which programs fit your profile"
2. "Understand why a match scored the way it did"
3. "Filter by region, level, and field"
4. "Track your plan on any device"

---

## 9. Replacement copy — opportunity roadmap

**Page title (was "Coming soon"):** {Type} — on your opportunity journey

**Intro (was "Why it's not live yet"):** ISKONNECT is building a unified student opportunity platform. We launch each category only when verification and matching meet the same standard as scholarships.

**Timeline label for live:** Available now

**Timeline label for future:** Planned for {quarter} {year}

**Notify CTA:** Notify me when {type} launches

**Primary action:** Explore scholarships now

**Dialog title (was "More opportunity types"):** Your opportunity journey

---

## 10. Replacement copy — match explanation disclaimer

**Remove from cards, badges, dashboard, score ring aria.**

**Place in match analysis modal only**, after factor breakdown:

```
Why did I match?

{score}% Eligibility Fit

Based on
✓ {factor 1}
✓ {factor 2}
...

Learn how matching works →

────────────────────────────
Scholarship providers make the final selection.
Meeting eligibility does not guarantee acceptance.
```

**Do not use:** "ISKONNECT estimate — the provider decides who is accepted."

---

## 11. Replacement copy — search page

**H1:** Search scholarships

**Helper text (replace current technical explanation):**

> Type a scholarship name or provider to search. Use filters to narrow by region, education level, or field of study.

**Find My Matches (when profile exists):** Find my matches

**Find My Matches (when profile incomplete):** Complete your profile to find matches (link style)

**Complete Your Profile:** Complete your profile → (inline link, not competing button)

---

## 12. Replacement copy — register page

**Tagline:** Create a free account to save scholarships, track matches, and manage your applications.

**Not:** Technical feature lists or "Join the platform" hype.

---

## 13. Status and badge labels

Use plain language from `scholarshipStatus.ts`. Never raw enum values.

| Internal | User-facing |
| --- | --- |
| `open` | Open now |
| `needs_verification` | Needs verification |
| `closed` | Closed |
| `qualified` | You likely qualify |
| `almost_qualified` | Almost — one requirement away |
| `not_eligible` | Not eligible based on current info |

---

## 14. Link text rules

Links must make sense out of context (WCAG 2.4.4).

| Bad | Good |
| --- | --- |
| Click here | View scholarship details |
| Read more | How we verify scholarships |
| Learn more | How matching works |

---

## 15. Email and notification copy (future)

When implemented, follow:

- Subject: specific action needed ("DOST-SEI deadline in 7 days")
- Body: one fact + one action
- No marketing fluff in transactional messages
- Unsubscribe always available for non-critical notifications

---

## Document history

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-01 | Initial content voice guide. Phase 5 CONT deliverable. |
