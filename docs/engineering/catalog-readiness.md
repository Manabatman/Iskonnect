# Catalog readiness report



**Owner:** Engineering / Product  

**Last verified:** 2026-08-01 (B12 import batch)  

**Task:** OPS-01



## Executive summary



**Launch recommendation: Do not launch publicly.** Production catalog (Supabase) has **117 published** active listings after B12 staging import (2026-08-01). The launch gate requires **≥300 published listings** with **median verification age under 90 days**. Median verification age is **~6.3 days** — within the 90-day gate. Catalog **depth** remains the primary blocker (**~183 listings short**). ISKONNECT does **not** promise students a 30-day re-verification SLA; see `verification-capacity.md`.



## Measured counts (production — 2026-08-01)



| Metric | Count | Source |

| --- | ---: | --- |

| Published (`is_active = true`) | **117** | Supabase live query |

| Verified within 90 days | **77** | Supabase live query |

| Distinct providers | **63** | Supabase live query |

| Median verification age | **~6.3 days** | Supabase `PERCENTILE_CONT` |

| Publishable for matching | **38** | `is_publishable` gate on active rows |

| Hand-seeded baseline (repo) | ~24 | `seed_data.py` (dev/CI only) |



### Production measurement query



```sql

SELECT

  COUNT(*) FILTER (WHERE is_active = true) AS published,

  COUNT(*) FILTER (

    WHERE is_active = true

      AND last_verified_at >= NOW() - INTERVAL '90 days'

  ) AS verified_within_90d,

  COUNT(DISTINCT provider) FILTER (WHERE is_active = true) AS distinct_providers,

  PERCENTILE_CONT(0.5) WITHIN GROUP (

    ORDER BY EXTRACT(EPOCH FROM (NOW() - last_verified_at)) / 86400

  ) FILTER (WHERE is_active = true AND last_verified_at IS NOT NULL) AS median_verification_age_days

FROM scholarships;

```



**Result pasted 2026-08-01:** published=117, verified_within_90d=77, distinct_providers=63, median_verification_age_days≈6.28.



## Gap analysis



| Gate | Target | Current | Gap |

| --- | ---: | ---: | --- |

| Published listings | ≥300 | 117 | **~183 short** |

| Median verification age | <90 days | ~6.3 days | **Met** |

| Publishable match catalog | ≥300 (ideal) | 38 | Completeness gate filters 117→38 |

| Broken links (active) | <1% | 37.6% | Quality backlog — see B12 quality report |



## B12 import progress (2026-08-01)



- Staging workflow executed: 14 rows (6 Gemini net-new + 8 discovery updates). See `docs/engineering/reports/b12-import-batch-2026-08-01.md`.

- Catalog grew **114 → 117** published active rows.

- Additional Gemini/discovery CSV batches required to approach 300.



## Launch blocker assessment



1. **Catalog depth** — Primary blocker (~183 listings short of 300).

2. **Publishability** — Only 38/117 active rows pass the match publishability gate; import batches should target completeness ≥40 before approve.

3. **Link health** — 37.6% broken links on active rows (automated validation + manual review needed).

4. **Verification freshness** — 90-day median gate **met** at current scale.



## Recommendations



1. **Do not open public marketing** until published count ≥300 **or** an explicit regional pilot with honest copy.

2. Continue B12 batches via staging (never direct production writes).

3. Raise completeness on imported rows before approve; target publishable ratio >80%.

4. Run link checker remediation on broken_link rows before next import batch.



## What would change this recommendation



- Production published count ≥300 with median verification age <90 days

- Publishable match catalog ≥200 with broken links <5%

- Student-facing copy reintroducing a fixed 30-day SLA (prohibited per A7)

