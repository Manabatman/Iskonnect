# Application Cycle Re-verification (July 2026)

**Verification date:** 2026-07-09  
**Reference date (as-of):** July 2026  
**Scope:** 8 scholarships from pilot bundles (`ched_unifast`, `dost`) plus JLSS (id 79)  
**Method:** 2026-first search on official domains; fallback to 2025/2024 only to determine cycle status — never to populate forward-looking `application_open_date` / `application_deadline` when the next cycle is unannounced.

## Executive summary

| ID | Program | Latest official cycle | Status (Jul 2026) | DB dates valid? | Correction required |
|----|---------|----------------------|-------------------|-----------------|---------------------|
| 1 | CHED Merit (CMSP) | AY 2025-2026 closed 2025-06-20 | `expected_reopen` | No — placeholders | Yes |
| 2 | DOST-SEI Undergraduate | AY 2026-2027 intake closed 2025-12-05 | `closed_for_this_cycle` | No — wrong year/values | Yes |
| 3 | DOST-SEI Graduate | Per-university AY 2025-2026 | `expected_reopen` | No — umbrella dates invalid | Yes |
| 5 | Tulong Dunong (TDP) | HEI-coordinated; no national 2026 calendar | `expected_reopen` | No — fabricated | Yes |
| 6 | UniFAST TES | HEI-coordinated; no national 2026 calendar | `expected_reopen` | No — fabricated | Yes |
| 19 | CHED K-12 Transition | Discontinued | `permanently_discontinued` | No — misleading future dates | Yes |
| 76 | BPMSP HE Track | AY 2026-2027 closed 2026-06-30 | `closed_for_this_cycle` | Partially — dates match official call | Yes (status only) |
| 79 | DOST-SEI JLSS | AY 2025-2026 intake closed 2025-05-23 | `expected_reopen` | No — archived + wrong dates | Yes |

### Critical pilot errors to fix

1. **DOST UG (id 2):** Pilot `field_changes.csv` recommended carrying **2024-10-13 / 2024-12-23** as `official_value`. That violates the no-carry-forward rule. The verified **2026 undergraduate cycle** (for AY 2026-2027 intake) ran **2025-10-20 → 2025-12-05** per DOST-SEI official Facebook — but that window is **already closed** as of July 2026; do not expose it as the live application window.
2. **All records with DB `application_open_date` in 2026** without official 2026 announcements (ids 1, 2, 3, 5, 6, 19) are **unsupported placeholders** and should be cleared pending the next official call.
3. **science-scholarships.ph homepage** still displays the **2024** undergraduate timeline (Oct–Dec 2024). Do not use that stale page for current cycle dates.

---

## Summary table

| ID | Title | DB open | DB deadline | DB status | Pilot recommended | Latest official open | Latest official deadline | Official AY | Correction? |
|----|-------|---------|-------------|-----------|-------------------|---------------------|-------------------------|-------------|-------------|
| 1 | CMSP | 2026-03-01 | 2026-06-30 | expected_reopen | cannot_verify open; deadline 2025-06-20 | cannot_verify | cannot_verify | Next call not published | **Yes** |
| 2 | DOST UG | 2026-02-01 | 2026-04-15 | expected_reopen | **2024-10-13 / 2024-12-23** (invalid) | 2025-10-20 | 2025-12-05 | 2026-2027 (intake closed) | **Yes** |
| 3 | DOST Grad | 2026-03-01 | 2026-05-31 | expected_reopen | cannot_verify | cannot_verify | cannot_verify | Per-program | **Yes** |
| 5 | TDP | 2026-04-01 | 2026-07-31 | open | expected_reopen | cannot_verify | cannot_verify | HEI-dependent | **Yes** |
| 6 | TES | 2026-05-01 | 2026-08-31 | open | expected_reopen | cannot_verify | cannot_verify | HEI-dependent | **Yes** |
| 19 | K-12 Transition | 2026-03-01 | 2026-06-30 | previous_cycle | permanently_discontinued | N/A | N/A | N/A | **Yes** |
| 76 | BPMSP HE | 2026-04-30 | 2026-06-30 | previous_cycle | cannot_verify | 2026-04-30 | 2026-06-30 | 2026-2027 (intake closed) | **Yes** |
| 79 | JLSS | 2026-04-13 | 2026-05-15 | archived | (not in pilot) | cannot_verify (2026) | cannot_verify (2026) | 2025-2026 last cycle closed | **Yes** |

---

## Per-scholarship detail

### ID 1 — CHED Merit Scholarship Program (CMSP)

**Previous recorded dates**

| Source | open | deadline | status | academic_year |
|--------|------|----------|--------|---------------|
| Supabase | 2026-03-01 | 2026-06-30 | expected_reopen | 2026-2027 |
| Pilot field_changes | cannot_verify | 2025-06-20 (last published) | expected_reopen | — |

**2026-first search:** No national call for **AY 2026-2027** CMSP found on `legacy.ched.gov.ph/merit-scholarship` or CHED issuances index. Latest national call is **Memorandum from the Executive Director No. 336, s. 2025** for **AY 2025-2026**.

**Latest official cycle (closed)**

| Field | Value |
|-------|-------|
| Academic year | 2025-2026 |
| Open | ~2025-05-20 (regional; Caraga RO filing period) |
| Deadline | **2025-06-20** |
| Status as of Jul 2026 | Closed for this cycle |

**Latest official dates for next cycle:** `cannot_verify`

**Evidence**

| URL | Publication | Snippet |
|-----|-------------|---------|
| https://legacy.ched.gov.ph/merit-scholarship/ | Current page (2025 call) | "AY 2025-2026 is now CLOSED! … deadline … June 20, 2025" |
| https://caraga.ched.gov.ph/ched-scholarship-program-csp/ | 2025 regional call | "Period of filing … May 20 until June 20, 2025 ONLY" |

**Confidence:** `verified` (last cycle closed); `cannot_verify` (next cycle dates)

**Correction required:** **Yes**

- Clear `application_open_date` and `application_deadline` (unsupported 2026 placeholders).
- Set `application_status` = `expected_reopen`.
- Set `last_open_date` = 2025-05-20, `last_close_date` = 2025-06-20 (historical).
- Set `academic_year_target` = null or remove until AY 2026-2027 call is published.

> The provider has not yet published the official 2026-2027 application schedule for CMSP on the national program page.

---

### ID 2 — DOST-SEI Undergraduate Scholarship

**Previous recorded dates**

| Source | open | deadline | status |
|--------|------|----------|--------|
| Supabase | 2026-02-01 | 2026-04-15 | expected_reopen |
| Pilot field_changes | **2024-10-13** | **2024-12-23** | expected_reopen |

**2026-first search:** Official **2026 DOST-SEI Undergraduate Scholarship** cycle confirmed via DOST-SEI official Facebook (provider official page). `science-scholarships.ph` homepage still shows **2024** dates — **do not use** for current cycle.

**Latest official cycle (closed as of July 2026)**

| Field | Value |
|-------|-------|
| Academic year target | 2026-2027 (intake) |
| Open | **2025-10-20** |
| Deadline | **2025-12-05** (extended; registered by 2025-11-24) |
| Qualifying exam | 2026-02-21 – 2026-02-22 |
| Status as of Jul 2026 | **Closed for this cycle** |

**Next cycle (AY 2027-2028):** `cannot_verify` — not announced on official portal as of verification.

**Evidence**

| URL | Publication | Snippet |
|-----|-------------|---------|
| https://www.facebook.com/DOST.SEI/posts/1312658064226102/ | DOST-SEI official Facebook | "deadline for the 2026 Undergraduate Scholarships Application is now December 5, 2025" |
| https://www.science-scholarships.ph/pdf/forms/2026%20DOST-SEI%20S&T%20Undergraduate%20Application%20Form%20I.pdf | 2026 form set | "2026 DOST-SEI Science and Technology Undergraduate Scholarships Application Form" |
| https://www.science-scholarships.ph/ | Stale homepage | Still lists Oct–Dec **2024** application timeline — superseded |

**Confidence:** `verified` (2026-labelled intake cycle dates via official Facebook); `cannot_verify` (next cycle)

**Correction required:** **Yes**

- **Revert pilot error:** Remove `official_value` rows recommending 2024-10-13 / 2024-12-23.
- Clear DB `application_open_date` / `application_deadline` (2026-02-01 / 2026-04-15 are invalid).
- Set `application_status` = `closed_for_this_cycle` (or `expected_reopen` if ISKONNECT treats post-deadline recurring programs as awaiting next call).
- Set `last_open_date` = 2025-10-20, `last_close_date` = 2025-12-05.
- Portal URL correction (separate from cycle pass): `ugrad.science-scholarships.ph` or `ugs.science-scholarships.ph` per current e-system.

> The provider has not yet published the official **next** (AY 2027-2028) application schedule. Do not display 2024 or stale homepage dates.

---

### ID 3 — DOST-SEI Graduate Scholarship (umbrella)

**Previous recorded dates**

| Source | open | deadline | status |
|--------|------|----------|--------|
| Supabase | 2026-03-01 | 2026-05-31 | expected_reopen |
| Pilot field_changes | cannot_verify | cannot_verify | expected_reopen |

**2026-first search:** No single national graduate application window. ASTHRDP/CBPSME/ERDT/STRAND publish **university-specific** deadlines for **AY 2025-2026** on `science-scholarships.ph` (e.g. UP Los Baños May 30 / Oct 30, 2025).

**Latest official dates:** `cannot_verify` at umbrella-record level.

**Status as of Jul 2026:** `expected_reopen` — programs remain active via consortium universities; each university may still accept for upcoming terms per its own calendar.

**Evidence**

| URL | Publication | Snippet |
|-----|-------------|---------|
| https://www.science-scholarships.ph/ | Program hub | ASTHRDP deadlines listed per university for AY 2025-2026 |
| https://science-scholarships.ph/pdf/2025_ASTHRDP_Brochure.pdf | 2025 brochure | Applications submitted to NSC member-university project leader |

**Confidence:** `cannot_verify` (single open/deadline on umbrella record)

**Correction required:** **Yes**

- Clear `application_open_date`, `application_deadline`, and misleading `academic_year_target` on umbrella record.
- Flag record for split into program-specific entries (ASTHRDP, ERDT, etc.).

> The provider has not published a single national graduate application schedule suitable for this umbrella record.

---

### ID 5 — Tulong Dunong Program (TDP)

**Previous recorded dates**

| Source | open | deadline | status |
|--------|------|----------|--------|
| Supabase | 2026-04-01 | 2026-07-31 | **open** |
| Pilot field_changes | — | — | expected_reopen |

**2026-first search:** No national TDP application calendar for 2026 on `unifast.gov.ph`. Program guidelines are evergreen; applications coordinated through **HEI UniFAST focal person** when a call is issued.

**Latest official dates:** `cannot_verify` (national open/deadline)

**Status as of Jul 2026:** `expected_reopen` — program active; timing depends on HEI and fund availability.

**Evidence**

| URL | Publication | Snippet |
|-----|-------------|---------|
| https://unifast.gov.ph/tes.html | Evergreen | "Coordinate with the UniFAST Focal Person of the HEI once there is a Call for TES Application" |
| https://unifast.gov.ph/assets/pdf/infgrfx/TES2025.pdf | TES/TDP brochure | TDP PhP7,500/sem; prioritization subject to fund availability |

**Confidence:** `partially_verified` (status); `cannot_verify` (dates)

**Correction required:** **Yes**

- Clear fabricated 2026-04-01 / 2026-07-31 dates.
- Change `application_status` from `open` to `expected_reopen`.
- Do not invent national open/close dates.

> The provider has not yet published a national 2026 TDP application schedule. Applications are HEI-coordinated.

---

### ID 6 — UniFAST Tertiary Education Subsidy (TES)

**Previous recorded dates**

| Source | open | deadline | status |
|--------|------|----------|--------|
| Supabase | 2026-05-01 | 2026-08-31 | **open** |
| Pilot field_changes | — | — | expected_reopen |

**2026-first search:** No national TES "Call for Application" memorandum dated 2026 found on `unifast.gov.ph/press-rel.html` (latest press releases are older). TES remains HEI-coordinated per official program page.

**Latest official dates:** `cannot_verify`

**Status as of Jul 2026:** `expected_reopen`

**Evidence**

| URL | Publication | Snippet |
|-----|-------------|---------|
| https://unifast.gov.ph/tes.html | Evergreen | "Please coordinate with the UniFAST Focal Person of the HEI once there is a Call for TES Application" |

**Confidence:** `partially_verified` (status); `cannot_verify` (dates)

**Correction required:** **Yes**

- Clear fabricated 2026-05-01 / 2026-08-31 dates.
- Change `application_status` from `open` to `expected_reopen`.
- Set `cycle_type` = `annual` (confirmed from TES brochure).

> The provider has not yet published the official 2026 national TES application schedule.

---

### ID 19 — CHED K-12 Transition Scholarship

**Previous recorded dates**

| Source | open | deadline | status |
|--------|------|----------|--------|
| Supabase | 2026-03-01 | 2026-06-30 | previous_cycle |
| Pilot field_changes | — | — | permanently_discontinued |

**2026-first search:** Program discontinued. Graduate scholarship component closed; nominations closed AY 2017-2018.

**Latest official dates:** N/A — program no longer accepts applications.

**Status as of Jul 2026:** `permanently_discontinued`

**Evidence**

| URL | Publication | Snippet |
|-----|-------------|---------|
| https://chedk12.wordpress.com/sgs/ | Historical | "Nominations for A.Y. 2017-2018 are now closed" |
| https://legacy.ched.gov.ph/k-12-project-management-unit/ | CHED legacy | K-12 Transition Program historical reference |

**Confidence:** `verified`

**Correction required:** **Yes**

- Archive record (`is_active` = false).
- Clear all future-dated application fields.
- Remove misleading `academic_year_target` = 2026-2027.

---

### ID 76 — Bagong Pilipinas Merit Scholarship Program (BPMSP) — HE Track

**Previous recorded dates**

| Source | open | deadline | status |
|--------|------|----------|--------|
| Supabase | 2026-04-30 | 2026-06-30 | previous_cycle |
| Pilot field_changes | cannot_verify | cannot_verify | expected_reopen |

**2026-first search:** Official **AY 2026-2027** call found via **CHED Regional Office 10 official Facebook** (CHED provider official page). JMC No. 1 s. 2026 FAQ on `caraga.ched.gov.ph` confirms program rules but does not state calendar dates.

**Latest official cycle (closed as of July 2026)**

| Field | Value |
|-------|-------|
| Academic year | 2026-2027 (First Semester) |
| Open | **2026-04-30** |
| Deadline | **2026-06-30** (or until slots filled) |
| Status as of Jul 2026 | **Closed for this cycle** (deadline passed) |

**Next cycle:** `cannot_verify`

**Evidence**

| URL | Publication | Snippet |
|-----|-------------|---------|
| https://www.facebook.com/chedro10/posts/1324867456497423/ | CHED RO 10 official Facebook | "Application Period: 30 April 2026 – 30 June 2026 … AY 2026–2027" |
| https://caraga.ched.gov.ph/wp-content/uploads/2026/05/BPMSP_FAQ_0428.pdf | May 2026 | JMC No. 1, Series of 2026; GAA FY 2026; portal bpms.ched.gov.ph |
| https://legacy.ched.gov.ph/ched-landbank-team-up-to-speed-up-scholarship-and-grant-releases/ | 2026-03-12 | "rollout of the Bagong Pilipinas Merit Scholarship Program this year" |

**Confidence:** `verified` (2026-2027 intake window via CHED official regional announcement); `cannot_verify` (next cycle)

**Correction required:** **Yes** (status correction)

- DB dates **2026-04-30 / 2026-06-30 match** the official call — pilot `cannot_verify` was overly cautious.
- Change `application_status` from `previous_cycle` to **`closed_for_this_cycle`**.
- Set `last_open_date` = 2026-04-30, `last_close_date` = 2026-06-30.
- Keep `application_open_date` / `application_deadline` as historical last cycle OR clear until next call (ISKONNECT policy: prefer clearing forward fields when window closed and next unannounced).

> Next BPMSP cycle dates not yet published as of July 2026.

---

### ID 79 — DOST-SEI Junior Level Science Scholarship (JLSS)

**Previous recorded dates**

| Source | open | deadline | status | is_active |
|--------|------|----------|--------|-----------|
| Supabase | 2026-04-13 | 2026-05-15 | archived | false |
| Pilot | (not verified) | — | — | — |

**2026-first search:** No **2026** JLSS application schedule on `jlss.science-scholarships.ph` or `science-scholarships.ph`. Latest published JLSS timeline on official portal is **2025 cycle**.

**Latest official cycle (closed)**

| Field | Value |
|-------|-------|
| Academic year | 2025-2026 (award effective 1st sem AY 2025-2026) |
| Open | **2025-04-21** |
| Deadline | **2025-05-23** |
| Qualifying exam | **2025-07-27** |
| Post-qualification docs | 2025-08-04 – 2025-08-24 |

**2026 JLSS dates:** `cannot_verify`

**Status as of Jul 2026:** Program appears **active** (portal accepts registration); last published cycle **closed**. Recommend `expected_reopen`, **not** `archived`.

**Evidence**

| URL | Publication | Snippet |
|-----|-------------|---------|
| https://www.science-scholarships.ph/ | Official hub | JLSS: "Start … APR 2025 … Last Day … MAY 23, 2025 … Exam JUL 2025" |
| https://jlss.science-scholarships.ph/ | JLSS portal | Open to regular 2nd-year students; post-exam docs Aug 4–24, 2025 |

**Confidence:** `verified` (2025 cycle closed); `cannot_verify` (2026 cycle); `partially_verified` (program still offered)

**Correction required:** **Yes**

- **Un-archive** if program remains on official DOST-SEI portal.
- Clear fabricated 2026-04-13 / 2026-05-15 dates.
- Set `application_status` = `expected_reopen`.
- Set `last_open_date` = 2025-04-21, `last_close_date` = 2025-05-23.

> The provider has not yet published the official 2026 JLSS application schedule.

---

## Records where 2026 cycle not officially announced (forward dates)

The following should **not** display national application open/deadline until the next official call:

| ID | Program | Note |
|----|---------|------|
| 1 | CMSP | National AY 2026-2027 call not published |
| 2 | DOST UG | AY 2026-2027 intake closed; AY 2027-2028 not announced |
| 3 | DOST Graduate | No umbrella schedule |
| 5 | TDP | HEI-coordinated only |
| 6 | TES | HEI-coordinated only |
| 79 | JLSS | 2026 JLSS schedule not published |

---

## Corrections backlog (append to bundle `field_changes.csv`)

Read-only report — import after human review. Use `verified_at` = 2026-07-09.

### ched_unifast/field_changes.csv (supplement)

```csv
id,field,iskconnect_value,official_value,action,change_reason,closure_type,confidence,source_url,evidence_snippet,official_last_updated,announcement_date,verified_at
1,application_open_date,2026-03-01,,update,annual_cycle_update,closed_for_this_cycle,cannot_verify,https://legacy.ched.gov.ph/merit-scholarship/,"No AY 2026-2027 CMSP call published; clear unsupported placeholder",,,2026-07-09
1,application_deadline,2026-06-30,,update,annual_cycle_update,closed_for_this_cycle,cannot_verify,https://legacy.ched.gov.ph/merit-scholarship/,"No AY 2026-2027 CMSP call published; clear unsupported placeholder",,,2026-07-09
1,last_open_date,2025-03-01,2025-05-20,update,annual_cycle_update,closed_for_this_cycle,verified,https://caraga.ched.gov.ph/ched-scholarship-program-csp/,"Regional filing opened May 20, 2025",,2025-05-20,2026-07-09
1,last_close_date,2025-06-30,2025-06-20,update,annual_cycle_update,closed_for_this_cycle,verified,https://legacy.ched.gov.ph/merit-scholarship/,"National deadline June 20, 2025 for AY 2025-2026",,2025-06-20,2026-07-09
5,application_open_date,2026-04-01,,update,annual_cycle_update,closed_for_this_cycle,cannot_verify,https://unifast.gov.ph/tes.html,"No national TDP 2026 calendar; HEI-coordinated",,,2026-07-09
5,application_deadline,2026-07-31,,update,annual_cycle_update,closed_for_this_cycle,cannot_verify,https://unifast.gov.ph/tes.html,"No national TDP 2026 calendar; HEI-coordinated",,,2026-07-09
5,application_status,open,expected_reopen,update,annual_cycle_update,closed_for_this_cycle,partially_verified,https://unifast.gov.ph/tes.html,"Active program; timing via HEI UniFAST focal person",,,2026-07-09
6,application_open_date,2026-05-01,,update,annual_cycle_update,closed_for_this_cycle,cannot_verify,https://unifast.gov.ph/tes.html,"No national TES 2026 calendar published",,,2026-07-09
6,application_deadline,2026-08-31,,update,annual_cycle_update,closed_for_this_cycle,cannot_verify,https://unifast.gov.ph/tes.html,"No national TES 2026 calendar published",,,2026-07-09
6,application_status,open,expected_reopen,update,annual_cycle_update,closed_for_this_cycle,partially_verified,https://unifast.gov.ph/tes.html,"Active program; HEI-coordinated calls",,,2026-07-09
19,application_open_date,2026-03-01,,update,program_discontinued,permanently_discontinued,verified,https://chedk12.wordpress.com/sgs/,"Program discontinued; clear misleading dates",,,2026-07-09
19,application_deadline,2026-06-30,,update,program_discontinued,permanently_discontinued,verified,https://chedk12.wordpress.com/sgs/,"Program discontinued; clear misleading dates",,,2026-07-09
19,academic_year_target,2026-2027,,update,program_discontinued,permanently_discontinued,verified,https://legacy.ched.gov.ph/k-12-project-management-unit/,"No active academic year; program ended",,,2026-07-09
76,application_status,previous_cycle,closed_for_this_cycle,update,annual_cycle_update,closed_for_this_cycle,verified,https://www.facebook.com/chedro10/posts/1324867456497423/,"AY 2026-2027 window Apr 30–Jun 30, 2026; closed as of July 2026",,2026-04-30,2026-07-09
76,application_open_date,2026-04-30,2026-04-30,confirm_unchanged,annual_cycle_update,closed_for_this_cycle,verified,https://www.facebook.com/chedro10/posts/1324867456497423/,"Official CHED RO10 call: opens 30 April 2026",,2026-04-30,2026-07-09
76,application_deadline,2026-06-30,2026-06-30,confirm_unchanged,annual_cycle_update,closed_for_this_cycle,verified,https://www.facebook.com/chedro10/posts/1324867456497423/,"Official CHED RO10 call: closes 30 June 2026",,2026-06-30,2026-07-09
76,last_open_date,,2026-04-30,update,annual_cycle_update,closed_for_this_cycle,verified,https://www.facebook.com/chedro10/posts/1324867456497423/,"Record last cycle open date",,2026-04-30,2026-07-09
76,last_close_date,,2026-06-30,update,annual_cycle_update,closed_for_this_cycle,verified,https://www.facebook.com/chedro10/posts/1324867456497423/,"Record last cycle close date",,2026-06-30,2026-07-09
```

### dost/field_changes.csv (supplement)

```csv
id,field,iskconnect_value,official_value,action,change_reason,closure_type,confidence,source_url,evidence_snippet,official_last_updated,announcement_date,verified_at
2,application_open_date,2026-02-01,,update,annual_cycle_update,closed_for_this_cycle,cannot_verify,https://www.facebook.com/DOST.SEI/posts/1312658064226102/,"Clear invalid placeholder; next cycle not announced",,,2026-07-09
2,application_deadline,2026-04-15,,update,annual_cycle_update,closed_for_this_cycle,cannot_verify,https://www.facebook.com/DOST.SEI/posts/1312658064226102/,"Clear invalid placeholder; next cycle not announced",,,2026-07-09
2,application_status,expected_reopen,closed_for_this_cycle,update,annual_cycle_update,closed_for_this_cycle,verified,https://www.facebook.com/DOST.SEI/posts/1312658064226102/,"2026 UG intake closed Dec 5, 2025; exam Feb 2026 completed",,2025-12-05,2026-07-09
2,last_open_date,2025-02-01,2025-10-20,update,annual_cycle_update,closed_for_this_cycle,verified,https://www.facebook.com/DOST.SEI/posts/1312658064226102/,"2026 DOST-SEI UG scholarship opened Oct 20, 2025",,2025-10-20,2026-07-09
2,last_close_date,2025-04-15,2025-12-05,update,annual_cycle_update,closed_for_this_cycle,verified,https://www.facebook.com/DOST.SEI/posts/1312658064226102/,"Deadline extended to Dec 5, 2025",,2025-12-05,2026-07-09
2,application_open_date,2026-02-01,2024-10-13,flag_review,annual_cycle_update,closed_for_this_cycle,cannot_verify,https://www.science-scholarships.ph/,"REVERT pilot row: 2024 dates must not be used as official_value",,,2026-07-09
3,application_open_date,2026-03-01,,update,annual_cycle_update,closed_for_this_cycle,cannot_verify,https://www.science-scholarships.ph/,"Umbrella record; no single national graduate schedule",,,2026-07-09
3,application_deadline,2026-05-31,,update,annual_cycle_update,closed_for_this_cycle,cannot_verify,https://www.science-scholarships.ph/,"Umbrella record; per-university deadlines only",,,2026-07-09
79,application_open_date,2026-04-13,,update,annual_cycle_update,closed_for_this_cycle,cannot_verify,https://www.science-scholarships.ph/,"No 2026 JLSS schedule published; clear placeholder",,,2026-07-09
79,application_deadline,2026-05-15,,update,annual_cycle_update,closed_for_this_cycle,cannot_verify,https://www.science-scholarships.ph/,"No 2026 JLSS schedule published; clear placeholder",,,2026-07-09
79,application_status,archived,expected_reopen,update,annual_cycle_update,closed_for_this_cycle,partially_verified,https://jlss.science-scholarships.ph/,"Program still on official portal; last cycle 2025 closed",,,2026-07-09
79,is_active,false,true,flag_review,annual_cycle_update,closed_for_this_cycle,partially_verified,https://jlss.science-scholarships.ph/,"Recommend reactivate; program not discontinued",,,2026-07-09
79,last_open_date,2026-04-13,2025-04-21,update,annual_cycle_update,closed_for_this_cycle,verified,https://www.science-scholarships.ph/,"JLSS 2025 cycle opened Apr 21, 2025",,2025-04-21,2026-07-09
79,last_close_date,2026-05-15,2025-05-23,update,annual_cycle_update,closed_for_this_cycle,verified,https://www.science-scholarships.ph/,"JLSS 2025 cycle closed May 23, 2025",,2025-05-23,2026-07-09
```

### Pilot error flag (id 2)

The following pilot rows in `dost/field_changes.csv` **must be superseded**, not imported:

| Row | Issue |
|-----|-------|
| `application_open_date` → 2024-10-13 | Carries 2024 cycle into DB; violates no-carry-forward rule |
| `application_deadline` → 2024-12-23 | Same |

Replace with: clear forward dates + `last_open_date`/`last_close_date` = 2025-10-20 / 2025-12-05 from DOST-SEI official Facebook.

---

## Next steps

1. Human review of this report (especially BPMSP Facebook source and DOST Facebook dates).
2. Append approved rows to bundle `field_changes.csv` files.
3. Resume provider verification starting with `tesda` bundle.
