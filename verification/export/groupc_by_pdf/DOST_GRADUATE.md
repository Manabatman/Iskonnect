# DATABASE_V3_GROUPC_DOST_GRADUATE.pdf — Implementation Details

Scholarships: 5

## DOST-SEI Graduate Scholarship Programs (Umbrella Entry covering ASTHRDP, CBPSME, ERDT, and STRAND) (ID: 3)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: Graduate (Master's Degree and Doctoral/PhD Degree).
- eligible_year_levels: MS Program: Years 1 and 2; PhD Program: Years 1, 2, and 3 (up to Year 4 for straight-PhD track).
- incoming_freshman_only: No (Lateral entry ongoing graduate students with earned units are eligible).
- existing_college: Ineligible for undergraduate degree enrollment; applicants must possess a completed Bachelor's degree (for MS) or Master's degree (for PhD).
- graduate_students: Yes (Incoming 1st year graduate students and regular ongoing MS/PhD students).
- current_enrollment: Must be admitted or enrolled as a regular graduate student in an approved priority S&T program at a DOST-SEI consortium member university.
- academic: Must meet the admission requirements for graduate studies at the accepting consortium university.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Governed by host university graduate school admission and retention standards; live database entry of 88% is an unverified artifact).
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE (Uncapped / No parental or personal income limit is imposed in official DOST graduate guidelines; live database cap of ₱500,000 is incorrect).
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted to designated DOST-SEI Graduate Scholarship Consortium Member Universities (e.g., NSC, ERDT, CBPSME, and STRAND consortia).
- courses: DOST-SEI Priority S&T Fields (Natural Sciences, Engineering, Science & Mathematics Education, Agriculture, Computer Science, etc.).
- sectoral/hidden: Educator status for CBPSME; Regional HEI faculty status for STRAND.
- work_experience: None
- good_moral: Required (Validated via NBI Clearance or Certificate of Good Moral Character).
- health: Physically and mentally fit to study, as certified by a licensed physician.
- other_rules/conflicts: Must be a full-time student; must NOT be employed or practicing a profession while on scholarship, or must secure an official approved leave of absence (LOA) from the employer; must not enjoy concurrent government or private scholarships; must execute a service contract.

### Timing
- who: Graduating college seniors entering graduate school, BS/BA degree holders applying for MS, MS degree holders applying for PhD, and regular ongoing MS/PhD students.
- freshmen/soph/junior/senior/grad/reapply: : Ineligible for undergraduate freshmen; incoming 1st-year | : Ineligible for undergraduate sophomores; ongoing | : Ineligible for undergraduate juniors. | : Graduating college seniors entering an MS program upon | : Yes (Bachelor's graduates for MS; Master's graduates for PhD). | : Yes.
- window: Announced per academic cycle by consortium universities (typically March/April for 1st Semester; September/October for 2nd Semester). → Varies by university (e.g., June 30 for 1st Semester intake). (Semester / Term intake.; AY AY 2025–2026 / AY 2026–2027.)

### Renewal
- maintain_gwa: Must maintain a satisfactory General Weighted Average (GWA/GPA) prescribed by the host graduate school each term.
- regular_load: Must carry a full academic load per semester based on the approved Program of Study (9–12 units regular term, 3–6 units midyear).
- no_failures: Must have no failing, incomplete, or dropped grades in coursework.
- return_service: Mandatory return service obligation in the Philippines on a full-time basis immediately after degree completion, equivalent to one (1) year of service for every year of scholarship availed.

### Disqualifiers / affiliations
- Employment or professional practice while on scholarship without an approved official leave of absence.
- Failure to maintain academic retention standards or receiving a failing grade in any graduate subject.
- Concurrent enjoyment of another government or private scholarship covering the same degree program.
- Failure to comply with the return service obligation or non-completion of the degree program without valid justification (requires full financial refund with interest).

### Benefits (catalog)
- tuition: Full actual tuition and other school fees.
- stipend: ₱30,000.00 per month for MS scholars; ₱38,000.00 per month for PhD scholars.
- allowance: Learning Materials and/or Connectivity Allowance of ₱20,000.00 per Academic Year.

### Documents (operational hidden reqs)
- Duly accomplished DOST-SEI Graduate Scholarship Information Sheet / Application Form.
- PSA Birth Certificate (Photocopy).
- Certified True Copy of Official Transcript of Records (TOR) for BS (and MS if applying for PhD).
- Official Endorsement Forms from two (2) former college professors (for MS) or two (2) former MS professors (for PhD).
- Medical Certificate from a licensed physician stating the applicant is physically and mentally fit to study.
- Valid NBI Clearance.
- Official Letter of Admission with regular status from the Program Head of the accepting institution.
- Approved Program of Study (POS).
- If employed: Official recommendation and approved Leave of Absence (LOA) from the head of agency, or proof of resignation.

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
  "rank_cutoff_alternative": null,
  "priority_courses": [
    "DOST-SEIPRIORITYS&TGRADUATEFIELDS"
  ],
  "school_type": [
    "SUC",
    "LUC",
    "PRIVATE_CONSORTIUM_HEI"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "semester_variable",
    "close": "semester_variable"
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
- ● Corrupted Financial Parameters: Live database ID 3 sets max_income: 500000 and
- verification: Verified | confidence: None

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Governed by host university graduate school admission and retention standards; live database entry of 88% is an unverified artifact).) vs renewal (Must maintain a satisfactory General Weighted Average (GWA/GPA) prescribed by the host graduate school each term.)
- CONTRADICTION: live DB GWA artifact vs official NOT SPECIFIED — NOT SPECIFIED IN OFFICIAL SOURCE (Governed by host university graduate school admission and retention standards; live database entry of 88% is an unverified artifact).

---

## Accelerated Science and Technology Human Resource Development Program (ASTHRDP) (ID: 133)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: Graduate (Master of Science / PhD in S&T).
- eligible_year_levels: MS Track: Years 1 and 2; PhD Track: Years 1, 2, and 3 (up to 4 years for straight-PhD).
- incoming_freshman_only: No (Lateral entry graduate students with earned units are eligible).
- existing_college: Ineligible for undergraduate degree; must possess a completed Bachelor's degree (for MS) or Master's degree (for PhD).
- graduate_students: Yes (Incoming 1st year graduate students and regular ongoing MS/PhD students).
- current_enrollment: Must be admitted or enrolled in an approved MS/PhD program at a National Science Consortium (NSC) member university.
- academic: Must meet the graduate school admission standards of the host NSC member university.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Governed by host NSC university graduate school retention policies).
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE (Uncapped / No income ceiling).
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to ASTHRDP National Science Consortium (NSC) Member Universities: UP Diliman, UP Los Baños, UP Manila, UP Visayas, Ateneo de Manila University, De La Salle University, University of San Carlos, Mindanao State University - Iligan Institute of Technology, Central Luzon State University, and Visayas State University.
- courses: Basic and Applied Sciences: Chemistry, Physics, Biological Sciences, Environmental Science, Meteorology/Earth Sciences, Mathematics, Computer Science, Materials Science, Food Science, Agriculture, and Biotechnology.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE.
- work_experience: None
- good_moral: Required (Validated via valid NBI Clearance).
- health: Physically and mentally fit to undergo graduate studies, as certified by a licensed physician.
- other_rules/conflicts: Must pursue full-time graduate studies; must NOT be employed or practicing a profession while on scholarship unless an official approved leave of absence (LOA) is granted; must execute a scholarship agreement.

### Timing
- who: Graduating college seniors entering graduate school, BS graduates applying for MS, MS graduates applying for PhD, and ongoing MS/PhD students at NSC universities. - Can current freshmen apply?: Ineligible for undergraduate freshmen; incoming 1st-year graduate students may apply.
- freshmen/soph/junior/senior/grad/reapply: : Ineligible for undergraduate freshmen; | : Ineligible for undergraduate sophomores; ongoing | : Ineligible for undergraduate juniors. | : Graduating undergraduate seniors entering an MS program | : Yes (BS/BA graduates for MS; MS graduates for PhD). | : Yes.
- window: Set annually per semester by NSC member universities (e.g., April/May for 1st Semester; September/October for 2nd Semester). → Varies by NSC university (e.g., July 31 for CLSU; August 15 for DLSU). (Semester / Term intake.; AY AY 2025–2026 / AY 2026–2027.)

### Renewal
- maintain_gwa: Maintain required cumulative GPA/GWA set by the host NSC university.
- regular_load: Full-time academic load (9–12 units per regular semester, 3–6 units midyear).
- no_failures: No failing or dropped grades in graduate coursework.
- return_service: Mandatory service obligation in the Philippines on a full-time basis immediately after degree completion, equivalent to one (1) year for every year of scholarship enjoyed.

### Disqualifiers / affiliations
- Unapproved employment or practice of profession while holding the scholarship.
- Academic failure or dropping below the host university's required retention GPA.
- Concurrent enjoyment of another government or private scholarship.
- Non-compliance with post-graduation service obligation (requires full financial refund with interest).

### Benefits (catalog)
- tuition: Full actual tuition and other school fees.
- stipend: ₱30,000.00 per month for MS scholars; ₱38,000.00 per month for PhD scholars.
- allowance: Learning Materials and/or Connectivity Allowance of ₱20,000.00 per Academic Year.

### Documents (operational hidden reqs)
- Accomplished ASTHRDP-NSC Information Sheet / Application Form. 2. Birth Certificate (PSA Photocopy). 3. Certified True Copy of Official Transcript of Records (TOR). 4. Endorsement from two (2) former college professors (for MS) or two (2) former MS professors (for PhD). 5. Medical Certificate from a licensed physician stating applicant is fit to study. 6. Valid NBI Clearance. 7. Official Letter of Admission with regular status from the accepting NSC university. 8. Approved Program of Study. 9. If employed: Recommendation and approved LOA from head of agency, or proof of resignation.

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
  "rank_cutoff_alternative": null,
  "priority_courses": [
    "BASIC_AND_APPLIED_SCIENCES",
    "CHEMISTRY",
    "PHYSICS",
    "BIOLOGY",
    "ENVIRONMENTAL_SCIENCE",
    "MATHEMATICS",
    "COMPUTER_SCIENCE"
  ],
  "school_type": [
    "SUC",
    "PRIVATE_CONSORTIUM_HEI"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "semester_variable",
    "close": "semester_variable"
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
- ● Incomplete Database State: Live database ID 133 has confidence_score: 0.05 and null
- verification: Verified | confidence: 98/100

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Governed by host NSC university graduate school retention policies).) vs renewal (Maintain required cumulative GPA/GWA set by the host NSC university.)

---

## Engineering Research and Development for Technology (ERDT) Scholarship Program (ID: 134)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: Graduate (Master of Science in Engineering / PhD in Engineering).
- eligible_year_levels: MS Track: Years 1 and 2; PhD Track: Years 1, 2, and 3 (up to 4 years for straight-PhD).
- incoming_freshman_only: No (Lateral entry ongoing graduate engineering students are eligible).
- existing_college: Ineligible for undergraduate degree; must possess a completed Bachelor's degree in engineering or related field.
- graduate_students: Yes (Incoming 1st year graduate engineering students and regular ongoing MS/PhD engineering scholars).
- current_enrollment: Must be admitted or enrolled in an approved graduate engineering program at an ERDT Consortium member university.
- academic: Must satisfy the graduate school admission standards of the host ERDT consortium institution.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE (Governed by host ERDT graduate school retention policies).
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE (Uncapped / No income ceiling).
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to the eight (8) ERDT Consortium Member Universities: University of the Philippines Diliman, University of the Philippines Los Baños, Ateneo de Manila University, De La Salle University, Mapúa University, University of San Carlos, Central Luzon State University, and Mindanao State University - Iligan Institute of Technology.
- courses: Graduate Engineering Disciplines: Agricultural and Biosystems Engineering, Chemical Engineering, Civil Engineering, Computer Engineering, Electrical Engineering, Electronics Engineering, Energy Engineering, Environmental Engineering, Industrial Engineering, Materials Science & Engineering, Mechanical Engineering, Mining/Metallurgical Engineering.
- sectoral/hidden: NOT SPECIFIED IN OFFICIAL SOURCE.
- work_experience: None
- good_moral: Required (Validated via valid NBI Clearance).
- health: Physically and mentally fit to study, as certified by a licensed physician.
- other_rules/conflicts: Must pursue full-time graduate engineering studies; must NOT be employed or practicing a profession while on scholarship unless an official approved leave of absence (LOA) is granted; must execute a scholarship agreement.

### Timing
- who: Graduating engineering seniors entering graduate school, BS engineering graduates applying for MS, MS engineering graduates applying for PhD, and ongoing graduate engineering students at ERDT universities.
- freshmen/soph/junior/senior/grad/reapply: : Ineligible for undergraduate freshmen; incoming 1st-year | : Ineligible for undergraduate sophomores; ongoing | : Ineligible for undergraduate juniors. | : Graduating engineering seniors entering an MS program | : Yes (BS Engineering graduates for MS; MS Engineering | : Yes.
- window: Set per term/semester by ERDT member universities (typically March/April for 1st Semester; September/October for 2nd Semester). → Varies by ERDT university. (Semester / Term intake.; AY AY 2025–2026 / AY 2026–2027.)

### Renewal
- maintain_gwa: Maintain required cumulative GPA/GWA set by the host ERDT university.
- regular_load: Full-time academic load per semester as prescribed in the approved POS.
- no_failures: No failing or dropped grades in graduate engineering coursework.
- return_service: Mandatory service obligation in the Philippines on a full-time basis immediately after degree completion, equivalent to one (1) year for every year of scholarship enjoyed.

### Disqualifiers / affiliations
- Unapproved employment or engineering practice while on scholarship.
- Academic failure or dropping below the ERDT institution's retention GWA.
- Concurrent enjoyment of another government or private scholarship grant.
- Non-compliance with return service obligation (requires full financial refund with interest).

### Benefits (catalog)
- tuition: Full actual tuition and other school fees.
- stipend: ₱30,000.00 per month for MS scholars; ₱38,000.00 per month for PhD scholars.
- allowance: Learning Materials and/or Connectivity Allowance of ₱20,000.00 per Academic Year.

### Documents (operational hidden reqs)
- Accomplished ERDT Application Form.
- Birth Certificate (PSA Photocopy).
- Certified True Copy of Official Transcript of Records (TOR) in Engineering.
- Endorsement from two (2) former engineering professors.
- Medical Certificate from a licensed physician.
- Valid NBI Clearance.
- Official Letter of Admission with regular status from the accepting ERDT graduate school.
- Approved Program of Study.
- If employed: Recommendation and approved LOA from head of agency, or proof of resignation.

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
  "rank_cutoff_alternative": null,
  "priority_courses": [
    "ENGINEERING",
    "CIVIL_ENGINEERING",
    "CHEMICAL_ENGINEERING",
    "ELECTRICAL_ENGINEERING",
    "MECHANICAL_ENGINEERING",
    "COMPUTER_ENGINEERING",
    "ENVIRONMENTAL_ENGINEERING"
  ],
  "school_type": [
    "SUC",
    "PRIVATE_CONSORTIUM_HEI"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "applic[ span_242](end_span)ation_win dow": {
    "open": "semester_variable",
    "close": "semester_variable"
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
- ● Incomplete Database Mapping: Live database ID 134 has confidence_score: 0.05 and
- verification: Verified | confidence: 98/100

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE (Governed by host ERDT graduate school retention policies).) vs renewal (Maintain required cumulative GPA/GWA set by the host ERDT university.)

---

## Capacity Building Program in Science and Mathematics Education (CBPSME) (ID: 135)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen.
- residency/destination: NOT SPECIFIED IN OFFICIAL SOURCE.
- education_level: Graduate (Master's / PhD in Science/Mathematics Education).
- eligible_year_levels: MS Track: Years 1 and 2; PhD Track: Years 1, 2, and 3.
- incoming_freshman_only: No (Lateral entry ongoing graduate education students are eligible).
- existing_college: Ineligible for undergraduate degree; must possess a completed Bachelor's degree in education, science, or mathematics.
- graduate_students: Yes (Incoming 1st year graduate education students and regular ongoing MS/PhD education scholars).
- current_enrollment: Must be admitted or enrolled in an approved graduate program in Science or Mathematics Education at a CBPSME Consortium University.
- academic: Must satisfy the graduate school admission standards of the host CBPSME member university.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted strictly to CBPSME Consortium Member Universities (e.g., Philippine Normal University, DLSU, UP Diliman, West Visayas State University, Bicol University, MSU-IIT, University of San Carlos, etc.).
- courses: Master's and Doctoral Programs in Science Education, Mathematics Education, Physics Teaching, Chemistry Teaching, Biology Teaching, and General Science Education.
- sectoral/hidden: Must be an active Science or Mathematics teacher/educator in basic education (DepEd or private school) or a higher education institution.
- work_experience: None
- good_moral: Required (Validated via NBI Clearance or Good Moral Certificate).
- health: Physically and mentally fit to undergo graduate studies, as certified by a licensed physician.
- other_rules/conflicts: Must secure an official study leave of absence from DepEd or employer; must execute a service contract binding the scholar to teach or serve in science/math education in the Philippines post-graduation.

### Timing
- who: Science and Mathematics teachers in DepEd/private schools, college science/math educators, and qualified graduates entering science/math education graduate programs.
- freshmen/soph/junior/senior/grad/reapply: : Ineligible for undergraduate freshmen; incoming 1st-year | : Ineligible for undergraduate sophomores; ongoing | : Ineligible for undergraduate juniors. | : Graduating education/science majors entering graduate | : Yes (BS Education/Science graduates for MS; MS Science | : Yes.
- window: Set annually per semester by CBPSME consortium universities (e.g., April/May for 1st Semester; September/October for 2nd Semester). → Varies by CBPSME university (e.g., June 30 for DepEd endorsement deadlines). (Semester / Term intake.; AY AY 2025–2026 / AY 2026–2027.)

### Renewal
- maintain_gwa: Maintain required cumulative GPA/GWA set by host CBPSME university.
- regular_load: Full-time credit load per semester as prescribed in POS.
- no_failures: No failing grades in graduate education subjects.
- return_service: Mandatory service obligation in teaching science/math in the Philippines immediately after degree completion, equivalent to one (1) year for every year of scholarship enjoyed.

### Disqualifiers / affiliations
- Failure to secure an approved official leave of absence from DepEd or employer.
- Academic failure or dropping below host university's retention standards.
- Concurrent enjoyment of another government scholarship.
- Refusal to render mandatory science/math teaching return service post-graduation.

### Benefits (catalog)
- tuition: Full actual tuition and other school fees.
- stipend: ₱30,000.00 per month for MS scholars; ₱38,000.00 per month for PhD scholars.
- allowance: Learning Materials and/or Connectivity Allowance of ₱20,000.00 per Academic Year.

### Documents (operational hidden reqs)
- Accomplished CBPSME Application Form.
- Birth Certificate (PSA Photocopy).
- Certified True Copy of Official Transcript of Records (TOR).
- Endorsement from two (2) former professors or school administrators.
- Medical Certificate from a licensed physician.
- Valid NBI Clearance.
- Letter of Admission with regular status from accepting CBPSME university.
- Approved Program of Study.
- Official DepEd or employer recommendation and approved Leave of Absence (LOA).

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
  "rank_cutoff_alternative": null,
  "sectoral_restriction": "SCIENCE_MATHEMATICS_TEACHER_EDUCATOR",
  "priority_courses": [
    "SCIENCE_EDUCATION",
    "MATHEMATICS_EDUCATION",
    "PHYSICS_TEACHING",
    "CHEMISTRY_TEACHING",
    "BIOLOGY_TEACHING"
  ],
  "school_type": [
    "SUC",
    "PRIVATE_CONSORTIUM_HEI[span _180](start_span)"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "semester_variable",
    "close": "semester_variable"
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
- ● Missing Sectoral Tag: Live database ID 135 lacks an educator sectoral restriction tag.
- verification: Verified - Last Verified Date: 2026-08-05 | confidence: 98/100

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE.) vs renewal (Maintain required cumulative GPA/GWA set by host CBPSME university.)

---

## Science and Technology Education for Regional Development (STRAND) - (formerly Science and Technology Regional Alliance of Universities for National Development) (ID: 136)

### Hard eligibility
- citizenship: Natural-born or naturalized Filipino citizen.
- residency/destination: Regional / Provincial HEI employment focus.
- education_level: Graduate (Master's Degree and PhD in S&T).
- eligible_year_levels: MS Track: Years 1 and 2; PhD Track: Years 1, 2, and 3.
- incoming_freshman_only: No (Lateral entry ongoing graduate students are eligible).
- existing_college: Ineligible for undergraduate degree; must possess a completed Bachelor's degree (for MS) or Master's degree (for PhD).
- graduate_students: Yes (Incoming 1st year graduate students and regular ongoing MS/PhD faculty scholars).
- current_enrollment: Must be admitted or enrolled in an approved graduate S&T program at a STRAND delivering/sending consortium university.
- academic: Must meet the graduate admission standards of the accepting STRAND university.
- minimum_gwa: NOT SPECIFIED IN OFFICIAL SOURCE.
- alt_class_rank: NOT SPECIFIED IN OFFICIAL SOURCE.
- income_ceilings: NOT SPECIFIED IN OFFICIAL SOURCE.
- age: NOT SPECIFIED IN OFFICIAL SOURCE.
- school/consortium: Restricted to STRAND Member Delivering and Sending Higher Education Institutions (Provincial/Regional SUCs and HEIs outside NCR).
- courses: Priority S&T Graduate Programs aligned with regional development agendas.
- sectoral/hidden: Must be a regular or plantilla faculty member of an eligible regional/provincial higher education institution (HEI).
- work_experience: None
- good_moral: Required (Validated via NBI Clearance or Good Moral Certificate).
- health: Physically and mentally fit to undergo graduate studies, as certified by a licensed physician.
- other_rules/conflicts: Must secure an official study leave of absence (LOA) from the home sending HEI; must execute a service contract to return to the home regional HEI to render service upon degree completion.

### Timing
- who: Regular/plantilla faculty members of regional SUCs and HEIs pursuing MS or PhD degrees in priority S&T fields.
- freshmen/soph/junior/senior/grad/reapply: : Ineligible for undergraduate freshmen; incoming 1st-year | : Ineligible for undergraduate sophomores; ongoing | : Ineligible for undergraduate juniors. | : Ineligible (must be an employed faculty member of a regional | : Yes (Faculty members holding BS degrees applying for MS, or | : Yes.
- window: Set annually per semester by STRAND consortium universities. → Varies by regional consortium university. (Semester / Term intake.; AY AY 2025–2026 / AY 2026–2027.)

### Renewal
- maintain_gwa: Maintain required cumulative GPA/GWA set by host STRAND university.
- regular_load: Full-time credit load per term as prescribed in POS.
- no_failures: No failing grades in graduate coursework.
- return_service: Mandatory return service obligation to the sending regional HEI immediately after degree completion, equivalent to one (1) year for every year of scholarship enjoyed.

### Disqualifiers / affiliations
- Non-faculty status or failure to secure an approved LOA from the regional sending HEI.
- Academic failure or dropping below host university retention standards.
- Concurrent enjoyment of another government scholarship.
- Failure to return to the home regional HEI to render service post-graduation.

### Benefits (catalog)
- tuition: Full actual tuition and other school fees.
- stipend: ₱30,000.00 per month for MS scholars; ₱38,000.00 per month for PhD scholars.
- allowance: Learning Materials and/or Connectivity Allowance of ₱20,000.00 per Academic Year.

### Documents (operational hidden reqs)
- Accomplished STRAND Application Form.
- Birth Certificate (PSA Photocopy).
- Certified True Copy of Official Transcript of Records (TOR).
- Endorsement from two (2) former professors or department heads.
- Medical Certificate from a licensed physician.
- Valid NBI Clearance.
- Official Letter of Admission with regular status from accepting STRAND university.
- Approved Program of Study.
- Official recommendation and approved Leave of Absence (LOA) from the President/Head of the sending regional HEI.

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
  "rank_cutoff_alternative": null,
  "sectoral_restriction": "REGIONAL_HEI_FACULTY_MEMBER",
  "priority_courses": [
    "DOST-SEIPRIORITYREGIONALS&TFIELDS"
  ],
  "school_type": [
    "SUC",
    "LUC",
    "PRIVATE_CONSORTIUM_HEI"
  ],
  "partner_school_restricted": true,
  "citizenship": "Filipino",
  "application_window": {
    "open": "semester_variable",
    "close": "semester_variable"
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
- ● Omission of Faculty Filter: Live database record ID 136 lacks an explicit regional faculty
- verification: Verified | confidence: 98/100

- CONTRADICTION/NOTE: entry GWA (NOT SPECIFIED IN OFFICIAL SOURCE.) vs renewal (Maintain required cumulative GPA/GWA set by host STRAND university.)

---
