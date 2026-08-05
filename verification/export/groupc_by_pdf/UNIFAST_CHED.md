# DATABASE_V3_GROUPC_UNIFAST_CHED.pdf — Implementation Details

Scholarships: 5

## CHED-UniFAST Tulong Dunong Program (CHED-TDP / UniFAST-TDP) (ID: 5)

### Hard eligibility
- citizenship: Filipino citizen
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE
- education_level: Undergraduate / College
- eligible_year_levels: 1st, 2nd, 3rd, 4th, and 5th Year
- incoming_freshman_only: No
- existing_college: Yes
- graduate_students: No
- current_enrollment: Must be enrolled in a first undergraduate degree in State Universities and Colleges (SUCs), CHED-recognized Local Universities and Colleges (LUCs) with Certificate of Program Compliance (COPC), or Private Higher Education Institutions (HEIs) with COPC or listed in the CHED Registry
- academic: Senior High School report card / Form 138 (for incoming freshmen) or a certified true copy of grades for the latest semester attended (for ongoing college students)
- minimum_gwa: 75.00% (passing grade)
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined annual gross family income of parents or legal guardians must not exceed ₱400,000.00
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Restricted to SUCs, CHED-recognized LUCs with COPC, or Private HEIs with COPC / included in the CHED Registry of Programs
- courses: Any recognized undergraduate degree program
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: NOT SPECIFIED IN OFFICIAL SOURCE
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Applicants must not be availing of multiple national government-funded educational grants, except for Free Higher Education under Republic Act 10931, DSWD AICS, or Student Monetary Assistance for Recovery and Transition (SMART)

### Timing
- who: Graduating high school students, incoming college freshmen, and ongoing undergraduate college students
- freshmen/soph/junior/senior/grad/reapply: : Yes | : Yes | : Yes | : Yes | : No | : Yes (grantees must reapply or re-confirm qualification
- window: Varies by CHED Regional Office (CHEDRO) and partner institution schedule → September 30 per JMC guidelines / as announced by regional advisories (Annual (disbursed semestrally at ₱7,500.00 per term); AY AY 2024–2025 / AY 2025–2026)

### Renewal
- maintain_gwa: Maintain a passing General Weighted Average (GWA) of at least 75.00%
- regular_load: Carry a regular academic credit load per semester as determined by the HEI
- no_failures: Maintain passing standing across all enrolled subjects
- return_service: None

### Disqualifiers / affiliations
- Concurrent enjoyment of major national government educational scholarship grants (excluding RA 10931 Free Tuition and DSWD AICS)
- Combined annual family gross income exceeding ₱400,000.00
- Enrollment in non-COPC degree programs or non-recognized private institutions
- Failure to maintain a passing GWA or regular credit load

### Benefits (catalog)
- tuition: Included in the financial grant (up to ₱15,000.00 per AY; serves as a direct subsidy in SUCs/LUCs where tuition is covered under RA 10931)
- stipend: NOT SPECIFIED IN OFFICIAL SOURCE (Integrated into general living allowance)
- allowance: ₱15,000.00 per academic year (₱7,500.00 per semester)

### Documents (operational hidden reqs)
- Fully accomplished UniFAST-TDP Application Form (Annex 2) 2. Certificate of Enrollment (COE) or Certificate of Registration (COR) 3. Certificate of Indigency issued by the Barangay, latest BIR Form 2316 / Income Tax Return, BIR Certificate of Tax Exemption, or Social Case Study Report 4. Academic Record: Form 138 / SF9 for incoming freshmen, or Certified True Copy of Grades for the latest semester attended for ongoing students

### Recommended schema
`json
{
  "education_level": [
    "College"
  ],
  "eligible_year_levels": [
    1,
    2,
    3,
    4,
    5
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": true,
  "minimum_gwa": 75.0,
  "income_limit": 400000,
  "rank_cutoff_alternative": null,
  "priority_courses": null,
  "school_type": [
    "SUC",
    "LUC",
    "Private HEI with COPC"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "06-01",
    "close": "09-30"
  },
  "deadline_type": "institution_dependent",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "return_service_required": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Program Compliance Risk: Applicants enrolled in HEI programs lacking COPC
- verification: Verified | confidence: None

- CONTRADICTION/NOTE: entry GWA (75.00% (passing grade)) vs renewal (Maintain a passing General Weighted Average (GWA) of at least 75.00%)

---

## CHED-UniFAST Tertiary Education Subsidy (TES) (enacted under Republic Act No. 10931, Universal Access to Quality Tertiary Education Act) (ID: 66)

### Hard eligibility
- citizenship: Filipino citizen
- residency/destination: Priority given to students residing and studying in municipalities without public university campuses
- education_level: Undergraduate / College
- eligible_year_levels: 1st, 2nd, 3rd, 4th, and 5th Year
- incoming_freshman_only: No
- existing_college: Yes
- graduate_students: No
- current_enrollment: Must be enrolled in an undergraduate degree program in an SUC, CHED-recognized LUC, or private HEI included in the UniFAST Registry
- academic: Passing GWA and regular academic credit load per term
- minimum_gwa: 75.00% (passing grade per HEI retention standards)
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Dynamically evaluated based on DSWD Listahan 2.0 / 4Ps household income ranking and poverty threshold deciles
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: SUCs, LUCs with institutional recognition, or private HEIs in the official UniFAST Registry
- courses: Any recognized undergraduate degree program
- sectoral/hidden: Priority given to 4Ps / Listahan households, Persons with Disabilities (TES-3A), and students in municipalities without public SUC/LUC campuses
- work_experience: None
- good_moral: NOT SPECIFIED IN OFFICIAL SOURCE
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Evaluated via UniFAST prioritization hierarchy: (1) Continuing StuFAPs grantees, (2) Listahan 2.0 / 4Ps ranked households, (3) Municipality exclusivity applicants

### Timing
- who: Enrolled undergraduate students submitted by their respective HEIs during official UniFAST portal intake calls
- freshmen/soph/junior/senior/grad/reapply: : Yes | : Yes | : Yes | : Yes | : No (except claiming TES-3B licensure reimbursement within 2 | : Yes (continuing grantees are re-validated semestrally)
- window: Set by UniFAST per academic billing cycle → Specified in UniFAST regional advisories (Annual prioritization / Semestral disbursement; AY AY 2024–2025 / AY 2025–2026)

### Renewal
- maintain_gwa: Maintain a passing GWA per semester according to HEI retention rules
- regular_load: Enrolled in a regular credit load per term
- no_failures: Compliance with academic standing requirements
- return_service: None

### Disqualifiers / affiliations
- Enrollment in non-registered private HEIs or non-compliant programs
- Exceeding the maximum residency period of the degree program
- Failure to maintain passing GWA or academic dismissal from the HEI
- Possession of an earned post-secondary or college degree

### Benefits (catalog)
- tuition: TES-1 covers full tuition and school fees in private HEIs (up to ₱20,000.00/sem or ₱40,000.00/AY)
- stipend: Integrated into living allowance (TES-2)
- allowance: TES-2 living allowance: up to ₱40,000.00 per AY (₱20,000.00 per semester)

### Documents (operational hidden reqs)
- Certificate of Enrollment / Registration Form (COR) from UniFAST-registered HEI
- DSWD 4Ps / Listahan Household ID, or Barangay Certificate of Indigency
- Valid Student ID / Government ID
- For TES-3A: PWD ID issued by NCDA / LGU
- For TES-3B: PRC Official Receipt, Review Center Receipt, and Notarized Letter of Intent

### Recommended schema
`
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 75.00, "income_limit": null, "rank_cutoff_alternative": null, "priority_courses": null, "school_type": ["SUC", "LUC", "UniFASTRegistered Private HEI"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "annual_billing", "close": "annual_billing"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": tr[spa n_228](end_span)ue, "first_time_only": false, "return_service_required": false, "needs_manual_review": true }
`

### FP/FN risks & contradictions
- ● Unregistered Private HEI Risk: Recommending TES to students in unregistered private
- verification: Verified | confidence: 96/100

- CONTRADICTION/NOTE: entry GWA (75.00% (passing grade per HEI retention standards)) vs renewal (Maintain a passing GWA per semester according to HEI retention rules)

---

## Scholarship Grant Program for Children and Dependents of Sugarcane Industry Workers and Small Sugarcane Farmers (SIDA-SGP) (ID: 118)

### Hard eligibility
- citizenship: Filipino citizen
- residency/destination: Resident of sugarcane-producing mill districts in the Philippines
- education_level: Undergraduate (College) and Graduate (Master's / Doctoral)
- eligible_year_levels: Undergraduate: Years 1–4; Graduate: Years 1–3
- incoming_freshman_only: No
- existing_college: Yes (with earned units relevant to priority degree programs)
- graduate_students: Yes (Master's and Doctoral degree levels)
- current_enrollment: Enrolled or accepted in an identified State University and College (SUC)
- academic: SHS report card / Form 138 (for freshmen), certified true copy of grades for latest semester (for college), or TOR & Diploma (for graduate applicants)
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Selection ranked 70% Academic + 30% Income; passing GWA required for retention)
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined annual gross income of parents/guardian must not exceed ₱400,000.00 for Undergraduate track; combined annual gross income of applicant/spouse/parents must not exceed ₱500,000.00 for Graduate track
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Restricted strictly to identified State Universities and Colleges (SUCs)
- courses: Agriculture, Agricultural Engineering and Mechanics, Chemical Engineering, Sugar Technology, and related ladderized programs specified under Sec. 6(b) of RA 10659
- sectoral/hidden: Must be certified by the Sugar Regulatory Administration (SRA) as legitimate children or dependents of sugarcane industry workers or small sugarcane farmers
- work_experience: None
- good_moral: Required (Certificate of Good Moral Character)
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Applicants must submit complete documents to their local SRA Mill District office to secure SRA certification prior to CHEDRO ranking

### Timing
- who: Graduating SHS students, ongoing college students with earned units, and graduate applicants admitted to SUCs
- freshmen/soph/junior/senior/grad/reapply: : Yes | : Yes | : Yes | : Yes | : Yes (for Master's/Doctoral programs) | : Yes
- window: Set annually per CHEDRO and SRA advisory → Announced per academic cycle (Annual; AY AY 2025–2026 / AY 2026–2027)

### Renewal
- maintain_gwa: Maintain passing GWA per semester as prescribed by SUC retention policies
- regular_load: Full-time credit load in approved priority degree program
- no_failures: Maintain regular academic standing without failing grades
- return_service: Mandatory 1 year of return service in the Philippines for every 1 year of scholarship availed, completed within 2 years after graduation (prioritizing government agencies directly working with the sugarcane industry, other government offices, or related private entities)

### Disqualifiers / affiliations
- Absence of official Sugar Regulatory Administration (SRA) certification
- Combined gross family income exceeding ₱400,000.00 (undergraduate) or ₱500,000.00 (graduate)
- Enrollment in non-priority programs or private (non-SUC) institutions
- Academic failure or dismissal from the SUC

### Benefits (catalog)
- tuition: SUC tuition is free under RA 10931 for undergraduates; Graduate track provides up to ₱60,000.00 per AY (₱30,000.00 per semester) for TOSF
- stipend: ₱10,000.00 per month (₱100,000.00 per 10-month AY) for both Undergraduate and Graduate tracks
- allowance: Integrated into monthly stipend

### Documents (operational hidden reqs)
- Official SRA Certification confirming applicant as child/dependent of a sugarcane worker or small sugarcane farmer
- Certificate of Good Moral Character
- Notice of Admission / Certificate of Registration from participating SUC
- Academic Record: Form 138 / SF9 (for SHS), Certified True Copy of Grades for latest semester (for college), or TOR & Diploma (for graduate applicants)
- Proof of Income: Latest Income Tax Return (ITR) or BIR Certificate of Tax Exemption (Income \le ₱400,000 for undergrad; \le ₱500,000 for grad)

### Recommended schema
`json
{
  "education_level": [
    "College",
    "Graduate"
  ],
  "eligible_year_levels": [
    1,
    2,
    3,
    4
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": true,
  "minimum_gwa": null,
  "income_limit": 400000,
  "sectoral_restriction": "SRA_CERTIFIED_SUGARCANE_WORKER_DEPENDENT",
  "priority_courses": [
    "AGRICULTURE",
    "AGRICULTURAL_ENGINEERING",
    "CHEMICAL_ENGINEERING",
    "SUGAR_TECHNOLOGY"
  ],
  "school_type": [
    "SUC"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "annual_notice",
    "close": "annual_notice"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "return_service_required": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Missing Sectoral Restriction Risk: The live database lacks an explicit tag for SRA
- verification: Verified | confidence: 98/100

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Selection ranked 70% Academic + 30% Income; passing GWA required for retention)) vs renewal (Maintain passing GWA per semester as prescribed by SUC retention policies)

---

## CHED Scholarship Program for Future Statisticians (Estatistikolar) (ID: 119)

### Hard eligibility
- citizenship: Filipino citizen
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE
- education_level: Undergraduate / College
- eligible_year_levels: 1st, 2nd, 3rd, and 4th Year - Incoming Freshman Only?: No
- incoming_freshman_only: No
- existing_college: Yes
- graduate_students: No
- current_enrollment: Enrolled or accepted in BS Statistics, BS Applied Statistics, or PSA-identified statistics programs in private HEIs with Government Recognition (GR) or SUCs/LUCs with COPC/IR
- academic: SHS GWA of at least 85.00% or equivalent for incoming freshmen; minimum college GWA of 80.00% or equivalent for 2nd to 4th-year college students
- minimum_gwa: 85.00% (Incoming Freshmen / Grade 12); 80.00% (Ongoing 2nd–4th Year College Students)
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined annual gross income of parents or legal guardians must not exceed ₱500,000.00
- age: NOT SPECIFIED IN OFFICIAL SOURCE ("covers college Filipino students regardless of age...")
- school/consortium: Private HEIs with Government Recognition (GR), State Universities and Colleges (SUCs), or Local Universities and Colleges (LUCs) with IR/COPC
- courses: Bachelor of Science in Statistics, Bachelor of Science in Applied Statistics, or programs specifically identified by the Philippine Statistics Authority (PSA)
- sectoral/hidden: Special equity groups (PWDs under RA 7279, Magna Carta for Poor under RA 11291, NCIP IPs, DHSUD Underprivileged/Homeless, First-Generation students) receive +5 bonus points in ranking
- work_experience: None
- good_moral: NOT SPECIFIED IN OFFICIAL SOURCE
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Ranking criteria: 70% Academic Performance + 30% Annual Gross Income (+5 equity bonus points). Must execute a notarized scholarship contract (Annex B-2).

### Timing
- who: SHS graduating students, incoming 1st-year college students, and ongoing 2nd, 3rd, and 4th-year college students enrolled in BS Statistics/Applied Statistics
- freshmen/soph/junior/senior/grad/reapply: : Yes | : Yes | : Yes | : Yes | : No | : Yes
- window: June 22, 2026 (for AY 2026–2027 intake) / June 15 for prior cycles → July 31, 2026 (for AY 2026–2027 intake) / August 15 for prior cycles (Annual; AY AY 2026–2027 (77 national slots authorized under CEB Res. 374-2026) ### 6. Benefits)

### Renewal
- maintain_gwa: Maintain a minimum General Weighted Average (GWA) of at least 80.00% or equivalent each semester - Regular Load: Carry regular academic load per term based on curriculum
- regular_load: Carry regular academic load per term based on curriculum
- no_failures: Maintain regular academic standing per CHEDRO monitoring
- return_service: Maintain minimum GWA of 80% during study; complete degree within prescribed period; no explicit mandatory post-grad public service years specified in CMO 14 s. 2025 contract, but scholar must adhere to contract terms

### Disqualifiers / affiliations
- Enrollment in non-statistics degree programs
- Combined parent gross annual income exceeding ₱500,000.00
- Freshmen SHS GWA below 85.00% or ongoing college GWA below 80.00%
- Unauthorized shifting, school transfer, or unexcused Leave of Absence

### Benefits (catalog)
- tuition: SUCs/LUCs: Covered under Free Higher Education (RA 10931); Private HEIs: Up to ₱40,000.00 per AY (₱20,000.00 per semester) TOSF coverage
- stipend: ₱7,000.00 per month (₱35,000.00 per semester = ₱70,000.00 per 10-month AY)
- allowance: Integrated into monthly stipend

### Documents (operational hidden reqs)
- Fully accomplished online Estatistikolar Application Form (Annex A)
- Proof of Citizenship: Birth Certificate issued by NSO/PSA
- Academic Record: Form 138/SF9 (GWA \ge 85% for freshmen) or Certified True Copy of Grades for latest semester (GWA \ge 80% for 2nd–4th year)
- Proof of Income: Latest Income Tax Return (ITR) of parents/guardian, BIR Certificate of Tax Exemption/Non-Filer, OFW Contract/Proof of Income, or Social Case Study Report (Income \le ₱500,000)
- Special Equity Proof (if applicable): DHSUD/MSWDO Indigent Certificate, NCIP IP Certificate, PWD ID, or Social Case Study for First-Gen/Magna Carta for Poor

### Recommended schema
`json
{
  "education_level": [
    "College"
  ],
  "eligible_year_levels": [
    1,
    2,
    3,
    4
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": true,
  "minimum_gwa": 85.0,
  "renewal_gwa": 80.0,
  "income_limit": 500000,
  "priority_courses": [
    "BSSTATISTICS",
    "BSAPPLIEDSTATISTICS"
  ],
  "degree_program_restricted": [
    "Bachelor of Science in Statistics",
    "Bachelor of Science in Applied Statistics"
  ],
  "school_type": [
    "SUC",
    "LUC",
    "Private HEI with Government Recognition"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "06-22",
    "close": "07-31"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "return_service_required": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Missing Degree Constraint Risk: Recommending Estatistikolar to general science or
- verification: Verified | confidence: 98/100

- CONTRADICTION/NOTE: entry GWA (85.00% (Incoming Freshmen / Grade 12); 80.00% (Ongoing 2nd–4th Year College Students)) vs renewal (Maintain a minimum General Weighted Average (GWA) of at least 80.00% or equivalent each semester - Regular Load: Carry regular academic load per term based on curriculum)

---

## Scholarships for Staff and Instructors' Knowledge Advancement Program (SIKAP) (ID: 120)

### Hard eligibility
- citizenship: Filipino citizen
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE
- education_level: Graduate (Master's and Doctorate degree levels)
- eligible_year_levels: Incoming and ongoing Master's and Doctoral graduate students
- incoming_freshman_only: No
- existing_college: Ineligible (Restricted to post-baccalaureate graduate students)
- graduate_students: Yes (Primary target cohort)
- current_enrollment: Must be admitted or enrolled in a Master's or Doctoral program at a CHED-recognized Delivering Higher Education Institution (DHEI)
- academic: Bachelor's degree (for Master's track) or Master's degree (for Doctorate track); official endorsement from sending HEI
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Governed by DHEI graduate admission and retention standards)
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE (Income uncapped; targeted at employed HEI personnel)
- age: NOT SPECIFIED IN OFFICIAL SOURCE (Subject to sending HEI retirement policies)
- school/consortium: Restricted strictly to CHED-recognized Delivering Higher Education Institutions (DHEIs) offering authorized graduate programs
- courses: Graduate degree programs in priority disciplines identified by CHED (e.g., STEAM, Teacher Education, Social Sciences, Health Sciences)
- sectoral/hidden: Must be an active full-time or part-time faculty member or non-teaching personnel of a recognized Philippine HEI (sending HEI)
- work_experience: None
- good_moral: Required (Endorsement by sending HEI President/Head)
- health: Physically and mentally fit for graduate study
- other_rules/conflicts: Requires a tripartite scholarship contract between CHED, Scholar, Sending HEI, and DHEI. Full-time contractual or Contract of Service faculty are eligible under Package B.

### Timing
- who: Active HEI faculty and non-teaching personnel pursuing Master's or Doctoral degrees
- freshmen/soph/junior/senior/grad/reapply: : Ineligible (Undergraduate freshmen cannot apply) | : Ineligible | : Ineligible | : Ineligible | : Yes (Bachelor's or Master's degree holders entering/enrolled in | : Yes
- window: Set annually per CHED call for applications → Announced per submission cycle (Annual / Semestral intake; AY AY 2025–2026 / AY 2026–2027)

### Renewal
- maintain_gwa: Maintain required passing GWA per DHEI graduate retention rules
- regular_load: Full-time or approved part-time credit load per approved curriculum plan
- no_failures: Zero failing or incomplete grades in graduate coursework
- return_service: Mandatory return service rendered to the sending HEI (1 to 2 years of service for every 1 year of scholarship availed)

### Disqualifiers / affiliations
- Non-employment as HEI faculty or non-teaching personnel
- Enrollment in non-DHEI or non-approved graduate programs
- Academic failure, unexcused dropping, or expulsion from the DHEI
- Failure to secure official endorsement from the sending HEI

### Benefits (catalog)
- tuition: 100% coverage of Actual Tuition and Other School Fees (TOSF) paid directly to the DHEI
- stipend: Living allowance based on study track (Full-Time vs Part-Time Package A/B): Master's up to ₱25,000.00–₱30,000.00/month; Doctorate up to ₱35,000.00–₱40,000.00/month
- allowance: Learning materials, connectivity, and book allowance provided per term

### Documents (operational hidden reqs)
- SIKAP Application Form and Plantilla / Employment Verification from Sending HEI
- Official Nomination and Endorsement Letter from Sending HEI President/Head
- Proof of Admission / Registration in a CHED-recognized DHEI
- Certified True Copy of Transcript of Records (TOR) for previous degrees
- Curriculum Vitae (CV) and Research Concept Paper / Dissertation Work Plan
- Certificate of Good Moral Character / Clearance from sending institution

### Recommended schema
`json
{
  "education_level": [
    "Graduate"
  ],
  "eligible_year_levels": [
    1,
    2,
    3
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": true,
  "minimum_gwa": null,
  "income_limit": null,
  "sectoral_restriction": "HEI_FACULTY_OR_NON_TEACHING_STAFF",
  "priority_courses": [
    "CHED_APPROVED_GRADUATE_PROGRAMS"
  ],
  "school_type": [
    "DHEI"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "annual_call",
    "close": "annual_call"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "return_service_required": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Target User Misclassification Risk: In the production database, ID 120 lists levels:
- verification: Verified | confidence: 98/100

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Governed by DHEI graduate admission and retention standards)) vs renewal (Maintain required passing GWA per DHEI graduate retention rules)

---
