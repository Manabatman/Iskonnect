# Student verification UX — three audience layers

**Generated:** 2026-08-05  
**Priority:** P0 before public beta

---

## Problem

Students currently see internal verification metadata on scholarship detail: field evidence lists, migration notes (“ISKONNECT id 16…”), retrieval timestamps, “Imported — not independently verified”, and change-history diffs. This is engineering/reviewer content, not applicant-facing information.

---

## Target architecture

### Layer 1 — Student view (default)

Show only:

- **Verified** / **Needs Review** / **Archived** (scholarship-centric wording)
- Last verified date
- Official website link
- Disclaimer: “Always confirm details on the official website before applying.”
- Optional: “Information is regularly reviewed against official sources.”

Hide: field evidence, snippets, internal IDs, link-health internals, completeness jargon, change history, “Imported”.

### Layer 2 — Transparency (optional, collapsed)

`▼ How was this information verified?`

- Official website
- Last verified
- High-level verification method
- Link status (OK / needs check)

Still no research notes or internal IDs.

### Layer 3 — Admin / reviewer

Full trail via admin API and catalog tools: field evidence, confidence, retrieved dates, reviewer, verification history, field changes, source PDFs.

### Layer 4 — Developer debug (optional, never default)

Raw metadata, scholarship IDs, migration notes.

---

## Student status copy matrix

| Internal badge | Student status | Student message |
|----------------|----------------|-----------------|
| `verified` | Verified | Information has been checked against an official source. |
| `partially_verified`, `imported_unverified`, `needs_review` | Needs Review | Some information could not be confirmed recently. Always confirm details on the official website. |
| Archived / inactive / closed | Archived | This opportunity is no longer accepting applications. |

**Retired label:** “Imported — not independently verified” (never show to students).

---

## API fields (student payload)

```json
{
  "student_verification_status": "verified | needs_review | archived",
  "student_verification_label": "Verified",
  "student_verification_message": "...",
  "last_verified_at": "2026-07-26T...",
  "official_website": "https://www.gabayguro.com"
}
```

`field_evidence` removed from public `GET /scholarships/{id}`. Admin: `GET /admin/scholarships/{id}/evidence`.

---

## Detail page layout

Hero → Eligibility → Requirements → Benefits → Application → Official website → **Verification (student strip)** → (admin-only evidence panel)

---

## Implementation checklist

- [x] Documented in source review
- [x] `verification_display.py` — student status + labels
- [x] Public API — strip `field_evidence`; add student verification fields
- [x] Admin evidence endpoint
- [x] `VerificationStrip.tsx` replaces public `TrustCard`
- [x] Hide change history on public detail
- [x] Filter internal snippets from any public evidence path
