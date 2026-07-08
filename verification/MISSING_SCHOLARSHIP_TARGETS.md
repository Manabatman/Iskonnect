# Missing Scholarship Search Targets

Search targets only — **no searching during export**. Use during ChatGPT verification conversations.

## Government

| Target | Official domain | Why it may be missing |
|--------|-----------------|----------------------|
| DOST-SEI JLSS | science-scholarships.ph | In DB as archived — confirm current status |
| DOST RA 7687 vs Merit | sei.dost.gov.ph | Separate tracks; verify both active |
| CHED-TES / UniFAST TES | unifast.gov.ph | May overlap with CHED Merit entries |
| TDP / TDDP | unifast.gov.ph | Distinct from TES |
| TESDA brand programs | tesda.gov.ph | Generic homepage may hide specific programs |
| GSIS GESP / GSSP | gsis.gov.ph | Partially in catalog |
| SSS educational assistance | sss.gov.ph | Loan vs grant distinction |
| OWWA EDSP / OFWD | owwa.gov.ph | Multiple OWWA education programs |
| OWWA Skills-for-Employment | owwa.gov.ph | May not be in catalog |
| Pag-IBIG educational programs | pagibigfund.gov.ph | Not in catalog |
| Landbank educational programs | landbank.com | Not in catalog |
| PVAO educational benefits | pvao.gov.ph | Beyond AFPSLAI/AFPEBSO |
| AFP dependent programs | afp.mil.ph | Military affiliation bundle |

## Private foundations

| Target | Official domain | Why it may be missing |
|--------|-----------------|----------------------|
| SM tech-voc vs college | sm-foundation.org | Separate tracks |
| Metrobank program pages | metrobank-foundation.org | Program-specific URLs |
| Ayala Foundation grants | ayalafoundation.org | Multiple programs |
| BPI Foundation | bpifoundation.org | Program-specific pages |
| Megaworld partner universities | megaworldfoundation.com | Partner list may be incomplete |

## Universities

| Target | Official domain | Why it may be missing |
|--------|-----------------|----------------------|
| UP System grants | up.edu.ph | Multiple grant types |
| Ateneo financial aid | ateneo.edu | Beyond catalog entry |
| DLSU scholarships | dlsu.edu.ph | Not fully cataloged |
| UST grant types | ust.edu.ph | Beyond equity scholarship |
| PUP individual grants | pup.edu.ph | May have multiple programs |

## LGU

| Target | Official domain | Why it may be missing |
|--------|-----------------|----------------------|
| Manila city scholarships | manila.gov.ph | Not yet in catalog |
| Caloocan LGU | caloocan.gov.ph | Not yet in catalog |
| Las Piñas LGU | laspinas.gov.ph | Not yet in catalog |
| Other NCR cities | *.gov.ph | Coverage gaps |

## International

| Target | Official domain | Why it may be missing |
|--------|-----------------|----------------------|
| JASSO | jasso.go.jp | International section |
| MEXT | mext.go.jp | Japan scholarships |
| Australia Awards | dfat.gov.au | Not in catalog |
| Fulbright Philippines | amchamphilippines.com / usembassy.gov | Not in catalog |

## How to report findings

- **Existing program, wrong/missing in ISKONNECT** → `new_scholarships.json`
- **Existing row, field wrong** → `field_changes.csv` with evidence
- **Program confirmed discontinued** → `field_changes.csv` with `program_discontinued` + closure type
