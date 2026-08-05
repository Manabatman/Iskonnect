# Gap analysis — verification reports vs codebase

**Generated:** 2026-08-05  
**Status vocabulary:** Already implemented · Partially implemented · Data issue only · Code issue · UX issue · Still missing · Obsolete · Conflicts with current implementation

---

## Engine / schema

| Finding | Status | Why | Files | Type | P | Effort |
|---------|--------|-----|-------|------|---|--------|
| Sparse columns + join tables (048) | Already implemented | Alembic applied | `048_*.py`, `models.py` | migration | — | — |
| Per-gate evaluators | Partially implemented | All `GATE_*=false` | `eligibility_gates.py`, `config.py` | backend | P1 | S |
| Academic OR (BPMSP #76) | Partially implemented | Data OK; gate off | `eligibility_gates.py` | backend+data | P1 | S |
| Affiliation enforcement gate-off | Still missing | Returns N/A when gate off | `evaluate_required_affiliations` | backend | P0 | S |
| Conflict enforcement gate-off | Partially implemented | Same N/A pattern | `evaluate_conflict_scopes` | backend | P1 | S |
| Destination / study preference | Still missing | No evaluator; no profile enum | `eligibility_result.py`, profiles | backend+frontend | P0 | M |
| Natural-born citizenship | Still missing | Coarse Filipino only | `eligibility_result.py` | backend | P2 | M |
| Gender restriction (Ayala #11) | Still missing | No evaluator | `eligibility_result.py` | backend+data | P1 | S |
| Renewal rules | Still missing (by design) | Out of matching scope | `_inventory_rules.py` | docs | P2 | L |
| JLSS application vs award year | Still missing | No dual-year model | eligibility | backend | P1 | M |
| CMSP weighted score | Still missing | Selection not hard gate | scoring | backend | P2 | M |
| Detail/Eligibility enrichment | Code issue | Raw dict without joins | `scholarships.py` | backend | P0 | S |
| members_only vs affiliations (#7) | Conflicts | Dual truths | models + gates | architecture | P1 | S |
| Report DDL names | Obsolete | Superseded by 048 sparse columns | 048 | docs | — | — |

---

## Catalog data (live verified 2026-08-05)

| Finding | Status | IDs | Fix | Type | P |
|---------|--------|-----|-----|------|---|
| Gabay Guro wrong courses | Data issue only | 16 | Education / BEED-BSED | data | P0 |
| Pagpupugay no frontliner | Data + taxonomy | 14 | medical_frontliner_dependent affiliation | data+UX | P0 |
| MEXT/GKS empty countries | Data issue only | 81, 65 | Japan / South Korea | data | P0 |
| JLSS inactive | Data issue only | 130 | Activate + structure | data | P0 |
| Megaworld/SM partners empty | Data issue only | 61, 10 | Partner allowlists | data | P0 |
| MSRS income wrong | Data issue only | 54 | 450k | data | P0 |
| DOST #3 wrong income/gwa | Data issue only | 3 | Null; use 133–136 | data | P1 |
| ASTHRDP/ERDT consortium incomplete | Partially implemented | 133, 134 | Complete 8-uni lists | data | P1 |
| CBPSME/STRAND schools empty | Data issue only | 135, 136 | Consortium data | data | P1 |
| GSSP parent SG null | Data issue only | 78 | max_parent_salary_grade=15 | data | P1 |
| Estatistikolar too broad | Data issue only | 119 | Statistics-specific | data | P1 |
| SIKAP missing affiliation | Data issue only | 120 | hei_faculty join | data | P1 |
| CoScho/GESP affiliations unused | Partially implemented | 117, 84, 78 | Affiliation fallback | backend | P0 |
| Image upload env | UX/ops | Admin | SUPABASE_URL + service role | config | P0 |

---

## False positive / false negative (public beta trust)

| Risk | Status | P |
|------|--------|---|
| Grade12 CompEng → MEXT/GKS/GESP/Gabay/Pagpupugay | Confirmed | P0 |
| JLSS FN (#130 inactive) | Confirmed | P0 |
| Non-partner Megaworld/SM | Confirmed | P0 |
| MSRS income 450–600k FP | Confirmed | P0 |
| QCSP multi-track GWA | Partial | P1 |
| DOST #3 income over-filter | Confirmed | P1 |
| Student sees internal verification UI | Confirmed UX | P0 |

---

## Student verification UX gap

| Surface | Status | Issue | Files |
|---------|--------|-------|-------|
| TrustCard on detail | UX issue | Field evidence, snippets, “Imported” | `TrustCard.tsx`, `ScholarshipDetailPage.tsx` |
| Public API field_evidence | UX issue | Full evidence on GET /scholarships/{id} | `scholarships.py`, `field_evidence.py` |
| Badge copy | UX issue | Database-centric labels | `verification_display.py` |
| Change history public | UX issue | Internal diffs on student page | `ScholarshipDetailPage.tsx` |

**Target:** Student strip (Verified / Needs Review / Archived) + admin-only evidence trail. See [`student_verification_ux.md`](student_verification_ux.md).
