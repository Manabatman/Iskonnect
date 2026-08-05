# DATABASE_V3_GROUPC_PRIVATE_FOUNDATIONS_P1.pdf — Implementation Details

Scholarships: 7

## Ayala Foundation U-Go Scholar Grant (U-GO Scholar Grant) (ID: 11)

### Hard eligibility
- citizenship: Filipino citizen
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE
- education_level: College / Undergraduate
- eligible_year_levels: 1st Year, 2nd Year, 3rd Year (and 4th Year if enrolled in a 5-year degree program)
- incoming_freshman_only: No
- existing_college: Yes
- graduate_students: No
- current_enrollment: Enrolled or will enroll in a public or state university/college (SUC/LUC) in the Philippines
- academic: Minimum Grade Point Average / General Weighted Average (GWA) of at least 85% with no failing grades; no disciplinary or administrative cases
- minimum_gwa: 85.00%
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Demonstrated financial need (family income within low-income threshold, parent ITR, BIR Tax Exemption, or Indigency)
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Restricted to public or state universities and colleges (SUCs/LUCs) in the Philippines
- courses: NOT SPECIFIED IN OFFICIAL SOURCE
- sectoral/hidden: Must be a female student
- work_experience: None
- good_moral: Required (must have no disciplinary or administrative cases)
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Must NOT have any existing scholarship grant

### Timing
- who: Female Filipino incoming 1st-year, 2nd-year, or 3rd-year college students (and 4th-year students taking a 5-year course) enrolled in public or state universities.
- freshmen/soph/junior/senior/grad/reapply: : Yes | : Yes | : Yes | : Yes (Only if taking a 5-year course and entering 4th year; | : No | : Yes, provided they meet all eligibility criteria and hold
- window: May 5, 2026 → June 6, 2026 (Annual; AY AY 2026–2027)

### Renewal
- maintain_gwa: Maintain a minimum GWA of 85.00% or equivalent each academic term.
- regular_load: Full-time credit load per term in a public/state university.
- no_failures: Zero failing grades.
- return_service: None.

### Disqualifiers / affiliations
- Male gender.
- Possession or active enjoyment of any other scholarship grant.
- Enrollment in a private higher education institution.
- Students expecting to graduate during the current academic year.
- GWA below 85.00% or presence of failing/incomplete grades.
- History of administrative or disciplinary sanctions.

### Benefits (catalog)
- tuition: NOT SPECIFIED IN OFFICIAL SOURCE (Public/state universities are covered under Republic Act 10931; grant provides direct educational financial support).
- stipend: Integrated into annual financial assistance.
- allowance: Approximately PHP 40,000.00 annual financial assistance.

### Documents (operational hidden reqs)
- Duly accomplished online application form.
- Current official Certificate of Registration / Enrollment signed by the registrar with wet signature.
- Latest copy of grades / Transcript of Records signed by the registrar with wet signature.
- Proof of financial need (Parents' or guardians' most recent Income Tax Return [ITR], BIR Tax Exemption Certificate, Barangay Certificate of Indigency, or OFW/seafarer contract/proof of income).
- Proof of college admission or Senior High School diploma (for incoming 1st-year students).
- Recent copy of electric or water bill (if available).
- Official Recommendation Letter (for shortlisted applicants).

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
  "income_limit": 400000,
  "gender_restriction": "FEMALE",
  "school_type": [
    "SUC",
    "LUC"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "scholarship_exclusivity_clause": true,
  "application_window": {
    "open": "05-05",
    "close": "06-06"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Gender Mismatch: Live database state currently lacks a gender filter tag. Displaying ID 11
- verification: Verified | confidence: None

- CONTRADICTION/NOTE: entry GWA (85.00%) vs renewal (Maintain a minimum GWA of 85.00% or equivalent each academic term.)

---

## Assistance for the Completion of College Education for Superior Students (MBFI-ACCESS) Program (ID: 13)

### Hard eligibility
- citizenship: Filipino citizen
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE
- education_level: College / Undergraduate
- eligible_year_levels: Year 1 (Incoming Freshmen) and Year 2 (Sophomores in Engineering tracks)
- incoming_freshman_only: No (Incoming Freshmen for general priority courses; Sophomores for Engineering).
- existing_college: Yes (Incoming 2nd-year Engineering students in partner HEIs).
- graduate_students: No
- current_enrollment: Accepted or enrolled in a priority course at an MBFI partner university
- academic: General Weighted Average (GWA) of at least 85.00% or equivalent in High School / previous college term; passing score in MBFI qualification exams and interviews
- minimum_gwa: 85.00%
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined gross annual family income not exceeding PHP 500,000.00
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Restricted strictly to MBFI partner universities/colleges (CHED Centers of Excellence/Development or Level II/III accredited institutions)
- courses: Specialized Science & Math, Teacher Education (BEED/BSED), Information Technology, Engineering, Business Administration / Entrepreneurship, Accountancy, Nursing, Architecture, Statistics
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Required
- health: Physically and mentally fit - Other Official Rules: Must pass screening, written examinations, and panel evaluation processes
- other_rules/conflicts: Must pass screening, written examinations, and panel evaluation processes

### Timing
- who: Incoming college freshmen enrolled in priority courses, and incoming sophomores taking Engineering at accredited partner institutions.
- freshmen/soph/junior/senior/grad/reapply: : Yes (as incoming 1st-year students entering college or | : Yes (Incoming 2nd-year Engineering students). | : No | : No | : No | : No
- window: Announced per academic year cycle via partner university scholarship offices → Specified in annual partner university advisories (Fixed / Annual; AY AY 2025–2026 / AY 2026–2027)

### Renewal
- maintain_gwa: Maintain a minimum semester GWA of 85.00% or university passing standards.
- regular_load: Full-time credit enrollment per term in approved priority course.
- no_failures: Zero failing grades in enrolled subjects.
- return_service: None (Encouraged participation in "Pay-it-forward Service to the 4Cs" via ASSET alumni association).

### Disqualifiers / affiliations
- Enrolling in non-partner higher education institutions.
- Combined annual family income exceeding PHP 500,000.00.
- GWA dropping below 85.00% or presence of failing grades.
- Failure to pass MBFI qualification examination or interview evaluation.

### Benefits (catalog)
- tuition: Full tuition and matriculation fee coverage at partner universities.
- stipend: Direct monthly living allowance.
- allowance: Fixed semester living and book allowances.

### Documents (operational hidden reqs)
- Accomplished MBFI-ACCESS Application Form.
- Official Report Card / Transcript of Records / Form 137 showing minimum GWA of
- 00%.
- Parents' Income Tax Return (ITR) or BIR Certificate of Tax Exemption showing annual family income below PHP 500,000.00.
- Certificate of Enrollment / Notice of Admission from an MBFI partner university.
- Certificate of Good Moral Character.
- Medical Certificate confirming physical and mental fitness.
- 2x2 ID Pictures.

### Recommended schema
`json
{
  "education_level": [
    "College"
  ],
  "eligible_year_levels": [
    1,
    2
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": true,
  "minimum_gwa": 85.0,
  "income_limit": 500000,
  "priority_courses": [
    "ACCOUNTANCY",
    "BUSINESS_ADMINISTRATION",
    "ENTREPRENEURSHIP",
    "EDUCATION",
    "INFORMATION_TECHNOLOGY",
    "ENGINEERING",
    "SPECIALIZED_SCIENCE_MATH",
    "NURSING",
    "ARCHITECTURE",
    "STATISTICS"
  ],
  "school_type": [
    "PRIVATE_HEI",
    "SUC"
  ],
  "partner_school_restricted": true,
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
- ● School Restriction Enforcement: Displaying ID 13 to students in non-partner HEIs causes
- verification: Verified | confidence: 95/100

- CONTRADICTION/NOTE: entry GWA (85.00%) vs renewal (Maintain a minimum semester GWA of 85.00% or university passing standards.)

---

## BPI Foundation Pagpupugay Scholarship Program (ID: 14)

### Hard eligibility
- citizenship: Filipino citizen
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE
- education_level: College / Undergraduate
- eligible_year_levels: 1st Year, 2nd Year, 3rd Year, 4th Year, and 5th Year
- incoming_freshman_only: No
- existing_college: Yes
- graduate_students: No
- current_enrollment: Enrolled or applying to any 4-year or 5-year college/university program in BPI Foundation partner schools nationwide (or non-partner HEIs upon direct coordination)
- academic: General Weighted Average (GWA) of at least 85.00% or equivalent / prevailing university standards for the previous school year (incoming 1st year) or previous semester (incoming 2nd-5th year)
- minimum_gwa: 85.00%
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Demonstrated financial need verified via parents'/guardian's Income Tax Return (ITR)
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Open to students in BPI Foundation partner universities (e.g., Ateneo de Manila, Mapua, Malayan Colleges, National Teachers College, University of Nueva Caceres) and accredited nationwide HEIs
- courses: Any 4-year or 5-year undergraduate degree program
- sectoral/hidden: Must be a qualified next-of-kin of medical frontliners (doctors, nurses, medical technologists, community health workers, administrative/utility/support staff in healthcare facilities) who passed away or contracted COVID-19 in the line of duty. Priority order: children of married frontliners; next-of-kin up to 3rd degree consanguinity for single frontliners
- work_experience: None
- good_moral: Required (Certificate of Good Moral Character)
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Requires hospital endorsement letter, official affidavits of endorsement and no objection, and proof of frontliner COVID-19 medical/death status

### Timing
- who: Qualified next-of-kin of eligible medical frontliners entering or currently enrolled in 1st to 5th year of college.
- freshmen/soph/junior/senior/grad/reapply: : Yes | : Yes | : Yes | : Yes (4th and 5th year undergraduate students). | : No | : Yes (Scholarships are evaluated for annual renewal).
- window: Announced per annual cycle (typically Q2/Q3) → Announced annually (e.g., July 31 / extended to September) (Annual; AY AY 2025–2026 / AY 2026–2027)

### Renewal
- maintain_gwa: Maintain a minimum GWA of 85.00% or prevailing university standards each semester.
- regular_load: Enrolled in full term credit load.
- no_failures: Compliance with university retention policies.
- return_service: None.

### Disqualifiers / affiliations
- Applicant is not a qualified next-of-kin (child or up to 3rd degree consanguinity) of an eligible COVID-19 medical frontliner.
- Frontliner was not assigned to a hospital or recognized healthcare facility.
- Semester GWA dropping below 85.00%.
- Failure to submit mandatory hospital endorsements or affidavits.

### Benefits (catalog)
- tuition: Up to PHP 100,000.00 per academic year covering tuition and matriculation fees (paid directly to partner HEI).
- stipend: Provided as monthly living subsidy for State University/College (SUC) scholars.
- allowance: Learning assistance allowance provided for SUC scholars.

### Documents (operational hidden reqs)
- Fully accomplished Scholarship Application Form and Data Privacy Form.
- Endorsement Letter signed by authorized representative of hospital/healthcare facility where frontliner was assigned.
- Affidavit of Endorsement and No Objection (from frontliner if living, or next-of-kin if deceased).
- PSA Birth Certificate of applicant (and family birth certificates showing common parents if nephew/niece up to 3rd degree).
- PSA Marriage Certificate (for widow/widower or parents).
- PRC ID or License ID of the medical frontliner.
- Death Certificate of frontliner indicating COVID-19 cause of death OR Medical Certificate indicating COVID-19 infection.
- Parents' or guardian's latest Income Tax Return (ITR).
- Official Transcript of Records / Copy of Grades showing minimum GWA of 85.00%.
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
  "minimum_gwa": 85.0,
  "income_limit": 400000,
  "sectoral_restriction": "COVID19_MEDICAL_FRONTLINER_NEXT_OF_KIN",
  "priority_courses": null,
  "school_type": [
    "PRIVATE_HEI",
    "SUC"
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
- ● Sectoral Tag Mismatch: Live database state currently lacks the specific
- verification: Verified | confidence: 96/100

- CONTRADICTION/NOTE: entry GWA (85.00%) vs renewal (Maintain a minimum GWA of 85.00% or prevailing university standards each semester.)

---

## San Miguel Foundation Educational Assistance / Community Scholarship Program (ID: 15)

### Hard eligibility
- citizenship: Filipino citizen
- residency/destination: Preference given to residents of San Miguel Corporation host communities or operational areas
- education_level: College / Undergraduate (and Technical-Vocational courses)
- eligible_year_levels: 1st Year, 2nd Year, 3rd Year, 4th Year, and 5th Year
- incoming_freshman_only: No
- existing_college: Yes
- graduate_students: No
- current_enrollment: Enrolled or accepted in designated partner universities or SUCs/LUCs in SMC host communities
- academic: Academically deserving student (minimum GWA parameter governed by partner university agreements, typically 85.00% to 88.00% without failing grades)
- minimum_gwa: 88.00% (Live database baseline; partner HEI MOA standards apply).
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Financially challenged background (family annual income < PHP 400,000.00 / demonstrated indigency)
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Restricted to SMC partner universities (e.g., UP Diliman, Dualtech Center, partner HEIs near SMC plants/townships)
- courses: Engineering (Civil, Electrical, Mechanical, Chemical), Agriculture, Agribusiness, Business / Accountancy, Applied Sciences (Applied Physics, Molecular Biology & Biotechnology), Technical-Vocational skills
- sectoral/hidden: Residents of SMC host communities / underprivileged family dependents
- work_experience: None
- good_moral: Required
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Must pass screening evaluation conducted by SMFI or partner university scholarship committee

### Timing
- who: Resident SHS graduates and ongoing college students enrolled in priority courses at partner institutions.
- freshmen/soph/junior/senior/grad/reapply: : Yes - Can current sophomores apply?: Yes | : Yes | : Yes (Incoming junior track available for specialized | : Yes | : No | : Yes
- window: Varies per partner university academic calendar → Announced annually by partner university scholarship offices (Annual; AY AY 2025–2026 / AY 2026–2027)

### Renewal
- maintain_gwa: Maintain required semester GWA prescribed in partner university MOA.
- regular_load: Full-time credit enrollment per term.
- no_failures: Zero failing grades in enrolled subjects.
- return_service: None required (Potential career/employment opportunities offered across SMC operating companies).

### Disqualifiers / affiliations
- Non-enrollment in an SMC partner university or non-priority degree course.
- Combined annual family income exceeding PHP 400,000.00.
- Failing grades or dropping subjects during the academic term.
- Misrepresentation of residency in SMC host communities.

### Benefits (catalog)
- tuition: Full tuition and matriculation fee coverage at partner institutions.
- stipend: Direct monthly living allowance.
- allowance: Fixed semester book and school supplies allowance.

### Documents (operational hidden reqs)
- SMFI Application Form / Partner University Scholarship Application Form.
- Official Transcript of Records / Report Card (Form 138 / SF9).
- Parents' Income Tax Return (ITR) or Barangay Certificate of Indigency.
- Barangay Certificate of Residency (proving residence in SMC host community).
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
  "minimum_gwa": 88.0,
  "income_limit": 400000,
  "priority_courses": [
    "CIVIL_ENGINEERING",
    "ELECTRICAL_ENGINEERING",
    "MECHANICAL_ENGINEERING",
    "CHEMICAL_ENGINEERING",
    "AGRICULTURE",
    "AGRIBUSINESS",
    "BUSINESS_ADMINISTRATION",
    "ACCOUNTANCY",
    "APPLIED_PHYSICS",
    "MOLECULAR_BIOLOGY"
  ],
  "school_type": [
    "PRIVATE_HEI",
    "SUC"
  ],
  "partner_school_restricted": true,
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
- ● Partner School Verification: Program relies on partner university agreements. Engine
- verification: Verified | confidence: 96/100

- CONTRADICTION/NOTE: entry GWA (88.00% (Live database baseline; partner HEI MOA standards apply).) vs renewal (Maintain required semester GWA prescribed in partner university MOA.)

---

## PLDT-Smart Foundation Gabay Guro Scholarship Program (ID: 16)

### Hard eligibility
- citizenship: Filipino citizen
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE
- education_level: College / Undergraduate
- eligible_year_levels: Year 1 (Incoming First-Year College Students)
- incoming_freshman_only: Yes
- existing_college: No
- graduate_students: No
- current_enrollment: Enrolled or admitted as a first-year student in Bachelor of Elementary Education (BEED) or Bachelor of Secondary Education (BSED) (major in English, Mathematics, Science) at a Gabay Guro partner SUC/college
- academic: General Weighted Average (GWA) of at least 85.00% during the final year of Senior High School
- minimum_gwa: 85.00%
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: Combined annual family gross income must NOT exceed PHP 250,000.00
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Restricted strictly to Gabay Guro partner SUCs nationwide (over 40+ partner state universities including MSU Gensan, PNU, etc.)
- courses: Bachelor of Elementary Education (BEED), Bachelor of Secondary Education (BSED) with majors in English, Mathematics, or Science
- sectoral/hidden: Aspiring teachers / Teacher Education majors
- work_experience: None
- good_moral: Required
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Must complete and sign the official Gabay Guro Undertaking Form committing to graduate and render teaching service in Philippine schools

### Timing
- who: Incoming first-year college students admitted to BEED or BSED programs at partner SUCs.
- freshmen/soph/junior/senior/grad/reapply: : Yes (prior to starting term in 1st year). | : No | : No | : No | : No | : No
- window: Announced per annual cycle via partner SUC scholarship offices → Specified in annual partner SUC scholarship advisories (Fixed / Annual; AY AY 2025–2026 / AY 2026–2027)

### Renewal
- maintain_gwa: Maintain required semester GWA prescribed by university (typically 2.0 or 85.00%).
- regular_load: Full-time credit load per semester in BEED/BSED program.
- no_failures: Zero failing or dropped grades.
- return_service: Mandatory teaching commitment in Philippine K-12 schools.

### Disqualifiers / affiliations
- Enrolling in non-education degree programs or non-partner universities.
- Combined family annual gross income exceeding PHP 250,000.00.
- SHS GWA below 85.00%.
- Refusal to sign the mandatory teaching return service undertaking.

### Benefits (catalog)
- tuition: Full coverage of tuition and matriculation fees.
- stipend: Direct monthly living allowance.
- allowance: Semester book allowance and connectivity support.

### Documents (operational hidden reqs)
- Gabay Guro Scholarship Questionnaire & Application Form (Revised 2023).
- Applicant's essay/autobiography ("MY AUTOBIOGRAPHY" in English or Filipino).
- Parents' Annual Income Tax Return (BIR Form 2316 / ITR) OR Barangay/DSWD Certificate of Indigency if unemployed/exempt.
- Latest Report Card / Rating (Form 138 / SF9) showing SHS GWA \ge 85.00\%.
- 2x2 ID Picture on white background.
- Signed Gabay Guro Undertaking Form.

### Recommended schema
`json
{
  "education_lev el": [
    "College"
  ],
  "eligible_year_levels": [
    1
  ],
  "incoming_year_only": true,
  "requires_current_enrollment": true,
  "minimum_gwa": 85.0,
  "income_limit": 250000,
  "priority_courses": [
    "BACHELOR_OF_ELEMENTARY_EDUCATION",
    "BACHELOR_OF_SECONDARY_EDUCATION"
  ],
  "school_type": [
    "SUC"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "return_service_required": true,
  "application_window": {
    "open": "annual_notice",
    "close": "annual_notice"
  },
  "deadline_type": "estimated",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Income Ceiling Mismatch: Live database currently displays max_income: 400000. Relying
- verification: Verified | confidence: 92/100

- CONTRADICTION/NOTE: entry GWA (85.00%) vs renewal (Maintain required semester GWA prescribed by university (typically 2.0 or 85.00%).)

---

## GBF STEM-College Scholarship (formerly GBF-Gokongwei Group STEM Scholarship for Excellence) (ID: 72)

### Hard eligibility
- citizenship: Filipino citizen
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE
- education_level: College / Undergraduate - Eligible Year Levels: 1st Year (Incoming Freshmen), 2nd Year, 3rd Year, 4th Year, and 5th Year (Continuing Students)
- eligible_year_levels: 1st Year (Incoming Freshmen), 2nd Year, 3rd Year, 4th Year, and 5th Year (Continuing Students)
- incoming_freshman_only: No
- existing_college: Yes (2nd Year and above)
- graduate_students: No (Applied strictly to first Bachelor's degree; GBF TeachSTEM Masters is a separate graduate track).
- current_enrollment: Enrolled or planning to enroll in a priority STEM degree program at a Philippine university/college
- academic: General Weighted Average (GWA) of at least 85.00% (or 2.0 / equivalent) with zero failed, dropped, or incomplete grades in high school or college; incoming freshmen must belong to the Top 10% of their SHS graduating batch
- minimum_gwa: 85.00% (or 2.0 / equivalent)
- alt_class_rank: Top 10% of Senior High School graduating batch (mandatory requirement for incoming freshmen)
- income_ceilings: Demonstrated financial need (submission of 2025 ITR, Certificate of Employment with salary, or BIR Tax Exemption required)
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Open to public and private universities in the Philippines offering GBF priority STEM degree programs
- courses: GBF-identified priority STEM degree courses (Engineering, Information Technology, Computer Science, Data Science, Chemistry, Life Sciences, Applied Mathematics, Agriculture, Food Technology)
- sectoral/hidden: STEM degree students
- work_experience: None
- good_moral: Required (good moral standing with active extracurricular/community involvement)
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Must be pursuing first bachelor's degree; willing to fulfill return service obligation

### Timing
- who: Incoming college freshmen (Top 10% batch rank) and continuing college students (2nd year and above) enrolled in priority STEM courses.
- freshmen/soph/junior/senior/grad/reapply: : Yes | : Yes | : Yes | : Yes (4th and 5th year continuing STEM students). | : No | : Yes
- window: Q1/Q2 annually → May 31, 2026 (Annual; AY AY 2026–2027)

### Renewal
- maintain_gwa: Maintain a minimum GWA of 85.00% (2.0 or equivalent) each academic term.
- regular_load: Full-time credit enrollment in priority STEM course
- no_failures: Zero failed, incomplete, or dropped grades
- return_service: Mandatory return service obligation / commitment to work within Gokongwei Group companies or local STEM industries.

### Disqualifiers / affiliations
- Enrolling in non-STEM degree programs
- GWA dropping below 85.00% (2.0) or presence of failed, dropped, or incomplete grades
- Incoming freshmen failing to prove Top 10% batch ranking
- Application for second undergraduate degree

### Benefits (catalog)
- tuition: Direct annual financial grant ranging from PHP 80,000.00 to PHP 120,000.00 (credited directly to scholar's bank account to cover tuition and academic fees).
- stipend: Integrated into annual financial grant.
- allowance: Integrated into annual financial grant. - Book Allowance: Integrated into annual financial grant.

### Documents (operational hidden reqs)
- Fully accomplished online application form.
- For Incoming Freshmen: Certified True Copy of Grade 12 Report Card (Form 138 / Form 137), Certificate of Batch Ranking showing Top 10% rank in Grade 12 (or Grade 11), Notice of Admission / Proof of University Application.
- For Continuing Students: Certified True Copy of Grades for the last 2 consecutive semesters, Registration Form for current term.
- Certificate of Good Moral Character.
- Proof of Annual Household Income (2025 ITR, Certificate of Employment with salary, OFW employment contract, Grab/Lalamove earnings record, or BIR Tax Exemption Certificate).
- Recommender's email address (must not be an immediate family member).

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
  "income_limit": 400000,
  "priority_courses": [
    "ENGINEERING",
    "INFORMATION_TECHNOLOGY",
    "COMPUTER_SCIENCE",
    "DATA_SCIENCE",
    "CHEMISTRY",
    "LIFE_SCIENCES",
    "APPLIED_MATHEMATICS",
    "AGRICULTURE",
    "FOOD_TECHNOLOGY"
  ],
  "school_type": [
    "PRIVATE_HEI",
    "SUC"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "return_service_required": true,
  "application_window": {
    "open": "01-15",
    "close": "05-31"
  },
  "deadline_type": "exact",
  "[span _710](end_span)cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● GWA Inversion: Live database state currently lists min_gwa: 92. Applying 92% will
- verification: Verified | confidence: 95/100

- CONTRADICTION/NOTE: entry GWA (85.00% (or 2.0 / equivalent)) vs renewal (Maintain a minimum GWA of 85.00% (2.0 or equivalent) each academic term.)

---

## Aboitiz Future Leaders Scholarship Program (Aboitiz Brights) (ID: 75)

### Hard eligibility
- citizenship: Filipino citizen
- residency/destination: Nationwide (open to eligible students nationwide enrolled in partner schools)
- education_level: College / Undergraduate
- eligible_year_levels: Year 2 ONLY (Incoming Sophomore Students)
- incoming_freshman_only: No (Incoming Freshmen are strictly barred: "The scholarship is ONLY open to incoming sophomore students who have completed their first year in college").
- existing_college: Yes (Exclusively incoming 2nd-year / sophomore students).
- graduate_students: No
- current_enrollment: Enrolled in an identified priority degree program at an Aboitiz Foundation partner university
- academic: Completed 1st year in college with strong academic performance (minimum GWA specified by partner university / foundation rules, typically 88.00% or 2.0 equivalent without failing grades)
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Live database state displays 75; official policy mandates maintaining good academic standing per partner university criteria).
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE (Financial need evaluated, but no rigid income cap published)
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Restricted strictly to Aboitiz Foundation partner universities (e.g., PSAU, UP System, DLSU, UST, Ateneo de Manila)
- courses: Pre-identified degree programs aligned with Aboitiz Group business units (Engineering, Information Technology, Data Science, Agriculture, Agribusiness, Veterinary Medicine, Finance / Business Administration)
- sectoral/hidden: Student leaders / high leadership potential
- work_experience: None
- good_moral: Required (no record of any form of disciplinary action)
- health: NOT SPECIFIED IN OFFICIAL SOURCE
- other_rules/conflicts: Current recipients of scholarships from other corporate foundations are NOT eligible under the program

### Timing
- who: Incoming sophomore students (Year 2) who have completed their 1st year of college at a partner university.
- freshmen/soph/junior/senior/grad/reapply: : No (Incoming freshmen cannot apply; must complete 1st | : Yes (Primary target cohort entering 2nd | : No | : No | : No | : No
- window: Summer period preceding 2nd year intake → Announced annually via university scholarship offices (Fixed / Annual; AY AY 2025–2026 / AY 2026–2027)

### Renewal
- maintain_gwa: Maintain good academic standing each semester per university standards.
- regular_load: Continuous full-time enrollment in priority course.
- no_failures: Zero failing grades or disciplinary records. - Return Service: Completion of mandatory 400-hour Aboitiz Group internship and active participation in foundation events.
- return_service: No post-graduation employment return service required.

### Disqualifiers / affiliations
- Incoming freshmen, 3rd year, or 4th year students.
- Active enjoyment of a scholarship from another corporate foundation.
- Enrollment in a non-partner university or non-priority degree program.
- Presence of disciplinary records or failing grades. ### 10. Temporal Eligibility Matrix User Profile Eligibility Status Actionable Guidance Incoming Freshman College Student Ineligible Strictly barred; must complete 1st year before applying. Incoming Sophomore (2nd Year, Partner HEI, Priority Course) Eligible Now Apply through partner university scholarship office. Incoming Junior or Senior College Student Ineligible Program intake strictly restricted to 2nd-year entry. Recipient of Another Corporate Foundation Grant Ineligible Corporate foundation exclusivity rule applies.

### Benefits (catalog)
- tuition: Full tuition fee coverage.
- stipend: Direct monthly living allowance.
- allowance: Integrated into monthly living allowance.

### Documents (operational hidden reqs)
- Copy of Student ID.
- Copy of Certificate of Good Moral Character.
- Certified Copy of College Grades starting 1st year / Transcript of Records. 4. Proof of Enrollment in an approved priority course at a partner university.

### Recommended schema
`json
{
  "education_level": [
    "College"
  ],
  "eligible_year_levels": [
    2
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": true,
  "minimum_gwa": 85.0,
  "income_limit": null,
  "priority_courses": [
    "ENGINEERING",
    "INFORMATION_TECHNOLOGY",
    "DATA_SCIENCE",
    "AGRICULTURE",
    "AGRIBUSINESS",
    "VETERINARY_MEDICINE",
    "FINANCE",
    "BUSINESS_ADMINISTRATION"
  ],
  "school_type": [
    "PRIVATE_HEI",
    "SUC"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "corporate_grant_exclusivity_clause": true,
  "application_window": {
    "open": "annual_notice",
    "close": "annual_notice"
  },
  "deadline_type": "estimated",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Critical Year Level Misconfiguration: Live database state currently lists
- verification: Verified | confidence: 98/100

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Live database state displays 75; official policy mandates maintaining good academic standing per partner university criteria).) vs renewal (Maintain good academic standing each semester per university standards.)
- CONTRADICTION: live DB GWA artifact vs official NOT SPECIFIED — NOT SPECIFIED IN OFFICIAL SOURCE (Live database state displays 75; official policy mandates maintaining good academic standing per partner university criteria).

---
