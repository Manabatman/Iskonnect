# DATABASE_V3_GROUPC_OTHER_GOVERNMENT.pdf — Implementation Details

Scholarships: 15

## Senior High School Voucher Program (SHS VP)3 (ID: 17)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen5.
- residency/destination: Resident of the Philippines5.
- education_level: Senior High School (Grades 11 and 12)4.
- eligible_year_levels: Grade 11 (Initial redemption occurs upon entry into Grade 11)4.
- incoming_freshman_only: Yes (Applicable to incoming Grade 11 SHS students)4.
- existing_college: Ineligible4.
- graduate_students: Ineligible4.
- current_enrollment: Must be enrolled or accepted in a non-DepEd VP-participating Senior High School3.
- academic: Successful completion of Grade 10 Junior High School (JHS)4.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Passing Grade 10 completion is required)4.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE5.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE (Grade 10 completers from public JHSs and private JHS Educational Service Contracting [ESC] grantees are automatically qualified regardless of income; non-ESC private applicants undergo online screening subject to national budget allocations)5.
- age: NOT SPECIFIED IN OFFICIAL SOURCE5.
- school/consortium: Restricted to VP-participating non-DepEd Senior High Schools (Private SHSs, SUCs, and LUCs)3.
- courses: All DepEd-approved SHS Tracks and Strands (Academic, Technical-Vocational-Livelihood [TVL], Sports, Arts and Design)4.
- sectoral/hidden: None5.
- work_experience: None
- good_moral: Certificate of Good Moral Character issued by the originating Junior High School4.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Automatically Qualified Voucher Recipients (QVRs) include Grade 10 completers from Public JHSs, SUC/LUC JHSs, and ESC grantees in Private JHSs5. Non-ESC private JHS completers must apply online via the Online Voucher Application Portal (OVAP)5. Vouchers are non-cashable grants disbursed directly to participating host schools via Land Bank of the Philippines accounts4.

### Timing
- who: Non-ESC Grade 10 completers from private junior high schools, and learners who completed JHS prior to the current school year re-entering basic education5.
- freshmen/soph/junior/senior/grad/reapply: : Yes (Incoming Grade 11 SHS students)4. | : No (Grade 12 voucher renewal is automatic for Grade | : No4. | : No4. | : No4. | : No4.
- window: Announced annually via DepEd Order (typically opens between October and January)5. → Specified in the annual policy guidelines (typically February 28 for online submissions)5. (Fixed / Annual5.; AY AY 2025–2026 / AY 2026–20275.)

### Renewal
- maintain_gwa: Promoted to Grade 12 in accordance with DepEd academic progression standards4.
- regular_load: Continuous full-time enrollment in the elected SHS track4.
- no_failures: Passing grades across all enrolled SHS subjects4.
- return_service: None4.

### Disqualifiers / affiliations
- Dropping out of Senior High School in the middle of an academic year4.
- Transferring to a DepEd Public Senior High School4.
- Failing Grade 11 or retaining Grade 11 academic status4.
- Transferring to a non-participating private Senior High School3.

### Benefits (catalog)
- tuition: Voucher subsidy disbursed directly to host school (NCR Private SHS: up to ₱22,500/year; NCR SUC/LUC SHS: ₱17,500/year; Non-NCR Private SHS: up to ₱17,500/year; Non-NCR SUC/LUC SHS: ₱14,000/year)4.
- stipend: None (Direct tuition voucher)5.
- allowance: None9.

### Documents (operational hidden reqs)
- PSA Certified Birth Certificate4.
- Grade 10 Report Card (Form 138 / SF9) showing Learner Reference Number (LRN)4.
- Certificate of Junior High School Completion4.
- Certificate of Good Moral Character signed by JHS Principal4.
- ESC Certification Letter issued by JHS Principal via ESC IMS (for ESC grantees) or Qualified Voucher Applicant (QVA) Certificate (for online applicants)4.

### Recommended schema
`json
{
  "education_level": [
    "Senior High School"
  ],
  "eligible_year_levels": [
    11
  ],
  "incoming_year_only": true,
  "requires_current_enrollment": true,
  "minimum_gwa": null,
  "income_limit": null,
  "school_type": [
    "Private SHS",
    "SUCSHS",
    "LUCSHS"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "10-01",
    "close": "02-28"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Income Parameter Misconfiguration: The live database export records max_income:
- verification: Verified3. | confidence: None

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Passing Grade 10 completion is required)4.) vs renewal (Promoted to Grade 12 in accordance with DepEd academic progression standards4.)

---

## Energy Regulatory Commission Graduate Fellowship Program9 (ID: 20)

### Hard eligibility
- citizenship: Natural-born Filipino citizen9.
- residency/destination: Resident of the Philippines9.
- education_level: Graduate (Master's or Doctorate)9.
- eligible_year_levels: 1st Year Master's or Doctoral students9.
- incoming_freshman_only: No9.
- existing_college: Ineligible (Restricted to post-baccalaureate graduate students)9.
- graduate_students: Yes9.
- current_enrollment: Accepted or enrolled in a graduate degree program in energy regulation, power engineering, or energy economics at an accredited university9.
- academic: Undergraduate General Weighted Average (GWA) of at least 88.00% or equivalent9.
- minimum_gwa: 88.00%9.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE9.
- income_ceilings: Combined gross annual family income must not exceed ₱500,000.009.
- age: NOT SPECIFIED IN OFFICIAL SOURCE9.
- school/consortium: CHED-accredited universities offering recognized graduate programs in law, economics, or engineering9.
- courses: Energy Law, Energy Economics, Power Engineering, Public Policy9.
- sectoral/hidden: None9.
- work_experience: None
- good_moral: Required9.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Must pass the ERC interview and selection board evaluation9.

### Timing
- who: Qualified Bachelor's degree graduates entering or pursuing graduate studies in priority energy disciplines9.
- freshmen/soph/junior/senior/grad/reapply: : No (Undergraduate freshmen barred)9. | : No9. | : No9. | : No9. | : Yes (Primary eligible cohort)9. | : Yes9.
- window: Announced annually per ERC official advisory9. → Specified in the annual Call for Candidates9. (Annual9.; AY AY 2025–2026 / AY 2026–20279.)

### Renewal
- maintain_gwa: Maintain graduate academic retention GWA specified by ERC (minimum 88.00% or university passing equivalent)9.
- regular_load: Enrolled in required graduate unit load per semester9.
- no_failures: Zero failing or incomplete marks in graduate coursework9.
- return_service: NOT SPECIFIED IN OFFICIAL SOURCE9.

### Disqualifiers / affiliations
- Undergraduate enrollment status9.
- Combined family gross annual income exceeding ₱500,000.009.
- Undergraduate GWA dropping below 88.00%9.
- Employment in conflicting energy sector enterprises violating regulatory ethics rules9.

### Benefits (catalog)
- tuition: Full tuition and matriculation fee coverage9.
- stipend: ₱12,000.00 per month9.
- allowance: Integrated into monthly stipend9.

### Documents (operational hidden reqs)
- Official Graduate Fellowship Application Form9.
- Official Transcript of Records (TOR) from Bachelor's degree showing GWA >= 88.00%9.
- Proof of Admission / Enrollment in an approved graduate program9.
- BIR Income Tax Return or Tax Exemption Certificate (Income <= ₱500,000.00)9.
- Certificate of Good Moral Character9.

### Recommended schema
`json
{
  "education_level": [
    "Graduate"
  ],
  "eligible_year_levels": [
    1,
    2
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": true,
  "minimum_gwa": 88.0,
  "income_limit": 500000,
  "school_type": [
    "CHED_RECOGNIZED_HEI"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "application_window": {
    "open": "annual_notice",
    "close": "annual_notice"
  },
  "deadline_type": "estimated",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Academic Level Misclassification: Displaying ID 20 to college undergraduate candidates
- verification: Partially Verified9. | confidence: 95/100.

- CONTRADICTION/NOTE: entry GWA (88.00%9.) vs renewal (Maintain graduate academic retention GWA specified by ERC (minimum 88.00% or university passing equivalent)9.)

---

## NCIP Educational Assistance Program (EAP) – Degree Track10 (ID: 52)

### Hard eligibility
- citizenship: Filipino citizen10.
- residency/destination: Resident member of a recognized Indigenous Cultural Community / Ancestral Domain10.
- education_level: College / Undergraduate9.
- eligible_year_levels: 1st, 2nd, 3rd, 4th, and 5th Year14.
- incoming_freshman_only: No14.
- existing_college: Yes14.
- graduate_students: Ineligible under the Degree Track (Covered under separate post-graduate assistance provisions)14.
- current_enrollment: Enrolled or accepted in a State College or University (SUC) or CHED-recognized HEI14.
- academic: Must maintain a General Weighted Average (GWA) of at least 80.00% per semester14.
- minimum_gwa: 80.00%14.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE10.
- income_ceilings: Combined family annual gross income must not exceed ₱200,000.009.
- age: NOT SPECIFIED IN OFFICIAL SOURCE10.
- school/consortium: State Universities and Colleges (SUCs) nearest to the applicant's ancestral domain residence are prioritized14.
- courses: Degree programs aligned with Ancestral Domain Sustainable Development and Protection Plans (ADSDPP)14.
- sectoral/hidden: Must submit an official Certificate of Confirmation (COC) issued by NCIP attesting to genuine IP tribal membership10.
- work_experience: None
- good_moral: Required10.
- health: Physically and mentally fit to pursue higher education14.
- other_rules/conflicts: Enrolled in a minimum load of 18 units per semester unless in graduating status14. Dual enjoyment of major government scholarship grants is prohibited14.

### Timing
- who: Qualified IP college students (incoming freshmen and ongoing upperclassmen)10.
- freshmen/soph/junior/senior/grad/reapply: : Yes14. | : Yes14. | : Yes14. | : Yes14. | : No14. | : Yes14.
- window: June 1 annually (via EAIS portal)9. → August 15 annually9. (Fixed / Annual9.; AY AY 2025–2026 / AY 2026–20279.)

### Renewal
- maintain_gwa: Maintain a semester GWA of at least 80.00%14.
- regular_load: Minimum enrollment of 18 units per semester14.
- no_failures: Zero failing, incomplete, or dropped subjects14.
- return_service: Mandatory service in the scholar's home IP community for a duration equal to the scholarship years enjoyed, or book donation to a community library14.

### Disqualifiers / affiliations
- Falsification or tampering of NCIP COC or academic records14.
- Semester GWA dropping below 80.00%14.
- Concurrent enjoyment of another major national government scholarship14.
- Unapproved shiftee or transferee status14.
- Dropping below 18 units without prior NCIP approval14.

### Benefits (catalog)
- tuition: Covered via SUC Free Higher Education or subsidized through the IP Education Allowance14.
- stipend: Integrated into the annual educational allowance14.
- allowance: ₱20,000.00 per Academic Year (disbursed semestrally at ₱10,000.00 per semester)14.

### Documents (operational hidden reqs)
- Official Certificate of Confirmation (COC) on Tribe Membership issued by NCIP10.
- Accomplished EAIS Online Application Form10.
- Form 138 / SF9 Report Card (for Freshmen) or Official Transcript of Records / Certificate of Grades (for Upperclassmen) showing GWA >= 80.00%10.
- Certificate of Enrollment / Registration Form showing at least 18 enrolled units14.
- BIR Tax Exemption Certificate, ITR, or Barangay Certificate of Indigency11.
- Certificate of Good Moral Character10.

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
  "minimum_gwa": 80.0,
  "income_limit": 200000,
  "sectoral_restriction": "NCIP_CERTIFIED_INDIGENOUS_PEOPLE",
  "school_type": [
    "SUC",
    "LUC",
    "PRIVATE_HEI"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "application_window": {
    "open": "06-01",
    "close": "08-15"
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
- ● Database GWA Discrepancy: The live database export records min_gwa: 75 for ID 529.
- verification: Verified10. | confidence: 75/1009.

- CONTRADICTION/NOTE: entry GWA (80.00%14.) vs renewal (Maintain a semester GWA of at least 80.00%14.)

---

## NCIP Merit-Based Scholarship Program (MBSP)10 (ID: 53)

### Hard eligibility
- citizenship: Filipino citizen10.
- residency/destination: Resident member of an Indigenous Cultural Community10.
- education_level: College / Undergraduate9.
- eligible_year_levels: 1st, 2nd, 3rd, 4th, and 5th Year14.
- incoming_freshman_only: No14.
- existing_college: Yes14.
- graduate_students: Ineligible under MBSP undergraduate track14.
- current_enrollment: Enrolled or accepted in an SUC or recognized HEI14.
- academic: General Weighted Average (GWA) of at least 85.00% per semester14.
- minimum_gwa: 85.00%14.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE10.
- income_ceilings: Combined family gross annual income must not exceed ₱300,000.009.
- age: NOT SPECIFIED IN OFFICIAL SOURCE10.
- school/consortium: SUCs or top accredited private HEIs14.
- courses: ADSDPP community priority courses and CHED priority fields14.
- sectoral/hidden: Must hold an official NCIP Certificate of Confirmation (COC)10.
- work_experience: None
- good_moral: Required10.
- health: Physically and mentally fit14.
- other_rules/conflicts: Enrolled in full semester load (at least 18 units)14.

### Timing
- who: Academically qualified IP college students10.
- freshmen/soph/junior/senior/grad/reapply: : Yes14. | : Yes14. | : Yes14. | : Yes14. | : No14. | : Yes14.
- window: June 1 annually9. → August 15 annually9. (Annual9.; AY AY 2025–2026 / AY 2026–20279.)

### Renewal
- maintain_gwa: Must maintain a semester GWA of at least 85.00%14.
- regular_load: Enrolled in at least 18 units per semester14.
- no_failures: Zero failing or incomplete grades14.
- return_service: Mandatory service in the scholar's home IP community equal to award duration14.

### Disqualifiers / affiliations
- GWA falling below 85.00%14.
- Dual enjoyment of another major national government scholarship14.
- Falsification of IP certification documents14.
- Unapproved transfer of school or course14.

### Benefits (catalog)
- tuition: Full tuition and matriculation fees covered14.
- stipend: Integrated into the annual merit grant package14.
- allowance: ₱50,000.00 per Academic Year (disbursed semestrally at ₱25,000.00 per semester)14.

### Documents (operational hidden reqs)
- Official NCIP Certificate of Confirmation (COC)10.
- Accomplished EAIS Online Application Form10.
- Form 138 / TOR showing GWA >= 85.00% with zero failing grades10.
- Certificate of Enrollment showing at least 18 enrolled units14.
- BIR Income Tax Return or Tax Exemption Certificate (Income <= ₱300,000.00)9.
- Certificate of Good Moral Character10.

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
  "minimum_gwa": 85.0,
  "income_limit": 300000,
  "sectoral_restriction": "NCIP_CERTIFIED_INDIGENOUS_PEOPLE",
  "school_type": [
    "SUC",
    "LUC",
    "PRIVATE_HEI"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "application_window": {
    "open": "06-01",
    "close": "08-15"
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
- ● Benefit Value Misalignment: The live database export records total_value: 30000 for ID
- verification: Verified10. | confidence: 94/100.

- CONTRADICTION/NOTE: entry GWA (85.00%14.) vs renewal (Must maintain a semester GWA of at least 85.00%14.)

---

## Agricultural Competitiveness Enhancement Fund – Grants-in-Aid Higher Education Program (ACEF-GIAHEP) SUC Track16 (ID: 55)

### Hard eligibility
- citizenship: Filipino citizen16.
- residency/destination: Resident of the Philippines16.
- education_level: College / Undergraduate9.
- eligible_year_levels: Freshmen and ongoing undergraduate students (Years 1 to 4/5)16.
- incoming_freshman_only: No16.
- existing_college: Yes16.
- graduate_students: Ineligible16.
- current_enrollment: Enrolled in an eligible agriculture-related degree program at a participating SUC16.
- academic: Minimum GWA of 75.00% or passing academic grade9.
- minimum_gwa: 75.00%9.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: Combined gross annual income of parents must not exceed ₱200,000.009.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to State Universities and Colleges (SUCs)16.
- courses: Agriculture, Agricultural Engineering, Agribusiness, Forestry, Fisheries, Veterinary Medicine16.
- sectoral/hidden: Parent must be a registered small farmer or fisherfolk listed in the Registry System for Basic Sectors in Agriculture (RSBSA) or certified by DA/LGU16.
- work_experience: None
- good_moral: Required.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Cannot enjoy another government scholarship covering the same expenditure items16.

### Timing
- who: Children of RSBSA-registered small farmers and fisherfolk entering or enrolled in SUC agriculture programs16.
- freshmen/soph/junior/senior/grad/reapply: : Yes16. | : Yes16. | : Yes16. | : Yes16. | : No16. | : Yes16.
- window: Announced per academic cycle16. → August 15 annually9. (Annual9.; AY AY 2025–2026 / AY 2026–20279.)

### Renewal
- maintain_gwa: Maintain passing academic GWA per semester (75.00% or SUC retention passing mark)9.
- regular_load: Full credit load per term16.
- no_failures: Compliance with SUC retention rules16.
- return_service: None9.

### Disqualifiers / affiliations
- Parent not registered in RSBSA or non-farming status16.
- Combined family annual income exceeding ₱200,000.009.
- Enrollment in non-agriculture degrees or private HEIs16.
- Academic failure or dismissal from SUC16.

### Benefits (catalog)
- tuition: Covered by SUC Free Higher Education or subsidized16.
- stipend: Integrated into semestral grant9.
- allowance: ₱30,000.00 per Academic Year (₱15,000.00 per semester)9.

### Documents (operational hidden reqs)
- Proof of RSBSA Registration or DA/LGU Agriculture Office Certification of parent16.
- PSA Birth Certificate of applicant16.
- Form 138 / SF9 Report Card or TOR showing passing GWA >= 75.00%9.
- BIR Tax Exemption Certificate or ITR showing family income <= ₱200,000.009.
- Certificate of Enrollment in an approved SUC agriculture degree program16.
- Certificate of Good Moral Character.

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
  "income_limit": 200000,
  "sectoral_restriction": "RSBSA_REGISTERED_FARMER_FISHERFOLK_DEPENDENT",
  "priority_courses": [
    "AGRICULTURE",
    "AGRICULTURAL_ENGINEERING",
    "FORESTRY",
    "FISHERIES",
    "VETERINARY_MEDICINE"
  ],
  "school_type": [
    "SUC"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "06-01",
    "close": "08-15"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Missing RSBSA Sectoral Filter: System must check user.is_rsbsa_dependent == true.
- verification: Verified16. | confidence: 94/100.

- CONTRADICTION/NOTE: entry GWA (75.00%9.) vs renewal (Maintain passing academic GWA per semester (75.00% or SUC retention passing mark)9.)

---

## DND-CHED-PASUC Scholarship Program17 (ID: 56)

### Hard eligibility
- citizenship: Natural-born Filipino citizen17.
- residency/destination: Resident of the Philippines17.
- education_level: College / Undergraduate (Baccalaureate degrees only; post-graduate excluded)17.
- eligible_year_levels: 1st, 2nd, 3rd, 4th, and 5th Year17.
- incoming_freshman_only: No17.
- existing_college: Yes17.
- graduate_students: Ineligible17.
- current_enrollment: Admitted or enrolled in a State University or College (SUC)17.
- academic: Minimum GWA of 80.00% or compliance with host SUC admission standards9.
- minimum_gwa: 80.00%9.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE (Selection prioritized by military operational causality status: KIA/CDD-CR first, active personnel second)17.
- age: Dependent child must be below 21 years of age at the beginning of the school year17.
- school/consortium: Restricted strictly to State Universities and Colleges (SUCs)17.
- courses: Any baccalaureate degree course offered by SUCs17.
- sectoral/hidden: Must be a legitimate child of active, KIA, or CDD-CR AFP military personnel17.
- work_experience: None
- good_moral: Required17.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: National quota of 200 scholarship slots17. Candidates must satisfy SUC admission standards on or before April 1017. Must sign AFPEBSO Certificate of Undertaking17. Unapproved transfer between SUCs or leaves of absence strictly prohibited17.

### Timing
- who: Dependents of KIA, CDD-CR, or active military personnel under 21 years old17.
- freshmen/soph/junior/senior/grad/reapply: : Yes17. | : Yes17. | : Yes17. | : Yes17. | : No17. | : Yes17.
- window: Annual application processing opens early in the calendar year17. → April 20 annually for document processing; Central Scholarship Board confirmation before May 1517. (Annual17.; AY AY 2025–2026 / AY 2026–20279.)

### Renewal
- maintain_gwa: Maintain passing GWA per SUC academic retention rules (minimum 80.00%)9.
- regular_load: Enrolled in full-time baccalaureate curriculum load17.
- no_failures: Zero failing marks17.
- return_service: None9.

### Disqualifiers / affiliations
- Dependent age reaching or exceeding 21 years old at the start of the SY17.
- Unapproved transfer to another HEI or taking leave of absence without CSB approval17.
- Academic failure or dismissal from host SUC17.
- Enrollment in private universities or post-graduate degree programs17.

### Benefits (catalog)
- tuition: 100% Tuition fee waiver covered by the host State University or College (SUC) for the entire course duration17.
- stipend: Integrated into AFPEBSO annual stipend17.
- allowance: AFPEBSO provides direct scholar stipend of ₱8,000.00 annually (₱4,000.00 per semester)17.

### Documents (operational hidden reqs)
- Duly accomplished AFPEBSO Application Form with two 2x2 photos17.
- Letter of Recommendation from DND-CHED-PASUC Central Scholarship Board17.
- Military Service Record of parent / Casualty Report (KIA or CDD-CR Order) issued by OTAG AFP17.
- PSA Marriage Certificate of parents and PSA Birth Certificate of applicant17.
- Transcript of Records / Report Card showing GWA >= 80.00%9.
- Certificate of Good Moral Character17.
- Signed AFPEBSO Certificate of Undertaking17.

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
  "minimum_gwa": 80.0,
  "age_limit": 20,
  "parent_employment_restriction": "AFP_MILITARY_PERSONNEL_KIA_CDDCR_ACTIVE",
  "school_type": [
    "SUC"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "01-15",
    "close": "04-20"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Age Limit Omission: System must enforce user.age < 21 at the start of the academic
- verification: Verified17. | confidence: 92/100.

- CONTRADICTION/NOTE: entry GWA (80.00%9.) vs renewal (Maintain passing GWA per SUC academic retention rules (minimum 80.00%)9.)

---

## DSWD Assistance to Individuals in Crisis Situations (AICS) Educational Assistance19 (ID: 57)

### Hard eligibility
- citizenship: Filipino citizen19.
- residency/destination: Resident of the Philippines (verified via Barangay Certificate of Indigency / Residency)19.
- education_level: Grade 11, Grade 12, College / TVET, Graduate9.
- eligible_year_levels: All year levels across secondary, tertiary, and vocational tracks9.
- incoming_freshman_only: No9.
- existing_college: Yes9.
- graduate_students: Eligible if in verified crisis9.
- current_enrollment: Enrolled in a recognized educational institution19.
- academic: Active student status19.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (No academic grade cutoff imposed; crisis evaluation prioritized)9.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: Combined family income within low-income / poverty threshold levels (₱150,000.00 cap in live DB export)9.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: None (Public or Private recognized institutions)19.
- courses: Any course or field of study19.
- sectoral/hidden: Target crisis categories: Breadwinner deceased, incapacitated, unemployed, or displaced; child of solo parent; child of OFW in distress; 4Ps beneficiary19.
- work_experience: None
- good_moral: NOT SPECIFIED IN OFFICIAL SOURCE.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Evaluated via DSWD Social Worker Case Assessment19. Grant provided as a one-time emergency assistance per academic year / crisis event19.

### Timing
- who: Students in crisis or financially distressed breadwinners19.
- freshmen/soph/junior/senior/grad/reapply: : Yes9. | : Yes9. | : Yes9. | : Yes9. | : Yes9. | : Yes (Subject to DSWD crisis re-evaluation guidelines)19.
- window: Year-round / Rolling intake9. → December 31 annually (or subject to annual budget allocation)9. (Rolling / Emergency assistance9.; AY AY 2025–2026 / AY 2026–20279.)

### Renewal
- maintain_gwa: None (One-time assistance per crisis evaluation)19.
- regular_load: Active enrollment19.
- no_failures: None
- return_service: None9.

### Disqualifiers / affiliations
- Non-indigent status or family income exceeding threshold19.
- Falsification of crisis documents or barangay indigency certificates19.
- Failure to pass DSWD social work case interview19.

### Benefits (catalog)
- tuition: None (Direct cash financial assistance paid to client)19.
- stipend: None19.
- allowance: Outright cash assistance grant up to ₱4,000.00 max depending on level (College/Vocational/Graduate: up to ₱4,000.00; SHS: up to ₱3,000.00; JHS: up to ₱2,000.00; Elementary: up to ₱1,000.00)9.

### Documents (operational hidden reqs)
- Certificate of Enrollment / Registration Form or School ID19.
- Barangay Certificate of Indigency / Residency19.
- Valid Government ID of applicant or parent/guardian19.
- DSWD Social Worker Intake and Assessment Sheet19.
- Specific Crisis Proof (Death Certificate of breadwinner, Medical Certificate, Notice of Termination, OFW Distress Report)19.

### Recommended schema
`json
{
  "education_level": [
    "Senior High School",
    "College",
    "TVET",
    "Graduate"
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
  "minimum_gwa": null,
  "income_limit": 150000,
  "is_emergency_grant": true,
  "school_type": [
    "RECOGNIZED_EDUCATIONAL_INSTITUTION"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "application_window": {
    "open": "01-01",
    "close": "12-31"
  },
  "deadline_type": "rolling",
  "cycle_type": "rolling",
  "renewable": false,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Program Type Misclassification: ID 57 is an emergency cash assistance grant, NOT a
- verification: Verified19. | confidence: 96/100.

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (No academic grade cutoff imposed; crisis evaluation prioritized)9.) vs renewal (None (One-time assistance per crisis evaluation)19.)

---

## Bagong Pilipinas Merit Scholarship Program (BPMSP) – Technical Education and Skills Development Authority (TVET) Diploma Track20 (ID: 77)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen24.
- residency/destination: Resident of the Philippines24.
- education_level: Technical Education and Skills Development Authority (TVET) Diploma level9.
- eligible_year_levels: 1st Year (Incoming first-time entrants into TVET diploma programs)20.
- incoming_freshman_only: Yes20.
- existing_college: Ineligible (Must have earned zero college or tertiary units)21.
- graduate_students: Ineligible21.
- current_enrollment: Accepted or enrolled in a priority diploma program offered by a TESDA-registered Technical Vocational Institution (TVI)20.
- academic: Grade 12 Senior High School General Weighted Average (GWA) of at least 90.00% or equivalent21.
- minimum_gwa: 90.00%21.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE for TVET track (HE track uses Top 5 / 95% GWA, TVET track mandates GWA >= 90%)21.
- income_ceilings: Combined annual gross income of parents/guardians must not exceed ₱2,000,000.0020.
- age: No age limit imposed (Irrespective of age provided candidate has earned no tertiary units)21.
- school/consortium: Restricted to TESDA-registered Technical Vocational Institutions (TVIs) delivering approved priority diploma programs20.
- courses: TESDA-identified priority diploma courses in key growth sectors20.
- sectoral/hidden: Special equity groups (PWDs, Solo Parents, IPs, Senior Citizens, first-generation students) receive 10 additional ranking points in selection scoring20.
- work_experience: None
- good_moral: Required21.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Applicants must NOT previously hold a technical-vocational diploma or NC Level III or higher (unless acquired as part of the SHS curriculum)21. TESDA has sole authority and exclusive jurisdiction over the TVET Diploma Track21. Transferees or shiftees with credited tertiary units are ineligible26.

### Timing
- who: Graduating SHS Grade 12 students, prior SHS graduates with no tertiary units, and 4th year HS graduates from SY 2015–2016 or earlier with no tertiary units21.
- freshmen/soph/junior/senior/grad/reapply: : Yes (Incoming 1st year TVET diploma students)21. | : No21. | : No21. | : No21. | : No21. | : No21.
- window: Announced per annual cycle (portal opens upon JMC call)20. → June 30, 2026 (for initial cycle)20. (Fixed / Annual20.; AY AY 2026–202720.)

### Renewal
- maintain_gwa: Must pass all subjects every semester to retain grant20.
- regular_load: Full-time credit enrollment in TVET diploma curriculum21.
- no_failures: Zero failing marks allowed20.
- return_service: Mandatory 1 year of return service in the Philippines for every 1 year of scholarship received, prioritizing public and government institutions20.

### Disqualifiers / affiliations
- Earning tertiary or college units prior to award21.
- Holding an NC Level III, NC Level IV, or prior TVET diploma (unless part of SHS curriculum)21.
- Combined parental gross annual income exceeding ₱2,000,000.0020.
- Failing any subject during the TVET diploma program20.
- Transferees or shiftees with credited tertiary units26.

### Benefits (catalog)
- tuition: Tuition subsidy up to ₱70,000.00 per academic year20.
- stipend: Integrated into annual living stipend20.
- allowance: Living stipend of ₱40,000.00 per academic year20.

### Documents (operational hidden reqs)
- Accomplished Online Application Form on official BPMSP portal21.
- PSA Certified Birth Certificate21.
- Certified True Copy of Learner's Progress Report Card (Form 138 / SF9) showing SHS GWA >= 90.00%21.
- Proof of Family Income (BIR Tax Exemption Certificate, BIR Form 2316 / 1701, DSWD 4Ps / Indigency Certificate, or OFW Employment Contract <= ₱2,000,000.00)20.
- Proof of Admission / Acceptance to a TESDA-registered TVI Diploma Program (Certificate of Acceptance, Training Agreement, or Enrollment Confirmation)21.
- Signed Parent / Legal Guardian Certification (Annex L)24.

### Recommended schema
`json
{
  "education_level": [
    "TVET"
  ],
  "eligible_year_levels": [
    1
  ],
  "incoming_year_only": true,
  "requires_current_enrollment": true,
  "minimum_gwa": 90.0,
  "income_limit": 2000000,
  "school_type": [
    "TESDA_REGISTERED_TVI"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "04-01",
    "close": "06-30"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "return_service_required": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Track and Level Confusion: Database ID 77 represents the TVET Track of BPMSP, whereas
- verification: Verified20. | confidence: 90/100.

- CONTRADICTION/NOTE: entry GWA (90.00%21.) vs renewal (Must pass all subjects every semester to retain grant20.)

---

## GSIS Educational Subsidy Program (GESP)9 (ID: 84)

### Hard eligibility
- citizenship: Filipino citizen.
- residency/destination: Resident of the Philippines.
- education_level: College / Undergraduate9.
- eligible_year_levels: 1st, 2nd, 3rd, 4th, and 5th Year9.
- incoming_freshman_only: No9.
- existing_college: Yes9.
- graduate_students: Ineligible9.
- current_enrollment: Enrolled in a 4- or 5-year college degree program in a CHED-recognized HEI9.
- academic: Active student status meeting university retention standards9.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Passing grade status required)9.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: Controlled via GSIS member parent salary grade (GSIS active members in lowest Salary Grades prioritized; SG 24 and below)9.
- age: Dependent child must be below 25 years old.
- school/consortium: CHED-recognized State Universities and Colleges or Private HEIs9.
- courses: Any undergraduate degree program9.
- sectoral/hidden: Parent must be an active GSIS member with updated premium contributions9.
- work_experience: None
- good_moral: Required.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Selection based on computer-generated ranking prioritizing members with lowest salary grade and longest length of service9.

### Timing
- who: Dependents of active GSIS members9.
- freshmen/soph/junior/senior/grad/reapply: : Yes9. | : Yes9. | : Yes9. | : Yes9. | : No9. | : Yes9.
- window: Announced per annual GSIS advisory9. → Specified in annual notice9. (Annual9.; AY AY 2025–2026 / AY 2026–20279.)

### Renewal
- maintain_gwa: Passing grades in all enrolled subjects9.
- regular_load: Full credit load per semester9.
- no_failures: Zero failing marks9.
- return_service: None9.

### Disqualifiers / affiliations
- Member parent inactive or in default of GSIS premium payments9.
- Dependent age reaching 25 years old9.
- Student failing any academic subject9.
- Member parent salary grade exceeding ceiling9.

### Benefits (catalog)
- tuition: Direct cash subsidy provided to scholar9.
- stipend: None9.
- allowance: ₱10,000.00 cash subsidy per Academic Year9.

### Documents (operational hidden reqs)
- Official GESP Application Form9.
- PSA Birth Certificate of nominated child9.
- Certificate of Employment / Service Record of GSIS member showing Salary Grade9.
- Certificate of Enrollment / Registration Form from CHED-recognized college9.
- School grade report / transcript showing passing marks9.

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
  "minimum_gwa": null,
  "income_limit": null,
  "parent_employment_restriction": "GSIS_ACTIVE_MEMBER",
  "school_type": [
    "CHED_RECOGNIZED_HEI"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "application_window": {
    "open": "annual_notice",
    "close": "annual_notice"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Differentiation from Other GSIS Grants: The system must maintain explicit separation
- verification: Verified9. | confidence: 98/100.

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Passing grade status required)9.) vs renewal (Passing grades in all enrolled subjects9.)

---

## Education for Development Scholarship Program (EDSP)18 (ID: 85)

### Hard eligibility
- citizenship: Natural-born Filipino citizen27.
- residency/destination: Resident of the Philippines27.
- education_level: College / Undergraduate9.
- eligible_year_levels: Category 1 (Incoming 1st Year Freshmen); Category 2 (2nd to 5th Year College Students)18.
- incoming_freshman_only: No (Has distinct tracks for incoming freshmen and ongoing 2nd-5th year college students)18.
- existing_college: Yes (Under EDSP Category 2)28.
- graduate_students: Ineligible18.
- current_enrollment: Enrolled or accepted in a 4- or 5-year baccalaureate degree program in an accredited Philippine college or university18.
- academic: ○ Category 1 (Freshmen): SHS Grade 12 General Weighted Average (GWA) of at least 80.00% with zero failing grades; must qualify via national qualifying examination (top DOST national exam takers)27. ○ Category 2 (Upperclassmen): Cumulative college GWA of at least 85.00% or equivalent with zero failing grades28.
- minimum_gwa: 80.00% (Freshmen entry) / 85.00% (Upperclassmen entry)27.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE27.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE for EDSP main track (Restricted by active OWWA member contribution status)18.
- age: Must be single and not over 21 years old for Category 1 (Freshmen)27; single and not over 30 years old for Category 2 (Upperclassmen)28.
- school/consortium: Accredited Philippine-based colleges and universities18.
- courses: Any 4- or 5-year baccalaureate degree program18.
- sectoral/hidden: Must be a child of an active OWWA member, or a sibling of a single / childless active OWWA member18.
- work_experience: None
- good_moral: Required27.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: OFW parent/sibling membership must be ACTIVE at the time of application18. Only one scholarship beneficiary per OFW family is allowed under OWWA scholarship programs27. Single marital status mandatory27.

### Timing
- who: Dependents of active OWWA members entering Grade 12 / 1st Year College or currently in 2nd to 5th Year College27.
- freshmen/soph/junior/senior/grad/reapply: : Yes (Incoming 1st Year Freshmen)27. | : Yes (Under Category 2)28. | : Yes (Under Category 2)28. | : Yes (Under Category 2)28. | : No18. | : Yes28.
- window: July 16 annually (for main application intake)28 / November 10 (for DOST-EDSP track)27. → July 31 annually28 / November 2827. (Fixed / Annual27.; AY AY 2025–2026 / AY 2026–202728.)

### Renewal
- maintain_gwa: Maintain a minimum GWA of at least 85.00% (or passing mark specified by OWWA RWO) each semester without failing grades27.
- regular_load: Full credit load per term as prescribed in curriculum18.
- no_failures: Zero failing, dropped, or incomplete grades27.
- return_service: None18.

### Disqualifiers / affiliations
- Inactive OWWA member contribution status18.
- Marriage of scholar during scholarship period (Must remain single)27.
- Dependent age exceeding 21 years old (Freshmen) or 30 years old (Upperclassmen)27.
- Incurring a failing grade or dropping a subject27.
- Concurrent enjoyment of another OWWA or major government scholarship grant27.

### Benefits (catalog)
- tuition: Direct financial grant disbursed to scholar27.
- stipend: Integrated into annual financial assistance package27.
- allowance: Financial assistance of ₱60,000.00 per Academic Year (disbursed at ₱30,000.00 per semester)18.

### Documents (operational hidden reqs)
- Proof of OFW Active Membership (OWWA Membership verification printout / Official Receipt)18.
- Valid Passport Bio Page of OFW parent / sibling27.
- PSA Birth Certificate of applicant dependent and PSA Marriage Certificate of parents27.
- Academic Records: Form 137 / Form 138 / TOR showing GWA >= 80% (Freshmen) or >= 85% (Upperclassmen) with zero failing marks27.
- Two (2) pieces 2x2 ID photos with white background and name tag27.
- Certificate of Good Moral Character27.

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
  "minimum_gwa": 80.0,
  "renewal_gwa": 85.0,
  "age_limit": 21,
  "parent_employment_restriction": "OWWA_ACTIVE_MEMBER_DEPENDENT",
  "school_type": [
    "CHED_RECOGNIZED_HEI"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "application_window": {
    "open": "07-16",
    "close": "07-31"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Age Mismatch across Categories: The system must apply age_limit: 21 for incoming 1st
- verification: Verified18. | confidence: 92/100.

- CONTRADICTION/NOTE: entry GWA (80.00% (Freshmen entry) / 85.00% (Upperclassmen entry)27.) vs renewal (Maintain a minimum GWA of at least 85.00% (or passing mark specified by OWWA RWO) each semester without failing grades27.)

---

## OFW Dependent Scholarship Program (ODSP)18 (ID: 86)

### Hard eligibility
- citizenship: Natural-born Filipino citizen28.
- residency/destination: Resident of the Philippines28.
- education_level: College / Undergraduate9.
- eligible_year_levels: Category 1 (Incoming 1st Year Freshmen); Category 2 (2nd to 5th Year College Students)18.
- incoming_freshman_only: No18.
- existing_college: Yes28.
- graduate_students: Ineligible18.
- current_enrollment: Enrolled or accepted in a college or university in the Philippines18.
- academic: SHS Report Card or college transcript showing General Weighted Average (GWA) of at least 75.00% or passing mark with no failing grades18.
- minimum_gwa: 75.00%18.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE28.
- income_ceilings: OFW parent monthly basic salary must NOT exceed USD $1,000.0018.
- age: Single and not over 21 years old for Category 1 (Freshmen)28; single and not over 30 years old for Category 2 (Upperclassmen)28.
- school/consortium: Philippine-based colleges and universities18.
- courses: Any undergraduate degree program18.
- sectoral/hidden: Dependent child or sibling of an active OWWA member18.
- work_experience: None
- good_moral: Required28.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Single marital status mandatory28. OFW membership must be active at application18. Allocation capped per province18.

### Timing
- who: Dependents of low-income active OWWA members entering or enrolled in college18.
- freshmen/soph/junior/senior/grad/reapply: : Yes18. | : Yes28. | : Yes28. | : Yes28. | : No18. | : Yes28.
- window: July 16 annually28. → July 31 annually28. (Fixed / Annual28.; AY AY 2025–2026 / AY 2026–202728.)

### Renewal
- maintain_gwa: Maintain a passing GWA per term (at least 75.00%) with zero failing grades18.
- regular_load: Enrolled in regular load per semester18.
- no_failures: Zero failing marks28.
- return_service: None18.

### Disqualifiers / affiliations
- OFW monthly salary exceeding USD $1,000.0028.
- Inactive OWWA contribution status18.
- Marriage of scholar during award period28.
- Dependent age exceeding 21 years old (Freshmen) or 30 years old (Upperclassmen)28.
- Incurring failing grades28.

### Benefits (catalog)
- tuition: Direct cash assistance disbursed to scholar28.
- stipend: Integrated into annual assistance grant28.
- allowance: Financial assistance of ₱20,000.00 per Academic Year (disbursed at ₱10,000.00 per semester)28.

### Documents (operational hidden reqs)
- Proof of OFW Active Membership (OWWA printout)18.
- Copy of OFW Valid Passport bio page28.
- Proof of OFW Monthly Salary (Employment Contract, Overseas Employment Certificate [OEC], Payslip showing salary <= USD $1,000.00)28.
- PSA Birth Certificate of applicant dependent28.
- Academic Report Card / TOR showing GWA >= 75.00%18.
- Two (2) 2x2 ID photos27.

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
  "age_limit": 21,
  "parent_employment_restriction": "OWWA_ACTIVE_MEMBER_SALARY_1000USD_BELOW",
  "school_type": [
    "CHED_RECOGNIZED_HEI"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "application_window": {
    "open": "07-16",
    "close": "07-31"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Salary Cap Filter: The system must check user.ofw_parent_monthly_salary_usd <= 1000.
- verification: Verified18. | confidence: 96/100.

- CONTRADICTION/NOTE: entry GWA (75.00%18.) vs renewal (Maintain a passing GWA per term (at least 75.00%) with zero failing grades18.)

---

## Congressional Migrant Workers Scholarship Program (CMWSP)27 (ID: 87)

### Hard eligibility
- citizenship: Natural-born Filipino citizen27.
- residency/destination: Resident of the Philippines27.
- education_level: College / Undergraduate9.
- eligible_year_levels: Year 1 (Incoming First-Year College Freshmen)27.
- incoming_freshman_only: Yes27.
- existing_college: Ineligible27.
- graduate_students: Ineligible27.
- current_enrollment: Enrolled or accepted as an incoming 1st-year college student in an accredited Philippine college or university27.
- academic: Senior High School General Weighted Average (GWA) of at least 80.00% or equivalent with zero failing grades27.
- minimum_gwa: 80.00%27.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE27.
- income_ceilings: Combined family annual income must NOT exceed USD $2,400.0027.
- age: OFW applicant must NOT be older than 45 years on date of application27; dependent child applicant must NOT be older than 21 years27.
- school/consortium: Accredited Philippine colleges and universities27.
- courses: Restricted to Science and Technology courses based on the Department of Science and Technology (DOST) priority list27.
- sectoral/hidden: Active or former documented OFW, or a legitimate child of an OFW27.
- work_experience: None
- good_moral: Required27.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Single marital status required for dependent child applicants27. Must pass selection evaluation27.

### Timing
- who: Incoming 1st-year college freshmen (OFWs under 45 or children of OFWs under 21)27.
- freshmen/soph/junior/senior/grad/reapply: : Yes (Prior to starting 1st term)27. | : No27. | : No27. | : No27. | : No27. | : No27.
- window: November 10 annually27. → November 28 annually27. (Fixed / Annual27.; AY AY 2026–202727.)

### Renewal
- maintain_gwa: Maintain required GWA (80.00%) per semester without failing grades27.
- regular_load: Full-time credit enrollment in approved S&T degree27.
- no_failures: Zero failing marks27.
- return_service: None27.

### Disqualifiers / affiliations
- Combined family annual income exceeding USD $2,400.0027.
- Enrolling in non-S&T degree programs27.
- Age exceeding 21 years (for dependent) or 45 years (for OFW)27.
- Incurring a failing grade in any subject27.

### Benefits (catalog)
- tuition: Direct financial grant disbursed to scholar27.
- stipend: Integrated into annual grant package27.
- allowance: Financial assistance of ₱60,000.00 per Academic Year (disbursed at ₱30,000.00 per semester)27.

### Documents (operational hidden reqs)
- Proof of OFW Status / Valid Passport Bio Page27.
- PSA Birth Certificate of dependent applicant27.
- Proof of Family Income showing combined annual income <= USD $2,400.0027.
- SHS Form 137 / Form 138 Report Card showing GWA >= 80.00% with zero failing grades27.
- Certificate of Enrollment / Admission in a DOST priority S&T course27.
- Two (2) 2x2 ID photos27.

### Recommended schema
`json
{
  "education_level": [
    "College"
  ],
  "eligible_year_levels": [
    1
  ],
  "incoming_year_only": true,
  "requires_current_enrollment": true,
  "minimum_gwa": 80.0,
  "age_limit": 21,
  "parent_employment_restriction": "OWWA_DOCUMENTED_OFW",
  "priority_courses": [
    "DOST_ST_PRIORITY_COURSES"
  ],
  "school_type": [
    "CHED_RECOGNIZED_HEI"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "application_window": {
    "open": "11-10",
    "close": "11-28"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Course Filter Constraint: The system must match user.course_code against the
- verification: Verified27. | confidence: 96/100.

- CONTRADICTION/NOTE: entry GWA (80.00%27.) vs renewal (Maintain required GWA (80.00%) per semester without failing grades27.)

---

## Training for Work Scholarship Program (TWSP)25 (ID: 112)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen25.
- residency/destination: Resident of the Philippines25.
- education_level: Technical-Vocational Education and Training (TVET)9.
- eligible_year_levels: Non-degree short-term TVET qualifications (NC I to NC IV)25.
- incoming_freshman_only: No25.
- existing_college: Eligible (Provided not currently enrolled in another TESDA scholarship)25.
- graduate_students: Eligible25.
- current_enrollment: Enrolled or accepted in a TESDA-registered TVET program25.
- academic: Basic literacy and numeracy; satisfies specific TVET qualification entry standards25.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Passing basic qualification entry test required)9.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE9.
- age: Must be at least 15 years old at the start of the training program25.
- school/consortium: TESDA Technology Institutions (TTIs) and TESDA-accredited private TVIs25.
- courses: TESDA priority sector qualifications (Construction, IT-BPM, Tourism, Agriculture, Logistics, Manufacturing)25.
- sectoral/hidden: Unemployed workers, underemployed, returning OFWs, displaced workers prioritized25.
- work_experience: None
- good_moral: NOT SPECIFIED IN OFFICIAL SOURCE.
- health: Physically fit to undergo technical training25.
- other_rules/conflicts: Trainee must NOT be currently enrolled in any other active TESDA scholarship grant25.

### Timing
- who: Any Filipino citizen aged 15 or older seeking technical skills training25.
- freshmen/soph/junior/senior/grad/reapply: : Yes25. | : Yes25. | : Yes25. | : Yes25. | : Yes25. | : Yes (For a different NC level or qualification sector)25.
- window: Year-round / Rolling intake9. → December 31 annually (or subject to allocation batch schedules)9. (Rolling / Continuous9.; AY AY 2025–2026 / AY 2026–20279.)

### Renewal
- maintain_gwa: Maintain 80% minimum attendance rate and pass practical competency evaluations25.
- regular_load: Full attendance during training schedule25.
- no_failures: None
- return_service: None9.

### Disqualifiers / affiliations
- Unexcused absences exceeding 20% of total training hours25.
- Simultaneous enrollment in another active TESDA scholarship program25.
- Age below 15 years old25.

### Benefits (catalog)
- tuition: 100% Full training cost waiver paid to TVI25.
- stipend: Integrated into daily training allowance25.
- allowance: Daily training allowance (₱160.00 per attendance day)25.

### Documents (operational hidden reqs)
- Accomplished TESDA Learner's Profile Form (MIS 03-02)25.
- Birth Certificate (PSA or Local Civil Registrar) or PhilSys ID25.
- Barangay Clearance or Police Clearance25.
- Three (3) 1x1 ID photos (white background, shirt with collar)25.

### Recommended schema
`json
{
  "education_level": [
    "TVET"
  ],
  "eligible_year_levels": [
    1
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": false,
  "minimum_gwa": null,
  "age_limit_min": 15,
  "school_type": [
    "TESDA_TECHNOLOGY_INSTITUTION",
    "TESDA_ACCREDITED_TVI"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "01-01",
    "close": "12-31"
  },
  "deadline_type": "rolling",
  "cycle_type": "rolling",
  "renewable": false,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Multiple Grant Conflict: System must check user.active_tesda_scholarship == false to
- verification: Verified25. | confidence: 95/100.

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Passing basic qualification entry test required)9.) vs renewal (Maintain 80% minimum attendance rate and pass practical competency evaluations25.)

---

## Special Training for Employment Program (STEP)25 (ID: 113)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen25.
- residency/destination: Resident of target barangay or municipality25.
- education_level: Technical-Vocational Education and Training (TVET)9.
- eligible_year_levels: Non-degree short-term TVET qualifications25.
- incoming_freshman_only: No25.
- existing_college: Eligible25.
- graduate_students: Eligible25.
- current_enrollment: Enrolled or accepted in a STEP community training program25.
- academic: Basic literacy and numeracy25.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE9.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE9.
- age: Must be at least 15 years old25.
- school/consortium: Community training centers and accredited TVIs25.
- courses: Specialty trade courses (e.g., Welding, Electronics Repair, Baking, Small Engine Repair, Cosmetology)25.
- sectoral/hidden: Underprivileged citizens, informal economy workers, displaced workers, 4Ps beneficiaries prioritized25.
- work_experience: None
- good_moral: NOT SPECIFIED IN OFFICIAL SOURCE.
- health: Physically fit for practical trade tasks25.
- other_rules/conflicts: Must NOT be enrolled in another TESDA scholarship concurrently25.

### Timing
- who: Barangay residents seeking self-employment trade skills25.
- freshmen/soph/junior/senior/grad/reapply: : Yes25. | : Yes25. | : Yes25. | : Yes25. | : Yes25. | : Yes (For a different trade toolkit program)25.
- window: Year-round / Rolling intake9. → December 31 annually9. (Rolling / Community batch intake25.; AY AY 2025–2026 / AY 2026–20279.)

### Renewal
- maintain_gwa: Maintain 80% minimum attendance rate and pass competency assessment25.
- regular_load: Full attendance during community training sessions25.
- no_failures: None
- return_service: None9.

### Disqualifiers / affiliations
- Unexcused attendance drop exceeding 20% of training duration25.
- Concurrent enrollment in another active TESDA scholarship25.
- Failure to complete practical trade modules25.

### Benefits (catalog)
- tuition: 100% Free training cost25.
- stipend: Integrated into daily training allowance25.
- allowance: Daily training allowance (₱160.00 per attendance day)25.

### Documents (operational hidden reqs)
- Accomplished TESDA Learner's Profile Form (MIS 03-02)25.
- Barangay Certificate of Indigency / Residency25.
- Birth Certificate or PhilSys ID25.
- Three (3) 1x1 ID photos25.

### Recommended schema
`json
{
  "education_level": [
    "TVET"
  ],
  "eligible_year_levels": [
    1
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": false,
  "minimum_gwa": null,
  "age_limit_min": 15,
  "includes_starter_toolkits": true,
  "school_type": [
    "COMMUNITY_TRAINING_CENTER",
    "TESDA_ACCREDITED_TVI"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "application_window": {
    "open": "01-01",
    "close": "12-31"
  },
  "deadline_type": "rolling",
  "cycle_type": "rolling",
  "renewable": false,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Targeted Matching: ID 113 is designed specifically for informal sector trade training with
- verification: Verified25. | confidence: 92/100.

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE9.) vs renewal (Maintain 80% minimum attendance rate and pass competency assessment25.)

---

## Education and Livelihood Assistance Program (ELAP)9 (ID: 124)

### Hard eligibility
- citizenship: Natural-born Filipino citizen18.
- residency/destination: Resident of the Philippines18.
- education_level: Elementary, Secondary (JHS/SHS), College / Tertiary9.
- eligible_year_levels: All year levels from primary through tertiary education9.
- incoming_freshman_only: No9.
- existing_college: Yes9.
- graduate_students: Ineligible18.
- current_enrollment: Enrolled in a recognized elementary, secondary, or tertiary institution18.
- academic: Passing General Weighted Average (GWA) of at least 75.00% or passing mark9.
- minimum_gwa: 75.00%9.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: Combined family annual gross income must NOT exceed ₱250,000.009.
- age: Dependent child must be below 21 years old for college level (or under 18 for basic education)18.
- school/consortium: Recognized public or private educational institutions18.
- courses: Any course or grade level18.
- sectoral/hidden: Must be a surviving dependent child of an active OWWA member who died or suffered permanent total disability31. Limited to ONE (1) child beneficiary per deceased/incapacitated OFW family31.
- work_experience: None
- good_moral: Required18.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: OFW parent must have been an active OWWA member at the time of death or permanent disability31.

### Timing
- who: Surviving child of deceased or permanently incapacitated active OFW31.
- freshmen/soph/junior/senior/grad/reapply: : Yes9. | : Yes9. | : Yes9. | : Yes9. | : No18. | : Yes (Continuous annual support until course
- window: Year-round intake following casualty event9. → Specified per regional office window / annual cycle9. (Annual9.; AY AY 2025–2026 / AY 2026–20279.)

### Renewal
- maintain_gwa: Maintain passing GWA (at least 75.00%) every school year9.
- regular_load: Continuous enrollment in regular grade/year level18.
- no_failures: Passing all enrolled subjects18.
- return_service: None9.

### Disqualifiers / affiliations
- OFW parent not an active OWWA member at time of death or disability31.
- More than one child beneficiary applying from the same family (Strictly 1 child per family rule)31.
- Combined family income exceeding ₱250,000.009.
- Academic failure or dropping out from school18.

### Benefits (catalog)
- tuition: Direct cash assistance grant18.
- stipend: Integrated into annual grant package18.
- allowance: None

### Documents (operational hidden reqs)
- Official Death Certificate or Medical Certificate of Permanent Disability of OFW issued by proper authority18.
- Proof of Active OWWA Membership at time of casualty event30.
- PSA Marriage Certificate of parents and PSA Birth Certificate of child beneficiary18.
- Form 138 Report Card or College Transcript showing passing GWA >= 75.00%9.
- BIR Tax Exemption Certificate, ITR, or Barangay Certificate of Indigency (Income <= ₱250,000.00)9.
- Certificate of Enrollment from school18.

### Recommended schema
`json
{
  "education_level": [
    "Senior High School",
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
  "income_limit": 250000,
  "parent_employment_restriction": "OWWA_DECEASED_OR_INCAPACITATED_ACTIVE_MEMBER",
  "one_beneficiary_per_family": true,
  "school_type": [
    "RECOGNIZED_EDUCATIONAL_INSTITUTION"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "application_window": {
    "open": "01-01",
    "close": "12-31"
  },
  "deadline_type": "rolling",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Missing Casualty and Single-Beneficiary Flags: ID 124 strictly requires
- verification: Verified18. | confidence: 92/100.

- CONTRADICTION/NOTE: entry GWA (75.00%9.) vs renewal (Maintain passing GWA (at least 75.00%) every school year9.)

---
