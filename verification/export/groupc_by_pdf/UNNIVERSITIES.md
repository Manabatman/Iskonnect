# DATABASE_V3_GROUPC_UNNIVERSITIES.pdf — Implementation Details

Scholarships: 19

## Ateneo Senior High School Financial Aid Grant1 (ID: 18)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen4.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: High School (Grade 11 entry)1.
- eligible_year_levels: Grade 111.
- incoming_freshman_only: Yes (Senior High School Grade 11 entry)1.
- existing_college: Ineligible1.
- graduate_students: Ineligible1.
- current_enrollment: Must be a graduating Grade 10 student eligible for admission to Ateneo Senior High School1.
- academic: High academic performance in Junior High School with strong conduct marks1.
- minimum_gwa: 90.00% (or equivalent high scholastic standing in JHS)3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: Family gross annual income must not exceed PHP 400,000.003.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Open to graduates of public, parochial, and private Junior High Schools1.
- courses: Applicable to all Ateneo Senior High School academic strands (STEM, ABM, HUMSS, GA)1.
- sectoral/hidden: Priority given to public and parochial high school completers1.
- work_experience: None
- good_moral: Required (Certificate of Good Moral Character from JHS Principal)2.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Application for financial aid is evaluated independently of the academic admission decision6.

### Timing
- who: Graduating Grade 10 Junior High School students1.
- freshmen/soph/junior/senior/grad/reapply: : No (restricted to incoming Grade 11 SHS applicants)1. | : No. | : No. | : No. | : No. | : No.
- window: Announced alongside the ASHS admission cycle (typically September)2. → Concurrent with the ASHS admission deadline (typically November/December)2. (Annual.; AY AY 2026–20272.)

### Renewal
- maintain_gwa: Must maintain required academic and conduct marks specified by ASHS OAA2.
- regular_load: Full-time credit enrollment in assigned SHS strand2.
- no_failures: Zero failing marks or major disciplinary infractions7.
- return_service: None required3.

### Disqualifiers / affiliations
- Combined parent annual gross income exceeding PHP 400,000.003.
- Submission of fraudulent income documents or altered report cards2.
- Incurring failing grades or severe behavioral reprimands7.

### Benefits (catalog)
- tuition: 100%, 75%, 50%, or 25% waiver of tuition and matriculation fees4.
- stipend: NOT SPECIFIED IN OFFICIAL SOURCE.
- allowance: Food and student learning allowance provided based on evaluated need4.

### Documents (operational hidden reqs)
- Parent's Personal Letter detailing household background and financial hardship2.
- Father's and Mother's Income Tax Return (ITR), Certificate of Employment, or BIR Tax Exemption2.
- Utility bills (electricity, water, telephone) for the last three months2.
- Grade 10 Report Card / Form 1382.
- Certificate of Good Moral Character2.

### Recommended schema
`json
{
  "education_level": [
    "High School"
  ],
  "eligible_year_levels": [
    11
  ],
  "incoming_year_only": true,
  "requires_current_enrollment": false,
  "minimum_gwa": 90.0,
  "income_limit": 400000,
  "school_type": [
    "Public JHS",
    "Parochial JHS",
    "Private JHS"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "application_window": {
    "open": "09-01",
    "close": "11-15"
  },
  "deadline_type": "estimated",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Risk: System presenting scholarship to Grade 10 students intending to enroll in
- verification: Verified3. | confidence: None

- CONTRADICTION/NOTE: entry GWA (90.00% (or equivalent high scholastic standing in JHS)3.) vs renewal (Must maintain required academic and conduct marks specified by ASHS OAA2.)

---

## Philippine Normal University Institutional Scholarship Program3 (ID: 23)

### Hard eligibility
- citizenship: Filipino citizen5.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: College (Undergraduate Teacher Education)3.
- eligible_year_levels: Years 1, 2, 3, and 43.
- incoming_freshman_only: No3.
- existing_college: Eligible3.
- graduate_students: Ineligible for undergraduate institutional track3.
- current_enrollment: Enrolled in a Bachelor of Secondary or Elementary Education program at PNU9.
- academic: Minimum GWA of 90.00% (or 2.00 PNU scale) with no failing grades3.
- minimum_gwa: 90.00%3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: Combined family gross annual income must not exceed PHP 400,000.003.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to Philippine Normal University campuses5.
- courses: Bachelor of Secondary Education, Bachelor of Elementary Education, Early Childhood Education9.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE.
- work_experience: None
- good_moral: Required10.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Must maintain full academic load each semester11.

### Timing
- who: Enrolled undergraduate students in teacher education programs at PNU5.
- freshmen/soph/junior/senior/grad/reapply: : Yes9. | : Yes9. | : Yes3. | : Yes3. | : No. | : Yes.
- window: Set per semester during registration week3. → Set per semester (typically 2 weeks after class commencement)3. (Semestral.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Maintain a minimum semestral GWA of 90.00% (2.00 or better)3.
- regular_load: Full-time course load per academic term11.
- no_failures: Zero dropped, incomplete, or failing marks11.
- return_service: None3.

### Disqualifiers / affiliations
- GWA falling below 90.00% or incurring an incomplete/failing grade3.
- Parent annual gross income exceeding PHP 400,000.003.
- Carrying an underload without prior academic deanship approval11.

### Benefits (catalog)
- tuition: Full waiver of remaining tuition and matriculation fees3.
- stipend: PHP 3,000.00 per month during active academic terms3.
- allowance: PHP 30,000.00 total annual stipend allowance3.

### Documents (operational hidden reqs)
- Duly accomplished PNU OSASS Scholarship Application Form3.
- Official Transcript of Records or Certified True Copy of Grades for preceding term9.
- Certificate of Enrollment / Registration Form showing full load10.
- Parents' Income Tax Return or BIR Certificate of Tax Exemption9.
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
    4
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": true,
  "minimum_gwa": 90.0,
  "income_limit": 400000,
  "school_type": [
    "SUC"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "08-15",
    "close": "09-15"
  },
  "deadline_type": "estimated",
  "cycle_type": "semester",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Risk: Recommending program to non-PNU education majors.
- verification: Verified3. | confidence: 92/100.

- CONTRADICTION/NOTE: entry GWA (90.00%3.) vs renewal (Maintain a minimum semestral GWA of 90.00% (2.00 or better)3.)

---

## UP Presidential Scholarship Program12 (ID: 24)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen12.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: College (Undergraduate)3.
- eligible_year_levels: Years 1, 2, 3, 4, and 53.
- incoming_freshman_only: No12.
- existing_college: Eligible12.
- graduate_students: Ineligible for undergraduate Presidential Scholarship (separate Graduate Presidential Fund exists)13.
- current_enrollment: Must be officially enrolled in a degree program in any UP constituent university12.
- academic: Outstanding scholastic record with a General Weighted Average (GWA) of at least 1.75 (or 95% equivalent)3.
- minimum_gwa: 1.75 on the UP grading scale (95.00% equivalent)3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: Family gross annual income must not exceed PHP 400,000.003.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to UP Constituent Universities (UPD, UPLB, UPM, UPV, UPC, UPMin, UPOU, UP Tacloban)12.
- courses: Open across all undergraduate degree programs12.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE.
- work_experience: None
- good_moral: Required12.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Number of awards is limited by annual vacant slot allocations across constituent units12.

### Timing
- who: Enrolled UP undergraduate students12.
- freshmen/soph/junior/senior/grad/reapply: : Yes (after earning initial term grades or based on UPCAT | : Yes12. | : Yes12. | : Yes12. | : No. | : Yes.
- window: Announced annually by OSFA at the start of the academic year (typically September)12. → Set per annual call (typically October)12. (Annual.; AY AY 2025–2026 / AY 2026–202712.)

### Renewal
- maintain_gwa: Maintain a cumulative GWA of 1.75 or better each academic term12.
- regular_load: Enrolled in a full academic load (at least 15 units per semester)12.
- no_failures: Zero failing grades (5.0), unremoved 4.0, or unremoved Incomplete (INC) marks7.
- return_service: None required3.

### Disqualifiers / affiliations
- GWA dropping below 1.75 or incurring a grade of 5.012.
- Dropping below full-time unit load without prior deanship authorization12.
- Family gross income exceeding PHP 400,000.003.

### Benefits (catalog)
- tuition: 100% tuition and miscellaneous fees coverage (under RA 10931 / UP GIAP framework)12.
- stipend: PHP 6,000.00 per month3.
- allowance: Book allowance of PHP 5,000.00 per semester12.

### Documents (operational hidden reqs)
- UP Form 5 / Official Certificate of Registration12.
- Certified True Copy of Grades / Transcript showing GWA <= 1.7512.
- Parents' Income Tax Return or BIR Certificate of Tax Exemption12.
- True Copy of Birth Certificate12.
- Certificate of Good Moral Character12.

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
  "income_limit": 400000,
  "school_type": [
    "SUC"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "09-01",
    "close": "10-15"
  },
  "deadline_type": "estimated",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Risk: Grade conversion error between percentage scales (95%) and UP decimal scale
- verification: Verified3. | confidence: 91/100.

- CONTRADICTION/NOTE: entry GWA (1.75 on the UP grading scale (95.00% equivalent)3.) vs renewal (Maintain a cumulative GWA of 1.75 or better each academic term12.)

---

## Ateneo de Manila University College Financial Aid Grant2 (ID: 40)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen5.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: College (Undergraduate)2.
- eligible_year_levels: Years 1, 2, 3, 4, and 52.
- incoming_freshman_only: No2.
- existing_college: Eligible (via upperclassmen financial aid application)2.
- graduate_students: Ineligible for undergraduate track2.
- current_enrollment: Accepted or currently enrolled in an undergraduate degree program at Ateneo de Manila University2.
- academic: Passing performance in the Ateneo College Entrance Test (ACET) and good academic standing6.
- minimum_gwa: 78.00% (or passing QPI standard for retention)3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: Combined gross annual income of parents must not exceed PHP 500,000.003.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to Ateneo de Manila University (Loyola Heights Campus)2.
- courses: Open across all undergraduate degree programs6.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE.
- work_experience: None
- good_moral: Required2.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Application for financial aid does not influence admission decisions6.

### Timing
- who: Incoming college freshmen, transferees, and ongoing Ateneo undergraduate students2.
- freshmen/soph/junior/senior/grad/reapply: : Yes2. | : Yes2. | : Yes2. | : Yes2. | : No2. | : Yes2.
- window: Concurrent with college admission opening (typically August/September)2. → October 15 (for SY 2027–2028: Thursday, 15 October 2026)2. (Annual.; AY AY 2026–2027 / AY 2027–20282.)

### Renewal
- maintain_gwa: Maintain required term QPI specified by the Office of Admission and Aid2.
- regular_load: Full-time credit enrollment per semester2.
- no_failures: Zero failing grades (F) or disciplinary probation7.
- return_service: None3.

### Disqualifiers / affiliations
- Parent annual gross income exceeding PHP 500,000.003.
- Failure to submit all required supporting financial documents by October 152.
- Incurring academic probation or serious disciplinary sanctions7.

### Benefits (catalog)
- tuition: 100%, 75%, 50%, or 25% coverage of tuition and fees4.
- stipend: PHP 3,000.00 per month (integrated into Student Learning Allowance)3.
- allowance: Food allowance provided based on assessed need4.

### Documents (operational hidden reqs)
- Parents' Personal Letter detailing family background and financial situation2.
- Certificate of Employment and Compensation or 2025 Annual Income Tax Return (ITR) / BIR Form 23162.
- Pay slips for the last two (2) months2.
- Utility bills (electricity, water, telephone) for the last three months2.
- Residence photos and house tour video2.
- Two (2) Scholarship Recommendation Forms submitted via go.ateneo.edu/scholarship-recommendations2.

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
  "requires_current_enrollment": false,
  "minimum_gwa": 78.0,
  "income_limit": 500000,
  "school_type": [
    "Private"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "08-01",
    "close": "10-15"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Risk: Students waiting for ACET admission results before submitting financial aid
- verification: Verified3. | confidence: 96/100.

- CONTRADICTION/NOTE: entry GWA (78.00% (or passing QPI standard for retention)3.) vs renewal (Maintain required term QPI specified by the Office of Admission and Aid2.)

---

## Ateneo Director's List Scholarship4 (ID: 41)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen5.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: College (Undergraduate entry)3.
- eligible_year_levels: Year 1 (Incoming Freshmen)3.
- incoming_freshman_only: Yes6.
- existing_college: Ineligible for initial award6.
- graduate_students: Ineligible6.
- current_enrollment: Must be an accepted incoming freshman in any undergraduate degree program at Ateneo de Manila University6.
- academic: Exceptional performance in the ACET and distinguished high school academic and co-curricular record4.
- minimum_gwa: 83.00% (or top ACET ranking equivalent)3.
- alt_class_rank: Awarded to top 150 ACET applicants4.
- income_ceilings: Uncapped (Merit-based award independent of family income)3.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to Ateneo de Manila University6.
- courses: Any undergraduate degree program of choice6.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE.
- work_experience: None
- good_moral: Required2.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Awarded automatically by the University Committee on Admission and Aid; no separate application form required4.

### Timing
- who: Incoming college freshmen taking the ACET4.
- freshmen/soph/junior/senior/grad/reapply: : No (awarded prior to freshman entry)6. | : No. | : No. | : No. | : No. | : No.
- window: Automatic evaluation upon filing ACET application4. → Concurrent with ACET registration closing2. (Annual.; AY AY 2026–20276.)

### Renewal
- maintain_gwa: Maintain required annual Quality Point Index (QPI) set by the OAA6.
- regular_load: Full-time academic credit load per semester2.
- no_failures: No failing grades or disciplinary sanctions7.
- return_service: None3.

### Disqualifiers / affiliations
- Declining admission to Ateneo de Manila University6.
- Failure to maintain required retention QPI6.
- Severe disciplinary infraction or honor code violation7.

### Benefits (catalog)
- tuition: PHP 100,000.00 annual fixed scholarship grant applicable toward tuition and fees4.
- stipend: NOT SPECIFIED IN OFFICIAL SOURCE.
- allowance: NOT SPECIFIED IN OFFICIAL SOURCE.

### Documents (operational hidden reqs)
- Ateneo College Application Form and ACET Examination Permit2.
- High School Transcript of Records / Form 1382.
- High School Principal / Counselor Recommendation Form2.

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
  "requires_current_enrollment": false,
  "minimum_gwa": 83.0,
  "income_limit": null,
  "school_type": [
    "Private"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "08-01",
    "close": "11-15"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Risk: Users attempting to submit a separate application form for Director's List.
- verification: Verified3. | confidence: 98/100.

- CONTRADICTION/NOTE: entry GWA (83.00% (or top ACET ranking equivalent)3.) vs renewal (Maintain required annual Quality Point Index (QPI) set by the OAA6.)

---

## Ateneo Law School Financial Aid Program3 (ID: 42)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen5.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: Graduate (Juris Doctor Program)3.
- eligible_year_levels: Years 1, 2, 3, and 4 (Juris Doctor)3.
- incoming_freshman_only: No3.
- existing_college: Ineligible (Restricted to law students)3.
- graduate_students: Yes (Juris Doctor is a professional law degree)3.
- current_enrollment: Must be admitted or enrolled in the Juris Doctor program at Ateneo Law School3.
- academic: Bachelor's degree completion, passing the Ateneo Law Admission Test (ALAT), and maintaining satisfactory academic standing3.
- minimum_gwa: 82.00% (or equivalent law school QPI requirement)3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: Combined family gross annual income must not exceed PHP 600,000.003.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to Ateneo Law School (Rockwell Campus)3.
- courses: Juris Doctor (JD) degree program3.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE.
- work_experience: None
- good_moral: Required2.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Must reapply annually for financial grant continuation3.

### Timing
- who: Incoming 1st-year Juris Doctor students and ongoing Ateneo Law students3.
- freshmen/soph/junior/senior/grad/reapply: : Yes (1st year JD students)3. | : Yes (2nd year JD students)3. | : Yes (3rd year JD students)3. | : Yes (4th year JD students)3. | : Yes (Bachelor's degree graduates entering law school)3. | : Yes3.
- window: Announced alongside law school admission results (typically May)3. → Set per annual law school calendar (typically June/July)3. (Annual.; AY AY 2025–2026 / AY 2026–20273.)

### Renewal
- maintain_gwa: Must maintain required Quality Point Index (QPI) specified by Ateneo Law School3.
- regular_load: Full-time law enrollment per semester19.
- no_failures: Zero failing marks (F) or unremoved incomplete grades in law subjects7.
- return_service: None3.

### Disqualifiers / affiliations
- Family gross annual income exceeding PHP 600,000.003.
- Academic failure or dropping below required law school QPI7.
- Honor code violation or disciplinary action by Ateneo Law School7.

### Benefits (catalog)
- tuition: Partial to 100% tuition and fee waiver3.
- stipend: NOT SPECIFIED IN OFFICIAL SOURCE.
- allowance: Book allowance provided for full-grant recipients3.

### Documents (operational hidden reqs)
- Ateneo Law School Financial Aid Application Form2.
- Latest Income Tax Return (ITR) of applicant, parents, or spouse2.
- Official Transcript of Records (TOR) from pre-law Bachelor's degree2.
- Certificate of Employment and pay slips (if employed)2.
- Certificate of Good Moral Character2.

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
  "minimum_gwa": 82.0,
  "income_limit": 600000,
  "degree_program_restricted": [
    "Juris Doctor"
  ],
  "school_type": [
    "Private"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "05-01",
    "close": "06-30"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Risk: Displaying scholarship to undergraduate pre-law students.
- verification: Verified3. | confidence: 96/100.

- CONTRADICTION/NOTE: entry GWA (82.00% (or equivalent law school QPI requirement)3.) vs renewal (Must maintain required Quality Point Index (QPI) specified by Ateneo Law School3.)

---

## DLSU Star Scholars Program20 (ID: 43)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen20.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: College (Undergraduate entry)3.
- eligible_year_levels: Year 1 (Incoming Freshmen)3.
- incoming_freshman_only: Yes20.
- existing_college: Ineligible for initial award20.
- graduate_students: Ineligible for initial entry (includes post-undergrad graduate grant)20.
- current_enrollment: Top-ranked applicant accepted into any undergraduate program at DLSU20.
- academic: Top performance in the DLSU College Admission Test (DCAT) and successful interview evaluation20.
- minimum_gwa: 90.00% (or top DCAT score equivalent)3.
- alt_class_rank: Selected among top DCAT examinees nationwide20.
- income_ceilings: Uncapped (Merit-based award)3.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to De La Salle University (Manila and Laguna campuses)20.
- courses: Open across all undergraduate programs (including BS Human Biology and ladderized master's)20.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE.
- work_experience: None
- good_moral: Required20.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Scholars receive continuous faculty mentorship from University Fellows throughout residency20.

### Timing
- who: Top-performing examinees in the DLSU College Admission Test20.
- freshmen/soph/junior/senior/grad/reapply: : No (awarded prior to freshman entry)20. | : No. | : No. | : No. | : No. | : No.
- window: Automatic consideration upon taking the DCAT20. → Interview screening completed prior to confirmation period (May/June)22. (Annual.; AY AY 2026–202722.)

### Renewal
- maintain_gwa: Maintain required Term GPA (TGPA) and Cumulative GPA (CGPA) specified by OAS24.
- regular_load: Full-time credit load per trimester20.
- no_failures: Zero failing marks or withdrawn subjects24.
- return_service: None3.

### Disqualifiers / affiliations
- Failure to maintain required CGPA retention standard24.
- Incurring a failing or withdrawn grade24.
- Disciplinary sanction or violation of the DLSU Student Handbook24.

### Benefits (catalog)
- tuition: Full 100% waiver of tuition, miscellaneous, and laboratory fees20.
- stipend: PHP 8,000.00 per month (living and accommodation stipend)3.
- allowance: Coverage for modest accommodation, meals, and books20.

### Documents (operational hidden reqs)
- DLSU College Admission Test (DCAT) Application and Results20.
- Senior High School Report Card / Form 13822.
- Recommendation letter from SHS Principal/Counselor20.
- University Fellows Interview Evaluation20.

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
  "requires_current_enrollment": false,
  "minimum_gwa": 90.0,
  "income_limit": null,
  "school_type": [
    "Private"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "01-15",
    "close": "05-17"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Risk: Displaying Star Scholars program to students with average DCAT scores.
- verification: Verified3. | confidence: 90/100.

- CONTRADICTION/NOTE: entry GWA (90.00% (or top DCAT score equivalent)3.) vs renewal (Maintain required Term GPA (TGPA) and Cumulative GPA (CGPA) specified by OAS24.)

---

## DLSU Archer Achievers Scholarship Program23 (ID: 44)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen23.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: College (Undergraduate entry)3.
- eligible_year_levels: Year 1 (Incoming Freshmen)3.
- incoming_freshman_only: Yes23.
- existing_college: Ineligible23.
- graduate_students: Ineligible23.
- current_enrollment: Enrolled in a Philippine private, public, or science high school at the time of application to DLSU23.
- academic: Among top examinees in the DCAT based on the Weighted Admission Index23.
- minimum_gwa: 83.00% (or top Weighted Admission Index score)3.
- alt_class_rank: Top percentile rank in DCAT examinee cohort23.
- income_ceilings: Uncapped (Merit-based award)3.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to De La Salle University23.
- courses: Open across all undergraduate programs (including ladderized BS/MS and BS Human Bio)23.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE.
- work_experience: None
- good_moral: Required23.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Grantees no longer undergo an interview process, but may choose to interview for scholarship upgrades (e.g., STAR, Vaugirard, Gokongwei)22.

### Timing
- who: Top DCAT examinees graduating from Philippine high schools23.
- freshmen/soph/junior/senior/grad/reapply: : No (automatically awarded upon college admission)23. | : No. | : No. | : No. | : No. | : No.
- window: Automatic evaluation upon taking the DCAT22. → Official notification letter sent via email prior to confirmation23. (Annual.; AY AY 2025–2026 / AY 2026–202722.)

### Renewal
- maintain_gwa: Maintain required Term GPA (TGPA) and Cumulative GPA (CGPA) per trimester24.
- regular_load: Full-time credit enrollment23.
- no_failures: Zero failing grades or unapproved course withdrawals24.
- return_service: None3.

### Disqualifiers / affiliations
- Failure to meet required trimester CGPA retention threshold24.
- Incurring failing or withdrawn marks24.
- Misconduct violating DLSU disciplinary standards24.

### Benefits (catalog)
- tuition: 100% waiver of tuition, miscellaneous, and other fees from term 1 through graduation23.
- stipend: None (Stipends are strictly NOT part of Archer Achiever benefits)25.
- allowance: None25.

### Documents (operational hidden reqs)
- DLSU College Admission Test (DCAT) Application23.
- Official Senior High School Transcript / Form 13825.
- Official Archer Achiever Award Letter issued by DLSU OAS23.

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
  "requires_current_enrollment": false,
  "minimum_gwa": 83.0,
  "income_limit": null,
  "school_type": [
    "Private"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "01-15",
    "close": "05-17"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Risk: Matching engine displaying Archer Achievers as including a monthly living stipend.
- verification: Verified3. | confidence: 98/100.

- CONTRADICTION/NOTE: entry GWA (83.00% (or top Weighted Admission Index score)3.) vs renewal (Maintain required Term GPA (TGPA) and Cumulative GPA (CGPA) per trimester24.)

---

## UST San Martin de Porres Equity Scholarship26 (ID: 45)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen5.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: College (Undergraduate)3.
- eligible_year_levels: Years 1, 2, 3, 4, and 53.
- incoming_freshman_only: No26.
- existing_college: Eligible26.
- graduate_students: Ineligible for undergraduate equity track26.
- current_enrollment: Must be officially enrolled in an undergraduate degree program at the University of Santo Tomas26.
- academic: Passing academic record with a General Weighted Average (GWA) of at least 85.00% (2.25 UST scale)3.
- minimum_gwa: 85.00%3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: Combined family gross annual income must not exceed PHP 300,000.003.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to the University of Santo Tomas (España, Manila campus)26.
- courses: Open across all UST faculties, colleges, and institutes26.
- sectoral/hidden: Special consideration for OWWA dependents, PD577 beneficiaries, and indigent candidates26.
- work_experience: None
- good_moral: Required (Good Moral Certificate issued by UST OSA)26.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Must submit complete financial indigency documents via the OSA SAAF portal26.

### Timing
- who: Enrolled UST undergraduate students in need of financial assistance26.
- freshmen/soph/junior/senior/grad/reapply: : Yes26. | : Yes26. | : Yes26. | : Yes26. | : No. | : Yes.
- window: Announced by UST OSA per semester/academic year26. → Set per term calendar26. (Annual / Semestral renewal.; AY AY 2025–2026 / AY 2026–202726.)

### Renewal
- maintain_gwa: Maintain a minimum semestral GWA of 85.00% (2.25)3.
- regular_load: Enrolled in full term load per UST curriculum26.
- no_failures: Zero failing grades or unremoved 3.0/INC marks7.
- return_service: None3.

### Disqualifiers / affiliations
- Family gross annual income exceeding PHP 300,000.003.
- Incurring failing grades or academic probation7.
- Behavioral reprimand or disciplinary sanction by UST Student Conduct Board26.

### Benefits (catalog)
- tuition: Partial to 100% waiver of tuition fees (average annual grant value PHP 45,000.00)3.
- stipend: NOT SPECIFIED IN OFFICIAL SOURCE.
- allowance: Integrated into tuition discount structure3.

### Documents (operational hidden reqs)
- UST OSA SAAF Application Form26.
- Official Transcript of Records / Grade Report showing GWA >= 85.00%3.
- Parents' Income Tax Return (ITR), BIR Tax Exemption, or Barangay Certificate of Indigency26.
- Certificate of Good Moral Character26.
- Electric and water utility bills for the last 3 months2.

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
  "school_type": [
    "Private"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "08-15",
    "close": "09-30"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Risk: Recommending program to students attending non-UST campuses or non-UST
- verification: Verified3. | confidence: 98/100.

- CONTRADICTION/NOTE: entry GWA (85.00%3.) vs renewal (Maintain a minimum semestral GWA of 85.00% (2.25)3.)

---

## Mindanao State University System Admission and Scholarship Examination (MSU-SASE) Academic Scholarship3 (ID: 46)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen5.
- residency/destination: Resident of regions covered by the MSU System (BARMM, Regions IX, X, XI, XII, XIII, CARAGA, and Palawan)3.
- education_level: College (Undergraduate entry)3.
- eligible_year_levels: Year 1 (Incoming Freshmen)3.
- incoming_freshman_only: Yes27.
- existing_college: Ineligible27.
- graduate_students: Ineligible27.
- current_enrollment: Must take the MSU-SASE and qualify for admission into any MSU campus (Main Marawi, IIT, Gensan, Maguindanao, Naawan, Sulu, Tawi-Tawi, Buug)27.
- academic: Top score ranking in the annual MSU-SASE27.
- minimum_gwa: 85.00% (or equivalent top SASE percentile score)3.
- alt_class_rank: Selected based on national SASE score ranking tiers27.
- income_ceilings: Uncapped (Merit-based award)3.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to MSU System campuses27.
- courses: Open across all undergraduate degree programs offered by the MSU System27.
- sectoral/hidden: Special slots for Indigenous Cultural Communities and Bangsamoro constituents27.
- work_experience: None
- good_moral: Required27.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Must enroll in the MSU campus assigned based on SASE qualification27.

### Timing
- who: Graduating Senior High School students registering for the MSU-SASE27.
- freshmen/soph/junior/senior/grad/reapply: : No (awarded strictly upon SASE entry)27. | : No. | : No. | : No. | : No. | : No.
- window: SASE registration opens annually in September/October27. → SASE registration closes in December/January; exam administered in November/February27. (Annual.; AY AY 2026–202727.)

### Renewal
- maintain_gwa: Maintain required Grade Point Average (GPA) per semester set by MSU System policy27.
- regular_load: Full-time academic credit enrollment27.
- no_failures: Zero failing marks (5.0) in any academic subject27.
- return_service: None3.

### Disqualifiers / affiliations
- Failing to meet SASE cut-off score for academic scholarship tier27.
- Dropping below required semestral GPA retention mark27.
- Transferring to a non-MSU institution27.

### Benefits (catalog)
- tuition: 100% tuition and registration fee waiver at all MSU campuses3.
- stipend: Semestral living allowance provided3.
- allowance: Total annual stipend grant value of PHP 20,000.003.

### Documents (operational hidden reqs)
- MSU-SASE Application Form and Exam Permit27.
- Certified True Copy of Grade 11 and Grade 12 Report Cards27.
- Certificate of Good Moral Character27.
- PSA Birth Certificate27.

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
  "requires_current_enrollment": false,
  "minimum_gwa": 85.0,
  "income_limit": null,
  "regions": [
    "BARMM",
    "Region IX - Zamboanga Peninsula",
    "Region X - Northern Mindanao",
    "Region XI - Davao",
    "Region XII - Soccsksargen",
    "Region XIII - Caraga"
  ],
  "school_type": [
    "SUC"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "09-15",
    "close": "01-15"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Risk: Recommending scholarship to upperclassmen or transfer students.
- verification: Verified3. | confidence: 95/100.

- CONTRADICTION/NOTE: entry GWA (85.00% (or equivalent top SASE percentile score)3.) vs renewal (Maintain required Grade Point Average (GPA) per semester set by MSU System policy27.)

---

## PUP Entrance Scholarship Program29 (ID: 68)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen30.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: College (Undergraduate entry)3.
- eligible_year_levels: Year 1 (Incoming Freshmen)3.
- incoming_freshman_only: Yes30.
- existing_college: Ineligible (Upperclassmen apply for Resident Scholarship instead)30.
- graduate_students: Ineligible29.
- current_enrollment: Must pass the PUP College Entrance Test (PUPCET) and enroll as a first-year student30.
- academic: High scholastic or specialized achievement under recognized qualification categories30.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Governed by category qualification)30.
- alt_class_rank: Top 10 bracket of graduating class of at least 500 graduates from a public high school30.
- income_ceilings: Uncapped for academic/artist tracks; indigent income criteria for First Gen/Indigent track30.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to the Polytechnic University of the Philippines (Main Sta. Mesa and branches/campuses)9.
- courses: Open across all undergraduate degree programs30.
- sectoral/hidden: Encompasses 11 official categories: (1) Public HS Top 10 (>=500 grads); (2) Cultural Artist; (3) Student Athlete; (4) Creative Media Artist; (5) Campus Journalist; (6) Differently-abled / PWD; (7) ALS Graduate; (8) Indigenous Peoples (IP); (9) Solo Parent; (10) Sangguniang Kabataan (SK) Official; (11) First Generation / Indigent Student30.
- work_experience: None
- good_moral: Required (Certificate of Good Moral Character)31.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Scholars receive formal "Entrance Scholar of PUP" certification and endorsement to corporate CSR grantors30.

### Timing
- who: Incoming first-year students qualifying under any of the 11 official categories30.
- freshmen/soph/junior/senior/grad/reapply: : Yes (during initial entry term)30. | : No. | : No. | : No. | : No. | : No.
- window: Concurrent with freshmen enrollment schedule30. → Specified per enrollment period by PUP OSFA30. (Annual.; AY AY 2025–2026 / AY 2026–202729.)

### Renewal
- maintain_gwa: Must transition to PUP Resident Scholarship (President's Lister GWA >= 1.50 or Dean's Lister GWA >= 1.75)33.
- regular_load: Full-time academic load per term30.
- no_failures: No grade lower than 2.50 in any subject33.
- return_service: None3.

### Disqualifiers / affiliations
- Failure to submit principal's sealed certification of category qualification30.
- Failing grade or mark below 2.50 in any term33.
- Submission of false credentials34.

### Benefits (catalog)
- tuition: 100% waiver of tuition and other school fees (under RA 10931 Universal Access)30.
- stipend: NOT SPECIFIED IN OFFICIAL SOURCE.
- allowance: Endorsement to private corporate/foundation grantors for external stipends29.

### Documents (operational hidden reqs)
- Certification from SHS Principal (with dry seal) attesting to category (e.g., Top 10 of >=500 grads, Campus Journalist, Cultural Artist)30.
- Form 138 / Grade 12 Senior High School Report Card31.
- Certificate of Good Moral Character31.
- PSA Birth Certificate31.
- Category Proof (e.g., NCIP Certificate for IP, PWD ID, SK Oath of Office, ALS Rating)12.

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
  "requires_current_enrollment": false,
  "minimum_gwa": null,
  "rank_cutoff_alternative": 10,
  "income_limit": null,
  "school_type": [
    "SUC"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "06-01",
    "close": "08-31"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": false,
  "first_time_only": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Risk: Recommending program to public high school top 10 graduates whose graduating
- verification: Verified3. | confidence: None

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Governed by category qualification)30.) vs renewal (Must transition to PUP Resident Scholarship (President's Lister GWA >= 1.50 or Dean's Lister GWA >= 1.75)33.)

---

## PUP Student Assistantship Program29 (ID: 69)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen30.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: College (Undergraduate)3.
- eligible_year_levels: Years 2, 3, 4, and 530.
- incoming_freshman_only: No30.
- existing_college: Yes (Requires at least 2nd-year standing)30.
- graduate_students: Ineligible29.
- current_enrollment: Must be currently enrolled as a regular student with at least two semesters (1 year) of residency at PUP30.
- academic: Passed all enrolled subjects in the preceding semester30.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Requires 100% passing rate in prior term)30.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE (Targeted at financially needy regular students)29.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to PUP Main Campus and constituent branches29.
- courses: Open across all undergraduate academic programs30.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE.
- work_experience: None
- good_moral: Required31.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Must be officially endorsed by the head of the PUP office/department to be served30.

### Timing
- who: Regular 2nd, 3rd, 4th, and 5th year PUP undergraduate students30.
- freshmen/soph/junior/senior/grad/reapply: : No (Requires at least 2nd-year standing and 1 year | : Yes30. | : Yes30. | : Yes30. | : No. | : Yes (Subject to semestral renewal)30.
- window: One week after the Adjustment Period of each semester30. → Set per semestral notice by PUP OSFA30. (Semestral renewal.; AY AY 2025–2026 / AY 2026–202729.)

### Renewal
- maintain_gwa: Must pass 100% of enrolled units in the preceding semester30.
- regular_load: Maintain regular student status per semester30.
- no_failures: Zero failing grades in any subject30.
- return_service: Work commitment of up to 24 hours per week or 100 hours per month31.

### Disqualifiers / affiliations
- Incurring a failing, dropped, or incomplete mark in the preceding term30.
- Irregular student status or year level lower than 2nd Year30.
- Exceeding the maximum limit of 24 work hours per week or 100 hours per month31.

### Benefits (catalog)
- tuition: None (Tuition is already covered under RA 10931)35.
- stipend: Hourly compensation of PHP 25.00 / hour31.
- allowance: Maximum monthly compensation of PHP 2,500.00 (based on max 100 hours/month)31.

### Documents (operational hidden reqs)
- Student Assistantship Endorsement Form (PUP-SAEF-5-OFSS-015) signed by Office Head29.
- Official Certificate of Registration (Registration Certificate) for current term30.
- Copy of Grades / Transcript for the preceding semester30.
- Student Personal Data Sheet29.

### Recommended schema
`json
{
  "education_level": [
    "College"
  ],
  "eligible_year_levels": [
    2,
    3,
    4,
    5
  ],
  "incoming_year_only": false,
  "requires_current_enrollment": true,
  "minimum_gwa": null,
  "income_limit": null,
  "school_type": [
    "SUC"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "09-15",
    "close": "10-15"
  },
  "deadline_type": "exact",
  "cycle_type": "semester",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Risk: Displaying assistantship vacancies to 1st-year freshmen.
- verification: Verified3. | confidence: 96/100.

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Requires 100% passing rate in prior term)30.) vs renewal (Must pass 100% of enrolled units in the preceding semester30.)

---

## UP College of Law Scholarship Program17 (ID: 70)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen12.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: Graduate (Juris Doctor Program)3.
- eligible_year_levels: Years 1, 2, 3, and 4 (Juris Doctor)3.
- incoming_freshman_only: No17.
- existing_college: Ineligible (Restricted to law students)17.
- graduate_students: Yes (Juris Doctor professional program)17.
- current_enrollment: Must be a bona fide Juris Doctor student at UP College of Law17.
- academic: Need is the primary selection criterion; academic merit is secondary17.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated holistically based on hardship)17.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: Evaluated based on Income Tax Return and household asset verification form17.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to UP College of Law (Diliman and BGC campuses)17.
- courses: Juris Doctor (JD) degree program17.
- sectoral/hidden: Diversity considerations explicitly prioritized: LGBTQIA+ individuals, members of Indigenous Peoples (IP) communities, Persons with Disabilities (PWDs), single parents, and aspiring first-generation lawyers17.
- work_experience: None
- good_moral: Required17.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Applicants must forego other active scholarship awards upon acceptance to UP Law Scholarship17. Background checks and home asset inspections are conducted17.

### Timing
- who: All bona fide Juris Doctor students at UP College of Law17.
- freshmen/soph/junior/senior/grad/reapply: : Yes (1st year JD students)17. | : Yes (2nd year JD students)17. | : Yes (3rd year JD students)17. | : Yes (4th year JD students)17. | : Yes (LAE applicants receiving application fee waivers)17. | : Yes17.
- window: June 30 annually17. → July 20 annually (Deadlines strictly applied)17. (Annual.; AY AY 2025–2026 / AY 2026–202717.)

### Renewal
- maintain_gwa: Maintain good academic standing per UP Law academic retention rules17.
- regular_load: Full-time credit enrollment in Juris Doctor curriculum17.
- no_failures: Compliance with law deanship retention rules17.
- return_service: Scholars render student service assistance to the UP College of Law17.

### Disqualifiers / affiliations
- Holding another active scholarship award without submitting an official withdrawal letter17.
- Misrepresentation during household asset inspection or background check17.
- Failure to submit all required ITRs/photos before the strict July 20 deadline17.

### Benefits (catalog)
- tuition: 100% waiver of tuition and miscellaneous fees17.
- stipend: PHP 10,000.00 per month for 3 to 4 months per semester (Tier 1 & Tier 2 scholars)17.
- allowance: Internet and book allowance set at PHP 10,000.00 per semester17.

### Documents (operational hidden reqs)
- Accomplished UP Law Online Scholarship Application Form17.
- Letter of Intent detailing financial hardship, family dynamics, and personal circumstances17.
- Latest Income Tax Return (ITR) of applicant, spouse, parents, or supporting siblings17.
- Household Asset Photos (front of home, living room, kitchen, bedroom, and major appliances)17.
- Landbank Account Details for stipend disbursement17.

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
  "minimum_gwa": null,
  "income_limit": null,
  "degree_program_restricted": [
    "Juris Doctor"
  ],
  "school_type": [
    "SUC"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "06-30",
    "close": "07-20"
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
- ● Risk: System assuming Socialized Tuition System (STS) discount precludes UP Law
- verification: Verified3. | confidence: 95/100.

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated holistically based on hardship)17.) vs renewal (Maintain good academic standing per UP Law academic retention rules17.)

---

## Ateneo Freshman Merit Scholarship (AFMS)4 (ID: 104)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen5.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: College (Undergraduate entry)3.
- eligible_year_levels: Year 1 (Incoming Freshmen)3.
- incoming_freshman_only: Yes4.
- existing_college: Ineligible6.
- graduate_students: Ineligible6.
- current_enrollment: Must be a top-ranked applicant accepted into any undergraduate degree program at Ateneo de Manila University6.
- academic: Exceptional ACET score ranking, outstanding high school academic performance, and demonstrated leadership roles4.
- minimum_gwa: 90.00% (or top 50 ACET examinee rank)3.
- alt_class_rank: Ranked within the top 50 applicants nationwide4.
- income_ceilings: Uncapped (Merit-based award independent of family income)3.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to Ateneo de Manila University (Loyola Heights)6.
- courses: Scholars may choose any undergraduate degree program of their choice6.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE.
- work_experience: None
- good_moral: Required2.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Awarded automatically; no separate application form required4.

### Timing
- who: High school seniors registering for the ACET4.
- freshmen/soph/junior/senior/grad/reapply: : No (awarded strictly upon freshman admission)6. | : No. | : No. | : No. | : No. | : No.
- window: Automatic evaluation upon filing ACET application4. → Concurrent with ACET application deadline2. (Annual.; AY AY 2026–20276.)

### Renewal
- maintain_gwa: Maintain required annual Quality Point Index (QPI) set by OAA for merit scholars6.
- regular_load: Full-time credit enrollment per semester2.
- no_failures: Zero failing marks or unremoved incomplete grades7.
- return_service: None3.

### Disqualifiers / affiliations
- Declining enrollment at Ateneo de Manila University6.
- Falling below the required merit QPI retention mark6.
- Major disciplinary sanction or violation of university rules7.

### Benefits (catalog)
- tuition: Full 100% waiver of tuition and matriculation fees for the entire duration of the chosen undergraduate degree4.
- stipend: NOT SPECIFIED IN OFFICIAL SOURCE.
- allowance: Annual book and learning allowance provided4.

### Documents (operational hidden reqs)
- Ateneo College Application Form and ACET Permit2.
- Senior High School Transcript of Records / Form 1382.
- Principal / Guidance Counselor Endorsement Form attesting to leadership roles2.

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
  "requires_current_enrollment": false,
  "minimum_gwa": 90.0,
  "income_limit": null,
  "school_type": [
    "Private"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "08-01",
    "close": "11-15"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Risk: Users misinterpreting AFMS as requiring a separate application form from ACET.
- verification: Verified3. | confidence: 98/100.

- CONTRADICTION/NOTE: entry GWA (90.00% (or top 50 ACET examinee rank)3.) vs renewal (Maintain required annual Quality Point Index (QPI) set by OAA for merit scholars6.)

---

## Ateneo Magis Scholarship4 (ID: 105)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen5.
- residency/destination: Applicants are selected across 4 geographic regions: NCR, Luzon, Visayas, and Mindanao4.
- education_level: College (Undergraduate entry)3.
- eligible_year_levels: Year 1 (Incoming Freshmen)3.
- incoming_freshman_only: Yes4.
- existing_college: Ineligible for initial award6.
- graduate_students: Ineligible6.
- current_enrollment: Must apply for Financial Aid and be admitted to an undergraduate degree program at Ateneo de Manila University6.
- academic: Outstanding scholastic achievement in Senior High School and high ACET performance4.
- minimum_gwa: 85.00% (or top financial aid applicant standing)3.
- alt_class_rank: Selected as the top financial aid recipient in the respective geographic island group4.
- income_ceilings: Family gross annual income must demonstrate severe financial constraint (capped at PHP 250,000.00)3.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to Ateneo de Manila University6.
- courses: Open across all 4- and 5-year undergraduate degree programs4.
- sectoral/hidden: Underprivileged candidates with potential for servant leadership4.
- work_experience: None
- good_moral: Required2.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Only applicants who qualify for an Ateneo Financial Aid Grant are considered for the Magis Scholarship4.

### Timing
- who: Incoming college freshmen applying for Ateneo Financial Aid4.
- freshmen/soph/junior/senior/grad/reapply: : No (awarded upon freshman entrance)6. | : No. | : No. | : No. | : No. | : No.
- window: Concurrent with Ateneo Financial Aid Application opening (August)2. → October 15 (Financial Aid submission deadline)2. (Annual.; AY AY 2025–2026 / AY 2026–20274.)

### Renewal
- maintain_gwa: Maintain required QPI standard set by OAA6.
- regular_load: Full-time credit enrollment2.
- no_failures: Zero failing grades7.
- return_service: None required3.

### Disqualifiers / affiliations
- Failure to qualify for an Ateneo Financial Aid Grant4.
- Parent annual gross income exceeding PHP 250,000.003.
- Severe disciplinary infraction or academic failure7.

### Benefits (catalog)
- tuition: 100% waiver of tuition and matriculation fees for any 4- or 5-year course4.
- stipend: PHP 4,000.00 per month (food and living allowance)3.
- allowance: Student learning, books, printing, and school supplies allowance4.

### Documents (operational hidden reqs)
- Complete Ateneo Financial Aid Application Package (Parents' letter, ITR, pay slips, utility bills)2.
- Residence Photos and House Tour Video2.
- High School Transcript of Records / Form 1382.
- Two (2) Recommendation Forms2.

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
  "requires_current_enrollment": false,
  "minimum_gwa": 85.0,
  "income_limit": 250000,
  "school_type": [
    "Private"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "08-01",
    "close": "10-15"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Risk: Displaying Magis Scholarship to candidates who did not complete the prerequisite
- verification: Verified3. | confidence: 98/100.

- CONTRADICTION/NOTE: entry GWA (85.00% (or top financial aid applicant standing)3.) vs renewal (Maintain required QPI standard set by OAA6.)

---

## St. La Salle Financial Assistance Grant21 (ID: 106)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen21.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: College (Undergraduate)3.
- eligible_year_levels: Years 1, 2, 3, 4, and 53.
- incoming_freshman_only: No22.
- existing_college: Eligible (Separate application calls for current students)22.
- graduate_students: Ineligible for undergraduate track (Separate St. Mutien Marie Grant exists)20.
- current_enrollment: Must pass the DLSU College Admissions Test (DCAT) or be an ongoing regular DLSU undergraduate22.
- academic: Evaluated based on high school academic competence and DCAT score22.
- minimum_gwa: 85.00%3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: Structured into 3 tiered income brackets: Bracket A (< PHP 450,000: 100% tuition + stipend); Bracket B (PHP 450,000–1,000,000: 100% tuition); Bracket C (PHP 1,000,001–1,800,000: Partial tuition waiver)22.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to De La Salle University (Manila and Laguna campuses)22.
- courses: Open across all undergraduate degree programs22.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE.
- work_experience: None
- good_moral: Required22.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Grantees awarded 100% waivers are exempted from paying the PHP 10,000 reservation fee22.

### Timing
- who: DCAT examinees, Special DCAT examinees, and ongoing DLSU undergraduate students22.
- freshmen/soph/junior/senior/grad/reapply: : Yes22. | : Yes22. | : Yes22. | : Yes22. | : No22. | : Yes22.
- window: April 17 for DCAT applicants; May 26 for Special DCAT applicants22. → May 17 for DCAT applicants; June 1 for Special DCAT applicants (No extensions)22. (Annual / Semestral.; AY AY 2026–202722.)

### Renewal
- maintain_gwa: Maintain required Term GPA and Cumulative GPA per trimester22.
- regular_load: Enrolled in full-time credit load22.
- no_failures: Zero failing marks or unapproved course withdrawals24.
- return_service: None3.

### Disqualifiers / affiliations
- Combined family gross annual income exceeding PHP 1,800,000.0022.
- Dropping below required trimester GPA retention mark24.
- Major disciplinary infraction or submission of falsified ITRs22.

### Benefits (catalog)
- tuition: Full 100% or partial tuition and fees waiver depending on income bracket22.
- stipend: PHP 3,500.00 per month (awarded to Bracket A scholars with family income < PHP 450k)3.
- allowance: Integrated into monthly stipend package22.

### Documents (operational hidden reqs)
- Accomplished St. La Salle Financial Assistance Online Application Form22.
- Parents' Income Tax Return (ITR), BIR Certificate of Tax Exemption, or Employment Contract22.
- Electric and water utility bills for the last 3 months22.
- High School Transcript of Records / Report Cards22.
- Letter of Explanation addressed to OAS Director for any missing document22.

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
  "requires_current_enrollment": false,
  "minimum_gwa": 85.0,
  "income_limit": 1800000,
  "school_type": [
    "Private"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "04-17",
    "close": "05-17"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Risk: Engine disqualifying applicants earning between PHP 700,000 and PHP 1,800,000
- verification: Verified3. | confidence: 96/100.

- CONTRADICTION/NOTE: entry GWA (85.00%3.) vs renewal (Maintain required Term GPA and Cumulative GPA per trimester22.)

---

## DLSU Vaugirard Scholarship Program20 (ID: 107)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen20.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: College (Undergraduate entry)3.
- eligible_year_levels: Year 1 (Incoming Freshmen)3.
- incoming_freshman_only: Yes20.
- existing_college: Ineligible20.
- graduate_students: Ineligible20.
- current_enrollment: Must be a graduating student from a Philippine Public or Science High School accepted to DLSU20.
- academic: Among top examinees in the DLSU College Admission Test (DCAT)20.
- minimum_gwa: 88.00% (or top DCAT score equivalent)3.
- alt_class_rank: Selected by University Committee screening from top public/science DCAT examinees20.
- income_ceilings: Combined family gross annual income must not exceed PHP 300,000.003.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to graduates of Philippine Public High Schools and Science High Schools enrolling at DLSU20.
- courses: Open across all undergraduate degree programs20.
- sectoral/hidden: Public and Science High School completers20.
- work_experience: None
- good_moral: Required20.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Candidates are invited for committee screening; cash incentives are awarded to scholars graduating with Latin honors20.

### Timing
- who: Graduating public and science high school seniors taking the DCAT20.
- freshmen/soph/junior/senior/grad/reapply: : No (awarded upon freshman entry)20. | : No. | : No. | : No. | : No. | : No.
- window: Automatic screening upon DCAT administration20. → Committee interviews conducted in April/May prior to confirmation20. (Annual.; AY AY 2026–202722.)

### Renewal
- maintain_gwa: Maintain required trimester GPA retention mark set by OAS24.
- regular_load: Full-time credit enrollment per trimester20.
- no_failures: Zero failing grades24.
- return_service: None3.

### Disqualifiers / affiliations
- High school origin from a private non-science institution20.
- Parent gross annual income exceeding PHP 300,000.003.
- Failure to maintain trimester GPA retention standard24.

### Benefits (catalog)
- tuition: 100% waiver of tuition, miscellaneous, and laboratory fees throughout stay at DLSU20.
- stipend: PHP 4,000.00 per month (monthly living stipend)3.
- allowance: Modest accommodation and allowance coverage20.

### Documents (operational hidden reqs)
- DCAT Application Form and Results20.
- Public / Science High School Form 138 / Transcript20.
- Parents' Income Tax Return or BIR Tax Exemption Certificate12.
- Certificate of Good Moral Character20.

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
  "requires_current_enrollment": false,
  "minimum_gwa": 88.0,
  "income_limit": 300000,
  "school_type": [
    "Public High School",
    "Science High School"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "01-15",
    "close": "05-17"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Risk: Matching engine displaying Vaugirard to private non-science high school graduates.
- verification: Verified3. | confidence: 98/100.

- CONTRADICTION/NOTE: entry GWA (88.00% (or top DCAT score equivalent)3.) vs renewal (Maintain required trimester GPA retention mark set by OAS24.)

---

## UST San Lorenzo Ruiz Student Assistance Scholarship26 (ID: 108)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen5.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: College (Undergraduate)3.
- eligible_year_levels: Years 1, 2, 3, 4, and 53.
- incoming_freshman_only: No26.
- existing_college: Eligible26.
- graduate_students: Ineligible26.
- current_enrollment: Must be officially enrolled in an undergraduate degree program at the University of Santo Tomas26.
- academic: Passing academic record with a General Weighted Average (GWA) of at least 82.00% (2.50 UST scale)3.
- minimum_gwa: 82.00%3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: Combined family gross annual income must not exceed PHP 250,000.003.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to the University of Santo Tomas (España, Manila)26.
- courses: Open across all UST faculties, colleges, and institutes26.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE.
- work_experience: None
- good_moral: Required (Certificate of Good Moral Character from OSA)26.
- health: Physically and mentally fit to perform student assistant duties26.
- other_rules/conflicts: Willingness to render twenty (20) to thirty (30) hours per week of service in assigned university offices26.

### Timing
- who: Enrolled UST undergraduate students seeking work-study aid26.
- freshmen/soph/junior/senior/grad/reapply: : Yes26. | : Yes26. | : Yes26. | : Yes26. | : No. | : Yes (Semestral renewal)26.
- window: Announced by UST OSA at the start of each semester26. → Set per semestral notice26. (Semestral.; AY AY 2025–2026 / AY 2026–202726.)

### Renewal
- maintain_gwa: Maintain a minimum semestral GWA of 82.00% (2.50)3.
- regular_load: Enrolled in full term credit load26.
- no_failures: Zero failing marks7.
- return_service: Render 20 to 30 hours per week of service in assigned UST unit26.

### Disqualifiers / affiliations
- Family gross annual income exceeding PHP 250,000.003.
- Failure to render the required 20–30 hours of weekly service26.
- Academic failure or disciplinary violation7.

### Benefits (catalog)
- tuition: Full or partial tuition and fees discount3.
- stipend: Hourly compensation or semestral stipend allowance (total value up to PHP 60,000.00/year)3.
- allowance: Integrated into work-study stipend package3.

### Documents (operational hidden reqs)
- UST OSA SAAF Application Form for San Lorenzo Ruiz Scholarship26.
- Official Grade Report / Transcript showing GWA >= 82.00%3.
- Parents' Income Tax Return (ITR) or Barangay Certificate of Indigency26.
- UST Health Service Medical Clearance26.
- Endorsement Form from assigned UST office supervisor26.

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
  "minimum_gwa": 82.0,
  "income_limit": 250000,
  "school_type": [
    "Private"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "08-15",
    "close": "09-30"
  },
  "deadline_type": "exact",
  "cycle_type": "semester",
  "renewable": true,
  "first_time_only": false,
  "return_service_required": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Risk: Enrolling students who cannot commit 20–30 hours per week due to heavy
- verification: Verified3. | confidence: 96/100.

- CONTRADICTION/NOTE: entry GWA (82.00%3.) vs renewal (Maintain a minimum semestral GWA of 82.00% (2.50)3.)

---

## UST Santo Tomas Academic Scholarship26 (ID: 109)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen5.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: High School (SHS), College, and Graduate (LEAPMed, Faculty of Civil Law, Faculty of Medicine and Surgery)26.
- eligible_year_levels: All year levels corresponding to the program26.
- incoming_freshman_only: No (Covers incoming freshmen Valedictorians/Salutatorians and ongoing Dean's Listers)4.
- existing_college: Eligible (Awarded per semester based on Dean's List ranking)26.
- graduate_students: Eligible (Applicable to Civil Law and Medicine and Surgery)26.
- current_enrollment: Must be officially enrolled in UST in Senior High School, College, LEAPMed, Law, or Medicine26.
- academic: Valedictorian or Salutatorian status for incoming freshmen; Top 1 or Top 2 rank in the college/faculty for upperclassmen4.
- minimum_gwa: 88.00% (or Dean's List Top 1/Top 2 rank cutoff)3.
- alt_class_rank: Rank 1 (100% waiver) or Rank 2 (50% waiver) in the academic department/batch4.
- income_ceilings: Uncapped (Merit-based award independent of income)3.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to the University of Santo Tomas26.
- courses: Open across all UST faculties, colleges, institutes, and professional schools26.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE.
- work_experience: None
- good_moral: Required26.
- health: NOT SPECIFIED IN OFFICIAL SOURCE.
- other_rules/conflicts: Application requires certification of academic rank from the High School Principal or College Registrar4.

### Timing
- who: Incoming freshmen (Valedictorians/Salutatorians) and ongoing UST top-ranked students4.
- freshmen/soph/junior/senior/grad/reapply: : Yes26. | : Yes26. | : Yes26. | : Yes26. | : Yes (Civil Law and Medicine students)26. | : Yes (Evaluated every semester based on term rank)26.
- window: Announced by UST OSA at the start of each term26. → Set per semestral deadline26. (Semestral.; AY AY 2025–2026 / AY 2026–202726.)

### Renewal
- maintain_gwa: Must maintain Top 1 or Top 2 academic ranking in the department each semester4.
- regular_load: Enrolled in full term credit load26.
- no_failures: Zero failing grades, 3.0 marks, or incomplete grades7.
- return_service: None3.

### Disqualifiers / affiliations
- Losing Top 1 or Top 2 rank in the academic batch/department4.
- Incurring an incomplete, dropped, or failing grade7.
- Disciplinary sanction issued by UST OSA26.

### Benefits (catalog)
- tuition: 100% tuition waiver for Rank 1 / Valedictorians; 50% tuition waiver for Rank 2 / Salutatorians4.
- stipend: NOT SPECIFIED IN OFFICIAL SOURCE.
- allowance: NOT SPECIFIED IN OFFICIAL SOURCE.

### Documents (operational hidden reqs)
- UST OSA SAAF Application Form for Santo Tomas Academic Scholarship26.
- High School Principal's Certification of Valedictorian/Salutatorian status (for Freshmen)4.
- Official Transcript / Registrar Certification of Top 1 or Top 2 Rank in Department (for Upperclassmen)26.
- Certificate of Good Moral Character26.

### Recommended schema
`json
{
  "education_level": [
    "Senior High School",
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
  "minimum_gwa": 88.0,
  "rank_cutoff_alternative": 2,
  "income_limit": null,
  "school_type": [
    "Private"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "08-15",
    "close": "09-30"
  },
  "deadline_type": "exact",
  "cycle_type": "semester",
  "renewable": true,
  "first_time_only": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Risk: Recommending scholarship to general Dean's Listers who are ranked outside the
- verification: Verified3. | confidence: 95/100.

- CONTRADICTION/NOTE: entry GWA (88.00% (or Dean's List Top 1/Top 2 rank cutoff)3.) vs renewal (Must maintain Top 1 or Top 2 academic ranking in the department each semester4.)

---
