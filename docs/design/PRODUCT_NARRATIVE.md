# ISKONNECT Product Narrative

> **Document type:** North star — experience principles, design pillars, and product story  
> **Status:** Approved specification  
> **Version:** 1.0  
> **Last updated:** 2026-08-01  
> **Authority:** This document is page one. Every other file in `docs/design/` cites it rather than restating it.

---

## What ISKONNECT should feel like

Linear feels fast. Stripe feels trustworthy. Duolingo feels encouraging. Apple feels elegant. GitHub feels professional.

**ISKONNECT should feel like a credible mentor who knows the system — and is on your side.**

Not a directory you browse. Not a startup pitch. Not an AI that guesses. A calm, honest guide that helps Filipino students discover real opportunities, understand why they fit, and take the next step — today with scholarships, tomorrow across their whole academic journey.

---

## Core story

**Connecting Filipino students to opportunity.**

Most students in the Philippines do not lack ability. They lack visibility. Scholarships exist; the path to them is scattered across provider sites, Facebook posts, and word of mouth. ISKONNECT exists to make that path legible — verified information, explained eligibility, and a clear next action — so students spend time applying, not searching.

Scholarships are the first milestone, not the final product. The long-term platform supports internships, competitions, research grants, fellowships, and every other opportunity category a student encounters from senior high through early career. Users who join now should feel they are early in something that will grow with them — because the roadmap shows dated, specific commitments, not because we tell them to feel lucky.

---

## Emotional arc

Every student journey follows the same arc. Design should reinforce it at each stage.

```
Curiosity          →  Confidence           →  Growth
"I wonder if       →  "I understand why    →  "This platform
 there are          →   I match and what     →   will grow with me
 options for me"    →   to do next"          →   beyond scholarships"
```

| Stage | User state | Design job |
| --- | --- | --- |
| **Curiosity** | Arrives from Google, a classmate's link, or a social post. Skeptical. Limited time. | Deliver value before registration. Show real scholarships immediately. Look credible in the first ten seconds. |
| **Confidence** | Has a profile or has browsed results. Wants to know *why* and *what next*. | Explain matches transparently. Never hide uncertainty — place it where users seek explanations. Every screen offers a next step. |
| **Growth** | Returns weekly. Saves scholarships. Tracks deadlines. | Surface progress. Remind them scholarships are the beginning. Show the opportunity journey without distracting from today's task. |

---

## Experience Principles

**Principles without a falsifiable test become decoration.** Each principle below includes an observable test that design reviews and QA can verify.

### Trust

Students believe the information — not because we claim it, but because we show why.

- Every factual claim on screen traces to a source, a timestamp, or an explicit "unknown" label.
- Verification dates, provider attribution, and official links are never removed to reduce clutter.
- Match scores measure eligibility fit against listed requirements — never presented as odds of winning.

**Observable test:** Users can identify why a scholarship matched in under 10 seconds.

### Hope

Students leave believing they have opportunities — not that scholarships are scarce or closed to them.

- Empty states never end without a concrete, honest next action.
- Excluded or ineligible results explain what would change the outcome.
- Copy avoids deficit framing ("only 3 scholarships found") in favor of forward framing ("3 you can explore now").

**Observable test:** No empty state ends without another action.

### Progress

Every screen moves the student forward. No abandoned flows. No decorative dead ends.

- Every page contains a visible next step — even when that step is "complete your profile to unlock matches" or "broaden your filters."
- Where no next step exists, we say so plainly and explain what would create one.
- "Coming soon" is reframed as intentional roadmap positioning, never as an apology for absence.

**Observable test:** Every page contains a next step.

### Confidence

Students understand why something matched, why it didn't, and what to do next. No magic. No mystery.

- Match explanations are one tap away, with factor breakdowns in plain language.
- Profile completion shows what each field unlocks.
- Errors state what happened and one recovery action — never a developer string.

**Observable test:** Users never wonder "What do I do now?"

### Growth

Scholarships are today's feature. The student opportunity platform is tomorrow's product.

- Every major page subtly communicates the broader journey without distracting from the current task.
- The opportunity roadmap shows dated commitments on a timeline — not vague ambition.
- Users feel they joined early because the product shows where it is going, not because we hype "exclusive early access."

**Observable test:** Every major page reminds users that scholarships are the beginning of a broader opportunity platform.

---

## Design Pillars

When two design options conflict, the higher-numbered pillar yields to the lower.

1. **Clarity beats cleverness.** Never sacrifice understanding for visual novelty. If a student has to guess what a control does, the design failed.

2. **Students always know what to do next.** One primary action per view. Secondary actions are visually subordinate. Progressive disclosure for everything else.

3. **Show progress before perfection.** We build trust incrementally — a partial profile still returns useful results; an unverified listing still appears with an honest label. Perfection is not a gate to value.

4. **Transparency over persuasion.** Never manipulate urgency. No fake scarcity. No countdown timers on open deadlines. No dark patterns toward registration. Honest limitations build more trust than optimistic exaggeration.

5. **Scholarships first. Opportunity platform second.** The roadmap inspires without distracting. Search, match, and apply remain the primary tasks until additional verticals ship.

---

## Resolved tensions

Two principles appear to conflict. These resolutions are binding.

### Progress vs honesty

"No dead ends" taken literally pressures the product into manufacturing next steps that do not exist. A student genuinely ineligible for every scholarship in the catalog deserves the truth plus something useful — broaden filters, complete a missing profile field, or save programs opening next cycle.

**Resolution:** Every screen offers a *real* next step. Where none exists, we say so plainly and explain what would change the outcome.

### Growth vs no-hype

"You joined early in something meaningful" is startup register. It erodes the Trust principle.

**Resolution:** Growth is communicated through evidence — dated roadmap items, changelog entries, and the opportunity journey timeline — never through atmosphere, exclusivity language, or fabricated momentum.

---

## The Opportunity Journey

ISKONNECT grows with the student. The interface tells this story subtly, never as a distraction from today's task.

```
Senior High
    ↓
Scholarships          ← live today
    ↓
Internships / OJT
    ↓
Competitions / Hackathons
    ↓
Research Grants / Fellowships
    ↓
Graduate Studies
    ↓
Career / Professional Development
```

**Today:** Scholarships are the only live vertical. Everything else appears on the journey timeline as dated, intentional commitments.

**Tomorrow:** Each vertical ships only when verification and matching quality meet the same bar scholarships required at launch. Speed of expansion never compromises trust.

---

## Brand voice (summary)

ISKONNECT speaks like a helpful mentor — encouraging without exaggerating, transparent without being cold, professional without being institutional.

- **Encouraging:** "You have options" — not "Revolutionary AI finds your dream scholarship!"
- **Transparent:** "We last verified this on March 12" — not "Verified ✓"
- **Credible:** "Providers make the final decision" — not "Guaranteed match!"
- **Never exaggerated:** No superlatives, no startup buzzwords, no implied endorsement by CHED, DOST, or any provider.

Full voice rules: [CONTENT_VOICE_GUIDE.md](./CONTENT_VOICE_GUIDE.md).

---

## How the narrative appears in UI

| Surface | Narrative expression |
| --- | --- |
| **Hero (landing)** | "Find scholarships you're actually eligible for" — immediate value, no hype. Static art-directed photography of real Filipino students. |
| **Onboarding / profile builder** | Each step explains what it unlocks. Progress meter tied to match quality, not arbitrary completion. |
| **Search** | Search-first. Filters progressive. Results immediate for guests. |
| **Scholarship cards** | Three questions answered without a tap: Can I apply? Am I likely eligible? How current is this? |
| **Match explanation ("Why did I match?")** | Factor breakdown, then non-guarantee copy — only where users seek understanding. |
| **Empty states** | Honest count + one next action. Never a blank page. |
| **Opportunity roadmap** | Journey timeline with current stage highlighted. Notify-me for future verticals. No "Coming soon" dead ends. |
| **Notifications / email** | Deadline reminders, profile nudges, verification updates. Plain language. One action per message. |
| **Settings / footer** | Changelog and roadmap links. Transparent about beta status. |

---

## Relationship to other documents

| Document | Relationship |
| --- | --- |
| [PRODUCT_DESIGN_SPEC.md](./PRODUCT_DESIGN_SPEC.md) | Implements this narrative in UX architecture, journeys, and per-surface specs. |
| [DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md) | Visual and motion expression of these principles. |
| [CONTENT_VOICE_GUIDE.md](./CONTENT_VOICE_GUIDE.md) | Copy rules derived from brand voice above. |
| [ACCESSIBILITY_SPEC.md](./ACCESSIBILITY_SPEC.md) | Functional requirement — accessibility is how Trust and Confidence reach every user. |
| [UI_DEFECT_REGISTER.md](./UI_DEFECT_REGISTER.md) | Known gaps between current UI and this narrative. |

---

## Catalog quality (timeless)

The long-term value of ISKONNECT depends on both experience quality and catalog quality. UX improvements cannot compensate for an insufficient breadth of verified opportunities. Product growth and catalog growth must progress together.

Design amplifies Hope. Catalog depth creates it. Operational catalog targets live in `docs/engineering/catalog-readiness.md` — not in this document.

---

## Document history

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 2026-08-01 | Initial north star document. Merged experience principles and product narrative per design blueprint plan. |
