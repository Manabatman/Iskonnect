# DATABASE_V3_GROUPC_PRIVATE_FOUNDATIONS_P2.pdf — Implementation Details

Scholarships: 7

## Security Bank Foundation State Universities Scholarship (Scholars for Better Communities Program) (ID: 58)

### Hard eligibility
- citizenship: Must be a natural-born or naturalized Filipino citizen.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: Undergraduate / College.
- eligible_year_levels: Year 1 (Incoming Freshmen) and limited upperclassmen in specific partner SUCs.
- incoming_freshman_only: Primary focus is incoming freshmen; limited upperclassmen entry exists per SUC slot allocation.
- existing_college: Yes (limited slots at specific partner State Universities and Colleges).
- graduate_students: Ineligible.
- current_enrollment: Must be accepted or enrolled in a partner State University or College, such as Polytechnic University of the Philippines (PUP).
- academic: Must possess a Grade 12 General Weighted Average (GWA) of at least 93.00% or equivalent, with no subject grade lower than 86.00%, and grades of at least 90.00% in high school subjects aligned with the chosen college degree.
- minimum_gwa: 93.00% (Entry GWA cutoff).
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE (Requires documentary proof of financial status via Income Tax Return or Certificate of Indigency; live database records a PHP 350,000.00 ceiling).
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Strictly restricted to designated partner State Universities and Colleges.
- courses: Degree programs aligned with bank operations, including Accountancy, Business Administration, Finance, Information Technology, Computer Science, Data Analytics, Communications, and Journalism.
- sectoral/hidden: Must NOT be a child or dependent of a Security Bank employee, and must not have an immediate family member within the second degree of consanguinity or affinity holding an active SBFI grant.
- work_experience: None
- good_moral: Required (Certificate of Good Moral Character from high school). - Health Requirements: NOT SPECIFIED IN OFFICIAL SOURCE.
- health: None
- other_rules/conflicts: Must carry the full academic load prescribed by the university curriculum per term.

### Timing
- who: Graduating Senior High School Grade 12 students entering 1st year college and continuing 1st year SUC students.
- freshmen/soph/junior/senior/grad/reapply: : Yes. | : No (unless applying for designated continuing SUC | : No. | : No. | : No. | : NOT SPECIFIED IN OFFICIAL SOURCE.
- window: Announced annually (typically Q1/Q2 prior to the academic year opening). → Specified in annual call for applications. (Fixed / Annual.; AY AY 2025–2026 / AY 2026–2027. ### 6. Benefits)

### Renewal
- maintain_gwa: Maintain a General Weighted Average (GWA) of at least 86.00% or equivalent by the end of each academic term. - Regular Load: Enrolled in the full unit load prescribed by the university curriculum.
- regular_load: Enrolled in the full unit load prescribed by the university curriculum.
- no_failures: No grade lower than 80.00% (or equivalent) in any academic subject per term.
- return_service: None mandatory; direct hiring opportunities provided upon graduation.

### Disqualifiers / affiliations
- Being a child or dependent of an employee of Security Bank Corporation or its subsidiaries.
- Having an immediate relative within the second degree of consanguinity or affinity holding an active SBFI scholarship.
- Term GWA dropping below 86.00% or receiving a subject grade below 80.00%.
- Enrolling in a non-partner state university or non-aligned degree program. ### 10. Temporal Eligibility Matrix Profile Status Eligibility Status Actionable Guidance Incoming Grade 12 SHS (GWA \ge 93%) Eligible Now Apply through SBFI external application portal upon acceptance at partner SUC. Enrolled SUC Freshman (entering 2nd Year) Conditionally Eligible Eligible only if continuing SUC slots are available for the target institution. Child of Security Bank Employee Never Eligible Ineligible for External Track; must apply under Internal/RMKK Track.

### Benefits (catalog)
- tuition: Full or partial tuition and matriculation fee coverage paid directly to the partner state university.
- stipend: Integrated into the annual educational grant package.
- allowance: Financial assistance package up to PHP 50,000.00 – PHP 60,000.00 per academic year.

### Documents (operational hidden reqs)
- Duly accomplished SBFI Online Application Form.
- High School Transcript of Records / Grade 12 Report Card showing final GWA.
- Proof of Admission or Acceptance Letter from partner State University. 4. Proof of Financial Status (Latest Parent Income Tax Return, Certificate of Indigency, or OFW Contract).
- PSA Birth Certificate of student applicant. 6. Certificate of Good Moral Character.
- School Grading System documentation (if non-percentage system).

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
  "minimum_gwa": 93.0,
  "renewal_gwa": 86.0,
  "income_limit": null,
  "partner_school_restricted": true,
  "priority_courses": [
    "ACCOUNTANCY",
    "FINANCE",
    "BUSINESS_ADMINISTRATION",
    "INFORMATION_TECHNOLOGY",
    "COMPUTER_SCIENCE",
    "DATA_ANALYTICS",
    "COMMUNICATIONS",
    "JOURNALISM"
  ],
  "citizenship": "Filipino",
  "application_window": {
    "open": "02-01",
    "close": "05-31"
  },
  "deadline_type": "estimated",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Academic Cutoff Discrepancy: The live production database records a minimum GWA of
- verification: Verified. | confidence: None

- CONTRADICTION/NOTE: entry GWA (93.00% (Entry GWA cutoff).) vs renewal (Maintain a General Weighted Average (GWA) of at least 86.00% or equivalent by the end of each academic term. - Regular Load: Enrolled in the full unit load prescribed by the university curriculum.)

---

## Youth Servant Leadership and Education Program (YSLEP) (ID: 59)

### Hard eligibility
- citizenship: Must be a Filipino citizen.
- residency/destination: Resident of Metro Manila (Archdiocese of Manila) or any of the 53 partner dioceses nationwide.
- education_level: Tertiary (College Undergraduate) and Technical-Vocational (TVET).
- eligible_year_levels: Years 1, 2, 3, 4, and 5.
- incoming_freshman_only: No.
- existing_college: Yes.
- graduate_students: Ineligible.
- current_enrollment: Enrolled or accepted in an accredited university, college, or TVET institution.
- academic: Senior High School overall GWA of at least 85.00% or equivalent.
- minimum_gwa: 85.00% (Entry and retention cutoff).
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE (Requires a Certificate of Indigency from the Barangay or DSWD verifying financial distress; live database specifies PHP 180,000.00).
- age: Must be between 18 and 25 years old at the time of application.
- school/consortium: Accredited partner institutions within participating dioceses.
- courses: Open to all degree programs; includes a dedicated track (YSLEP-GEN129) prioritizing Agriculture degrees and sustainable farming.
- sectoral/hidden: Must be single; must be an active member of a Basic Ecclesial Community (GKK) or Parish Youth Ministry.
- work_experience: None
- good_moral: Required (Certificate of Good Moral Character).
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Zero-tolerance policy regarding vices (smoking, alcohol consumption, substance abuse, gambling, and computer game addiction); must NOT hold a Grant-in-Aid Working Student (GIA/WS) award from the school.

### Timing
- who: Single Senior High School graduates and continuing college or TVET students aged 18 to 25.
- freshmen/soph/junior/senior/grad/reapply: : Yes. | : Yes. | : Yes. | : Yes. | : No. | : Yes.
- window: Set annually by local diocesan YSLEP secretariats. → Determined per participating diocese. (Fixed / Annual.; AY AY 2025–2026 / AY 2026–2027.)

### Renewal
- maintain_gwa: Maintain a general average of at least 85.00% per academic term.
- regular_load: Full-time credit load; shifting degree programs without approval is barred.
- no_failures: Passing grades in all enrolled subjects.
- return_service: Post-graduation pledge ("Balik-Handog"): Join the Caritas YSL Alumni Association (CAMASA) and donate 1% of gross monthly salary (or a minimum of PHP 100.00/month) upon employment to finance future scholars.

### Disqualifiers / affiliations
- Marriage, pregnancy, or exceeding 25 years of age.
- Engagement in vices (smoking, alcohol, gambling, illegal drugs, or gaming addiction).
- Holding a school Grant-in-Aid Working Student (GIA/WS) grant or major external award.
- Term GWA dropping below 85.00% or unapproved shifting of degree program.
- Failure to attend mandatory monthly YSL formation workshops or complete 50 annual volunteer hours.

### Benefits (catalog)
- tuition: Direct financial grant covering matriculation and tuition fees.
- stipend: Integrated into the overall annual educational allowance.
- allowance: Annual financial support package valued at approximately PHP 30,000.00 – PHP 35,000.00 per scholar.

### Documents (operational hidden reqs)
- Accomplished Caritas Manila YSLEP Application Form.
- Photocopy of SHS Report Card / College Transcript showing GWA \ge 85.00%.
- Certificate of Good Moral Character.
- PSA Birth Certificate or Baptismal Certificate.
- Certificate of Indigency from Barangay or DSWD.
- Parents' Marriage Certificate (photocopy).
- Two (2) 2x2 ID photos.
- Interview clearance from local Screening Committee.

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
  "minimum_gwa": 85.0,
  "renewal_gwa": 85.0,
  "income_limit": null,
  "age_limit": 25,
  "sectoral_restriction": "PARISH_YOUTH_MINISTRY_MEMBER",
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
- ● Database GWA Understatement: Live production database lists min_gwa: 80. Official
- verification: Verified. | confidence: 88/100.

- CONTRADICTION/NOTE: entry GWA (85.00% (Entry and retention cutoff).) vs renewal (Maintain a general average of at least 85.00% per academic term.)

---

## AFPSLAI Educational Grant Program (EGP) — Non-Business Track (ID: 62)

### Hard eligibility
- citizenship: Must be a Filipino citizen.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: Undergraduate / College.
- eligible_year_levels: Year 1 (Incoming Freshmen), Year 2 (Sophomores), and Year 3 (Juniors).
- incoming_freshman_only: No.
- existing_college: Yes (2nd and 3rd year college students; 4th year students are strictly barred).
- graduate_students: Ineligible.
- current_enrollment: Accepted or enrolled in a non-business baccalaureate degree program.
- academic: Proof of highest educational attainment demonstrating passing academic standing.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Passing academic standing required; live database records 85.00%).
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: Total annual gross family income of the sponsor must not exceed PHP 1,000,000.00.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Recognized Philippine colleges and universities.
- courses: Restricted EXCLUSIVELY to non-business baccalaureate courses (e.g., Computer Science, IT, Engineering, Social Sciences, Agriculture, Science). Business-related courses are covered under the separate Scholarship Apprentice Program).
- sectoral/hidden: Sponsor must be an active, retired, or deceased Regular Member of AFPSLAI in good standing. Applicant must be a legitimate, illegitimate, or legally adopted child. If sponsor is single/unmarried without children, a legitimate/adopted sibling may apply.
- work_experience: None
- good_moral: Required (Certificate of Good Moral Character).
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Strictly limited to ONE (1) grantee per sponsor/family; applicant must NOT hold any other external scholarship grant (except school merit tuition discounts).

### Timing
- who: Dependents (children or qualified siblings) of regular AFPSLAI members who are incoming freshmen, 2nd-year, or 3rd-year college students.
- freshmen/soph/junior/senior/grad/reapply: : Yes. | : Yes. | : Yes. | : No (4th-year students are ineligible). | : No. | : No (if another family member was a prior grantee).
- window: Announced annually (typically May/June). → Specified per cycle (e.g., June 26 or July 15). (Fixed / Annual. - Current AY Covered: AY 2026–2027.; AY AY 2026–2027.)

### Renewal
- maintain_gwa: Maintain passing academic standing per university curriculum.
- regular_load: Full-time credit enrollment.
- no_failures: No failing or dropped subjects. - Return Service: None.
- return_service: None required for EGP track (unlike the SAP business track which requires a 6-to-11 month service bond).

### Disqualifiers / affiliations
- Total gross annual family income exceeding PHP 1,000,000.00.
- Being in the 4th year level or pursuing a graduate degree.
- Enrolling in a business-related degree program under the EGP track.
- Application where a family member / sibling was a previous AFPSLAI scholar.
- Dual enjoyment of external non-school scholarship grants.
- Submission of Barangay clearance instead of Police/NBI clearance.

### Benefits (catalog)
- tuition: Up to PHP 30,000.00 per school term (and up to PHP 10,000.00 for mandatory summer/midyear terms).
- stipend: PHP 4,000.00 per month.
- allowance: ROTC incentive of PHP 2,000.00 per month during terms when ROTC is enrolled.

### Documents (operational hidden reqs)
- Duly accomplished AFPSLAI EGP Application Form.
- PSA Birth Certificate of applicant.
- Report Cards / Certified True Copy of Grades / TOR.
- Certificate of Good Moral Character.
- Valid Police Clearance or NBI Clearance of applicant (Barangay clearance strictly barred).
- Parent/Sponsor Proof of Income: Latest payslip / Certificate of Pension (COP) AND latest Income Tax Return (ITR) for both parents.
- Official Local Government Certificate of No Income / Affidavit if parent is unemployed.
- PSA CENOMAR and Affidavit of No Child (if sponsor is a sibling).

### Recommended schema
`json
{
  "education_level": [
    "College"
  ],
  "eligible_year_levels": [
    1,
    2,
    3
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": true,
  "minimum_gwa": null,
  "income_limit": 1000000,
  "parent_employment_restriction": "AFPSLAI_REGULAR_MEMBER",
  "course_track_restriction": "NON_BUSINESS_COURSES",
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "application_window": {
    "open": "05-01",
    "close": "06-26"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Income Limit Discrepancy: Live production database lists max_income: 500000. Updated
- verification: Verified. | confidence: 96/100.

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Passing academic standing required; live database records 85.00%).) vs renewal (Maintain passing academic standing per university curriculum.)
- CONTRADICTION: live DB GWA artifact vs official NOT SPECIFIED — NOT SPECIFIED IN OFFICIAL SOURCE (Passing academic standing required; live database records 85.00%).

---

## Security Bank Foundation Scholars for Better Communities Scholarship Program (External) (ID: 71)

### Hard eligibility
- citizenship: Must be a Filipino citizen.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE (Live database records NCR region filter).
- education_level: Undergraduate / College.
- eligible_year_levels: Year 1 (Incoming Freshmen) and limited upperclassmen in designated partner HEIs.
- incoming_freshman_only: Primary entry is incoming 1st year; limited upperclassmen slots exist per university.
- existing_college: Yes (limited slots).
- graduate_students: Ineligible.
- current_enrollment: Accepted or enrolled in any of SBFI's 8 partner universities (Ateneo de Manila University, De La Salle University, Far Eastern University, Polytechnic University of the Philippines, University of Santo Tomas, etc.).
- academic: High school Grade 12 GWA of at least 93.00% or equivalent; no subject grade lower than 86.00%; grades of 90.00%+ in subjects aligned with college course.
- minimum_gwa: 93.00% (Entry) / 86.00% (Continuation).
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE (Requires parent ITR, Indigency Certificate, or OFW Contract).
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Strictly restricted to SBFI's 8 partner universities. - Priority Courses: Business Administration, Finance, Accountancy, Financial Management, Information Technology, Computer Science, Data Analytics, Communications, and Journalism.
- courses: Business Administration, Finance, Accountancy, Financial Management, Information Technology, Computer Science, Data Analytics, Communications, and Journalism.
- sectoral/hidden: Must NOT be a child of a Security Bank employee, and must not have an active SBFI scholar relative within the second degree.
- work_experience: None
- good_moral: Required.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Must maintain full-time credit enrollment per term.

### Timing
- who: Graduating SHS Grade 12 students and continuing 1st-year students at partner HEIs.
- freshmen/soph/junior/senior/grad/reapply: : Yes. | : No (unless occupying open continuing slots). | : No. | : No. | : No. - Can previous applicants reapply?: NOT SPECIFIED IN | : NOT SPECIFIED IN
- window: Announced per annual cycle. → Announced per annual cycle. (Fixed / Annual.; AY AY 2025–2026 / AY 2026–2027.)

### Renewal
- maintain_gwa: Term GWA of at least 86.00%.
- regular_load: Enrolled in prescribed full unit load per term.
- no_failures: No grade lower than 80.00% in any subject.
- return_service: None mandatory.

### Disqualifiers / affiliations
- Parent being an employee of Security Bank Corporation or its affiliates.
- Having a relative within the second degree of consanguinity/affinity actively holding an SBFI scholarship.
- Term GWA dropping below 86.00% or subject grade below 80.00%.
- Enrolling in a non-partner university or non-priority program.

### Benefits (catalog)
- tuition: Full or partial tuition and matriculation fee coverage paid directly to the university.
- stipend: Integrated into educational grant package.
- allowance: Annual educational allowance package provided.

### Documents (operational hidden reqs)
- Accomplished SBFI External Scholarship Online Application Form.
- High School Transcript / Grade 12 Report Card showing final GWA.
- Acceptance / Admission Letter from partner university.
- Proof of Financial Status (Parent ITR, Indigency Certificate, or OFW Contract).
- PSA Birth Certificate.
- Certificate of Good Moral Character. 7. School Grading System and Course Curriculum.

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
  "minimum_gwa": 93.0,
  "renewal_gwa": 86.0,
  "income_limit": null,
  "partner_school_restricted": true,
  "priority_courses": [
    "ACCOUNTANCY",
    "FINANCE",
    "BUSINESS_ADMINISTRATION",
    "INFORMATION_TECHNOLOGY",
    "COMPUTER_SCIENCE",
    "DATA_ANALYTICS",
    "COMMUNICATIONS",
    "JOURNALISM"
  ],
  "citizenship": "Filipino",
  "application_window": {
    "open": "02-01",
    "close": "05-31"
  },
  "deadline_type": "estimated",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Database URL Corruption: Live database lists an incorrect portal URL
- verification: Verified. - Last Verified Date: 2026-08-05. | confidence: 95/100.

- CONTRADICTION/NOTE: entry GWA (93.00% (Entry) / 86.00% (Continuation).) vs renewal (Term GWA of at least 86.00%.)

---

## Regalo Mo, Kinabukasan Ko (RMKK) Scholarship Program (Agency Personnel Track) (ID: 111)

### Hard eligibility
- citizenship: Must be a Filipino citizen.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: Elementary, High School, Senior High School, and College.
- eligible_year_levels: College Years 1, 2, 3, and 4.
- incoming_freshman_only: No.
- existing_college: Yes.
- graduate_students: Ineligible.
- current_enrollment: Enrolled in an accredited educational institution.
- academic: Passing GWA (typically \ge 80.00% or equivalent).
- minimum_gwa: 80.00%.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: Targeted at low-income third-party agency staff assigned to Security Bank; live database records a PHP 250,000.00 income cap.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Recognized schools, colleges, and universities.
- courses: Open to various undergraduate degree programs (e.g., Business Administration, Marketing Management, Education).
- sectoral/hidden: Sponsor must be an active third-party agency staff member (e.g., security guard, janitor) assigned to Security Bank Corporation or a legitimate child/dependent.
- work_experience: None
- good_moral: Required.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Agency personnel sponsor must be in active service with Security Bank's accredited staffing agencies.

### Timing
- who: Security Bank agency personnel and their legitimate children.
- freshmen/soph/junior/senior/grad/reapply: : Yes. | : Yes. | : Yes. | : Yes. | : No. | : Yes.
- window: Announced annually via SBFI CSR advisories. → Specified in internal notices. (Fixed / Annual.; AY AY 2025–2026 / AY 2026–2027.)

### Renewal
- maintain_gwa: Maintain passing GWA (\ge 80.00%) each academic year.
- regular_load: Continuous enrollment.
- no_failures: Passing grades in all enrolled subjects.
- return_service: None; direct employment preference at Security Bank upon graduation.

### Disqualifiers / affiliations
- Separation or termination of the sponsor agency personnel from Security Bank assignment.
- Failure to maintain passing academic grades.
- Fraudulent representation of employment or dependency.

### Benefits (catalog)
- tuition: Direct educational assistance grant credited toward tuition/fees.
- stipend: Integrated into educational support grant.
- allowance: Tiered annual financial assistance: Elementary (PHP 25,000.00), High School (PHP 27,000.00), Senior High School (PHP 30,000.00), College (PHP 60,000.00 per year).

### Documents (operational hidden reqs)
- Accomplished SBFI RMKK Application Form.
- Certificate of Employment of Agency Personnel parent from accredited Security Bank agency.
- PSA Birth Certificate of student applicant.
- Report Card / College Transcript of Records showing passing grades.
- Certificate of Enrollment / Registration Card.
- Certificate of Good Moral Character.

### Recommended schema
`json
{
  "education_level": [
    "Elementary",
    "High School",
    "Senior High School",
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
  "income_limit": 250000,
  "sectoral_restriction": "SECURITY_BANK_AGENCY_PERSONNEL_DEPENDENT",
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
- ● Benefit Understatement: Live database lists total_value: 30000. Official college award
- verification: Verified. | confidence: 92/100.

- CONTRADICTION/NOTE: entry GWA (80.00%.) vs renewal (Maintain passing GWA (\ge 80.00%) each academic year.)

---

## GBF STEM-College Scholarship (Formerly GBF-Gokongwei Group STEM Scholarship for Excellence) (ID: 72)

### Hard eligibility
- citizenship: Must be a natural-born or naturalized Filipino citizen.
- residency/destination: Resident of the Philippines.
- education_level: Undergraduate / College.
- eligible_year_levels: Year 1 (Incoming Freshmen) and Year 2+ (Continuing College Students).
- incoming_freshman_only: No.
- existing_college: Yes (2nd year and above).
- graduate_students: Ineligible for College Track (Separate TeachSTEM Master's exists).
- current_enrollment: Enrolled or planning to enroll in a priority STEM degree program in a recognized Philippine university.
- academic: Minimum overall General Weighted Average (GWA) of 85.00% or 2.0 (or equivalent); incoming freshmen must belong to the Top 10% of their Senior High School graduating batch.
- minimum_gwa: 85.00% or 2.0.
- alt_class_rank: Top 10% of SHS batch for incoming freshmen.
- income_ceilings: Must demonstrate financial need; proof of annual household income required (Live database specifies PHP 400,000.00 cap).
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Philippine colleges and universities offering accredited priority STEM programs.
- courses: GBF Priority STEM Courses including Chemical Engineering, Civil Engineering, Computer Engineering, Electrical Engineering, Electronics Engineering, Industrial Engineering, Mechanical Engineering, Materials Engineering, Mining Engineering, Geodetic Engineering, Computer Science, Information Technology, Data Science, Chemistry, Accountancy, Animal Science, and Avionics Technology.
- sectoral/hidden: None.
- work_experience: None
- good_moral: Required (Certificate of Good Moral Character).
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Must have NO failing (5.0), dropped, or incomplete (INC) grades in high school or prior college semesters; must not hold another major corporate scholarship grant.

### Timing
- who: Graduating Grade 12 SHS students and continuing college students (2nd year and above) enrolled in priority STEM programs.
- freshmen/soph/junior/senior/grad/reapply: : Yes (as incoming 1st year or entering 2nd year). | : Yes. | : Yes. | : Yes. | : No. | : Yes.
- window: Announced annually (typically Q1/Q2). → May 31, 2026 (for AY 2026–2027 cycle). (Fixed / Annual.; AY AY 2026–2027.)

### Renewal
- maintain_gwa: Maintain a term GWA of at least 85.00% or 2.0.
- regular_load: Full-time credit enrollment in approved STEM program.
- no_failures: Zero failing, incomplete, or dropped grades.
- return_service: Mandatory return service obligation (render service in the Philippines or within Gokongwei Group companies equal to scholarship period).

### Disqualifiers / affiliations
- Enrolling in non-STEM degree programs.
- Term GWA dropping below 85.00% or receiving a failing, dropped, or incomplete mark.
- Failure to submit proof of top 10% class rank for incoming freshman entry.
- Holding an overlapping major corporate scholarship.

### Benefits (catalog)
- tuition: Covered as part of the direct financial grant package.
- stipend: Integrated into the annual financial grant.
- allowance: Direct annual financial grant of PHP 80,000.00 to PHP 120,000.00 per year (depending on the university, directly credited to scholar's bank account).

### Documents (operational hidden reqs)
- Certified True Copy of Grade 12 Report Card (for Freshmen) OR Certified True Copy of Grades for last 2 consecutive semesters (for Upperclassmen).
- Certificate of Class Rank (Top 10% certification for incoming freshmen).
- Notice of Admission or Proof of University Application.
- Certificate of Good Moral Character.
- Proof of Household Income (Parent ITR, Certificate of Employment with salary, OFW contract, or BIR Tax Exemption Certificate).
- Proof of Billing (Utility bill matching residence address).
- Recommender's email address (Non-relative reference). ### 8. Renewal Requirements ● Maintain GWA: Maintain a term GWA of at least 85.00% or 2.0. ● Regular Load: Full-time credit enrollment in approved STEM program. ● No Failures: Zero failing, incomplete, or dropped grades. ● Return Service: Compliance with post-graduation return service agreement.

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
  "renewal_gwa": 85.0,
  "rank_cutoff_alternative": 10,
  "income_limit": 400000,
  "priority_courses": [
    "CHEMICAL_ENGINEERING",
    "CIVIL_ENGINEERING",
    "COMPUTER_ENGINEERING",
    "ELECTRICAL_ENGINEERING",
    "ELECTRONICS_ENGINEERING",
    "INDUSTRIAL_ENGINEERING",
    "MECHANICAL_ENGINEERING",
    "COMPUTER_SCIENCE",
    "INFORMATION_TECHNOLOGY",
    "DATA_SCIENCE",
    "CHEMISTRY",
    "ACCOUNTANCY"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "application_window": {
    "open": "01-15",
    "close": "05-31"
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
- ● Database Portal URL Correction: Live database link points to aggregator
- verification: Verified. | confidence: 94/100.

- CONTRADICTION/NOTE: entry GWA (85.00% or 2.0.) vs renewal (Maintain a term GWA of at least 85.00% or 2.0.)

---

## Aboitiz Future Leaders Scholarship Program (AFLSP) / Aboitiz Brights (ID: 75)

### Hard eligibility
- citizenship: Must be a Filipino citizen.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: Undergraduate / College.
- eligible_year_levels: Year 2 (Incoming Sophomores ONLY).
- incoming_freshman_only: NO (Incoming Freshmen are strictly INELIGIBLE).
- existing_college: YES (Strictly restricted to incoming 2nd-year college students).
- graduate_students: Ineligible.
- current_enrollment: Enrolled as an incoming sophomore student at a designated partner university.
- academic: First-year college GWA/GPA of at least 88.00% or 2.0 (or equivalent); NO dropped subjects, NO failing grades (5.0), and NO unremoved incomplete (INC) or 4.0 grades in any academic subject.
- minimum_gwa: 88.00% or 2.00.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE (Requires submission of household financial proof or Affidavit of Income).
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to designated partner universities: Ateneo de Manila University, De La Salle University, Mapúa University, University of Santo Tomas, UP Diliman, UP Baguio, UP Cebu, UP Los Baños, and UP Mindanao.
- courses: Engineering (Electrical, Industrial, Civil, Chemical, Computer, Mechanical, Materials, Mining, Geodetic, Electronics), Data Science, Computer Science, BA Communication / Journalism, BS Agriculture, BS Forestry, BS Psychology.
- sectoral/hidden: None.
- work_experience: None
- good_moral: Required (Certificate of Good Moral Character; no record of any form of disciplinary action).
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Applicants receiving scholarships from other corporate foundations are ineligible (CHED and DOST scholars are allowed).

### Timing
- who: Incoming 2nd-year college (sophomore) students enrolled in pre-identified courses at partner universities.
- freshmen/soph/junior/senior/grad/reapply: : No (Must complete 1st year to apply as an incoming | : Yes (Primary and exclusive target applicant cohort). | : No. | : No. | : No. | : Yes (if entering sophomore year).
- window: August 1 annually. → September 1 annually. (Fixed / Annual.; AY AY 2025–2026 / AY 2026–2027.)

### Renewal
- maintain_gwa: Maintain required term GWA (at least 88.00% / 2.0).
- regular_load: Full credit load per term.
- no_failures: Zero failing grades (5.0), dropped marks (DRP), or unremoved incomplete (INC/4.0) grades.
- return_service: No mandatory employment return service bond; scholars must complete a mandatory 400-hour internship within Aboitiz Group business units and attend leadership development sessions.

### Disqualifiers / affiliations
- Being an incoming freshman, 3rd-year, or 4th-year college student.
- Enrolling in a non-partner university or non-identified degree program.
- Having any grade of 5.0, DRP, or unremoved INC/4.0 mark in 1st year college.
- Holding an active scholarship grant from another corporate foundation.
- First-year GWA dropping below 88.00% or 2.0.

### Benefits (catalog)
- tuition: Full 100% tuition and matriculation fee coverage.
- stipend: PHP 10,000.00 per month.
- allowance: Board Exam Review Fee allowance of PHP 15,000.00.

### Documents (operational hidden reqs)
- Copy of Student ID.
- Certificate of Good Moral Character.
- Certified True Copy of Grades / Transcript of Records covering full 1st year college.
- Certificate of Enrollment / Registration Form for 1st and 2nd term of current SY.
- Copy of Certificates of College Leadership, Awards, or Seminars.
- Proof of Household Income / Affidavit of Income Source.

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
  "requires_current_enrollment ": true,
  "minimum_gwa": 88.0,
  "renewal_gwa": 88.0,
  "income_limit": null,
  "partner_school_restricted": true,
  "priority_courses": [
    "ELECTRICAL_ENGINEERING",
    "INDUSTRIAL_ENGINEERING",
    "CIVIL_ENGINEERING",
    "CHEMICAL_ENGINEERING",
    "COMPUTER_ENGINEERING",
    "MECHANICAL_ENGINEERING",
    "MATERIALS_ENGINEERING",
    "MINING_ENGINEERING",
    "GEODETIC_ENGINEERING",
    "ELECTRONICS_ENGINEERING",
    "DATA_SCIENCE",
    "COMPUTER_SCIENCE",
    "COMMUNICATION",
    "JOURNALISM",
    "AGRICULTURE",
    "FORESTRY",
    "PSYCHOLOGY"
  ],
  "citizenship": "Filipino",
  "application_window": {
    "open": "08-01",
    "close": "09-01"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "return_service_required": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Critical GWA & Year Level Database Error: Live production database lists min_gwa: 75
- verification: Verified. | confidence: 95/100.

- CONTRADICTION/NOTE: entry GWA (88.00% or 2.00.) vs renewal (Maintain required term GWA (at least 88.00% / 2.0).)

---
