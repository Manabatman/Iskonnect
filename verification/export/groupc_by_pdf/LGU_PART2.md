# DATABASE_V3_GROUPC_LGU_PART2.pdf — Implementation Details

Scholarships: 16

## Pasig City Regular Academic Scholarship Program4 (ID: 25)

### Hard eligibility
- citizenship: Filipino citizen3
- residency/destination: Bonafide resident of Pasig City5
- education_level: Elementary, Junior High School, Senior High School, College4
- eligible_year_levels: All year levels (Grade 1 through College Senior)1
- incoming_freshman_only: No7
- existing_college: Yes7
- graduate_students: No1
- current_enrollment: Enrolled in a recognized public or private educational institution4
- academic: Passing general weighted average as certified by report of grades5
- minimum_gwa: 85.00%1
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined family gross annual income not exceeding PHP 300,000.00 or submission of a Barangay Certificate of Indigence1
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Recognized public or private schools5
- courses: NOT SPECIFIED IN OFFICIAL SOURCE
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Certificate of Good Moral Character8
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Strict enforcement of the "One-Scholar-One-Family Policy" (only one scholar per household)6; Voter's Certification Record (VCR) of parent (for minors) or student (if 18+)8.

### Timing
- who: Resident students in elementary, secondary, and tertiary levels4
- freshmen/soph/junior/senior/grad/reapply: : Yes7 | : Yes7 | : Yes7 | : Yes7 | : No1 | : Yes (via annual renewal/reenlistment)7
- window: August 1, 20251 → September 19, 20257 (Annual1; AY AY 2025–20264)

### Renewal
- maintain_gwa: 85.00%1
- regular_load: Full-time academic load5
- no_failures: No failing or dropped subjects5
- return_service: False1

### Disqualifiers / affiliations
- Sibling already enjoying a Pasig City scholarship (violating One-Scholar-One-Family rule)6.
- Non-residency in Pasig City5.
- Annual family income exceeding PHP 300,000.00 without indigency status1.

### Benefits (catalog)
- tuition: Covered up to city cap for private school scholars; free in SUCs/LUCs1
- stipend: PHP 1,500.00 per month1
- allowance: Total annual value up to PHP 25,000.001

### Documents (operational hidden reqs)
- Printed Online Scholarship Application Form5
- School ID (photocopy, front and back)5
- Report of Grades / Card for the preceding academic year4
- Proof of Enrollment / Enrolment Slip for current academic year4
- Proof of Parents' / Guardians' Income (ITR, Pay Slip, or Barangay Certificate of Indigence)4
- Barangay Certificate of Residency with years of residence indicated4
- Voter's Certification Record (VCR) of parent or applicant8
- Written Essay: "Why do I want to be a Pasig Scholar?"4

### Recommended schema
`json
{
  "education_level": [
    "Elementary",
    "High School",
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
  "income_limit": 300000,
  "residency_restriction": "PASIG_CITY",
  "one_scholar_per_family_clause": true,
  "school_type": [
    "PUBLIC",
    "PRIVATE"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "application_window": {
    "open": "2025-08-01",
    "close": "2025-09-19"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Household Conflict Risk: Recommending this program to applicants whose family
- verification: Verified1 | confidence: None


---

## Pasig City Arts and Design Scholarship Program5 (ID: 26)

### Hard eligibility
- citizenship: Filipino citizen3
- residency/destination: Bonafide resident of Pasig City5
- education_level: Grade 11, Grade 12, College1
- eligible_year_levels: SHS Grade 11–12 and College Years 1–41
- incoming_freshman_only: No1
- existing_college: Yes1
- graduate_students: No1
- current_enrollment: Enrolled in Grade 11/12 Arts & Design Track or an artistic/creative tertiary degree4
- academic: Minimum GWA of 80.00%1
- minimum_gwa: 80.00%1
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined gross annual family income not exceeding PHP 350,000.001
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Recognized secondary and tertiary institutions5
- courses: Fine Arts, Graphic Design, Performing Arts, Architecture, Multimedia Arts, and SHS Arts & Design track4
- sectoral/hidden: Demonstrated artistic proficiency or enrollment in creative track4
- work_experience: None
- good_moral: Certificate of Good Moral Character8
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: One-Scholar-One-Family Policy applies6.

### Timing
- who: SHS Arts & Design students and creative tertiary majors4
- freshmen/soph/junior/senior/grad/reapply: : Yes1 | : Yes1 | : Yes1 | : Yes1 | : No1 | : Yes8
- window: August 1, 20251 → September 10, 20261 (Annual1; AY AY 2025–2026 / AY 2026–20271)

### Renewal
- maintain_gwa: 80.00%1
- regular_load: Full load in creative discipline5
- no_failures: Zero failing grades5
- return_service: False1

### Disqualifiers / affiliations
- Enrolled in non-arts/design degree programs4.
- Family income exceeding PHP 350,000.001.
- Non-residency in Pasig City5.

### Benefits (catalog)
- tuition: Full or partial coverage up to city cap1
- stipend: PHP 1,500.00 per month1
- allowance: Total annual value of PHP 28,000.001

### Documents (operational hidden reqs)
- Printed Online Application Form5
- Barangay Certificate of Residency4
- Proof of Enrollment in Arts & Design track / creative degree4
- Latest Report of Grades / TOR (GWA 80.00%)1
- Proof of Family Income (ITR / Indigency Certificate)4
- Portfolio of Creative Works / Portfolio Assessment Sheet5

### Recommended schema
`json
{
  "education_level": [
    "Grade 11",
    "Grade 12",
    "College"
  ],
  "eligible_year_levels": [
    11,
    12,
    1,
    2,
    3,
    4
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": true,
  "minimum_gwa": 80.0,
  "income_limit": 350000,
  "priority_courses": [
    "ARTS_AND_DESIGN_TRACK",
    "FINE_ARTS",
    "MULTIMEDIA_ARTS",
    "PERFORMING_ARTS"
  ],
  "residency_restriction": "PASIG_CITY",
  "school_type": [
    "PUBLIC",
    "PRIVATE"
  ],
  "application_window": {
    "open": "2025-08-01",
    "close": "2026-09-10"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Specialization Mismatch: Displaying this program to general STEM/ABM or non-creative
- verification: Verified1 | confidence: 95/100


---

## Cebu City College Scholarship Program1 (ID: 36)

### Hard eligibility
- citizenship: Filipino citizen3
- residency/destination: Bonafide resident of Cebu City1
- education_level: College1
- eligible_year_levels: Year 1, Year 2, Year 3, Year 41
- incoming_freshman_only: No1
- existing_college: Yes1
- graduate_students: No1
- current_enrollment: Enrolled in accredited partner colleges or universities within Cebu City1
- academic: Minimum GWA of 80.00% with no failing grades1
- minimum_gwa: 80.00%1
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined family annual income not exceeding PHP 350,000.001
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Accredited partner Higher Education Institutions in Cebu City1
- courses: CHED and City priority degree courses1
- sectoral/hidden: Registered voter status (applicant or parent) in Cebu City1
- work_experience: None
- good_moral: Certificate of Good Moral Character3
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Must not be a recipient of another major government scholarship2.

### Timing
- who: Resident high school graduates and ongoing college students in Cebu City1
- freshmen/soph/junior/senior/grad/reapply: : Yes1 | : Yes1 | : Yes1 | : Yes1 | : No1 | : Yes1
- window: June 15 annually1 → August 30 annually1 (Annual1; AY AY 2025–2026 / AY 2026–20271)

### Renewal
- maintain_gwa: 80.00%1
- regular_load: Full semestral unit load1
- no_failures: Zero failing marks1
- return_service: False1

### Disqualifiers / affiliations
- Non-voter status of parents or student in Cebu City1.
- Enrolling in non-accredited tertiary institutions outside Cebu City1.
- Family gross annual income exceeding PHP 350,000.001.

### Benefits (catalog)
- tuition: Up to PHP 10,000.00 per semester (PHP 20,000.00 per academic year) paid directly to partner school1
- stipend: NOT SPECIFIED IN OFFICIAL SOURCE
- allowance: Integrated into tuition subsidy voucher1

### Documents (operational hidden reqs)
- Cebu City Scholarship Application Form1
- Certificate of Residency from Barangay1
- Voter's Certification (Parent or Student) from COMELEC Cebu City1
- Form 138 / High School Report Card or Official TOR1
- Parents' Income Tax Return or Certificate of Indigency1
- Certificate of Good Moral Character3

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
  "minimum_gwa": 80.0,
  "income_limit": 350000,
  "residency_restriction": "CEBU_CITY",
  "voter_status_required": true,
  "school_type": [
    "PARTNER_HEI_CEBU_CITY"
  ],
  "partner_school_restricted": true,
  "application_window": {
    "open": "06-15",
    "close": "08-30"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Voter Status Failure: Applicants residing in Cebu City whose parents are registered voters
- verification: Verified1 | confidence: 92/100


---

## Scholarship on Tertiary Education Program – Financial Assistance (STEP-FA) Category B1 (ID: 37)

### Hard eligibility
- citizenship: Filipino citizen3
- residency/destination: Resident of Davao City13
- education_level: College1
- eligible_year_levels: Years 1, 2, 3, and 41
- incoming_freshman_only: No1
- existing_college: Yes12
- graduate_students: No1
- current_enrollment: Enrolled in a CHED-recognized Higher Education Institution in Davao City13
- academic: GWA of 90.00% to 92.99% (or 88.00% threshold per legacy baseline)1
- minimum_gwa: 88.00%1
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: PHP 300,000.00 annual family gross income; verified indigent/below-average income status by CSWDO1
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Recognized HEIs located within Davao City13
- courses: CHED-prescribed priority programs13
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Certificate of Good Moral Character13
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Strict "One Child Per Family" rule for EBSU grants13; candidate must not enjoy other government/private grants except school academic honor incentives13.

### Timing
- who: Graduating SHS students and enrolled tertiary students in Davao City12
- freshmen/soph/junior/senior/grad/reapply: : Yes12 | : Yes12 | : Yes12 | : Yes12 | : No1 | : Yes13
- window: April 1 annually12 → May 31 annually12 (Annual1; AY AY 2025–2026 / AY 2026–202712)

### Renewal
- maintain_gwa: 88.00%–90.00%1
- regular_load: Full academic unit load13
- no_failures: Zero failing or incomplete grades13
- return_service: False1

### Disqualifiers / affiliations
- Sibling already benefiting from an EBSU grant13.
- Enjoying another government/private scholarship13.
- GWA falling below 88.00% or presence of failing marks12.

### Benefits (catalog)
- tuition: False (direct financial assistance allowance)1
- stipend: PHP 2,000.00 per month1
- allowance: PHP 20,000.00 per semester (PHP 40,000.00 per academic year)1

### Documents (operational hidden reqs)
- EBSU eScholar Application Form11
- Certificate of Residency from Barangay12
- CSWDO Certificate of Indigency / Eligibility12
- Income Tax Return or Tax Exemption Certificate of both parents12
- SHS Report Card (for Freshmen) or Official TOR for past 2 semesters (for upperclassmen) showing required GWA12
- Certificate of Good Moral Character12
- Sworn statement of no sibling enjoying an EBSU scholarship13

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
  "minimum_gwa": 88.0,
  "maximum_gwa_cap": 92.99,
  "income_limit": 300000,
  "residency_restriction": "DAVAO_CITY",
  "one_child_per_family_clause": true,
  "school_type": [
    "DAVAO_CITY_HEI"
  ],
  "partner_school_restricted": true,
  "application_window": {
    "open": "04-01",
    "close": "05-31"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Category Misclassification: Applicants with GWA
- verification: Verified1 | confidence: 90/100

- CONTRADICTION/NOTE: entry GWA (88.00%1) vs renewal (88.00%–90.00%1)

---

## Special Educational Assistance Program (SEAP) for Lumad / Financial Assistance Program for Lumad Students1 (ID: 38)

### Hard eligibility
- citizenship: Filipino citizen3
- residency/destination: Resident of Davao City belonging to a recognized IP tribe12
- education_level: College, TVET1
- eligible_year_levels: All tertiary and vocational year levels1
- incoming_freshman_only: No1
- existing_college: Yes1
- graduate_students: No1
- current_enrollment: Enrolled or accepted in a tertiary or TVET institution in Davao City12
- academic: Passing general average (75.00% GWA minimum)1
- minimum_gwa: 75.00%1
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: PHP 200,000.00 annual family income; CSWDO Indigency certification1
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Recognized colleges, universities, or TVET centers in Davao City12
- courses: NOT SPECIFIED IN OFFICIAL SOURCE
- sectoral/hidden: Certificate of Tribal Membership / Indigenous Peoples certification issued by National Commission on Indigenous Peoples (NCIP) or Tribal Council12
- work_experience: None
- good_moral: Certificate of Good Moral Character12
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Must comply with EBSU one-scholar-per-family policy13.

### Timing
- who: Lumad / Indigenous tertiary and TVET students in Davao City12
- freshmen/soph/junior/senior/grad/reapply: : Yes1 | : Yes1 | : Yes1 | : Yes1 | : No1 | : Yes13
- window: April 1 annually12 → May 31 annually12 (Annual1; AY AY 2025–2026 / AY 2026–202712)

### Renewal
- maintain_gwa: 75.00% (passing status)1
- regular_load: Enrolled in prescribed program units13
- no_failures: Maintain passing grades12
- return_service: False1

### Disqualifiers / affiliations
- Lack of official NCIP tribal certification12.
- Non-residency in Davao City12.
- Family gross annual income exceeding PHP 200,000.001.

### Benefits (catalog)
- tuition: False (direct financial assistance)1
- stipend: PHP 2,000.00 per month1
- allowance: Total annual value of PHP 30,000.00 (PHP 15,000.00 per semester)1

### Documents (operational hidden reqs)
- EBSU Lumad Scholarship Application Form11
- NCIP Certificate of Tribal Membership / Indigenous Cultural Community Certification12
- CSWDO Certificate of Indigency12
- Certificate of Residency from Barangay12
- Parents' ITR or Tax Exemption Certificate12
- High School Report Card or College Grade Slip (GWA 75.00%)1
- Certificate of Good Moral Character12

### Recommended schema
`json
{
  "education_level": [
    "College",
    "TVET"
  ],
  "eligible_year_levels": [
    1,
    2,
    3,
    4
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": true,
  "minimum_gwa": 75.0,
  "income_limit": 200000,
  "sectoral_restriction": "NCIP_CERTIFIED_LUMAD_IP",
  "residency_restriction": "DAVAO_CITY",
  "school_type": [
    "DAVAO_CITY_HEI_TVET"
  ],
  "application_window": {
    "open": "04-01",
    "close": "05-31"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Sectoral Tag Omission: Recommending this program without checking
- verification: Verified1 | confidence: 98/100

- CONTRADICTION/NOTE: entry GWA (75.00%1) vs renewal (75.00% (passing status)1)

---

## Bislig City Collegiate Scholarship Program1 (ID: 39)

### Hard eligibility
- citizenship: Filipino citizen3
- residency/destination: Bonafide resident of Bislig City, Surigao del Sur1
- education_level: College1
- eligible_year_levels: Years 1, 2, 3, and 41
- incoming_freshman_only: No1
- existing_college: Yes1
- graduate_students: No1
- current_enrollment: Enrolled in an accredited Higher Education Institution1
- academic: Minimum GWA of 82.00% with no failing marks1
- minimum_gwa: 82.00%1
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined family annual gross income not exceeding PHP 240,000.001
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: CHED-recognized HEIs in Region XIII / Mindanao1
- courses: Agriculture, Teacher Education, Engineering, Information Technology, and Health Sciences1
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Certificate of Good Moral Character3
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Must not enjoy duplicate local government scholarship grants2.

### Timing
- who: Resident college students in Bislig City1
- freshmen/soph/junior/senior/grad/reapply: : Yes1 | : Yes1 | : Yes1 | : Yes1 | : No1 | : Yes1
- window: June 1 annually1 → July 31 annually1 (Annual1; AY AY 2025–2026 / AY 2026–20271)

### Renewal
- maintain_gwa: 82.00%1
- regular_load: Full load per semester1
- no_failures: Zero failing grades1
- return_service: False1

### Disqualifiers / affiliations
- Non-residency in Bislig City1.
- Family gross annual income exceeding PHP 240,000.001.
- Failure to maintain 82.00% GWA1.

### Benefits (catalog)
- tuition: False1
- stipend: NOT SPECIFIED IN OFFICIAL SOURCE
- allowance: Financial assistance grant of PHP 6,000.00 per semester (PHP 12,000.00 per academic year)1

### Documents (operational hidden reqs)
- Bislig City Scholarship Application Form1
- Barangay Certificate of Residency1
- Proof of Income (ITR or Barangay Certificate of Indigency PHP 240,000)1
- Official Report of Grades / TOR (GWA 82.00%)1
- Certificate of Enrollment / Registration Form1
- Certificate of Good Moral Character3

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
  "minimum_gwa": 82.0,
  "income_limit": 240000,
  "residency_restriction": "BISLIG_CITY",
  "school_type": [
    "CHED_RECOGNIZED_HEI"
  ],
  "application_window": {
    "open": "06-01",
    "close": "07-31"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Regional Boundary Risk: Students residing in adjacent Surigao del Sur municipalities (e.g.,
- verification: Verified1 | confidence: 96/100


---

## Cebu Province Grants Intended for Tertiary Students (CP GIFTS Program)1 (ID: 49)

### Hard eligibility
- citizenship: Filipino citizen3
- residency/destination: Resident of Cebu Province (component towns and cities outside independent chartered cities)1
- education_level: College1
- eligible_year_levels: Years 1, 2, 3, and 41
- incoming_freshman_only: No1
- existing_college: Yes1
- graduate_students: No1
- current_enrollment: Enrolled in a recognized State University, Local College, or Private HEI in Cebu1
- academic: Minimum GWA of 85.00%1
- minimum_gwa: 85.00%1
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined gross annual family income not exceeding PHP 200,000.001
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Recognized HEIs operating within Cebu Province1
- courses: NOT SPECIFIED IN OFFICIAL SOURCE
- sectoral/hidden: Indigent status verified by MSWDO1
- work_experience: None
- good_moral: Certificate of Good Moral Character3
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Mandatory participation in provincial civic and environmental activities1.

### Timing
- who: Resident college students in Cebu Province1
- freshmen/soph/junior/senior/grad/reapply: : Yes1 | : Yes1 | : Yes1 | : Yes1 | : No1 | : Yes1
- window: July 1 annually1 → August 15 annually1 (Annual1; AY AY 2025–2026 / AY 2026–20271)

### Renewal
- maintain_gwa: 85.00%1
- regular_load: Full-time credit load1
- no_failures: Zero failing marks1
- return_service: True (community civic engagement hours mandated by province)1

### Disqualifiers / affiliations
- Independent chartered city residency (e.g., Cebu City, Lapu-Lapu City, Mandaue City) if excluded under specific provincial guidelines1.
- Family gross income exceeding PHP 200,000.001.
- Failing grades during semestral evaluation1.

### Benefits (catalog)
- tuition: False1
- stipend: NOT SPECIFIED IN OFFICIAL SOURCE
- allowance: PHP 10,000.00 per semester (PHP 20,000.00 per academic year)1

### Documents (operational hidden reqs)
- CP-GIFTS Application Form1
- Barangay and MSWDO Certificate of Indigency1
- Certificate of Residency from Municipality/City1
- Parents' ITR or BIR Tax Exemption Certificate ( PHP 200,000)1
- College TOR or SHS Form 138 (GWA 85.00%)1
- Certificate of Good Moral Character3

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
  "income_limit": 200000,
  "residency_restriction": "CEBU_PROVINCE",
  "return_service_required": true,
  "school_type": [
    "CEBU_PROVINCE_HEI"
  ],
  "application_window": {
    "open": "07-01",
    "close": "08-15"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● City Jurisdiction Conflict: Students residing in highly urbanized independent cities in
- verification: Verified1 | confidence: 88/100


---

## Tabuk City College Academic Scholarship1 (ID: 51)

### Hard eligibility
- citizenship: Filipino citizen3
- residency/destination: Bonafide resident of Tabuk City, Kalinga1
- education_level: College1
- eligible_year_levels: Years 1, 2, 3, and 41
- incoming_freshman_only: No1
- existing_college: Yes1
- graduate_students: No1
- current_enrollment: Enrolled in a recognized tertiary institution1
- academic: Minimum GWA of 75.00% (passing average)1
- minimum_gwa: 75.00%1
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined family gross annual income not exceeding PHP 120,000.001
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Accredited colleges and universities in CAR / Northern Luzon1
- courses: NOT SPECIFIED IN OFFICIAL SOURCE
- sectoral/hidden: Indigent family background certified by CSWDO1
- work_experience: None
- good_moral: Certificate of Good Moral Character3
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Must not receive duplicate financial grants from Tabuk City LGU2.

### Timing
- who: Resident college students in Tabuk City1
- freshmen/soph/junior/senior/grad/reapply: : Yes1 | : Yes1 | : Yes1 | : Yes1 | : No1 | : Yes1
- window: July 15, 20261 → August 31, 20261 (Semestral / Annual1; AY AY 2026–20271)

### Renewal
- maintain_gwa: 75.00%1
- regular_load: Full academic load1
- no_failures: Zero failing grades1
- return_service: False1

### Disqualifiers / affiliations
- Family gross annual income exceeding PHP 120,000.001.
- Non-residency in Tabuk City1.
- Presence of failing marks during semestral review1.

### Benefits (catalog)
- tuition: False1
- stipend: NOT SPECIFIED IN OFFICIAL SOURCE
- allowance: PHP 4,000.00 per semester (PHP 8,000.00 per academic year)1

### Documents (operational hidden reqs)
- Tabuk City Scholarship Application Form1
- Barangay Certificate of Residency1
- CSWDO Certificate of Indigency ( PHP 120,000 income)1
- College Grade Slip or Form 138 (GWA 75.00%)1
- Certificate of Enrollment / Registration Slip1
- Certificate of Good Moral Character3

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
  "minimum_gwa": 75.0,
  "income_limit": 120000,
  "residency_restriction": "TABUK_CITY",
  "school_type": [
    "RECOGNIZED_HEI"
  ],
  "application_window": {
    "open": "2026-07-15",
    "close": "2026-08-31"
  },
  "deadline_type": "exact",
  "cycle_type": "semester",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Strict Poverty Threshold: The PHP 120,000 income ceiling is low; applicants above this
- verification: Verified1 | confidence: 90/100


---

## Quezon City Scholarship Program (QCSP)2 (ID: 88)

### Hard eligibility
- citizenship: Filipino citizen2
- residency/destination: Bona fide resident of Quezon City holding a valid QCitizen ID2
- education_level: Senior High School, College, TVET, Postgraduate2
- eligible_year_levels: All year levels corresponding to track2
- incoming_freshman_only: No (Varies: QC Excel is incoming 1st year; Academic/Economic cover ongoing)2
- existing_college: Yes2
- graduate_students: Yes (Postgraduate Scholarship Track)2
- current_enrollment: Enrolled, registered, or accepted in an educational institution recognized by the city2
- academic: Academic Track: GWA 1.75 (89.00%) or SHS Academic Honors 1–10; Economic Track: GWA 3.00 (75.00%); Athletic/Arts & Youth Leaders Tracks: GWA 2.50 (85.00%)2
- minimum_gwa: 89.00% (1.75 Academic Track) / 75.00% (Economic Track)2
- alt_class_rank: Academic Honors Top 1 to 10 of graduating SHS class2
- income_ceilings: Combined family annual income not exceeding PHP 400,000.001
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Educational institutions recognized by Quezon City / CHED / DepEd / TESDA2
- courses: City priority disciplines for QC Excel & Specialized Tracks2
- sectoral/hidden: Economic track prioritizes 4Ps, solo parent dependents, PWDs, ALS graduates, and displaced families2
- work_experience: None
- good_moral: Certificate of Good Moral Character2
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Must NOT be a recipient of any other Local Government Unit (LGU) scholarship2.

### Timing
- who: Resident SHS, College, TVET, and Postgraduate students in Quezon City2
- freshmen/soph/junior/senior/grad/reapply: : Yes2 | : Yes2 | : Yes2 | : Yes2 | : Yes (Postgraduate track)2 | : Yes (Semestral renewal required for tertiary)2
- window: May 25, 20262 → June 13, 20262 (Annual application with semestral renewal enlistment2; AY AY 2025–2026 / AY 2026–20272)

### Renewal
- maintain_gwa: 1.75 (Academic), 2.50 (Leadership/Sports), 3.00 (Economic)2
- regular_load: Full semestral unit load2
- no_failures: Zero failing grades during semestral evaluation2
- return_service: False (community civic volunteerism encouraged)1

### Disqualifiers / affiliations
- Holding a scholarship from another Local Government Unit (LGU exclusivity violation)2.
- Lack of valid QCitizen ID or non-residency in Quezon City2.
- Family gross annual income exceeding PHP 400,000.001.

### Benefits (catalog)
- tuition: Covered per track allocation in partner institutions1
- stipend: PHP 3,500.00 per month (PHP 17,500.00 per semester)1
- allowance: Direct financial stipend up to PHP 75,000.00 per academic year depending on category1

### Documents (operational hidden reqs)
- Valid QCitizen ID2
- Accomplished QC eServices Online Application2
- Proof of Residency in Quezon City2
- Grade Slip / TOR / Form 138 showing required GWA2
- Proof of Enrollment in recognized institution2
- Income Tax Return or Barangay Certificate of Indigency2
- Track-specific proofs (SK Endorsement, Sports Certificate, PWD ID, Solo Parent ID)2

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
  "minimum_gwa": 89.0,
  "rank_cutoff_alternative": 10,
  "income_limit": 400000,
  "residency_restriction": "QUEZON_CITY_QCITIZEN_ID",
  "lgu_exclusivity_clause": true,
  "school_type": [
    "RECOGNIZED_INSTITUTION"
  ],
  "application_window": {
    "open": "05-25",
    "close": "06-13"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Dual LGU Conflict: Students enjoying another city grant (e.g., Manila, Taguig) who apply
- verification: Verified1 | confidence: 88/100

- CONTRADICTION/NOTE: entry GWA (89.00% (1.75 Academic Track) / 75.00% (Economic Track)2) vs renewal (1.75 (Academic), 2.50 (Leadership/Sports), 3.00 (Economic)2)

---

## Manuel L. Quezon Filipino Language and Literature Scholarship Program16 (ID: 89)

### Hard eligibility
- citizenship: Filipino citizen18
- residency/destination: Resident of Quezon City holding a valid QCitizen ID15
- education_level: College, Graduate (Master's / PhD), and Creative Writers/Researchers1
- eligible_year_levels: All tertiary and post-graduate year levels16
- incoming_freshman_only: No16
- existing_college: Yes16
- graduate_students: Yes16
- current_enrollment: Enrolled in eligible degree programs: Filipino Language, Filipino Literature, Journalism, Philippine Studies, Education (Filipino major), Comparative Literature, or Linguistics16
- academic: Pass QCYDO interviews, aptitude tests, or submit a portfolio of published original works / literary awards from recognized publisher16
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (evaluated via literary proficiency/portfolio)16
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE (Uncapped under specialized mandate)1
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Recognized public or private Higher Education Institutions15
- courses: BA/BS/MA/PhD in Filipino, Panitikan, Philippine Studies, Malikhaing Pagsulat, Journalism, Education major in Filipino, Linguistics16
- sectoral/hidden: Active involvement or demonstrated proficiency in Filipino literary writing, research, or education16
- work_experience: None
- good_moral: Certificate of Good Moral Character16
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Must NOT hold another LGU scholarship grant15.

### Timing
- who: Tertiary students, postgraduate scholars, educators, and creative writers specializing in Filipino16
- freshmen/soph/junior/senior/grad/reapply: : Yes16 | : Yes16 | : Yes16 | : Yes16 | : Yes (Postgraduate and Creative Writing track)16 | : Yes16
- window: January 22, 202618 → Announced per annual cycle16 (Annual / Semestral1; AY AY 2025–2026 / AY 2026–202715)

### Renewal
- maintain_gwa: Satisfactory academic standing in specialized degree16
- regular_load: Enrolled in prescribed program units16
- no_failures: Zero failing marks16
- return_service: False1

### Disqualifiers / affiliations
- Enrollment in non-Filipino/non-Philippine studies degree programs16.
- Failure to present literary portfolio or approved research proposal16.
- Non-residency in Quezon City15.

### Benefits (catalog)
- tuition: Up to PHP 160,000.00 per AY for tertiary scholars in private HEIs; up to PHP 105,000.00 per AY for postgraduate scholars18
- stipend: NOT SPECIFIED IN OFFICIAL SOURCE
- allowance: PHP 50,000.00 annual stipend for public HEI tertiary scholars18

### Documents (operational hidden reqs)
- Valid QCitizen ID15
- Online Application via QC eServices16
- Proof of Enrollment in eligible Filipino language/literature/Philippine studies degree16
- Academic Grades / Official TOR16
- Literary Portfolio / Proof of Published Works / Certification of Publication from recognized publisher16
- Approved Research Proposal on Filipino language/literature (for Postgraduate track)18

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
    4,
    5
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": true,
  "priority_courses": [
    "BA_FILIPINO",
    "BS_EDUCATION_FILIPINO",
    "MA_FILIPINO",
    "PHD_FILIPINO",
    "PHILIPPINE_STUDIES",
    "MALIKHAING_PAGSULAT",
    "LINGUISTICS_FILIPINO"
  ],
  "residency_restriction": "QUEZON_CITY_QCITIZEN_ID",
  "lgu_exclusivity_clause": true,
  "school_type": [
    "PUBLIC",
    "PRIVATE"
  ],
  "application_window": {
    "open": "01-22",
    "close": "annual_notice"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Field of Study Filtering: System must validate user.course_code against approved
- verification: Verified17 | confidence: 98/100

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (evaluated via literary proficiency/portfolio)16) vs renewal (Satisfactory academic standing in specialized degree16)

---

## Pasig City Sports Scholarship Program5 (ID: 92)

### Hard eligibility
- citizenship: Filipino citizen3
- residency/destination: Bonafide resident of Pasig City5
- education_level: Grade 11, Grade 12, College1
- eligible_year_levels: SHS Grade 11–12 and College Years 1–41
- incoming_freshman_only: No1
- existing_college: Yes1
- graduate_students: No1
- current_enrollment: Enrolled in a recognized secondary or tertiary institution5
- academic: Minimum GWA of 80.00%1
- minimum_gwa: 80.00%1
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined gross annual family income not exceeding PHP 350,000.001
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Recognized public or private schools5
- courses: NOT SPECIFIED IN OFFICIAL SOURCE
- sectoral/hidden: Endorsement from Pasig City Sports Development Office or verified athletic portfolio in recognized sports competitions5
- work_experience: None
- good_moral: Certificate of Good Moral Character8
- health: Physically fit to participate in athletic training and competition9
- other_rules/conflicts: One-Scholar-One-Family Policy applies6.

### Timing
- who: Student-athletes in SHS and College5
- freshmen/soph/junior/senior/grad/reapply: : Yes1 | : Yes1 | : Yes1 | : Yes1 | : No1 | : Yes8
- window: August 1, 20251 → September 10, 20261 (Annual1; AY AY 2025–2026 / AY 2026–20271)

### Renewal
- maintain_gwa: 80.00%1
- regular_load: Full-time student status5
- no_failures: Zero failing grades5
- return_service: False1

### Disqualifiers / affiliations
- Absence of recognized athletic credentials or sports office endorsement5.
- Non-residency in Pasig City5.
- GWA dropping below 80.00%1.

### Benefits (catalog)
- tuition: Full or partial coverage up to city limit1
- stipend: PHP 2,000.00 per month1
- allowance: Total annual value of PHP 30,000.001

### Documents (operational hidden reqs)
- Printed Online Application Form5
- Barangay Certificate of Residency4
- Proof of Enrollment4
- Report of Grades / TOR showing GWA 80.00%1
- Parents' Proof of Income / Indigency Certificate4
- Athletic Portfolio / Certificates of Sports Medals & Awards / Endorsement from Sports Office9

### Recommended schema
`json
{
  "education_level": [
    "Grade 11",
    "Grade 12",
    "College"
  ],
  "eligible_year_levels": [
    11,
    12,
    1,
    2,
    3,
    4
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": true,
  "minimum_gwa": 80.0,
  "income_limit": 350000,
  "residency_restriction": "PASIG_CITY",
  "athletic_qualification_required": true,
  "school_type": [
    "PUBLIC",
    "PRIVATE"
  ],
  "application_window": {
    "open": "2025-08-01",
    "close": "2026-09-10"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Credentials Verification: Applicants uploading non-sanctioned sports certificates will be
- verification: Verified1 | confidence: 96/100


---

## Pasig City Out-of-School Learners (OSL) Scholarship Program5 (ID: 93)

### Hard eligibility
- citizenship: Filipino citizen3
- residency/destination: Bonafide resident of Pasig City5
- education_level: TVET, College1
- eligible_year_levels: Entry level and ongoing TVET / College years1
- incoming_freshman_only: No1
- existing_college: Yes1
- graduate_students: No1
- current_enrollment: Enrolled or registered in a TVET center or college following ALS / OSL completion5
- academic: ALS Completion Certificate or Presentation Portfolio Assessment Scoring Sheet with Passed Grade / Form 137 / AF-5 Permanent Record5
- minimum_gwa: 75.00% (passing equivalent)1
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined annual gross family income not exceeding PHP 200,000.001
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Accredited TVET centers, SUCs, LUCs, or partner private institutions5
- courses: Technical-vocational skills courses and priority diploma degrees5
- sectoral/hidden: Out-of-school youth / ALS completer status verified by learning center5
- work_experience: None
- good_moral: Certificate of Good Moral Character8
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: One-Scholar-One-Family Policy applies6.

### Timing
- who: Out-of-school learners and ALS completers entering TVET or College5
- freshmen/soph/junior/senior/grad/reapply: : Yes1 | : Yes1 | : Yes1 | : Yes1 | : No1 | : Yes8
- window: August 1, 20251 → September 30, 20251 (Annual1; AY AY 2025–2026 / AY 2026–20271)

### Renewal
- maintain_gwa: 75.00% (passing average)1
- regular_load: Full load in TVET module or degree curriculum5
- no_failures: Zero dropped modules or failing subjects5
- return_service: False1

### Disqualifiers / affiliations
- Regular formal school graduates who are not out-of-school youth or ALS completers5.
- Income exceeding PHP 200,000.001.
- Non-residency in Pasig City5.

### Benefits (catalog)
- tuition: Full tuition coverage for accredited TVET / tertiary programs1
- stipend: PHP 2,500.00 per month1
- allowance: Total annual value of PHP 35,000.001

### Documents (operational hidden reqs)
- Printed Online Application Form5
- Barangay Certificate of Residency4
- ALS Completion Certificate / Presentation Portfolio Assessment Scoring Sheet with Passed Grade5
- Learner's Permanent Record (AF-5 or Form 137) from learning center5
- Proof of Income / Barangay Indigency Certificate4
- Proof of Enrollment in TVET / College4
- Certificate of Good Moral Character8

### Recommended schema
`json
{
  "education_level": [
    "TVET",
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
  "minimum_gwa": 75.0,
  "income_limit": 200000,
  "als_osl_status_required": true,
  "residency_restriction": "PASIG_CITY",
  "school_type": [
    "TVET_CENTER",
    "PUBLIC",
    "PRIVATE"
  ],
  "application_window": {
    "open": "2025-08-01",
    "close": "2025-09-30"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Misclassification of Student Origin: Regular continuous high school graduates who apply
- verification: Verified1 | confidence: 92/100

- CONTRADICTION/NOTE: entry GWA (75.00% (passing equivalent)1) vs renewal (75.00% (passing average)1)

---

## Pasig City Sangguniang Kabataan (SK) Endorsed Scholarship Program5 (ID: 94)

### Hard eligibility
- citizenship: Filipino citizen3
- residency/destination: Bonafide resident of Pasig City5
- education_level: College1
- eligible_year_levels: College Years 1, 2, 3, and 41
- incoming_freshman_only: No1
- existing_college: Yes1
- graduate_students: No1
- current_enrollment: Enrolled in a recognized college or university5
- academic: Minimum GWA of 82.00%1
- minimum_gwa: 82.00%1
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined family gross annual income not exceeding PHP 250,000.001
- age: Must meet SK youth age mandate (15–30 years old per SK Reform Act)5
- school/consortium: Recognized public or private HEIs5
- courses: NOT SPECIFIED IN OFFICIAL SOURCE
- sectoral/hidden: Formal SK Endorsement Resolution / Certification signed by the Barangay SK Chairperson4
- work_experience: None
- good_moral: Certificate of Good Moral Character8
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: One-Scholar-One-Family Policy applies6.

### Timing
- who: SK officials and SK-endorsed youth volunteers in Pasig City4
- freshmen/soph/junior/senior/grad/reapply: : Yes1 | : Yes1 | : Yes1 | : Yes1 | : No1 | : Yes8
- window: August 1, 20251 → August 20, 20261 (Annual1; AY AY 2025–2026 / AY 2026–20271)

### Renewal
- maintain_gwa: 82.00%1
- regular_load: Full semestral unit load5
- no_failures: Zero failing grades5
- return_service: True (mandatory participation in Barangay SK youth projects)1

### Disqualifiers / affiliations
- Lack of official endorsement from the local Barangay SK Council4.
- Exceeding the SK youth age threshold (30 years old)5.
- Income exceeding PHP 250,000.001.

### Benefits (catalog)
- tuition: False1
- stipend: PHP 1,500.00 per month1
- allowance: Total annual value of PHP 20,000.001

### Documents (operational hidden reqs)
- Printed Online Application Form5
- Official Barangay SK Endorsement Certificate / Resolution4
- Barangay Certificate of Residency4
- Proof of Enrollment in College4
- College TOR or SHS Card showing GWA 82.00%1
- Proof of Income / Indigency Certificate4
- Certificate of Good Moral Character8

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
  "minimum_gwa": 82.0,
  "income_limit": 250000,
  "sk_endorsement_required": true,
  "residency_restriction": "PASIG_CITY",
  "return_service_required": true,
  "school_type": [
    "PUBLIC",
    "PRIVATE"
  ],
  "application_window": {
    "open": "2025-08-01",
    "close": "2026-08-20"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Endorsement Verification: Applications submitted without a signed SK Endorsement
- verification: Verified1 | confidence: 94/100


---

## Scholarship on Tertiary Education Program – Financial Assistance (STEP-FA) Category A1 (ID: 101)

### Hard eligibility
- citizenship: Filipino citizen3
- residency/destination: Resident of Davao City13
- education_level: College1
- eligible_year_levels: Years 1, 2, 3, and 41
- incoming_freshman_only: No1
- existing_college: Yes12
- graduate_students: No1
- current_enrollment: Enrolled in a CHED-recognized HEI in Davao City13
- academic: GWA of at least 93.00% with no failing marks12
- minimum_gwa: 93.00%1
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: PHP 250,000.00 annual family income; verified indigent/below-average income by CSWDO1
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Recognized HEIs operating within Davao City13
- courses: CHED-prescribed priority courses13
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Certificate of Good Moral Character13
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Strict "One Child Per Family" rule13; candidate must not hold other government/private scholarship grants13.

### Timing
- who: Resident high-honor SHS graduates and ongoing college scholars12
- freshmen/soph/junior/senior/grad/reapply: : Yes12 | : Yes12 | : Yes12 | : Yes12 | : No1 | : Yes13
- window: April 1 annually12 → May 31 annually12 (Annual1; AY AY 2025–2026 / AY 2026–202712)

### Renewal
- maintain_gwa: 93.00%1
- regular_load: Full semestral unit load13
- no_failures: Zero failing or incomplete grades13
- return_service: False1

### Disqualifiers / affiliations
- GWA dropping below 93.00% (automatically downgrades scholar to Category B or C)12.
- Sibling already holding an EBSU grant13.
- Non-residency in Davao City13.

### Benefits (catalog)
- tuition: Full tuition coverage up to cap or direct cash grant1
- stipend: PHP 3,000.00 per month1
- allowance: PHP 25,000.00 per semester (PHP 50,000.00 per academic year)1

### Documents (operational hidden reqs)
- EBSU eScholar Application Form11
- Barangay Certificate of Residency12
- CSWDO Indigency Certificate / Eligibility Certification12
- Parents' ITR or Tax Exemption Certificate12
- SHS Grade 12 Card or College TOR showing GWA 93.00%12
- Certificate of Good Moral Character12
- Sworn affidavit of no sibling benefiting from EBSU13

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
  "minimum_gwa": 93.0,
  "income_limit": 250000,
  "residency_restriction": "DAVAO_CITY",
  "one_child_per_family_clause": true,
  "school_type": [
    "DAVAO_CITY_HEI"
  ],
  "application_window": {
    "open": "04-01",
    "close": "05-31"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Strict Grade Demotion: Scholars whose GWA falls to 92.50% must be dynamically
- verification: Verified1 | confidence: 90/100


---

## Scholarship on Tertiary Education Program – Financial Assistance (STEP-FA) Category C1 (ID: 102)

### Hard eligibility
- citizenship: Filipino citizen3
- residency/destination: Resident of Davao City13
- education_level: College1
- eligible_year_levels: Years 1, 2, 3, and 41
- incoming_freshman_only: No1
- existing_college: Yes12
- graduate_students: No1
- current_enrollment: Enrolled in a CHED-recognized HEI in Davao City13
- academic: GWA of 80.00% to 89.99% with no failing marks12
- minimum_gwa: 80.00%1
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined family annual gross income not exceeding PHP 180,000.001
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Recognized HEIs operating within Davao City13
- courses: CHED-prescribed priority degree courses13
- sectoral/hidden: Verified indigency status by CSWDO12
- work_experience: None
- good_moral: Certificate of Good Moral Character13
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Strict "One Child Per Family" rule13; candidate must not hold duplicate government/private scholarship grants13.

### Timing
- who: Indigent resident college students in Davao City12
- freshmen/soph/junior/senior/grad/reapply: : Yes12 | : Yes12 | : Yes12 | : Yes12 | : No1 | : Yes13
- window: April 1 annually12 → May 31 annually12 (Annual1; AY AY 2025–2026 / AY 2026–202712)

### Renewal
- maintain_gwa: 80.00%1
- regular_load: Full semestral unit load13
- no_failures: Zero failing marks13
- return_service: False1

### Disqualifiers / affiliations
- Family gross income exceeding PHP 180,000.001.
- Sibling already enjoying an EBSU scholarship13.
- Presence of failing or incomplete grades13.

### Benefits (catalog)
- tuition: False1
- stipend: PHP 1,000.00 per month1
- allowance: PHP 7,500.00 per semester (PHP 15,000.00 per academic year)1

### Documents (operational hidden reqs)
- EBSU eScholar Application Form11
- Certificate of Residency from Barangay12
- CSWDO Indigency Certificate12
- Parents' ITR or Tax Exemption Certificate ( PHP 180,000)1
- SHS Grade 12 Card or College TOR showing GWA 80%–89.99%12
- Certificate of Good Moral Character12
- Sworn affidavit of no sibling enjoying EBSU grants13

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
  "minimum_gwa": 80.0,
  "maximum_gwa_cap": 89.99,
  "income_limit": 180000,
  "residency_restriction": "DAVAO_CITY",
  "one_child_per_family_clause": true,
  "school_type": [
    "DAVAO_CITY_HEI"
  ],
  "application_window": {
    "open": "04-01",
    "close": "05-31"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Grade Upgrade Potential: Applicants attaining a GWA
- verification: Verified1 | confidence: None


---

## Medical and Law Education Assistance Program1 (ID: 103)

### Hard eligibility
- citizenship: Filipino citizen3
- residency/destination: Bonafide resident of Davao City13
- education_level: Graduate (Doctor of Medicine or Juris Doctor)1
- eligible_year_levels: Medical/Law Years 1, 2, 3, and 41
- incoming_freshman_only: No13
- existing_college: Yes (as professional medical/law students)13
- graduate_students: Yes1
- current_enrollment: Accepted or enrolled in a Davao City-based medical or law school13
- academic: Incoming 1st Year: Bachelor's degree average grade of at least 85.00% with no grade below 75.00% in any subject; Ongoing (2nd–4th Year): Average grade of at least 77.00% (or 85.00% per updated EBSU release) with no grade below 75.00% in preceding year level12
- minimum_gwa: 85.00%1
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined family gross annual income not exceeding PHP 500,000.00; Statement of Assets, Liabilities, and Net Worth (SALN) if parent is in government1
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Restricted exclusively to Davao City-based medical and law schools13
- courses: Doctor of Medicine, Juris Doctor (Law)11
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Certificate of Good Moral Character13
- health: Medical Certificate issued by a government hospital confirming physical and mental fitness13
- other_rules/conflicts: Certification from school confirming no other active scholarship grant13; Sworn statement of no parent or sibling as an active city scholar13; Mandatory return service obligation in Davao City1.

### Timing
- who: Bachelor's degree graduates entering 1st year medical/law school and ongoing medical/law students in Davao City12
- freshmen/soph/junior/senior/grad/reapply: : Yes (as incoming 1st year med/law students)13 | : Yes13 | : Yes13 | : Yes13 | : Yes (Bachelor's graduates entering professional school)13 | : Yes13
- window: April 1 annually12 → May 31 annually12 (Annual1; AY AY 2025–2026 / AY 2026–202712)

### Renewal
- maintain_gwa: 77.00%–85.00% depending on professional year level12
- regular_load: Full load in medical or law curriculum13
- no_failures: No grade below 75.00% in any subject12
- return_service: True (mandatory return service in Davao City public health facilities or legal offices)1

### Disqualifiers / affiliations
- Enrolling in medical or law schools outside Davao City13.
- Failing grade ( ) in any subject during undergraduate or professional study12.
- Dual scholarship holding13.

### Benefits (catalog)
- tuition: Full tuition and matriculation fee coverage at partner school1
- stipend: PHP 4,000.00 per month1
- allowance: Total annual value up to PHP 100,000.001

### Documents (operational hidden reqs)
- EBSU Med-Law Application Form11
- Official TOR with Certification of GWA 85.00%13
- NMAT Result (for Medical applicants) or PhilSAT / Law Admission Result13
- Certificate of Admission from Davao City-based Medical or Law school13
- Certificate of Residency from Barangay13
- Parents' ITR / SALN / CSWDO Certificate of Indigency13
- Certificate of Good Moral Character13
- Government Hospital Medical Certificate13
- Sworn statement of no sibling/parent as active city scholar13
- School Certification of no duplicate scholarship grant13

### Recommended schema
`json
{
  "education_level": [
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
  "minimum_gwa": 85.0,
  "income_limit": 500000,
  "priority_courses": [
    "DOCTOR_OF_MEDICINE",
    "JURIS_DOCTOR"
  ],
  "residency_restriction": "DAVAO_CITY",
  "return_service_required": true,
  "school_type": [
    "DAVAO_CITY_MED_LAW_SCHOOL"
  ],
  "partner_school_restricted": true,
  "application_window": {
    "open": "04-01",
    "close": "05-31"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● School Location Failure: Applicants admitted to medical/law schools outside Davao City
- verification: Verified1 | confidence: 98/100

- CONTRADICTION/NOTE: entry GWA (85.00%1) vs renewal (77.00%–85.00% depending on professional year level12)

---
