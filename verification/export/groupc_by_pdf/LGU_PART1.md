# DATABASE_V3_GROUPC_LGU_PART1.pdf — Implementation Details

Scholarships: 18

## Taguig City Lifeline Assistance for Neighbors In-Need (L.A.N.I.) Premier Scholarship1 (ID: 27)

### Hard eligibility
- citizenship: Filipino Citizen1
- residency/destination: Bona fide resident of Taguig City for at least three (3) years immediately preceding the application1.
- education_level: College / Undergraduate1.
- eligible_year_levels: 1, 2, 3, 4, 51.
- incoming_freshman_only: No1.
- existing_college: Yes1.
- graduate_students: No (Covered under LEAD track ID 97)1.
- current_enrollment: Enrolled or enrolling in the UP System (Luzon campuses) or CHED-certified Centers of Excellence in NCR1.
- academic: Senior High School or college academic performance meeting admission and retention cutoffs1.
- minimum_gwa: 90% (or equivalent 1.75 semestral weighted average)1.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Restricted to University of the Philippines System (Luzon campuses) and CHED-certified Centers of Excellence in NCR1.
- courses: NOT SPECIFIED IN OFFICIAL SOURCE
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Required (Certificate of Good Moral Character issued for the current school year)1.
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Must be a registered voter of Taguig City if 18 years or older, with at least one parent registered as a voter of Taguig City1.

### Timing
- who: Graduating SHS students and ongoing college students enrolled in qualifying COE institutions or UP Luzon campuses1.
- freshmen/soph/junior/senior/grad/reapply: : Yes1. | : Yes1. | : Yes1. | : Yes1. | : No1. | : Yes (Requires semestral renewal)1.
- window: Semestral schedule announced by the Taguig Scholarship Secretariat1. → Announced per semestral intake window1. (Semestral3.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Must maintain a General Weighted Average (GWA) not lower than 2.50 per semester5.
- regular_load: Enrolled in at least 15 academic units per semester or equivalent per trimester5.
- no_failures: Zero failing grades (5.0), unremoved 4.0, Incomplete (INC), or Dropped marks5.
- return_service: None mandated; scholars are encouraged to serve Taguig City1.

### Disqualifiers / affiliations
- Residing in Taguig City for less than three (3) consecutive years1.
- Non-voter status of applicant (if 18+) or parent in Taguig City1.
- Semester GWA dropping below 2.50 or receiving grades of 5.0, 4.0, INC, or Dropped5.
- Enrollment in non-COE institutions or non-UP Luzon campuses1.

### Benefits (catalog)
- tuition: Integrated into financial grant1.
- stipend: Integrated into semestral allowance1.
- allowance: PHP 40,000.00 to PHP 50,000.00 per school year (PHP 20,000.00 to PHP 25,000.00 per semester)1.

### Documents (operational hidden reqs)
- Completely filled-out LANI Scholarship Application Form with recent 2x2 pictures1.
- Registration Form or Official Receipt of Enrollment for the current semester1.
- Authenticated Copy of Grades/Transcript of Records for the preceding semester1.
- Certificate of Good Moral Character issued for the current academic year1.
- Voter's Certification issued by COMELEC (for applicant if >=18 years old, and parent)1.
- Certificate of Residency (minimum 3 years)1.
- Proof of Billing under the applicant's or parent's name1.

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
  "minimum_gwa": 90.0,
  "renewal_gwa": 81.0,
  "income_limit": null,
  "school_type": [
    "UP_SYSTEM_LUZON",
    "CHED_CENTER_OF_EXCELLENCE_NCR"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "residency_restriction": "TAGUIG_CITY_3_YEARS",
  "voter_requirement": "TAGUIG_REGISTERED_VOTER",
  "application_window": {
    "open": "semestral_notice",
    "close": "semestral_notice"
  },
  "deadline_type": "semestral",
  "cycle_type": "semester",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● COE Validation Risk: Automated matching engines may grant recommendations to
- verification: Verified1. | confidence: None

- CONTRADICTION/NOTE: entry GWA (90% (or equivalent 1.75 semestral weighted average)1.) vs renewal (Must maintain a General Weighted Average (GWA) not lower than 2.50 per semester5.)

---

## Taguig City L.A.N.I. Priority Courses and Skills Training Scholarship1 (ID: 28)

### Hard eligibility
- citizenship: Filipino Citizen1
- residency/destination: Bona fide resident of Taguig City for at least three (3) years immediately preceding the application1.
- education_level: College / Undergraduate / Professional (Law & Medicine)1.
- eligible_year_levels: 1, 2, 3, 4, 51.
- incoming_freshman_only: No1.
- existing_college: Yes1.
- graduate_students: No (Except Law and Medicine)1.
- current_enrollment: Must be enrolled in DOST-listed priority courses in DOST-listed schools, top-performing Law/Medicine schools as listed by PRC/CHED, or PWD applicants endorsed by PDAO1.
- academic: GWA of at least 82% or equivalent1.
- minimum_gwa: 82.00%1.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Restricted to DOST-listed institutions, top PRC/CHED performing law/medical schools, or PDAO-accredited institutions1.
- courses: DOST S&T Priority Courses, Law (Juris Doctor), Medicine (Doctor of Medicine)1.
- sectoral/hidden: PWD applicants must submit an official ID/endorsement from the Taguig Persons with Disabilities Affairs Office (PDAO)1.
- work_experience: None
- good_moral: Required1.
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Applicant and/or parent must be registered voters of Taguig City1.

### Timing
- who: High school graduates and current tertiary/professional students meeting course and institutional criteria1.
- freshmen/soph/junior/senior/grad/reapply: : Yes1. | : Yes1. | : Yes1. | : Yes1. | : No (Unless entering Law/Medicine)1. | : Yes1.
- window: Semestral schedule published by Taguig Secretariat1. → Semestral deadline1. (Semestral3.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Semestral GWA >= 2.50 (81%)5.
- regular_load: Minimum 15 credit units per semester5.
- no_failures: Zero failing or incomplete grades5.
- return_service: None1.

### Disqualifiers / affiliations
- Enrolling in non-priority courses outside DOST/Law/Medicine frameworks1.
- Failure to present valid Taguig PDAO endorsement for PWD track1.
- Accumulation of failing, incomplete, or dropped subjects5.

### Benefits (catalog)
- tuition: Direct grant allocation1.
- stipend: Integrated into allowance1.
- allowance: PHP 40,000.00 to PHP 50,000.00 per school year (PHP 20,000.00 to PHP 25,000.00 per semester)1.

### Documents (operational hidden reqs)
- Filled LANI Application Form1.
- Enrollment Certificate / Registration Form1.
- Preceding Term Grade Report / Transcript of Records1.
- Taguig PDAO ID and Endorsement (for PWD applicants)1.
- COMELEC Voter's Certification of applicant/parent1.
- Certificate of Good Moral Character1.

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
  "minimum_gwa": 82.0,
  "income_limit": null,
  "priority_courses": [
    "DOST_ST_PRIORITY",
    "LAW_JURIS_DOCTOR",
    "DOCTOR_OF_MEDICINE"
  ],
  "sectoral_restriction": "PWD_TAGUIG_PDAO_ENDORSED",
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "residency_restriction": "TAGUIG_CITY_3_YEARS",
  "application_window": {
    "open": "semestral_notice",
    "close": "semestral_notice"
  },
  "deadline_type": "semestral",
  "cycle_type": "semester",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Course Misclassification: System must strictly validate course codes against DOST
- verification: None | confidence: 95/1003.

- CONTRADICTION/NOTE: entry GWA (82.00%1.) vs renewal (Semestral GWA >= 2.50 (81%)5.)

---

## Taguig City L.A.N.I. State Universities and Colleges (SUC) / Local Colleges and Universities (LCU) Assistance Scholarship1 (ID: 29)

### Hard eligibility
- citizenship: Filipino Citizen1
- residency/destination: Bona fide resident of Taguig City for at least three (3) years1.
- education_level: College / Undergraduate1.
- eligible_year_levels: 1, 2, 3, 4, 51.
- incoming_freshman_only: No1.
- existing_college: Yes1.
- graduate_students: No1.
- current_enrollment: Must be enrolled in a State University or College (SUC) or Local College/University (LCU) in NCR1.
- academic: Passing academic standing with GWA >= 80%1.
- minimum_gwa: 80.00%1.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Restricted to SUCs and LCUs within NCR (e.g., PUP, PLM, UDM, TCU)1.
- courses: NOT SPECIFIED IN OFFICIAL SOURCE
- sectoral/hidden: Sub-categorized by high school background: Public HS graduates receive Basic+SUC/LCU grant; Private HS graduates receive SUC/LCU grant1.
- work_experience: None
- good_moral: Required1.
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Voter registration requirement for applicant/parent1.

### Timing
- who: Taguig resident public or private high school graduates enrolled in NCR SUCs or LCUs1.
- freshmen/soph/junior/senior/grad/reapply: : Yes1. | : Yes1. | : Yes1. | : Yes1. | : No1. | : Yes1.
- window: Announced semestrally1. → Semestral cutoff1. (Semestral3.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Semestral GWA >= 2.505.
- regular_load: Minimum 15 units per term5.
- no_failures: Zero failing grades5.
- return_service: None1.

### Disqualifiers / affiliations
- Transferring to a private college or university1.
- Dropping below minimum 15-unit term load5.

### Benefits (catalog)
- tuition: Direct financial grant1.
- stipend: Integrated into allowance1.
- allowance: Public HS Grads (Basic + SUC/LCU): PHP 15,000.00/year; Private HS Grads (SUC/LCU): PHP 10,000.00/year1.

### Documents (operational hidden reqs)
- Filled LANI Application Form1.
- Official Certificate of Registration from SUC/LCU1.
- High School Diploma / Form 138 (for new entry) or Term Grade Report1.
- Barangay Certificate of Residency1.
- COMELEC Voter's Certificate1.

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
  "income_limit": null,
  "school_type": [
    "SUC",
    "LUC"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "residency_restriction": "TAGUIG_CITY_3_YEARS",
  "application_window": {
    "open": "semestral_notice",
    "close": "semestral_notice"
  },
  "deadline_type": "semestral",
  "cycle_type": "semester",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● High School Origin Routing: The engine must differentiate between public and private
- verification: Verified1. | confidence: 95/1003.

- CONTRADICTION/NOTE: entry GWA (80.00%1.) vs renewal (Semestral GWA >= 2.505.)

---

## Taguig City L.A.N.I. Lifeline Bar and Board Review Assistance1 (ID: 30)

### Hard eligibility
- citizenship: Filipino Citizen1
- residency/destination: Bona fide resident of Taguig City for at least three (3) years immediately preceding application1.
- education_level: College Graduate / Post-Graduate Graduate1.
- eligible_year_levels: Graduated / Board Reviewee2.
- incoming_freshman_only: No2.
- existing_college: No2.
- graduate_students: Yes (Law/Medical/Graduate reviewees)2.
- current_enrollment: Must be officially registered in a recognized review center or scheduled for upcoming board/bar exam2.
- academic: Completion of tertiary degree program eligible for board/bar examination2.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Graduation from a CHED/PRC-recognized college or university1.
- courses: Any course requiring PRC Board Licensure or Supreme Court Bar Examination2.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Required1.
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Must submit PRC Notice of Admission (NOA) or Supreme Court permit2.

### Timing
- who: College/professional graduates preparing for upcoming licensure examinations2.
- freshmen/soph/junior/senior/grad/reapply: : No2. | : No2. | : No2. | : No2. | : Yes (Primary target cohort)2. | : No (One-time assistance grant per exam)2.
- window: Announced prior to major national board/bar exam cycles2. → Specified per review disbursement cycle2. (Rolling / Exam-based2.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Non-renewable (One-time grant)2.
- regular_load: N/A2.
- no_failures: N/A2.
- return_service: None; commitment to serve Taguig City1.

### Disqualifiers / affiliations
- Enrolled ongoing undergraduate students2.
- Failure to present official PRC Notice of Admission or Supreme Court permit2.
- Prior enjoyment of Taguig Bar/Board assistance for the same exam type2.

### Benefits (catalog)
- tuition: Review center fee support2.
- stipend: None2.
- allowance: One-time grant: PHP 20,000.00 for Bar and Physician Licensure Exams; PHP 15,000.00 for other PRC Board Exams2.

### Documents (operational hidden reqs)
- Filled Review Assistance Application Form2.
- PRC Notice of Admission (NOA) or Bar Exam Registration2.
- Two (2) valid government-issued IDs2.
- Transcript of Records showing degree completion1.
- Taguig COMELEC Voter's Certification1.
- Certificate of Residency1.

### Recommended schema
`json
{
  "education_level": [
    "Graduate"
  ],
  "eligible_year_levels": [
    5,
    6
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": false,
  "minimum_gwa": null,
  "income_limit": null,
  "target_cohort": "LICENSURE_EXAM_REVIEWEES",
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "residency_restriction": "TAGUIG_CITY_3_YEARS",
  "application_window": {
    "open": "rolling_exam_based",
    "close": "rolling_exam_based"
  },
  "deadline_type": "rolling",
  "cycle_type": "exam_cycle",
  "renewable": false,
  "first_time_only": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Status Mismatch: Displaying this scholarship to current undergraduate students will
- verification: Verified1. | confidence: 95/1003.

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE) vs renewal (Non-renewable (One-time grant)2.)

---

## Makati City College Scholarship Program – SUC and Priority Courses Tracks6 (ID: 31)

### Hard eligibility
- citizenship: Filipino Citizen6
- residency/destination: Bona fide resident of Makati City6.
- education_level: College / Undergraduate3.
- eligible_year_levels: 1 (Incoming Freshmen)6.
- incoming_freshman_only: Yes6.
- existing_college: Ineligible for initial entry6.
- graduate_students: Ineligible6.
- current_enrollment: Enrolled or accepted as an incoming 1st-year student in any Metro Manila SUC (other than UMak) or DOST-accredited priority course6.
- academic: Fresh senior high school graduate belonging to the Top 10 Percent of the graduating class6.
- minimum_gwa: Minimum GWA of 1.50 (or equivalent 88–90% scale)3.
- alt_class_rank: Belong to the Top 10% of the SHS graduating class6.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Metro Manila SUCs (excluding UMak) or DOST-accredited schools6.
- courses: DOST-listed priority courses6.
- sectoral/hidden: PWDs enrolled in top performing CHED/PRC schools qualify under the PHP 40,000 track6.
- work_experience: None
- good_moral: Required6.
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Must sign a mandatory Service Agreement committing to serve with the Makati City Government upon graduation6.

### Timing
- who: Graduating SHS students from Makati public schools belonging to the top 10% of their class6.
- freshmen/soph/junior/senior/grad/reapply: : Yes (at initial college entry)6. | : No6. | : No6. | : No6. | : No6. | : No6.
- window: Annual cycle announced following SHS graduation6. → Specified per annual intake notice6. (Fixed / Annual3.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Must maintain a GWA of at least 1.50 (or equivalent) each term6.
- regular_load: Full academic credit load required6.
- no_failures: No grade of 5.0, 4.0, Incomplete, or Dropped subjects6.
- return_service: Mandatory service agreement to serve with the Makati City Government after graduation6.

### Disqualifiers / affiliations
- Failing grades (5.0), unremoved 4.0, or incomplete marks6.
- Refusal to sign or fulfill the mandatory Makati City Government service agreement6.
- Non-residency in Makati City6.

### Benefits (catalog)
- tuition: Covered per institutional billing6.
- stipend: Integrated into total grant6.
- allowance: SUC Track: PHP 20,000.00 total benefit per school year; DOST Priority Courses / PWD Track: PHP 40,000.00 total benefit per school year6.

### Documents (operational hidden reqs)
- Official Application Form6.
- SHS Form 138 showing GWA and Certification of Top 10% Class Rank signed by Principal6.
- Proof of Residency in Makati City (Barangay Certificate / Voter's ID)6.
- Certificate of Enrollment / Admission Notice from Metro Manila SUC or DOST-accredited HEI6.
- Parents' Income Tax Return or Certificate of Indigency6.
- Signed Service Contract Agreement6.

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
  "minimum_gwa": 88.0,
  "rank_cutoff_alternative": 10,
  "income_limit": null,
  "school_type": [
    "SUC"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "residency_restriction": "MAKATI_CITY_RESIDENT",
  "return_service_required": true,
  "application_window": {
    "open": "annual_notice",
    "close": "annual_notice"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Service Obligation Friction: Candidates seeking unencumbered grants may reject the
- verification: Verified3. | confidence: 95/1003.

- CONTRADICTION/NOTE: entry GWA (Minimum GWA of 1.50 (or equivalent 88–90% scale)3.) vs renewal (Must maintain a GWA of at least 1.50 (or equivalent) each term6.)

---

## University of Makati (UMak) Token Fee Exemption Program7 (ID: 32)

### Hard eligibility
- citizenship: Filipino Citizen7
- residency/destination: Priority given to bona fide Makati City residents (determined via UMak residency verification)10. Non-Makati residents eligible for specific honor tracks7.
- education_level: College / Undergraduate3.
- eligible_year_levels: 1, 2, 3, 4, 57.
- incoming_freshman_only: No (Entrance exemption is freshman-only; academic retention applies to all years)7.
- existing_college: Yes7.
- graduate_students: Restricted (Separate graduate fee schedules apply)10.
- current_enrollment: Must be officially admitted and enrolled at the University of Makati7.
- academic: Entrance exemption requires SHS graduation with "Highest Honor" (GWA 98–100) or "High Honor" (GWA 95–97)7. Continuing exemption governed by semestral GWA cutoffs8.
- minimum_gwa: Entrance cutoff: 95.00% (High Honor) or 98.00% (Highest Honor)7. Renewal cutoff: GWA <= 2.50 (If GWA is 2.75–3.00, student pays PHP 2,000/unit)11.
- alt_class_rank: Senior High School Honor Roll certification7.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Restricted strictly to students enrolled at the University of Makati7.
- courses: Any undergraduate degree program offered by UMak7.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Required (Good disciplinary standing)7.
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Governed by UMak retention policies; unofficially dropped subjects cause forfeiture7.

### Timing
- who: Officially enrolled UMak undergraduate students7.
- freshmen/soph/junior/senior/grad/reapply: : Yes7. | : Yes7. | : Yes7. | : Yes7. | : No7. | : Yes (Automated evaluation or semestral application on
- window: Scheduled per semester on the OLEA system (e.g., January intake for 2nd Sem)7. → Specified per term registration schedule12. (Semestral3.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Must maintain prescribed GWA per semester (GWA <= 2.50)8.
- regular_load: Full academic load carried each term7.
- no_failures: Zero failing grades or unofficially dropped subjects7.
- return_service: None7.

### Disqualifiers / affiliations
- GWA dropping between 2.75 and 3.00 results in loss of exemption and triggers a PHP 2,000 per unit tuition fee11.
- Accumulation of unofficially dropped (UD) courses exceeding institutional limits7.

### Benefits (catalog)
- tuition: 100% exemption from tuition/token fees for qualified honor entrants and high-performing scholars7.
- stipend: NOT SPECIFIED IN OFFICIAL SOURCE
- allowance: Token exemption value equivalent to PHP 1,000.00 – PHP 5,000.00 per semester depending on residency tier3.

### Documents (operational hidden reqs)
- SHS Grade 12 Report Card (1st and 2nd Semesters)7.
- Certificate of Highest Honor (GWA 98–100) or High Honor (GWA 95–97) signed by Principal7.
- Voter's Certification of applicant or parent (for Makati resident tagging)10.
- Official UMak Grade Report for preceding semester (for continuing applicants)7.
- Online application submission via UMak OLEA account7.

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
  "minimum_gwa": 95.0,
  "renewal_gwa": 81.0,
  "income_limit": null,
  "school_type": [
    "UMAK_ONLY"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "OLEA_semestral_dates",
    "close": "OLEA_semestral_dates"
  },
  "deadline_type": "semestral",
  "cycle_type": "semester",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Grade Penalty Threshold: The system must enforce logic checking for GWAs between
- verification: Verified3. | confidence: None

- CONTRADICTION/NOTE: entry GWA (Entrance cutoff: 95.00% (High Honor) or 98.00% (Highest Honor)7. Renewal cutoff: GWA <= 2.50 (If GWA is 2.75–3.00, student pays PHP 2,000/unit)11.) vs renewal (Must maintain prescribed GWA per semester (GWA <= 2.50)8.)

---

## Valenzuela City Dr. Pio Valenzuela Scholarship Program13 (ID: 33)

### Hard eligibility
- citizenship: Natural-born Filipino Citizen13.
- residency/destination: Long-term resident of Valenzuela City (at least four consecutive years of residency immediately prior to application)13.
- education_level: College / Undergraduate (Incoming Freshmen)13.
- eligible_year_levels: 1 (Incoming First-Year College Students)13.
- incoming_freshman_only: Yes13.
- existing_college: Ineligible for new entry13.
- graduate_students: Ineligible13.
- current_enrollment: Enrolled or applying for admission in any CHED-accredited college or university13.
- academic: SHS GWA of at least 85.00% with no subject grade below 85% in Grade 11 (1st and 2nd sem) and Grade 12 (1st sem)13. Must pass the scholarship qualifying examination13.
- minimum_gwa: 85.00% (with zero subject grades below 85%)13.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined gross annual income of employed parents must NOT exceed PHP 120,000.0013.
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Any public or private HEI accredited by the Commission on Higher Education (CHED)13.
- courses: Open to all baccalaureate degree programs under GAS, STEM, HUMSS, and ABM strands17.
- sectoral/hidden: Underprivileged/low-income family status verified via BIR ITR or Barangay Certificate of Indigency13.
- work_experience: None
- good_moral: Required (Certificate of Good Moral Character)13.
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Must be a graduate of a public or private senior high school in Valenzuela City13. Voter's certificate of parent/applicant required16.

### Timing
- who: Graduating Grade 12 students and SHS graduates residing in Valenzuela City for >= 4 years13.
- freshmen/soph/junior/senior/grad/reapply: : Yes (prior to/at starting college intake)13. | : No13. | : No13. | : No13. | : No13. | : No13.
- window: January 3 annually13. → Late February / Mid-March (e.g., March 20)13. (Fixed / Annual3.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Must maintain a semestral GWA of at least 2.00 (85%)13.
- regular_load: Full-time credit enrollment13.
- no_failures: Individual subject grades must not fall below 2.2513.
- return_service: None13.

### Disqualifiers / affiliations
- Parents' annual gross income exceeding PHP 120,000.0013.
- Subject grade below 85% in SHS or below 2.25 in college13.
- Residency in Valenzuela City less than four (4) consecutive years13.
- Non-natural-born citizenship13.

### Benefits (catalog)
- tuition: Educational grant allocation13.
- stipend: Integrated into annual grant13.
- allowance: PHP 30,000.00 per academic year (PHP 15,000.00 per semester)13.

### Documents (operational hidden reqs)
- Accomplished Dr. Pio Valenzuela Scholarship Application Form14.
- Certified True Copy of Grade 11 Report Card (1st & 2nd Semesters) and Grade 12 Report Card (1st Semester) showing GWA >= 85% and no grade below 8516.
- Proof of Income: Certified True Copy of 2024 ITR (Form 2316) showing annual gross income <= PHP 120,000.00, or Joint Affidavit and Certificate of Non-Filing of ITR if unemployed16.
- Barangay Certificate of Residency and Indigency of parents16.
- PSA Certified Birth Certificate of applicant16.
- Certificate of Good Moral Character16.
- Voter's Certificate of registered parent or guardian16.
- Photo of actual street residence of applicant16.

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
  "minimum_gwa": 85.0,
  "renewal_gwa": 85.0,
  "income_limit": 120000,
  "school_type": [
    "CHED_ACCREDITED_HEI"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino (Natural-born)",
  "residency_restriction": "VALENZUELA_CITY_4_YEARS",
  "application_window": {
    "open": "01-03",
    "close": "03-20"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Strict Income Disqualification: The PHP 120,000 annual income threshold is exceptionally
- verification: None | confidence: 95/1003.

- CONTRADICTION/NOTE: entry GWA (85.00% (with zero subject grades below 85%)13.) vs renewal (Must maintain a semestral GWA of at least 2.00 (85%)13.)

---

## NavotaAs Academic College Scholarship Program19 (ID: 34)

### Hard eligibility
- citizenship: Filipino Citizen19
- residency/destination: Bona fide resident of Navotas City19.
- education_level: College / Undergraduate3.
- eligible_year_levels: 1, 2, 3, 4, 53.
- incoming_freshman_only: No3.
- existing_college: Yes3.
- graduate_students: No3.
- current_enrollment: Enrolled or accepted in a recognized higher education institution19.
- academic: Outstanding academic standing with SHS or college GWA of at least 88.00%3.
- minimum_gwa: 88.00%3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Recognized public or private colleges and universities19.
- courses: NOT SPECIFIED IN OFFICIAL SOURCE
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Required19.
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Resident voter requirements apply19.

### Timing
- who: Qualified resident college students and incoming freshmen3.
- freshmen/soph/junior/senior/grad/reapply: : Yes3. | : Yes3. | : Yes3. | : Yes3. | : No3. | : Yes3.
- window: Annual application schedule published by Navotas City Hall19. → Announced per annual cycle19. (Fixed / Annual3.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Maintain required academic average (>= 88.00%) per term3.
- regular_load: Full credit load per term19.
- no_failures: Zero failing grades19.
- return_service: None3.

### Disqualifiers / affiliations
- Loss of Navotas residency status19.
- Failure to maintain required 88.00% GWA3.

### Benefits (catalog)
- tuition: Full tuition fee coverage3.
- stipend: PHP 2,200.00 per month3.
- allowance: Integrated into monthly stipend package3.

### Documents (operational hidden reqs)
- NavotaAs Application Form19.
- Proof of Residency in Navotas City19.
- Report Card / TOR showing GWA >= 88.00%3.
- Certificate of Enrollment19.
- Certificate of Good Moral Character19.

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
  "minimum_gwa": 88.0,
  "income_limit": null,
  "school_type": [
    "RECOGNIZED_HEI"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "residency_restriction": "NAVOTAS_CITY_RESIDENT",
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
- ● High Total Value Perception: Live DB lists total_value: 262000 reflecting 4-year cumulative
- verification: Verified3. | confidence: 98/1003.

- CONTRADICTION/NOTE: entry GWA (88.00%3.) vs renewal (Maintain required academic average (>= 88.00%) per term3.)

---

## Marikina City Medical Scholarship Program3 (ID: 35)

### Hard eligibility
- citizenship: Filipino Citizen3
- residency/destination: Bona fide resident of Marikina City3.
- education_level: Graduate (Doctor of Medicine)3.
- eligible_year_levels: 1, 2, 3, 4 (Medical School Years)3.
- incoming_freshman_only: No3.
- existing_college: Eligible as medical students3.
- graduate_students: Yes (Restricted strictly to Doctor of Medicine degree)3.
- current_enrollment: Accepted or enrolled in a recognized Doctor of Medicine program3.
- academic: Bachelor's degree completion and NMAT score meeting medical school entry standards; GWA >= 85.00%3.
- minimum_gwa: 85.00%3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined annual gross family income must not exceed PHP 600,000.003.
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Accredited medical schools3.
- courses: Doctor of Medicine3.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Required3.
- health: Physically and mentally fit3.
- other_rules/conflicts: Mandatory return service obligation in Marikina City public hospitals/health centers upon passing the Physician Licensure Examination3.

### Timing
- who: Incoming and ongoing medical students residing in Marikina City3.
- freshmen/soph/junior/senior/grad/reapply: : Yes (1st year medical students)3. | : Yes (2nd year medical students)3. | : Yes (3rd year medical students)3. | : Yes (4th year medical students)3. | : Yes (Bachelor's graduates entering medical school)3. | : Yes3.
- window: Summer intake period prior to medical academic year3. → Announced per annual notice3. (Fixed / Annual3.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Maintain passing GWA prescribed by medical school and scholarship rules3.
- regular_load: Full-time enrollment in medical curriculum3.
- no_failures: Zero failing grades in medical subjects3.
- return_service: Mandatory return service in Marikina City public health facilities3.

### Disqualifiers / affiliations
- Family income exceeding PHP 600,000.003.
- Failure to fulfill return service contract3.
- Academic failure or dismissal from medical school3.

### Benefits (catalog)
- tuition: Full tuition and matriculation fee coverage3.
- stipend: PHP 4,000.00 per month3.
- allowance: Integrated into stipend package3.

### Documents (operational hidden reqs)
- Application Form3.
- Proof of Marikina Residency3.
- Transcript of Records (TOR) of completed Bachelor's degree (GWA >= 85%)3.
- NMAT Score Report3.
- Admission / Enrollment Certificate from accredited Medical School3.
- Income Tax Return of parents (income <= PHP 600,000)3.
- Signed Return Service Contract3.

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
  "income_limit": 600000,
  "priority_courses": [
    "DOCTOR_OF_MEDICINE"
  ],
  "school_type": [
    "ACCREDITED_MEDICAL_SCHOOLS"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "residency_restriction": "MARIKINA_CITY_RESIDENT",
  "return_service_required": true,
  "application_window": {
    "open": "annual_notice",
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
- ● Pre-Med Candidate Confusion: Automated rules must block undergraduate pre-med
- verification: Verified3. | confidence: 92/1003.

- CONTRADICTION/NOTE: entry GWA (85.00%3.) vs renewal (Maintain passing GWA prescribed by medical school and scholarship rules3.)

---

## Muntinlupa Most Outstanding Students (10 MOST) Academic Scholarship20 (ID: 47)

### Hard eligibility
- citizenship: Filipino Citizen25
- residency/destination: Bona fide resident of Muntinlupa City holding a valid Muntinlupa Care Card21.
- education_level: College / Undergraduate3.
- eligible_year_levels: 1 (Incoming Freshmen)3.
- incoming_freshman_only: Yes3.
- existing_college: Ineligible for initial entry21.
- graduate_students: Ineligible21.
- current_enrollment: Must be admitted/enrolled in UP (Luzon campuses), DOST priority programs, or CHED Centers of Excellence21.
- academic: Yearly 10 MOST Awardees or top-ranked public SHS graduates with GWA >= 90.00%3.
- minimum_gwa: 90.00%3.
- alt_class_rank: Designated 10 MOST Awardee status21.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: UP Luzon Campuses, DOST Priority Program Schools, CHED Centers of Excellence21.
- courses: DOST Priority Programs, CHED COE Programs21.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Required (Certificate of Good Moral)21.
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Must possess an active Muntinlupa Care Card number21.

### Timing
- who: 10 MOST Awardees and qualified top public SHS graduates in Muntinlupa21.
- freshmen/soph/junior/senior/grad/reapply: : Yes (at initial college entry)21. | : No21. | : No21. | : No21. | : No21. | : No21.
- window: Mid-year cycle following annual MOST pre-awarding events21. → Announced on MSD portal25. (Fixed / Annual3.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Maintain required academic standing per semester21.
- regular_load: Full-time credit enrollment21.
- no_failures: Zero failing grades21.
- return_service: Mandatory scheduling of service obligation via MSD portal20.

### Disqualifiers / affiliations
- Enrolling in non-COE private institutions outside UP/DOST frameworks21.
- Lack of valid Muntinlupa Care Card21.
- Non-compliance with mandatory MSD service obligation20.

### Benefits (catalog)
- tuition: Full or partial tuition grant per university billing3.
- stipend: PHP 5,000.00 per month3.
- allowance: PHP 130,000.00 maximum total financial package per school year3.

### Documents (operational hidden reqs)
- Duly accomplished MSD Application Form21.
- Muntinlupa Care Card or Official Receipt with Care Card Number21.
- SHS Form 138 showing GWA >= 90.00%3.
- Certificate of Good Moral Character21.
- Voter's ID or Voter's Certification of applicant or parents21.
- Certificate of Enrollment from UP Luzon, DOST school, or CHED COE21.
- 2x2 ID Picture21.

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
  "minimum_gwa": 90.0,
  "income_limit": null,
  "school_type": [
    "UP_SYSTEM_LUZON",
    "DOST_PRIORITY_SCHOOLS",
    "CHED_CENTER_OF_EXCELLENCE"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "residency_restriction": "MUNTINLUPA_CARE_CARD_HOLDER",
  "return_service_required": true,
  "application_window": {
    "open": "annual_notice",
    "close": "annual_notice"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Care Card Dependency: Automated recommendation logic must check if the applicant
- verification: Verified3. | confidence: 90/1003.

- CONTRADICTION/NOTE: entry GWA (90.00%3.) vs renewal (Maintain required academic standing per semester21.)

---

## Muntinlupa Continuing Assistance for Reintegrating Students (CARES) Financial Assistance Program21 (ID: 48)

### Hard eligibility
- citizenship: Filipino Citizen25
- residency/destination: Bona fide resident of Muntinlupa City holding an active Muntinlupa Care Card21.
- education_level: College / Undergraduate3.
- eligible_year_levels: 1, 2, 3, 4, 53.
- incoming_freshman_only: No21.
- existing_college: Yes21.
- graduate_students: Ineligible21.
- current_enrollment: Must be enrolled in any college or university within Luzon25.
- academic: Must maintain the required number of units and General Weighted Average (GWA) set by the MSD (GWA >= 80.00%)3.
- minimum_gwa: 80.00%3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Any recognized public or private college or university in Luzon25.
- courses: NOT SPECIFIED IN OFFICIAL SOURCE
- sectoral/hidden: Caters to recipients of Basic Scholarship in their continuing college studies26. Categorized into three (3) brackets26.
- work_experience: None
- good_moral: Required21.
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Requires Muntinlupa Care Card registration21.

### Timing
- who: Incoming freshmen and existing college students in Luzon colleges/universities21.
- freshmen/soph/junior/senior/grad/reapply: : Yes21. | : Yes21. | : Yes21. | : Yes21. | : No21. | : Yes21.
- window: Semestral schedule posted on MSD portal/Facebook page21. → Semestral cutoff27. (Semestral3.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Maintain GWA set by MSD (GWA <= 2.50 / 80%)26.
- regular_load: Enrolled in prescribed credit units per semester26.
- no_failures: Zero failing grades23.
- return_service: Scheduling of service obligation via MSD online portal20.

### Disqualifiers / affiliations
- Enrolling in institutions outside Luzon25.
- Failure to maintain required MSD GWA or term credit units26.
- Lack of valid Muntinlupa Care Card registration21.

### Benefits (catalog)
- tuition: Direct stipend assistance26.
- stipend: PHP 1,000.00 per month3.
- allowance: PHP 10,000.00 per academic year (PHP 5,000.00 per semester)3.

### Documents (operational hidden reqs)
- Duly accomplished CARES Application Form21.
- Muntinlupa Care Card or Official Receipt with Care Card Number21.
- Current School ID21.
- Certificate of Enrollment for the current semester21.
- Certified Copy of Previous Semester Grades21.
- Curriculum / Prospectus (if applicable)23.

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
  "income_limit": null,
  "school_type": [
    "RECOGNIZED_HEI_IN_LUZON"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "residency_restriction": "MUNTINLUPA_CARE_CARD_HOLDER",
  "return_service_required": true,
  "application_window": {
    "open": "semestral_notice",
    "close": "semestral_notice"
  },
  "deadline_type": "semestral",
  "cycle_type": "semester",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Geographic Filter Mismatch: Filtering must enforce HEI location IN ('Luzon') to prevent
- verification: Verified3. | confidence: 96/1003.

- CONTRADICTION/NOTE: entry GWA (80.00%3.) vs renewal (Maintain GWA set by MSD (GWA <= 2.50 / 80%)26.)

---

## Parañaque City Tertiary Education Financial Assistance Program3 (ID: 50)

### Hard eligibility
- citizenship: Filipino Citizen3
- residency/destination: Bona fide resident of Parañaque City3.
- education_level: College / Undergraduate3.
- eligible_year_levels: 1, 2, 3, 4, 53.
- incoming_freshman_only: No3.
- existing_college: Yes3.
- graduate_students: No3.
- current_enrollment: Must be enrolled in a CHED-recognized college or university3.
- academic: Minimum GWA of 80.00%3.
- minimum_gwa: 80.00%3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined annual gross family income must not exceed PHP 300,000.003.
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: CHED-recognized colleges and universities3.
- courses: NOT SPECIFIED IN OFFICIAL SOURCE
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Required3.
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Voter's certification of applicant or parent in Parañaque City required3.

### Timing
- who: Qualified Parañaque resident college students3.
- freshmen/soph/junior/senior/grad/reapply: : Yes3. | : Yes3. | : Yes3. | : Yes3. | : No3. | : Yes3.
- window: Semestral schedule published by Parañaque City Government3. → Specified per term (e.g., August 20 for AY 2026 intake)3. (Semestral3.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Maintain semestral GWA of at least 80.00%3.
- regular_load: Full-time credit enrollment3.
- no_failures: Zero failing grades3.
- return_service: None3.

### Disqualifiers / affiliations
- Family income exceeding PHP 300,000.003.
- Non-residency in Parañaque City3.
- Failure to maintain required 80.00% GWA3.

### Benefits (catalog)
- tuition: Direct cash assistance allocation3.
- stipend: NOT SPECIFIED IN OFFICIAL SOURCE
- allowance: PHP 12,000.00 per academic year (PHP 6,000.00 per semester)3.

### Documents (operational hidden reqs)
- Application Form3.
- Certificate of Enrollment / Registration Form3.
- Preceding Term Grade Report (GWA >= 80.00%)3.
- Barangay Certificate of Residency in Parañaque City3.
- Parents' Income Tax Return or Certificate of Indigency3.
- Parañaque COMELEC Voter's Certificate3.

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
  "income_limit": 300000,
  "school_type": [
    "CHED_RECOGNIZED_HEI"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "residency_restriction": "PARANAQUE_CITY_RESIDENT",
  "application_window": {
    "open": "08-01",
    "close": "08-20"
  },
  "deadline_type": "exact",
  "cycle_type": "semester",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Short Application Windows: Application windows are precise and time-sensitive; the
- verification: Verified3. | confidence: 95/1003.

- CONTRADICTION/NOTE: entry GWA (80.00%3.) vs renewal (Maintain semestral GWA of at least 80.00%3.)

---

## Taguig City L.A.N.I. Full Scholarship Track1 (ID: 95)

### Hard eligibility
- citizenship: Filipino Citizen1
- residency/destination: Bona fide resident of Taguig City for at least three (3) years1.
- education_level: College / Undergraduate / Professional1.
- eligible_year_levels: 1, 2, 3, 4, 51.
- incoming_freshman_only: No1.
- existing_college: Yes1.
- graduate_students: No (Except Law and Medicine)1.
- current_enrollment: Enrolled in any recognized college/university for Top 10 public SHS graduates, or DOST priority/law/medicine schools1.
- academic: GWA of at least 85.00% or designated Top 10 class rank1.
- minimum_gwa: 85.00%1.
- alt_class_rank: Top 10 graduates of public high schools in Taguig1.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Unrestricted for Top 10 public SHS grads; DOST/PRC/CHED accredited for priority tracks1.
- courses: Unrestricted for Top 10 public SHS grads; DOST S&T, Law, and Medicine for other applicants1.
- sectoral/hidden: PDAO endorsement required for PWD applicants1.
- work_experience: None
- good_moral: Required1.
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Voter registration requirement for applicant/parent1.

### Timing
- who: Top 10 graduates of Taguig public high schools and qualified priority course students1.
- freshmen/soph/junior/senior/grad/reapply: : Yes1. | : Yes1. | : Yes1. | : Yes1. | : No1. | : Yes1.
- window: Semestral publication1. → Semestral deadline1. (Semestral3.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Semestral GWA >= 2.505.
- regular_load: Minimum 15 credit units5.
- no_failures: Zero failing grades5.
- return_service: None1.

### Disqualifiers / affiliations
- Loss of 15-unit term load5.
- Accumulation of failing or incomplete marks5.

### Benefits (catalog)
- tuition: Direct financial grant1.
- stipend: Integrated into allowance1.
- allowance: PHP 40,000.00 to PHP 50,000.00 per school year (PHP 20,000.00 to PHP 25,000.00 per semester)1.

### Documents (operational hidden reqs)
- Filled LANI Application Form1.
- Principal's Certification of Top 10 Class Rank (for public SHS grads)1.
- Grade Report showing GWA >= 85.00%1.
- Taguig COMELEC Voter's Certificate1.
- Certificate of Enrollment1.

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
  "rank_cutoff_alternative": 10,
  "income_limit": null,
  "school_type": [
    "RECOGNIZED_HEI"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "residency_restriction": "TAGUIG_CITY_3_YEARS",
  "application_window": {
    "open": "semestral_notice",
    "close": "semestral_notice"
  },
  "deadline_type": "semestral",
  "cycle_type": "semester",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Overriding School Restrictions: Matching engine must override school/course restrictions
- verification: Verified1. | confidence: 95/1003.

- CONTRADICTION/NOTE: entry GWA (85.00%1.) vs renewal (Semestral GWA >= 2.505.)

---

## Taguig City L.A.N.I. Basic Scholarship Track1 (ID: 96)

### Hard eligibility
- citizenship: Filipino Citizen1
- residency/destination: Bona fide resident of Taguig City for at least three (3) years1.
- education_level: College / Undergraduate1.
- eligible_year_levels: 1, 2, 3, 4, 51.
- incoming_freshman_only: No1.
- existing_college: Yes1.
- graduate_students: No1.
- current_enrollment: Enrolled in any private college or university in NCR (not enrolled in an SUC or LUC)1.
- academic: Passing academic standing with GWA >= 78.00%1.
- minimum_gwa: 78.00%1.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Private higher education institutions in NCR (Excludes SUCs and LUCs)1.
- courses: NOT SPECIFIED IN OFFICIAL SOURCE
- sectoral/hidden: Must be a graduate of a public high school in Taguig City or nearby NCR municipalities/cities1.
- work_experience: None
- good_moral: Required1.
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Voter registration requirement for applicant/parent1.

### Timing
- who: Taguig resident public high school graduates enrolled in private colleges in NCR1.
- freshmen/soph/junior/senior/grad/reapply: : Yes1. | : Yes1. | : Yes1. | : Yes1. | : No1. | : Yes1.
- window: Semestral schedule1. → Semestral cutoff1. (Semestral3.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Semestral GWA >= 2.505.
- regular_load: Minimum 15 credit units5.
- no_failures: Zero failing grades5.
- return_service: None1.

### Disqualifiers / affiliations
- Enrolling in an SUC or LUC (must transfer to SUC/LCU assistance track ID 29)1.
- Graduation from a private high school1.

### Benefits (catalog)
- tuition: Direct grant allocation1.
- stipend: Integrated into allowance1.
- allowance: PHP 10,000.00 per school year (PHP 5,000.00 per semester)1.

### Documents (operational hidden reqs)
- Filled LANI Application Form1.
- Public SHS Diploma / Form 1381.
- Certificate of Enrollment from private HEI in NCR1.
- Preceding Semester Grade Report (GWA >= 78.00%)1.
- Taguig COMELEC Voter's Certificate1.

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
  "minimum_gwa": 78.0,
  "income_limit": null,
  "school_type": [
    "PRIVATE_HEI_NCR"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "residency_restriction": "TAGUIG_CITY_3_YEARS",
  "application_window": {
    "open": "semestral_notice",
    "close": "semestral_notice"
  },
  "deadline_type": "semestral",
  "cycle_type": "semester",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● High School Origin Routing: System must verify user.high_school_type == 'Public' and
- verification: None | confidence: None

- CONTRADICTION/NOTE: entry GWA (78.00%1.) vs renewal (Semestral GWA >= 2.505.)

---

## Taguig City L.A.N.I. Leadership and Educators Advancement and Development (LEAD) Graduate Scholarship1 (ID: 97)

### Hard eligibility
- citizenship: Filipino Citizen1
- residency/destination: Bona fide resident of Taguig City for at least three (3) years immediately preceding application1.
- education_level: Graduate (Master's or Doctoral Degree)1.
- eligible_year_levels: 1, 2, 3 (Postgraduate Years)1.
- incoming_freshman_only: No1.
- existing_college: No (Restricted to post-baccalaureate graduate students)1.
- graduate_students: Yes (Primary target cohort)1.
- current_enrollment: Enrolled in a Master's or Doctoral program with courses aligned with applicant's profession1.
- academic: Latest work performance rating of "Excellent" or at least "Very Satisfactory"1; GWA >= 85.00%3.
- minimum_gwa: 85.00%1.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: Must NOT exceed 50 years of age at time of application1.
- school/consortium: Recognized public or private graduate schools1.
- courses: Graduate degree courses strictly aligned with applicant's current profession1.
- sectoral/hidden: Must have been in service for at least three (3) years in a national or local government office in Taguig, or a teacher in a public/private school in Taguig, or uniformed PNP personnel based in Taguig1.
- work_experience: None
- good_moral: Required (Good moral character in paper and deeds)1.
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: DepEd teachers require endorsement from DepEd Superintendent; PNP personnel require endorsement from Taguig Chief of Police; Taguig LGU employees require endorsement from Department Head and City Administrator1.

### Timing
- who: Resident public/private teachers, government employees, and uniformed personnel in Taguig taking Master's or Doctoral degrees1.
- freshmen/soph/junior/senior/grad/reapply: : N/A1. | : N/A1. | : N/A1. | : N/A1. | : Yes (Master's/Doctoral enrollees)1. | : Yes1.
- window: Semestral schedule (DepEd applicants submitted per DepEd-TAPAT Division Office schedule)1. → Semestral cutoff1. (Annual / Semestral1.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Maintain passing graduate school GWA1.
- regular_load: Enrolled in active graduate credit units1.
- no_failures: Zero failing grades5.
- return_service: Mandatory commitment to continue serving Taguig City1.

### Disqualifiers / affiliations
- Applicant age exceeding 50 years old1.
- Work performance rating dropping below "Very Satisfactory"1.
- Service in Taguig location less than three (3) years1.
- Enrollment in graduate courses unaligned with current profession1.

### Benefits (catalog)
- tuition: Direct grant subsidy1.
- stipend: Integrated into grant1.
- allowance: PHP 18,000.00 to PHP 60,000.00 per school year depending on school category4.

### Documents (operational hidden reqs)
- Filled LEAD Application Form with 3 sets of 2x2 photos1.
- Registration Form / Proof of Enrolment in Master's or Doctoral program1.
- Authenticated Copy of Grades / Transcript of Records1.
- Updated Curriculum Checklist of enrolled graduate course1.
- Service Record proving at least 3 years of service in Taguig1.
- Latest Work Performance Evaluation (Very Satisfactory or Excellent)1.
- Official Sectoral Endorsement (DepEd Superintendent / Police Chief / City Administrator)1.
- Signed copy of approved thesis/dissertation proposal (for research grant)1.

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
  "minimum_gwa": 85.0,
  "income_limit": null,
  "age_limit": 50,
  "sectoral_restriction": "TAGUIG_GOVT_TEACHER_PNP_3_YEARS",
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "residency_restriction": "TAGUIG_CITY_3_YEARS",
  "return_service_required": true,
  "application_window": {
    "open": "semestral_notice",
    "close": "semestral_notice"
  },
  "deadline_type": "semestral",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Sectoral Endorsement Failure: Automated matching engines must require users to
- verification: Verified1. | confidence: 95/1003.

- CONTRADICTION/NOTE: entry GWA (85.00%1.) vs renewal (Maintain passing graduate school GWA1.)

---

## Makati City Premier and Specialized School Scholarship6 (ID: 98)

### Hard eligibility
- citizenship: Filipino Citizen6
- residency/destination: Bona fide resident of Makati City6.
- education_level: College / Undergraduate3.
- eligible_year_levels: 1 (Incoming Freshmen)6.
- incoming_freshman_only: Yes6.
- existing_college: Ineligible for initial entry6.
- graduate_students: Ineligible6.
- current_enrollment: Enrolled or accepted as an incoming 1st-year student in a private college or university in Metro Manila declared a CHED Center of Excellence6.
- academic: Fresh senior high school graduate belonging to the Top 10 Percent of the graduating class6.
- minimum_gwa: Minimum GWA of 1.50 (or equivalent 88.00% scale)3.
- alt_class_rank: Belong to the Top 10% of the SHS graduating class6.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Private colleges and universities in Metro Manila declared as CHED Centers of Excellence6.
- courses: CHED Center of Excellence degree programs6.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Required6.
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Must sign a mandatory Service Contract Agreement committing to serve with the Makati City Government after graduation6.

### Timing
- who: Graduating SHS students from Makati public schools belonging to the top 10% of their class6.
- freshmen/soph/junior/senior/grad/reapply: : Yes (at initial college entry)6. | : No6. | : No6. | : No6. | : No6. | : No6.
- window: Annual cycle following SHS graduation6. → Specified per annual intake notice6. (Fixed / Annual3.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Must maintain a GWA of at least 1.50 (or equivalent) each term6.
- regular_load: Full credit load required6.
- no_failures: Zero failing (5.0), unremoved 4.0, or incomplete marks6.
- return_service: Mandatory service agreement committing scholar to serve with the Makati City Government6.

### Disqualifiers / affiliations
- Enrolling in non-COE private institutions or public SUCs (must shift to SUC track ID 31)6.
- Failing grades (5.0) or dropping below minimum GWA6.
- Non-compliance with mandatory service agreement6.

### Benefits (catalog)
- tuition: Covered up to grant cap6.
- stipend: PHP 4,000.00 per month (integrated into total award)3.
- allowance: PHP 80,000.00 total scholarship benefit per school year6.

### Documents (operational hidden reqs)
- Official Application Form6.
- SHS Form 138 showing GWA and Principal's Certification of Top 10% Class Rank6.
- Proof of Residency in Makati City6.
- Admission Letter / Certificate of Enrollment from private CHED Center of Excellence in Metro Manila6.
- Parents' ITR or Certificate of Indigency6.
- Signed Service Contract Agreement6.

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
  "minimum_gwa": 88.0,
  "rank_cutoff_alternative": 10,
  "income_limit": null,
  "school_type": [
    "PRIVATE_CHED_CENTER_OF_EXCELLENCE_NCR"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "residency_restriction": "MAKATI_CITY_RESIDENT",
  "return_service_required": true,
  "application_window": {
    "open": "annual_notice",
    "close": "annual_notice"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● COE Course Validation: System must verify that the specific program enrolled in is
- verification: None | confidence: 96/1003.

- CONTRADICTION/NOTE: entry GWA (Minimum GWA of 1.50 (or equivalent 88.00% scale)3.) vs renewal (Must maintain a GWA of at least 1.50 (or equivalent) each term6.)

---

## University of Makati Special Institutional Scholarship7 (ID: 99)

### Hard eligibility
- citizenship: Filipino Citizen7
- residency/destination: Dependent on sub-track (Makati employees/DILG/OSCA tracks require local affiliation; sports/arts tracks open)7.
- education_level: College / TVET3.
- eligible_year_levels: 1, 2, 3, 4, 53.
- incoming_freshman_only: No7.
- existing_college: Yes7.
- graduate_students: Restricted7.
- current_enrollment: Officially enrolled at the University of Makati7.
- academic: Passing GWA >= 75.00% (or standard college retention GWA <= 2.50)3.
- minimum_gwa: 75.00%3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: Senior Citizen track requires applicant to be at least 70 years of age at time of application7.
- school/consortium: Restricted strictly to students enrolled at the University of Makati7.
- courses: Any undergraduate or technical-vocational course offered at UMak7.
- sectoral/hidden: Must belong to one of the designated categories and present official endorsement:
- work_experience: None
- good_moral: Required7.
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Endorsement letters must be submitted once per academic year or per term as mandated7.

### Timing
- who: Officially enrolled UMak students meeting special sectoral criteria7.
- freshmen/soph/junior/senior/grad/reapply: : Yes7. | : Yes7. | : Yes7. | : Yes7. | : No7. | : Yes (Requires annual/semestral re-endorsement)7.
- window: Announced semestrally on UMak OLEA system7. → Term registration deadline12. (Semestral3.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Maintain passing GWA and comply with university retention policies7.
- regular_load: Full academic credit load carried7.
- no_failures: Zero failing grades7.
- return_service: Active participation in university sports, culture, or community programs (for athletes/artists)7.

### Disqualifiers / affiliations
- Failure to submit updated sectoral endorsement letter7.
- Unapproved reduction of academic unit load7.

### Benefits (catalog)
- tuition: Full (100%) or Partial (50%) exemption from tuition/token fees7.
- stipend: PHP 1,000.00 per month (depending on sponsor track)3.
- allowance: Total value up to PHP 15,000.00 per school year3.

### Documents (operational hidden reqs)
- Proof of Enrollment at UMak7.
- Preceding Term Grade Report7.
- Specific Sectoral Endorsement / ID: ○ DILG Makati Endorsement Letter7. ○ OSCA Endorsement + Senior Citizen ID (for age >= 70)7. ○ Center for Inclusive Education Endorsement + PWD ID7. ○ AFP Beneficiary Certificate / ID7. ○ Proof of Parent Employment in Makati City Government11.
- Online application submission via UMak OLEA Portal7.

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
    4,
    5
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": true,
  "minimum_gwa": 75.0,
  "income_limit": null,
  "sectoral_restriction": "UMAK_SPECIAL_SECTORAL_ENDORSED",
  "school_type": [
    "UMAK_ONLY"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "OLEA_semestral_dates",
    "close": "OLEA_semestral_dates"
  },
  "deadline_type": "semestral",
  "cycle_type": "semester",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Annual Endorsement Expiration: Endorsements for DILG and employee tracks expire
- verification: Verified3. | confidence: 96/1003.

- CONTRADICTION/NOTE: entry GWA (75.00%3.) vs renewal (Maintain passing GWA and comply with university retention policies7.)

---

## NavotaAs Fisherfolk Children Scholarship Track19 (ID: 100)

### Hard eligibility
- citizenship: Filipino Citizen19
- residency/destination: Bona fide resident of Navotas City19.
- education_level: College / TVET3.
- eligible_year_levels: 1, 2, 3, 43.
- incoming_freshman_only: No3.
- existing_college: Yes3.
- graduate_students: No3.
- current_enrollment: Enrolled or accepted in a recognized college, university, or technical-vocational institution19.
- academic: GWA of at least 78.00%3.
- minimum_gwa: 78.00%3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined annual gross family income must not exceed PHP 180,000.003.
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Recognized public or private HEIs or TVET training centers19.
- courses: Agriculture, Fisheries, Marine Biology, TVET trades, and general degree programs19.
- sectoral/hidden: Parent must be an officially registered fisherfolk listed in the Navotas City Juan Magsasaka / Fisherfolk Database maintained by the City Agriculture's Office (CAO)19.
- work_experience: None
- good_moral: Required19.
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Must present official Fisherfolk Identification Card (ID) issued by CAO19.

### Timing
- who: Direct legitimate children or dependents of registered Navotas fisherfolk3.
- freshmen/soph/junior/senior/grad/reapply: : Yes3. | : Yes3. | : Yes3. | : Yes3. | : No3. | : Yes3.
- window: Annual cycle managed by City Agriculture's Office19. → Announced per annual cycle19. (Fixed / Annual3.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Maintain passing academic GWA (>= 78.00%)3.
- regular_load: Enrolled in regular credit load19.
- no_failures: Zero failing grades19.
- return_service: None3.

### Disqualifiers / affiliations
- Delisting of parent from the official Navotas Fisherfolk Database19.
- Combined family annual gross income exceeding PHP 180,000.003.
- Failure to maintain required 78.00% GWA3.

### Benefits (catalog)
- tuition: Full or partial tuition grant coverage3.
- stipend: PHP 1,500.00 per month3.
- allowance: Integrated into monthly stipend3.

### Documents (operational hidden reqs)
- Application Form19.
- Official Fisherfolk Registration Certificate / Fisherfolk ID issued by CAO (Juan Magsasaka Database record)19.
- Proof of Relationship (PSA Birth Certificate of applicant showing registered parent)19.
- Barangay Certificate of Residency in Navotas City19.
- School Report Card / TOR (GWA >= 78.00%)3.
- Income Tax Return or Barangay Certificate of Indigency (Income <= PHP 180,000)3.

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
  "minimum_gwa": 78.0,
  "income_limit": 180000,
  "sectoral_restriction": "NAVOTAS_REGISTERED_FISHERFOLK_DEPENDENT",
  "school_type": [
    "RECOGNIZED_HEI_OR_TVET"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "residency_restriction": "NAVOTAS_CITY_RESIDENT",
  "application_window": {
    "open": "annual_notice",
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
- ● Database Verification Dependency: The matching engine must verify parent inclusion in
- verification: Verified3. | confidence: 95/1003.

- CONTRADICTION/NOTE: entry GWA (78.00%3.) vs renewal (Maintain passing academic GWA (>= 78.00%)3.)

---
