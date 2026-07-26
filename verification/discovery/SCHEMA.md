# Discovery Output Schema

Extends `NEW_SCHOLARSHIP_KEYS` from `app/verification/report_schema.py` with mission-required metadata for import review.

## validated_new_scholarships.json (array of objects)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| title | string | yes | Official program name |
| aliases | string[] | no | Abbreviations, alternate names |
| provider | string | yes | |
| provider_type | string | yes | Government, Private, Institutional, LGU |
| scholarship_type | string | yes | Merit-based, Need, Merit-and-Need, Affiliation |
| legal_basis | string | no | RA/CMO/JMC when applicable |
| primary_link | string | yes | Official program page |
| application_portal_url | string | no | Separate portal if any |
| description | string | yes | |
| eligible_levels | string[] | yes | College, Graduate, Faculty, etc. |
| eligible_courses_psced | string[] | no | STEM, Agriculture, etc. |
| eligible_courses_specific | string[] | no | |
| citizenship_required | string | no | Filipino, etc. |
| academic_requirements | string | no | GWA, exam, year level |
| min_gwa_normalized | number | no | 0–100 scale |
| max_income_threshold | number | no | PHP annual unless noted |
| income_requirements | string | no | Free-text when structured cap unclear |
| geographic_restrictions | string | no | |
| eligible_regions | string[] | no | |
| priority_groups | string[] | no | |
| members_only | boolean | no | OWWA membership, etc. |
| benefits | string | no | Summary of package |
| benefit_summary | string | yes | Short import summary |
| required_documents | string[] | no | |
| maintaining_requirements | string | no | |
| renewal_rules | string | no | |
| return_service | string | no | |
| has_return_service | boolean | no | |
| application_status | string | no | open, expected_reopen, closed_for_this_cycle |
| application_open_date | string | no | ISO date; empty if cannot_verify |
| application_deadline | string | no | ISO date; empty if cannot_verify |
| cycle_type | string | no | annual, semester, rolling |
| contact_email | string | no | |
| contact_phone | string | no | |
| source_urls | string[] | yes | All evidence URLs |
| evidence_snippet | string | yes | Quote from official source |
| last_updated | string | no | Publication/update date from source |
| verification_confidence | string | yes | verified, partially_verified, cannot_verify |
| discovery_classification | string | yes | add_immediately |
| research_candidate_id | string | no | PDF slug for traceability |

## existing_scholarships.csv

`research_title,research_provider,matched_id,matched_title,match_basis,suggested_updates,verification_confidence,source_url,evidence_snippet,verified_at`

## duplicate_candidates.json

Array: `{ research_title, research_provider, matched_ids[], match_type, reasoning, recommended_resolution, verification_confidence, source_urls[] }`

## rejected_candidates.json

Array: `{ research_title, research_provider, classification, reason, verification_confidence, source_urls[] }`

Classification values: `not_a_scholarship`, `cannot_verify`, `out_of_scope`
