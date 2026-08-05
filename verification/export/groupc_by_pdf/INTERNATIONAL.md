# DATABASE_V3_GROUPC_INTERNATIONAL.pdf — Implementation Details

Scholarships: 11

## TaiwanICDF International Higher Education Scholarship Program3 (ID: 60)

### Hard eligibility
- citizenship: Citizen of an eligible partner country, including the Philippines4.
- residency/destination: Resident in the country of citizenship4.
- education_level: Graduate (Master's and Doctoral degree levels)3.
- eligible_year_levels: Year 1 (Incoming Graduate Students)4.
- incoming_freshman_only: No4.
- existing_college: Ineligible for initial award unless applying for entry-level graduate degree studies4.
- graduate_students: Yes3.
- current_enrollment: Must apply for admission to a designated TaiwanICDF partner university program4.
- academic: Outstanding academic record from prior post-secondary studies4.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated holistically via transcripts and university admission standards; live database parameter lists 85.00%)3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: Must be above 18 years of age4.
- school/consortium: Restricted strictly to designated TaiwanICDF partner institutions4.
- courses: Agriculture, Science and Engineering, Public Health and Medicine, Business Administration7.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Good moral character required4.
- health: Satisfactory physical and mental health4.
- other_rules/conflicts: Applicants cannot hold any other Republic of China (Taiwan) government scholarship concurrently8.

### Timing
- who: Bachelor's degree holders applying for Master's programs, and Master's degree holders applying for PhD programs at partner Taiwanese universities4.
- freshmen/soph/junior/senior/grad/reapply: : No | : No | : No | : Yes (provided they graduate prior to scholarship intake)8. | : Yes4. | : Yes4.
- window: Mid-January / February 1 annually8. → March 15 / March 31 annually4. (Annual3.; AY AY 2026–20274.)

### Renewal
- maintain_gwa: Satisfy academic GPA retention thresholds established by the host institution4.
- regular_load: Full-time credit load per semester4.
- no_failures: Zero failing grades in enrolled coursework4.
- return_service: None required by TaiwanICDF, though scholars are expected to return home to foster local development3.

### Disqualifiers / affiliations
- Holding ROC (Taiwan) citizenship or overseas Chinese student status4.
- Concurrent enjoyment of another Taiwanese government scholarship8.
- Failure to secure official admission from an approved TaiwanICDF partner university program4.

### Benefits (catalog)
- tuition: 100% full coverage of tuition and credit fees3.
- stipend: NTD 15,000 for Master's students; NTD 17,000–18,000 for PhD students4.
- allowance: Campus housing / dormitory allowance provided4.

### Documents (operational hidden reqs)
- Completed Online Application Form4.
- Passport Biopage / Certificate of Nationality4.
- Highest Degree Diploma and Official Academic Transcripts4.
- Proof of English Language Proficiency (TOEFL / IELTS / Official Institutional Certificate)4.
- Two Letters of Recommendation4.
- Copy of Application Submission to a TaiwanICDF Partner University4.

### Recommended schema
`json
{
  "education_level": [
    "Graduate"
  ],
  "eligible_year_levels": [
    1
  ],
  "incoming_year_only": true,
  "requires_current_enrollment": false,
  "minimum_gwa": null,
  "income_limit": null,
  "rank_cutoff_alternative": null,
  "priority_courses": [
    "Agriculture",
    "Science and Engineering",
    "Public Health",
    "Business Administration"
  ],
  "school_type": [
    "Foreign Partner University"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "residency_restriction": "Philippines",
  "application_window": {
    "open": "01-15",
    "close": "03-31"
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
- ● Risk: Recommending program to undergraduate applicants3.
- verification: Verified3. | confidence: None

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated holistically via transcripts and university admission standards; live database parameter lists 85.00%)3.) vs renewal (Satisfy academic GPA retention thresholds established by the host institution4.)
- CONTRADICTION: live DB GWA artifact vs official NOT SPECIFIED — NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated holistically via transcripts and university admission standards; live database parameter lists 85.00%)3.

---

## Erasmus Mundus Joint Masters Scholarship3 (ID: 63)

### Hard eligibility
- citizenship: Open to candidates worldwide, including Filipino citizens10.
- residency/destination: Worldwide residency; mandatory physical mobility across at least two different host countries11.
- education_level: Graduate (Master's degree level, 60, 90, or 120 ECTS)10.
- eligible_year_levels: Incoming Master's students10.
- incoming_freshman_only: No10.
- existing_college: Graduating Bachelor's students eligible provided their degree is conferred prior to intake10.
- graduate_students: Yes10.
- current_enrollment: Must hold a recognized first higher education degree (Bachelor's degree or equivalent)10.
- academic: Outstanding academic performance in prior undergraduate studies10.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Consortium-specific; live DB list is 90.00%)3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: NOT SPECIFIED IN OFFICIAL SOURCE (No upper age limit).
- school/consortium: Restricted to participating Erasmus Mundus Joint Master consortia HEIs9.
- courses: Comprehensive academic fields listed in the Erasmus Mundus Catalogue9.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: NOT SPECIFIED IN OFFICIAL SOURCE
- health: Health insurance covered under EU framework10.
- other_rules/conflicts: Mandatory physical mobility in at least two different countries11; maximum application limit of three (3) EMJM programs per application cycle9.

### Timing
- who: Bachelor's degree holders or final-year undergraduate students graduating prior to program start10.
- freshmen/soph/junior/senior/grad/reapply: : No | : No | : No | : Yes (if graduating before Master's intake)10. | : Yes10. | : Yes9.
- window: October / November annually9. → January / February 12 (varies per consortium)9. (Annual3.; AY AY 2026–202713.)

### Renewal
- maintain_gwa: Satisfy academic progression standards established by consortium regulations11.
- regular_load: Full credit load per semester11.
- no_failures: Pass all mandatory study modules11.
- return_service: None3.

### Disqualifiers / affiliations
- Failure to complete Bachelor's degree prior to Master's program commencement10.
- Applying to more than three Erasmus Mundus Joint Master programs in a single cycle9.
- Non-compliance with compulsory physical mobility track rules11.

### Benefits (catalog)
- tuition: 100% full coverage of participation costs, tuition, and enrollment fees10.
- stipend: €1,400 per month living allowance (up to 24 months maximum)3.
- allowance: Travel, visa, and installation contributions integrated into overall grant10.

### Documents (operational hidden reqs)
- Bachelor's Diploma or Official Certificate of Expected Graduation10.
- Official Academic Transcripts of Records (TOR)10.
- Proof of English Language Proficiency (IELTS / TOEFL)9.
- Motivation Letter / Statement of Purpose9.
- Two Academic / Professional Recommendation Letters9.
- Passport / Proof of Nationality9.
- Curriculum Vitae (Europass format)9.

### Recommended schema
`json
{
  "education_level": [
    "Graduate"
  ],
  "eligible_year_levels": [
    1
  ],
  "incoming_year_only": true,
  "requires_current_enrollment": false,
  "minimum_gwa": null,
  "income_limit": null,
  "rank_cutoff_alternative": null,
  "priority_courses": [
    "Erasmus Mundus Catalogue Disciplines"
  ],
  "school_type": [
    "EUConsortium HEIs"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "residency_restriction": null,
  "application_window": {
    "open": "10-01",
    "close": "02-12"
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
- ● Risk: Recommending scholarship to students expecting to study at a single university11.
- verification: Verified3. | confidence: 95/1003.

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Consortium-specific; live DB list is 90.00%)3.) vs renewal (Satisfy academic progression standards established by consortium regulations11.)
- CONTRADICTION: live DB GWA artifact vs official NOT SPECIFIED — NOT SPECIFIED IN OFFICIAL SOURCE (Consortium-specific; live DB list is 90.00%)3.

---

## Global Korea Scholarship for Graduate Degrees (GKS-G)14 (ID: 64)

### Hard eligibility
- citizenship: Applicant and both parents must hold citizenship of an NIIED-designated country; dual citizens holding Korean nationality are strictly barred16.
- residency/destination: Resident in home country16.
- education_level: Graduate (Master's or Doctoral degree programs)3.
- eligible_year_levels: Incoming Graduate Students16.
- incoming_freshman_only: No16.
- existing_college: Graduating Bachelor's/Master's students eligible16.
- graduate_students: Yes16.
- current_enrollment: Must have graduated or be expected to graduate from a Bachelor's degree (for Master's) or Master's degree (for PhD)16.
- academic: Cumulative GPA must be on a 100-point scale or ranked in the top 20% of the class; CGPA , , , or 16.
- minimum_gwa: Equivalent to 80% percentile cutoff16.
- alt_class_rank: Top 20% of graduating class19.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: Under 40 years of age (born after September 1, 1986); under 45 years for academic professors from ODA recipient countries18.
- school/consortium: Restricted to participating NIIED-approved Korean Universities14.
- courses: Fields offered by designated Korean universities14.
- sectoral/hidden: Special tracks available (e.g., Global Network, R&D)19.
- work_experience: None
- good_moral: Good moral character16.
- health: Physically and mentally healthy (Personal Medical Assessment required)16.
- other_rules/conflicts: Former GKS scholars or graduates of Korean high schools/universities are ineligible with specific exceptions19.

### Timing
- who: Bachelor's degree holders applying for Master's programs and Master's degree holders applying for Doctoral programs16.
- freshmen/soph/junior/senior/grad/reapply: : No | : No | : No | : Yes (if graduating prior to intake)18. | : Yes16. | : Subject to NIIED reapplication rules19.
- window: Mid-February annually14. → March / April annually (set by individual embassies/universities)14. (Annual3.; AY AY 2026–202714.)

### Renewal
- maintain_gwa: Maintain CGPA or equivalent per term18.
- regular_load: Continuous full-time enrollment16.
- no_failures: Achieve passing marks in all enrolled modules16.
- return_service: Expected to return or adhere to NIIED visa regulations3.

### Disqualifiers / affiliations
- Holding Korean citizenship or dual citizenship with South Korea16.
- CGPA falling below 80% percentile threshold18.
- Previous receipt of a degree scholarship from the Korean government19.

### Benefits (catalog)
- tuition: 100% full coverage of tuition fees funded by NIIED and host university3.
- stipend: KRW 1,000,000 per month (Master's/PhD); KRW 1,500,000 for Research scholars.
- allowance: Settlement allowance (KRW 200,000 single grant).

### Documents (operational hidden reqs)
- GKS-G Official Application Form16.
- Personal Statement and Study Plan16.
- One Recommendation Letter16.
- GKS Applicant Agreement & Personal Medical Assessment16.
- Bachelor's / Master's Diploma and Transcripts (Apostilled / Consular Authenticated)16.
- Proof of Citizenship for Applicant and Both Parents16.
- Language Proficiency Certificates (TOPIK / TOEFL / IELTS)16.

### Recommended schema
`json
{
  "education_level": [
    "Graduate"
  ],
  "eligible_year_levels": [
    1
  ],
  "incoming_year_only": true,
  "requires_current_enrollment": false,
  "minimum_gwa": 80.0,
  "income_limit": null,
  "rank_cutoff_alternative": 20,
  "priority_courses": [
    "All Graduate Fields at Participating Universities"
  ],
  "school_type": [
    "Korean HEIs"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "residency_restriction": "Philippines",
  "application_window": {
    "open": "02-15",
    "close": "03-31"
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
- ● Risk: Inaccurate GPA conversion disqualifying eligible applicants19.
- verification: Verified3. | confidence: 98/1003.

- CONTRADICTION/NOTE: entry GWA (Equivalent to 80% percentile cutoff16.) vs renewal (Maintain CGPA or equivalent per term18.)

---

## Global Korea Scholarship for Undergraduate Degrees (GKS-U)20 (ID: 65)

### Hard eligibility
- citizenship: Non-Korean citizenship for applicant and both parents; dual citizens holding Korean nationality are barred18.
- residency/destination: Resident in home country18.
- education_level: Undergraduate / College (Bachelor's or Associate degree)18.
- eligible_year_levels: Year 1 (Incoming College Freshmen)18.
- incoming_freshman_only: Yes18.
- existing_college: Ineligible (except Associate degree graduates applying for Bachelor's entry)18.
- graduate_students: Ineligible20.
- current_enrollment: High school graduate or expected to graduate Grade 12 prior to intake18.
- academic: Cumulative GPA of 80% or higher on a 100-point scale or ranked in the top 20% of high school graduating class18.
- minimum_gwa: 80% percentile cutoff18.
- alt_class_rank: Top 20% of class18.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: Under 25 years of age (born after March 1, 2001)18.
- school/consortium: Restricted to designated NIIED-approved Korean Universities (Type A and Type B)18.
- courses: Four-year Bachelor's degree or Associate degree courses offered by designated universities18.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Good moral character20.
- health: Mentally and physically fit (Personal Medical Assessment required)20.
- other_rules/conflicts: High school graduates from Korea or former Korean government degree scholarship recipients are barred19.

### Timing
- who: Senior High School Grade 12 graduating students, SHS graduates, and Associate degree graduates18.
- freshmen/soph/junior/senior/grad/reapply: : Only if applying as an incoming freshman with zero | : No | : No | : No | : High School / Associate degree graduates only18. | : Subject to NIIED reapplication rules20.
- window: September annually17. → October / November annually (set by Embassy / University 1st round)17. (Annual3.; AY AY 2026–202720.)

### Renewal
- maintain_gwa: Maintain CGPA per semester18.
- regular_load: Full credit enrollment20.
- no_failures: Zero failing marks20.
- return_service: None3.

### Disqualifiers / affiliations
- Age exceeding 25 years at application deadline18.
- Holding Korean citizenship or dual nationality18.
- Earning tertiary units in a 4-year degree program prior to application20.

### Benefits (catalog)
- tuition: 100% full tuition coverage3.
- stipend: KRW 900,000 per month.
- allowance: Settlement allowance (KRW 200,000 single grant).

### Documents (operational hidden reqs)
- GKS-U Application Form20.
- Personal Statement and Study Plan20.
- One Recommendation Letter20.
- High School Graduation Certificate / Associate Degree Diploma (Apostilled)18.
- Official High School / Associate Academic Transcripts18.
- Proof of Citizenship for Applicant and Both Parents18.
- Personal Medical Assessment20.

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
  "minimum_gwa": 80.0,
  "income_limit": null,
  "rank_cutoff_alternative": 20,
  "age_limit": 25,
  "priority_courses": [
    "Four-year Undergraduate Degrees"
  ],
  "school_type": [
    "Korean HEIs"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "residency_restriction": "Philippines",
  "application_window": {
    "open": "09-01",
    "close": "10-31"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "return_service_required": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Risk: Showing scholarship to applicants over 25 years of age18.
- verification: Verified3. | confidence: 98/1003.

- CONTRADICTION/NOTE: entry GWA (80% percentile cutoff18.) vs renewal (Maintain CGPA per semester18.)

---

## Australia Awards Scholarships (Philippines)3 (ID: 74)

### Hard eligibility
- citizenship: Filipino Citizen24.
- residency/destination: Resided in the Philippines for at least 12 months prior to application deadline24.
- education_level: Graduate (Master's Degree level)3.
- eligible_year_levels: Incoming Master's Students24.
- incoming_freshman_only: No24.
- existing_college: Ineligible24.
- graduate_students: Yes24.
- current_enrollment: Must have completed a formal undergraduate degree24.
- academic: Academic competence evaluated holistically from undergraduate transcripts24.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated holistically; live DB parameter lists NULL)3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: NOT SPECIFIED IN OFFICIAL SOURCE (Must meet adult visa eligibility).
- school/consortium: Eligible Australian Universities24.
- courses: Agriculture, Marine, and Natural Resource Management; Climate Change; Cybersecurity & Critical Technology; Education; International Relations & National Security24.
- sectoral/hidden: Open Category (all qualified individuals) and Targeted Category (nominated by 11 Philippine Government agencies)24.
- work_experience: Minimum two (2) years cumulative work experience upon application24.
- good_moral: Good moral character24.
- health: Must satisfy Australian student visa health requirements24.
- other_rules/conflicts: Must commit to returning to the Philippines to implement a Re-entry Action Plan (REAP)24; cannot hold another active scholarship24.

### Timing
- who: Filipino professionals holding a Bachelor's degree with at least 2 years work experience24.
- freshmen/soph/junior/senior/grad/reapply: : No | : No | : No | : No | : Yes (Bachelor's graduates)24. | : Yes (provided they have not held a long-term Australia
- window: February 1 annually24. → April 30 annually24. (Annual3.; AY AY 2026–2027 / Commencement 202724.)

### Renewal
- maintain_gwa: Maintain satisfactory academic progress per university rules24.
- regular_load: Continuous full-time course enrollment28.
- no_failures: Zero failed academic units24.
- return_service: Mandatory Return Service in the Philippines to execute Re-entry Action Plan (REAP)3.

### Disqualifiers / affiliations
- Holding dual Australian citizenship or permanent residency24.
- Having less than two years cumulative work experience24.
- Failure to submit an approved Re-entry Action Plan24.

### Benefits (catalog)
- tuition: 100% full tuition fee coverage3.
- stipend: Contribution to Living Expenses (CLE) paid fortnightly/monthly24.
- allowance: One-off establishment allowance on arrival24.

### Documents (operational hidden reqs)
- Re-entry Action Plan (REAP) Proposal24.
- Proof of Citizenship (Passport or Birth Certificate)24.
- Proof of Residency (Government ID, lease contract, or utility bill)24.
- Official Academic Transcripts and Diplomas24.
- Curriculum Vitae documenting years work experience24.
- Referee Reports (Academic and Work Supervisor)24.
- English Language Test Results (IELTS / TOEFL / PTE)25.

### Recommended schema
`json
{
  "education_level": [
    "Graduate"
  ],
  "eligible_year_levels": [
    1
  ],
  "incoming_year_only": true,
  "requires_current_enrollment": false,
  "minimum_gwa": null,
  "income_limit": null,
  "work_experience_years": 2,
  "priority_courses": [
    "Agriculture",
    "Climate Change",
    "Cybersecurity",
    "Education",
    "National Security"
  ],
  "school_type": [
    "Australian HEIs"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "residency_restriction": "Philippines (>= 12 months)",
  "application_window": {
    "open": "02-01",
    "close": "04-30"
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
- ● Risk: Recommending program to fresh graduates without required work experience24.
- verification: Verified3. | confidence: 98/1003.

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated holistically; live DB parameter lists NULL)3.) vs renewal (Maintain satisfactory academic progress per university rules24.)
- CONTRADICTION: live DB GWA artifact vs official NOT SPECIFIED — NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated holistically; live DB parameter lists NULL)3.

---

## Japanese Government (MEXT) Scholarship – Research Student Category29 (ID: 80)

### Hard eligibility
- citizenship: Filipino Citizen (processed by Embassy of Japan in Manila)29.
- residency/destination: Resident in the Philippines29.
- education_level: Graduate (Master's / PhD / Non-degree Research Student)3.
- eligible_year_levels: Incoming Research/Graduate Students29.
- incoming_freshman_only: No29.
- existing_college: Graduating university seniors eligible29.
- graduate_students: Yes29.
- current_enrollment: Must have completed 16 years of school education or hold a Bachelor's degree29.
- academic: High academic performance in university studies29.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via academic transcript and written exam)3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: Born on or after April 2, 1992 (Under 35 years old)29.
- school/consortium: Japanese national, public, or private universities29.
- courses: Fields matching university major or related academic fields29.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Good moral standing.
- health: Physically and mentally fit (Medical Certificate required)29.
- other_rules/conflicts: Willingness to learn Japanese; military personnel barred29.

### Timing
- who: Bachelor's degree holders or graduating college seniors29.
- freshmen/soph/junior/senior/grad/reapply: : No | : No | : No | : Yes (if graduating before departure to Japan)29. | : Yes29. | : Yes29.
- window: Mid-April / May annually29. → Late May / June annually29. (Annual3.; AY AY 2026–2027 / Departure April/October 202729.)

### Renewal
- maintain_gwa: Satisfy graduate school retention and academic standards29.
- regular_load: Full credit load29.
- no_failures: Zero failed research modules29.
- return_service: Expected to return; mandatory return service for Philippine public servants3.

### Disqualifiers / affiliations
- Born before April 2, 199229.
- Holding Japanese nationality29.
- Failure to pass MEXT written examination and embassy interview29.

### Benefits (catalog)
- tuition: 100% full coverage of tuition, entrance, and examination fees3.
- stipend: JPY 143,000–145,000 per month (varies for Research/Master's/PhD).
- allowance: Regional stipend allowance top-up.

### Documents (operational hidden reqs)
- Application Form & Placement Preference Form29.
- Field of Study and Research Plan29.
- Official Transcript of Records (TOR)29.
- Graduation Certificate / Degree Diploma29.
- Recommendation Letter from Dean/President or Advisor29.
- Certificate of Health29.
- Thesis Abstract / Research Papers (if applicable)29.

### Recommended schema
`json
{
  "education_level": [
    "Graduate"
  ],
  "eligible_year_levels": [
    1
  ],
  "incoming_year_only": true,
  "requires_current_enrollment": false,
  "minimum_gwa": null,
  "income_limit": null,
  "age_limit": 34,
  "priority_courses": [
    "All Fields Offered at Japanese Universities"
  ],
  "school_type": [
    "Japanese Universities"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "residency_restriction": "Philippines",
  "application_window": {
    "open": "04-15",
    "close": "05-31"
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
- ● Risk: Recommending program to applicants exceeding age limit29.
- verification: Verified3. | confidence: 98/1003.

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via academic transcript and written exam)3.) vs renewal (Satisfy graduate school retention and academic standards29.)

---

## Japanese Government (MEXT) Scholarship – Undergraduate Student Category29 (ID: 81)

### Hard eligibility
- citizenship: Filipino Citizen29.
- residency/destination: Resident in the Philippines29.
- education_level: Undergraduate / College (Bachelor's Degree)3.
- eligible_year_levels: Year 1 (Incoming Freshmen)29.
- incoming_freshman_only: Yes29.
- existing_college: Eligible if within age limit, but award starts at 1st year29.
- graduate_students: Ineligible29.
- current_enrollment: Completed 12 years of school education or graduating Grade 12 by March preceding intake29.
- academic: High school academic excellence29.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via written examinations in Mathematics, English, Japanese, and Science)3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: Born on or after April 2, 2002 (17 to 24 years old)29.
- school/consortium: Designated Japanese Universities29.
- courses: Social Sciences & Humanities (Law, Politics, Economics, Literature) and Natural Sciences (Science, Engineering, Agriculture, Medicine)29.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Good moral character.
- health: Mentally and physically fit29.
- other_rules/conflicts: Mandatory 1-year preparatory Japanese language education in Japan29.

### Timing
- who: Senior High School Grade 12 graduating students or SHS graduates29.
- freshmen/soph/junior/senior/grad/reapply: : Yes (if within age limit, but must restart as 1st year)29. | : Only if age-eligible. | : No | : No | : Only SHS / High School graduates29. | : Yes29.
- window: Mid-April / May annually29. → Late May / June annually29. (Annual3.; AY AY 2026–2027 / Departure April 202729.)

### Renewal
- maintain_gwa: Pass university academic performance standards per term29.
- regular_load: Full credit load per term29.
- no_failures: Zero failing marks29.
- return_service: Expected return service3.

### Disqualifiers / affiliations
- Born before April 2, 200229.
- Holding Japanese nationality29.
- Failure to pass MEXT written examinations in STEM/Humanities subjects29.

### Benefits (catalog)
- tuition: 100% full coverage of tuition and entrance examination fees3.
- stipend: JPY 117,000 per month.
- allowance: Preparatory training allowance.

### Documents (operational hidden reqs)
- Application Form & Placement Preference Form29.
- SHS Form 138 / SF9 / High School Transcripts29.
- High School Diploma / Graduation Certificate29.
- Recommendation Letter from High School Principal/Teacher29.
- Certificate of Health29.

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
  "income_limit": null,
  "age_limit": 24,
  "priority_courses": [
    "Social Sciences",
    "Humanities",
    "Natural Sciences",
    "Medicine"
  ],
  "school_type": [
    "Japanese Universities"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "residency_restriction": "Philippines",
  "application_window": {
    "open": "04-15",
    "close": "05-31"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "return_service_required": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Risk: Recommending scholarship to upperclassmen who do not wish to restart as 1st
- verification: Verified3. | confidence: 98/1003.

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via written examinations in Mathematics, English, Japanese, and Science)3.) vs renewal (Pass university academic performance standards per term29.)

---

## Japanese Government (MEXT) Scholarship – Specialized Training College Student Category29 (ID: 82)

### Hard eligibility
- citizenship: Filipino Citizen29.
- residency/destination: Resident in the Philippines29.
- education_level: Technical-Vocational / TVET3.
- eligible_year_levels: Entry-level vocational diploma track29.
- incoming_freshman_only: Yes29.
- existing_college: Eligible if within age limit29.
- graduate_students: Ineligible29.
- current_enrollment: High school graduate or expected to graduate Grade 12 by March preceding arrival29.
- academic: Strong high school academic record29.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via written examinations in English, Mathematics, and Japanese)3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: Born on or after April 2, 2002 (17 to 24 years old)29.
- school/consortium: Japanese Specialized Training Colleges (Senshu-Gakko)29.
- courses: Technology, Personal Care/Nutrition, Education/Welfare, Business, Fashion/Home Economics, Culture/General Education29.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE
- work_experience: None
- good_moral: Good moral character.
- health: Mentally and physically fit29.
- other_rules/conflicts: 1-year Japanese language preparatory course included prior to 2-year vocational studies29.

### Timing
- who: Senior High School Grade 12 graduating students or SHS graduates29.
- freshmen/soph/junior/senior/grad/reapply: : Yes (if age-eligible)29. | : Only if age-eligible. | : No | : No | : High School / SHS graduates only29. | : Yes29.
- window: Mid-April / May annually29. → Late May / June annually29. (Annual3.; AY AY 2026–2027 / Departure April 202729.)

### Renewal
- maintain_gwa: Satisfy specialized college retention standards29.
- regular_load: Full credit load per term29.
- no_failures: Zero failing marks29.
- return_service: Expected return service3.

### Disqualifiers / affiliations
- Born before April 2, 200229.
- Holding Japanese nationality29.
- Failure to pass written examinations in English, Mathematics, and Japanese29.

### Benefits (catalog)
- tuition: 100% full coverage of tuition and vocational education fees3.
- stipend: JPY 117,000 per month.
- allowance: Preparatory training allowance.

### Documents (operational hidden reqs)
- Application Form29.
- SHS Form 138 / High School Academic Transcripts29.
- High School Diploma / Graduation Certificate29.
- Recommendation Letter29.
- Medical Certificate29.

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
  "requires_current_enrollment": false,
  "minimum_gwa": null,
  "income_limit": null,
  "age_limit": 24,
  "priority_courses": [
    "Technology",
    "Nutrition",
    "Business",
    "Fashion",
    "Culture"
  ],
  "school_type": [
    "Japanese Specialized Training Colleges"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "residency_restriction": "Philippines",
  "application_window": {
    "open": "04-15",
    "close": "05-31"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "return_service_required": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Risk: Misclassifying vocational track as a 4-year Bachelor's degree29.
- verification: Verified3. | confidence: 98/1003.

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via written examinations in English, Mathematics, and Japanese)3.) vs renewal (Satisfy specialized college retention standards29.)

---

## Japanese Government (MEXT) Scholarship – College of Technology Student Category (KOSEN)29 (ID: 83)

### Hard eligibility
- citizenship: Filipino Citizen29.
- residency/destination: Resident in the Philippines29.
- education_level: College / TVET (KOSEN Associate Degree / Practical Engineering)3.
- eligible_year_levels: Entry into 3rd year of KOSEN system following 1 year of preparatory training29.
- incoming_freshman_only: Yes29.
- existing_college: Eligible if within age threshold29.
- graduate_students: Ineligible29.
- current_enrollment: High school graduate or expected to graduate Grade 12 by March preceding arrival29.
- academic: High academic performance in STEM / Mathematics and Physics29.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via written examinations in Mathematics, Physics, Chemistry, English, and Japanese)3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: Born on or after April 2, 2002 (17 to 24 years old)29.
- school/consortium: National Colleges of Technology (KOSEN) in Japan29.
- courses: Mechanical Engineering, Electrical & Electronic Engineering, Information Technology, Chemical Engineering, Civil Engineering, Architecture, Materials Engineering29.
- sectoral/hidden: STEM focus29.
- work_experience: None
- good_moral: Good moral character.
- health: Mentally and physically fit29.
- other_rules/conflicts: Includes 1-year preparatory Japanese language and STEM education29.

### Timing
- who: Senior High School STEM graduating students or SHS graduates29.
- freshmen/soph/junior/senior/grad/reapply: : Yes (if age-eligible)29. | : Only if age-eligible. | : No | : No | : High School / SHS graduates only29. | : Yes29.
- window: Mid-April / May annually29. → Late May / June annually29. (Annual3.; AY AY 2026–2027 / Departure April 202729.)

### Renewal
- maintain_gwa: Satisfy KOSEN engineering academic standards29.
- regular_load: Full credit load per term29.
- no_failures: Zero failing marks29.
- return_service: Expected return service3.

### Disqualifiers / affiliations
- Born before April 2, 200229.
- Holding Japanese nationality29.
- Failure to pass written examinations in Mathematics, Physics, Chemistry, English, and Japanese29.

### Benefits (catalog)
- tuition: 100% full coverage of tuition, entrance, and laboratory fees3.
- stipend: JPY 117,000 per month.
- allowance: Preparatory training allowance.

### Documents (operational hidden reqs)
- Application Form29.
- SHS Form 138 / High School Transcripts29.
- High School Diploma / Graduation Certificate29.
- Recommendation Letter from Principal/STEM Teacher29.
- Certificate of Health29.

### Recommended schema
`json
{
  "education_level": [
    "College",
    "TVET"
  ],
  "eligible_year_levels": [
    1
  ],
  "incoming_year_only": true,
  "requires_current_enrollment": false,
  "minimum_gwa": null,
  "income_limit": null,
  "age_limit": 24,
  "priority_courses": [
    "Mechanical",
    "Electrical",
    "Information Technology",
    "Chemical",
    "Civil",
    "Architecture"
  ],
  "school_type": [
    "Japanese KOSENColleges"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "residency_restriction": "Philippines",
  "application_window": {
    "open": "04-15",
    "close": "05-31"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": true,
  "first_time_only": true,
  "return_service_required": false,
  "needs_manual_review": false
}
`

### FP/FN risks & contradictions
- ● Risk: Non-STEM students applying without necessary Physics/Chemistry background29.
- verification: Verified3. | confidence: 98/1003.

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via written examinations in Mathematics, Physics, Chemistry, English, and Japanese)3.) vs renewal (Satisfy KOSEN engineering academic standards29.)

---

## Fulbright-Philippine Space Agency (PhilSA) Foreign Student Program in Space Science and Technology Applications (SSTA)30 (ID: 90)

### Hard eligibility
- citizenship: Filipino Citizen residing in the Philippines at application and selection time; dual citizens or US permanent residents are barred30.
- residency/destination: Resident in the Philippines30.
- education_level: Graduate (Master's or Doctoral studies)3.
- eligible_year_levels: Year 1 (Incoming Graduate Students)30.
- incoming_freshman_only: No30.
- existing_college: Ineligible30.
- graduate_students: Yes30.
- current_enrollment: Completed Bachelor's degree with major in field of specialization and an excellent academic record31.
- academic: Excellent undergraduate academic record31.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via transcript and research objective statement)3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: NOT SPECIFIED IN OFFICIAL SOURCE
- school/consortium: Accredited Higher Education Institutions in the United States30.
- courses: Space Applications (Earth observation, meteorology, PNT, telecom), Spacecraft Systems (satellites, rocketry, robotics, cybersecurity), Space Science (astronomy, space biology/medicine), Space Law, Economics, and Administration30.
- sectoral/hidden: Space Science and Technology Applications (SSTA) and allied sectors31.
- work_experience: Minimum two (2) years of professional work experience after college graduation30.
- good_moral: No pending administrative or criminal charges; no conviction30.
- health: Physically and mentally fit to pursue graduate studies in the US30.
- other_rules/conflicts: Must commit to returning to the Philippines immediately upon program completion to fulfill return service30; no dependent support provided31.

### Timing
- who: Bachelor's degree holders with at least 2 years post-college professional work experience in space-related disciplines30.
- freshmen/soph/junior/senior/grad/reapply: : No | : No | : No | : No | : Yes (Bachelor's or Master's degree graduates)30. | : Yes (if not received a Fulbright grant within the past 5
- window: January 20 annually31. → April 18 / April 30 / June 19 (depending on AY cycle announcement)30. (Annual3.; AY AY 2026–2027 / AY 2027–202830.)

### Renewal
- maintain_gwa: Satisfy academic GPA retention policies of host US university30.
- regular_load: Full credit load30.
- no_failures: Zero failed academic units30.
- return_service: Mandatory Return Service obligation in the Philippines immediately upon program completion3.

### Disqualifiers / affiliations
- Holding dual US citizenship or permanent resident status30.
- Having less than two years post-college professional work experience30.
- Presently living, studying, or working in the United States30.

### Benefits (catalog)
- tuition: 100% full coverage of tuition and university fees3.
- stipend: Monthly maintenance allowance30.
- allowance: Settling-in allowance, in-transit allowance, allowable excess baggage grant31.

### Documents (operational hidden reqs)
- Completed Online Application via IIE Portal30.
- Research Objective Statement (3 to 5 pages)30.
- Personal Statement (maximum 3 pages)30.
- Updated Curriculum Vitae / Resume (maximum 6 pages)30.
- Official Transcripts of Records and Diplomas30.
- Three Letters of Recommendation30.
- Passport Biopage Copy30.
- NBI Clearance (secured within 6 months)30.
- Writing Samples (maximum 20 pages) & Bibliography30.

### Recommended schema
`json
{
  "education_level": [
    "Graduate"
  ],
  "eligible_year_levels": [
    1
  ],
  "incoming_year_only": true,
  "requires_current_enrollment": false,
  "minimum_gwa": null,
  "income_limit": null,
  "work_experience_years": 2,
  "priority_courses": [
    "Space Applications",
    "Spacecraft Systems",
    "Space Science",
    "Space Law"
  ],
  "school_type": [
    "USHigher Education Institutions"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "residency_restriction": "Philippines",
  "application_window": {
    "open": "01-20",
    "close": "06-19"
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
- ● Risk: Recommending grant to applicants counting college assistantships as work
- verification: Verified3. | confidence: 98/1003.

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via transcript and research objective statement)3.) vs renewal (Satisfy academic GPA retention policies of host US university30.)

---

## Chevening Scholarship3 (ID: 91)

### Hard eligibility
- citizenship: Filipino Citizen (or citizen of a Chevening-eligible territory)34.
- residency/destination: Resident in the Philippines or an eligible Chevening territory34.
- education_level: Graduate (One-year taught Master's degree)3.
- eligible_year_levels: Incoming Master's Students36.
- incoming_freshman_only: No37.
- existing_college: Ineligible37.
- graduate_students: Yes36.
- current_enrollment: Must have completed an undergraduate degree enabling entry into a UK postgraduate program10.
- academic: Meets UK university Master's entry requirements37.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Must obtain an unconditional offer from a UK university; live database parameter lists NULL)3.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE
- age: NOT SPECIFIED IN OFFICIAL SOURCE (No upper age limit).
- school/consortium: Any recognized UK Higher Education Institution36.
- courses: Any eligible one-year taught Master's degree program in the UK (MBA fee contribution capped at £22,000)36.
- sectoral/hidden: High leadership potential / emerging leaders37.
- work_experience: Minimum two (2) years of work experience (equivalent to 2,800 hours)24.
- good_moral: Good moral character; compliance with Chevening Code of Conduct37.
- health: Must receive medical clearance and UK visa entry clearance37.
- other_rules/conflicts: Must return to home country for at least two (2) years after scholarship completion36; no financial or visa support provided for dependants37.

### Timing
- who: Bachelor's degree holders with at least 2 years work experience37.
- freshmen/soph/junior/senior/grad/reapply: : No | : No | : No | : No | : Yes (Bachelor's degree graduates)37. | : Yes (if not previously funded by a UK government
- window: August / September annually3. → November / October 7 annually (e.g., October 7, 2026 in DB)3. (Annual3.; AY AY 2026–20273.)

### Renewal
- maintain_gwa: Satisfy academic progression rules of host UK university37.
- regular_load: Continuous full-time enrollment37.
- no_failures: Complete all Master's course modules37.
- return_service: Mandatory 2-year return to home country following completion of award3.

### Disqualifiers / affiliations
- Holding British or dual British citizenship37.
- Having less than two years (2,800 hours) work experience24.
- Previous receipt of a UK government-funded scholarship36.

### Benefits (catalog)
- tuition: 100% full tuition fee coverage (MBA fee contribution capped at £22,000)3.
- stipend: Personal living allowance (stipend rate varies for London vs Non-London institutions)36.
- allowance: Arrival allowance, departure allowance, travel top-up allowance for London events36.

### Documents (operational hidden reqs)
- Completed Online Application Form via Chevening portal34.
- Official Undergraduate Transcripts and Degree Certificate37.
- Selection of Three Eligible Taught UK Master's Courses36.
- Two Reference Letters37.
- Valid Passport / Proof of Citizenship37.
- Evidence of 2 Years Work Experience (2,800 hours)24.
- Unconditional Offer Letter from at least one UK course choice (by July deadline)36.

### Recommended schema
`json
{
  "education_level": [
    "Graduate"
  ],
  "eligible_year_levels": [
    1
  ],
  "incoming_year_only": true,
  "requires_current_enrollment": false,
  "minimum_gwa": null,
  "income_limit": null,
  "work_experience_years": 2,
  "priority_courses": [
    "One-year Taught Master's Degrees"
  ],
  "school_type": [
    "UKHigher Education Institutions"
  ],
  "partner_school_restricted": false,
  "citizenship": "Filipino",
  "residency_restriction": "Philippines",
  "application_window": {
    "open": "08-01",
    "close": "11-07"
  },
  "deadline_type": "exact",
  "cycle_type": "annual",
  "renewable": false,
  "first_time_only": true,
  "return_service_required": true,
  "needs_manual_review": true
}
`

### FP/FN risks & contradictions
- ● Risk: Recommending grant for 2-year research Master's programs36.
- verification: Verified3. | confidence: 98/1003.

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Must obtain an unconditional offer from a UK university; live database parameter lists NULL)3.) vs renewal (Satisfy academic progression rules of host UK university37.)
- CONTRADICTION: live DB GWA artifact vs official NOT SPECIFIED — NOT SPECIFIED IN OFFICIAL SOURCE (Must obtain an unconditional offer from a UK university; live database parameter lists NULL)3.

---
