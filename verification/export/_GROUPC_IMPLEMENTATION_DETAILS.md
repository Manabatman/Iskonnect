# Group C Verification PDFs — Implementation Details Extraction

Exhaustive hard-rule extraction for matching/catalog implications. Structured by source PDF then by scholarship.

## SOURCE: `DATABASE_V3_GROUPC_DOST_GRADUATE.pdf`

**Scholarships in this PDF:** 5

### DOST-SEI Graduate Scholarship Programs (Umbrella Entry covering ASTHRDP, CBPSME, ERDT, and STRAND) (ID: 3)

#### Identity / Affiliations
- **Provider:** Department of Science and Technology - Science Education Institute (DOST-SEI)
- **Category:** Government / National / Graduate / Merit-based
- **Website:** https://www.science-scholarships.ph/
- **Portal:** https://www.science-scholarships.ph/
- **Guidelines:** DOST-SEI Local Graduate Scholarship Guidelines & Application E-Forms
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** Graduate (Master's Degree and Doctoral/PhD Degree).
- **Eligible Year Levels:** MS Program: Years 1 and 2; PhD Program: Years 1, 2, and 3 (up to Year 4 for straight-PhD track).
- **Incoming Freshman Only:** No (Lateral entry ongoing graduate students with earned units are eligible).
- **Existing College Students:** Ineligible for undergraduate degree enrollment; applicants must possess a completed Bachelor's degree (for MS) or Master's degree (for PhD).
- **Graduate Students:** Yes (Incoming 1st year graduate students and regular ongoing MS/PhD students).
- **Current Enrollment:** Must be admitted or enrolled as a regular graduate student in an approved priority S&T program at a DOST-SEI consortium member university.
- **Academic Requirements:** Must meet the admission requirements for graduate studies at the accepting consortium university.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Governed by host university graduate school admission and retention standards; live database entry of 88% is an unverified artifact).
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE (Uncapped / No parental or personal income limit is imposed in official DOST graduate guidelines; live database cap of ₱500,000 is incorrect).
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted to designated DOST-SEI Graduate Scholarship Consortium Member Universities (e.g., NSC, ERDT, CBPSME, and STRAND consortia).
- **Course Restrictions:** DOST-SEI Priority S&T Fields (Natural Sciences, Engineering, Science & Mathematics Education, Agriculture, Computer Science, etc.).
- **Sectoral / Hidden Requirements:** Educator status for CBPSME; Regional HEI faculty status for STRAND.
- **Good Moral:** Required (Validated via NBI Clearance or Certificate of Good Moral Character).
- **Health:** Physically and mentally fit to study, as certified by a licensed physician.
- **Other Official Rules / Conflicts:** Must be a full-time student; must NOT be employed or practicing a profession while on scholarship, or must secure an official approved leave of absence (LOA) from the employer; must not enjoy concurrent government or private scholarships; must execute a service contract.

#### Timing
- **Who May Apply:** Graduating college seniors entering graduate school, BS/BA degree holders applying for MS, MS degree holders applying for PhD, and regular ongoing MS/PhD students.
- **Freshmen:** : Ineligible for undergraduate freshmen; incoming 1st-year
- **Sophomores:** : Ineligible for undergraduate sophomores; ongoing
- **Juniors:** : Ineligible for undergraduate juniors.
- **Seniors:** : Graduating college seniors entering an MS program upon
- **Graduates:** : Yes (Bachelor's graduates for MS; Master's graduates for PhD).
- **Reapply:** : Yes.
- **Opening:** Announced per academic cycle by consortium universities (typically March/April for 1st Semester; September/October for 2nd Semester).
- **Closing:** Varies by university (e.g., June 30 for 1st Semester intake).
- **Cycle:** Semester / Term intake.
- **AY Covered:** AY 2025–2026 / AY 2026–2027.

#### Benefits (catalog)
- **Tuition:** Full actual tuition and other school fees.
- **Monthly Stipend:** ₱30,000.00 per month for MS scholars; ₱38,000.00 per month for PhD scholars.
- **Allowance:** Learning Materials and/or Connectivity Allowance of ₱20,000.00 per Academic Year.
- **Return Service:** Mandatory return service obligation in the Philippines on a full-time basis immediately after degree completion, equivalent to one (1) year of service for every year of scholarship availed.

#### Renewal
- **Maintain GWA:** Must maintain a satisfactory General Weighted Average (GWA/GPA) prescribed by the host graduate school each term.
- **Regular Load:** Must carry a full academic load per semester based on the approved Program of Study (9–12 units regular term, 3–6 units midyear).
- **No Failures:** Must have no failing, incomplete, or dropped grades in coursework.

#### Disqualifying / Conflicts
- Employment or professional practice while on scholarship without an approved official leave of absence.
- Failure to maintain academic retention standards or receiving a failing grade in any graduate subject.
- Concurrent enjoyment of another government or private scholarship covering the same degree program.
- Failure to comply with the return service obligation or non-completion of the degree program without valid justification (requires full financial refund with interest).

#### Required Documents (hidden operational requirements)
- Duly accomplished DOST-SEI Graduate Scholarship Information Sheet / Application Form.
- PSA Birth Certificate (Photocopy).
- Certified True Copy of Official Transcript of Records (TOR) for BS (and MS if applying for PhD).
- Official Endorsement Forms from two (2) former college professors (for MS) or two (2) former MS professors (for PhD).
- Medical Certificate from a licensed physician stating the applicant is physically and mentally fit to study.
- Valid NBI Clearance.
- Official Letter of Admission with regular status from the Program Head of the accepting institution.
- Approved Program of Study (POS).
- If employed: Official recommendation and approved Leave of Absence (LOA) from the head of agency, or proof of resignation.

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": null, "income_limit": null, "rank_cutoff_alternative": null, "priority_courses": ["DOST-SEIPRIORITYS&TGRADUATEFIELDS"], "school_type": ["SUC", "LUC", "PRIVATE_CONSORTIUM_HEI"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "semester_variable", "close": "semester_variable"}, "deadline_type": "exact", "cycle_type": "semester", "renewable": true, "first_time_only": false, "return_service_required": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Corrupted Financial Parameters: Live database ID 3 sets max_income: 500000 and
- **Verification:** Verified | Confidence: n/a
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Governed by host university graduate school admission and retention standards; live database entry of 88% is an unverified artifact).) differs from renewal Maintain GWA (Must maintain a satisfactory General Weighted Average (GWA/GPA) prescribed by the host graduate school each term.)
  - Live DB GWA vs official NOT SPECIFIED: NOT SPECIFIED IN OFFICIAL SOURCE (Governed by host university graduate school admission and retention standards; live database entry of 88% is an unverified artifact).

---

### Accelerated Science and Technology Human Resource Development Program (ASTHRDP) (ID: 133)

#### Identity / Affiliations
- **Provider:** Department of Science and Technology - Science Education Institute (DOST-SEI)
- **Category:** Government / National / Graduate / Merit-based
- **Website:** https://asthrdp.science-scholarships.ph/
- **Portal:** https://asthrdp.science-scholarships.ph/
- **Guidelines:** DOST-SEI ASTHRDP-NSC Information Sheet & Scholar Handbook
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** Graduate (Master of Science / PhD in S&T).
- **Eligible Year Levels:** MS Track: Years 1 and 2; PhD Track: Years 1, 2, and 3 (up to 4 years for straight-PhD).
- **Incoming Freshman Only:** No (Lateral entry graduate students with earned units are eligible).
- **Existing College Students:** Ineligible for undergraduate degree; must possess a completed Bachelor's degree (for MS) or Master's degree (for PhD).
- **Graduate Students:** Yes (Incoming 1st year graduate students and regular ongoing MS/PhD students).
- **Current Enrollment:** Must be admitted or enrolled in an approved MS/PhD program at a National Science Consortium (NSC) member university.
- **Academic Requirements:** Must meet the graduate school admission standards of the host NSC member university.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Governed by host NSC university graduate school retention policies).
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE (Uncapped / No income ceiling).
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to ASTHRDP National Science Consortium (NSC) Member Universities: UP Diliman, UP Los Baños, UP Manila, UP Visayas, Ateneo de Manila University, De La Salle University, University of San Carlos, Mindanao State University - Iligan Institute of Technology, Central Luzon State University, and Visayas State University.
- **Course Restrictions:** Basic and Applied Sciences: Chemistry, Physics, Biological Sciences, Environmental Science, Meteorology/Earth Sciences, Mathematics, Computer Science, Materials Science, Food Science, Agriculture, and Biotechnology.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Good Moral:** Required (Validated via valid NBI Clearance).
- **Health:** Physically and mentally fit to undergo graduate studies, as certified by a licensed physician.
- **Other Official Rules / Conflicts:** Must pursue full-time graduate studies; must NOT be employed or practicing a profession while on scholarship unless an official approved leave of absence (LOA) is granted; must execute a scholarship agreement.

#### Timing
- **Who May Apply:** Graduating college seniors entering graduate school, BS graduates applying for MS, MS graduates applying for PhD, and ongoing MS/PhD students at NSC universities. - Can current freshmen apply?: Ineligible for undergraduate freshmen; incoming 1st-year graduate students may apply.
- **Freshmen:** : Ineligible for undergraduate freshmen;
- **Sophomores:** : Ineligible for undergraduate sophomores; ongoing
- **Juniors:** : Ineligible for undergraduate juniors.
- **Seniors:** : Graduating undergraduate seniors entering an MS program
- **Graduates:** : Yes (BS/BA graduates for MS; MS graduates for PhD).
- **Reapply:** : Yes.
- **Opening:** Set annually per semester by NSC member universities (e.g., April/May for 1st Semester; September/October for 2nd Semester).
- **Closing:** Varies by NSC university (e.g., July 31 for CLSU; August 15 for DLSU).
- **Cycle:** Semester / Term intake.
- **AY Covered:** AY 2025–2026 / AY 2026–2027.

#### Benefits (catalog)
- **Tuition:** Full actual tuition and other school fees.
- **Monthly Stipend:** ₱30,000.00 per month for MS scholars; ₱38,000.00 per month for PhD scholars.
- **Allowance:** Learning Materials and/or Connectivity Allowance of ₱20,000.00 per Academic Year.
- **Return Service:** Mandatory service obligation in the Philippines on a full-time basis immediately after degree completion, equivalent to one (1) year for every year of scholarship enjoyed.

#### Renewal
- **Maintain GWA:** Maintain required cumulative GPA/GWA set by the host NSC university.
- **Regular Load:** Full-time academic load (9–12 units per regular semester, 3–6 units midyear).
- **No Failures:** No failing or dropped grades in graduate coursework.

#### Disqualifying / Conflicts
- Unapproved employment or practice of profession while holding the scholarship.
- Academic failure or dropping below the host university's required retention GPA.
- Concurrent enjoyment of another government or private scholarship.
- Non-compliance with post-graduation service obligation (requires full financial refund with interest).

#### Required Documents (hidden operational requirements)
- Accomplished ASTHRDP-NSC Information Sheet / Application Form. 2. Birth Certificate (PSA Photocopy). 3. Certified True Copy of Official Transcript of Records (TOR). 4. Endorsement from two (2) former college professors (for MS) or two (2) former MS professors (for PhD). 5. Medical Certificate from a licensed physician stating applicant is fit to study. 6. Valid NBI Clearance. 7. Official Letter of Admission with regular status from the accepting NSC university. 8. Approved Program of Study. 9. If employed: Recommendation and approved LOA from head of agency, or proof of resignation.

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": null, "income_limit": null, "rank_cutoff_alternative": null, "priority_courses": ["BASIC_AND_APPLIED_SCIENCES", "CHEMISTRY", "PHYSICS", "BIOLOGY", "ENVIRONMENTAL_SCIENCE", "MATHEMATICS", "COMPUTER_SCIENCE"], "school_type": ["SUC", "PRIVATE_CONSORTIUM_HEI"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "semester_variable", "close": "semester_variable"}, "deadline_type": "exact", "cycle_type": "semester", "renewable": true, "first_time_only": false, "return_service_required": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Incomplete Database State: Live database ID 133 has confidence_score: 0.05 and null
- **Verification:** Verified | Confidence: 98/100
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Governed by host NSC university graduate school retention policies).) differs from renewal Maintain GWA (Maintain required cumulative GPA/GWA set by the host NSC university.)

---

### Engineering Research and Development for Technology (ERDT) Scholarship Program (ID: 134)

#### Identity / Affiliations
- **Provider:** Department of Science and Technology - Science Education Institute (DOST-SEI)
- **Category:** Government / National / Graduate / Merit-based
- **Website:** https://erdt.science-scholarships.ph/
- **Portal:** https://erdt.science-scholarships.ph/
- **Guidelines:** ERDT Graduate Scholarship Program Guidelines & Brochure
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** Graduate (Master of Science in Engineering / PhD in Engineering).
- **Eligible Year Levels:** MS Track: Years 1 and 2; PhD Track: Years 1, 2, and 3 (up to 4 years for straight-PhD).
- **Incoming Freshman Only:** No (Lateral entry ongoing graduate engineering students are eligible).
- **Existing College Students:** Ineligible for undergraduate degree; must possess a completed Bachelor's degree in engineering or related field.
- **Graduate Students:** Yes (Incoming 1st year graduate engineering students and regular ongoing MS/PhD engineering scholars).
- **Current Enrollment:** Must be admitted or enrolled in an approved graduate engineering program at an ERDT Consortium member university.
- **Academic Requirements:** Must satisfy the graduate school admission standards of the host ERDT consortium institution.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Governed by host ERDT graduate school retention policies).
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE (Uncapped / No income ceiling).
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to the eight (8) ERDT Consortium Member Universities: University of the Philippines Diliman, University of the Philippines Los Baños, Ateneo de Manila University, De La Salle University, Mapúa University, University of San Carlos, Central Luzon State University, and Mindanao State University - Iligan Institute of Technology.
- **Course Restrictions:** Graduate Engineering Disciplines: Agricultural and Biosystems Engineering, Chemical Engineering, Civil Engineering, Computer Engineering, Electrical Engineering, Electronics Engineering, Energy Engineering, Environmental Engineering, Industrial Engineering, Materials Science & Engineering, Mechanical Engineering, Mining/Metallurgical Engineering.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Good Moral:** Required (Validated via valid NBI Clearance).
- **Health:** Physically and mentally fit to study, as certified by a licensed physician.
- **Other Official Rules / Conflicts:** Must pursue full-time graduate engineering studies; must NOT be employed or practicing a profession while on scholarship unless an official approved leave of absence (LOA) is granted; must execute a scholarship agreement.

#### Timing
- **Who May Apply:** Graduating engineering seniors entering graduate school, BS engineering graduates applying for MS, MS engineering graduates applying for PhD, and ongoing graduate engineering students at ERDT universities.
- **Freshmen:** : Ineligible for undergraduate freshmen; incoming 1st-year
- **Sophomores:** : Ineligible for undergraduate sophomores; ongoing
- **Juniors:** : Ineligible for undergraduate juniors.
- **Seniors:** : Graduating engineering seniors entering an MS program
- **Graduates:** : Yes (BS Engineering graduates for MS; MS Engineering
- **Reapply:** : Yes.
- **Opening:** Set per term/semester by ERDT member universities (typically March/April for 1st Semester; September/October for 2nd Semester).
- **Closing:** Varies by ERDT university.
- **Cycle:** Semester / Term intake.
- **AY Covered:** AY 2025–2026 / AY 2026–2027.

#### Benefits (catalog)
- **Tuition:** Full actual tuition and other school fees.
- **Monthly Stipend:** ₱30,000.00 per month for MS scholars; ₱38,000.00 per month for PhD scholars.
- **Allowance:** Learning Materials and/or Connectivity Allowance of ₱20,000.00 per Academic Year.
- **Return Service:** Mandatory service obligation in the Philippines on a full-time basis immediately after degree completion, equivalent to one (1) year for every year of scholarship enjoyed.

#### Renewal
- **Maintain GWA:** Maintain required cumulative GPA/GWA set by the host ERDT university.
- **Regular Load:** Full-time academic load per semester as prescribed in the approved POS.
- **No Failures:** No failing or dropped grades in graduate engineering coursework.

#### Disqualifying / Conflicts
- Unapproved employment or engineering practice while on scholarship.
- Academic failure or dropping below the ERDT institution's retention GWA.
- Concurrent enjoyment of another government or private scholarship grant.
- Non-compliance with return service obligation (requires full financial refund with interest).

#### Required Documents (hidden operational requirements)
- Accomplished ERDT Application Form.
- Birth Certificate (PSA Photocopy).
- Certified True Copy of Official Transcript of Records (TOR) in Engineering.
- Endorsement from two (2) former engineering professors.
- Medical Certificate from a licensed physician.
- Valid NBI Clearance.
- Official Letter of Admission with regular status from the accepting ERDT graduate school.
- Approved Program of Study.
- If employed: Recommendation and approved LOA from head of agency, or proof of resignation.

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": null, "income_limit": null, "rank_cutoff_alternative": null, "priority_courses": ["ENGINEERING", "CIVIL_ENGINEERING", "CHEMICAL_ENGINEERING", "ELECTRICAL_ENGINEERING", "MECHANICAL_ENGINEERING", "COMPUTER_ENGINEERING", "ENVIRONMENTAL_ENGINEERING"], "school_type": ["SUC", "PRIVATE_CONSORTIUM_HEI"], "partner_school_restricted": true, "citizenship": "Filipino", "applic[ span_242](end_span)ation_win dow": {"open": "semester_variable", "close": "semester_variable"}, "deadline_type": "exact", "cycle_type": "semester", "renewable": true, "first_time_only": false, "return_service_required": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Incomplete Database Mapping: Live database ID 134 has confidence_score: 0.05 and
- **Verification:** Verified | Confidence: 98/100
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Governed by host ERDT graduate school retention policies).) differs from renewal Maintain GWA (Maintain required cumulative GPA/GWA set by the host ERDT university.)

---

### Capacity Building Program in Science and Mathematics Education (CBPSME) (ID: 135)

#### Identity / Affiliations
- **Provider:** Department of Science and Technology - Science Education Institute (DOST-SEI)
- **Category:** Government / National / Graduate / Educator Sectoral
- **Website:** https://cbpsme.science-scholarships.ph/
- **Portal:** https://cbpsme.science-scholarships.ph/
- **Guidelines:** CBPSME Graduate Scholarship Guidelines & Application Forms
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** Graduate (Master's / PhD in Science/Mathematics Education).
- **Eligible Year Levels:** MS Track: Years 1 and 2; PhD Track: Years 1, 2, and 3.
- **Incoming Freshman Only:** No (Lateral entry ongoing graduate education students are eligible).
- **Existing College Students:** Ineligible for undergraduate degree; must possess a completed Bachelor's degree in education, science, or mathematics.
- **Graduate Students:** Yes (Incoming 1st year graduate education students and regular ongoing MS/PhD education scholars).
- **Current Enrollment:** Must be admitted or enrolled in an approved graduate program in Science or Mathematics Education at a CBPSME Consortium University.
- **Academic Requirements:** Must satisfy the graduate school admission standards of the host CBPSME member university.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to CBPSME Consortium Member Universities (e.g., Philippine Normal University, DLSU, UP Diliman, West Visayas State University, Bicol University, MSU-IIT, University of San Carlos, etc.).
- **Course Restrictions:** Master's and Doctoral Programs in Science Education, Mathematics Education, Physics Teaching, Chemistry Teaching, Biology Teaching, and General Science Education.
- **Sectoral / Hidden Requirements:** Must be an active Science or Mathematics teacher/educator in basic education (DepEd or private school) or a higher education institution.
- **Good Moral:** Required (Validated via NBI Clearance or Good Moral Certificate).
- **Health:** Physically and mentally fit to undergo graduate studies, as certified by a licensed physician.
- **Other Official Rules / Conflicts:** Must secure an official study leave of absence from DepEd or employer; must execute a service contract binding the scholar to teach or serve in science/math education in the Philippines post-graduation.

#### Timing
- **Who May Apply:** Science and Mathematics teachers in DepEd/private schools, college science/math educators, and qualified graduates entering science/math education graduate programs.
- **Freshmen:** : Ineligible for undergraduate freshmen; incoming 1st-year
- **Sophomores:** : Ineligible for undergraduate sophomores; ongoing
- **Juniors:** : Ineligible for undergraduate juniors.
- **Seniors:** : Graduating education/science majors entering graduate
- **Graduates:** : Yes (BS Education/Science graduates for MS; MS Science
- **Reapply:** : Yes.
- **Opening:** Set annually per semester by CBPSME consortium universities (e.g., April/May for 1st Semester; September/October for 2nd Semester).
- **Closing:** Varies by CBPSME university (e.g., June 30 for DepEd endorsement deadlines).
- **Cycle:** Semester / Term intake.
- **AY Covered:** AY 2025–2026 / AY 2026–2027.

#### Benefits (catalog)
- **Tuition:** Full actual tuition and other school fees.
- **Monthly Stipend:** ₱30,000.00 per month for MS scholars; ₱38,000.00 per month for PhD scholars.
- **Allowance:** Learning Materials and/or Connectivity Allowance of ₱20,000.00 per Academic Year.
- **Return Service:** Mandatory service obligation in teaching science/math in the Philippines immediately after degree completion, equivalent to one (1) year for every year of scholarship enjoyed.

#### Renewal
- **Maintain GWA:** Maintain required cumulative GPA/GWA set by host CBPSME university.
- **Regular Load:** Full-time credit load per semester as prescribed in POS.
- **No Failures:** No failing grades in graduate education subjects.

#### Disqualifying / Conflicts
- Failure to secure an approved official leave of absence from DepEd or employer.
- Academic failure or dropping below host university's retention standards.
- Concurrent enjoyment of another government scholarship.
- Refusal to render mandatory science/math teaching return service post-graduation.

#### Required Documents (hidden operational requirements)
- Accomplished CBPSME Application Form.
- Birth Certificate (PSA Photocopy).
- Certified True Copy of Official Transcript of Records (TOR).
- Endorsement from two (2) former professors or school administrators.
- Medical Certificate from a licensed physician.
- Valid NBI Clearance.
- Letter of Admission with regular status from accepting CBPSME university.
- Approved Program of Study.
- Official DepEd or employer recommendation and approved Leave of Absence (LOA).

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": null, "income_limit": null, "rank_cutoff_alternative": null, "sectoral_restriction": "SCIENCE_MATHEMATICS_TEACHER_EDUCATOR", "priority_courses": ["SCIENCE_EDUCATION", "MATHEMATICS_EDUCATION", "PHYSICS_TEACHING", "CHEMISTRY_TEACHING", "BIOLOGY_TEACHING"], "school_type": ["SUC", "PRIVATE_CONSORTIUM_HEI[span _180](start_span)"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "semester_variable", "close": "semester_variable"}, "deadline_type": "exact", "cycle_type": "semester", "renewable": true, "first_time_only": false, "return_service_required": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Missing Sectoral Tag: Live database ID 135 lacks an educator sectoral restriction tag.
- **Verification:** Verified - Last Verified Date: 2026-08-05 | Confidence: 98/100
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE.) differs from renewal Maintain GWA (Maintain required cumulative GPA/GWA set by host CBPSME university.)

---

### Science and Technology Education for Regional Development (STRAND) - (formerly Science and Technology Regional Alliance of Universities for National Development) (ID: 136)

#### Identity / Affiliations
- **Provider:** Department of Science and Technology - Science Education Institute (DOST-SEI)
- **Category:** Government / National / Graduate / Institutional Faculty Sectoral
- **Website:** https://www.science-scholarships.ph/
- **Portal:** https://www.science-scholarships.ph/
- **Guidelines:** DOST-SEI STRAND Graduate Scholarship Guidelines
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen.
- **Residency / Destination:** Regional / Provincial HEI employment focus.
- **Education Level:** Graduate (Master's Degree and PhD in S&T).
- **Eligible Year Levels:** MS Track: Years 1 and 2; PhD Track: Years 1, 2, and 3.
- **Incoming Freshman Only:** No (Lateral entry ongoing graduate students are eligible).
- **Existing College Students:** Ineligible for undergraduate degree; must possess a completed Bachelor's degree (for MS) or Master's degree (for PhD).
- **Graduate Students:** Yes (Incoming 1st year graduate students and regular ongoing MS/PhD faculty scholars).
- **Current Enrollment:** Must be admitted or enrolled in an approved graduate S&T program at a STRAND delivering/sending consortium university.
- **Academic Requirements:** Must meet the graduate admission standards of the accepting STRAND university.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted to STRAND Member Delivering and Sending Higher Education Institutions (Provincial/Regional SUCs and HEIs outside NCR).
- **Course Restrictions:** Priority S&T Graduate Programs aligned with regional development agendas.
- **Sectoral / Hidden Requirements:** Must be a regular or plantilla faculty member of an eligible regional/provincial higher education institution (HEI).
- **Good Moral:** Required (Validated via NBI Clearance or Good Moral Certificate).
- **Health:** Physically and mentally fit to undergo graduate studies, as certified by a licensed physician.
- **Other Official Rules / Conflicts:** Must secure an official study leave of absence (LOA) from the home sending HEI; must execute a service contract to return to the home regional HEI to render service upon degree completion.

#### Timing
- **Who May Apply:** Regular/plantilla faculty members of regional SUCs and HEIs pursuing MS or PhD degrees in priority S&T fields.
- **Freshmen:** : Ineligible for undergraduate freshmen; incoming 1st-year
- **Sophomores:** : Ineligible for undergraduate sophomores; ongoing
- **Juniors:** : Ineligible for undergraduate juniors.
- **Seniors:** : Ineligible (must be an employed faculty member of a regional
- **Graduates:** : Yes (Faculty members holding BS degrees applying for MS, or
- **Reapply:** : Yes.
- **Opening:** Set annually per semester by STRAND consortium universities.
- **Closing:** Varies by regional consortium university.
- **Cycle:** Semester / Term intake.
- **AY Covered:** AY 2025–2026 / AY 2026–2027.

#### Benefits (catalog)
- **Tuition:** Full actual tuition and other school fees.
- **Monthly Stipend:** ₱30,000.00 per month for MS scholars; ₱38,000.00 per month for PhD scholars.
- **Allowance:** Learning Materials and/or Connectivity Allowance of ₱20,000.00 per Academic Year.
- **Return Service:** Mandatory return service obligation to the sending regional HEI immediately after degree completion, equivalent to one (1) year for every year of scholarship enjoyed.

#### Renewal
- **Maintain GWA:** Maintain required cumulative GPA/GWA set by host STRAND university.
- **Regular Load:** Full-time credit load per term as prescribed in POS.
- **No Failures:** No failing grades in graduate coursework.

#### Disqualifying / Conflicts
- Non-faculty status or failure to secure an approved LOA from the regional sending HEI.
- Academic failure or dropping below host university retention standards.
- Concurrent enjoyment of another government scholarship.
- Failure to return to the home regional HEI to render service post-graduation.

#### Required Documents (hidden operational requirements)
- Accomplished STRAND Application Form.
- Birth Certificate (PSA Photocopy).
- Certified True Copy of Official Transcript of Records (TOR).
- Endorsement from two (2) former professors or department heads.
- Medical Certificate from a licensed physician.
- Valid NBI Clearance.
- Official Letter of Admission with regular status from accepting STRAND university.
- Approved Program of Study.
- Official recommendation and approved Leave of Absence (LOA) from the President/Head of the sending regional HEI.

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": null, "income_limit": null, "rank_cutoff_alternative": null, "sectoral_restriction": "REGIONAL_HEI_FACULTY_MEMBER", "priority_courses": ["DOST-SEIPRIORITYREGIONALS&TFIELDS"], "school_type": ["SUC", "LUC", "PRIVATE_CONSORTIUM_HEI"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "semester_variable", "close": "semester_variable"}, "deadline_type": "exact", "cycle_type": "semester", "renewable": true, "first_time_only": false, "return_service_required": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Omission of Faculty Filter: Live database record ID 136 lacks an explicit regional faculty
- **Verification:** Verified | Confidence: 98/100
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE.) differs from renewal Maintain GWA (Maintain required cumulative GPA/GWA set by host STRAND university.)

---

## SOURCE: `DATABASE_V3_GROUPC_INTERNATIONAL.pdf`

**Scholarships in this PDF:** 11

### TaiwanICDF International Higher Education Scholarship Program3 (ID: 60)

#### Identity / Affiliations
- **Provider:** Taiwan International Cooperation and Development Fund (TaiwanICDF)3
- **Category:** Foreign Government / International / Merit-based / Graduate3
- **Website:** https://www.icdf.org.tw3
- **Portal:** https://www.icdf.org.tw / TaiwanICDF Online Application System3
- **Guidelines:** TaiwanICDF International Higher Education Scholarship Program Application Guidebook4
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Citizen of an eligible partner country, including the Philippines4.
- **Residency / Destination:** Resident in the country of citizenship4.
- **Education Level:** Graduate (Master's and Doctoral degree levels)3.
- **Eligible Year Levels:** Year 1 (Incoming Graduate Students)4.
- **Incoming Freshman Only:** No4.
- **Existing College Students:** Ineligible for initial award unless applying for entry-level graduate degree studies4.
- **Graduate Students:** Yes3.
- **Current Enrollment:** Must apply for admission to a designated TaiwanICDF partner university program4.
- **Academic Requirements:** Outstanding academic record from prior post-secondary studies4.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated holistically via transcripts and university admission standards; live database parameter lists 85.00%)3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** Must be above 18 years of age4.
- **School / Consortium Restrictions:** Restricted strictly to designated TaiwanICDF partner institutions4.
- **Course Restrictions:** Agriculture, Science and Engineering, Public Health and Medicine, Business Administration7.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Good moral character required4.
- **Health:** Satisfactory physical and mental health4.
- **Other Official Rules / Conflicts:** Applicants cannot hold any other Republic of China (Taiwan) government scholarship concurrently8.

#### Timing
- **Who May Apply:** Bachelor's degree holders applying for Master's programs, and Master's degree holders applying for PhD programs at partner Taiwanese universities4.
- **Freshmen:** : No
- **Sophomores:** : No
- **Juniors:** : No
- **Seniors:** : Yes (provided they graduate prior to scholarship intake)8.
- **Graduates:** : Yes4.
- **Reapply:** : Yes4.
- **Opening:** Mid-January / February 1 annually8.
- **Closing:** March 15 / March 31 annually4.
- **Cycle:** Annual3.
- **AY Covered:** AY 2026–20274.

#### Benefits (catalog)
- **Tuition:** 100% full coverage of tuition and credit fees3.
- **Monthly Stipend:** NTD 15,000 for Master's students; NTD 17,000–18,000 for PhD students4.
- **Allowance:** Campus housing / dormitory allowance provided4.
- **Return Service:** None required by TaiwanICDF, though scholars are expected to return home to foster local development3.

#### Renewal
- **Maintain GWA:** Satisfy academic GPA retention thresholds established by the host institution4.
- **Regular Load:** Full-time credit load per semester4.
- **No Failures:** Zero failing grades in enrolled coursework4.

#### Disqualifying / Conflicts
- Holding ROC (Taiwan) citizenship or overseas Chinese student status4.
- Concurrent enjoyment of another Taiwanese government scholarship8.
- Failure to secure official admission from an approved TaiwanICDF partner university program4.

#### Required Documents (hidden operational requirements)
- Completed Online Application Form4.
- Passport Biopage / Certificate of Nationality4.
- Highest Degree Diploma and Official Academic Transcripts4.
- Proof of English Language Proficiency (TOEFL / IELTS / Official Institutional Certificate)4.
- Two Letters of Recommendation4.
- Copy of Application Submission to a TaiwanICDF Partner University4.

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": null, "income_limit": null, "rank_cutoff_alternative": null, "priority_courses": ["Agriculture", "Science and Engineering", "Public Health", "Business Administration"], "school_type": ["Foreign Partner University"], "partner_school_restricted": true, "citizenship": "Filipino", "residency_restriction": "Philippines", "application_window": {"open": "01-15", "close": "03-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "return_service_required": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Recommending program to undergraduate applicants3.
- **Verification:** Verified3. | Confidence: n/a
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated holistically via transcripts and university admission standards; live database parameter lists 85.00%)3.) differs from renewal Maintain GWA (Satisfy academic GPA retention thresholds established by the host institution4.)
  - Live DB GWA vs official NOT SPECIFIED: NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated holistically via transcripts and university admission standards; live database parameter lists 85.00%)3.

---

### Erasmus Mundus Joint Masters Scholarship3 (ID: 63)

#### Identity / Affiliations
- **Provider:** European Union / European Education and Culture Executive Agency (EACEA)3
- **Category:** Foreign Government / International / Merit-based / Graduate3
- **Website:** https://erasmus-plus.ec.europa.eu3
- **Portal:** https://www.eacea.ec.europa.eu/scholarships/erasmus-mundus-catalogue_en9
- **Guidelines:** Erasmus+ Programme Guide (Key Action 2: Erasmus Mundus Action)11
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Open to candidates worldwide, including Filipino citizens10.
- **Residency / Destination:** Worldwide residency; mandatory physical mobility across at least two different host countries11.
- **Education Level:** Graduate (Master's degree level, 60, 90, or 120 ECTS)10.
- **Eligible Year Levels:** Incoming Master's students10.
- **Incoming Freshman Only:** No10.
- **Existing College Students:** Graduating Bachelor's students eligible provided their degree is conferred prior to intake10.
- **Graduate Students:** Yes10.
- **Current Enrollment:** Must hold a recognized first higher education degree (Bachelor's degree or equivalent)10.
- **Academic Requirements:** Outstanding academic performance in prior undergraduate studies10.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Consortium-specific; live DB list is 90.00%)3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE (No upper age limit).
- **School / Consortium Restrictions:** Restricted to participating Erasmus Mundus Joint Master consortia HEIs9.
- **Course Restrictions:** Comprehensive academic fields listed in the Erasmus Mundus Catalogue9.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Health:** Health insurance covered under EU framework10.
- **Other Official Rules / Conflicts:** Mandatory physical mobility in at least two different countries11; maximum application limit of three (3) EMJM programs per application cycle9.

#### Timing
- **Who May Apply:** Bachelor's degree holders or final-year undergraduate students graduating prior to program start10.
- **Freshmen:** : No
- **Sophomores:** : No
- **Juniors:** : No
- **Seniors:** : Yes (if graduating before Master's intake)10.
- **Graduates:** : Yes10.
- **Reapply:** : Yes9.
- **Opening:** October / November annually9.
- **Closing:** January / February 12 (varies per consortium)9.
- **Cycle:** Annual3.
- **AY Covered:** AY 2026–202713.

#### Benefits (catalog)
- **Tuition:** 100% full coverage of participation costs, tuition, and enrollment fees10.
- **Monthly Stipend:** €1,400 per month living allowance (up to 24 months maximum)3.
- **Allowance:** Travel, visa, and installation contributions integrated into overall grant10.
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Satisfy academic progression standards established by consortium regulations11.
- **Regular Load:** Full credit load per semester11.
- **No Failures:** Pass all mandatory study modules11.

#### Disqualifying / Conflicts
- Failure to complete Bachelor's degree prior to Master's program commencement10.
- Applying to more than three Erasmus Mundus Joint Master programs in a single cycle9.
- Non-compliance with compulsory physical mobility track rules11.

#### Required Documents (hidden operational requirements)
- Bachelor's Diploma or Official Certificate of Expected Graduation10.
- Official Academic Transcripts of Records (TOR)10.
- Proof of English Language Proficiency (IELTS / TOEFL)9.
- Motivation Letter / Statement of Purpose9.
- Two Academic / Professional Recommendation Letters9.
- Passport / Proof of Nationality9.
- Curriculum Vitae (Europass format)9.

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": null, "income_limit": null, "rank_cutoff_alternative": null, "priority_courses": ["Erasmus Mundus Catalogue Disciplines"], "school_type": ["EUConsortium HEIs"], "partner_school_restricted": true, "citizenship": "Filipino", "residency_restriction": null, "application_window": {"open": "10-01", "close": "02-12"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "return_service_required": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Recommending scholarship to students expecting to study at a single university11.
- **Verification:** Verified3. | Confidence: 95/1003.
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Consortium-specific; live DB list is 90.00%)3.) differs from renewal Maintain GWA (Satisfy academic progression standards established by consortium regulations11.)
  - Live DB GWA vs official NOT SPECIFIED: NOT SPECIFIED IN OFFICIAL SOURCE (Consortium-specific; live DB list is 90.00%)3.

---

### Global Korea Scholarship for Graduate Degrees (GKS-G)14 (ID: 64)

#### Identity / Affiliations
- **Provider:** National Institute for International Education (NIIED) / Ministry of Education, South Korea14
- **Category:** Foreign Government / International / Merit-based / Graduate3
- **Website:** https://www.studyinkorea.go.kr3
- **Portal:** Online Application System (Embassy Track) / Direct University Submission14
- **Guidelines:** 2026 GKS-G Application Guidelines for Graduate Degrees14
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Applicant and both parents must hold citizenship of an NIIED-designated country; dual citizens holding Korean nationality are strictly barred16.
- **Residency / Destination:** Resident in home country16.
- **Education Level:** Graduate (Master's or Doctoral degree programs)3.
- **Eligible Year Levels:** Incoming Graduate Students16.
- **Incoming Freshman Only:** No16.
- **Existing College Students:** Graduating Bachelor's/Master's students eligible16.
- **Graduate Students:** Yes16.
- **Current Enrollment:** Must have graduated or be expected to graduate from a Bachelor's degree (for Master's) or Master's degree (for PhD)16.
- **Academic Requirements:** Cumulative GPA must be on a 100-point scale or ranked in the top 20% of the class; CGPA , , , or 16.
- **Minimum GWA:** Equivalent to 80% percentile cutoff16.
- **Alt Class Rank:** Top 20% of graduating class19.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** Under 40 years of age (born after September 1, 1986); under 45 years for academic professors from ODA recipient countries18.
- **School / Consortium Restrictions:** Restricted to participating NIIED-approved Korean Universities14.
- **Course Restrictions:** Fields offered by designated Korean universities14.
- **Sectoral / Hidden Requirements:** Special tracks available (e.g., Global Network, R&D)19.
- **Good Moral:** Good moral character16.
- **Health:** Physically and mentally healthy (Personal Medical Assessment required)16.
- **Other Official Rules / Conflicts:** Former GKS scholars or graduates of Korean high schools/universities are ineligible with specific exceptions19.

#### Timing
- **Who May Apply:** Bachelor's degree holders applying for Master's programs and Master's degree holders applying for Doctoral programs16.
- **Freshmen:** : No
- **Sophomores:** : No
- **Juniors:** : No
- **Seniors:** : Yes (if graduating prior to intake)18.
- **Graduates:** : Yes16.
- **Reapply:** : Subject to NIIED reapplication rules19.
- **Opening:** Mid-February annually14.
- **Closing:** March / April annually (set by individual embassies/universities)14.
- **Cycle:** Annual3.
- **AY Covered:** AY 2026–202714.

#### Benefits (catalog)
- **Tuition:** 100% full coverage of tuition fees funded by NIIED and host university3.
- **Monthly Stipend:** KRW 1,000,000 per month (Master's/PhD); KRW 1,500,000 for Research scholars.
- **Allowance:** Settlement allowance (KRW 200,000 single grant).
- **Return Service:** Expected to return or adhere to NIIED visa regulations3.

#### Renewal
- **Maintain GWA:** Maintain CGPA or equivalent per term18.
- **Regular Load:** Continuous full-time enrollment16.
- **No Failures:** Achieve passing marks in all enrolled modules16.

#### Disqualifying / Conflicts
- Holding Korean citizenship or dual citizenship with South Korea16.
- CGPA falling below 80% percentile threshold18.
- Previous receipt of a degree scholarship from the Korean government19.

#### Required Documents (hidden operational requirements)
- GKS-G Official Application Form16.
- Personal Statement and Study Plan16.
- One Recommendation Letter16.
- GKS Applicant Agreement & Personal Medical Assessment16.
- Bachelor's / Master's Diploma and Transcripts (Apostilled / Consular Authenticated)16.
- Proof of Citizenship for Applicant and Both Parents16.
- Language Proficiency Certificates (TOPIK / TOEFL / IELTS)16.

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": 80.00, "income_limit": null, "rank_cutoff_alternative": 20, "priority_courses": ["All Graduate Fields at Participating Universities"], "school_type": ["Korean HEIs"], "partner_school_restricted": true, "citizenship": "Filipino", "residency_restriction": "Philippines", "application_window": {"open": "02-15", "close": "03-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "return_service_required": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Inaccurate GPA conversion disqualifying eligible applicants19.
- **Verification:** Verified3. | Confidence: 98/1003.
- **Contradictions:**
  - Entry min_gwa (Equivalent to 80% percentile cutoff16.) differs from renewal Maintain GWA (Maintain CGPA or equivalent per term18.)

---

### Global Korea Scholarship for Undergraduate Degrees (GKS-U)20 (ID: 65)

#### Identity / Affiliations
- **Provider:** National Institute for International Education (NIIED) / Ministry of Education, South Korea20
- **Category:** Foreign Government / International / Merit-based / Undergraduate3
- **Website:** https://www.studyinkorea.go.kr3
- **Portal:** Online Application System / Embassy or University Track Submission18
- **Guidelines:** 2026 GKS-U Application Guidelines for Undergraduate Degrees20
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Non-Korean citizenship for applicant and both parents; dual citizens holding Korean nationality are barred18.
- **Residency / Destination:** Resident in home country18.
- **Education Level:** Undergraduate / College (Bachelor's or Associate degree)18.
- **Eligible Year Levels:** Year 1 (Incoming College Freshmen)18.
- **Incoming Freshman Only:** Yes18.
- **Existing College Students:** Ineligible (except Associate degree graduates applying for Bachelor's entry)18.
- **Graduate Students:** Ineligible20.
- **Current Enrollment:** High school graduate or expected to graduate Grade 12 prior to intake18.
- **Academic Requirements:** Cumulative GPA of 80% or higher on a 100-point scale or ranked in the top 20% of high school graduating class18.
- **Minimum GWA:** 80% percentile cutoff18.
- **Alt Class Rank:** Top 20% of class18.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** Under 25 years of age (born after March 1, 2001)18.
- **School / Consortium Restrictions:** Restricted to designated NIIED-approved Korean Universities (Type A and Type B)18.
- **Course Restrictions:** Four-year Bachelor's degree or Associate degree courses offered by designated universities18.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Good moral character20.
- **Health:** Mentally and physically fit (Personal Medical Assessment required)20.
- **Other Official Rules / Conflicts:** High school graduates from Korea or former Korean government degree scholarship recipients are barred19.

#### Timing
- **Who May Apply:** Senior High School Grade 12 graduating students, SHS graduates, and Associate degree graduates18.
- **Freshmen:** : Only if applying as an incoming freshman with zero
- **Sophomores:** : No
- **Juniors:** : No
- **Seniors:** : No
- **Graduates:** : High School / Associate degree graduates only18.
- **Reapply:** : Subject to NIIED reapplication rules20.
- **Opening:** September annually17.
- **Closing:** October / November annually (set by Embassy / University 1st round)17.
- **Cycle:** Annual3.
- **AY Covered:** AY 2026–202720.

#### Benefits (catalog)
- **Tuition:** 100% full tuition coverage3.
- **Monthly Stipend:** KRW 900,000 per month.
- **Allowance:** Settlement allowance (KRW 200,000 single grant).
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Maintain CGPA per semester18.
- **Regular Load:** Full credit enrollment20.
- **No Failures:** Zero failing marks20.

#### Disqualifying / Conflicts
- Age exceeding 25 years at application deadline18.
- Holding Korean citizenship or dual nationality18.
- Earning tertiary units in a 4-year degree program prior to application20.

#### Required Documents (hidden operational requirements)
- GKS-U Application Form20.
- Personal Statement and Study Plan20.
- One Recommendation Letter20.
- High School Graduation Certificate / Associate Degree Diploma (Apostilled)18.
- Official High School / Associate Academic Transcripts18.
- Proof of Citizenship for Applicant and Both Parents18.
- Personal Medical Assessment20.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": 80.00, "income_limit": null, "rank_cutoff_alternative": 20, "age_limit": 25, "priority_courses": ["Four-year Undergraduate Degrees"], "school_type": ["Korean HEIs"], "partner_school_restricted": true, "citizenship": "Filipino", "residency_restriction": "Philippines", "application_window": {"open": "09-01", "close": "10-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "return_service_required": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Showing scholarship to applicants over 25 years of age18.
- **Verification:** Verified3. | Confidence: 98/1003.
- **Contradictions:**
  - Entry min_gwa (80% percentile cutoff18.) differs from renewal Maintain GWA (Maintain CGPA per semester18.)

---

### Australia Awards Scholarships (Philippines)3 (ID: 74)

#### Identity / Affiliations
- **Provider:** Australian Government (Department of Foreign Affairs and Trade - DFAT)3
- **Category:** Foreign Government / International / Merit-based / Graduate3
- **Website:** https://www.australiaawardsphilippines.org3
- **Portal:** OASIS / Australia Awards Philippines Portal24
- **Guidelines:** Australia Awards Scholarships Policy Handbook & Philippines Information Sheet24
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen24.
- **Residency / Destination:** Resided in the Philippines for at least 12 months prior to application deadline24.
- **Education Level:** Graduate (Master's Degree level)3.
- **Eligible Year Levels:** Incoming Master's Students24.
- **Incoming Freshman Only:** No24.
- **Existing College Students:** Ineligible24.
- **Graduate Students:** Yes24.
- **Current Enrollment:** Must have completed a formal undergraduate degree24.
- **Academic Requirements:** Academic competence evaluated holistically from undergraduate transcripts24.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated holistically; live DB parameter lists NULL)3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE (Must meet adult visa eligibility).
- **School / Consortium Restrictions:** Eligible Australian Universities24.
- **Course Restrictions:** Agriculture, Marine, and Natural Resource Management; Climate Change; Cybersecurity & Critical Technology; Education; International Relations & National Security24.
- **Sectoral / Hidden Requirements:** Open Category (all qualified individuals) and Targeted Category (nominated by 11 Philippine Government agencies)24.
- **Work Experience:** Minimum two (2) years cumulative work experience upon application24.
- **Good Moral:** Good moral character24.
- **Health:** Must satisfy Australian student visa health requirements24.
- **Other Official Rules / Conflicts:** Must commit to returning to the Philippines to implement a Re-entry Action Plan (REAP)24; cannot hold another active scholarship24.

#### Timing
- **Who May Apply:** Filipino professionals holding a Bachelor's degree with at least 2 years work experience24.
- **Freshmen:** : No
- **Sophomores:** : No
- **Juniors:** : No
- **Seniors:** : No
- **Graduates:** : Yes (Bachelor's graduates)24.
- **Reapply:** : Yes (provided they have not held a long-term Australia
- **Opening:** February 1 annually24.
- **Closing:** April 30 annually24.
- **Cycle:** Annual3.
- **AY Covered:** AY 2026–2027 / Commencement 202724.

#### Benefits (catalog)
- **Tuition:** 100% full tuition fee coverage3.
- **Monthly Stipend:** Contribution to Living Expenses (CLE) paid fortnightly/monthly24.
- **Allowance:** One-off establishment allowance on arrival24.
- **Return Service:** Mandatory Return Service in the Philippines to execute Re-entry Action Plan (REAP)3.

#### Renewal
- **Maintain GWA:** Maintain satisfactory academic progress per university rules24.
- **Regular Load:** Continuous full-time course enrollment28.
- **No Failures:** Zero failed academic units24.

#### Disqualifying / Conflicts
- Holding dual Australian citizenship or permanent residency24.
- Having less than two years cumulative work experience24.
- Failure to submit an approved Re-entry Action Plan24.

#### Required Documents (hidden operational requirements)
- Re-entry Action Plan (REAP) Proposal24.
- Proof of Citizenship (Passport or Birth Certificate)24.
- Proof of Residency (Government ID, lease contract, or utility bill)24.
- Official Academic Transcripts and Diplomas24.
- Curriculum Vitae documenting years work experience24.
- Referee Reports (Academic and Work Supervisor)24.
- English Language Test Results (IELTS / TOEFL / PTE)25.

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": null, "income_limit": null, "work_experience_years": 2, "priority_courses": ["Agriculture", "Climate Change", "Cybersecurity", "Education", "National Security"], "school_type": ["Australian HEIs"], "partner_school_restricted": true, "citizenship": "Filipino", "residency_restriction": "Philippines (>= 12 months)", "application_window": {"open": "02-01", "close": "04-30"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "return_service_required": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Recommending program to fresh graduates without required work experience24.
- **Verification:** Verified3. | Confidence: 98/1003.
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated holistically; live DB parameter lists NULL)3.) differs from renewal Maintain GWA (Maintain satisfactory academic progress per university rules24.)
  - Live DB GWA vs official NOT SPECIFIED: NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated holistically; live DB parameter lists NULL)3.

---

### Japanese Government (MEXT) Scholarship – Research Student Category29 (ID: 80)

#### Identity / Affiliations
- **Provider:** Ministry of Education, Culture, Sports, Science and Technology (MEXT), Japan / Embassy of Japan in the Philippines29
- **Category:** Foreign Government / International / Merit-based / Graduate3
- **Website:** https://www.ph.emb-japan.go.jp/itpr_en/00_000193.html3
- **Portal:** Submission to Embassy of Japan in Manila / JICC29
- **Guidelines:** MEXT Application Guidelines for Research Students29
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen (processed by Embassy of Japan in Manila)29.
- **Residency / Destination:** Resident in the Philippines29.
- **Education Level:** Graduate (Master's / PhD / Non-degree Research Student)3.
- **Eligible Year Levels:** Incoming Research/Graduate Students29.
- **Incoming Freshman Only:** No29.
- **Existing College Students:** Graduating university seniors eligible29.
- **Graduate Students:** Yes29.
- **Current Enrollment:** Must have completed 16 years of school education or hold a Bachelor's degree29.
- **Academic Requirements:** High academic performance in university studies29.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via academic transcript and written exam)3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** Born on or after April 2, 1992 (Under 35 years old)29.
- **School / Consortium Restrictions:** Japanese national, public, or private universities29.
- **Course Restrictions:** Fields matching university major or related academic fields29.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Good moral standing.
- **Health:** Physically and mentally fit (Medical Certificate required)29.
- **Other Official Rules / Conflicts:** Willingness to learn Japanese; military personnel barred29.

#### Timing
- **Who May Apply:** Bachelor's degree holders or graduating college seniors29.
- **Freshmen:** : No
- **Sophomores:** : No
- **Juniors:** : No
- **Seniors:** : Yes (if graduating before departure to Japan)29.
- **Graduates:** : Yes29.
- **Reapply:** : Yes29.
- **Opening:** Mid-April / May annually29.
- **Closing:** Late May / June annually29.
- **Cycle:** Annual3.
- **AY Covered:** AY 2026–2027 / Departure April/October 202729.

#### Benefits (catalog)
- **Tuition:** 100% full coverage of tuition, entrance, and examination fees3.
- **Monthly Stipend:** JPY 143,000–145,000 per month (varies for Research/Master's/PhD).
- **Allowance:** Regional stipend allowance top-up.
- **Return Service:** Expected to return; mandatory return service for Philippine public servants3.

#### Renewal
- **Maintain GWA:** Satisfy graduate school retention and academic standards29.
- **Regular Load:** Full credit load29.
- **No Failures:** Zero failed research modules29.

#### Disqualifying / Conflicts
- Born before April 2, 199229.
- Holding Japanese nationality29.
- Failure to pass MEXT written examination and embassy interview29.

#### Required Documents (hidden operational requirements)
- Application Form & Placement Preference Form29.
- Field of Study and Research Plan29.
- Official Transcript of Records (TOR)29.
- Graduation Certificate / Degree Diploma29.
- Recommendation Letter from Dean/President or Advisor29.
- Certificate of Health29.
- Thesis Abstract / Research Papers (if applicable)29.

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": null, "income_limit": null, "age_limit": 34, "priority_courses": ["All Fields Offered at Japanese Universities"], "school_type": ["Japanese Universities"], "partner_school_restricted": false, "citizenship": "Filipino", "residency_restriction": "Philippines", "application_window": {"open": "04-15", "close": "05-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "return_service_required": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Recommending program to applicants exceeding age limit29.
- **Verification:** Verified3. | Confidence: 98/1003.
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via academic transcript and written exam)3.) differs from renewal Maintain GWA (Satisfy graduate school retention and academic standards29.)

---

### Japanese Government (MEXT) Scholarship – Undergraduate Student Category29 (ID: 81)

#### Identity / Affiliations
- **Provider:** Ministry of Education, Culture, Sports, Science and Technology (MEXT), Japan / Embassy of Japan in the Philippines29
- **Category:** Foreign Government / International / Merit-based / Undergraduate3
- **Website:** https://www.ph.emb-japan.go.jp/itpr_en/00_000193.html3
- **Portal:** Submission to Embassy of Japan in Manila / JICC29
- **Guidelines:** MEXT Application Guidelines for Undergraduate Students29
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen29.
- **Residency / Destination:** Resident in the Philippines29.
- **Education Level:** Undergraduate / College (Bachelor's Degree)3.
- **Eligible Year Levels:** Year 1 (Incoming Freshmen)29.
- **Incoming Freshman Only:** Yes29.
- **Existing College Students:** Eligible if within age limit, but award starts at 1st year29.
- **Graduate Students:** Ineligible29.
- **Current Enrollment:** Completed 12 years of school education or graduating Grade 12 by March preceding intake29.
- **Academic Requirements:** High school academic excellence29.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via written examinations in Mathematics, English, Japanese, and Science)3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** Born on or after April 2, 2002 (17 to 24 years old)29.
- **School / Consortium Restrictions:** Designated Japanese Universities29.
- **Course Restrictions:** Social Sciences & Humanities (Law, Politics, Economics, Literature) and Natural Sciences (Science, Engineering, Agriculture, Medicine)29.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Good moral character.
- **Health:** Mentally and physically fit29.
- **Other Official Rules / Conflicts:** Mandatory 1-year preparatory Japanese language education in Japan29.

#### Timing
- **Who May Apply:** Senior High School Grade 12 graduating students or SHS graduates29.
- **Freshmen:** : Yes (if within age limit, but must restart as 1st year)29.
- **Sophomores:** : Only if age-eligible.
- **Juniors:** : No
- **Seniors:** : No
- **Graduates:** : Only SHS / High School graduates29.
- **Reapply:** : Yes29.
- **Opening:** Mid-April / May annually29.
- **Closing:** Late May / June annually29.
- **Cycle:** Annual3.
- **AY Covered:** AY 2026–2027 / Departure April 202729.

#### Benefits (catalog)
- **Tuition:** 100% full coverage of tuition and entrance examination fees3.
- **Monthly Stipend:** JPY 117,000 per month.
- **Allowance:** Preparatory training allowance.
- **Return Service:** Expected return service3.

#### Renewal
- **Maintain GWA:** Pass university academic performance standards per term29.
- **Regular Load:** Full credit load per term29.
- **No Failures:** Zero failing marks29.

#### Disqualifying / Conflicts
- Born before April 2, 200229.
- Holding Japanese nationality29.
- Failure to pass MEXT written examinations in STEM/Humanities subjects29.

#### Required Documents (hidden operational requirements)
- Application Form & Placement Preference Form29.
- SHS Form 138 / SF9 / High School Transcripts29.
- High School Diploma / Graduation Certificate29.
- Recommendation Letter from High School Principal/Teacher29.
- Certificate of Health29.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": null, "income_limit": null, "age_limit": 24, "priority_courses": ["Social Sciences", "Humanities", "Natural Sciences", "Medicine"], "school_type": ["Japanese Universities"], "partner_school_restricted": false, "citizenship": "Filipino", "residency_restriction": "Philippines", "application_window": {"open": "04-15", "close": "05-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "return_service_required": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Recommending scholarship to upperclassmen who do not wish to restart as 1st
- **Verification:** Verified3. | Confidence: 98/1003.
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via written examinations in Mathematics, English, Japanese, and Science)3.) differs from renewal Maintain GWA (Pass university academic performance standards per term29.)

---

### Japanese Government (MEXT) Scholarship – Specialized Training College Student Category29 (ID: 82)

#### Identity / Affiliations
- **Provider:** Ministry of Education, Culture, Sports, Science and Technology (MEXT), Japan / Embassy of Japan in the Philippines29
- **Category:** Foreign Government / International / Vocational / Merit-based3
- **Website:** https://www.ph.emb-japan.go.jp/itpr_en/00_000193.html3
- **Portal:** Submission to Embassy of Japan in Manila / JICC29
- **Guidelines:** MEXT Application Guidelines for Specialized Training College Students29
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen29.
- **Residency / Destination:** Resident in the Philippines29.
- **Education Level:** Technical-Vocational / TVET3.
- **Eligible Year Levels:** Entry-level vocational diploma track29.
- **Incoming Freshman Only:** Yes29.
- **Existing College Students:** Eligible if within age limit29.
- **Graduate Students:** Ineligible29.
- **Current Enrollment:** High school graduate or expected to graduate Grade 12 by March preceding arrival29.
- **Academic Requirements:** Strong high school academic record29.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via written examinations in English, Mathematics, and Japanese)3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** Born on or after April 2, 2002 (17 to 24 years old)29.
- **School / Consortium Restrictions:** Japanese Specialized Training Colleges (Senshu-Gakko)29.
- **Course Restrictions:** Technology, Personal Care/Nutrition, Education/Welfare, Business, Fashion/Home Economics, Culture/General Education29.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Good moral character.
- **Health:** Mentally and physically fit29.
- **Other Official Rules / Conflicts:** 1-year Japanese language preparatory course included prior to 2-year vocational studies29.

#### Timing
- **Who May Apply:** Senior High School Grade 12 graduating students or SHS graduates29.
- **Freshmen:** : Yes (if age-eligible)29.
- **Sophomores:** : Only if age-eligible.
- **Juniors:** : No
- **Seniors:** : No
- **Graduates:** : High School / SHS graduates only29.
- **Reapply:** : Yes29.
- **Opening:** Mid-April / May annually29.
- **Closing:** Late May / June annually29.
- **Cycle:** Annual3.
- **AY Covered:** AY 2026–2027 / Departure April 202729.

#### Benefits (catalog)
- **Tuition:** 100% full coverage of tuition and vocational education fees3.
- **Monthly Stipend:** JPY 117,000 per month.
- **Allowance:** Preparatory training allowance.
- **Return Service:** Expected return service3.

#### Renewal
- **Maintain GWA:** Satisfy specialized college retention standards29.
- **Regular Load:** Full credit load per term29.
- **No Failures:** Zero failing marks29.

#### Disqualifying / Conflicts
- Born before April 2, 200229.
- Holding Japanese nationality29.
- Failure to pass written examinations in English, Mathematics, and Japanese29.

#### Required Documents (hidden operational requirements)
- Application Form29.
- SHS Form 138 / High School Academic Transcripts29.
- High School Diploma / Graduation Certificate29.
- Recommendation Letter29.
- Medical Certificate29.

#### Recommended Schema / Fields
```json
{ "education_level": ["TVET"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": null, "income_limit": null, "age_limit": 24, "priority_courses": ["Technology", "Nutrition", "Business", "Fashion", "Culture"], "school_type": ["Japanese Specialized Training Colleges"], "partner_school_restricted": false, "citizenship": "Filipino", "residency_restriction": "Philippines", "application_window": {"open": "04-15", "close": "05-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "return_service_required": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Misclassifying vocational track as a 4-year Bachelor's degree29.
- **Verification:** Verified3. | Confidence: 98/1003.
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via written examinations in English, Mathematics, and Japanese)3.) differs from renewal Maintain GWA (Satisfy specialized college retention standards29.)

---

### Japanese Government (MEXT) Scholarship – College of Technology Student Category (KOSEN)29 (ID: 83)

#### Identity / Affiliations
- **Provider:** Ministry of Education, Culture, Sports, Science and Technology (MEXT), Japan / Embassy of Japan in the Philippines29
- **Category:** Foreign Government / International / Engineering-TVET / Merit-based3
- **Website:** https://www.ph.emb-japan.go.jp/itpr_en/00_000193.html3
- **Portal:** Submission to Embassy of Japan in Manila / JICC29
- **Guidelines:** MEXT Application Guidelines for College of Technology Students29
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen29.
- **Residency / Destination:** Resident in the Philippines29.
- **Education Level:** College / TVET (KOSEN Associate Degree / Practical Engineering)3.
- **Eligible Year Levels:** Entry into 3rd year of KOSEN system following 1 year of preparatory training29.
- **Incoming Freshman Only:** Yes29.
- **Existing College Students:** Eligible if within age threshold29.
- **Graduate Students:** Ineligible29.
- **Current Enrollment:** High school graduate or expected to graduate Grade 12 by March preceding arrival29.
- **Academic Requirements:** High academic performance in STEM / Mathematics and Physics29.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via written examinations in Mathematics, Physics, Chemistry, English, and Japanese)3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** Born on or after April 2, 2002 (17 to 24 years old)29.
- **School / Consortium Restrictions:** National Colleges of Technology (KOSEN) in Japan29.
- **Course Restrictions:** Mechanical Engineering, Electrical & Electronic Engineering, Information Technology, Chemical Engineering, Civil Engineering, Architecture, Materials Engineering29.
- **Sectoral / Hidden Requirements:** STEM focus29.
- **Good Moral:** Good moral character.
- **Health:** Mentally and physically fit29.
- **Other Official Rules / Conflicts:** Includes 1-year preparatory Japanese language and STEM education29.

#### Timing
- **Who May Apply:** Senior High School STEM graduating students or SHS graduates29.
- **Freshmen:** : Yes (if age-eligible)29.
- **Sophomores:** : Only if age-eligible.
- **Juniors:** : No
- **Seniors:** : No
- **Graduates:** : High School / SHS graduates only29.
- **Reapply:** : Yes29.
- **Opening:** Mid-April / May annually29.
- **Closing:** Late May / June annually29.
- **Cycle:** Annual3.
- **AY Covered:** AY 2026–2027 / Departure April 202729.

#### Benefits (catalog)
- **Tuition:** 100% full coverage of tuition, entrance, and laboratory fees3.
- **Monthly Stipend:** JPY 117,000 per month.
- **Allowance:** Preparatory training allowance.
- **Return Service:** Expected return service3.

#### Renewal
- **Maintain GWA:** Satisfy KOSEN engineering academic standards29.
- **Regular Load:** Full credit load per term29.
- **No Failures:** Zero failing marks29.

#### Disqualifying / Conflicts
- Born before April 2, 200229.
- Holding Japanese nationality29.
- Failure to pass written examinations in Mathematics, Physics, Chemistry, English, and Japanese29.

#### Required Documents (hidden operational requirements)
- Application Form29.
- SHS Form 138 / High School Transcripts29.
- High School Diploma / Graduation Certificate29.
- Recommendation Letter from Principal/STEM Teacher29.
- Certificate of Health29.

#### Recommended Schema / Fields
```json
{ "education_level": ["College", "TVET"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": null, "income_limit": null, "age_limit": 24, "priority_courses": ["Mechanical", "Electrical", "Information Technology", "Chemical", "Civil", "Architecture"], "school_type": ["Japanese KOSENColleges"], "partner_school_restricted": false, "citizenship": "Filipino", "residency_restriction": "Philippines", "application_window": {"open": "04-15", "close": "05-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "return_service_required": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Non-STEM students applying without necessary Physics/Chemistry background29.
- **Verification:** Verified3. | Confidence: 98/1003.
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via written examinations in Mathematics, Physics, Chemistry, English, and Japanese)3.) differs from renewal Maintain GWA (Satisfy KOSEN engineering academic standards29.)

---

### Fulbright-Philippine Space Agency (PhilSA) Foreign Student Program in Space Science and Technology Applications (SSTA)30 (ID: 90)

#### Identity / Affiliations
- **Provider:** Philippine-American Educational Foundation (PAEF / Fulbright Commission) & Philippine Space Agency (PhilSA)30
- **Category:** Foreign Government / Joint Agency / Merit-based / Graduate3
- **Website:** https://www.fulbright.org.ph / https://philsa.gov.ph3
- **Portal:** https://apply.iie.org/ffsp20273
- **Guidelines:** Fulbright-PhilSA Foreign Student Program Call for Applications30
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen residing in the Philippines at application and selection time; dual citizens or US permanent residents are barred30.
- **Residency / Destination:** Resident in the Philippines30.
- **Education Level:** Graduate (Master's or Doctoral studies)3.
- **Eligible Year Levels:** Year 1 (Incoming Graduate Students)30.
- **Incoming Freshman Only:** No30.
- **Existing College Students:** Ineligible30.
- **Graduate Students:** Yes30.
- **Current Enrollment:** Completed Bachelor's degree with major in field of specialization and an excellent academic record31.
- **Academic Requirements:** Excellent undergraduate academic record31.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via transcript and research objective statement)3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Accredited Higher Education Institutions in the United States30.
- **Course Restrictions:** Space Applications (Earth observation, meteorology, PNT, telecom), Spacecraft Systems (satellites, rocketry, robotics, cybersecurity), Space Science (astronomy, space biology/medicine), Space Law, Economics, and Administration30.
- **Sectoral / Hidden Requirements:** Space Science and Technology Applications (SSTA) and allied sectors31.
- **Work Experience:** Minimum two (2) years of professional work experience after college graduation30.
- **Good Moral:** No pending administrative or criminal charges; no conviction30.
- **Health:** Physically and mentally fit to pursue graduate studies in the US30.
- **Other Official Rules / Conflicts:** Must commit to returning to the Philippines immediately upon program completion to fulfill return service30; no dependent support provided31.

#### Timing
- **Who May Apply:** Bachelor's degree holders with at least 2 years post-college professional work experience in space-related disciplines30.
- **Freshmen:** : No
- **Sophomores:** : No
- **Juniors:** : No
- **Seniors:** : No
- **Graduates:** : Yes (Bachelor's or Master's degree graduates)30.
- **Reapply:** : Yes (if not received a Fulbright grant within the past 5
- **Opening:** January 20 annually31.
- **Closing:** April 18 / April 30 / June 19 (depending on AY cycle announcement)30.
- **Cycle:** Annual3.
- **AY Covered:** AY 2026–2027 / AY 2027–202830.

#### Benefits (catalog)
- **Tuition:** 100% full coverage of tuition and university fees3.
- **Monthly Stipend:** Monthly maintenance allowance30.
- **Allowance:** Settling-in allowance, in-transit allowance, allowable excess baggage grant31.
- **Return Service:** Mandatory Return Service obligation in the Philippines immediately upon program completion3.

#### Renewal
- **Maintain GWA:** Satisfy academic GPA retention policies of host US university30.
- **Regular Load:** Full credit load30.
- **No Failures:** Zero failed academic units30.

#### Disqualifying / Conflicts
- Holding dual US citizenship or permanent resident status30.
- Having less than two years post-college professional work experience30.
- Presently living, studying, or working in the United States30.

#### Required Documents (hidden operational requirements)
- Completed Online Application via IIE Portal30.
- Research Objective Statement (3 to 5 pages)30.
- Personal Statement (maximum 3 pages)30.
- Updated Curriculum Vitae / Resume (maximum 6 pages)30.
- Official Transcripts of Records and Diplomas30.
- Three Letters of Recommendation30.
- Passport Biopage Copy30.
- NBI Clearance (secured within 6 months)30.
- Writing Samples (maximum 20 pages) & Bibliography30.

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": null, "income_limit": null, "work_experience_years": 2, "priority_courses": ["Space Applications", "Spacecraft Systems", "Space Science", "Space Law"], "school_type": ["USHigher Education Institutions"], "partner_school_restricted": false, "citizenship": "Filipino", "residency_restriction": "Philippines", "application_window": {"open": "01-20", "close": "06-19"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "return_service_required": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Recommending grant to applicants counting college assistantships as work
- **Verification:** Verified3. | Confidence: 98/1003.
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated via transcript and research objective statement)3.) differs from renewal Maintain GWA (Satisfy academic GPA retention policies of host US university30.)

---

### Chevening Scholarship3 (ID: 91)

#### Identity / Affiliations
- **Provider:** Foreign, Commonwealth & Development Office (FCDO) / UK Government3
- **Category:** Foreign Government / International / Merit-based / Graduate3
- **Website:** https://www.chevening.org/apply3
- **Portal:** Chevening Online Application System34
- **Guidelines:** Chevening Scholarship Terms and Conditions36
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen (or citizen of a Chevening-eligible territory)34.
- **Residency / Destination:** Resident in the Philippines or an eligible Chevening territory34.
- **Education Level:** Graduate (One-year taught Master's degree)3.
- **Eligible Year Levels:** Incoming Master's Students36.
- **Incoming Freshman Only:** No37.
- **Existing College Students:** Ineligible37.
- **Graduate Students:** Yes36.
- **Current Enrollment:** Must have completed an undergraduate degree enabling entry into a UK postgraduate program10.
- **Academic Requirements:** Meets UK university Master's entry requirements37.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Must obtain an unconditional offer from a UK university; live database parameter lists NULL)3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE (No upper age limit).
- **School / Consortium Restrictions:** Any recognized UK Higher Education Institution36.
- **Course Restrictions:** Any eligible one-year taught Master's degree program in the UK (MBA fee contribution capped at £22,000)36.
- **Sectoral / Hidden Requirements:** High leadership potential / emerging leaders37.
- **Work Experience:** Minimum two (2) years of work experience (equivalent to 2,800 hours)24.
- **Good Moral:** Good moral character; compliance with Chevening Code of Conduct37.
- **Health:** Must receive medical clearance and UK visa entry clearance37.
- **Other Official Rules / Conflicts:** Must return to home country for at least two (2) years after scholarship completion36; no financial or visa support provided for dependants37.

#### Timing
- **Who May Apply:** Bachelor's degree holders with at least 2 years work experience37.
- **Freshmen:** : No
- **Sophomores:** : No
- **Juniors:** : No
- **Seniors:** : No
- **Graduates:** : Yes (Bachelor's degree graduates)37.
- **Reapply:** : Yes (if not previously funded by a UK government
- **Opening:** August / September annually3.
- **Closing:** November / October 7 annually (e.g., October 7, 2026 in DB)3.
- **Cycle:** Annual3.
- **AY Covered:** AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** 100% full tuition fee coverage (MBA fee contribution capped at £22,000)3.
- **Monthly Stipend:** Personal living allowance (stipend rate varies for London vs Non-London institutions)36.
- **Allowance:** Arrival allowance, departure allowance, travel top-up allowance for London events36.
- **Return Service:** Mandatory 2-year return to home country following completion of award3.

#### Renewal
- **Maintain GWA:** Satisfy academic progression rules of host UK university37.
- **Regular Load:** Continuous full-time enrollment37.
- **No Failures:** Complete all Master's course modules37.

#### Disqualifying / Conflicts
- Holding British or dual British citizenship37.
- Having less than two years (2,800 hours) work experience24.
- Previous receipt of a UK government-funded scholarship36.

#### Required Documents (hidden operational requirements)
- Completed Online Application Form via Chevening portal34.
- Official Undergraduate Transcripts and Degree Certificate37.
- Selection of Three Eligible Taught UK Master's Courses36.
- Two Reference Letters37.
- Valid Passport / Proof of Citizenship37.
- Evidence of 2 Years Work Experience (2,800 hours)24.
- Unconditional Offer Letter from at least one UK course choice (by July deadline)36.

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": null, "income_limit": null, "work_experience_years": 2, "priority_courses": ["One-year Taught Master's Degrees"], "school_type": ["UKHigher Education Institutions"], "partner_school_restricted": false, "citizenship": "Filipino", "residency_restriction": "Philippines", "application_window": {"open": "08-01", "close": "11-07"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": false, "first_time_only": true, "return_service_required": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Recommending grant for 2-year research Master's programs36.
- **Verification:** Verified3. | Confidence: 98/1003.
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Must obtain an unconditional offer from a UK university; live database parameter lists NULL)3.) differs from renewal Maintain GWA (Satisfy academic progression rules of host UK university37.)
  - Live DB GWA vs official NOT SPECIFIED: NOT SPECIFIED IN OFFICIAL SOURCE (Must obtain an unconditional offer from a UK university; live database parameter lists NULL)3.

---

## SOURCE: `DATABASE_V3_GROUPC_LGU_PART1.pdf`

**Scholarships in this PDF:** 18

### Taguig City Lifeline Assistance for Neighbors In-Need (L.A.N.I.) Premier Scholarship1 (ID: 27)

#### Identity / Affiliations
- **Provider:** Taguig City Government / Taguig Scholarship Secretariat1
- **Category:** Local Government Unit (LGU) / Merit-based1
- **Website:** https://www.taguig.gov.ph1
- **Portal:** https://tcu.edu.ph/lani-scholarship1
- **Guidelines:** Taguig City Ordinance No. 9, Series of 2011; Executive Order No. 2011-111
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen1
- **Residency / Destination:** Bona fide resident of Taguig City for at least three (3) years immediately preceding the application1.
- **Education Level:** College / Undergraduate1.
- **Eligible Year Levels:** 1, 2, 3, 4, 51.
- **Incoming Freshman Only:** No1.
- **Existing College Students:** Yes1.
- **Graduate Students:** No (Covered under LEAD track ID 97)1.
- **Current Enrollment:** Enrolled or enrolling in the UP System (Luzon campuses) or CHED-certified Centers of Excellence in NCR1.
- **Academic Requirements:** Senior High School or college academic performance meeting admission and retention cutoffs1.
- **Minimum GWA:** 90% (or equivalent 1.75 semestral weighted average)1.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Restricted to University of the Philippines System (Luzon campuses) and CHED-certified Centers of Excellence in NCR1.
- **Course Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Required (Certificate of Good Moral Character issued for the current school year)1.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Must be a registered voter of Taguig City if 18 years or older, with at least one parent registered as a voter of Taguig City1.

#### Timing
- **Who May Apply:** Graduating SHS students and ongoing college students enrolled in qualifying COE institutions or UP Luzon campuses1.
- **Freshmen:** : Yes1.
- **Sophomores:** : Yes1.
- **Juniors:** : Yes1.
- **Seniors:** : Yes1.
- **Graduates:** : No1.
- **Reapply:** : Yes (Requires semestral renewal)1.
- **Opening:** Semestral schedule announced by the Taguig Scholarship Secretariat1.
- **Closing:** Announced per semestral intake window1.
- **Cycle:** Semestral3.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Integrated into financial grant1.
- **Monthly Stipend:** Integrated into semestral allowance1.
- **Allowance:** PHP 40,000.00 to PHP 50,000.00 per school year (PHP 20,000.00 to PHP 25,000.00 per semester)1.
- **Return Service:** None mandated; scholars are encouraged to serve Taguig City1.

#### Renewal
- **Maintain GWA:** Must maintain a General Weighted Average (GWA) not lower than 2.50 per semester5.
- **Regular Load:** Enrolled in at least 15 academic units per semester or equivalent per trimester5.
- **No Failures:** Zero failing grades (5.0), unremoved 4.0, Incomplete (INC), or Dropped marks5.

#### Disqualifying / Conflicts
- Residing in Taguig City for less than three (3) consecutive years1.
- Non-voter status of applicant (if 18+) or parent in Taguig City1.
- Semester GWA dropping below 2.50 or receiving grades of 5.0, 4.0, INC, or Dropped5.
- Enrollment in non-COE institutions or non-UP Luzon campuses1.

#### Required Documents (hidden operational requirements)
- Completely filled-out LANI Scholarship Application Form with recent 2x2 pictures1.
- Registration Form or Official Receipt of Enrollment for the current semester1.
- Authenticated Copy of Grades/Transcript of Records for the preceding semester1.
- Certificate of Good Moral Character issued for the current academic year1.
- Voter's Certification issued by COMELEC (for applicant if >=18 years old, and parent)1.
- Certificate of Residency (minimum 3 years)1.
- Proof of Billing under the applicant's or parent's name1.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 90.00, "renewal_gwa": 81.00, "income_limit": null, "school_type": ["UP_SYSTEM_LUZON", "CHED_CENTER_OF_EXCELLENCE_NCR"], "partner_school_restricted": true, "citizenship": "Filipino", "residency_restriction": "TAGUIG_CITY_3_YEARS", "voter_requirement": "TAGUIG_REGISTERED_VOTER", "application_window": {"open": "semestral_notice", "close": "semestral_notice"}, "deadline_type": "semestral", "cycle_type": "semester", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● COE Validation Risk: Automated matching engines may grant recommendations to
- **Verification:** Verified1. | Confidence: n/a
- **Contradictions:**
  - Entry min_gwa (90% (or equivalent 1.75 semestral weighted average)1.) differs from renewal Maintain GWA (Must maintain a General Weighted Average (GWA) not lower than 2.50 per semester5.)

---

### Taguig City L.A.N.I. Priority Courses and Skills Training Scholarship1 (ID: 28)

#### Identity / Affiliations
- **Provider:** Taguig City Government / Taguig Scholarship Secretariat1
- **Category:** Local Government Unit (LGU) / Merit-and-Need1
- **Website:** https://www.taguig.gov.ph1
- **Portal:** https://tcu.edu.ph/lani-scholarship1
- **Guidelines:** Taguig City Ordinance No. 9, Series of 2011; Executive Order No. 2011-111
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen1
- **Residency / Destination:** Bona fide resident of Taguig City for at least three (3) years immediately preceding the application1.
- **Education Level:** College / Undergraduate / Professional (Law & Medicine)1.
- **Eligible Year Levels:** 1, 2, 3, 4, 51.
- **Incoming Freshman Only:** No1.
- **Existing College Students:** Yes1.
- **Graduate Students:** No (Except Law and Medicine)1.
- **Current Enrollment:** Must be enrolled in DOST-listed priority courses in DOST-listed schools, top-performing Law/Medicine schools as listed by PRC/CHED, or PWD applicants endorsed by PDAO1.
- **Academic Requirements:** GWA of at least 82% or equivalent1.
- **Minimum GWA:** 82.00%1.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Restricted to DOST-listed institutions, top PRC/CHED performing law/medical schools, or PDAO-accredited institutions1.
- **Course Restrictions:** DOST S&T Priority Courses, Law (Juris Doctor), Medicine (Doctor of Medicine)1.
- **Sectoral / Hidden Requirements:** PWD applicants must submit an official ID/endorsement from the Taguig Persons with Disabilities Affairs Office (PDAO)1.
- **Good Moral:** Required1.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Applicant and/or parent must be registered voters of Taguig City1.

#### Timing
- **Who May Apply:** High school graduates and current tertiary/professional students meeting course and institutional criteria1.
- **Freshmen:** : Yes1.
- **Sophomores:** : Yes1.
- **Juniors:** : Yes1.
- **Seniors:** : Yes1.
- **Graduates:** : No (Unless entering Law/Medicine)1.
- **Reapply:** : Yes1.
- **Opening:** Semestral schedule published by Taguig Secretariat1.
- **Closing:** Semestral deadline1.
- **Cycle:** Semestral3.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Direct grant allocation1.
- **Monthly Stipend:** Integrated into allowance1.
- **Allowance:** PHP 40,000.00 to PHP 50,000.00 per school year (PHP 20,000.00 to PHP 25,000.00 per semester)1.
- **Return Service:** None1.

#### Renewal
- **Maintain GWA:** Semestral GWA >= 2.50 (81%)5.
- **Regular Load:** Minimum 15 credit units per semester5.
- **No Failures:** Zero failing or incomplete grades5.

#### Disqualifying / Conflicts
- Enrolling in non-priority courses outside DOST/Law/Medicine frameworks1.
- Failure to present valid Taguig PDAO endorsement for PWD track1.
- Accumulation of failing, incomplete, or dropped subjects5.

#### Required Documents (hidden operational requirements)
- Filled LANI Application Form1.
- Enrollment Certificate / Registration Form1.
- Preceding Term Grade Report / Transcript of Records1.
- Taguig PDAO ID and Endorsement (for PWD applicants)1.
- COMELEC Voter's Certification of applicant/parent1.
- Certificate of Good Moral Character1.

#### Recommended Schema / Fields
```json
{ "education_level": ["College", "Graduate"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 82.00, "income_limit": null, "priority_courses": ["DOST_ST_PRIORITY", "LAW_JURIS_DOCTOR", "DOCTOR_OF_MEDICINE"], "sectoral_restriction": "PWD_TAGUIG_PDAO_ENDORSED", "partner_school_restricted": true, "citizenship": "Filipino", "residency_restriction": "TAGUIG_CITY_3_YEARS", "application_window": {"open": "semestral_notice", "close": "semestral_notice"}, "deadline_type": "semestral", "cycle_type": "semester", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Course Misclassification: System must strictly validate course codes against DOST
- **Verification:** n/a | Confidence: 95/1003.
- **Contradictions:**
  - Entry min_gwa (82.00%1.) differs from renewal Maintain GWA (Semestral GWA >= 2.50 (81%)5.)

---

### Taguig City L.A.N.I. State Universities and Colleges (SUC) / Local Colleges and Universities (LCU) Assistance Scholarship1 (ID: 29)

#### Identity / Affiliations
- **Provider:** Taguig City Government / Taguig Scholarship Secretariat1
- **Category:** Local Government Unit (LGU) / Need-and-Merit1
- **Website:** https://www.taguig.gov.ph1
- **Portal:** https://tcu.edu.ph/lani-scholarship1
- **Guidelines:** City Ordinance No. 9, Series of 2011; Executive Order No. 2011-111
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen1
- **Residency / Destination:** Bona fide resident of Taguig City for at least three (3) years1.
- **Education Level:** College / Undergraduate1.
- **Eligible Year Levels:** 1, 2, 3, 4, 51.
- **Incoming Freshman Only:** No1.
- **Existing College Students:** Yes1.
- **Graduate Students:** No1.
- **Current Enrollment:** Must be enrolled in a State University or College (SUC) or Local College/University (LCU) in NCR1.
- **Academic Requirements:** Passing academic standing with GWA >= 80%1.
- **Minimum GWA:** 80.00%1.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Restricted to SUCs and LCUs within NCR (e.g., PUP, PLM, UDM, TCU)1.
- **Course Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Sectoral / Hidden Requirements:** Sub-categorized by high school background: Public HS graduates receive Basic+SUC/LCU grant; Private HS graduates receive SUC/LCU grant1.
- **Good Moral:** Required1.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Voter registration requirement for applicant/parent1.

#### Timing
- **Who May Apply:** Taguig resident public or private high school graduates enrolled in NCR SUCs or LCUs1.
- **Freshmen:** : Yes1.
- **Sophomores:** : Yes1.
- **Juniors:** : Yes1.
- **Seniors:** : Yes1.
- **Graduates:** : No1.
- **Reapply:** : Yes1.
- **Opening:** Announced semestrally1.
- **Closing:** Semestral cutoff1.
- **Cycle:** Semestral3.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Direct financial grant1.
- **Monthly Stipend:** Integrated into allowance1.
- **Allowance:** Public HS Grads (Basic + SUC/LCU): PHP 15,000.00/year; Private HS Grads (SUC/LCU): PHP 10,000.00/year1.
- **Return Service:** None1.

#### Renewal
- **Maintain GWA:** Semestral GWA >= 2.505.
- **Regular Load:** Minimum 15 units per term5.
- **No Failures:** Zero failing grades5.

#### Disqualifying / Conflicts
- Transferring to a private college or university1.
- Dropping below minimum 15-unit term load5.

#### Required Documents (hidden operational requirements)
- Filled LANI Application Form1.
- Official Certificate of Registration from SUC/LCU1.
- High School Diploma / Form 138 (for new entry) or Term Grade Report1.
- Barangay Certificate of Residency1.
- COMELEC Voter's Certificate1.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 80.00, "income_limit": null, "school_type": ["SUC", "LUC"], "partner_school_restricted": false, "citizenship": "Filipino", "residency_restriction": "TAGUIG_CITY_3_YEARS", "application_window": {"open": "semestral_notice", "close": "semestral_notice"}, "deadline_type": "semestral", "cycle_type": "semester", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● High School Origin Routing: The engine must differentiate between public and private
- **Verification:** Verified1. | Confidence: 95/1003.
- **Contradictions:**
  - Entry min_gwa (80.00%1.) differs from renewal Maintain GWA (Semestral GWA >= 2.505.)

---

### Taguig City L.A.N.I. Lifeline Bar and Board Review Assistance1 (ID: 30)

#### Identity / Affiliations
- **Provider:** Taguig City Government / Taguig Scholarship Secretariat1
- **Category:** Local Government Unit (LGU) / Licensure Review Assistance2
- **Website:** https://www.taguig.gov.ph1
- **Portal:** Taguig Scholarship Secretariat / Physical Submission2
- **Guidelines:** City Ordinance No. 9 s. 2011; LANI Review Guidelines1
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen1
- **Residency / Destination:** Bona fide resident of Taguig City for at least three (3) years immediately preceding application1.
- **Education Level:** College Graduate / Post-Graduate Graduate1.
- **Eligible Year Levels:** Graduated / Board Reviewee2.
- **Incoming Freshman Only:** No2.
- **Existing College Students:** No2.
- **Graduate Students:** Yes (Law/Medical/Graduate reviewees)2.
- **Current Enrollment:** Must be officially registered in a recognized review center or scheduled for upcoming board/bar exam2.
- **Academic Requirements:** Completion of tertiary degree program eligible for board/bar examination2.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Graduation from a CHED/PRC-recognized college or university1.
- **Course Restrictions:** Any course requiring PRC Board Licensure or Supreme Court Bar Examination2.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Required1.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Must submit PRC Notice of Admission (NOA) or Supreme Court permit2.

#### Timing
- **Who May Apply:** College/professional graduates preparing for upcoming licensure examinations2.
- **Freshmen:** : No2.
- **Sophomores:** : No2.
- **Juniors:** : No2.
- **Seniors:** : No2.
- **Graduates:** : Yes (Primary target cohort)2.
- **Reapply:** : No (One-time assistance grant per exam)2.
- **Opening:** Announced prior to major national board/bar exam cycles2.
- **Closing:** Specified per review disbursement cycle2.
- **Cycle:** Rolling / Exam-based2.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Review center fee support2.
- **Monthly Stipend:** None2.
- **Allowance:** One-time grant: PHP 20,000.00 for Bar and Physician Licensure Exams; PHP 15,000.00 for other PRC Board Exams2.
- **Return Service:** None; commitment to serve Taguig City1.

#### Renewal
- **Maintain GWA:** Non-renewable (One-time grant)2.
- **Regular Load:** N/A2.
- **No Failures:** N/A2.

#### Disqualifying / Conflicts
- Enrolled ongoing undergraduate students2.
- Failure to present official PRC Notice of Admission or Supreme Court permit2.
- Prior enjoyment of Taguig Bar/Board assistance for the same exam type2.

#### Required Documents (hidden operational requirements)
- Filled Review Assistance Application Form2.
- PRC Notice of Admission (NOA) or Bar Exam Registration2.
- Two (2) valid government-issued IDs2.
- Transcript of Records showing degree completion1.
- Taguig COMELEC Voter's Certification1.
- Certificate of Residency1.

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [5, 6], "incoming_year_only": false, "requires_current_enrollment": false, "minimum_gwa": null, "income_limit": null, "target_cohort": "LICENSURE_EXAM_REVIEWEES", "partner_school_restricted": false, "citizenship": "Filipino", "residency_restriction": "TAGUIG_CITY_3_YEARS", "application_window": {"open": "rolling_exam_based", "close": "rolling_exam_based"}, "deadline_type": "rolling", "cycle_type": "exam_cycle", "renewable": false, "first_time_only": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Status Mismatch: Displaying this scholarship to current undergraduate students will
- **Verification:** Verified1. | Confidence: 95/1003.
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE) differs from renewal Maintain GWA (Non-renewable (One-time grant)2.)

---

### Makati City College Scholarship Program – SUC and Priority Courses Tracks6 (ID: 31)

#### Identity / Affiliations
- **Provider:** Makati City Government / City Education Department6
- **Category:** Local Government Unit (LGU) / Merit-and-Need3
- **Website:** https://www.makati.gov.ph6
- **Portal:** Makati City Education Department Portal / Physical Office6
- **Guidelines:** Makati City Ordinance No. 2019-A-0366
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen6
- **Residency / Destination:** Bona fide resident of Makati City6.
- **Education Level:** College / Undergraduate3.
- **Eligible Year Levels:** 1 (Incoming Freshmen)6.
- **Incoming Freshman Only:** Yes6.
- **Existing College Students:** Ineligible for initial entry6.
- **Graduate Students:** Ineligible6.
- **Current Enrollment:** Enrolled or accepted as an incoming 1st-year student in any Metro Manila SUC (other than UMak) or DOST-accredited priority course6.
- **Academic Requirements:** Fresh senior high school graduate belonging to the Top 10 Percent of the graduating class6.
- **Minimum GWA:** Minimum GWA of 1.50 (or equivalent 88–90% scale)3.
- **Alt Class Rank:** Belong to the Top 10% of the SHS graduating class6.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Metro Manila SUCs (excluding UMak) or DOST-accredited schools6.
- **Course Restrictions:** DOST-listed priority courses6.
- **Sectoral / Hidden Requirements:** PWDs enrolled in top performing CHED/PRC schools qualify under the PHP 40,000 track6.
- **Good Moral:** Required6.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Must sign a mandatory Service Agreement committing to serve with the Makati City Government upon graduation6.

#### Timing
- **Who May Apply:** Graduating SHS students from Makati public schools belonging to the top 10% of their class6.
- **Freshmen:** : Yes (at initial college entry)6.
- **Sophomores:** : No6.
- **Juniors:** : No6.
- **Seniors:** : No6.
- **Graduates:** : No6.
- **Reapply:** : No6.
- **Opening:** Annual cycle announced following SHS graduation6.
- **Closing:** Specified per annual intake notice6.
- **Cycle:** Fixed / Annual3.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Covered per institutional billing6.
- **Monthly Stipend:** Integrated into total grant6.
- **Allowance:** SUC Track: PHP 20,000.00 total benefit per school year; DOST Priority Courses / PWD Track: PHP 40,000.00 total benefit per school year6.
- **Return Service:** Mandatory service agreement to serve with the Makati City Government after graduation6.

#### Renewal
- **Maintain GWA:** Must maintain a GWA of at least 1.50 (or equivalent) each term6.
- **Regular Load:** Full academic credit load required6.
- **No Failures:** No grade of 5.0, 4.0, Incomplete, or Dropped subjects6.

#### Disqualifying / Conflicts
- Failing grades (5.0), unremoved 4.0, or incomplete marks6.
- Refusal to sign or fulfill the mandatory Makati City Government service agreement6.
- Non-residency in Makati City6.

#### Required Documents (hidden operational requirements)
- Official Application Form6.
- SHS Form 138 showing GWA and Certification of Top 10% Class Rank signed by Principal6.
- Proof of Residency in Makati City (Barangay Certificate / Voter's ID)6.
- Certificate of Enrollment / Admission Notice from Metro Manila SUC or DOST-accredited HEI6.
- Parents' Income Tax Return or Certificate of Indigency6.
- Signed Service Contract Agreement6.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": true, "minimum_gwa": 88.00, "rank_cutoff_alternative": 10, "income_limit": null, "school_type": ["SUC"], "partner_school_restricted": true, "citizenship": "Filipino", "residency_restriction": "MAKATI_CITY_RESIDENT", "return_service_required": true, "application_window": {"open": "annual_notice", "close": "annual_notice"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Service Obligation Friction: Candidates seeking unencumbered grants may reject the
- **Verification:** Verified3. | Confidence: 95/1003.
- **Contradictions:**
  - Entry min_gwa (Minimum GWA of 1.50 (or equivalent 88–90% scale)3.) differs from renewal Maintain GWA (Must maintain a GWA of at least 1.50 (or equivalent) each term6.)

---

### University of Makati (UMak) Token Fee Exemption Program7 (ID: 32)

#### Identity / Affiliations
- **Provider:** University of Makati / City Government of Makati7
- **Category:** Institutional / Local University / Merit-and-Need3
- **Website:** https://www.umak.edu.ph7
- **Portal:** UMak OLEA Portal (https://www.umak.edu.ph/admissions/scholarships/)7
- **Guidelines:** UMak City Ordinance No. 2024-108; UMak Revised Scholarship Guidelines AY 2025–20267
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen7
- **Residency / Destination:** Priority given to bona fide Makati City residents (determined via UMak residency verification)10. Non-Makati residents eligible for specific honor tracks7.
- **Education Level:** College / Undergraduate3.
- **Eligible Year Levels:** 1, 2, 3, 4, 57.
- **Incoming Freshman Only:** No (Entrance exemption is freshman-only; academic retention applies to all years)7.
- **Existing College Students:** Yes7.
- **Graduate Students:** Restricted (Separate graduate fee schedules apply)10.
- **Current Enrollment:** Must be officially admitted and enrolled at the University of Makati7.
- **Academic Requirements:** Entrance exemption requires SHS graduation with "Highest Honor" (GWA 98–100) or "High Honor" (GWA 95–97)7. Continuing exemption governed by semestral GWA cutoffs8.
- **Minimum GWA:** Entrance cutoff: 95.00% (High Honor) or 98.00% (Highest Honor)7. Renewal cutoff: GWA <= 2.50 (If GWA is 2.75–3.00, student pays PHP 2,000/unit)11.
- **Alt Class Rank:** Senior High School Honor Roll certification7.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Restricted strictly to students enrolled at the University of Makati7.
- **Course Restrictions:** Any undergraduate degree program offered by UMak7.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Required (Good disciplinary standing)7.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Governed by UMak retention policies; unofficially dropped subjects cause forfeiture7.

#### Timing
- **Who May Apply:** Officially enrolled UMak undergraduate students7.
- **Freshmen:** : Yes7.
- **Sophomores:** : Yes7.
- **Juniors:** : Yes7.
- **Seniors:** : Yes7.
- **Graduates:** : No7.
- **Reapply:** : Yes (Automated evaluation or semestral application on
- **Opening:** Scheduled per semester on the OLEA system (e.g., January intake for 2nd Sem)7.
- **Closing:** Specified per term registration schedule12.
- **Cycle:** Semestral3.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** 100% exemption from tuition/token fees for qualified honor entrants and high-performing scholars7.
- **Monthly Stipend:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Allowance:** Token exemption value equivalent to PHP 1,000.00 – PHP 5,000.00 per semester depending on residency tier3.
- **Return Service:** None7.

#### Renewal
- **Maintain GWA:** Must maintain prescribed GWA per semester (GWA <= 2.50)8.
- **Regular Load:** Full academic load carried each term7.
- **No Failures:** Zero failing grades or unofficially dropped subjects7.

#### Disqualifying / Conflicts
- GWA dropping between 2.75 and 3.00 results in loss of exemption and triggers a PHP 2,000 per unit tuition fee11.
- Accumulation of unofficially dropped (UD) courses exceeding institutional limits7.

#### Required Documents (hidden operational requirements)
- SHS Grade 12 Report Card (1st and 2nd Semesters)7.
- Certificate of Highest Honor (GWA 98–100) or High Honor (GWA 95–97) signed by Principal7.
- Voter's Certification of applicant or parent (for Makati resident tagging)10.
- Official UMak Grade Report for preceding semester (for continuing applicants)7.
- Online application submission via UMak OLEA account7.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 95.00, "renewal_gwa": 81.00, "income_limit": null, "school_type": ["UMAK_ONLY"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "OLEA_semestral_dates", "close": "OLEA_semestral_dates"}, "deadline_type": "semestral", "cycle_type": "semester", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Grade Penalty Threshold: The system must enforce logic checking for GWAs between
- **Verification:** Verified3. | Confidence: n/a
- **Contradictions:**
  - Entry min_gwa (Entrance cutoff: 95.00% (High Honor) or 98.00% (Highest Honor)7. Renewal cutoff: GWA <= 2.50 (If GWA is 2.75–3.00, student pays PHP 2,000/unit)11.) differs from renewal Maintain GWA (Must maintain prescribed GWA per semester (GWA <= 2.50)8.)

---

### Valenzuela City Dr. Pio Valenzuela Scholarship Program13 (ID: 33)

#### Identity / Affiliations
- **Provider:** Valenzuela City Government / City Social Welfare and Development Office13
- **Category:** Local Government Unit (LGU) / Merit-and-Need3
- **Website:** https://www.valenzuela.gov.ph13
- **Portal:** https://www.valenzuela.gov.ph/drpioscholarship13
- **Guidelines:** Valenzuela Municipal Council Ordinance No. 12 of 1995 (amended by City Ordinance No. 37, Series of 2009)13
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born Filipino Citizen13.
- **Residency / Destination:** Long-term resident of Valenzuela City (at least four consecutive years of residency immediately prior to application)13.
- **Education Level:** College / Undergraduate (Incoming Freshmen)13.
- **Eligible Year Levels:** 1 (Incoming First-Year College Students)13.
- **Incoming Freshman Only:** Yes13.
- **Existing College Students:** Ineligible for new entry13.
- **Graduate Students:** Ineligible13.
- **Current Enrollment:** Enrolled or applying for admission in any CHED-accredited college or university13.
- **Academic Requirements:** SHS GWA of at least 85.00% with no subject grade below 85% in Grade 11 (1st and 2nd sem) and Grade 12 (1st sem)13. Must pass the scholarship qualifying examination13.
- **Minimum GWA:** 85.00% (with zero subject grades below 85%)13.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined gross annual income of employed parents must NOT exceed PHP 120,000.0013.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Any public or private HEI accredited by the Commission on Higher Education (CHED)13.
- **Course Restrictions:** Open to all baccalaureate degree programs under GAS, STEM, HUMSS, and ABM strands17.
- **Sectoral / Hidden Requirements:** Underprivileged/low-income family status verified via BIR ITR or Barangay Certificate of Indigency13.
- **Good Moral:** Required (Certificate of Good Moral Character)13.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Must be a graduate of a public or private senior high school in Valenzuela City13. Voter's certificate of parent/applicant required16.

#### Timing
- **Who May Apply:** Graduating Grade 12 students and SHS graduates residing in Valenzuela City for >= 4 years13.
- **Freshmen:** : Yes (prior to/at starting college intake)13.
- **Sophomores:** : No13.
- **Juniors:** : No13.
- **Seniors:** : No13.
- **Graduates:** : No13.
- **Reapply:** : No13.
- **Opening:** January 3 annually13.
- **Closing:** Late February / Mid-March (e.g., March 20)13.
- **Cycle:** Fixed / Annual3.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Educational grant allocation13.
- **Monthly Stipend:** Integrated into annual grant13.
- **Allowance:** PHP 30,000.00 per academic year (PHP 15,000.00 per semester)13.
- **Return Service:** None13.

#### Renewal
- **Maintain GWA:** Must maintain a semestral GWA of at least 2.00 (85%)13.
- **Regular Load:** Full-time credit enrollment13.
- **No Failures:** Individual subject grades must not fall below 2.2513.

#### Disqualifying / Conflicts
- Parents' annual gross income exceeding PHP 120,000.0013.
- Subject grade below 85% in SHS or below 2.25 in college13.
- Residency in Valenzuela City less than four (4) consecutive years13.
- Non-natural-born citizenship13.

#### Required Documents (hidden operational requirements)
- Accomplished Dr. Pio Valenzuela Scholarship Application Form14.
- Certified True Copy of Grade 11 Report Card (1st & 2nd Semesters) and Grade 12 Report Card (1st Semester) showing GWA >= 85% and no grade below 8516.
- Proof of Income: Certified True Copy of 2024 ITR (Form 2316) showing annual gross income <= PHP 120,000.00, or Joint Affidavit and Certificate of Non-Filing of ITR if unemployed16.
- Barangay Certificate of Residency and Indigency of parents16.
- PSA Certified Birth Certificate of applicant16.
- Certificate of Good Moral Character16.
- Voter's Certificate of registered parent or guardian16.
- Photo of actual street residence of applicant16.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": true, "minimum_gwa": 85.00, "renewal_gwa": 85.00, "income_limit": 120000, "school_type": ["CHED_ACCREDITED_HEI"], "partner_school_restricted": false, "citizenship": "Filipino (Natural-born)", "residency_restriction": "VALENZUELA_CITY_4_YEARS", "application_window": {"open": "01-03", "close": "03-20"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Strict Income Disqualification: The PHP 120,000 annual income threshold is exceptionally
- **Verification:** n/a | Confidence: 95/1003.
- **Contradictions:**
  - Entry min_gwa (85.00% (with zero subject grades below 85%)13.) differs from renewal Maintain GWA (Must maintain a semestral GWA of at least 2.00 (85%)13.)

---

### NavotaAs Academic College Scholarship Program19 (ID: 34)

#### Identity / Affiliations
- **Provider:** Navotas City Government19
- **Category:** Local Government Unit (LGU) / Merit-based3
- **Website:** https://www.navotas.gov.ph19
- **Portal:** Navotas City Hall / City Education Office19
- **Guidelines:** Navotas City Ordinance on Academic Scholarships19
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen19
- **Residency / Destination:** Bona fide resident of Navotas City19.
- **Education Level:** College / Undergraduate3.
- **Eligible Year Levels:** 1, 2, 3, 4, 53.
- **Incoming Freshman Only:** No3.
- **Existing College Students:** Yes3.
- **Graduate Students:** No3.
- **Current Enrollment:** Enrolled or accepted in a recognized higher education institution19.
- **Academic Requirements:** Outstanding academic standing with SHS or college GWA of at least 88.00%3.
- **Minimum GWA:** 88.00%3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Recognized public or private colleges and universities19.
- **Course Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Required19.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Resident voter requirements apply19.

#### Timing
- **Who May Apply:** Qualified resident college students and incoming freshmen3.
- **Freshmen:** : Yes3.
- **Sophomores:** : Yes3.
- **Juniors:** : Yes3.
- **Seniors:** : Yes3.
- **Graduates:** : No3.
- **Reapply:** : Yes3.
- **Opening:** Annual application schedule published by Navotas City Hall19.
- **Closing:** Announced per annual cycle19.
- **Cycle:** Fixed / Annual3.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Full tuition fee coverage3.
- **Monthly Stipend:** PHP 2,200.00 per month3.
- **Allowance:** Integrated into monthly stipend package3.
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Maintain required academic average (>= 88.00%) per term3.
- **Regular Load:** Full credit load per term19.
- **No Failures:** Zero failing grades19.

#### Disqualifying / Conflicts
- Loss of Navotas residency status19.
- Failure to maintain required 88.00% GWA3.

#### Required Documents (hidden operational requirements)
- NavotaAs Application Form19.
- Proof of Residency in Navotas City19.
- Report Card / TOR showing GWA >= 88.00%3.
- Certificate of Enrollment19.
- Certificate of Good Moral Character19.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 88.00, "income_limit": null, "school_type": ["RECOGNIZED_HEI"], "partner_school_restricted": false, "citizenship": "Filipino", "residency_restriction": "NAVOTAS_CITY_RESIDENT", "application_window": {"open": "annual_notice", "close": "annual_notice"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● High Total Value Perception: Live DB lists total_value: 262000 reflecting 4-year cumulative
- **Verification:** Verified3. | Confidence: 98/1003.
- **Contradictions:**
  - Entry min_gwa (88.00%3.) differs from renewal Maintain GWA (Maintain required academic average (>= 88.00%) per term3.)

---

### Marikina City Medical Scholarship Program3 (ID: 35)

#### Identity / Affiliations
- **Provider:** Marikina City Government3
- **Category:** Local Government Unit (LGU) / Graduate / Return Service Obligation3
- **Website:** https://www.marikina.gov.ph3
- **Portal:** Marikina City Hall / Health & Education Office3
- **Guidelines:** Marikina City Ordinance on Medical Scholarships3
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen3
- **Residency / Destination:** Bona fide resident of Marikina City3.
- **Education Level:** Graduate (Doctor of Medicine)3.
- **Eligible Year Levels:** 1, 2, 3, 4 (Medical School Years)3.
- **Incoming Freshman Only:** No3.
- **Existing College Students:** Eligible as medical students3.
- **Graduate Students:** Yes (Restricted strictly to Doctor of Medicine degree)3.
- **Current Enrollment:** Accepted or enrolled in a recognized Doctor of Medicine program3.
- **Academic Requirements:** Bachelor's degree completion and NMAT score meeting medical school entry standards; GWA >= 85.00%3.
- **Minimum GWA:** 85.00%3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined annual gross family income must not exceed PHP 600,000.003.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Accredited medical schools3.
- **Course Restrictions:** Doctor of Medicine3.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Required3.
- **Health:** Physically and mentally fit3.
- **Other Official Rules / Conflicts:** Mandatory return service obligation in Marikina City public hospitals/health centers upon passing the Physician Licensure Examination3.

#### Timing
- **Who May Apply:** Incoming and ongoing medical students residing in Marikina City3.
- **Freshmen:** : Yes (1st year medical students)3.
- **Sophomores:** : Yes (2nd year medical students)3.
- **Juniors:** : Yes (3rd year medical students)3.
- **Seniors:** : Yes (4th year medical students)3.
- **Graduates:** : Yes (Bachelor's graduates entering medical school)3.
- **Reapply:** : Yes3.
- **Opening:** Summer intake period prior to medical academic year3.
- **Closing:** Announced per annual notice3.
- **Cycle:** Fixed / Annual3.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Full tuition and matriculation fee coverage3.
- **Monthly Stipend:** PHP 4,000.00 per month3.
- **Allowance:** Integrated into stipend package3.
- **Return Service:** Mandatory return service in Marikina City public health facilities3.

#### Renewal
- **Maintain GWA:** Maintain passing GWA prescribed by medical school and scholarship rules3.
- **Regular Load:** Full-time enrollment in medical curriculum3.
- **No Failures:** Zero failing grades in medical subjects3.

#### Disqualifying / Conflicts
- Family income exceeding PHP 600,000.003.
- Failure to fulfill return service contract3.
- Academic failure or dismissal from medical school3.

#### Required Documents (hidden operational requirements)
- Application Form3.
- Proof of Marikina Residency3.
- Transcript of Records (TOR) of completed Bachelor's degree (GWA >= 85%)3.
- NMAT Score Report3.
- Admission / Enrollment Certificate from accredited Medical School3.
- Income Tax Return of parents (income <= PHP 600,000)3.
- Signed Return Service Contract3.

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 85.00, "income_limit": 600000, "priority_courses": ["DOCTOR_OF_MEDICINE"], "school_type": ["ACCREDITED_MEDICAL_SCHOOLS"], "partner_school_restricted": false, "citizenship": "Filipino", "residency_restriction": "MARIKINA_CITY_RESIDENT", "return_service_required": true, "application_window": {"open": "annual_notice", "close": "annual_notice"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Pre-Med Candidate Confusion: Automated rules must block undergraduate pre-med
- **Verification:** Verified3. | Confidence: 92/1003.
- **Contradictions:**
  - Entry min_gwa (85.00%3.) differs from renewal Maintain GWA (Maintain passing GWA prescribed by medical school and scholarship rules3.)

---

### Muntinlupa Most Outstanding Students (10 MOST) Academic Scholarship20 (ID: 47)

#### Identity / Affiliations
- **Provider:** Muntinlupa Scholarship Division (MSD), City Government of Muntinlupa21
- **Category:** Local Government Unit (LGU) / Merit-based3
- **Website:** https://www.muntinlupacity.gov.ph24
- **Portal:** https://msd.muntinlupacity.gov.ph23
- **Guidelines:** Muntinlupa City Ordinance No. 2023-143; MSD Service Charter21
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen25
- **Residency / Destination:** Bona fide resident of Muntinlupa City holding a valid Muntinlupa Care Card21.
- **Education Level:** College / Undergraduate3.
- **Eligible Year Levels:** 1 (Incoming Freshmen)3.
- **Incoming Freshman Only:** Yes3.
- **Existing College Students:** Ineligible for initial entry21.
- **Graduate Students:** Ineligible21.
- **Current Enrollment:** Must be admitted/enrolled in UP (Luzon campuses), DOST priority programs, or CHED Centers of Excellence21.
- **Academic Requirements:** Yearly 10 MOST Awardees or top-ranked public SHS graduates with GWA >= 90.00%3.
- **Minimum GWA:** 90.00%3.
- **Alt Class Rank:** Designated 10 MOST Awardee status21.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** UP Luzon Campuses, DOST Priority Program Schools, CHED Centers of Excellence21.
- **Course Restrictions:** DOST Priority Programs, CHED COE Programs21.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Required (Certificate of Good Moral)21.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Must possess an active Muntinlupa Care Card number21.

#### Timing
- **Who May Apply:** 10 MOST Awardees and qualified top public SHS graduates in Muntinlupa21.
- **Freshmen:** : Yes (at initial college entry)21.
- **Sophomores:** : No21.
- **Juniors:** : No21.
- **Seniors:** : No21.
- **Graduates:** : No21.
- **Reapply:** : No21.
- **Opening:** Mid-year cycle following annual MOST pre-awarding events21.
- **Closing:** Announced on MSD portal25.
- **Cycle:** Fixed / Annual3.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Full or partial tuition grant per university billing3.
- **Monthly Stipend:** PHP 5,000.00 per month3.
- **Allowance:** PHP 130,000.00 maximum total financial package per school year3.
- **Return Service:** Mandatory scheduling of service obligation via MSD portal20.

#### Renewal
- **Maintain GWA:** Maintain required academic standing per semester21.
- **Regular Load:** Full-time credit enrollment21.
- **No Failures:** Zero failing grades21.

#### Disqualifying / Conflicts
- Enrolling in non-COE private institutions outside UP/DOST frameworks21.
- Lack of valid Muntinlupa Care Card21.
- Non-compliance with mandatory MSD service obligation20.

#### Required Documents (hidden operational requirements)
- Duly accomplished MSD Application Form21.
- Muntinlupa Care Card or Official Receipt with Care Card Number21.
- SHS Form 138 showing GWA >= 90.00%3.
- Certificate of Good Moral Character21.
- Voter's ID or Voter's Certification of applicant or parents21.
- Certificate of Enrollment from UP Luzon, DOST school, or CHED COE21.
- 2x2 ID Picture21.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": true, "minimum_gwa": 90.00, "income_limit": null, "school_type": ["UP_SYSTEM_LUZON", "DOST_PRIORITY_SCHOOLS", "CHED_CENTER_OF_EXCELLENCE"], "partner_school_restricted": true, "citizenship": "Filipino", "residency_restriction": "MUNTINLUPA_CARE_CARD_HOLDER", "return_service_required": true, "application_window": {"open": "annual_notice", "close": "annual_notice"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Care Card Dependency: Automated recommendation logic must check if the applicant
- **Verification:** Verified3. | Confidence: 90/1003.
- **Contradictions:**
  - Entry min_gwa (90.00%3.) differs from renewal Maintain GWA (Maintain required academic standing per semester21.)

---

### Muntinlupa Continuing Assistance for Reintegrating Students (CARES) Financial Assistance Program21 (ID: 48)

#### Identity / Affiliations
- **Provider:** Muntinlupa Scholarship Division (MSD), City Government of Muntinlupa21
- **Category:** Local Government Unit (LGU) / Financial Assistance / Need-based3
- **Website:** https://www.muntinlupacity.gov.ph24
- **Portal:** https://msd.muntinlupacity.gov.ph23
- **Guidelines:** Muntinlupa City Ordinance No. 2023-143; MSD Service Charter21
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen25
- **Residency / Destination:** Bona fide resident of Muntinlupa City holding an active Muntinlupa Care Card21.
- **Education Level:** College / Undergraduate3.
- **Eligible Year Levels:** 1, 2, 3, 4, 53.
- **Incoming Freshman Only:** No21.
- **Existing College Students:** Yes21.
- **Graduate Students:** Ineligible21.
- **Current Enrollment:** Must be enrolled in any college or university within Luzon25.
- **Academic Requirements:** Must maintain the required number of units and General Weighted Average (GWA) set by the MSD (GWA >= 80.00%)3.
- **Minimum GWA:** 80.00%3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Any recognized public or private college or university in Luzon25.
- **Course Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Sectoral / Hidden Requirements:** Caters to recipients of Basic Scholarship in their continuing college studies26. Categorized into three (3) brackets26.
- **Good Moral:** Required21.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Requires Muntinlupa Care Card registration21.

#### Timing
- **Who May Apply:** Incoming freshmen and existing college students in Luzon colleges/universities21.
- **Freshmen:** : Yes21.
- **Sophomores:** : Yes21.
- **Juniors:** : Yes21.
- **Seniors:** : Yes21.
- **Graduates:** : No21.
- **Reapply:** : Yes21.
- **Opening:** Semestral schedule posted on MSD portal/Facebook page21.
- **Closing:** Semestral cutoff27.
- **Cycle:** Semestral3.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Direct stipend assistance26.
- **Monthly Stipend:** PHP 1,000.00 per month3.
- **Allowance:** PHP 10,000.00 per academic year (PHP 5,000.00 per semester)3.
- **Return Service:** Scheduling of service obligation via MSD online portal20.

#### Renewal
- **Maintain GWA:** Maintain GWA set by MSD (GWA <= 2.50 / 80%)26.
- **Regular Load:** Enrolled in prescribed credit units per semester26.
- **No Failures:** Zero failing grades23.

#### Disqualifying / Conflicts
- Enrolling in institutions outside Luzon25.
- Failure to maintain required MSD GWA or term credit units26.
- Lack of valid Muntinlupa Care Card registration21.

#### Required Documents (hidden operational requirements)
- Duly accomplished CARES Application Form21.
- Muntinlupa Care Card or Official Receipt with Care Card Number21.
- Current School ID21.
- Certificate of Enrollment for the current semester21.
- Certified Copy of Previous Semester Grades21.
- Curriculum / Prospectus (if applicable)23.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 80.00, "income_limit": null, "school_type": ["RECOGNIZED_HEI_IN_LUZON"], "partner_school_restricted": false, "citizenship": "Filipino", "residency_restriction": "MUNTINLUPA_CARE_CARD_HOLDER", "return_service_required": true, "application_window": {"open": "semestral_notice", "close": "semestral_notice"}, "deadline_type": "semestral", "cycle_type": "semester", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Geographic Filter Mismatch: Filtering must enforce HEI location IN ('Luzon') to prevent
- **Verification:** Verified3. | Confidence: 96/1003.
- **Contradictions:**
  - Entry min_gwa (80.00%3.) differs from renewal Maintain GWA (Maintain GWA set by MSD (GWA <= 2.50 / 80%)26.)

---

### Parañaque City Tertiary Education Financial Assistance Program3 (ID: 50)

#### Identity / Affiliations
- **Provider:** Parañaque City Government / City Special Services Office3
- **Category:** Local Government Unit (LGU) / Need-and-Merit3
- **Website:** https://www.paranaquecity.gov.ph3
- **Portal:** Parañaque City Secretariat Portal / Physical Submission3
- **Guidelines:** Parañaque City Ordinance on Tertiary Financial Assistance3
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen3
- **Residency / Destination:** Bona fide resident of Parañaque City3.
- **Education Level:** College / Undergraduate3.
- **Eligible Year Levels:** 1, 2, 3, 4, 53.
- **Incoming Freshman Only:** No3.
- **Existing College Students:** Yes3.
- **Graduate Students:** No3.
- **Current Enrollment:** Must be enrolled in a CHED-recognized college or university3.
- **Academic Requirements:** Minimum GWA of 80.00%3.
- **Minimum GWA:** 80.00%3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined annual gross family income must not exceed PHP 300,000.003.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** CHED-recognized colleges and universities3.
- **Course Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Required3.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Voter's certification of applicant or parent in Parañaque City required3.

#### Timing
- **Who May Apply:** Qualified Parañaque resident college students3.
- **Freshmen:** : Yes3.
- **Sophomores:** : Yes3.
- **Juniors:** : Yes3.
- **Seniors:** : Yes3.
- **Graduates:** : No3.
- **Reapply:** : Yes3.
- **Opening:** Semestral schedule published by Parañaque City Government3.
- **Closing:** Specified per term (e.g., August 20 for AY 2026 intake)3.
- **Cycle:** Semestral3.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Direct cash assistance allocation3.
- **Monthly Stipend:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Allowance:** PHP 12,000.00 per academic year (PHP 6,000.00 per semester)3.
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Maintain semestral GWA of at least 80.00%3.
- **Regular Load:** Full-time credit enrollment3.
- **No Failures:** Zero failing grades3.

#### Disqualifying / Conflicts
- Family income exceeding PHP 300,000.003.
- Non-residency in Parañaque City3.
- Failure to maintain required 80.00% GWA3.

#### Required Documents (hidden operational requirements)
- Application Form3.
- Certificate of Enrollment / Registration Form3.
- Preceding Term Grade Report (GWA >= 80.00%)3.
- Barangay Certificate of Residency in Parañaque City3.
- Parents' Income Tax Return or Certificate of Indigency3.
- Parañaque COMELEC Voter's Certificate3.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 80.00, "income_limit": 300000, "school_type": ["CHED_RECOGNIZED_HEI"], "partner_school_restricted": false, "citizenship": "Filipino", "residency_restriction": "PARANAQUE_CITY_RESIDENT", "application_window": {"open": "08-01", "close": "08-20"}, "deadline_type": "exact", "cycle_type": "semester", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Short Application Windows: Application windows are precise and time-sensitive; the
- **Verification:** Verified3. | Confidence: 95/1003.
- **Contradictions:**
  - Entry min_gwa (80.00%3.) differs from renewal Maintain GWA (Maintain semestral GWA of at least 80.00%3.)

---

### Taguig City L.A.N.I. Full Scholarship Track1 (ID: 95)

#### Identity / Affiliations
- **Provider:** Taguig City Government / Taguig Scholarship Secretariat1
- **Category:** Local Government Unit (LGU) / Merit-and-Need1
- **Website:** https://www.taguig.gov.ph1
- **Portal:** https://tcu.edu.ph/lani-scholarship1
- **Guidelines:** City Ordinance No. 9, Series of 2011; Executive Order No. 2011-111
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen1
- **Residency / Destination:** Bona fide resident of Taguig City for at least three (3) years1.
- **Education Level:** College / Undergraduate / Professional1.
- **Eligible Year Levels:** 1, 2, 3, 4, 51.
- **Incoming Freshman Only:** No1.
- **Existing College Students:** Yes1.
- **Graduate Students:** No (Except Law and Medicine)1.
- **Current Enrollment:** Enrolled in any recognized college/university for Top 10 public SHS graduates, or DOST priority/law/medicine schools1.
- **Academic Requirements:** GWA of at least 85.00% or designated Top 10 class rank1.
- **Minimum GWA:** 85.00%1.
- **Alt Class Rank:** Top 10 graduates of public high schools in Taguig1.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Unrestricted for Top 10 public SHS grads; DOST/PRC/CHED accredited for priority tracks1.
- **Course Restrictions:** Unrestricted for Top 10 public SHS grads; DOST S&T, Law, and Medicine for other applicants1.
- **Sectoral / Hidden Requirements:** PDAO endorsement required for PWD applicants1.
- **Good Moral:** Required1.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Voter registration requirement for applicant/parent1.

#### Timing
- **Who May Apply:** Top 10 graduates of Taguig public high schools and qualified priority course students1.
- **Freshmen:** : Yes1.
- **Sophomores:** : Yes1.
- **Juniors:** : Yes1.
- **Seniors:** : Yes1.
- **Graduates:** : No1.
- **Reapply:** : Yes1.
- **Opening:** Semestral publication1.
- **Closing:** Semestral deadline1.
- **Cycle:** Semestral3.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Direct financial grant1.
- **Monthly Stipend:** Integrated into allowance1.
- **Allowance:** PHP 40,000.00 to PHP 50,000.00 per school year (PHP 20,000.00 to PHP 25,000.00 per semester)1.
- **Return Service:** None1.

#### Renewal
- **Maintain GWA:** Semestral GWA >= 2.505.
- **Regular Load:** Minimum 15 credit units5.
- **No Failures:** Zero failing grades5.

#### Disqualifying / Conflicts
- Loss of 15-unit term load5.
- Accumulation of failing or incomplete marks5.

#### Required Documents (hidden operational requirements)
- Filled LANI Application Form1.
- Principal's Certification of Top 10 Class Rank (for public SHS grads)1.
- Grade Report showing GWA >= 85.00%1.
- Taguig COMELEC Voter's Certificate1.
- Certificate of Enrollment1.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 85.00, "rank_cutoff_alternative": 10, "income_limit": null, "school_type": ["RECOGNIZED_HEI"], "partner_school_restricted": false, "citizenship": "Filipino", "residency_restriction": "TAGUIG_CITY_3_YEARS", "application_window": {"open": "semestral_notice", "close": "semestral_notice"}, "deadline_type": "semestral", "cycle_type": "semester", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Overriding School Restrictions: Matching engine must override school/course restrictions
- **Verification:** Verified1. | Confidence: 95/1003.
- **Contradictions:**
  - Entry min_gwa (85.00%1.) differs from renewal Maintain GWA (Semestral GWA >= 2.505.)

---

### Taguig City L.A.N.I. Basic Scholarship Track1 (ID: 96)

#### Identity / Affiliations
- **Provider:** Taguig City Government / Taguig Scholarship Secretariat1
- **Category:** Local Government Unit (LGU) / Need-based1
- **Website:** https://www.taguig.gov.ph1
- **Portal:** https://tcu.edu.ph/lani-scholarship1
- **Guidelines:** City Ordinance No. 9, Series of 2011; Executive Order No. 2011-111
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen1
- **Residency / Destination:** Bona fide resident of Taguig City for at least three (3) years1.
- **Education Level:** College / Undergraduate1.
- **Eligible Year Levels:** 1, 2, 3, 4, 51.
- **Incoming Freshman Only:** No1.
- **Existing College Students:** Yes1.
- **Graduate Students:** No1.
- **Current Enrollment:** Enrolled in any private college or university in NCR (not enrolled in an SUC or LUC)1.
- **Academic Requirements:** Passing academic standing with GWA >= 78.00%1.
- **Minimum GWA:** 78.00%1.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Private higher education institutions in NCR (Excludes SUCs and LUCs)1.
- **Course Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Sectoral / Hidden Requirements:** Must be a graduate of a public high school in Taguig City or nearby NCR municipalities/cities1.
- **Good Moral:** Required1.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Voter registration requirement for applicant/parent1.

#### Timing
- **Who May Apply:** Taguig resident public high school graduates enrolled in private colleges in NCR1.
- **Freshmen:** : Yes1.
- **Sophomores:** : Yes1.
- **Juniors:** : Yes1.
- **Seniors:** : Yes1.
- **Graduates:** : No1.
- **Reapply:** : Yes1.
- **Opening:** Semestral schedule1.
- **Closing:** Semestral cutoff1.
- **Cycle:** Semestral3.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Direct grant allocation1.
- **Monthly Stipend:** Integrated into allowance1.
- **Allowance:** PHP 10,000.00 per school year (PHP 5,000.00 per semester)1.
- **Return Service:** None1.

#### Renewal
- **Maintain GWA:** Semestral GWA >= 2.505.
- **Regular Load:** Minimum 15 credit units5.
- **No Failures:** Zero failing grades5.

#### Disqualifying / Conflicts
- Enrolling in an SUC or LUC (must transfer to SUC/LCU assistance track ID 29)1.
- Graduation from a private high school1.

#### Required Documents (hidden operational requirements)
- Filled LANI Application Form1.
- Public SHS Diploma / Form 1381.
- Certificate of Enrollment from private HEI in NCR1.
- Preceding Semester Grade Report (GWA >= 78.00%)1.
- Taguig COMELEC Voter's Certificate1.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 78.00, "income_limit": null, "school_type": ["PRIVATE_HEI_NCR"], "partner_school_restricted": false, "citizenship": "Filipino", "residency_restriction": "TAGUIG_CITY_3_YEARS", "application_window": {"open": "semestral_notice", "close": "semestral_notice"}, "deadline_type": "semestral", "cycle_type": "semester", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● High School Origin Routing: System must verify user.high_school_type == 'Public' and
- **Verification:** n/a | Confidence: n/a
- **Contradictions:**
  - Entry min_gwa (78.00%1.) differs from renewal Maintain GWA (Semestral GWA >= 2.505.)

---

### Taguig City L.A.N.I. Leadership and Educators Advancement and Development (LEAD) Graduate Scholarship1 (ID: 97)

#### Identity / Affiliations
- **Provider:** Taguig City Government / Taguig Scholarship Secretariat1
- **Category:** Local Government Unit (LGU) / Graduate / Public & Educator Sectoral1
- **Website:** https://www.taguig.gov.ph1
- **Portal:** https://tcu.edu.ph/lani-scholarship1
- **Guidelines:** City Ordinance No. 9, Series of 2011; LANI LEAD Guidelines1
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen1
- **Residency / Destination:** Bona fide resident of Taguig City for at least three (3) years immediately preceding application1.
- **Education Level:** Graduate (Master's or Doctoral Degree)1.
- **Eligible Year Levels:** 1, 2, 3 (Postgraduate Years)1.
- **Incoming Freshman Only:** No1.
- **Existing College Students:** No (Restricted to post-baccalaureate graduate students)1.
- **Graduate Students:** Yes (Primary target cohort)1.
- **Current Enrollment:** Enrolled in a Master's or Doctoral program with courses aligned with applicant's profession1.
- **Academic Requirements:** Latest work performance rating of "Excellent" or at least "Very Satisfactory"1; GWA >= 85.00%3.
- **Minimum GWA:** 85.00%1.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** Must NOT exceed 50 years of age at time of application1.
- **School / Consortium Restrictions:** Recognized public or private graduate schools1.
- **Course Restrictions:** Graduate degree courses strictly aligned with applicant's current profession1.
- **Sectoral / Hidden Requirements:** Must have been in service for at least three (3) years in a national or local government office in Taguig, or a teacher in a public/private school in Taguig, or uniformed PNP personnel based in Taguig1.
- **Good Moral:** Required (Good moral character in paper and deeds)1.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** DepEd teachers require endorsement from DepEd Superintendent; PNP personnel require endorsement from Taguig Chief of Police; Taguig LGU employees require endorsement from Department Head and City Administrator1.

#### Timing
- **Who May Apply:** Resident public/private teachers, government employees, and uniformed personnel in Taguig taking Master's or Doctoral degrees1.
- **Freshmen:** : N/A1.
- **Sophomores:** : N/A1.
- **Juniors:** : N/A1.
- **Seniors:** : N/A1.
- **Graduates:** : Yes (Master's/Doctoral enrollees)1.
- **Reapply:** : Yes1.
- **Opening:** Semestral schedule (DepEd applicants submitted per DepEd-TAPAT Division Office schedule)1.
- **Closing:** Semestral cutoff1.
- **Cycle:** Annual / Semestral1.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Direct grant subsidy1.
- **Monthly Stipend:** Integrated into grant1.
- **Allowance:** PHP 18,000.00 to PHP 60,000.00 per school year depending on school category4.
- **Return Service:** Mandatory commitment to continue serving Taguig City1.

#### Renewal
- **Maintain GWA:** Maintain passing graduate school GWA1.
- **Regular Load:** Enrolled in active graduate credit units1.
- **No Failures:** Zero failing grades5.

#### Disqualifying / Conflicts
- Applicant age exceeding 50 years old1.
- Work performance rating dropping below "Very Satisfactory"1.
- Service in Taguig location less than three (3) years1.
- Enrollment in graduate courses unaligned with current profession1.

#### Required Documents (hidden operational requirements)
- Filled LEAD Application Form with 3 sets of 2x2 photos1.
- Registration Form / Proof of Enrolment in Master's or Doctoral program1.
- Authenticated Copy of Grades / Transcript of Records1.
- Updated Curriculum Checklist of enrolled graduate course1.
- Service Record proving at least 3 years of service in Taguig1.
- Latest Work Performance Evaluation (Very Satisfactory or Excellent)1.
- Official Sectoral Endorsement (DepEd Superintendent / Police Chief / City Administrator)1.
- Signed copy of approved thesis/dissertation proposal (for research grant)1.

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1, 2, 3], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 85.00, "income_limit": null, "age_limit": 50, "sectoral_restriction": "TAGUIG_GOVT_TEACHER_PNP_3_YEARS", "partner_school_restricted": false, "citizenship": "Filipino", "residency_restriction": "TAGUIG_CITY_3_YEARS", "return_service_required": true, "application_window": {"open": "semestral_notice", "close": "semestral_notice"}, "deadline_type": "semestral", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Sectoral Endorsement Failure: Automated matching engines must require users to
- **Verification:** Verified1. | Confidence: 95/1003.
- **Contradictions:**
  - Entry min_gwa (85.00%1.) differs from renewal Maintain GWA (Maintain passing graduate school GWA1.)

---

### Makati City Premier and Specialized School Scholarship6 (ID: 98)

#### Identity / Affiliations
- **Provider:** Makati City Government / City Education Department6
- **Category:** Local Government Unit (LGU) / Merit-based3
- **Website:** https://www.makati.gov.ph6
- **Portal:** Makati City Education Department Portal / Physical Office6
- **Guidelines:** Makati City Ordinance No. 2019-A-0366
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen6
- **Residency / Destination:** Bona fide resident of Makati City6.
- **Education Level:** College / Undergraduate3.
- **Eligible Year Levels:** 1 (Incoming Freshmen)6.
- **Incoming Freshman Only:** Yes6.
- **Existing College Students:** Ineligible for initial entry6.
- **Graduate Students:** Ineligible6.
- **Current Enrollment:** Enrolled or accepted as an incoming 1st-year student in a private college or university in Metro Manila declared a CHED Center of Excellence6.
- **Academic Requirements:** Fresh senior high school graduate belonging to the Top 10 Percent of the graduating class6.
- **Minimum GWA:** Minimum GWA of 1.50 (or equivalent 88.00% scale)3.
- **Alt Class Rank:** Belong to the Top 10% of the SHS graduating class6.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Private colleges and universities in Metro Manila declared as CHED Centers of Excellence6.
- **Course Restrictions:** CHED Center of Excellence degree programs6.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Required6.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Must sign a mandatory Service Contract Agreement committing to serve with the Makati City Government after graduation6.

#### Timing
- **Who May Apply:** Graduating SHS students from Makati public schools belonging to the top 10% of their class6.
- **Freshmen:** : Yes (at initial college entry)6.
- **Sophomores:** : No6.
- **Juniors:** : No6.
- **Seniors:** : No6.
- **Graduates:** : No6.
- **Reapply:** : No6.
- **Opening:** Annual cycle following SHS graduation6.
- **Closing:** Specified per annual intake notice6.
- **Cycle:** Fixed / Annual3.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Covered up to grant cap6.
- **Monthly Stipend:** PHP 4,000.00 per month (integrated into total award)3.
- **Allowance:** PHP 80,000.00 total scholarship benefit per school year6.
- **Return Service:** Mandatory service agreement committing scholar to serve with the Makati City Government6.

#### Renewal
- **Maintain GWA:** Must maintain a GWA of at least 1.50 (or equivalent) each term6.
- **Regular Load:** Full credit load required6.
- **No Failures:** Zero failing (5.0), unremoved 4.0, or incomplete marks6.

#### Disqualifying / Conflicts
- Enrolling in non-COE private institutions or public SUCs (must shift to SUC track ID 31)6.
- Failing grades (5.0) or dropping below minimum GWA6.
- Non-compliance with mandatory service agreement6.

#### Required Documents (hidden operational requirements)
- Official Application Form6.
- SHS Form 138 showing GWA and Principal's Certification of Top 10% Class Rank6.
- Proof of Residency in Makati City6.
- Admission Letter / Certificate of Enrollment from private CHED Center of Excellence in Metro Manila6.
- Parents' ITR or Certificate of Indigency6.
- Signed Service Contract Agreement6.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": true, "minimum_gwa": 88.00, "rank_cutoff_alternative": 10, "income_limit": null, "school_type": ["PRIVATE_CHED_CENTER_OF_EXCELLENCE_NCR"], "partner_school_restricted": true, "citizenship": "Filipino", "residency_restriction": "MAKATI_CITY_RESIDENT", "return_service_required": true, "application_window": {"open": "annual_notice", "close": "annual_notice"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● COE Course Validation: System must verify that the specific program enrolled in is
- **Verification:** n/a | Confidence: 96/1003.
- **Contradictions:**
  - Entry min_gwa (Minimum GWA of 1.50 (or equivalent 88.00% scale)3.) differs from renewal Maintain GWA (Must maintain a GWA of at least 1.50 (or equivalent) each term6.)

---

### University of Makati Special Institutional Scholarship7 (ID: 99)

#### Identity / Affiliations
- **Provider:** University of Makati (UMak) / Partner Sponsoring Agencies7
- **Category:** Institutional / Sectoral & Affiliation3
- **Website:** https://www.umak.edu.ph7
- **Portal:** UMak OLEA Portal (https://www.umak.edu.ph/admissions/scholarships/)7
- **Guidelines:** UMak City Ordinance No. 2024-108; UMak Special Scholarship Guidelines8
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen7
- **Residency / Destination:** Dependent on sub-track (Makati employees/DILG/OSCA tracks require local affiliation; sports/arts tracks open)7.
- **Education Level:** College / TVET3.
- **Eligible Year Levels:** 1, 2, 3, 4, 53.
- **Incoming Freshman Only:** No7.
- **Existing College Students:** Yes7.
- **Graduate Students:** Restricted7.
- **Current Enrollment:** Officially enrolled at the University of Makati7.
- **Academic Requirements:** Passing GWA >= 75.00% (or standard college retention GWA <= 2.50)3.
- **Minimum GWA:** 75.00%3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Age Restrictions:** Senior Citizen track requires applicant to be at least 70 years of age at time of application7.
- **School / Consortium Restrictions:** Restricted strictly to students enrolled at the University of Makati7.
- **Course Restrictions:** Any undergraduate or technical-vocational course offered at UMak7.
- **Sectoral / Hidden Requirements:** Must belong to one of the designated categories and present official endorsement:
- **Good Moral:** Required7.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Endorsement letters must be submitted once per academic year or per term as mandated7.

#### Timing
- **Who May Apply:** Officially enrolled UMak students meeting special sectoral criteria7.
- **Freshmen:** : Yes7.
- **Sophomores:** : Yes7.
- **Juniors:** : Yes7.
- **Seniors:** : Yes7.
- **Graduates:** : No7.
- **Reapply:** : Yes (Requires annual/semestral re-endorsement)7.
- **Opening:** Announced semestrally on UMak OLEA system7.
- **Closing:** Term registration deadline12.
- **Cycle:** Semestral3.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Full (100%) or Partial (50%) exemption from tuition/token fees7.
- **Monthly Stipend:** PHP 1,000.00 per month (depending on sponsor track)3.
- **Allowance:** Total value up to PHP 15,000.00 per school year3.
- **Return Service:** Active participation in university sports, culture, or community programs (for athletes/artists)7.

#### Renewal
- **Maintain GWA:** Maintain passing GWA and comply with university retention policies7.
- **Regular Load:** Full academic credit load carried7.
- **No Failures:** Zero failing grades7.

#### Disqualifying / Conflicts
- Failure to submit updated sectoral endorsement letter7.
- Unapproved reduction of academic unit load7.

#### Required Documents (hidden operational requirements)
- Proof of Enrollment at UMak7.
- Preceding Term Grade Report7.
- Specific Sectoral Endorsement / ID: ○ DILG Makati Endorsement Letter7. ○ OSCA Endorsement + Senior Citizen ID (for age >= 70)7. ○ Center for Inclusive Education Endorsement + PWD ID7. ○ AFP Beneficiary Certificate / ID7. ○ Proof of Parent Employment in Makati City Government11.
- Online application submission via UMak OLEA Portal7.

#### Recommended Schema / Fields
```json
{ "education_level": ["College", "TVET"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 75.00, "income_limit": null, "sectoral_restriction": "UMAK_SPECIAL_SECTORAL_ENDORSED", "school_type": ["UMAK_ONLY"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "OLEA_semestral_dates", "close": "OLEA_semestral_dates"}, "deadline_type": "semestral", "cycle_type": "semester", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Annual Endorsement Expiration: Endorsements for DILG and employee tracks expire
- **Verification:** Verified3. | Confidence: 96/1003.
- **Contradictions:**
  - Entry min_gwa (75.00%3.) differs from renewal Maintain GWA (Maintain passing GWA and comply with university retention policies7.)

---

### NavotaAs Fisherfolk Children Scholarship Track19 (ID: 100)

#### Identity / Affiliations
- **Provider:** Navotas City Government / City Agriculture's Office (CAO)19
- **Category:** Local Government Unit (LGU) / Need-based / Sectoral3
- **Website:** https://www.navotas.gov.ph19
- **Portal:** City Agriculture's Office / Navotas City Hall19
- **Guidelines:** Navotas City Ordinance on Fisherfolk Educational Support19
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino Citizen19
- **Residency / Destination:** Bona fide resident of Navotas City19.
- **Education Level:** College / TVET3.
- **Eligible Year Levels:** 1, 2, 3, 43.
- **Incoming Freshman Only:** No3.
- **Existing College Students:** Yes3.
- **Graduate Students:** No3.
- **Current Enrollment:** Enrolled or accepted in a recognized college, university, or technical-vocational institution19.
- **Academic Requirements:** GWA of at least 78.00%3.
- **Minimum GWA:** 78.00%3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined annual gross family income must not exceed PHP 180,000.003.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Recognized public or private HEIs or TVET training centers19.
- **Course Restrictions:** Agriculture, Fisheries, Marine Biology, TVET trades, and general degree programs19.
- **Sectoral / Hidden Requirements:** Parent must be an officially registered fisherfolk listed in the Navotas City Juan Magsasaka / Fisherfolk Database maintained by the City Agriculture's Office (CAO)19.
- **Good Moral:** Required19.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Must present official Fisherfolk Identification Card (ID) issued by CAO19.

#### Timing
- **Who May Apply:** Direct legitimate children or dependents of registered Navotas fisherfolk3.
- **Freshmen:** : Yes3.
- **Sophomores:** : Yes3.
- **Juniors:** : Yes3.
- **Seniors:** : Yes3.
- **Graduates:** : No3.
- **Reapply:** : Yes3.
- **Opening:** Annual cycle managed by City Agriculture's Office19.
- **Closing:** Announced per annual cycle19.
- **Cycle:** Fixed / Annual3.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Full or partial tuition grant coverage3.
- **Monthly Stipend:** PHP 1,500.00 per month3.
- **Allowance:** Integrated into monthly stipend3.
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Maintain passing academic GWA (>= 78.00%)3.
- **Regular Load:** Enrolled in regular credit load19.
- **No Failures:** Zero failing grades19.

#### Disqualifying / Conflicts
- Delisting of parent from the official Navotas Fisherfolk Database19.
- Combined family annual gross income exceeding PHP 180,000.003.
- Failure to maintain required 78.00% GWA3.

#### Required Documents (hidden operational requirements)
- Application Form19.
- Official Fisherfolk Registration Certificate / Fisherfolk ID issued by CAO (Juan Magsasaka Database record)19.
- Proof of Relationship (PSA Birth Certificate of applicant showing registered parent)19.
- Barangay Certificate of Residency in Navotas City19.
- School Report Card / TOR (GWA >= 78.00%)3.
- Income Tax Return or Barangay Certificate of Indigency (Income <= PHP 180,000)3.

#### Recommended Schema / Fields
```json
{ "education_level": ["College", "TVET"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 78.00, "income_limit": 180000, "sectoral_restriction": "NAVOTAS_REGISTERED_FISHERFOLK_DEPENDENT", "school_type": ["RECOGNIZED_HEI_OR_TVET"], "partner_school_restricted": false, "citizenship": "Filipino", "residency_restriction": "NAVOTAS_CITY_RESIDENT", "application_window": {"open": "annual_notice", "close": "annual_notice"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Database Verification Dependency: The matching engine must verify parent inclusion in
- **Verification:** Verified3. | Confidence: 95/1003.
- **Contradictions:**
  - Entry min_gwa (78.00%3.) differs from renewal Maintain GWA (Maintain passing academic GWA (>= 78.00%)3.)

---

## SOURCE: `DATABASE_V3_GROUPC_LGU_PART2.pdf`

**Scholarships in this PDF:** 16

### Pasig City Regular Academic Scholarship Program4 (ID: 25)

#### Identity / Affiliations
- **Provider:** Pasig City Government (Pasig City Education Department – Scholarships and Awards Section / PCED-SAS)5
- **Category:** Local Government Unit / Merit-and-Need1
- **Website:** https://www.pasigcity.gov.ph1
- **Portal:** https://scholars.pasigcity.gov.ph1
- **Guidelines:** Pasig City Education Department Citizen's Charter5
- **Status:** Active1

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen3
- **Residency / Destination:** Bonafide resident of Pasig City5
- **Education Level:** Elementary, Junior High School, Senior High School, College4
- **Eligible Year Levels:** All year levels (Grade 1 through College Senior)1
- **Incoming Freshman Only:** No7
- **Existing College Students:** Yes7
- **Graduate Students:** No1
- **Current Enrollment:** Enrolled in a recognized public or private educational institution4
- **Academic Requirements:** Passing general weighted average as certified by report of grades5
- **Minimum GWA:** 85.00%1
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined family gross annual income not exceeding PHP 300,000.00 or submission of a Barangay Certificate of Indigence1
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Recognized public or private schools5
- **Course Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Certificate of Good Moral Character8
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Strict enforcement of the "One-Scholar-One-Family Policy" (only one scholar per household)6; Voter's Certification Record (VCR) of parent (for minors) or student (if 18+)8.

#### Timing
- **Who May Apply:** Resident students in elementary, secondary, and tertiary levels4
- **Freshmen:** : Yes7
- **Sophomores:** : Yes7
- **Juniors:** : Yes7
- **Seniors:** : Yes7
- **Graduates:** : No1
- **Reapply:** : Yes (via annual renewal/reenlistment)7
- **Opening:** August 1, 20251
- **Closing:** September 19, 20257
- **Cycle:** Annual1
- **AY Covered:** AY 2025–20264

#### Benefits (catalog)
- **Tuition:** Covered up to city cap for private school scholars; free in SUCs/LUCs1
- **Monthly Stipend:** PHP 1,500.00 per month1
- **Allowance:** Total annual value up to PHP 25,000.001
- **Return Service:** False1

#### Renewal
- **Maintain GWA:** 85.00%1
- **Regular Load:** Full-time academic load5
- **No Failures:** No failing or dropped subjects5

#### Disqualifying / Conflicts
- Sibling already enjoying a Pasig City scholarship (violating One-Scholar-One-Family rule)6.
- Non-residency in Pasig City5.
- Annual family income exceeding PHP 300,000.00 without indigency status1.

#### Required Documents (hidden operational requirements)
- Printed Online Scholarship Application Form5
- School ID (photocopy, front and back)5
- Report of Grades / Card for the preceding academic year4
- Proof of Enrollment / Enrolment Slip for current academic year4
- Proof of Parents' / Guardians' Income (ITR, Pay Slip, or Barangay Certificate of Indigence)4
- Barangay Certificate of Residency with years of residence indicated4
- Voter's Certification Record (VCR) of parent or applicant8
- Written Essay: "Why do I want to be a Pasig Scholar?"4

#### Recommended Schema / Fields
```json
{ "education_level": ["Elementary", "High School", "College"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 85.00, "income_limit": 300000, "residency_restriction": "PASIG_CITY", "one_scholar_per_family_clause": true, "school_type": ["PUBLIC", "PRIVATE"], "partner_school_restricted": false, "citizenship": "Filipino", "application_window": {"open": "2025-08-01", "close": "2025-09-19"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Household Conflict Risk: Recommending this program to applicants whose family
- **Verification:** Verified1 | Confidence: n/a

---

### Pasig City Arts and Design Scholarship Program5 (ID: 26)

#### Identity / Affiliations
- **Provider:** Pasig City Government (PCED-SAS)5
- **Category:** Local Government Unit / Talent & Specialization1
- **Website:** https://scholars.pasigcity.gov.ph1
- **Portal:** https://scholars.pasigcity.gov.ph1
- **Guidelines:** Pasig City Education Department Citizen's Charter5
- **Status:** Active1

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen3
- **Residency / Destination:** Bonafide resident of Pasig City5
- **Education Level:** Grade 11, Grade 12, College1
- **Eligible Year Levels:** SHS Grade 11–12 and College Years 1–41
- **Incoming Freshman Only:** No1
- **Existing College Students:** Yes1
- **Graduate Students:** No1
- **Current Enrollment:** Enrolled in Grade 11/12 Arts & Design Track or an artistic/creative tertiary degree4
- **Academic Requirements:** Minimum GWA of 80.00%1
- **Minimum GWA:** 80.00%1
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined gross annual family income not exceeding PHP 350,000.001
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Recognized secondary and tertiary institutions5
- **Course Restrictions:** Fine Arts, Graphic Design, Performing Arts, Architecture, Multimedia Arts, and SHS Arts & Design track4
- **Sectoral / Hidden Requirements:** Demonstrated artistic proficiency or enrollment in creative track4
- **Good Moral:** Certificate of Good Moral Character8
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** One-Scholar-One-Family Policy applies6.

#### Timing
- **Who May Apply:** SHS Arts & Design students and creative tertiary majors4
- **Freshmen:** : Yes1
- **Sophomores:** : Yes1
- **Juniors:** : Yes1
- **Seniors:** : Yes1
- **Graduates:** : No1
- **Reapply:** : Yes8
- **Opening:** August 1, 20251
- **Closing:** September 10, 20261
- **Cycle:** Annual1
- **AY Covered:** AY 2025–2026 / AY 2026–20271

#### Benefits (catalog)
- **Tuition:** Full or partial coverage up to city cap1
- **Monthly Stipend:** PHP 1,500.00 per month1
- **Allowance:** Total annual value of PHP 28,000.001
- **Return Service:** False1

#### Renewal
- **Maintain GWA:** 80.00%1
- **Regular Load:** Full load in creative discipline5
- **No Failures:** Zero failing grades5

#### Disqualifying / Conflicts
- Enrolled in non-arts/design degree programs4.
- Family income exceeding PHP 350,000.001.
- Non-residency in Pasig City5.

#### Required Documents (hidden operational requirements)
- Printed Online Application Form5
- Barangay Certificate of Residency4
- Proof of Enrollment in Arts & Design track / creative degree4
- Latest Report of Grades / TOR (GWA 80.00%)1
- Proof of Family Income (ITR / Indigency Certificate)4
- Portfolio of Creative Works / Portfolio Assessment Sheet5

#### Recommended Schema / Fields
```json
{ "education_level": ["Grade 11", "Grade 12", "College"], "eligible_year_levels": [11, 12, 1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 80.00, "income_limit": 350000, "priority_courses": ["ARTS_AND_DESIGN_TRACK", "FINE_ARTS", "MULTIMEDIA_ARTS", "PERFORMING_ARTS"], "residency_restriction": "PASIG_CITY", "school_type": ["PUBLIC", "PRIVATE"], "application_window": {"open": "2025-08-01", "close": "2026-09-10"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Specialization Mismatch: Displaying this program to general STEM/ABM or non-creative
- **Verification:** Verified1 | Confidence: 95/100

---

### Cebu City College Scholarship Program1 (ID: 36)

#### Identity / Affiliations
- **Provider:** Cebu City Government (Cebu City Scholarship Committee)1
- **Category:** Local Government Unit / Merit-and-Need1
- **Website:** https://www.cebucity.gov.ph1
- **Portal:** Cebu City Hall Scholarship Office Portal / City e-Services1
- **Guidelines:** Cebu City College Scholarship Ordinance1
- **Status:** Active1

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen3
- **Residency / Destination:** Bonafide resident of Cebu City1
- **Education Level:** College1
- **Eligible Year Levels:** Year 1, Year 2, Year 3, Year 41
- **Incoming Freshman Only:** No1
- **Existing College Students:** Yes1
- **Graduate Students:** No1
- **Current Enrollment:** Enrolled in accredited partner colleges or universities within Cebu City1
- **Academic Requirements:** Minimum GWA of 80.00% with no failing grades1
- **Minimum GWA:** 80.00%1
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined family annual income not exceeding PHP 350,000.001
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Accredited partner Higher Education Institutions in Cebu City1
- **Course Restrictions:** CHED and City priority degree courses1
- **Sectoral / Hidden Requirements:** Registered voter status (applicant or parent) in Cebu City1
- **Good Moral:** Certificate of Good Moral Character3
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Must not be a recipient of another major government scholarship2.

#### Timing
- **Who May Apply:** Resident high school graduates and ongoing college students in Cebu City1
- **Freshmen:** : Yes1
- **Sophomores:** : Yes1
- **Juniors:** : Yes1
- **Seniors:** : Yes1
- **Graduates:** : No1
- **Reapply:** : Yes1
- **Opening:** June 15 annually1
- **Closing:** August 30 annually1
- **Cycle:** Annual1
- **AY Covered:** AY 2025–2026 / AY 2026–20271

#### Benefits (catalog)
- **Tuition:** Up to PHP 10,000.00 per semester (PHP 20,000.00 per academic year) paid directly to partner school1
- **Monthly Stipend:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Allowance:** Integrated into tuition subsidy voucher1
- **Return Service:** False1

#### Renewal
- **Maintain GWA:** 80.00%1
- **Regular Load:** Full semestral unit load1
- **No Failures:** Zero failing marks1

#### Disqualifying / Conflicts
- Non-voter status of parents or student in Cebu City1.
- Enrolling in non-accredited tertiary institutions outside Cebu City1.
- Family gross annual income exceeding PHP 350,000.001.

#### Required Documents (hidden operational requirements)
- Cebu City Scholarship Application Form1
- Certificate of Residency from Barangay1
- Voter's Certification (Parent or Student) from COMELEC Cebu City1
- Form 138 / High School Report Card or Official TOR1
- Parents' Income Tax Return or Certificate of Indigency1
- Certificate of Good Moral Character3

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 80.00, "income_limit": 350000, "residency_restriction": "CEBU_CITY", "voter_status_required": true, "school_type": ["PARTNER_HEI_CEBU_CITY"], "partner_school_restricted": true, "application_window": {"open": "06-15", "close": "08-30"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Voter Status Failure: Applicants residing in Cebu City whose parents are registered voters
- **Verification:** Verified1 | Confidence: 92/100

---

### Scholarship on Tertiary Education Program – Financial Assistance (STEP-FA) Category B1 (ID: 37)

#### Identity / Affiliations
- **Provider:** Davao City Government (Educational Benefit System Unit / EBSU)11
- **Category:** Local Government Unit / Merit-and-Need1
- **Website:** https://davaocity.gov.ph1
- **Portal:** https://ebsu-escholar.davaocity.gov.ph11
- **Guidelines:** Executive Order No. 7 s. 2014 / EBSU Program Code11
- **Status:** Active1

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen3
- **Residency / Destination:** Resident of Davao City13
- **Education Level:** College1
- **Eligible Year Levels:** Years 1, 2, 3, and 41
- **Incoming Freshman Only:** No1
- **Existing College Students:** Yes12
- **Graduate Students:** No1
- **Current Enrollment:** Enrolled in a CHED-recognized Higher Education Institution in Davao City13
- **Academic Requirements:** GWA of 90.00% to 92.99% (or 88.00% threshold per legacy baseline)1
- **Minimum GWA:** 88.00%1
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** PHP 300,000.00 annual family gross income; verified indigent/below-average income status by CSWDO1
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Recognized HEIs located within Davao City13
- **Course Restrictions:** CHED-prescribed priority programs13
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Certificate of Good Moral Character13
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Strict "One Child Per Family" rule for EBSU grants13; candidate must not enjoy other government/private grants except school academic honor incentives13.

#### Timing
- **Who May Apply:** Graduating SHS students and enrolled tertiary students in Davao City12
- **Freshmen:** : Yes12
- **Sophomores:** : Yes12
- **Juniors:** : Yes12
- **Seniors:** : Yes12
- **Graduates:** : No1
- **Reapply:** : Yes13
- **Opening:** April 1 annually12
- **Closing:** May 31 annually12
- **Cycle:** Annual1
- **AY Covered:** AY 2025–2026 / AY 2026–202712

#### Benefits (catalog)
- **Tuition:** False (direct financial assistance allowance)1
- **Monthly Stipend:** PHP 2,000.00 per month1
- **Allowance:** PHP 20,000.00 per semester (PHP 40,000.00 per academic year)1
- **Return Service:** False1

#### Renewal
- **Maintain GWA:** 88.00%–90.00%1
- **Regular Load:** Full academic unit load13
- **No Failures:** Zero failing or incomplete grades13

#### Disqualifying / Conflicts
- Sibling already benefiting from an EBSU grant13.
- Enjoying another government/private scholarship13.
- GWA falling below 88.00% or presence of failing marks12.

#### Required Documents (hidden operational requirements)
- EBSU eScholar Application Form11
- Certificate of Residency from Barangay12
- CSWDO Certificate of Indigency / Eligibility12
- Income Tax Return or Tax Exemption Certificate of both parents12
- SHS Report Card (for Freshmen) or Official TOR for past 2 semesters (for upperclassmen) showing required GWA12
- Certificate of Good Moral Character12
- Sworn statement of no sibling enjoying an EBSU scholarship13

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 88.00, "maximum_gwa_cap": 92.99, "income_limit": 300000, "residency_restriction": "DAVAO_CITY", "one_child_per_family_clause": true, "school_type": ["DAVAO_CITY_HEI"], "partner_school_restricted": true, "application_window": {"open": "04-01", "close": "05-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Category Misclassification: Applicants with GWA
- **Verification:** Verified1 | Confidence: 90/100
- **Contradictions:**
  - Entry min_gwa (88.00%1) differs from renewal Maintain GWA (88.00%–90.00%1)

---

### Special Educational Assistance Program (SEAP) for Lumad / Financial Assistance Program for Lumad Students1 (ID: 38)

#### Identity / Affiliations
- **Provider:** Davao City Government (EBSU)11
- **Category:** Local Government Unit / Sectoral (Indigenous Peoples)1
- **Website:** https://davaocity.gov.ph1
- **Portal:** https://ebsu-escholar.davaocity.gov.ph11
- **Guidelines:** Executive Order No. 7 s. 2014 / EBSU Lumad Assistance Mandate11
- **Status:** Active1

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen3
- **Residency / Destination:** Resident of Davao City belonging to a recognized IP tribe12
- **Education Level:** College, TVET1
- **Eligible Year Levels:** All tertiary and vocational year levels1
- **Incoming Freshman Only:** No1
- **Existing College Students:** Yes1
- **Graduate Students:** No1
- **Current Enrollment:** Enrolled or accepted in a tertiary or TVET institution in Davao City12
- **Academic Requirements:** Passing general average (75.00% GWA minimum)1
- **Minimum GWA:** 75.00%1
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** PHP 200,000.00 annual family income; CSWDO Indigency certification1
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Recognized colleges, universities, or TVET centers in Davao City12
- **Course Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Sectoral / Hidden Requirements:** Certificate of Tribal Membership / Indigenous Peoples certification issued by National Commission on Indigenous Peoples (NCIP) or Tribal Council12
- **Good Moral:** Certificate of Good Moral Character12
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Must comply with EBSU one-scholar-per-family policy13.

#### Timing
- **Who May Apply:** Lumad / Indigenous tertiary and TVET students in Davao City12
- **Freshmen:** : Yes1
- **Sophomores:** : Yes1
- **Juniors:** : Yes1
- **Seniors:** : Yes1
- **Graduates:** : No1
- **Reapply:** : Yes13
- **Opening:** April 1 annually12
- **Closing:** May 31 annually12
- **Cycle:** Annual1
- **AY Covered:** AY 2025–2026 / AY 2026–202712

#### Benefits (catalog)
- **Tuition:** False (direct financial assistance)1
- **Monthly Stipend:** PHP 2,000.00 per month1
- **Allowance:** Total annual value of PHP 30,000.00 (PHP 15,000.00 per semester)1
- **Return Service:** False1

#### Renewal
- **Maintain GWA:** 75.00% (passing status)1
- **Regular Load:** Enrolled in prescribed program units13
- **No Failures:** Maintain passing grades12

#### Disqualifying / Conflicts
- Lack of official NCIP tribal certification12.
- Non-residency in Davao City12.
- Family gross annual income exceeding PHP 200,000.001.

#### Required Documents (hidden operational requirements)
- EBSU Lumad Scholarship Application Form11
- NCIP Certificate of Tribal Membership / Indigenous Cultural Community Certification12
- CSWDO Certificate of Indigency12
- Certificate of Residency from Barangay12
- Parents' ITR or Tax Exemption Certificate12
- High School Report Card or College Grade Slip (GWA 75.00%)1
- Certificate of Good Moral Character12

#### Recommended Schema / Fields
```json
{ "education_level": ["College", "TVET"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 75.00, "income_limit": 200000, "sectoral_restriction": "NCIP_CERTIFIED_LUMAD_IP", "residency_restriction": "DAVAO_CITY", "school_type": ["DAVAO_CITY_HEI_TVET"], "application_window": {"open": "04-01", "close": "05-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Sectoral Tag Omission: Recommending this program without checking
- **Verification:** Verified1 | Confidence: 98/100
- **Contradictions:**
  - Entry min_gwa (75.00%1) differs from renewal Maintain GWA (75.00% (passing status)1)

---

### Bislig City Collegiate Scholarship Program1 (ID: 39)

#### Identity / Affiliations
- **Provider:** Bislig City Local Government Unit (Surigao del Sur, Region XIII - Caraga)1
- **Category:** Local Government Unit / Merit-and-Need1
- **Website:** https://www.bislig.gov.ph1
- **Portal:** Bislig City Mayor's Office – Scholarship Division Portal1
- **Guidelines:** Bislig City Scholarship Ordinance1
- **Status:** Active1

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen3
- **Residency / Destination:** Bonafide resident of Bislig City, Surigao del Sur1
- **Education Level:** College1
- **Eligible Year Levels:** Years 1, 2, 3, and 41
- **Incoming Freshman Only:** No1
- **Existing College Students:** Yes1
- **Graduate Students:** No1
- **Current Enrollment:** Enrolled in an accredited Higher Education Institution1
- **Academic Requirements:** Minimum GWA of 82.00% with no failing marks1
- **Minimum GWA:** 82.00%1
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined family annual gross income not exceeding PHP 240,000.001
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** CHED-recognized HEIs in Region XIII / Mindanao1
- **Course Restrictions:** Agriculture, Teacher Education, Engineering, Information Technology, and Health Sciences1
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Certificate of Good Moral Character3
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Must not enjoy duplicate local government scholarship grants2.

#### Timing
- **Who May Apply:** Resident college students in Bislig City1
- **Freshmen:** : Yes1
- **Sophomores:** : Yes1
- **Juniors:** : Yes1
- **Seniors:** : Yes1
- **Graduates:** : No1
- **Reapply:** : Yes1
- **Opening:** June 1 annually1
- **Closing:** July 31 annually1
- **Cycle:** Annual1
- **AY Covered:** AY 2025–2026 / AY 2026–20271

#### Benefits (catalog)
- **Tuition:** False1
- **Monthly Stipend:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Allowance:** Financial assistance grant of PHP 6,000.00 per semester (PHP 12,000.00 per academic year)1
- **Return Service:** False1

#### Renewal
- **Maintain GWA:** 82.00%1
- **Regular Load:** Full load per semester1
- **No Failures:** Zero failing grades1

#### Disqualifying / Conflicts
- Non-residency in Bislig City1.
- Family gross annual income exceeding PHP 240,000.001.
- Failure to maintain 82.00% GWA1.

#### Required Documents (hidden operational requirements)
- Bislig City Scholarship Application Form1
- Barangay Certificate of Residency1
- Proof of Income (ITR or Barangay Certificate of Indigency PHP 240,000)1
- Official Report of Grades / TOR (GWA 82.00%)1
- Certificate of Enrollment / Registration Form1
- Certificate of Good Moral Character3

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 82.00, "income_limit": 240000, "residency_restriction": "BISLIG_CITY", "school_type": ["CHED_RECOGNIZED_HEI"], "application_window": {"open": "06-01", "close": "07-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Regional Boundary Risk: Students residing in adjacent Surigao del Sur municipalities (e.g.,
- **Verification:** Verified1 | Confidence: 96/100

---

### Cebu Province Grants Intended for Tertiary Students (CP GIFTS Program)1 (ID: 49)

#### Identity / Affiliations
- **Provider:** Cebu Provincial Government1
- **Category:** Local Government Unit / Need-based1
- **Website:** https://www.cebu.gov.ph1
- **Portal:** Cebu Provincial Capitol – Education Assistance Office Portal1
- **Guidelines:** Cebu Provincial Board Ordinance on CP-GIFTS1
- **Status:** Active1

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen3
- **Residency / Destination:** Resident of Cebu Province (component towns and cities outside independent chartered cities)1
- **Education Level:** College1
- **Eligible Year Levels:** Years 1, 2, 3, and 41
- **Incoming Freshman Only:** No1
- **Existing College Students:** Yes1
- **Graduate Students:** No1
- **Current Enrollment:** Enrolled in a recognized State University, Local College, or Private HEI in Cebu1
- **Academic Requirements:** Minimum GWA of 85.00%1
- **Minimum GWA:** 85.00%1
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined gross annual family income not exceeding PHP 200,000.001
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Recognized HEIs operating within Cebu Province1
- **Course Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Sectoral / Hidden Requirements:** Indigent status verified by MSWDO1
- **Good Moral:** Certificate of Good Moral Character3
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Mandatory participation in provincial civic and environmental activities1.

#### Timing
- **Who May Apply:** Resident college students in Cebu Province1
- **Freshmen:** : Yes1
- **Sophomores:** : Yes1
- **Juniors:** : Yes1
- **Seniors:** : Yes1
- **Graduates:** : No1
- **Reapply:** : Yes1
- **Opening:** July 1 annually1
- **Closing:** August 15 annually1
- **Cycle:** Annual1
- **AY Covered:** AY 2025–2026 / AY 2026–20271

#### Benefits (catalog)
- **Tuition:** False1
- **Monthly Stipend:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Allowance:** PHP 10,000.00 per semester (PHP 20,000.00 per academic year)1
- **Return Service:** True (community civic engagement hours mandated by province)1

#### Renewal
- **Maintain GWA:** 85.00%1
- **Regular Load:** Full-time credit load1
- **No Failures:** Zero failing marks1

#### Disqualifying / Conflicts
- Independent chartered city residency (e.g., Cebu City, Lapu-Lapu City, Mandaue City) if excluded under specific provincial guidelines1.
- Family gross income exceeding PHP 200,000.001.
- Failing grades during semestral evaluation1.

#### Required Documents (hidden operational requirements)
- CP-GIFTS Application Form1
- Barangay and MSWDO Certificate of Indigency1
- Certificate of Residency from Municipality/City1
- Parents' ITR or BIR Tax Exemption Certificate ( PHP 200,000)1
- College TOR or SHS Form 138 (GWA 85.00%)1
- Certificate of Good Moral Character3

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 85.00, "income_limit": 200000, "residency_restriction": "CEBU_PROVINCE", "return_service_required": true, "school_type": ["CEBU_PROVINCE_HEI"], "application_window": {"open": "07-01", "close": "08-15"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● City Jurisdiction Conflict: Students residing in highly urbanized independent cities in
- **Verification:** Verified1 | Confidence: 88/100

---

### Tabuk City College Academic Scholarship1 (ID: 51)

#### Identity / Affiliations
- **Provider:** Tabuk City Local Government Unit (Kalinga, CAR)1
- **Category:** Local Government Unit / Need-based1
- **Website:** https://www.tabuk.gov.ph1
- **Portal:** Tabuk City Special Services Division / Scholarship Office Portal1
- **Guidelines:** Tabuk City Educational Assistance Ordinance1
- **Status:** Active1

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen3
- **Residency / Destination:** Bonafide resident of Tabuk City, Kalinga1
- **Education Level:** College1
- **Eligible Year Levels:** Years 1, 2, 3, and 41
- **Incoming Freshman Only:** No1
- **Existing College Students:** Yes1
- **Graduate Students:** No1
- **Current Enrollment:** Enrolled in a recognized tertiary institution1
- **Academic Requirements:** Minimum GWA of 75.00% (passing average)1
- **Minimum GWA:** 75.00%1
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined family gross annual income not exceeding PHP 120,000.001
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Accredited colleges and universities in CAR / Northern Luzon1
- **Course Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Sectoral / Hidden Requirements:** Indigent family background certified by CSWDO1
- **Good Moral:** Certificate of Good Moral Character3
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Must not receive duplicate financial grants from Tabuk City LGU2.

#### Timing
- **Who May Apply:** Resident college students in Tabuk City1
- **Freshmen:** : Yes1
- **Sophomores:** : Yes1
- **Juniors:** : Yes1
- **Seniors:** : Yes1
- **Graduates:** : No1
- **Reapply:** : Yes1
- **Opening:** July 15, 20261
- **Closing:** August 31, 20261
- **Cycle:** Semestral / Annual1
- **AY Covered:** AY 2026–20271

#### Benefits (catalog)
- **Tuition:** False1
- **Monthly Stipend:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Allowance:** PHP 4,000.00 per semester (PHP 8,000.00 per academic year)1
- **Return Service:** False1

#### Renewal
- **Maintain GWA:** 75.00%1
- **Regular Load:** Full academic load1
- **No Failures:** Zero failing grades1

#### Disqualifying / Conflicts
- Family gross annual income exceeding PHP 120,000.001.
- Non-residency in Tabuk City1.
- Presence of failing marks during semestral review1.

#### Required Documents (hidden operational requirements)
- Tabuk City Scholarship Application Form1
- Barangay Certificate of Residency1
- CSWDO Certificate of Indigency ( PHP 120,000 income)1
- College Grade Slip or Form 138 (GWA 75.00%)1
- Certificate of Enrollment / Registration Slip1
- Certificate of Good Moral Character3

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 75.00, "income_limit": 120000, "residency_restriction": "TABUK_CITY", "school_type": ["RECOGNIZED_HEI"], "application_window": {"open": "2026-07-15", "close": "2026-08-31"}, "deadline_type": "exact", "cycle_type": "semester", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Strict Poverty Threshold: The PHP 120,000 income ceiling is low; applicants above this
- **Verification:** Verified1 | Confidence: 90/100

---

### Quezon City Scholarship Program (QCSP)2 (ID: 88)

#### Identity / Affiliations
- **Provider:** Quezon City Government (Quezon City Youth Development Office / QCYDO)2
- **Category:** Local Government Unit / Merit, Need, & Sectoral Tracks2
- **Website:** https://quezoncity.gov.ph2
- **Portal:** QC eServices Portal (https://qceservices.quezoncity.gov.ph)2
- **Guidelines:** City Ordinance No. SP-3283, S-2024 (Expanded Scholarship Code)2
- **Status:** Active1

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen2
- **Residency / Destination:** Bona fide resident of Quezon City holding a valid QCitizen ID2
- **Education Level:** Senior High School, College, TVET, Postgraduate2
- **Eligible Year Levels:** All year levels corresponding to track2
- **Incoming Freshman Only:** No (Varies: QC Excel is incoming 1st year; Academic/Economic cover ongoing)2
- **Existing College Students:** Yes2
- **Graduate Students:** Yes (Postgraduate Scholarship Track)2
- **Current Enrollment:** Enrolled, registered, or accepted in an educational institution recognized by the city2
- **Academic Requirements:** Academic Track: GWA 1.75 (89.00%) or SHS Academic Honors 1–10; Economic Track: GWA 3.00 (75.00%); Athletic/Arts & Youth Leaders Tracks: GWA 2.50 (85.00%)2
- **Minimum GWA:** 89.00% (1.75 Academic Track) / 75.00% (Economic Track)2
- **Alt Class Rank:** Academic Honors Top 1 to 10 of graduating SHS class2
- **Income Ceilings:** Combined family annual income not exceeding PHP 400,000.001
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Educational institutions recognized by Quezon City / CHED / DepEd / TESDA2
- **Course Restrictions:** City priority disciplines for QC Excel & Specialized Tracks2
- **Sectoral / Hidden Requirements:** Economic track prioritizes 4Ps, solo parent dependents, PWDs, ALS graduates, and displaced families2
- **Good Moral:** Certificate of Good Moral Character2
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Must NOT be a recipient of any other Local Government Unit (LGU) scholarship2.

#### Timing
- **Who May Apply:** Resident SHS, College, TVET, and Postgraduate students in Quezon City2
- **Freshmen:** : Yes2
- **Sophomores:** : Yes2
- **Juniors:** : Yes2
- **Seniors:** : Yes2
- **Graduates:** : Yes (Postgraduate track)2
- **Reapply:** : Yes (Semestral renewal required for tertiary)2
- **Opening:** May 25, 20262
- **Closing:** June 13, 20262
- **Cycle:** Annual application with semestral renewal enlistment2
- **AY Covered:** AY 2025–2026 / AY 2026–20272

#### Benefits (catalog)
- **Tuition:** Covered per track allocation in partner institutions1
- **Monthly Stipend:** PHP 3,500.00 per month (PHP 17,500.00 per semester)1
- **Allowance:** Direct financial stipend up to PHP 75,000.00 per academic year depending on category1
- **Return Service:** False (community civic volunteerism encouraged)1

#### Renewal
- **Maintain GWA:** 1.75 (Academic), 2.50 (Leadership/Sports), 3.00 (Economic)2
- **Regular Load:** Full semestral unit load2
- **No Failures:** Zero failing grades during semestral evaluation2

#### Disqualifying / Conflicts
- Holding a scholarship from another Local Government Unit (LGU exclusivity violation)2.
- Lack of valid QCitizen ID or non-residency in Quezon City2.
- Family gross annual income exceeding PHP 400,000.001.

#### Required Documents (hidden operational requirements)
- Valid QCitizen ID2
- Accomplished QC eServices Online Application2
- Proof of Residency in Quezon City2
- Grade Slip / TOR / Form 138 showing required GWA2
- Proof of Enrollment in recognized institution2
- Income Tax Return or Barangay Certificate of Indigency2
- Track-specific proofs (SK Endorsement, Sports Certificate, PWD ID, Solo Parent ID)2

#### Recommended Schema / Fields
```json
{ "education_level": ["Senior High School", "College", "TVET", "Graduate"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 89.00, "rank_cutoff_alternative": 10, "income_limit": 400000, "residency_restriction": "QUEZON_CITY_QCITIZEN_ID", "lgu_exclusivity_clause": true, "school_type": ["RECOGNIZED_INSTITUTION"], "application_window": {"open": "05-25", "close": "06-13"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Dual LGU Conflict: Students enjoying another city grant (e.g., Manila, Taguig) who apply
- **Verification:** Verified1 | Confidence: 88/100
- **Contradictions:**
  - Entry min_gwa (89.00% (1.75 Academic Track) / 75.00% (Economic Track)2) differs from renewal Maintain GWA (1.75 (Academic), 2.50 (Leadership/Sports), 3.00 (Economic)2)

---

### Manuel L. Quezon Filipino Language and Literature Scholarship Program16 (ID: 89)

#### Identity / Affiliations
- **Provider:** Quezon City Government (QCYDO)15
- **Category:** Local Government Unit / Specialization (Filipino Language & Literature)1
- **Website:** https://qceservices.quezoncity.gov.ph1
- **Portal:** QC eServices Portal (https://qceservices.quezoncity.gov.ph)16
- **Guidelines:** City Ordinance No. SP-3458, S-2025 (amending SP-3283, S-2024)17
- **Status:** Active1

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen18
- **Residency / Destination:** Resident of Quezon City holding a valid QCitizen ID15
- **Education Level:** College, Graduate (Master's / PhD), and Creative Writers/Researchers1
- **Eligible Year Levels:** All tertiary and post-graduate year levels16
- **Incoming Freshman Only:** No16
- **Existing College Students:** Yes16
- **Graduate Students:** Yes16
- **Current Enrollment:** Enrolled in eligible degree programs: Filipino Language, Filipino Literature, Journalism, Philippine Studies, Education (Filipino major), Comparative Literature, or Linguistics16
- **Academic Requirements:** Pass QCYDO interviews, aptitude tests, or submit a portfolio of published original works / literary awards from recognized publisher16
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (evaluated via literary proficiency/portfolio)16
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE (Uncapped under specialized mandate)1
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Recognized public or private Higher Education Institutions15
- **Course Restrictions:** BA/BS/MA/PhD in Filipino, Panitikan, Philippine Studies, Malikhaing Pagsulat, Journalism, Education major in Filipino, Linguistics16
- **Sectoral / Hidden Requirements:** Active involvement or demonstrated proficiency in Filipino literary writing, research, or education16
- **Good Moral:** Certificate of Good Moral Character16
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Must NOT hold another LGU scholarship grant15.

#### Timing
- **Who May Apply:** Tertiary students, postgraduate scholars, educators, and creative writers specializing in Filipino16
- **Freshmen:** : Yes16
- **Sophomores:** : Yes16
- **Juniors:** : Yes16
- **Seniors:** : Yes16
- **Graduates:** : Yes (Postgraduate and Creative Writing track)16
- **Reapply:** : Yes16
- **Opening:** January 22, 202618
- **Closing:** Announced per annual cycle16
- **Cycle:** Annual / Semestral1
- **AY Covered:** AY 2025–2026 / AY 2026–202715

#### Benefits (catalog)
- **Tuition:** Up to PHP 160,000.00 per AY for tertiary scholars in private HEIs; up to PHP 105,000.00 per AY for postgraduate scholars18
- **Monthly Stipend:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Allowance:** PHP 50,000.00 annual stipend for public HEI tertiary scholars18
- **Return Service:** False1

#### Renewal
- **Maintain GWA:** Satisfactory academic standing in specialized degree16
- **Regular Load:** Enrolled in prescribed program units16
- **No Failures:** Zero failing marks16

#### Disqualifying / Conflicts
- Enrollment in non-Filipino/non-Philippine studies degree programs16.
- Failure to present literary portfolio or approved research proposal16.
- Non-residency in Quezon City15.

#### Required Documents (hidden operational requirements)
- Valid QCitizen ID15
- Online Application via QC eServices16
- Proof of Enrollment in eligible Filipino language/literature/Philippine studies degree16
- Academic Grades / Official TOR16
- Literary Portfolio / Proof of Published Works / Certification of Publication from recognized publisher16
- Approved Research Proposal on Filipino language/literature (for Postgraduate track)18

#### Recommended Schema / Fields
```json
{ "education_level": ["College", "Graduate"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "priority_courses": [ "BA_FILIPINO", "BS_EDUCATION_FILIPINO", "MA_FILIPINO", "PHD_FILIPINO", "PHILIPPINE_STUDIES", "MALIKHAING_PAGSULAT", "LINGUISTICS_FILIPINO" ], "residency_restriction": "QUEZON_CITY_QCITIZEN_ID", "lgu_exclusivity_clause": true, "school_type": ["PUBLIC", "PRIVATE"], "application_window": {"open": "01-22", "close": "annual_notice"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Field of Study Filtering: System must validate user.course_code against approved
- **Verification:** Verified17 | Confidence: 98/100
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (evaluated via literary proficiency/portfolio)16) differs from renewal Maintain GWA (Satisfactory academic standing in specialized degree16)

---

### Pasig City Sports Scholarship Program5 (ID: 92)

#### Identity / Affiliations
- **Provider:** Pasig City Government (PCED-SAS / Pasig Sports Development Office)5
- **Category:** Local Government Unit / Athletic Merit1
- **Website:** https://scholars.pasigcity.gov.ph1
- **Portal:** https://scholars.pasigcity.gov.ph1
- **Guidelines:** Pasig City Education Department Citizen's Charter5
- **Status:** Active1

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen3
- **Residency / Destination:** Bonafide resident of Pasig City5
- **Education Level:** Grade 11, Grade 12, College1
- **Eligible Year Levels:** SHS Grade 11–12 and College Years 1–41
- **Incoming Freshman Only:** No1
- **Existing College Students:** Yes1
- **Graduate Students:** No1
- **Current Enrollment:** Enrolled in a recognized secondary or tertiary institution5
- **Academic Requirements:** Minimum GWA of 80.00%1
- **Minimum GWA:** 80.00%1
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined gross annual family income not exceeding PHP 350,000.001
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Recognized public or private schools5
- **Course Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Sectoral / Hidden Requirements:** Endorsement from Pasig City Sports Development Office or verified athletic portfolio in recognized sports competitions5
- **Good Moral:** Certificate of Good Moral Character8
- **Health:** Physically fit to participate in athletic training and competition9
- **Other Official Rules / Conflicts:** One-Scholar-One-Family Policy applies6.

#### Timing
- **Who May Apply:** Student-athletes in SHS and College5
- **Freshmen:** : Yes1
- **Sophomores:** : Yes1
- **Juniors:** : Yes1
- **Seniors:** : Yes1
- **Graduates:** : No1
- **Reapply:** : Yes8
- **Opening:** August 1, 20251
- **Closing:** September 10, 20261
- **Cycle:** Annual1
- **AY Covered:** AY 2025–2026 / AY 2026–20271

#### Benefits (catalog)
- **Tuition:** Full or partial coverage up to city limit1
- **Monthly Stipend:** PHP 2,000.00 per month1
- **Allowance:** Total annual value of PHP 30,000.001
- **Return Service:** False1

#### Renewal
- **Maintain GWA:** 80.00%1
- **Regular Load:** Full-time student status5
- **No Failures:** Zero failing grades5

#### Disqualifying / Conflicts
- Absence of recognized athletic credentials or sports office endorsement5.
- Non-residency in Pasig City5.
- GWA dropping below 80.00%1.

#### Required Documents (hidden operational requirements)
- Printed Online Application Form5
- Barangay Certificate of Residency4
- Proof of Enrollment4
- Report of Grades / TOR showing GWA 80.00%1
- Parents' Proof of Income / Indigency Certificate4
- Athletic Portfolio / Certificates of Sports Medals & Awards / Endorsement from Sports Office9

#### Recommended Schema / Fields
```json
{ "education_level": ["Grade 11", "Grade 12", "College"], "eligible_year_levels": [11, 12, 1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 80.00, "income_limit": 350000, "residency_restriction": "PASIG_CITY", "athletic_qualification_required": true, "school_type": ["PUBLIC", "PRIVATE"], "application_window": {"open": "2025-08-01", "close": "2026-09-10"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Credentials Verification: Applicants uploading non-sanctioned sports certificates will be
- **Verification:** Verified1 | Confidence: 96/100

---

### Pasig City Out-of-School Learners (OSL) Scholarship Program5 (ID: 93)

#### Identity / Affiliations
- **Provider:** Pasig City Government (PCED-SAS)5
- **Category:** Local Government Unit / Need-based & Alternative Learning1
- **Website:** https://scholars.pasigcity.gov.ph1
- **Portal:** https://scholars.pasigcity.gov.ph1
- **Guidelines:** Pasig City Education Department Citizen's Charter5
- **Status:** Active1

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen3
- **Residency / Destination:** Bonafide resident of Pasig City5
- **Education Level:** TVET, College1
- **Eligible Year Levels:** Entry level and ongoing TVET / College years1
- **Incoming Freshman Only:** No1
- **Existing College Students:** Yes1
- **Graduate Students:** No1
- **Current Enrollment:** Enrolled or registered in a TVET center or college following ALS / OSL completion5
- **Academic Requirements:** ALS Completion Certificate or Presentation Portfolio Assessment Scoring Sheet with Passed Grade / Form 137 / AF-5 Permanent Record5
- **Minimum GWA:** 75.00% (passing equivalent)1
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined annual gross family income not exceeding PHP 200,000.001
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Accredited TVET centers, SUCs, LUCs, or partner private institutions5
- **Course Restrictions:** Technical-vocational skills courses and priority diploma degrees5
- **Sectoral / Hidden Requirements:** Out-of-school youth / ALS completer status verified by learning center5
- **Good Moral:** Certificate of Good Moral Character8
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** One-Scholar-One-Family Policy applies6.

#### Timing
- **Who May Apply:** Out-of-school learners and ALS completers entering TVET or College5
- **Freshmen:** : Yes1
- **Sophomores:** : Yes1
- **Juniors:** : Yes1
- **Seniors:** : Yes1
- **Graduates:** : No1
- **Reapply:** : Yes8
- **Opening:** August 1, 20251
- **Closing:** September 30, 20251
- **Cycle:** Annual1
- **AY Covered:** AY 2025–2026 / AY 2026–20271

#### Benefits (catalog)
- **Tuition:** Full tuition coverage for accredited TVET / tertiary programs1
- **Monthly Stipend:** PHP 2,500.00 per month1
- **Allowance:** Total annual value of PHP 35,000.001
- **Return Service:** False1

#### Renewal
- **Maintain GWA:** 75.00% (passing average)1
- **Regular Load:** Full load in TVET module or degree curriculum5
- **No Failures:** Zero dropped modules or failing subjects5

#### Disqualifying / Conflicts
- Regular formal school graduates who are not out-of-school youth or ALS completers5.
- Income exceeding PHP 200,000.001.
- Non-residency in Pasig City5.

#### Required Documents (hidden operational requirements)
- Printed Online Application Form5
- Barangay Certificate of Residency4
- ALS Completion Certificate / Presentation Portfolio Assessment Scoring Sheet with Passed Grade5
- Learner's Permanent Record (AF-5 or Form 137) from learning center5
- Proof of Income / Barangay Indigency Certificate4
- Proof of Enrollment in TVET / College4
- Certificate of Good Moral Character8

#### Recommended Schema / Fields
```json
{ "education_level": ["TVET", "College"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 75.00, "income_limit": 200000, "als_osl_status_required": true, "residency_restriction": "PASIG_CITY", "school_type": ["TVET_CENTER", "PUBLIC", "PRIVATE"], "application_window": {"open": "2025-08-01", "close": "2025-09-30"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Misclassification of Student Origin: Regular continuous high school graduates who apply
- **Verification:** Verified1 | Confidence: 92/100
- **Contradictions:**
  - Entry min_gwa (75.00% (passing equivalent)1) differs from renewal Maintain GWA (75.00% (passing average)1)

---

### Pasig City Sangguniang Kabataan (SK) Endorsed Scholarship Program5 (ID: 94)

#### Identity / Affiliations
- **Provider:** Pasig City Government (PCED-SAS in partnership with Barangay SK Councils)5
- **Category:** Local Government Unit / Youth Leadership & Affiliation1
- **Website:** https://scholars.pasigcity.gov.ph1
- **Portal:** https://scholars.pasigcity.gov.ph1
- **Guidelines:** Pasig City Education Department Citizen's Charter5
- **Status:** Active1

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen3
- **Residency / Destination:** Bonafide resident of Pasig City5
- **Education Level:** College1
- **Eligible Year Levels:** College Years 1, 2, 3, and 41
- **Incoming Freshman Only:** No1
- **Existing College Students:** Yes1
- **Graduate Students:** No1
- **Current Enrollment:** Enrolled in a recognized college or university5
- **Academic Requirements:** Minimum GWA of 82.00%1
- **Minimum GWA:** 82.00%1
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined family gross annual income not exceeding PHP 250,000.001
- **Age Restrictions:** Must meet SK youth age mandate (15–30 years old per SK Reform Act)5
- **School / Consortium Restrictions:** Recognized public or private HEIs5
- **Course Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Sectoral / Hidden Requirements:** Formal SK Endorsement Resolution / Certification signed by the Barangay SK Chairperson4
- **Good Moral:** Certificate of Good Moral Character8
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** One-Scholar-One-Family Policy applies6.

#### Timing
- **Who May Apply:** SK officials and SK-endorsed youth volunteers in Pasig City4
- **Freshmen:** : Yes1
- **Sophomores:** : Yes1
- **Juniors:** : Yes1
- **Seniors:** : Yes1
- **Graduates:** : No1
- **Reapply:** : Yes8
- **Opening:** August 1, 20251
- **Closing:** August 20, 20261
- **Cycle:** Annual1
- **AY Covered:** AY 2025–2026 / AY 2026–20271

#### Benefits (catalog)
- **Tuition:** False1
- **Monthly Stipend:** PHP 1,500.00 per month1
- **Allowance:** Total annual value of PHP 20,000.001
- **Return Service:** True (mandatory participation in Barangay SK youth projects)1

#### Renewal
- **Maintain GWA:** 82.00%1
- **Regular Load:** Full semestral unit load5
- **No Failures:** Zero failing grades5

#### Disqualifying / Conflicts
- Lack of official endorsement from the local Barangay SK Council4.
- Exceeding the SK youth age threshold (30 years old)5.
- Income exceeding PHP 250,000.001.

#### Required Documents (hidden operational requirements)
- Printed Online Application Form5
- Official Barangay SK Endorsement Certificate / Resolution4
- Barangay Certificate of Residency4
- Proof of Enrollment in College4
- College TOR or SHS Card showing GWA 82.00%1
- Proof of Income / Indigency Certificate4
- Certificate of Good Moral Character8

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 82.00, "income_limit": 250000, "sk_endorsement_required": true, "residency_restriction": "PASIG_CITY", "return_service_required": true, "school_type": ["PUBLIC", "PRIVATE"], "application_window": {"open": "2025-08-01", "close": "2026-08-20"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Endorsement Verification: Applications submitted without a signed SK Endorsement
- **Verification:** Verified1 | Confidence: 94/100

---

### Scholarship on Tertiary Education Program – Financial Assistance (STEP-FA) Category A1 (ID: 101)

#### Identity / Affiliations
- **Provider:** Davao City Government (Educational Benefit System Unit / EBSU)11
- **Category:** Local Government Unit / High Merit1
- **Website:** https://davaocity.gov.ph1
- **Portal:** https://ebsu-escholar.davaocity.gov.ph11
- **Guidelines:** Executive Order No. 7 s. 2014 / EBSU High Merit Rules11
- **Status:** Active1

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen3
- **Residency / Destination:** Resident of Davao City13
- **Education Level:** College1
- **Eligible Year Levels:** Years 1, 2, 3, and 41
- **Incoming Freshman Only:** No1
- **Existing College Students:** Yes12
- **Graduate Students:** No1
- **Current Enrollment:** Enrolled in a CHED-recognized HEI in Davao City13
- **Academic Requirements:** GWA of at least 93.00% with no failing marks12
- **Minimum GWA:** 93.00%1
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** PHP 250,000.00 annual family income; verified indigent/below-average income by CSWDO1
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Recognized HEIs operating within Davao City13
- **Course Restrictions:** CHED-prescribed priority courses13
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Certificate of Good Moral Character13
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Strict "One Child Per Family" rule13; candidate must not hold other government/private scholarship grants13.

#### Timing
- **Who May Apply:** Resident high-honor SHS graduates and ongoing college scholars12
- **Freshmen:** : Yes12
- **Sophomores:** : Yes12
- **Juniors:** : Yes12
- **Seniors:** : Yes12
- **Graduates:** : No1
- **Reapply:** : Yes13
- **Opening:** April 1 annually12
- **Closing:** May 31 annually12
- **Cycle:** Annual1
- **AY Covered:** AY 2025–2026 / AY 2026–202712

#### Benefits (catalog)
- **Tuition:** Full tuition coverage up to cap or direct cash grant1
- **Monthly Stipend:** PHP 3,000.00 per month1
- **Allowance:** PHP 25,000.00 per semester (PHP 50,000.00 per academic year)1
- **Return Service:** False1

#### Renewal
- **Maintain GWA:** 93.00%1
- **Regular Load:** Full semestral unit load13
- **No Failures:** Zero failing or incomplete grades13

#### Disqualifying / Conflicts
- GWA dropping below 93.00% (automatically downgrades scholar to Category B or C)12.
- Sibling already holding an EBSU grant13.
- Non-residency in Davao City13.

#### Required Documents (hidden operational requirements)
- EBSU eScholar Application Form11
- Barangay Certificate of Residency12
- CSWDO Indigency Certificate / Eligibility Certification12
- Parents' ITR or Tax Exemption Certificate12
- SHS Grade 12 Card or College TOR showing GWA 93.00%12
- Certificate of Good Moral Character12
- Sworn affidavit of no sibling benefiting from EBSU13

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 93.00, "income_limit": 250000, "residency_restriction": "DAVAO_CITY", "one_child_per_family_clause": true, "school_type": ["DAVAO_CITY_HEI"], "application_window": {"open": "04-01", "close": "05-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Strict Grade Demotion: Scholars whose GWA falls to 92.50% must be dynamically
- **Verification:** Verified1 | Confidence: 90/100

---

### Scholarship on Tertiary Education Program – Financial Assistance (STEP-FA) Category C1 (ID: 102)

#### Identity / Affiliations
- **Provider:** Davao City Government (EBSU)11
- **Category:** Local Government Unit / Need-based1
- **Website:** https://davaocity.gov.ph1
- **Portal:** https://ebsu-escholar.davaocity.gov.ph11
- **Guidelines:** Executive Order No. 7 s. 2014 / EBSU Need-Based Aid Rules11
- **Status:** Active1

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen3
- **Residency / Destination:** Resident of Davao City13
- **Education Level:** College1
- **Eligible Year Levels:** Years 1, 2, 3, and 41
- **Incoming Freshman Only:** No1
- **Existing College Students:** Yes12
- **Graduate Students:** No1
- **Current Enrollment:** Enrolled in a CHED-recognized HEI in Davao City13
- **Academic Requirements:** GWA of 80.00% to 89.99% with no failing marks12
- **Minimum GWA:** 80.00%1
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined family annual gross income not exceeding PHP 180,000.001
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Recognized HEIs operating within Davao City13
- **Course Restrictions:** CHED-prescribed priority degree courses13
- **Sectoral / Hidden Requirements:** Verified indigency status by CSWDO12
- **Good Moral:** Certificate of Good Moral Character13
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Strict "One Child Per Family" rule13; candidate must not hold duplicate government/private scholarship grants13.

#### Timing
- **Who May Apply:** Indigent resident college students in Davao City12
- **Freshmen:** : Yes12
- **Sophomores:** : Yes12
- **Juniors:** : Yes12
- **Seniors:** : Yes12
- **Graduates:** : No1
- **Reapply:** : Yes13
- **Opening:** April 1 annually12
- **Closing:** May 31 annually12
- **Cycle:** Annual1
- **AY Covered:** AY 2025–2026 / AY 2026–202712

#### Benefits (catalog)
- **Tuition:** False1
- **Monthly Stipend:** PHP 1,000.00 per month1
- **Allowance:** PHP 7,500.00 per semester (PHP 15,000.00 per academic year)1
- **Return Service:** False1

#### Renewal
- **Maintain GWA:** 80.00%1
- **Regular Load:** Full semestral unit load13
- **No Failures:** Zero failing marks13

#### Disqualifying / Conflicts
- Family gross income exceeding PHP 180,000.001.
- Sibling already enjoying an EBSU scholarship13.
- Presence of failing or incomplete grades13.

#### Required Documents (hidden operational requirements)
- EBSU eScholar Application Form11
- Certificate of Residency from Barangay12
- CSWDO Indigency Certificate12
- Parents' ITR or Tax Exemption Certificate ( PHP 180,000)1
- SHS Grade 12 Card or College TOR showing GWA 80%–89.99%12
- Certificate of Good Moral Character12
- Sworn affidavit of no sibling enjoying EBSU grants13

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 80.00, "maximum_gwa_cap": 89.99, "income_limit": 180000, "residency_restriction": "DAVAO_CITY", "one_child_per_family_clause": true, "school_type": ["DAVAO_CITY_HEI"], "application_window": {"open": "04-01", "close": "05-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Grade Upgrade Potential: Applicants attaining a GWA
- **Verification:** Verified1 | Confidence: n/a

---

### Medical and Law Education Assistance Program1 (ID: 103)

#### Identity / Affiliations
- **Provider:** Davao City Government (EBSU)11
- **Category:** Local Government Unit / Graduate Professional (Medicine & Law)1
- **Website:** https://davaocity.gov.ph1
- **Portal:** https://ebsu-escholar.davaocity.gov.ph11
- **Guidelines:** Executive Order No. 7 s. 2014 / EBSU Med-Law Rules11
- **Status:** Active1

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen3
- **Residency / Destination:** Bonafide resident of Davao City13
- **Education Level:** Graduate (Doctor of Medicine or Juris Doctor)1
- **Eligible Year Levels:** Medical/Law Years 1, 2, 3, and 41
- **Incoming Freshman Only:** No13
- **Existing College Students:** Yes (as professional medical/law students)13
- **Graduate Students:** Yes1
- **Current Enrollment:** Accepted or enrolled in a Davao City-based medical or law school13
- **Academic Requirements:** Incoming 1st Year: Bachelor's degree average grade of at least 85.00% with no grade below 75.00% in any subject; Ongoing (2nd–4th Year): Average grade of at least 77.00% (or 85.00% per updated EBSU release) with no grade below 75.00% in preceding year level12
- **Minimum GWA:** 85.00%1
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined family gross annual income not exceeding PHP 500,000.00; Statement of Assets, Liabilities, and Net Worth (SALN) if parent is in government1
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Restricted exclusively to Davao City-based medical and law schools13
- **Course Restrictions:** Doctor of Medicine, Juris Doctor (Law)11
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Certificate of Good Moral Character13
- **Health:** Medical Certificate issued by a government hospital confirming physical and mental fitness13
- **Other Official Rules / Conflicts:** Certification from school confirming no other active scholarship grant13; Sworn statement of no parent or sibling as an active city scholar13; Mandatory return service obligation in Davao City1.

#### Timing
- **Who May Apply:** Bachelor's degree graduates entering 1st year medical/law school and ongoing medical/law students in Davao City12
- **Freshmen:** : Yes (as incoming 1st year med/law students)13
- **Sophomores:** : Yes13
- **Juniors:** : Yes13
- **Seniors:** : Yes13
- **Graduates:** : Yes (Bachelor's graduates entering professional school)13
- **Reapply:** : Yes13
- **Opening:** April 1 annually12
- **Closing:** May 31 annually12
- **Cycle:** Annual1
- **AY Covered:** AY 2025–2026 / AY 2026–202712

#### Benefits (catalog)
- **Tuition:** Full tuition and matriculation fee coverage at partner school1
- **Monthly Stipend:** PHP 4,000.00 per month1
- **Allowance:** Total annual value up to PHP 100,000.001
- **Return Service:** True (mandatory return service in Davao City public health facilities or legal offices)1

#### Renewal
- **Maintain GWA:** 77.00%–85.00% depending on professional year level12
- **Regular Load:** Full load in medical or law curriculum13
- **No Failures:** No grade below 75.00% in any subject12

#### Disqualifying / Conflicts
- Enrolling in medical or law schools outside Davao City13.
- Failing grade ( ) in any subject during undergraduate or professional study12.
- Dual scholarship holding13.

#### Required Documents (hidden operational requirements)
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

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 85.00, "income_limit": 500000, "priority_courses": ["DOCTOR_OF_MEDICINE", "JURIS_DOCTOR"], "residency_restriction": "DAVAO_CITY", "return_service_required": true, "school_type": ["DAVAO_CITY_MED_LAW_SCHOOL"], "partner_school_restricted": true, "application_window": {"open": "04-01", "close": "05-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● School Location Failure: Applicants admitted to medical/law schools outside Davao City
- **Verification:** Verified1 | Confidence: 98/100
- **Contradictions:**
  - Entry min_gwa (85.00%1) differs from renewal Maintain GWA (77.00%–85.00% depending on professional year level12)

---

## SOURCE: `DATABASE_V3_GROUPC_OTHER_GOVERNMENT.pdf`

**Scholarships in this PDF:** 15

### Senior High School Voucher Program (SHS VP)3 (ID: 17)

#### Identity / Affiliations
- **Provider:** Department of Education (DepEd) in partnership with the Private Education Assistance Committee (PEAC)3
- **Category:** Government / Basic Education Financial Assistance / Grant3
- **Website:** https://deped.gov.ph5, https://ovp.peac.org.ph3
- **Portal:** https://ovap.deped.gov.ph5
- **Guidelines:** DepEd Order No. 11, s. 2015; DepEd Order No. 46, s. 2015; DepEd Order No. 60, s. 2017; DepEd Order No. 16, s. 20203
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen5.
- **Residency / Destination:** Resident of the Philippines5.
- **Education Level:** Senior High School (Grades 11 and 12)4.
- **Eligible Year Levels:** Grade 11 (Initial redemption occurs upon entry into Grade 11)4.
- **Incoming Freshman Only:** Yes (Applicable to incoming Grade 11 SHS students)4.
- **Existing College Students:** Ineligible4.
- **Graduate Students:** Ineligible4.
- **Current Enrollment:** Must be enrolled or accepted in a non-DepEd VP-participating Senior High School3.
- **Academic Requirements:** Successful completion of Grade 10 Junior High School (JHS)4.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Passing Grade 10 completion is required)4.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE5.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE (Grade 10 completers from public JHSs and private JHS Educational Service Contracting [ESC] grantees are automatically qualified regardless of income; non-ESC private applicants undergo online screening subject to national budget allocations)5.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE5.
- **School / Consortium Restrictions:** Restricted to VP-participating non-DepEd Senior High Schools (Private SHSs, SUCs, and LUCs)3.
- **Course Restrictions:** All DepEd-approved SHS Tracks and Strands (Academic, Technical-Vocational-Livelihood [TVL], Sports, Arts and Design)4.
- **Sectoral / Hidden Requirements:** None5.
- **Good Moral:** Certificate of Good Moral Character issued by the originating Junior High School4.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Automatically Qualified Voucher Recipients (QVRs) include Grade 10 completers from Public JHSs, SUC/LUC JHSs, and ESC grantees in Private JHSs5. Non-ESC private JHS completers must apply online via the Online Voucher Application Portal (OVAP)5. Vouchers are non-cashable grants disbursed directly to participating host schools via Land Bank of the Philippines accounts4.

#### Timing
- **Who May Apply:** Non-ESC Grade 10 completers from private junior high schools, and learners who completed JHS prior to the current school year re-entering basic education5.
- **Freshmen:** : Yes (Incoming Grade 11 SHS students)4.
- **Sophomores:** : No (Grade 12 voucher renewal is automatic for Grade
- **Juniors:** : No4.
- **Seniors:** : No4.
- **Graduates:** : No4.
- **Reapply:** : No4.
- **Opening:** Announced annually via DepEd Order (typically opens between October and January)5.
- **Closing:** Specified in the annual policy guidelines (typically February 28 for online submissions)5.
- **Cycle:** Fixed / Annual5.
- **AY Covered:** AY 2025–2026 / AY 2026–20275.

#### Benefits (catalog)
- **Tuition:** Voucher subsidy disbursed directly to host school (NCR Private SHS: up to ₱22,500/year; NCR SUC/LUC SHS: ₱17,500/year; Non-NCR Private SHS: up to ₱17,500/year; Non-NCR SUC/LUC SHS: ₱14,000/year)4.
- **Monthly Stipend:** None (Direct tuition voucher)5.
- **Allowance:** None9.
- **Return Service:** None4.

#### Renewal
- **Maintain GWA:** Promoted to Grade 12 in accordance with DepEd academic progression standards4.
- **Regular Load:** Continuous full-time enrollment in the elected SHS track4.
- **No Failures:** Passing grades across all enrolled SHS subjects4.

#### Disqualifying / Conflicts
- Dropping out of Senior High School in the middle of an academic year4.
- Transferring to a DepEd Public Senior High School4.
- Failing Grade 11 or retaining Grade 11 academic status4.
- Transferring to a non-participating private Senior High School3.

#### Required Documents (hidden operational requirements)
- PSA Certified Birth Certificate4.
- Grade 10 Report Card (Form 138 / SF9) showing Learner Reference Number (LRN)4.
- Certificate of Junior High School Completion4.
- Certificate of Good Moral Character signed by JHS Principal4.
- ESC Certification Letter issued by JHS Principal via ESC IMS (for ESC grantees) or Qualified Voucher Applicant (QVA) Certificate (for online applicants)4.

#### Recommended Schema / Fields
```json
{ "education_level": ["Senior High School"], "eligible_year_levels": [11], "incoming_year_only": true, "requires_current_enrollment": true, "minimum_gwa": null, "income_limit": null, "school_type": ["Private SHS", "SUCSHS", "LUCSHS"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "10-01", "close": "02-28"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Income Parameter Misconfiguration: The live database export records max_income:
- **Verification:** Verified3. | Confidence: n/a
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Passing Grade 10 completion is required)4.) differs from renewal Maintain GWA (Promoted to Grade 12 in accordance with DepEd academic progression standards4.)

---

### Energy Regulatory Commission Graduate Fellowship Program9 (ID: 20)

#### Identity / Affiliations
- **Provider:** Energy Regulatory Commission (ERC)9
- **Category:** Government / Graduate Fellowship / Institutional9
- **Website:** https://erc.gov.ph9
- **Portal:** https://erc.gov.ph9
- **Guidelines:** ERC Fellowship Program Guidelines9
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Natural-born Filipino citizen9.
- **Residency / Destination:** Resident of the Philippines9.
- **Education Level:** Graduate (Master's or Doctorate)9.
- **Eligible Year Levels:** 1st Year Master's or Doctoral students9.
- **Incoming Freshman Only:** No9.
- **Existing College Students:** Ineligible (Restricted to post-baccalaureate graduate students)9.
- **Graduate Students:** Yes9.
- **Current Enrollment:** Accepted or enrolled in a graduate degree program in energy regulation, power engineering, or energy economics at an accredited university9.
- **Academic Requirements:** Undergraduate General Weighted Average (GWA) of at least 88.00% or equivalent9.
- **Minimum GWA:** 88.00%9.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE9.
- **Income Ceilings:** Combined gross annual family income must not exceed ₱500,000.009.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE9.
- **School / Consortium Restrictions:** CHED-accredited universities offering recognized graduate programs in law, economics, or engineering9.
- **Course Restrictions:** Energy Law, Energy Economics, Power Engineering, Public Policy9.
- **Sectoral / Hidden Requirements:** None9.
- **Good Moral:** Required9.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Must pass the ERC interview and selection board evaluation9.

#### Timing
- **Who May Apply:** Qualified Bachelor's degree graduates entering or pursuing graduate studies in priority energy disciplines9.
- **Freshmen:** : No (Undergraduate freshmen barred)9.
- **Sophomores:** : No9.
- **Juniors:** : No9.
- **Seniors:** : No9.
- **Graduates:** : Yes (Primary eligible cohort)9.
- **Reapply:** : Yes9.
- **Opening:** Announced annually per ERC official advisory9.
- **Closing:** Specified in the annual Call for Candidates9.
- **Cycle:** Annual9.
- **AY Covered:** AY 2025–2026 / AY 2026–20279.

#### Benefits (catalog)
- **Tuition:** Full tuition and matriculation fee coverage9.
- **Monthly Stipend:** ₱12,000.00 per month9.
- **Allowance:** Integrated into monthly stipend9.
- **Return Service:** NOT SPECIFIED IN OFFICIAL SOURCE9.

#### Renewal
- **Maintain GWA:** Maintain graduate academic retention GWA specified by ERC (minimum 88.00% or university passing equivalent)9.
- **Regular Load:** Enrolled in required graduate unit load per semester9.
- **No Failures:** Zero failing or incomplete marks in graduate coursework9.

#### Disqualifying / Conflicts
- Undergraduate enrollment status9.
- Combined family gross annual income exceeding ₱500,000.009.
- Undergraduate GWA dropping below 88.00%9.
- Employment in conflicting energy sector enterprises violating regulatory ethics rules9.

#### Required Documents (hidden operational requirements)
- Official Graduate Fellowship Application Form9.
- Official Transcript of Records (TOR) from Bachelor's degree showing GWA >= 88.00%9.
- Proof of Admission / Enrollment in an approved graduate program9.
- BIR Income Tax Return or Tax Exemption Certificate (Income <= ₱500,000.00)9.
- Certificate of Good Moral Character9.

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1, 2], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 88.00, "income_limit": 500000, "school_type": ["CHED_RECOGNIZED_HEI"], "partner_school_restricted": false, "citizenship": "Filipino", "application_window": {"open": "annual_notice", "close": "annual_notice"}, "deadline_type": "estimated", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Academic Level Misclassification: Displaying ID 20 to college undergraduate candidates
- **Verification:** Partially Verified9. | Confidence: 95/100.
- **Contradictions:**
  - Entry min_gwa (88.00%9.) differs from renewal Maintain GWA (Maintain graduate academic retention GWA specified by ERC (minimum 88.00% or university passing equivalent)9.)

---

### NCIP Educational Assistance Program (EAP) – Degree Track10 (ID: 52)

#### Identity / Affiliations
- **Provider:** National Commission on Indigenous Peoples (NCIP)10
- **Category:** Government / Need-and-Sectoral / Tribal10
- **Website:** https://ncip.gov.ph12, https://eais.ncip.gov.ph10
- **Portal:** https://eais.ncip.gov.ph10
- **Guidelines:** NCIP Administrative Order No. 1, s. 2022; Indigenous Peoples Education and Advocacy Services (IPEAS) Guidelines10
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen10.
- **Residency / Destination:** Resident member of a recognized Indigenous Cultural Community / Ancestral Domain10.
- **Education Level:** College / Undergraduate9.
- **Eligible Year Levels:** 1st, 2nd, 3rd, 4th, and 5th Year14.
- **Incoming Freshman Only:** No14.
- **Existing College Students:** Yes14.
- **Graduate Students:** Ineligible under the Degree Track (Covered under separate post-graduate assistance provisions)14.
- **Current Enrollment:** Enrolled or accepted in a State College or University (SUC) or CHED-recognized HEI14.
- **Academic Requirements:** Must maintain a General Weighted Average (GWA) of at least 80.00% per semester14.
- **Minimum GWA:** 80.00%14.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE10.
- **Income Ceilings:** Combined family annual gross income must not exceed ₱200,000.009.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE10.
- **School / Consortium Restrictions:** State Universities and Colleges (SUCs) nearest to the applicant's ancestral domain residence are prioritized14.
- **Course Restrictions:** Degree programs aligned with Ancestral Domain Sustainable Development and Protection Plans (ADSDPP)14.
- **Sectoral / Hidden Requirements:** Must submit an official Certificate of Confirmation (COC) issued by NCIP attesting to genuine IP tribal membership10.
- **Good Moral:** Required10.
- **Health:** Physically and mentally fit to pursue higher education14.
- **Other Official Rules / Conflicts:** Enrolled in a minimum load of 18 units per semester unless in graduating status14. Dual enjoyment of major government scholarship grants is prohibited14.

#### Timing
- **Who May Apply:** Qualified IP college students (incoming freshmen and ongoing upperclassmen)10.
- **Freshmen:** : Yes14.
- **Sophomores:** : Yes14.
- **Juniors:** : Yes14.
- **Seniors:** : Yes14.
- **Graduates:** : No14.
- **Reapply:** : Yes14.
- **Opening:** June 1 annually (via EAIS portal)9.
- **Closing:** August 15 annually9.
- **Cycle:** Fixed / Annual9.
- **AY Covered:** AY 2025–2026 / AY 2026–20279.

#### Benefits (catalog)
- **Tuition:** Covered via SUC Free Higher Education or subsidized through the IP Education Allowance14.
- **Monthly Stipend:** Integrated into the annual educational allowance14.
- **Allowance:** ₱20,000.00 per Academic Year (disbursed semestrally at ₱10,000.00 per semester)14.
- **Return Service:** Mandatory service in the scholar's home IP community for a duration equal to the scholarship years enjoyed, or book donation to a community library14.

#### Renewal
- **Maintain GWA:** Maintain a semester GWA of at least 80.00%14.
- **Regular Load:** Minimum enrollment of 18 units per semester14.
- **No Failures:** Zero failing, incomplete, or dropped subjects14.

#### Disqualifying / Conflicts
- Falsification or tampering of NCIP COC or academic records14.
- Semester GWA dropping below 80.00%14.
- Concurrent enjoyment of another major national government scholarship14.
- Unapproved shiftee or transferee status14.
- Dropping below 18 units without prior NCIP approval14.

#### Required Documents (hidden operational requirements)
- Official Certificate of Confirmation (COC) on Tribe Membership issued by NCIP10.
- Accomplished EAIS Online Application Form10.
- Form 138 / SF9 Report Card (for Freshmen) or Official Transcript of Records / Certificate of Grades (for Upperclassmen) showing GWA >= 80.00%10.
- Certificate of Enrollment / Registration Form showing at least 18 enrolled units14.
- BIR Tax Exemption Certificate, ITR, or Barangay Certificate of Indigency11.
- Certificate of Good Moral Character10.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 80.00, "income_limit": 200000, "sectoral_restriction": "NCIP_CERTIFIED_INDIGENOUS_PEOPLE", "school_type": ["SUC", "LUC", "PRIVATE_HEI"], "partner_school_restricted": false, "citizenship": "Filipino", "application_window": {"open": "06-01", "close": "08-15"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "return_service_required": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Database GWA Discrepancy: The live database export records min_gwa: 75 for ID 529.
- **Verification:** Verified10. | Confidence: 75/1009.
- **Contradictions:**
  - Entry min_gwa (80.00%14.) differs from renewal Maintain GWA (Maintain a semester GWA of at least 80.00%14.)

---

### NCIP Merit-Based Scholarship Program (MBSP)10 (ID: 53)

#### Identity / Affiliations
- **Provider:** National Commission on Indigenous Peoples (NCIP)10
- **Category:** Government / Merit-and-Sectoral / Tribal10
- **Website:** https://ncip.gov.ph12, https://eais.ncip.gov.ph10
- **Portal:** https://eais.ncip.gov.ph10
- **Guidelines:** NCIP Administrative Order No. 1, s. 2022; IPEAS Guidelines10
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen10.
- **Residency / Destination:** Resident member of an Indigenous Cultural Community10.
- **Education Level:** College / Undergraduate9.
- **Eligible Year Levels:** 1st, 2nd, 3rd, 4th, and 5th Year14.
- **Incoming Freshman Only:** No14.
- **Existing College Students:** Yes14.
- **Graduate Students:** Ineligible under MBSP undergraduate track14.
- **Current Enrollment:** Enrolled or accepted in an SUC or recognized HEI14.
- **Academic Requirements:** General Weighted Average (GWA) of at least 85.00% per semester14.
- **Minimum GWA:** 85.00%14.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE10.
- **Income Ceilings:** Combined family gross annual income must not exceed ₱300,000.009.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE10.
- **School / Consortium Restrictions:** SUCs or top accredited private HEIs14.
- **Course Restrictions:** ADSDPP community priority courses and CHED priority fields14.
- **Sectoral / Hidden Requirements:** Must hold an official NCIP Certificate of Confirmation (COC)10.
- **Good Moral:** Required10.
- **Health:** Physically and mentally fit14.
- **Other Official Rules / Conflicts:** Enrolled in full semester load (at least 18 units)14.

#### Timing
- **Who May Apply:** Academically qualified IP college students10.
- **Freshmen:** : Yes14.
- **Sophomores:** : Yes14.
- **Juniors:** : Yes14.
- **Seniors:** : Yes14.
- **Graduates:** : No14.
- **Reapply:** : Yes14.
- **Opening:** June 1 annually9.
- **Closing:** August 15 annually9.
- **Cycle:** Annual9.
- **AY Covered:** AY 2025–2026 / AY 2026–20279.

#### Benefits (catalog)
- **Tuition:** Full tuition and matriculation fees covered14.
- **Monthly Stipend:** Integrated into the annual merit grant package14.
- **Allowance:** ₱50,000.00 per Academic Year (disbursed semestrally at ₱25,000.00 per semester)14.
- **Return Service:** Mandatory service in the scholar's home IP community equal to award duration14.

#### Renewal
- **Maintain GWA:** Must maintain a semester GWA of at least 85.00%14.
- **Regular Load:** Enrolled in at least 18 units per semester14.
- **No Failures:** Zero failing or incomplete grades14.

#### Disqualifying / Conflicts
- GWA falling below 85.00%14.
- Dual enjoyment of another major national government scholarship14.
- Falsification of IP certification documents14.
- Unapproved transfer of school or course14.

#### Required Documents (hidden operational requirements)
- Official NCIP Certificate of Confirmation (COC)10.
- Accomplished EAIS Online Application Form10.
- Form 138 / TOR showing GWA >= 85.00% with zero failing grades10.
- Certificate of Enrollment showing at least 18 enrolled units14.
- BIR Income Tax Return or Tax Exemption Certificate (Income <= ₱300,000.00)9.
- Certificate of Good Moral Character10.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 85.00, "income_limit": 300000, "sectoral_restriction": "NCIP_CERTIFIED_INDIGENOUS_PEOPLE", "school_type": ["SUC", "LUC", "PRIVATE_HEI"], "partner_school_restricted": false, "citizenship": "Filipino", "application_window": {"open": "06-01", "close": "08-15"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "return_service_required": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Benefit Value Misalignment: The live database export records total_value: 30000 for ID
- **Verification:** Verified10. | Confidence: 94/100.
- **Contradictions:**
  - Entry min_gwa (85.00%14.) differs from renewal Maintain GWA (Must maintain a semester GWA of at least 85.00%14.)

---

### Agricultural Competitiveness Enhancement Fund – Grants-in-Aid Higher Education Program (ACEF-GIAHEP) SUC Track16 (ID: 55)

#### Identity / Affiliations
- **Provider:** Department of Agriculture (DA) in coordination with CHED16
- **Category:** Government / Need-and-Sectoral / Agriculture16
- **Website:** https://da.gov.ph9
- **Portal:** Integrated via participating State Universities and Colleges (SUCs) and DA Regional Field Offices16.
- **Guidelines:** DA-CHED Joint Memorandum Circular No. 2, s. 2024; Republic Act No. 10848 (ACEF Law)16
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen16.
- **Residency / Destination:** Resident of the Philippines16.
- **Education Level:** College / Undergraduate9.
- **Eligible Year Levels:** Freshmen and ongoing undergraduate students (Years 1 to 4/5)16.
- **Incoming Freshman Only:** No16.
- **Existing College Students:** Yes16.
- **Graduate Students:** Ineligible16.
- **Current Enrollment:** Enrolled in an eligible agriculture-related degree program at a participating SUC16.
- **Academic Requirements:** Minimum GWA of 75.00% or passing academic grade9.
- **Minimum GWA:** 75.00%9.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** Combined gross annual income of parents must not exceed ₱200,000.009.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to State Universities and Colleges (SUCs)16.
- **Course Restrictions:** Agriculture, Agricultural Engineering, Agribusiness, Forestry, Fisheries, Veterinary Medicine16.
- **Sectoral / Hidden Requirements:** Parent must be a registered small farmer or fisherfolk listed in the Registry System for Basic Sectors in Agriculture (RSBSA) or certified by DA/LGU16.
- **Good Moral:** Required.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Cannot enjoy another government scholarship covering the same expenditure items16.

#### Timing
- **Who May Apply:** Children of RSBSA-registered small farmers and fisherfolk entering or enrolled in SUC agriculture programs16.
- **Freshmen:** : Yes16.
- **Sophomores:** : Yes16.
- **Juniors:** : Yes16.
- **Seniors:** : Yes16.
- **Graduates:** : No16.
- **Reapply:** : Yes16.
- **Opening:** Announced per academic cycle16.
- **Closing:** August 15 annually9.
- **Cycle:** Annual9.
- **AY Covered:** AY 2025–2026 / AY 2026–20279.

#### Benefits (catalog)
- **Tuition:** Covered by SUC Free Higher Education or subsidized16.
- **Monthly Stipend:** Integrated into semestral grant9.
- **Allowance:** ₱30,000.00 per Academic Year (₱15,000.00 per semester)9.
- **Return Service:** None9.

#### Renewal
- **Maintain GWA:** Maintain passing academic GWA per semester (75.00% or SUC retention passing mark)9.
- **Regular Load:** Full credit load per term16.
- **No Failures:** Compliance with SUC retention rules16.

#### Disqualifying / Conflicts
- Parent not registered in RSBSA or non-farming status16.
- Combined family annual income exceeding ₱200,000.009.
- Enrollment in non-agriculture degrees or private HEIs16.
- Academic failure or dismissal from SUC16.

#### Required Documents (hidden operational requirements)
- Proof of RSBSA Registration or DA/LGU Agriculture Office Certification of parent16.
- PSA Birth Certificate of applicant16.
- Form 138 / SF9 Report Card or TOR showing passing GWA >= 75.00%9.
- BIR Tax Exemption Certificate or ITR showing family income <= ₱200,000.009.
- Certificate of Enrollment in an approved SUC agriculture degree program16.
- Certificate of Good Moral Character.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 75.00, "income_limit": 200000, "sectoral_restriction": "RSBSA_REGISTERED_FARMER_FISHERFOLK_DEPENDENT", "priority_courses": ["AGRICULTURE", "AGRICULTURAL_ENGINEERING", "FORESTRY", "FISHERIES", "VETERINARY_MEDICINE"], "school_type": ["SUC"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "06-01", "close": "08-15"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Missing RSBSA Sectoral Filter: System must check user.is_rsbsa_dependent == true.
- **Verification:** Verified16. | Confidence: 94/100.
- **Contradictions:**
  - Entry min_gwa (75.00%9.) differs from renewal Maintain GWA (Maintain passing academic GWA per semester (75.00% or SUC retention passing mark)9.)

---

### DND-CHED-PASUC Scholarship Program17 (ID: 56)

#### Identity / Affiliations
- **Provider:** Armed Forces of the Philippines Educational Benefit System Office (AFPEBSO), Department of National Defense (DND), CHED, PASUC17
- **Category:** Government / Military Dependent / Affiliation17
- **Website:** https://afpebs.ph, https://www.afp.mil.ph9
- **Portal:** AFPEBSO Central Office & Regional AFPEBSO Offices17.
- **Guidelines:** CHED Memorandum Order (CMO) No. 22, s. 2004 (IRR of DND-CHED-PASUC Scholarship Program signed March 22, 2004)17
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Natural-born Filipino citizen17.
- **Residency / Destination:** Resident of the Philippines17.
- **Education Level:** College / Undergraduate (Baccalaureate degrees only; post-graduate excluded)17.
- **Eligible Year Levels:** 1st, 2nd, 3rd, 4th, and 5th Year17.
- **Incoming Freshman Only:** No17.
- **Existing College Students:** Yes17.
- **Graduate Students:** Ineligible17.
- **Current Enrollment:** Admitted or enrolled in a State University or College (SUC)17.
- **Academic Requirements:** Minimum GWA of 80.00% or compliance with host SUC admission standards9.
- **Minimum GWA:** 80.00%9.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE (Selection prioritized by military operational causality status: KIA/CDD-CR first, active personnel second)17.
- **Age Restrictions:** Dependent child must be below 21 years of age at the beginning of the school year17.
- **School / Consortium Restrictions:** Restricted strictly to State Universities and Colleges (SUCs)17.
- **Course Restrictions:** Any baccalaureate degree course offered by SUCs17.
- **Sectoral / Hidden Requirements:** Must be a legitimate child of active, KIA, or CDD-CR AFP military personnel17.
- **Good Moral:** Required17.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** National quota of 200 scholarship slots17. Candidates must satisfy SUC admission standards on or before April 1017. Must sign AFPEBSO Certificate of Undertaking17. Unapproved transfer between SUCs or leaves of absence strictly prohibited17.

#### Timing
- **Who May Apply:** Dependents of KIA, CDD-CR, or active military personnel under 21 years old17.
- **Freshmen:** : Yes17.
- **Sophomores:** : Yes17.
- **Juniors:** : Yes17.
- **Seniors:** : Yes17.
- **Graduates:** : No17.
- **Reapply:** : Yes17.
- **Opening:** Annual application processing opens early in the calendar year17.
- **Closing:** April 20 annually for document processing; Central Scholarship Board confirmation before May 1517.
- **Cycle:** Annual17.
- **AY Covered:** AY 2025–2026 / AY 2026–20279.

#### Benefits (catalog)
- **Tuition:** 100% Tuition fee waiver covered by the host State University or College (SUC) for the entire course duration17.
- **Monthly Stipend:** Integrated into AFPEBSO annual stipend17.
- **Allowance:** AFPEBSO provides direct scholar stipend of ₱8,000.00 annually (₱4,000.00 per semester)17.
- **Return Service:** None9.

#### Renewal
- **Maintain GWA:** Maintain passing GWA per SUC academic retention rules (minimum 80.00%)9.
- **Regular Load:** Enrolled in full-time baccalaureate curriculum load17.
- **No Failures:** Zero failing marks17.

#### Disqualifying / Conflicts
- Dependent age reaching or exceeding 21 years old at the start of the SY17.
- Unapproved transfer to another HEI or taking leave of absence without CSB approval17.
- Academic failure or dismissal from host SUC17.
- Enrollment in private universities or post-graduate degree programs17.

#### Required Documents (hidden operational requirements)
- Duly accomplished AFPEBSO Application Form with two 2x2 photos17.
- Letter of Recommendation from DND-CHED-PASUC Central Scholarship Board17.
- Military Service Record of parent / Casualty Report (KIA or CDD-CR Order) issued by OTAG AFP17.
- PSA Marriage Certificate of parents and PSA Birth Certificate of applicant17.
- Transcript of Records / Report Card showing GWA >= 80.00%9.
- Certificate of Good Moral Character17.
- Signed AFPEBSO Certificate of Undertaking17.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 80.00, "age_limit": 20, "parent_employment_restriction": "AFP_MILITARY_PERSONNEL_KIA_CDDCR_ACTIVE", "school_type": ["SUC"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "01-15", "close": "04-20"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Age Limit Omission: System must enforce user.age < 21 at the start of the academic
- **Verification:** Verified17. | Confidence: 92/100.
- **Contradictions:**
  - Entry min_gwa (80.00%9.) differs from renewal Maintain GWA (Maintain passing GWA per SUC academic retention rules (minimum 80.00%)9.)

---

### DSWD Assistance to Individuals in Crisis Situations (AICS) Educational Assistance19 (ID: 57)

#### Identity / Affiliations
- **Provider:** Department of Social Welfare and Development (DSWD)19
- **Category:** Government / Emergency Financial Aid / Social Protection19
- **Website:** https://www.dswd.gov.ph9
- **Portal:** DSWD Regional Field Offices and Community Crisis Intervention Sections (CIS)19.
- **Guidelines:** DSWD Memorandum Circular No. 21, Series of 201919
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen19.
- **Residency / Destination:** Resident of the Philippines (verified via Barangay Certificate of Indigency / Residency)19.
- **Education Level:** Grade 11, Grade 12, College / TVET, Graduate9.
- **Eligible Year Levels:** All year levels across secondary, tertiary, and vocational tracks9.
- **Incoming Freshman Only:** No9.
- **Existing College Students:** Yes9.
- **Graduate Students:** Eligible if in verified crisis9.
- **Current Enrollment:** Enrolled in a recognized educational institution19.
- **Academic Requirements:** Active student status19.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (No academic grade cutoff imposed; crisis evaluation prioritized)9.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** Combined family income within low-income / poverty threshold levels (₱150,000.00 cap in live DB export)9.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** None (Public or Private recognized institutions)19.
- **Course Restrictions:** Any course or field of study19.
- **Sectoral / Hidden Requirements:** Target crisis categories: Breadwinner deceased, incapacitated, unemployed, or displaced; child of solo parent; child of OFW in distress; 4Ps beneficiary19.
- **Good Moral:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Evaluated via DSWD Social Worker Case Assessment19. Grant provided as a one-time emergency assistance per academic year / crisis event19.

#### Timing
- **Who May Apply:** Students in crisis or financially distressed breadwinners19.
- **Freshmen:** : Yes9.
- **Sophomores:** : Yes9.
- **Juniors:** : Yes9.
- **Seniors:** : Yes9.
- **Graduates:** : Yes9.
- **Reapply:** : Yes (Subject to DSWD crisis re-evaluation guidelines)19.
- **Opening:** Year-round / Rolling intake9.
- **Closing:** December 31 annually (or subject to annual budget allocation)9.
- **Cycle:** Rolling / Emergency assistance9.
- **AY Covered:** AY 2025–2026 / AY 2026–20279.

#### Benefits (catalog)
- **Tuition:** None (Direct cash financial assistance paid to client)19.
- **Monthly Stipend:** None19.
- **Allowance:** Outright cash assistance grant up to ₱4,000.00 max depending on level (College/Vocational/Graduate: up to ₱4,000.00; SHS: up to ₱3,000.00; JHS: up to ₱2,000.00; Elementary: up to ₱1,000.00)9.
- **Return Service:** None9.

#### Renewal
- **Maintain GWA:** None (One-time assistance per crisis evaluation)19.
- **Regular Load:** Active enrollment19.

#### Disqualifying / Conflicts
- Non-indigent status or family income exceeding threshold19.
- Falsification of crisis documents or barangay indigency certificates19.
- Failure to pass DSWD social work case interview19.

#### Required Documents (hidden operational requirements)
- Certificate of Enrollment / Registration Form or School ID19.
- Barangay Certificate of Indigency / Residency19.
- Valid Government ID of applicant or parent/guardian19.
- DSWD Social Worker Intake and Assessment Sheet19.
- Specific Crisis Proof (Death Certificate of breadwinner, Medical Certificate, Notice of Termination, OFW Distress Report)19.

#### Recommended Schema / Fields
```json
{ "education_level": ["Senior High School", "College", "TVET", "Graduate"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": null, "income_limit": 150000, "is_emergency_grant": true, "school_type": ["RECOGNIZED_EDUCATIONAL_INSTITUTION"], "partner_school_restricted": false, "citizenship": "Filipino", "application_window": {"open": "01-01", "close": "12-31"}, "deadline_type": "rolling", "cycle_type": "rolling", "renewable": false, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Program Type Misclassification: ID 57 is an emergency cash assistance grant, NOT a
- **Verification:** Verified19. | Confidence: 96/100.
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (No academic grade cutoff imposed; crisis evaluation prioritized)9.) differs from renewal Maintain GWA (None (One-time assistance per crisis evaluation)19.)

---

### Bagong Pilipinas Merit Scholarship Program (BPMSP) – Technical Education and Skills Development Authority (TVET) Diploma Track20 (ID: 77)

#### Identity / Affiliations
- **Provider:** Technical Education and Skills Development Authority (TESDA) in joint partnership with CHED and DepEd20
- **Category:** Government / National / Merit-based / Technical-Vocational20
- **Website:** https://bpms.ched.gov.ph9, https://tesda.gov.ph25
- **Portal:** https://bpms.ched.gov.ph9
- **Guidelines:** CHED-DepEd-TESDA Joint Memorandum Circular (JMC) No. 1, Series of 202620
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen24.
- **Residency / Destination:** Resident of the Philippines24.
- **Education Level:** Technical Education and Skills Development Authority (TVET) Diploma level9.
- **Eligible Year Levels:** 1st Year (Incoming first-time entrants into TVET diploma programs)20.
- **Incoming Freshman Only:** Yes20.
- **Existing College Students:** Ineligible (Must have earned zero college or tertiary units)21.
- **Graduate Students:** Ineligible21.
- **Current Enrollment:** Accepted or enrolled in a priority diploma program offered by a TESDA-registered Technical Vocational Institution (TVI)20.
- **Academic Requirements:** Grade 12 Senior High School General Weighted Average (GWA) of at least 90.00% or equivalent21.
- **Minimum GWA:** 90.00%21.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE for TVET track (HE track uses Top 5 / 95% GWA, TVET track mandates GWA >= 90%)21.
- **Income Ceilings:** Combined annual gross income of parents/guardians must not exceed ₱2,000,000.0020.
- **Age Restrictions:** No age limit imposed (Irrespective of age provided candidate has earned no tertiary units)21.
- **School / Consortium Restrictions:** Restricted to TESDA-registered Technical Vocational Institutions (TVIs) delivering approved priority diploma programs20.
- **Course Restrictions:** TESDA-identified priority diploma courses in key growth sectors20.
- **Sectoral / Hidden Requirements:** Special equity groups (PWDs, Solo Parents, IPs, Senior Citizens, first-generation students) receive 10 additional ranking points in selection scoring20.
- **Good Moral:** Required21.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Applicants must NOT previously hold a technical-vocational diploma or NC Level III or higher (unless acquired as part of the SHS curriculum)21. TESDA has sole authority and exclusive jurisdiction over the TVET Diploma Track21. Transferees or shiftees with credited tertiary units are ineligible26.

#### Timing
- **Who May Apply:** Graduating SHS Grade 12 students, prior SHS graduates with no tertiary units, and 4th year HS graduates from SY 2015–2016 or earlier with no tertiary units21.
- **Freshmen:** : Yes (Incoming 1st year TVET diploma students)21.
- **Sophomores:** : No21.
- **Juniors:** : No21.
- **Seniors:** : No21.
- **Graduates:** : No21.
- **Reapply:** : No21.
- **Opening:** Announced per annual cycle (portal opens upon JMC call)20.
- **Closing:** June 30, 2026 (for initial cycle)20.
- **Cycle:** Fixed / Annual20.
- **AY Covered:** AY 2026–202720.

#### Benefits (catalog)
- **Tuition:** Tuition subsidy up to ₱70,000.00 per academic year20.
- **Monthly Stipend:** Integrated into annual living stipend20.
- **Allowance:** Living stipend of ₱40,000.00 per academic year20.
- **Return Service:** Mandatory 1 year of return service in the Philippines for every 1 year of scholarship received, prioritizing public and government institutions20.

#### Renewal
- **Maintain GWA:** Must pass all subjects every semester to retain grant20.
- **Regular Load:** Full-time credit enrollment in TVET diploma curriculum21.
- **No Failures:** Zero failing marks allowed20.

#### Disqualifying / Conflicts
- Earning tertiary or college units prior to award21.
- Holding an NC Level III, NC Level IV, or prior TVET diploma (unless part of SHS curriculum)21.
- Combined parental gross annual income exceeding ₱2,000,000.0020.
- Failing any subject during the TVET diploma program20.
- Transferees or shiftees with credited tertiary units26.

#### Required Documents (hidden operational requirements)
- Accomplished Online Application Form on official BPMSP portal21.
- PSA Certified Birth Certificate21.
- Certified True Copy of Learner's Progress Report Card (Form 138 / SF9) showing SHS GWA >= 90.00%21.
- Proof of Family Income (BIR Tax Exemption Certificate, BIR Form 2316 / 1701, DSWD 4Ps / Indigency Certificate, or OFW Employment Contract <= ₱2,000,000.00)20.
- Proof of Admission / Acceptance to a TESDA-registered TVI Diploma Program (Certificate of Acceptance, Training Agreement, or Enrollment Confirmation)21.
- Signed Parent / Legal Guardian Certification (Annex L)24.

#### Recommended Schema / Fields
```json
{ "education_level": ["TVET"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": true, "minimum_gwa": 90.00, "income_limit": 2000000, "school_type": ["TESDA_REGISTERED_TVI"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "04-01", "close": "06-30"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "return_service_required": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Track and Level Confusion: Database ID 77 represents the TVET Track of BPMSP, whereas
- **Verification:** Verified20. | Confidence: 90/100.
- **Contradictions:**
  - Entry min_gwa (90.00%21.) differs from renewal Maintain GWA (Must pass all subjects every semester to retain grant20.)

---

### GSIS Educational Subsidy Program (GESP)9 (ID: 84)

#### Identity / Affiliations
- **Provider:** Government Service Insurance System (GSIS)9
- **Category:** Government / Dependent Affiliation / Financial Subsidy9
- **Website:** https://www.gsis.gov.ph9
- **Portal:** GSIS Touch Mobile App / GSIS Branch Offices9.
- **Guidelines:** GSIS Board Resolution No. 49-2021; GESP Policy Guidelines9
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen.
- **Residency / Destination:** Resident of the Philippines.
- **Education Level:** College / Undergraduate9.
- **Eligible Year Levels:** 1st, 2nd, 3rd, 4th, and 5th Year9.
- **Incoming Freshman Only:** No9.
- **Existing College Students:** Yes9.
- **Graduate Students:** Ineligible9.
- **Current Enrollment:** Enrolled in a 4- or 5-year college degree program in a CHED-recognized HEI9.
- **Academic Requirements:** Active student status meeting university retention standards9.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Passing grade status required)9.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** Controlled via GSIS member parent salary grade (GSIS active members in lowest Salary Grades prioritized; SG 24 and below)9.
- **Age Restrictions:** Dependent child must be below 25 years old.
- **School / Consortium Restrictions:** CHED-recognized State Universities and Colleges or Private HEIs9.
- **Course Restrictions:** Any undergraduate degree program9.
- **Sectoral / Hidden Requirements:** Parent must be an active GSIS member with updated premium contributions9.
- **Good Moral:** Required.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Selection based on computer-generated ranking prioritizing members with lowest salary grade and longest length of service9.

#### Timing
- **Who May Apply:** Dependents of active GSIS members9.
- **Freshmen:** : Yes9.
- **Sophomores:** : Yes9.
- **Juniors:** : Yes9.
- **Seniors:** : Yes9.
- **Graduates:** : No9.
- **Reapply:** : Yes9.
- **Opening:** Announced per annual GSIS advisory9.
- **Closing:** Specified in annual notice9.
- **Cycle:** Annual9.
- **AY Covered:** AY 2025–2026 / AY 2026–20279.

#### Benefits (catalog)
- **Tuition:** Direct cash subsidy provided to scholar9.
- **Monthly Stipend:** None9.
- **Allowance:** ₱10,000.00 cash subsidy per Academic Year9.
- **Return Service:** None9.

#### Renewal
- **Maintain GWA:** Passing grades in all enrolled subjects9.
- **Regular Load:** Full credit load per semester9.
- **No Failures:** Zero failing marks9.

#### Disqualifying / Conflicts
- Member parent inactive or in default of GSIS premium payments9.
- Dependent age reaching 25 years old9.
- Student failing any academic subject9.
- Member parent salary grade exceeding ceiling9.

#### Required Documents (hidden operational requirements)
- Official GESP Application Form9.
- PSA Birth Certificate of nominated child9.
- Certificate of Employment / Service Record of GSIS member showing Salary Grade9.
- Certificate of Enrollment / Registration Form from CHED-recognized college9.
- School grade report / transcript showing passing marks9.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": null, "income_limit": null, "parent_employment_restriction": "GSIS_ACTIVE_MEMBER", "school_type": ["CHED_RECOGNIZED_HEI"], "partner_school_restricted": false, "citizenship": "Filipino", "application_window": {"open": "annual_notice", "close": "annual_notice"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Differentiation from Other GSIS Grants: The system must maintain explicit separation
- **Verification:** Verified9. | Confidence: 98/100.
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Passing grade status required)9.) differs from renewal Maintain GWA (Passing grades in all enrolled subjects9.)

---

### Education for Development Scholarship Program (EDSP)18 (ID: 85)

#### Identity / Affiliations
- **Provider:** Overseas Workers Welfare Administration (OWWA)18
- **Category:** Government / Merit-and-Need / OFW Dependent27
- **Website:** https://owwa.gov.ph9
- **Portal:** https://scholarship.owwa.gov.ph27
- **Guidelines:** OWWA EDSP Guidelines18
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Natural-born Filipino citizen27.
- **Residency / Destination:** Resident of the Philippines27.
- **Education Level:** College / Undergraduate9.
- **Eligible Year Levels:** Category 1 (Incoming 1st Year Freshmen); Category 2 (2nd to 5th Year College Students)18.
- **Incoming Freshman Only:** No (Has distinct tracks for incoming freshmen and ongoing 2nd-5th year college students)18.
- **Existing College Students:** Yes (Under EDSP Category 2)28.
- **Graduate Students:** Ineligible18.
- **Current Enrollment:** Enrolled or accepted in a 4- or 5-year baccalaureate degree program in an accredited Philippine college or university18.
- **Academic Requirements:** ○ Category 1 (Freshmen): SHS Grade 12 General Weighted Average (GWA) of at least 80.00% with zero failing grades; must qualify via national qualifying examination (top DOST national exam takers)27. ○ Category 2 (Upperclassmen): Cumulative college GWA of at least 85.00% or equivalent with zero failing grades28.
- **Minimum GWA:** 80.00% (Freshmen entry) / 85.00% (Upperclassmen entry)27.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE27.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE for EDSP main track (Restricted by active OWWA member contribution status)18.
- **Age Restrictions:** Must be single and not over 21 years old for Category 1 (Freshmen)27; single and not over 30 years old for Category 2 (Upperclassmen)28.
- **School / Consortium Restrictions:** Accredited Philippine-based colleges and universities18.
- **Course Restrictions:** Any 4- or 5-year baccalaureate degree program18.
- **Sectoral / Hidden Requirements:** Must be a child of an active OWWA member, or a sibling of a single / childless active OWWA member18.
- **Good Moral:** Required27.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** OFW parent/sibling membership must be ACTIVE at the time of application18. Only one scholarship beneficiary per OFW family is allowed under OWWA scholarship programs27. Single marital status mandatory27.

#### Timing
- **Who May Apply:** Dependents of active OWWA members entering Grade 12 / 1st Year College or currently in 2nd to 5th Year College27.
- **Freshmen:** : Yes (Incoming 1st Year Freshmen)27.
- **Sophomores:** : Yes (Under Category 2)28.
- **Juniors:** : Yes (Under Category 2)28.
- **Seniors:** : Yes (Under Category 2)28.
- **Graduates:** : No18.
- **Reapply:** : Yes28.
- **Opening:** July 16 annually (for main application intake)28 / November 10 (for DOST-EDSP track)27.
- **Closing:** July 31 annually28 / November 2827.
- **Cycle:** Fixed / Annual27.
- **AY Covered:** AY 2025–2026 / AY 2026–202728.

#### Benefits (catalog)
- **Tuition:** Direct financial grant disbursed to scholar27.
- **Monthly Stipend:** Integrated into annual financial assistance package27.
- **Allowance:** Financial assistance of ₱60,000.00 per Academic Year (disbursed at ₱30,000.00 per semester)18.
- **Return Service:** None18.

#### Renewal
- **Maintain GWA:** Maintain a minimum GWA of at least 85.00% (or passing mark specified by OWWA RWO) each semester without failing grades27.
- **Regular Load:** Full credit load per term as prescribed in curriculum18.
- **No Failures:** Zero failing, dropped, or incomplete grades27.

#### Disqualifying / Conflicts
- Inactive OWWA member contribution status18.
- Marriage of scholar during scholarship period (Must remain single)27.
- Dependent age exceeding 21 years old (Freshmen) or 30 years old (Upperclassmen)27.
- Incurring a failing grade or dropping a subject27.
- Concurrent enjoyment of another OWWA or major government scholarship grant27.

#### Required Documents (hidden operational requirements)
- Proof of OFW Active Membership (OWWA Membership verification printout / Official Receipt)18.
- Valid Passport Bio Page of OFW parent / sibling27.
- PSA Birth Certificate of applicant dependent and PSA Marriage Certificate of parents27.
- Academic Records: Form 137 / Form 138 / TOR showing GWA >= 80% (Freshmen) or >= 85% (Upperclassmen) with zero failing marks27.
- Two (2) pieces 2x2 ID photos with white background and name tag27.
- Certificate of Good Moral Character27.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 80.00, "renewal_gwa": 85.00, "age_limit": 21, "parent_employment_restriction": "OWWA_ACTIVE_MEMBER_DEPENDENT", "school_type": ["CHED_RECOGNIZED_HEI"], "partner_school_restricted": false, "citizenship": "Filipino", "application_window": {"open": "07-16", "close": "07-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Age Mismatch across Categories: The system must apply age_limit: 21 for incoming 1st
- **Verification:** Verified18. | Confidence: 92/100.
- **Contradictions:**
  - Entry min_gwa (80.00% (Freshmen entry) / 85.00% (Upperclassmen entry)27.) differs from renewal Maintain GWA (Maintain a minimum GWA of at least 85.00% (or passing mark specified by OWWA RWO) each semester without failing grades27.)

---

### OFW Dependent Scholarship Program (ODSP)18 (ID: 86)

#### Identity / Affiliations
- **Provider:** Overseas Workers Welfare Administration (OWWA)18
- **Category:** Government / Need-based / OFW Dependent28
- **Website:** https://owwa.gov.ph9
- **Portal:** https://scholarship.owwa.gov.ph27
- **Guidelines:** OWWA ODSP Operating Guidelines18
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Natural-born Filipino citizen28.
- **Residency / Destination:** Resident of the Philippines28.
- **Education Level:** College / Undergraduate9.
- **Eligible Year Levels:** Category 1 (Incoming 1st Year Freshmen); Category 2 (2nd to 5th Year College Students)18.
- **Incoming Freshman Only:** No18.
- **Existing College Students:** Yes28.
- **Graduate Students:** Ineligible18.
- **Current Enrollment:** Enrolled or accepted in a college or university in the Philippines18.
- **Academic Requirements:** SHS Report Card or college transcript showing General Weighted Average (GWA) of at least 75.00% or passing mark with no failing grades18.
- **Minimum GWA:** 75.00%18.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE28.
- **Income Ceilings:** OFW parent monthly basic salary must NOT exceed USD $1,000.0018.
- **Age Restrictions:** Single and not over 21 years old for Category 1 (Freshmen)28; single and not over 30 years old for Category 2 (Upperclassmen)28.
- **School / Consortium Restrictions:** Philippine-based colleges and universities18.
- **Course Restrictions:** Any undergraduate degree program18.
- **Sectoral / Hidden Requirements:** Dependent child or sibling of an active OWWA member18.
- **Good Moral:** Required28.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Single marital status mandatory28. OFW membership must be active at application18. Allocation capped per province18.

#### Timing
- **Who May Apply:** Dependents of low-income active OWWA members entering or enrolled in college18.
- **Freshmen:** : Yes18.
- **Sophomores:** : Yes28.
- **Juniors:** : Yes28.
- **Seniors:** : Yes28.
- **Graduates:** : No18.
- **Reapply:** : Yes28.
- **Opening:** July 16 annually28.
- **Closing:** July 31 annually28.
- **Cycle:** Fixed / Annual28.
- **AY Covered:** AY 2025–2026 / AY 2026–202728.

#### Benefits (catalog)
- **Tuition:** Direct cash assistance disbursed to scholar28.
- **Monthly Stipend:** Integrated into annual assistance grant28.
- **Allowance:** Financial assistance of ₱20,000.00 per Academic Year (disbursed at ₱10,000.00 per semester)28.
- **Return Service:** None18.

#### Renewal
- **Maintain GWA:** Maintain a passing GWA per term (at least 75.00%) with zero failing grades18.
- **Regular Load:** Enrolled in regular load per semester18.
- **No Failures:** Zero failing marks28.

#### Disqualifying / Conflicts
- OFW monthly salary exceeding USD $1,000.0028.
- Inactive OWWA contribution status18.
- Marriage of scholar during award period28.
- Dependent age exceeding 21 years old (Freshmen) or 30 years old (Upperclassmen)28.
- Incurring failing grades28.

#### Required Documents (hidden operational requirements)
- Proof of OFW Active Membership (OWWA printout)18.
- Copy of OFW Valid Passport bio page28.
- Proof of OFW Monthly Salary (Employment Contract, Overseas Employment Certificate [OEC], Payslip showing salary <= USD $1,000.00)28.
- PSA Birth Certificate of applicant dependent28.
- Academic Report Card / TOR showing GWA >= 75.00%18.
- Two (2) 2x2 ID photos27.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 75.00, "age_limit": 21, "parent_employment_restriction": "OWWA_ACTIVE_MEMBER_SALARY_1000USD_BELOW", "school_type": ["CHED_RECOGNIZED_HEI"], "partner_school_restricted": false, "citizenship": "Filipino", "application_window": {"open": "07-16", "close": "07-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Salary Cap Filter: The system must check user.ofw_parent_monthly_salary_usd <= 1000.
- **Verification:** Verified18. | Confidence: 96/100.
- **Contradictions:**
  - Entry min_gwa (75.00%18.) differs from renewal Maintain GWA (Maintain a passing GWA per term (at least 75.00%) with zero failing grades18.)

---

### Congressional Migrant Workers Scholarship Program (CMWSP)27 (ID: 87)

#### Identity / Affiliations
- **Provider:** Overseas Workers Welfare Administration (OWWA)27
- **Category:** Government / Merit-and-Need / Science & Technology27
- **Website:** https://owwa.gov.ph9
- **Portal:** https://scholarship.owwa.gov.ph27
- **Guidelines:** Republic Act No. 8042 (Migrant Workers Act); OWWA CMWSP Rules27
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Natural-born Filipino citizen27.
- **Residency / Destination:** Resident of the Philippines27.
- **Education Level:** College / Undergraduate9.
- **Eligible Year Levels:** Year 1 (Incoming First-Year College Freshmen)27.
- **Incoming Freshman Only:** Yes27.
- **Existing College Students:** Ineligible27.
- **Graduate Students:** Ineligible27.
- **Current Enrollment:** Enrolled or accepted as an incoming 1st-year college student in an accredited Philippine college or university27.
- **Academic Requirements:** Senior High School General Weighted Average (GWA) of at least 80.00% or equivalent with zero failing grades27.
- **Minimum GWA:** 80.00%27.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE27.
- **Income Ceilings:** Combined family annual income must NOT exceed USD $2,400.0027.
- **Age Restrictions:** OFW applicant must NOT be older than 45 years on date of application27; dependent child applicant must NOT be older than 21 years27.
- **School / Consortium Restrictions:** Accredited Philippine colleges and universities27.
- **Course Restrictions:** Restricted to Science and Technology courses based on the Department of Science and Technology (DOST) priority list27.
- **Sectoral / Hidden Requirements:** Active or former documented OFW, or a legitimate child of an OFW27.
- **Good Moral:** Required27.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Single marital status required for dependent child applicants27. Must pass selection evaluation27.

#### Timing
- **Who May Apply:** Incoming 1st-year college freshmen (OFWs under 45 or children of OFWs under 21)27.
- **Freshmen:** : Yes (Prior to starting 1st term)27.
- **Sophomores:** : No27.
- **Juniors:** : No27.
- **Seniors:** : No27.
- **Graduates:** : No27.
- **Reapply:** : No27.
- **Opening:** November 10 annually27.
- **Closing:** November 28 annually27.
- **Cycle:** Fixed / Annual27.
- **AY Covered:** AY 2026–202727.

#### Benefits (catalog)
- **Tuition:** Direct financial grant disbursed to scholar27.
- **Monthly Stipend:** Integrated into annual grant package27.
- **Allowance:** Financial assistance of ₱60,000.00 per Academic Year (disbursed at ₱30,000.00 per semester)27.
- **Return Service:** None27.

#### Renewal
- **Maintain GWA:** Maintain required GWA (80.00%) per semester without failing grades27.
- **Regular Load:** Full-time credit enrollment in approved S&T degree27.
- **No Failures:** Zero failing marks27.

#### Disqualifying / Conflicts
- Combined family annual income exceeding USD $2,400.0027.
- Enrolling in non-S&T degree programs27.
- Age exceeding 21 years (for dependent) or 45 years (for OFW)27.
- Incurring a failing grade in any subject27.

#### Required Documents (hidden operational requirements)
- Proof of OFW Status / Valid Passport Bio Page27.
- PSA Birth Certificate of dependent applicant27.
- Proof of Family Income showing combined annual income <= USD $2,400.0027.
- SHS Form 137 / Form 138 Report Card showing GWA >= 80.00% with zero failing grades27.
- Certificate of Enrollment / Admission in a DOST priority S&T course27.
- Two (2) 2x2 ID photos27.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": true, "minimum_gwa": 80.00, "age_limit": 21, "parent_employment_restriction": "OWWA_DOCUMENTED_OFW", "priority_courses": ["DOST_ST_PRIORITY_COURSES"], "school_type": ["CHED_RECOGNIZED_HEI"], "partner_school_restricted": false, "citizenship": "Filipino", "application_window": {"open": "11-10", "close": "11-28"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Course Filter Constraint: The system must match user.course_code against the
- **Verification:** Verified27. | Confidence: 96/100.
- **Contradictions:**
  - Entry min_gwa (80.00%27.) differs from renewal Maintain GWA (Maintain required GWA (80.00%) per semester without failing grades27.)

---

### Training for Work Scholarship Program (TWSP)25 (ID: 112)

#### Identity / Affiliations
- **Provider:** Technical Education and Skills Development Authority (TESDA)25
- **Category:** Government / Technical-Vocational / Sectoral Grant25
- **Website:** https://tesda.gov.ph9
- **Portal:** TESDA Online Program / Regional TESDA Technology Institutions (TTIs) and Accredited TVIs25.
- **Guidelines:** TESDA Circular No. 018-2022; TWSP Operating Guidelines25
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen25.
- **Residency / Destination:** Resident of the Philippines25.
- **Education Level:** Technical-Vocational Education and Training (TVET)9.
- **Eligible Year Levels:** Non-degree short-term TVET qualifications (NC I to NC IV)25.
- **Incoming Freshman Only:** No25.
- **Existing College Students:** Eligible (Provided not currently enrolled in another TESDA scholarship)25.
- **Graduate Students:** Eligible25.
- **Current Enrollment:** Enrolled or accepted in a TESDA-registered TVET program25.
- **Academic Requirements:** Basic literacy and numeracy; satisfies specific TVET qualification entry standards25.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Passing basic qualification entry test required)9.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE9.
- **Age Restrictions:** Must be at least 15 years old at the start of the training program25.
- **School / Consortium Restrictions:** TESDA Technology Institutions (TTIs) and TESDA-accredited private TVIs25.
- **Course Restrictions:** TESDA priority sector qualifications (Construction, IT-BPM, Tourism, Agriculture, Logistics, Manufacturing)25.
- **Sectoral / Hidden Requirements:** Unemployed workers, underemployed, returning OFWs, displaced workers prioritized25.
- **Good Moral:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Health:** Physically fit to undergo technical training25.
- **Other Official Rules / Conflicts:** Trainee must NOT be currently enrolled in any other active TESDA scholarship grant25.

#### Timing
- **Who May Apply:** Any Filipino citizen aged 15 or older seeking technical skills training25.
- **Freshmen:** : Yes25.
- **Sophomores:** : Yes25.
- **Juniors:** : Yes25.
- **Seniors:** : Yes25.
- **Graduates:** : Yes25.
- **Reapply:** : Yes (For a different NC level or qualification sector)25.
- **Opening:** Year-round / Rolling intake9.
- **Closing:** December 31 annually (or subject to allocation batch schedules)9.
- **Cycle:** Rolling / Continuous9.
- **AY Covered:** AY 2025–2026 / AY 2026–20279.

#### Benefits (catalog)
- **Tuition:** 100% Full training cost waiver paid to TVI25.
- **Monthly Stipend:** Integrated into daily training allowance25.
- **Allowance:** Daily training allowance (₱160.00 per attendance day)25.
- **Return Service:** None9.

#### Renewal
- **Maintain GWA:** Maintain 80% minimum attendance rate and pass practical competency evaluations25.
- **Regular Load:** Full attendance during training schedule25.

#### Disqualifying / Conflicts
- Unexcused absences exceeding 20% of total training hours25.
- Simultaneous enrollment in another active TESDA scholarship program25.
- Age below 15 years old25.

#### Required Documents (hidden operational requirements)
- Accomplished TESDA Learner's Profile Form (MIS 03-02)25.
- Birth Certificate (PSA or Local Civil Registrar) or PhilSys ID25.
- Barangay Clearance or Police Clearance25.
- Three (3) 1x1 ID photos (white background, shirt with collar)25.

#### Recommended Schema / Fields
```json
{ "education_level": ["TVET"], "eligible_year_levels": [1], "incoming_year_only": false, "requires_current_enrollment": false, "minimum_gwa": null, "age_limit_min": 15, "school_type": ["TESDA_TECHNOLOGY_INSTITUTION", "TESDA_ACCREDITED_TVI"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "01-01", "close": "12-31"}, "deadline_type": "rolling", "cycle_type": "rolling", "renewable": false, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Multiple Grant Conflict: System must check user.active_tesda_scholarship == false to
- **Verification:** Verified25. | Confidence: 95/100.
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Passing basic qualification entry test required)9.) differs from renewal Maintain GWA (Maintain 80% minimum attendance rate and pass practical competency evaluations25.)

---

### Special Training for Employment Program (STEP)25 (ID: 113)

#### Identity / Affiliations
- **Provider:** Technical Education and Skills Development Authority (TESDA)25
- **Category:** Government / Technical-Vocational / Community-Based25
- **Website:** https://tesda.gov.ph9
- **Portal:** Community-Based Training Centers / TESDA Provincial Offices25.
- **Guidelines:** TESDA Circular No. 018-2022; STEP Operating Guidelines25
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen25.
- **Residency / Destination:** Resident of target barangay or municipality25.
- **Education Level:** Technical-Vocational Education and Training (TVET)9.
- **Eligible Year Levels:** Non-degree short-term TVET qualifications25.
- **Incoming Freshman Only:** No25.
- **Existing College Students:** Eligible25.
- **Graduate Students:** Eligible25.
- **Current Enrollment:** Enrolled or accepted in a STEP community training program25.
- **Academic Requirements:** Basic literacy and numeracy25.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE9.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE9.
- **Age Restrictions:** Must be at least 15 years old25.
- **School / Consortium Restrictions:** Community training centers and accredited TVIs25.
- **Course Restrictions:** Specialty trade courses (e.g., Welding, Electronics Repair, Baking, Small Engine Repair, Cosmetology)25.
- **Sectoral / Hidden Requirements:** Underprivileged citizens, informal economy workers, displaced workers, 4Ps beneficiaries prioritized25.
- **Good Moral:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Health:** Physically fit for practical trade tasks25.
- **Other Official Rules / Conflicts:** Must NOT be enrolled in another TESDA scholarship concurrently25.

#### Timing
- **Who May Apply:** Barangay residents seeking self-employment trade skills25.
- **Freshmen:** : Yes25.
- **Sophomores:** : Yes25.
- **Juniors:** : Yes25.
- **Seniors:** : Yes25.
- **Graduates:** : Yes25.
- **Reapply:** : Yes (For a different trade toolkit program)25.
- **Opening:** Year-round / Rolling intake9.
- **Closing:** December 31 annually9.
- **Cycle:** Rolling / Community batch intake25.
- **AY Covered:** AY 2025–2026 / AY 2026–20279.

#### Benefits (catalog)
- **Tuition:** 100% Free training cost25.
- **Monthly Stipend:** Integrated into daily training allowance25.
- **Allowance:** Daily training allowance (₱160.00 per attendance day)25.
- **Return Service:** None9.

#### Renewal
- **Maintain GWA:** Maintain 80% minimum attendance rate and pass competency assessment25.
- **Regular Load:** Full attendance during community training sessions25.

#### Disqualifying / Conflicts
- Unexcused attendance drop exceeding 20% of training duration25.
- Concurrent enrollment in another active TESDA scholarship25.
- Failure to complete practical trade modules25.

#### Required Documents (hidden operational requirements)
- Accomplished TESDA Learner's Profile Form (MIS 03-02)25.
- Barangay Certificate of Indigency / Residency25.
- Birth Certificate or PhilSys ID25.
- Three (3) 1x1 ID photos25.

#### Recommended Schema / Fields
```json
{ "education_level": ["TVET"], "eligible_year_levels": [1], "incoming_year_only": false, "requires_current_enrollment": false, "minimum_gwa": null, "age_limit_min": 15, "includes_starter_toolkits": true, "school_type": ["COMMUNITY_TRAINING_CENTER", "TESDA_ACCREDITED_TVI"], "partner_school_restricted": false, "citizenship": "Filipino", "application_window": {"open": "01-01", "close": "12-31"}, "deadline_type": "rolling", "cycle_type": "rolling", "renewable": false, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Targeted Matching: ID 113 is designed specifically for informal sector trade training with
- **Verification:** Verified25. | Confidence: 92/100.
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE9.) differs from renewal Maintain GWA (Maintain 80% minimum attendance rate and pass competency assessment25.)

---

### Education and Livelihood Assistance Program (ELAP)9 (ID: 124)

#### Identity / Affiliations
- **Provider:** Overseas Workers Welfare Administration (OWWA)9
- **Category:** Government / Need-and-Crisis / OFW Dependent31
- **Website:** https://owwa.gov.ph/education-and-livelihood-assistance-program-elap/9
- **Portal:** OWWA Regional Welfare Offices (RWOs)27.
- **Guidelines:** OWWA ELAP Operating Guidelines; Republic Act No. 804218
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Natural-born Filipino citizen18.
- **Residency / Destination:** Resident of the Philippines18.
- **Education Level:** Elementary, Secondary (JHS/SHS), College / Tertiary9.
- **Eligible Year Levels:** All year levels from primary through tertiary education9.
- **Incoming Freshman Only:** No9.
- **Existing College Students:** Yes9.
- **Graduate Students:** Ineligible18.
- **Current Enrollment:** Enrolled in a recognized elementary, secondary, or tertiary institution18.
- **Academic Requirements:** Passing General Weighted Average (GWA) of at least 75.00% or passing mark9.
- **Minimum GWA:** 75.00%9.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** Combined family annual gross income must NOT exceed ₱250,000.009.
- **Age Restrictions:** Dependent child must be below 21 years old for college level (or under 18 for basic education)18.
- **School / Consortium Restrictions:** Recognized public or private educational institutions18.
- **Course Restrictions:** Any course or grade level18.
- **Sectoral / Hidden Requirements:** Must be a surviving dependent child of an active OWWA member who died or suffered permanent total disability31. Limited to ONE (1) child beneficiary per deceased/incapacitated OFW family31.
- **Good Moral:** Required18.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** OFW parent must have been an active OWWA member at the time of death or permanent disability31.

#### Timing
- **Who May Apply:** Surviving child of deceased or permanently incapacitated active OFW31.
- **Freshmen:** : Yes9.
- **Sophomores:** : Yes9.
- **Juniors:** : Yes9.
- **Seniors:** : Yes9.
- **Graduates:** : No18.
- **Reapply:** : Yes (Continuous annual support until course
- **Opening:** Year-round intake following casualty event9.
- **Closing:** Specified per regional office window / annual cycle9.
- **Cycle:** Annual9.
- **AY Covered:** AY 2025–2026 / AY 2026–20279.

#### Benefits (catalog)
- **Tuition:** Direct cash assistance grant18.
- **Monthly Stipend:** Integrated into annual grant package18.
- **Return Service:** None9.

#### Renewal
- **Maintain GWA:** Maintain passing GWA (at least 75.00%) every school year9.
- **Regular Load:** Continuous enrollment in regular grade/year level18.
- **No Failures:** Passing all enrolled subjects18.

#### Disqualifying / Conflicts
- OFW parent not an active OWWA member at time of death or disability31.
- More than one child beneficiary applying from the same family (Strictly 1 child per family rule)31.
- Combined family income exceeding ₱250,000.009.
- Academic failure or dropping out from school18.

#### Required Documents (hidden operational requirements)
- Official Death Certificate or Medical Certificate of Permanent Disability of OFW issued by proper authority18.
- Proof of Active OWWA Membership at time of casualty event30.
- PSA Marriage Certificate of parents and PSA Birth Certificate of child beneficiary18.
- Form 138 Report Card or College Transcript showing passing GWA >= 75.00%9.
- BIR Tax Exemption Certificate, ITR, or Barangay Certificate of Indigency (Income <= ₱250,000.00)9.
- Certificate of Enrollment from school18.

#### Recommended Schema / Fields
```json
{ "education_level": ["Senior High School", "College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 75.00, "income_limit": 250000, "parent_employment_restriction": "OWWA_DECEASED_OR_INCAPACITATED_ACTIVE_MEMBER", "one_beneficiary_per_family": true, "school_type": ["RECOGNIZED_EDUCATIONAL_INSTITUTION"], "partner_school_restricted": false, "citizenship": "Filipino", "application_window": {"open": "01-01", "close": "12-31"}, "deadline_type": "rolling", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Missing Casualty and Single-Beneficiary Flags: ID 124 strictly requires
- **Verification:** Verified18. | Confidence: 92/100.
- **Contradictions:**
  - Entry min_gwa (75.00%9.) differs from renewal Maintain GWA (Maintain passing GWA (at least 75.00%) every school year9.)

---

## SOURCE: `DATABASE_V3_GROUPC_PRIVATE_FOUNDATIONS_P1.pdf`

**Scholarships in this PDF:** 7

### Ayala Foundation U-Go Scholar Grant (U-GO Scholar Grant) (ID: 11)

#### Identity / Affiliations
- **Provider:** Ayala Foundation, Inc. (in partnership with U-Go Global)
- **Category:** Private / Foundation / Merit-and-Need / Female Empowerment
- **Website:** https://ayalafoundation.org/programs/scholarships/
- **Portal:** Official Eligibility Form Portal (sent via email/QR upon eligibility screening)
- **Guidelines:** Ayala Foundation & U-Go Grant Program Official Guidelines
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Education Level:** College / Undergraduate
- **Eligible Year Levels:** 1st Year, 2nd Year, 3rd Year (and 4th Year if enrolled in a 5-year degree program)
- **Incoming Freshman Only:** No
- **Existing College Students:** Yes
- **Graduate Students:** No
- **Current Enrollment:** Enrolled or will enroll in a public or state university/college (SUC/LUC) in the Philippines
- **Academic Requirements:** Minimum Grade Point Average / General Weighted Average (GWA) of at least 85% with no failing grades; no disciplinary or administrative cases
- **Minimum GWA:** 85.00%
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Demonstrated financial need (family income within low-income threshold, parent ITR, BIR Tax Exemption, or Indigency)
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Restricted to public or state universities and colleges (SUCs/LUCs) in the Philippines
- **Course Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Sectoral / Hidden Requirements:** Must be a female student
- **Good Moral:** Required (must have no disciplinary or administrative cases)
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Must NOT have any existing scholarship grant

#### Timing
- **Who May Apply:** Female Filipino incoming 1st-year, 2nd-year, or 3rd-year college students (and 4th-year students taking a 5-year course) enrolled in public or state universities.
- **Freshmen:** : Yes
- **Sophomores:** : Yes
- **Juniors:** : Yes
- **Seniors:** : Yes (Only if taking a 5-year course and entering 4th year;
- **Graduates:** : No
- **Reapply:** : Yes, provided they meet all eligibility criteria and hold
- **Opening:** May 5, 2026
- **Closing:** June 6, 2026
- **Cycle:** Annual
- **AY Covered:** AY 2026–2027

#### Benefits (catalog)
- **Tuition:** NOT SPECIFIED IN OFFICIAL SOURCE (Public/state universities are covered under Republic Act 10931; grant provides direct educational financial support).
- **Monthly Stipend:** Integrated into annual financial assistance.
- **Allowance:** Approximately PHP 40,000.00 annual financial assistance.
- **Return Service:** None.

#### Renewal
- **Maintain GWA:** Maintain a minimum GWA of 85.00% or equivalent each academic term.
- **Regular Load:** Full-time credit load per term in a public/state university.
- **No Failures:** Zero failing grades.

#### Disqualifying / Conflicts
- Male gender.
- Possession or active enjoyment of any other scholarship grant.
- Enrollment in a private higher education institution.
- Students expecting to graduate during the current academic year.
- GWA below 85.00% or presence of failing/incomplete grades.
- History of administrative or disciplinary sanctions.

#### Required Documents (hidden operational requirements)
- Duly accomplished online application form.
- Current official Certificate of Registration / Enrollment signed by the registrar with wet signature.
- Latest copy of grades / Transcript of Records signed by the registrar with wet signature.
- Proof of financial need (Parents' or guardians' most recent Income Tax Return [ITR], BIR Tax Exemption Certificate, Barangay Certificate of Indigency, or OFW/seafarer contract/proof of income).
- Proof of college admission or Senior High School diploma (for incoming 1st-year students).
- Recent copy of electric or water bill (if available).
- Official Recommendation Letter (for shortlisted applicants).

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 85.00, "income_limit": 400000, "gender_restriction": "FEMALE", "school_type": ["SUC", "LUC"], "partner_school_restricted": false, "citizenship": "Filipino", "scholarship_exclusivity_clause": true, "application_window": { "open": "05-05", "close": "06-06" }, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Gender Mismatch: Live database state currently lacks a gender filter tag. Displaying ID 11
- **Verification:** Verified | Confidence: n/a
- **Contradictions:**
  - Entry min_gwa (85.00%) differs from renewal Maintain GWA (Maintain a minimum GWA of 85.00% or equivalent each academic term.)

---

### Assistance for the Completion of College Education for Superior Students (MBFI-ACCESS) Program (ID: 13)

#### Identity / Affiliations
- **Provider:** Metrobank Foundation, Inc. (MBFI) / GT Foundation, Inc. (GTFI)
- **Category:** Private / Foundation / Merit-and-Need
- **Website:** https://www.mbfoundation.org.ph
- **Portal:** Coordinated directly through scholarship offices of designated partner universities and Metrobank Foundation offices
- **Guidelines:** MBFI-ACCESS Scholarship Program Guidelines & Partner University MOAs
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Education Level:** College / Undergraduate
- **Eligible Year Levels:** Year 1 (Incoming Freshmen) and Year 2 (Sophomores in Engineering tracks)
- **Incoming Freshman Only:** No (Incoming Freshmen for general priority courses; Sophomores for Engineering).
- **Existing College Students:** Yes (Incoming 2nd-year Engineering students in partner HEIs).
- **Graduate Students:** No
- **Current Enrollment:** Accepted or enrolled in a priority course at an MBFI partner university
- **Academic Requirements:** General Weighted Average (GWA) of at least 85.00% or equivalent in High School / previous college term; passing score in MBFI qualification exams and interviews
- **Minimum GWA:** 85.00%
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined gross annual family income not exceeding PHP 500,000.00
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Restricted strictly to MBFI partner universities/colleges (CHED Centers of Excellence/Development or Level II/III accredited institutions)
- **Course Restrictions:** Specialized Science & Math, Teacher Education (BEED/BSED), Information Technology, Engineering, Business Administration / Entrepreneurship, Accountancy, Nursing, Architecture, Statistics
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** Required
- **Health:** Physically and mentally fit - Other Official Rules: Must pass screening, written examinations, and panel evaluation processes
- **Other Official Rules / Conflicts:** Must pass screening, written examinations, and panel evaluation processes

#### Timing
- **Who May Apply:** Incoming college freshmen enrolled in priority courses, and incoming sophomores taking Engineering at accredited partner institutions.
- **Freshmen:** : Yes (as incoming 1st-year students entering college or
- **Sophomores:** : Yes (Incoming 2nd-year Engineering students).
- **Juniors:** : No
- **Seniors:** : No
- **Graduates:** : No
- **Reapply:** : No
- **Opening:** Announced per academic year cycle via partner university scholarship offices
- **Closing:** Specified in annual partner university advisories
- **Cycle:** Fixed / Annual
- **AY Covered:** AY 2025–2026 / AY 2026–2027

#### Benefits (catalog)
- **Tuition:** Full tuition and matriculation fee coverage at partner universities.
- **Monthly Stipend:** Direct monthly living allowance.
- **Allowance:** Fixed semester living and book allowances.
- **Return Service:** None (Encouraged participation in "Pay-it-forward Service to the 4Cs" via ASSET alumni association).

#### Renewal
- **Maintain GWA:** Maintain a minimum semester GWA of 85.00% or university passing standards.
- **Regular Load:** Full-time credit enrollment per term in approved priority course.
- **No Failures:** Zero failing grades in enrolled subjects.

#### Disqualifying / Conflicts
- Enrolling in non-partner higher education institutions.
- Combined annual family income exceeding PHP 500,000.00.
- GWA dropping below 85.00% or presence of failing grades.
- Failure to pass MBFI qualification examination or interview evaluation.

#### Required Documents (hidden operational requirements)
- Accomplished MBFI-ACCESS Application Form.
- Official Report Card / Transcript of Records / Form 137 showing minimum GWA of
- 00%.
- Parents' Income Tax Return (ITR) or BIR Certificate of Tax Exemption showing annual family income below PHP 500,000.00.
- Certificate of Enrollment / Notice of Admission from an MBFI partner university.
- Certificate of Good Moral Character.
- Medical Certificate confirming physical and mental fitness.
- 2x2 ID Pictures.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 85.00, "income_limit": 500000, "priority_courses": [ "ACCOUNTANCY", "BUSINESS_ADMINISTRATION", "ENTREPRENEURSHIP", "EDUCATION", "INFORMATION_TECHNOLOGY", "ENGINEERING", "SPECIALIZED_SCIENCE_MATH", "NURSING", "ARCHITECTURE", "STATISTICS" ], "school_type": ["PRIVATE_HEI", "SUC"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": { "open": "annual_notice", "close": "annual_notice" }, "deadline_type": "estimated", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● School Restriction Enforcement: Displaying ID 13 to students in non-partner HEIs causes
- **Verification:** Verified | Confidence: 95/100
- **Contradictions:**
  - Entry min_gwa (85.00%) differs from renewal Maintain GWA (Maintain a minimum semester GWA of 85.00% or university passing standards.)

---

### BPI Foundation Pagpupugay Scholarship Program (ID: 14)

#### Identity / Affiliations
- **Provider:** BPI Foundation, Inc.
- **Category:** Private / Foundation / Merit-and-Need / Frontliner Next-of-Kin
- **Website:** https://www.bpifoundation.org/programs/special-projects/pagpupugay-scholarship
- **Portal:** Online submission via BPI Foundation portal forms or partner university scholarship offices
- **Guidelines:** BPI Foundation Pagpupugay Scholarship Guidelines & Application E-Forms
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Education Level:** College / Undergraduate
- **Eligible Year Levels:** 1st Year, 2nd Year, 3rd Year, 4th Year, and 5th Year
- **Incoming Freshman Only:** No
- **Existing College Students:** Yes
- **Graduate Students:** No
- **Current Enrollment:** Enrolled or applying to any 4-year or 5-year college/university program in BPI Foundation partner schools nationwide (or non-partner HEIs upon direct coordination)
- **Academic Requirements:** General Weighted Average (GWA) of at least 85.00% or equivalent / prevailing university standards for the previous school year (incoming 1st year) or previous semester (incoming 2nd-5th year)
- **Minimum GWA:** 85.00%
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Demonstrated financial need verified via parents'/guardian's Income Tax Return (ITR)
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Open to students in BPI Foundation partner universities (e.g., Ateneo de Manila, Mapua, Malayan Colleges, National Teachers College, University of Nueva Caceres) and accredited nationwide HEIs
- **Course Restrictions:** Any 4-year or 5-year undergraduate degree program
- **Sectoral / Hidden Requirements:** Must be a qualified next-of-kin of medical frontliners (doctors, nurses, medical technologists, community health workers, administrative/utility/support staff in healthcare facilities) who passed away or contracted COVID-19 in the line of duty. Priority order: children of married frontliners; next-of-kin up to 3rd degree consanguinity for single frontliners
- **Good Moral:** Required (Certificate of Good Moral Character)
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Requires hospital endorsement letter, official affidavits of endorsement and no objection, and proof of frontliner COVID-19 medical/death status

#### Timing
- **Who May Apply:** Qualified next-of-kin of eligible medical frontliners entering or currently enrolled in 1st to 5th year of college.
- **Freshmen:** : Yes
- **Sophomores:** : Yes
- **Juniors:** : Yes
- **Seniors:** : Yes (4th and 5th year undergraduate students).
- **Graduates:** : No
- **Reapply:** : Yes (Scholarships are evaluated for annual renewal).
- **Opening:** Announced per annual cycle (typically Q2/Q3)
- **Closing:** Announced annually (e.g., July 31 / extended to September)
- **Cycle:** Annual
- **AY Covered:** AY 2025–2026 / AY 2026–2027

#### Benefits (catalog)
- **Tuition:** Up to PHP 100,000.00 per academic year covering tuition and matriculation fees (paid directly to partner HEI).
- **Monthly Stipend:** Provided as monthly living subsidy for State University/College (SUC) scholars.
- **Allowance:** Learning assistance allowance provided for SUC scholars.
- **Return Service:** None.

#### Renewal
- **Maintain GWA:** Maintain a minimum GWA of 85.00% or prevailing university standards each semester.
- **Regular Load:** Enrolled in full term credit load.
- **No Failures:** Compliance with university retention policies.

#### Disqualifying / Conflicts
- Applicant is not a qualified next-of-kin (child or up to 3rd degree consanguinity) of an eligible COVID-19 medical frontliner.
- Frontliner was not assigned to a hospital or recognized healthcare facility.
- Semester GWA dropping below 85.00%.
- Failure to submit mandatory hospital endorsements or affidavits.

#### Required Documents (hidden operational requirements)
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

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 85.00, "income_limit": 400000, "sectoral_restriction": "COVID19_MEDICAL_FRONTLINER_NEXT_OF_KIN", "priority_courses": null, "school_type": ["PRIVATE_HEI", "SUC"], "partner_school_restricted": false, "citizenship": "Filipino", "application_window": { "open": "annual_notice", "close": "annual_notice" }, "deadline_type": "estimated", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Sectoral Tag Mismatch: Live database state currently lacks the specific
- **Verification:** Verified | Confidence: 96/100
- **Contradictions:**
  - Entry min_gwa (85.00%) differs from renewal Maintain GWA (Maintain a minimum GWA of 85.00% or prevailing university standards each semester.)

---

### San Miguel Foundation Educational Assistance / Community Scholarship Program (ID: 15)

#### Identity / Affiliations
- **Provider:** San Miguel Foundation, Inc. (SMFI) / San Miguel Corporation (SMC) subsidiaries
- **Category:** Private / Foundation / Need-and-Merit / Host Community Support
- **Website:** https://www.sanmiguel.com.ph/page/san-miguel-foundation
- **Portal:** Processed via scholarship offices of partner universities and local SMC plant community relations offices
- **Guidelines:** San Miguel Foundation Community & College Scholarship Program Guidelines
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen
- **Residency / Destination:** Preference given to residents of San Miguel Corporation host communities or operational areas
- **Education Level:** College / Undergraduate (and Technical-Vocational courses)
- **Eligible Year Levels:** 1st Year, 2nd Year, 3rd Year, 4th Year, and 5th Year
- **Incoming Freshman Only:** No
- **Existing College Students:** Yes
- **Graduate Students:** No
- **Current Enrollment:** Enrolled or accepted in designated partner universities or SUCs/LUCs in SMC host communities
- **Academic Requirements:** Academically deserving student (minimum GWA parameter governed by partner university agreements, typically 85.00% to 88.00% without failing grades)
- **Minimum GWA:** 88.00% (Live database baseline; partner HEI MOA standards apply).
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Financially challenged background (family annual income < PHP 400,000.00 / demonstrated indigency)
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Restricted to SMC partner universities (e.g., UP Diliman, Dualtech Center, partner HEIs near SMC plants/townships)
- **Course Restrictions:** Engineering (Civil, Electrical, Mechanical, Chemical), Agriculture, Agribusiness, Business / Accountancy, Applied Sciences (Applied Physics, Molecular Biology & Biotechnology), Technical-Vocational skills
- **Sectoral / Hidden Requirements:** Residents of SMC host communities / underprivileged family dependents
- **Good Moral:** Required
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Must pass screening evaluation conducted by SMFI or partner university scholarship committee

#### Timing
- **Who May Apply:** Resident SHS graduates and ongoing college students enrolled in priority courses at partner institutions.
- **Freshmen:** : Yes - Can current sophomores apply?: Yes
- **Sophomores:** : Yes
- **Juniors:** : Yes (Incoming junior track available for specialized
- **Seniors:** : Yes
- **Graduates:** : No
- **Reapply:** : Yes
- **Opening:** Varies per partner university academic calendar
- **Closing:** Announced annually by partner university scholarship offices
- **Cycle:** Annual
- **AY Covered:** AY 2025–2026 / AY 2026–2027

#### Benefits (catalog)
- **Tuition:** Full tuition and matriculation fee coverage at partner institutions.
- **Monthly Stipend:** Direct monthly living allowance.
- **Allowance:** Fixed semester book and school supplies allowance.
- **Return Service:** None required (Potential career/employment opportunities offered across SMC operating companies).

#### Renewal
- **Maintain GWA:** Maintain required semester GWA prescribed in partner university MOA.
- **Regular Load:** Full-time credit enrollment per term.
- **No Failures:** Zero failing grades in enrolled subjects.

#### Disqualifying / Conflicts
- Non-enrollment in an SMC partner university or non-priority degree course.
- Combined annual family income exceeding PHP 400,000.00.
- Failing grades or dropping subjects during the academic term.
- Misrepresentation of residency in SMC host communities.

#### Required Documents (hidden operational requirements)
- SMFI Application Form / Partner University Scholarship Application Form.
- Official Transcript of Records / Report Card (Form 138 / SF9).
- Parents' Income Tax Return (ITR) or Barangay Certificate of Indigency.
- Barangay Certificate of Residency (proving residence in SMC host community).
- Certificate of Good Moral Character.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 88.00, "income_limit": 400000, "priority_courses": [ "CIVIL_ENGINEERING", "ELECTRICAL_ENGINEERING", "MECHANICAL_ENGINEERING", "CHEMICAL_ENGINEERING", "AGRICULTURE", "AGRIBUSINESS", "BUSINESS_ADMINISTRATION", "ACCOUNTANCY", "APPLIED_PHYSICS", "MOLECULAR_BIOLOGY" ], "school_type": ["PRIVATE_HEI", "SUC"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": { "open": "annual_notice", "close": "annual_notice" }, "deadline_type": "estimated", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Partner School Verification: Program relies on partner university agreements. Engine
- **Verification:** Verified | Confidence: 96/100
- **Contradictions:**
  - Entry min_gwa (88.00% (Live database baseline; partner HEI MOA standards apply).) differs from renewal Maintain GWA (Maintain required semester GWA prescribed in partner university MOA.)

---

### PLDT-Smart Foundation Gabay Guro Scholarship Program (ID: 16)

#### Identity / Affiliations
- **Provider:** PLDT-Smart Foundation (PSF) & PLDT Manager's Club, Inc.
- **Category:** Private / Foundation / Merit-and-Need / Teacher Education
- **Website:** https://www.gabayguro.com
- **Portal:** Administered directly through scholarship offices of partner State Universities and Colleges (SUCs) nationwide
- **Guidelines:** Gabay Guro Scholarship Questionnaire & Application Form (Revised 2023)
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Education Level:** College / Undergraduate
- **Eligible Year Levels:** Year 1 (Incoming First-Year College Students)
- **Incoming Freshman Only:** Yes
- **Existing College Students:** No
- **Graduate Students:** No
- **Current Enrollment:** Enrolled or admitted as a first-year student in Bachelor of Elementary Education (BEED) or Bachelor of Secondary Education (BSED) (major in English, Mathematics, Science) at a Gabay Guro partner SUC/college
- **Academic Requirements:** General Weighted Average (GWA) of at least 85.00% during the final year of Senior High School
- **Minimum GWA:** 85.00%
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined annual family gross income must NOT exceed PHP 250,000.00
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Restricted strictly to Gabay Guro partner SUCs nationwide (over 40+ partner state universities including MSU Gensan, PNU, etc.)
- **Course Restrictions:** Bachelor of Elementary Education (BEED), Bachelor of Secondary Education (BSED) with majors in English, Mathematics, or Science
- **Sectoral / Hidden Requirements:** Aspiring teachers / Teacher Education majors
- **Good Moral:** Required
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Must complete and sign the official Gabay Guro Undertaking Form committing to graduate and render teaching service in Philippine schools

#### Timing
- **Who May Apply:** Incoming first-year college students admitted to BEED or BSED programs at partner SUCs.
- **Freshmen:** : Yes (prior to starting term in 1st year).
- **Sophomores:** : No
- **Juniors:** : No
- **Seniors:** : No
- **Graduates:** : No
- **Reapply:** : No
- **Opening:** Announced per annual cycle via partner SUC scholarship offices
- **Closing:** Specified in annual partner SUC scholarship advisories
- **Cycle:** Fixed / Annual
- **AY Covered:** AY 2025–2026 / AY 2026–2027

#### Benefits (catalog)
- **Tuition:** Full coverage of tuition and matriculation fees.
- **Monthly Stipend:** Direct monthly living allowance.
- **Allowance:** Semester book allowance and connectivity support.
- **Return Service:** Mandatory teaching commitment in Philippine K-12 schools.

#### Renewal
- **Maintain GWA:** Maintain required semester GWA prescribed by university (typically 2.0 or 85.00%).
- **Regular Load:** Full-time credit load per semester in BEED/BSED program.
- **No Failures:** Zero failing or dropped grades.

#### Disqualifying / Conflicts
- Enrolling in non-education degree programs or non-partner universities.
- Combined family annual gross income exceeding PHP 250,000.00.
- SHS GWA below 85.00%.
- Refusal to sign the mandatory teaching return service undertaking.

#### Required Documents (hidden operational requirements)
- Gabay Guro Scholarship Questionnaire & Application Form (Revised 2023).
- Applicant's essay/autobiography ("MY AUTOBIOGRAPHY" in English or Filipino).
- Parents' Annual Income Tax Return (BIR Form 2316 / ITR) OR Barangay/DSWD Certificate of Indigency if unemployed/exempt.
- Latest Report Card / Rating (Form 138 / SF9) showing SHS GWA \ge 85.00\%.
- 2x2 ID Picture on white background.
- Signed Gabay Guro Undertaking Form.

#### Recommended Schema / Fields
```json
{ "education_lev el": ["College"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": true, "minimum_gwa": 85.00, "income_limit": 250000, "priority_courses": [ "BACHELOR_OF_ELEMENTARY_EDUCATION", "BACHELOR_OF_SECONDARY_EDUCATION" ], "school_type": ["SUC"], "partner_school_restricted": true, "citizenship": "Filipino", "return_service_required": true, "application_window": { "open": "annual_notice", "close": "annual_notice" }, "deadline_type": "estimated", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Income Ceiling Mismatch: Live database currently displays max_income: 400000. Relying
- **Verification:** Verified | Confidence: 92/100
- **Contradictions:**
  - Entry min_gwa (85.00%) differs from renewal Maintain GWA (Maintain required semester GWA prescribed by university (typically 2.0 or 85.00%).)

---

### GBF STEM-College Scholarship (formerly GBF-Gokongwei Group STEM Scholarship for Excellence) (ID: 72)

#### Identity / Affiliations
- **Provider:** Gokongwei Brothers Foundation, Inc. (GBF) in partnership with Gokongwei Group business units
- **Category:** Private / Foundation / Merit-and-Need / STEM Focus
- **Website:** https://www.gokongweibrothersfoundation.org
- **Portal:** GBF Online Portal (bit.ly/GBFSTEMCollege)
- **Guidelines:** GBF STEM-College Scholarship Program Guidelines AY 2026–2027
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Education Level:** College / Undergraduate - Eligible Year Levels: 1st Year (Incoming Freshmen), 2nd Year, 3rd Year, 4th Year, and 5th Year (Continuing Students)
- **Eligible Year Levels:** 1st Year (Incoming Freshmen), 2nd Year, 3rd Year, 4th Year, and 5th Year (Continuing Students)
- **Incoming Freshman Only:** No
- **Existing College Students:** Yes (2nd Year and above)
- **Graduate Students:** No (Applied strictly to first Bachelor's degree; GBF TeachSTEM Masters is a separate graduate track).
- **Current Enrollment:** Enrolled or planning to enroll in a priority STEM degree program at a Philippine university/college
- **Academic Requirements:** General Weighted Average (GWA) of at least 85.00% (or 2.0 / equivalent) with zero failed, dropped, or incomplete grades in high school or college; incoming freshmen must belong to the Top 10% of their SHS graduating batch
- **Minimum GWA:** 85.00% (or 2.0 / equivalent)
- **Alt Class Rank:** Top 10% of Senior High School graduating batch (mandatory requirement for incoming freshmen)
- **Income Ceilings:** Demonstrated financial need (submission of 2025 ITR, Certificate of Employment with salary, or BIR Tax Exemption required)
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Open to public and private universities in the Philippines offering GBF priority STEM degree programs
- **Course Restrictions:** GBF-identified priority STEM degree courses (Engineering, Information Technology, Computer Science, Data Science, Chemistry, Life Sciences, Applied Mathematics, Agriculture, Food Technology)
- **Sectoral / Hidden Requirements:** STEM degree students
- **Good Moral:** Required (good moral standing with active extracurricular/community involvement)
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Must be pursuing first bachelor's degree; willing to fulfill return service obligation

#### Timing
- **Who May Apply:** Incoming college freshmen (Top 10% batch rank) and continuing college students (2nd year and above) enrolled in priority STEM courses.
- **Freshmen:** : Yes
- **Sophomores:** : Yes
- **Juniors:** : Yes
- **Seniors:** : Yes (4th and 5th year continuing STEM students).
- **Graduates:** : No
- **Reapply:** : Yes
- **Opening:** Q1/Q2 annually
- **Closing:** May 31, 2026
- **Cycle:** Annual
- **AY Covered:** AY 2026–2027

#### Benefits (catalog)
- **Tuition:** Direct annual financial grant ranging from PHP 80,000.00 to PHP 120,000.00 (credited directly to scholar's bank account to cover tuition and academic fees).
- **Monthly Stipend:** Integrated into annual financial grant.
- **Allowance:** Integrated into annual financial grant. - Book Allowance: Integrated into annual financial grant.
- **Return Service:** Mandatory return service obligation / commitment to work within Gokongwei Group companies or local STEM industries.

#### Renewal
- **Maintain GWA:** Maintain a minimum GWA of 85.00% (2.0 or equivalent) each academic term.
- **Regular Load:** Full-time credit enrollment in priority STEM course
- **No Failures:** Zero failed, incomplete, or dropped grades

#### Disqualifying / Conflicts
- Enrolling in non-STEM degree programs
- GWA dropping below 85.00% (2.0) or presence of failed, dropped, or incomplete grades
- Incoming freshmen failing to prove Top 10% batch ranking
- Application for second undergraduate degree

#### Required Documents (hidden operational requirements)
- Fully accomplished online application form.
- For Incoming Freshmen: Certified True Copy of Grade 12 Report Card (Form 138 / Form 137), Certificate of Batch Ranking showing Top 10% rank in Grade 12 (or Grade 11), Notice of Admission / Proof of University Application.
- For Continuing Students: Certified True Copy of Grades for the last 2 consecutive semesters, Registration Form for current term.
- Certificate of Good Moral Character.
- Proof of Annual Household Income (2025 ITR, Certificate of Employment with salary, OFW employment contract, Grab/Lalamove earnings record, or BIR Tax Exemption Certificate).
- Recommender's email address (must not be an immediate family member).

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 85.00, "rank_cutoff_alternative": 10, "income_limit": 400000, "priority_courses": [ "ENGINEERING", "INFORMATION_TECHNOLOGY", "COMPUTER_SCIENCE", "DATA_SCIENCE", "CHEMISTRY", "LIFE_SCIENCES", "APPLIED_MATHEMATICS", "AGRICULTURE", "FOOD_TECHNOLOGY" ], "school_type": ["PRIVATE_HEI", "SUC"], "partner_school_restricted": false, "citizenship": "Filipino", "return_service_required": true, "application_window": { "open": "01-15", "close": "05-31" }, "deadline_type": "exact", "[span _710](end_span)cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● GWA Inversion: Live database state currently lists min_gwa: 92. Applying 92% will
- **Verification:** Verified | Confidence: 95/100
- **Contradictions:**
  - Entry min_gwa (85.00% (or 2.0 / equivalent)) differs from renewal Maintain GWA (Maintain a minimum GWA of 85.00% (2.0 or equivalent) each academic term.)

---

### Aboitiz Future Leaders Scholarship Program (Aboitiz Brights) (ID: 75)

#### Identity / Affiliations
- **Provider:** Aboitiz Foundation, Inc.
- **Category:** Private / Foundation / Merit-and-Need / Leadership Development
- **Website:** https://aboitiz.com/aboitiz-foundation/aboitiz-future-leaders-scholarship
- **Portal:** Submitted through partner university scholarship offices via online application portal link
- **Guidelines:** Aboitiz Future Leaders Scholarship Program Guidelines & FAQ
- **Status:** Active ### 2. Purpose The Aboitiz Future Leaders Scholarship empowers talented young Filipinos demonstrating exceptional leadership potential by providing full tertiary education financial support, mentorship, upskilling, and professional development to prepare them as future industry leaders.

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen
- **Residency / Destination:** Nationwide (open to eligible students nationwide enrolled in partner schools)
- **Education Level:** College / Undergraduate
- **Eligible Year Levels:** Year 2 ONLY (Incoming Sophomore Students)
- **Incoming Freshman Only:** No (Incoming Freshmen are strictly barred: "The scholarship is ONLY open to incoming sophomore students who have completed their first year in college").
- **Existing College Students:** Yes (Exclusively incoming 2nd-year / sophomore students).
- **Graduate Students:** No
- **Current Enrollment:** Enrolled in an identified priority degree program at an Aboitiz Foundation partner university
- **Academic Requirements:** Completed 1st year in college with strong academic performance (minimum GWA specified by partner university / foundation rules, typically 88.00% or 2.0 equivalent without failing grades)
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Live database state displays 75; official policy mandates maintaining good academic standing per partner university criteria).
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE (Financial need evaluated, but no rigid income cap published)
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Restricted strictly to Aboitiz Foundation partner universities (e.g., PSAU, UP System, DLSU, UST, Ateneo de Manila)
- **Course Restrictions:** Pre-identified degree programs aligned with Aboitiz Group business units (Engineering, Information Technology, Data Science, Agriculture, Agribusiness, Veterinary Medicine, Finance / Business Administration)
- **Sectoral / Hidden Requirements:** Student leaders / high leadership potential
- **Good Moral:** Required (no record of any form of disciplinary action)
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Current recipients of scholarships from other corporate foundations are NOT eligible under the program

#### Timing
- **Who May Apply:** Incoming sophomore students (Year 2) who have completed their 1st year of college at a partner university.
- **Freshmen:** : No (Incoming freshmen cannot apply; must complete 1st
- **Sophomores:** : Yes (Primary target cohort entering 2nd
- **Juniors:** : No
- **Seniors:** : No
- **Graduates:** : No
- **Reapply:** : No
- **Opening:** Summer period preceding 2nd year intake
- **Closing:** Announced annually via university scholarship offices
- **Cycle:** Fixed / Annual
- **AY Covered:** AY 2025–2026 / AY 2026–2027

#### Benefits (catalog)
- **Tuition:** Full tuition fee coverage.
- **Monthly Stipend:** Direct monthly living allowance.
- **Allowance:** Integrated into monthly living allowance.
- **Return Service:** No post-graduation employment return service required.

#### Renewal
- **Maintain GWA:** Maintain good academic standing each semester per university standards.
- **Regular Load:** Continuous full-time enrollment in priority course.
- **No Failures:** Zero failing grades or disciplinary records. - Return Service: Completion of mandatory 400-hour Aboitiz Group internship and active participation in foundation events.

#### Disqualifying / Conflicts
- Incoming freshmen, 3rd year, or 4th year students.
- Active enjoyment of a scholarship from another corporate foundation.
- Enrollment in a non-partner university or non-priority degree program.
- Presence of disciplinary records or failing grades. ### 10. Temporal Eligibility Matrix User Profile Eligibility Status Actionable Guidance Incoming Freshman College Student Ineligible Strictly barred; must complete 1st year before applying. Incoming Sophomore (2nd Year, Partner HEI, Priority Course) Eligible Now Apply through partner university scholarship office. Incoming Junior or Senior College Student Ineligible Program intake strictly restricted to 2nd-year entry. Recipient of Another Corporate Foundation Grant Ineligible Corporate foundation exclusivity rule applies.

#### Required Documents (hidden operational requirements)
- Copy of Student ID.
- Copy of Certificate of Good Moral Character.
- Certified Copy of College Grades starting 1st year / Transcript of Records. 4. Proof of Enrollment in an approved priority course at a partner university.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [2], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 85.00, "income_limit": null, "priority_courses": [ "ENGINEERING", "INFORMATION_TECHNOLOGY", "DATA_SCIENCE", "AGRICULTURE", "AGRIBUSINESS", "VETERINARY_MEDICINE", "FINANCE", "BUSINESS_ADMINISTRATION" ], "school_type": ["PRIVATE_HEI", "SUC"], "partner_school_restricted": true, "citizenship": "Filipino", "corporate_grant_exclusivity_clause": true, "application_window": { "open": "annual_notice", "close": "annual_notice" }, "deadline_type": "estimated", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Critical Year Level Misconfiguration: Live database state currently lists
- **Verification:** Verified | Confidence: 98/100
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Live database state displays 75; official policy mandates maintaining good academic standing per partner university criteria).) differs from renewal Maintain GWA (Maintain good academic standing each semester per university standards.)
  - Live DB GWA vs official NOT SPECIFIED: NOT SPECIFIED IN OFFICIAL SOURCE (Live database state displays 75; official policy mandates maintaining good academic standing per partner university criteria).

---

## SOURCE: `DATABASE_V3_GROUPC_PRIVATE_FOUNDATIONS_P2.pdf`

**Scholarships in this PDF:** 7

### Security Bank Foundation State Universities Scholarship (Scholars for Better Communities Program) (ID: 58)

#### Identity / Affiliations
- **Provider:** Security Bank Foundation, Inc. (SBFI)
- **Category:** Private / Corporate Foundation / Merit-and-Need
- **Website:** https://www.securitybank.com/foundation
- **Portal:** https://www.securitybank.com/foundation
- **Guidelines:** SBFI Scholars for Better Communities Guidelines
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Must be a natural-born or naturalized Filipino citizen.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** Undergraduate / College.
- **Eligible Year Levels:** Year 1 (Incoming Freshmen) and limited upperclassmen in specific partner SUCs.
- **Incoming Freshman Only:** Primary focus is incoming freshmen; limited upperclassmen entry exists per SUC slot allocation.
- **Existing College Students:** Yes (limited slots at specific partner State Universities and Colleges).
- **Graduate Students:** Ineligible.
- **Current Enrollment:** Must be accepted or enrolled in a partner State University or College, such as Polytechnic University of the Philippines (PUP).
- **Academic Requirements:** Must possess a Grade 12 General Weighted Average (GWA) of at least 93.00% or equivalent, with no subject grade lower than 86.00%, and grades of at least 90.00% in high school subjects aligned with the chosen college degree.
- **Minimum GWA:** 93.00% (Entry GWA cutoff).
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE (Requires documentary proof of financial status via Income Tax Return or Certificate of Indigency; live database records a PHP 350,000.00 ceiling).
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Strictly restricted to designated partner State Universities and Colleges.
- **Course Restrictions:** Degree programs aligned with bank operations, including Accountancy, Business Administration, Finance, Information Technology, Computer Science, Data Analytics, Communications, and Journalism.
- **Sectoral / Hidden Requirements:** Must NOT be a child or dependent of a Security Bank employee, and must not have an immediate family member within the second degree of consanguinity or affinity holding an active SBFI grant.
- **Good Moral:** Required (Certificate of Good Moral Character from high school). - Health Requirements: NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Must carry the full academic load prescribed by the university curriculum per term.

#### Timing
- **Who May Apply:** Graduating Senior High School Grade 12 students entering 1st year college and continuing 1st year SUC students.
- **Freshmen:** : Yes.
- **Sophomores:** : No (unless applying for designated continuing SUC
- **Juniors:** : No.
- **Seniors:** : No.
- **Graduates:** : No.
- **Reapply:** : NOT SPECIFIED IN OFFICIAL SOURCE.
- **Opening:** Announced annually (typically Q1/Q2 prior to the academic year opening).
- **Closing:** Specified in annual call for applications.
- **Cycle:** Fixed / Annual.
- **AY Covered:** AY 2025–2026 / AY 2026–2027. ### 6. Benefits

#### Benefits (catalog)
- **Tuition:** Full or partial tuition and matriculation fee coverage paid directly to the partner state university.
- **Monthly Stipend:** Integrated into the annual educational grant package.
- **Allowance:** Financial assistance package up to PHP 50,000.00 – PHP 60,000.00 per academic year.
- **Return Service:** None mandatory; direct hiring opportunities provided upon graduation.

#### Renewal
- **Maintain GWA:** Maintain a General Weighted Average (GWA) of at least 86.00% or equivalent by the end of each academic term. - Regular Load: Enrolled in the full unit load prescribed by the university curriculum.
- **Regular Load:** Enrolled in the full unit load prescribed by the university curriculum.
- **No Failures:** No grade lower than 80.00% (or equivalent) in any academic subject per term.

#### Disqualifying / Conflicts
- Being a child or dependent of an employee of Security Bank Corporation or its subsidiaries.
- Having an immediate relative within the second degree of consanguinity or affinity holding an active SBFI scholarship.
- Term GWA dropping below 86.00% or receiving a subject grade below 80.00%.
- Enrolling in a non-partner state university or non-aligned degree program. ### 10. Temporal Eligibility Matrix Profile Status Eligibility Status Actionable Guidance Incoming Grade 12 SHS (GWA \ge 93%) Eligible Now Apply through SBFI external application portal upon acceptance at partner SUC. Enrolled SUC Freshman (entering 2nd Year) Conditionally Eligible Eligible only if continuing SUC slots are available for the target institution. Child of Security Bank Employee Never Eligible Ineligible for External Track; must apply under Internal/RMKK Track.

#### Required Documents (hidden operational requirements)
- Duly accomplished SBFI Online Application Form.
- High School Transcript of Records / Grade 12 Report Card showing final GWA.
- Proof of Admission or Acceptance Letter from partner State University. 4. Proof of Financial Status (Latest Parent Income Tax Return, Certificate of Indigency, or OFW Contract).
- PSA Birth Certificate of student applicant. 6. Certificate of Good Moral Character.
- School Grading System documentation (if non-percentage system).

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 93.00, "renewal_gwa": 86.00, "income_limit": null, "partner_school_restricted": true, "priority_courses": [ "ACCOUNTANCY", "FINANCE", "BUSINESS_ADMINISTRATION", "INFORMATION_TECHNOLOGY", "COMPUTER_SCIENCE", "DATA_ANALYTICS", "COMMUNICATIONS", "JOURNALISM" ], "citizenship": "Filipino", "application_window": {"open": "02-01", "close": "05-31"}, "deadline_type": "estimated", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Academic Cutoff Discrepancy: The live production database records a minimum GWA of
- **Verification:** Verified. | Confidence: n/a
- **Contradictions:**
  - Entry min_gwa (93.00% (Entry GWA cutoff).) differs from renewal Maintain GWA (Maintain a General Weighted Average (GWA) of at least 86.00% or equivalent by the end of each academic term. - Regular Load: Enrolled in the full unit load prescribed by the university curriculum.)

---

### Youth Servant Leadership and Education Program (YSLEP) (ID: 59)

#### Identity / Affiliations
- **Provider:** Caritas Manila, Inc.
- **Category:** Private / Faith-Based / Need-and-Merit
- **Website:** https://caritasmanila.org.ph
- **Portal:** Caritas Manila YSLEP Secretariat / Partner Diocesan Offices / NDMU CMRE Office
- **Guidelines:** Caritas Manila YSLEP Application Guidelines and Servant Leadership Formation Manual
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Must be a Filipino citizen.
- **Residency / Destination:** Resident of Metro Manila (Archdiocese of Manila) or any of the 53 partner dioceses nationwide.
- **Education Level:** Tertiary (College Undergraduate) and Technical-Vocational (TVET).
- **Eligible Year Levels:** Years 1, 2, 3, 4, and 5.
- **Incoming Freshman Only:** No.
- **Existing College Students:** Yes.
- **Graduate Students:** Ineligible.
- **Current Enrollment:** Enrolled or accepted in an accredited university, college, or TVET institution.
- **Academic Requirements:** Senior High School overall GWA of at least 85.00% or equivalent.
- **Minimum GWA:** 85.00% (Entry and retention cutoff).
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE (Requires a Certificate of Indigency from the Barangay or DSWD verifying financial distress; live database specifies PHP 180,000.00).
- **Age Restrictions:** Must be between 18 and 25 years old at the time of application.
- **School / Consortium Restrictions:** Accredited partner institutions within participating dioceses.
- **Course Restrictions:** Open to all degree programs; includes a dedicated track (YSLEP-GEN129) prioritizing Agriculture degrees and sustainable farming.
- **Sectoral / Hidden Requirements:** Must be single; must be an active member of a Basic Ecclesial Community (GKK) or Parish Youth Ministry.
- **Good Moral:** Required (Certificate of Good Moral Character).
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Zero-tolerance policy regarding vices (smoking, alcohol consumption, substance abuse, gambling, and computer game addiction); must NOT hold a Grant-in-Aid Working Student (GIA/WS) award from the school.

#### Timing
- **Who May Apply:** Single Senior High School graduates and continuing college or TVET students aged 18 to 25.
- **Freshmen:** : Yes.
- **Sophomores:** : Yes.
- **Juniors:** : Yes.
- **Seniors:** : Yes.
- **Graduates:** : No.
- **Reapply:** : Yes.
- **Opening:** Set annually by local diocesan YSLEP secretariats.
- **Closing:** Determined per participating diocese.
- **Cycle:** Fixed / Annual.
- **AY Covered:** AY 2025–2026 / AY 2026–2027.

#### Benefits (catalog)
- **Tuition:** Direct financial grant covering matriculation and tuition fees.
- **Monthly Stipend:** Integrated into the overall annual educational allowance.
- **Allowance:** Annual financial support package valued at approximately PHP 30,000.00 – PHP 35,000.00 per scholar.
- **Return Service:** Post-graduation pledge ("Balik-Handog"): Join the Caritas YSL Alumni Association (CAMASA) and donate 1% of gross monthly salary (or a minimum of PHP 100.00/month) upon employment to finance future scholars.

#### Renewal
- **Maintain GWA:** Maintain a general average of at least 85.00% per academic term.
- **Regular Load:** Full-time credit load; shifting degree programs without approval is barred.
- **No Failures:** Passing grades in all enrolled subjects.

#### Disqualifying / Conflicts
- Marriage, pregnancy, or exceeding 25 years of age.
- Engagement in vices (smoking, alcohol, gambling, illegal drugs, or gaming addiction).
- Holding a school Grant-in-Aid Working Student (GIA/WS) grant or major external award.
- Term GWA dropping below 85.00% or unapproved shifting of degree program.
- Failure to attend mandatory monthly YSL formation workshops or complete 50 annual volunteer hours.

#### Required Documents (hidden operational requirements)
- Accomplished Caritas Manila YSLEP Application Form.
- Photocopy of SHS Report Card / College Transcript showing GWA \ge 85.00%.
- Certificate of Good Moral Character.
- PSA Birth Certificate or Baptismal Certificate.
- Certificate of Indigency from Barangay or DSWD.
- Parents' Marriage Certificate (photocopy).
- Two (2) 2x2 ID photos.
- Interview clearance from local Screening Committee.

#### Recommended Schema / Fields
```json
{ "education_level": ["College", "TVET"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 85.00, "renewal_gwa": 85.00, "income_limit": null, "age_limit": 25, "sectoral_restriction": "PARISH_YOUTH_MINISTRY_MEMBER", "partner_school_restricted": false, "citizenship": "Filipino", "application_window": {"open": "annual_notice", "close": "annual_notice"}, "deadline_type": "estimated", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Database GWA Understatement: Live production database lists min_gwa: 80. Official
- **Verification:** Verified. | Confidence: 88/100.
- **Contradictions:**
  - Entry min_gwa (85.00% (Entry and retention cutoff).) differs from renewal Maintain GWA (Maintain a general average of at least 85.00% per academic term.)

---

### AFPSLAI Educational Grant Program (EGP) — Non-Business Track (ID: 62)

#### Identity / Affiliations
- **Provider:** Armed Forces and Police Savings and Loan Association, Inc. (AFPSLAI)
- **Category:** Private / Affiliation / Need-and-Merit
- **Website:** https://www.afpslai.com.ph
- **Portal:** Physical submission at nearest AFPSLAI branch office (forms downloadable online)
- **Guidelines:** AFPSLAI Educational Grant Program (EGP) Policy Guidelines & Form EGP
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Must be a Filipino citizen.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** Undergraduate / College.
- **Eligible Year Levels:** Year 1 (Incoming Freshmen), Year 2 (Sophomores), and Year 3 (Juniors).
- **Incoming Freshman Only:** No.
- **Existing College Students:** Yes (2nd and 3rd year college students; 4th year students are strictly barred).
- **Graduate Students:** Ineligible.
- **Current Enrollment:** Accepted or enrolled in a non-business baccalaureate degree program.
- **Academic Requirements:** Proof of highest educational attainment demonstrating passing academic standing.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Passing academic standing required; live database records 85.00%).
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** Total annual gross family income of the sponsor must not exceed PHP 1,000,000.00.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Recognized Philippine colleges and universities.
- **Course Restrictions:** Restricted EXCLUSIVELY to non-business baccalaureate courses (e.g., Computer Science, IT, Engineering, Social Sciences, Agriculture, Science). Business-related courses are covered under the separate Scholarship Apprentice Program).
- **Sectoral / Hidden Requirements:** Sponsor must be an active, retired, or deceased Regular Member of AFPSLAI in good standing. Applicant must be a legitimate, illegitimate, or legally adopted child. If sponsor is single/unmarried without children, a legitimate/adopted sibling may apply.
- **Good Moral:** Required (Certificate of Good Moral Character).
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Strictly limited to ONE (1) grantee per sponsor/family; applicant must NOT hold any other external scholarship grant (except school merit tuition discounts).

#### Timing
- **Who May Apply:** Dependents (children or qualified siblings) of regular AFPSLAI members who are incoming freshmen, 2nd-year, or 3rd-year college students.
- **Freshmen:** : Yes.
- **Sophomores:** : Yes.
- **Juniors:** : Yes.
- **Seniors:** : No (4th-year students are ineligible).
- **Graduates:** : No.
- **Reapply:** : No (if another family member was a prior grantee).
- **Opening:** Announced annually (typically May/June).
- **Closing:** Specified per cycle (e.g., June 26 or July 15).
- **Cycle:** Fixed / Annual. - Current AY Covered: AY 2026–2027.
- **AY Covered:** AY 2026–2027.

#### Benefits (catalog)
- **Tuition:** Up to PHP 30,000.00 per school term (and up to PHP 10,000.00 for mandatory summer/midyear terms).
- **Monthly Stipend:** PHP 4,000.00 per month.
- **Allowance:** ROTC incentive of PHP 2,000.00 per month during terms when ROTC is enrolled.
- **Return Service:** None required for EGP track (unlike the SAP business track which requires a 6-to-11 month service bond).

#### Renewal
- **Maintain GWA:** Maintain passing academic standing per university curriculum.
- **Regular Load:** Full-time credit enrollment.
- **No Failures:** No failing or dropped subjects. - Return Service: None.

#### Disqualifying / Conflicts
- Total gross annual family income exceeding PHP 1,000,000.00.
- Being in the 4th year level or pursuing a graduate degree.
- Enrolling in a business-related degree program under the EGP track.
- Application where a family member / sibling was a previous AFPSLAI scholar.
- Dual enjoyment of external non-school scholarship grants.
- Submission of Barangay clearance instead of Police/NBI clearance.

#### Required Documents (hidden operational requirements)
- Duly accomplished AFPSLAI EGP Application Form.
- PSA Birth Certificate of applicant.
- Report Cards / Certified True Copy of Grades / TOR.
- Certificate of Good Moral Character.
- Valid Police Clearance or NBI Clearance of applicant (Barangay clearance strictly barred).
- Parent/Sponsor Proof of Income: Latest payslip / Certificate of Pension (COP) AND latest Income Tax Return (ITR) for both parents.
- Official Local Government Certificate of No Income / Affidavit if parent is unemployed.
- PSA CENOMAR and Affidavit of No Child (if sponsor is a sibling).

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": null, "income_limit": 1000000, "parent_employment_restriction": "AFPSLAI_REGULAR_MEMBER", "course_track_restriction": "NON_BUSINESS_COURSES", "partner_school_restricted": false, "citizenship": "Filipino", "application_window": {"open": "05-01", "close": "06-26"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Income Limit Discrepancy: Live production database lists max_income: 500000. Updated
- **Verification:** Verified. | Confidence: 96/100.
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Passing academic standing required; live database records 85.00%).) differs from renewal Maintain GWA (Maintain passing academic standing per university curriculum.)
  - Live DB GWA vs official NOT SPECIFIED: NOT SPECIFIED IN OFFICIAL SOURCE (Passing academic standing required; live database records 85.00%).

---

### Security Bank Foundation Scholars for Better Communities Scholarship Program (External) (ID: 71)

#### Identity / Affiliations
- **Provider:** Security Bank Foundation, Inc. (SBFI)
- **Category:** Private / Corporate Foundation / Merit-and-Need
- **Website:** https://www.securitybank.com/foundation
- **Portal:** https://www.securitybank.com/foundation
- **Guidelines:** SBFI External Scholarship Program Guidelines
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Must be a Filipino citizen.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE (Live database records NCR region filter).
- **Education Level:** Undergraduate / College.
- **Eligible Year Levels:** Year 1 (Incoming Freshmen) and limited upperclassmen in designated partner HEIs.
- **Incoming Freshman Only:** Primary entry is incoming 1st year; limited upperclassmen slots exist per university.
- **Existing College Students:** Yes (limited slots).
- **Graduate Students:** Ineligible.
- **Current Enrollment:** Accepted or enrolled in any of SBFI's 8 partner universities (Ateneo de Manila University, De La Salle University, Far Eastern University, Polytechnic University of the Philippines, University of Santo Tomas, etc.).
- **Academic Requirements:** High school Grade 12 GWA of at least 93.00% or equivalent; no subject grade lower than 86.00%; grades of 90.00%+ in subjects aligned with college course.
- **Minimum GWA:** 93.00% (Entry) / 86.00% (Continuation).
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE (Requires parent ITR, Indigency Certificate, or OFW Contract).
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Strictly restricted to SBFI's 8 partner universities. - Priority Courses: Business Administration, Finance, Accountancy, Financial Management, Information Technology, Computer Science, Data Analytics, Communications, and Journalism.
- **Course Restrictions:** Business Administration, Finance, Accountancy, Financial Management, Information Technology, Computer Science, Data Analytics, Communications, and Journalism.
- **Sectoral / Hidden Requirements:** Must NOT be a child of a Security Bank employee, and must not have an active SBFI scholar relative within the second degree.
- **Good Moral:** Required.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Must maintain full-time credit enrollment per term.

#### Timing
- **Who May Apply:** Graduating SHS Grade 12 students and continuing 1st-year students at partner HEIs.
- **Freshmen:** : Yes.
- **Sophomores:** : No (unless occupying open continuing slots).
- **Juniors:** : No.
- **Seniors:** : No.
- **Graduates:** : No. - Can previous applicants reapply?: NOT SPECIFIED IN
- **Reapply:** : NOT SPECIFIED IN
- **Opening:** Announced per annual cycle.
- **Closing:** Announced per annual cycle.
- **Cycle:** Fixed / Annual.
- **AY Covered:** AY 2025–2026 / AY 2026–2027.

#### Benefits (catalog)
- **Tuition:** Full or partial tuition and matriculation fee coverage paid directly to the university.
- **Monthly Stipend:** Integrated into educational grant package.
- **Allowance:** Annual educational allowance package provided.
- **Return Service:** None mandatory.

#### Renewal
- **Maintain GWA:** Term GWA of at least 86.00%.
- **Regular Load:** Enrolled in prescribed full unit load per term.
- **No Failures:** No grade lower than 80.00% in any subject.

#### Disqualifying / Conflicts
- Parent being an employee of Security Bank Corporation or its affiliates.
- Having a relative within the second degree of consanguinity/affinity actively holding an SBFI scholarship.
- Term GWA dropping below 86.00% or subject grade below 80.00%.
- Enrolling in a non-partner university or non-priority program.

#### Required Documents (hidden operational requirements)
- Accomplished SBFI External Scholarship Online Application Form.
- High School Transcript / Grade 12 Report Card showing final GWA.
- Acceptance / Admission Letter from partner university.
- Proof of Financial Status (Parent ITR, Indigency Certificate, or OFW Contract).
- PSA Birth Certificate.
- Certificate of Good Moral Character. 7. School Grading System and Course Curriculum.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 93.00, "renewal_gwa": 86.00, "income_limit": null, "partner_school_restricted": true, "priority_courses": [ "ACCOUNTANCY", "FINANCE", "BUSINESS_ADMINISTRATION", "INFORMATION_TECHNOLOGY", "COMPUTER_SCIENCE", "DATA_ANALYTICS", "COMMUNICATIONS", "JOURNALISM" ], "citizenship": "Filipino", "application_window": {"open": "02-01", "close": "05-31"}, "deadline_type": "estimated", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Database URL Corruption: Live database lists an incorrect portal URL
- **Verification:** Verified. - Last Verified Date: 2026-08-05. | Confidence: 95/100.
- **Contradictions:**
  - Entry min_gwa (93.00% (Entry) / 86.00% (Continuation).) differs from renewal Maintain GWA (Term GWA of at least 86.00%.)

---

### Regalo Mo, Kinabukasan Ko (RMKK) Scholarship Program (Agency Personnel Track) (ID: 111)

#### Identity / Affiliations
- **Provider:** Security Bank Foundation, Inc. (SBFI)
- **Category:** Private / Corporate CSR / Affiliation-and-Need
- **Website:** https://www.securitybank.com/foundation
- **Portal:** SBFI Internal / Agency Personnel Application Portal
- **Guidelines:** SBFI Regalo Mo, Kinabukasan Ko Program Guidelines
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Must be a Filipino citizen.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** Elementary, High School, Senior High School, and College.
- **Eligible Year Levels:** College Years 1, 2, 3, and 4.
- **Incoming Freshman Only:** No.
- **Existing College Students:** Yes.
- **Graduate Students:** Ineligible.
- **Current Enrollment:** Enrolled in an accredited educational institution.
- **Academic Requirements:** Passing GWA (typically \ge 80.00% or equivalent).
- **Minimum GWA:** 80.00%.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** Targeted at low-income third-party agency staff assigned to Security Bank; live database records a PHP 250,000.00 income cap.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Recognized schools, colleges, and universities.
- **Course Restrictions:** Open to various undergraduate degree programs (e.g., Business Administration, Marketing Management, Education).
- **Sectoral / Hidden Requirements:** Sponsor must be an active third-party agency staff member (e.g., security guard, janitor) assigned to Security Bank Corporation or a legitimate child/dependent.
- **Good Moral:** Required.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Agency personnel sponsor must be in active service with Security Bank's accredited staffing agencies.

#### Timing
- **Who May Apply:** Security Bank agency personnel and their legitimate children.
- **Freshmen:** : Yes.
- **Sophomores:** : Yes.
- **Juniors:** : Yes.
- **Seniors:** : Yes.
- **Graduates:** : No.
- **Reapply:** : Yes.
- **Opening:** Announced annually via SBFI CSR advisories.
- **Closing:** Specified in internal notices.
- **Cycle:** Fixed / Annual.
- **AY Covered:** AY 2025–2026 / AY 2026–2027.

#### Benefits (catalog)
- **Tuition:** Direct educational assistance grant credited toward tuition/fees.
- **Monthly Stipend:** Integrated into educational support grant.
- **Allowance:** Tiered annual financial assistance: Elementary (PHP 25,000.00), High School (PHP 27,000.00), Senior High School (PHP 30,000.00), College (PHP 60,000.00 per year).
- **Return Service:** None; direct employment preference at Security Bank upon graduation.

#### Renewal
- **Maintain GWA:** Maintain passing GWA (\ge 80.00%) each academic year.
- **Regular Load:** Continuous enrollment.
- **No Failures:** Passing grades in all enrolled subjects.

#### Disqualifying / Conflicts
- Separation or termination of the sponsor agency personnel from Security Bank assignment.
- Failure to maintain passing academic grades.
- Fraudulent representation of employment or dependency.

#### Required Documents (hidden operational requirements)
- Accomplished SBFI RMKK Application Form.
- Certificate of Employment of Agency Personnel parent from accredited Security Bank agency.
- PSA Birth Certificate of student applicant.
- Report Card / College Transcript of Records showing passing grades.
- Certificate of Enrollment / Registration Card.
- Certificate of Good Moral Character.

#### Recommended Schema / Fields
```json
{ "education_level": ["Elementary", "High School", "Senior High School", "College"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 80.00, "income_limit": 250000, "sectoral_restriction": "SECURITY_BANK_AGENCY_PERSONNEL_DEPENDENT", "partner_school_restricted": false, "citizenship": "Filipino", "application_window": {"open": "annual_notice", "close": "annual_notice"}, "deadline_type": "estimated", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Benefit Understatement: Live database lists total_value: 30000. Official college award
- **Verification:** Verified. | Confidence: 92/100.
- **Contradictions:**
  - Entry min_gwa (80.00%.) differs from renewal Maintain GWA (Maintain passing GWA (\ge 80.00%) each academic year.)

---

### GBF STEM-College Scholarship (Formerly GBF-Gokongwei Group STEM Scholarship for Excellence) (ID: 72)

#### Identity / Affiliations
- **Provider:** Gokongwei Brothers Foundation, Inc. (GBF)
- **Category:** Private / Corporate Foundation / Merit-and-Need
- **Website:** https://www.gokongweibrothersfoundation.org
- **Portal:** https://bit.ly/GBFSTEMCollege
- **Guidelines:** GBF STEM-College Scholarship Program Guidelines
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Must be a natural-born or naturalized Filipino citizen.
- **Residency / Destination:** Resident of the Philippines.
- **Education Level:** Undergraduate / College.
- **Eligible Year Levels:** Year 1 (Incoming Freshmen) and Year 2+ (Continuing College Students).
- **Incoming Freshman Only:** No.
- **Existing College Students:** Yes (2nd year and above).
- **Graduate Students:** Ineligible for College Track (Separate TeachSTEM Master's exists).
- **Current Enrollment:** Enrolled or planning to enroll in a priority STEM degree program in a recognized Philippine university.
- **Academic Requirements:** Minimum overall General Weighted Average (GWA) of 85.00% or 2.0 (or equivalent); incoming freshmen must belong to the Top 10% of their Senior High School graduating batch.
- **Minimum GWA:** 85.00% or 2.0.
- **Alt Class Rank:** Top 10% of SHS batch for incoming freshmen.
- **Income Ceilings:** Must demonstrate financial need; proof of annual household income required (Live database specifies PHP 400,000.00 cap).
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Philippine colleges and universities offering accredited priority STEM programs.
- **Course Restrictions:** GBF Priority STEM Courses including Chemical Engineering, Civil Engineering, Computer Engineering, Electrical Engineering, Electronics Engineering, Industrial Engineering, Mechanical Engineering, Materials Engineering, Mining Engineering, Geodetic Engineering, Computer Science, Information Technology, Data Science, Chemistry, Accountancy, Animal Science, and Avionics Technology.
- **Sectoral / Hidden Requirements:** None.
- **Good Moral:** Required (Certificate of Good Moral Character).
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Must have NO failing (5.0), dropped, or incomplete (INC) grades in high school or prior college semesters; must not hold another major corporate scholarship grant.

#### Timing
- **Who May Apply:** Graduating Grade 12 SHS students and continuing college students (2nd year and above) enrolled in priority STEM programs.
- **Freshmen:** : Yes (as incoming 1st year or entering 2nd year).
- **Sophomores:** : Yes.
- **Juniors:** : Yes.
- **Seniors:** : Yes.
- **Graduates:** : No.
- **Reapply:** : Yes.
- **Opening:** Announced annually (typically Q1/Q2).
- **Closing:** May 31, 2026 (for AY 2026–2027 cycle).
- **Cycle:** Fixed / Annual.
- **AY Covered:** AY 2026–2027.

#### Benefits (catalog)
- **Tuition:** Covered as part of the direct financial grant package.
- **Monthly Stipend:** Integrated into the annual financial grant.
- **Allowance:** Direct annual financial grant of PHP 80,000.00 to PHP 120,000.00 per year (depending on the university, directly credited to scholar's bank account).
- **Return Service:** Mandatory return service obligation (render service in the Philippines or within Gokongwei Group companies equal to scholarship period).

#### Renewal
- **Maintain GWA:** Maintain a term GWA of at least 85.00% or 2.0.
- **Regular Load:** Full-time credit enrollment in approved STEM program.
- **No Failures:** Zero failing, incomplete, or dropped grades.

#### Disqualifying / Conflicts
- Enrolling in non-STEM degree programs.
- Term GWA dropping below 85.00% or receiving a failing, dropped, or incomplete mark.
- Failure to submit proof of top 10% class rank for incoming freshman entry.
- Holding an overlapping major corporate scholarship.

#### Required Documents (hidden operational requirements)
- Certified True Copy of Grade 12 Report Card (for Freshmen) OR Certified True Copy of Grades for last 2 consecutive semesters (for Upperclassmen).
- Certificate of Class Rank (Top 10% certification for incoming freshmen).
- Notice of Admission or Proof of University Application.
- Certificate of Good Moral Character.
- Proof of Household Income (Parent ITR, Certificate of Employment with salary, OFW contract, or BIR Tax Exemption Certificate).
- Proof of Billing (Utility bill matching residence address).
- Recommender's email address (Non-relative reference). ### 8. Renewal Requirements ● Maintain GWA: Maintain a term GWA of at least 85.00% or 2.0. ● Regular Load: Full-time credit enrollment in approved STEM program. ● No Failures: Zero failing, incomplete, or dropped grades. ● Return Service: Compliance with post-graduation return service agreement.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 85.00, "renewal_gwa": 85.00, "rank_cutoff_alternative": 10, "income_limit": 400000, "priority_courses": [ "CHEMICAL_ENGINEERING", "CIVIL_ENGINEERING", "COMPUTER_ENGINEERING", "ELECTRICAL_ENGINEERING", "ELECTRONICS_ENGINEERING", "INDUSTRIAL_ENGINEERING", "MECHANICAL_ENGINEERING", "COMPUTER_SCIENCE", "INFORMATION_TECHNOLOGY", "DATA_SCIENCE", "CHEMISTRY", "ACCOUNTANCY" ], "partner_school_restricted": false, "citizenship": "Filipino", "application_window": {"open": "01-15", "close": "05-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "return_service_required": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Database Portal URL Correction: Live database link points to aggregator
- **Verification:** Verified. | Confidence: 94/100.
- **Contradictions:**
  - Entry min_gwa (85.00% or 2.0.) differs from renewal Maintain GWA (Maintain a term GWA of at least 85.00% or 2.0.)

---

### Aboitiz Future Leaders Scholarship Program (AFLSP) / Aboitiz Brights (ID: 75)

#### Identity / Affiliations
- **Provider:** Aboitiz Foundation, Inc.
- **Category:** Private / Corporate Foundation / Merit-based
- **Website:** https://aboitiz.com/aboitiz-foundation/aboitiz-future-leaders-scholarship
- **Portal:** https://sites.google.com/aboitiz.com/aboitiz-future-leaders-scholar/home AND University Scholarship Portals (e.g., UP SIKAP portal https://sikap.upd.edu.ph)
- **Guidelines:** Aboitiz Future Leaders Scholarship Program Guidelines AY 2025–2026 / AY 2026–2027
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Must be a Filipino citizen.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** Undergraduate / College.
- **Eligible Year Levels:** Year 2 (Incoming Sophomores ONLY).
- **Incoming Freshman Only:** NO (Incoming Freshmen are strictly INELIGIBLE).
- **Existing College Students:** YES (Strictly restricted to incoming 2nd-year college students).
- **Graduate Students:** Ineligible.
- **Current Enrollment:** Enrolled as an incoming sophomore student at a designated partner university.
- **Academic Requirements:** First-year college GWA/GPA of at least 88.00% or 2.0 (or equivalent); NO dropped subjects, NO failing grades (5.0), and NO unremoved incomplete (INC) or 4.0 grades in any academic subject.
- **Minimum GWA:** 88.00% or 2.00.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE (Requires submission of household financial proof or Affidavit of Income).
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to designated partner universities: Ateneo de Manila University, De La Salle University, Mapúa University, University of Santo Tomas, UP Diliman, UP Baguio, UP Cebu, UP Los Baños, and UP Mindanao.
- **Course Restrictions:** Engineering (Electrical, Industrial, Civil, Chemical, Computer, Mechanical, Materials, Mining, Geodetic, Electronics), Data Science, Computer Science, BA Communication / Journalism, BS Agriculture, BS Forestry, BS Psychology.
- **Sectoral / Hidden Requirements:** None.
- **Good Moral:** Required (Certificate of Good Moral Character; no record of any form of disciplinary action).
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Applicants receiving scholarships from other corporate foundations are ineligible (CHED and DOST scholars are allowed).

#### Timing
- **Who May Apply:** Incoming 2nd-year college (sophomore) students enrolled in pre-identified courses at partner universities.
- **Freshmen:** : No (Must complete 1st year to apply as an incoming
- **Sophomores:** : Yes (Primary and exclusive target applicant cohort).
- **Juniors:** : No.
- **Seniors:** : No.
- **Graduates:** : No.
- **Reapply:** : Yes (if entering sophomore year).
- **Opening:** August 1 annually.
- **Closing:** September 1 annually.
- **Cycle:** Fixed / Annual.
- **AY Covered:** AY 2025–2026 / AY 2026–2027.

#### Benefits (catalog)
- **Tuition:** Full 100% tuition and matriculation fee coverage.
- **Monthly Stipend:** PHP 10,000.00 per month.
- **Allowance:** Board Exam Review Fee allowance of PHP 15,000.00.
- **Return Service:** No mandatory employment return service bond; scholars must complete a mandatory 400-hour internship within Aboitiz Group business units and attend leadership development sessions.

#### Renewal
- **Maintain GWA:** Maintain required term GWA (at least 88.00% / 2.0).
- **Regular Load:** Full credit load per term.
- **No Failures:** Zero failing grades (5.0), dropped marks (DRP), or unremoved incomplete (INC/4.0) grades.

#### Disqualifying / Conflicts
- Being an incoming freshman, 3rd-year, or 4th-year college student.
- Enrolling in a non-partner university or non-identified degree program.
- Having any grade of 5.0, DRP, or unremoved INC/4.0 mark in 1st year college.
- Holding an active scholarship grant from another corporate foundation.
- First-year GWA dropping below 88.00% or 2.0.

#### Required Documents (hidden operational requirements)
- Copy of Student ID.
- Certificate of Good Moral Character.
- Certified True Copy of Grades / Transcript of Records covering full 1st year college.
- Certificate of Enrollment / Registration Form for 1st and 2nd term of current SY.
- Copy of Certificates of College Leadership, Awards, or Seminars.
- Proof of Household Income / Affidavit of Income Source.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [2], "incoming_year_only": false, "requires_current_enrollment ": true, "minimum_gwa": 88.00, "renewal_gwa": 88.00, "income_limit": null, "partner_school_restricted": true, "priority_courses": [ "ELECTRICAL_ENGINEERING", "INDUSTRIAL_ENGINEERING", "CIVIL_ENGINEERING", "CHEMICAL_ENGINEERING", "COMPUTER_ENGINEERING", "MECHANICAL_ENGINEERING", "MATERIALS_ENGINEERING", "MINING_ENGINEERING", "GEODETIC_ENGINEERING", "ELECTRONICS_ENGINEERING", "DATA_SCIENCE", "COMPUTER_SCIENCE", "COMMUNICATION", "JOURNALISM", "AGRICULTURE", "FORESTRY", "PSYCHOLOGY" ], "citizenship": "Filipino", "application_window": {"open": "08-01", "close": "09-01"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "return_service_required": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Critical GWA & Year Level Database Error: Live production database lists min_gwa: 75
- **Verification:** Verified. | Confidence: 95/100.
- **Contradictions:**
  - Entry min_gwa (88.00% or 2.00.) differs from renewal Maintain GWA (Maintain required term GWA (at least 88.00% / 2.0).)

---

## SOURCE: `DATABASE_V3_GROUPC_UNIFAST_CHED.pdf`

**Scholarships in this PDF:** 5

### CHED-UniFAST Tulong Dunong Program (CHED-TDP / UniFAST-TDP) (ID: 5)

#### Identity / Affiliations
- **Provider:** Unified Student Financial Assistance System for Tertiary Education (UniFAST) / Commission on Higher Education (CHED)
- **Category:** Government / National / Undergraduate / Need-based Grant-in-Aid
- **Website:** https://unifast.gov.ph
- **Portal:** https://unifast.gov.ph/tes.html
- **Guidelines:** CHED-DBM Joint Memorandum Circular (JMC) No. 04, s. 2019; UniFAST Memorandum Circular No. 02, s. 2026
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Education Level:** Undergraduate / College
- **Eligible Year Levels:** 1st, 2nd, 3rd, 4th, and 5th Year
- **Incoming Freshman Only:** No
- **Existing College Students:** Yes
- **Graduate Students:** No
- **Current Enrollment:** Must be enrolled in a first undergraduate degree in State Universities and Colleges (SUCs), CHED-recognized Local Universities and Colleges (LUCs) with Certificate of Program Compliance (COPC), or Private Higher Education Institutions (HEIs) with COPC or listed in the CHED Registry
- **Academic Requirements:** Senior High School report card / Form 138 (for incoming freshmen) or a certified true copy of grades for the latest semester attended (for ongoing college students)
- **Minimum GWA:** 75.00% (passing grade)
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined annual gross family income of parents or legal guardians must not exceed ₱400,000.00
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Restricted to SUCs, CHED-recognized LUCs with COPC, or Private HEIs with COPC / included in the CHED Registry of Programs
- **Course Restrictions:** Any recognized undergraduate degree program
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Good Moral:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Applicants must not be availing of multiple national government-funded educational grants, except for Free Higher Education under Republic Act 10931, DSWD AICS, or Student Monetary Assistance for Recovery and Transition (SMART)

#### Timing
- **Who May Apply:** Graduating high school students, incoming college freshmen, and ongoing undergraduate college students
- **Freshmen:** : Yes
- **Sophomores:** : Yes
- **Juniors:** : Yes
- **Seniors:** : Yes
- **Graduates:** : No
- **Reapply:** : Yes (grantees must reapply or re-confirm qualification
- **Opening:** Varies by CHED Regional Office (CHEDRO) and partner institution schedule
- **Closing:** September 30 per JMC guidelines / as announced by regional advisories
- **Cycle:** Annual (disbursed semestrally at ₱7,500.00 per term)
- **AY Covered:** AY 2024–2025 / AY 2025–2026

#### Benefits (catalog)
- **Tuition:** Included in the financial grant (up to ₱15,000.00 per AY; serves as a direct subsidy in SUCs/LUCs where tuition is covered under RA 10931)
- **Monthly Stipend:** NOT SPECIFIED IN OFFICIAL SOURCE (Integrated into general living allowance)
- **Allowance:** ₱15,000.00 per academic year (₱7,500.00 per semester)
- **Return Service:** None

#### Renewal
- **Maintain GWA:** Maintain a passing General Weighted Average (GWA) of at least 75.00%
- **Regular Load:** Carry a regular academic credit load per semester as determined by the HEI
- **No Failures:** Maintain passing standing across all enrolled subjects

#### Disqualifying / Conflicts
- Concurrent enjoyment of major national government educational scholarship grants (excluding RA 10931 Free Tuition and DSWD AICS)
- Combined annual family gross income exceeding ₱400,000.00
- Enrollment in non-COPC degree programs or non-recognized private institutions
- Failure to maintain a passing GWA or regular credit load

#### Required Documents (hidden operational requirements)
- Fully accomplished UniFAST-TDP Application Form (Annex 2) 2. Certificate of Enrollment (COE) or Certificate of Registration (COR) 3. Certificate of Indigency issued by the Barangay, latest BIR Form 2316 / Income Tax Return, BIR Certificate of Tax Exemption, or Social Case Study Report 4. Academic Record: Form 138 / SF9 for incoming freshmen, or Certified True Copy of Grades for the latest semester attended for ongoing students

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 75.00, "income_limit": 400000, "rank_cutoff_alternative": null, "priority_courses": null, "school_type": ["SUC", "LUC", "Private HEI with COPC"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "06-01", "close": "09-30"}, "deadline_type": "institution_dependent", "cycle_type": "annual", "renewable": true, "first_time_only": false, "return_service_required": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Program Compliance Risk: Applicants enrolled in HEI programs lacking COPC
- **Verification:** Verified | Confidence: n/a
- **Contradictions:**
  - Entry min_gwa (75.00% (passing grade)) differs from renewal Maintain GWA (Maintain a passing General Weighted Average (GWA) of at least 75.00%)

---

### CHED-UniFAST Tertiary Education Subsidy (TES) (enacted under Republic Act No. 10931, Universal Access to Quality Tertiary Education Act) (ID: 66)

#### Identity / Affiliations
- **Provider:** Unified Student Financial Assistance System for Tertiary Education (UniFAST) / Commission on Higher Education (CHED)
- **Category:** Government / National / Undergraduate / Need-based Subsidy
- **Website:** https://unifast.gov.ph
- **Portal:** UniFAST Portal / HEI-administered Portal
- **Guidelines:** CHED-UniFAST-DBM Joint Memorandum Circular No. 01 s. 2017; JMC No. 04 s. 2020; Memorandum Circular No. 1 s. 2021 (TES-3B)
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen
- **Residency / Destination:** Priority given to students residing and studying in municipalities without public university campuses
- **Education Level:** Undergraduate / College
- **Eligible Year Levels:** 1st, 2nd, 3rd, 4th, and 5th Year
- **Incoming Freshman Only:** No
- **Existing College Students:** Yes
- **Graduate Students:** No
- **Current Enrollment:** Must be enrolled in an undergraduate degree program in an SUC, CHED-recognized LUC, or private HEI included in the UniFAST Registry
- **Academic Requirements:** Passing GWA and regular academic credit load per term
- **Minimum GWA:** 75.00% (passing grade per HEI retention standards)
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Dynamically evaluated based on DSWD Listahan 2.0 / 4Ps household income ranking and poverty threshold deciles
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** SUCs, LUCs with institutional recognition, or private HEIs in the official UniFAST Registry
- **Course Restrictions:** Any recognized undergraduate degree program
- **Sectoral / Hidden Requirements:** Priority given to 4Ps / Listahan households, Persons with Disabilities (TES-3A), and students in municipalities without public SUC/LUC campuses
- **Good Moral:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Evaluated via UniFAST prioritization hierarchy: (1) Continuing StuFAPs grantees, (2) Listahan 2.0 / 4Ps ranked households, (3) Municipality exclusivity applicants

#### Timing
- **Who May Apply:** Enrolled undergraduate students submitted by their respective HEIs during official UniFAST portal intake calls
- **Freshmen:** : Yes
- **Sophomores:** : Yes
- **Juniors:** : Yes
- **Seniors:** : Yes
- **Graduates:** : No (except claiming TES-3B licensure reimbursement within 2
- **Reapply:** : Yes (continuing grantees are re-validated semestrally)
- **Opening:** Set by UniFAST per academic billing cycle
- **Closing:** Specified in UniFAST regional advisories
- **Cycle:** Annual prioritization / Semestral disbursement
- **AY Covered:** AY 2024–2025 / AY 2025–2026

#### Benefits (catalog)
- **Tuition:** TES-1 covers full tuition and school fees in private HEIs (up to ₱20,000.00/sem or ₱40,000.00/AY)
- **Monthly Stipend:** Integrated into living allowance (TES-2)
- **Allowance:** TES-2 living allowance: up to ₱40,000.00 per AY (₱20,000.00 per semester)
- **Return Service:** None

#### Renewal
- **Maintain GWA:** Maintain a passing GWA per semester according to HEI retention rules
- **Regular Load:** Enrolled in a regular credit load per term
- **No Failures:** Compliance with academic standing requirements

#### Disqualifying / Conflicts
- Enrollment in non-registered private HEIs or non-compliant programs
- Exceeding the maximum residency period of the degree program
- Failure to maintain passing GWA or academic dismissal from the HEI
- Possession of an earned post-secondary or college degree

#### Required Documents (hidden operational requirements)
- Certificate of Enrollment / Registration Form (COR) from UniFAST-registered HEI
- DSWD 4Ps / Listahan Household ID, or Barangay Certificate of Indigency
- Valid Student ID / Government ID
- For TES-3A: PWD ID issued by NCDA / LGU
- For TES-3B: PRC Official Receipt, Review Center Receipt, and Notarized Letter of Intent

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 75.00, "income_limit": null, "rank_cutoff_alternative": null, "priority_courses": null, "school_type": ["SUC", "LUC", "UniFASTRegistered Private HEI"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "annual_billing", "close": "annual_billing"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": tr[spa n_228](end_span)ue, "first_time_only": false, "return_service_required": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Unregistered Private HEI Risk: Recommending TES to students in unregistered private
- **Verification:** Verified | Confidence: 96/100
- **Contradictions:**
  - Entry min_gwa (75.00% (passing grade per HEI retention standards)) differs from renewal Maintain GWA (Maintain a passing GWA per semester according to HEI retention rules)

---

### Scholarship Grant Program for Children and Dependents of Sugarcane Industry Workers and Small Sugarcane Farmers (SIDA-SGP) (ID: 118)

#### Identity / Affiliations
- **Provider:** Commission on Higher Education (CHED) in partnership with the Sugar Regulatory Administration (SRA) under Republic Act No. 10659 (Sugarcane Industry Development Act of 2015)
- **Category:** Government / National / Need-based / Sectoral Agriculture Grant
- **Website:** https://legacy.ched.gov.ph/sida-sgp/
- **Portal:** SRA Mill District Offices / CHED Regional Office Portals
- **Guidelines:** CHED Memorandum Order (CMO) No. 30, s. 2016; CMO No. 02, s. 2020 (Amendments); CMO No. 15, s. 2026
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen
- **Residency / Destination:** Resident of sugarcane-producing mill districts in the Philippines
- **Education Level:** Undergraduate (College) and Graduate (Master's / Doctoral)
- **Eligible Year Levels:** Undergraduate: Years 1–4; Graduate: Years 1–3
- **Incoming Freshman Only:** No
- **Existing College Students:** Yes (with earned units relevant to priority degree programs)
- **Graduate Students:** Yes (Master's and Doctoral degree levels)
- **Current Enrollment:** Enrolled or accepted in an identified State University and College (SUC)
- **Academic Requirements:** SHS report card / Form 138 (for freshmen), certified true copy of grades for latest semester (for college), or TOR & Diploma (for graduate applicants)
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Selection ranked 70% Academic + 30% Income; passing GWA required for retention)
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined annual gross income of parents/guardian must not exceed ₱400,000.00 for Undergraduate track; combined annual gross income of applicant/spouse/parents must not exceed ₱500,000.00 for Graduate track
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE
- **School / Consortium Restrictions:** Restricted strictly to identified State Universities and Colleges (SUCs)
- **Course Restrictions:** Agriculture, Agricultural Engineering and Mechanics, Chemical Engineering, Sugar Technology, and related ladderized programs specified under Sec. 6(b) of RA 10659
- **Sectoral / Hidden Requirements:** Must be certified by the Sugar Regulatory Administration (SRA) as legitimate children or dependents of sugarcane industry workers or small sugarcane farmers
- **Good Moral:** Required (Certificate of Good Moral Character)
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Applicants must submit complete documents to their local SRA Mill District office to secure SRA certification prior to CHEDRO ranking

#### Timing
- **Who May Apply:** Graduating SHS students, ongoing college students with earned units, and graduate applicants admitted to SUCs
- **Freshmen:** : Yes
- **Sophomores:** : Yes
- **Juniors:** : Yes
- **Seniors:** : Yes
- **Graduates:** : Yes (for Master's/Doctoral programs)
- **Reapply:** : Yes
- **Opening:** Set annually per CHEDRO and SRA advisory
- **Closing:** Announced per academic cycle
- **Cycle:** Annual
- **AY Covered:** AY 2025–2026 / AY 2026–2027

#### Benefits (catalog)
- **Tuition:** SUC tuition is free under RA 10931 for undergraduates; Graduate track provides up to ₱60,000.00 per AY (₱30,000.00 per semester) for TOSF
- **Monthly Stipend:** ₱10,000.00 per month (₱100,000.00 per 10-month AY) for both Undergraduate and Graduate tracks
- **Allowance:** Integrated into monthly stipend
- **Return Service:** Mandatory 1 year of return service in the Philippines for every 1 year of scholarship availed, completed within 2 years after graduation (prioritizing government agencies directly working with the sugarcane industry, other government offices, or related private entities)

#### Renewal
- **Maintain GWA:** Maintain passing GWA per semester as prescribed by SUC retention policies
- **Regular Load:** Full-time credit load in approved priority degree program
- **No Failures:** Maintain regular academic standing without failing grades

#### Disqualifying / Conflicts
- Absence of official Sugar Regulatory Administration (SRA) certification
- Combined gross family income exceeding ₱400,000.00 (undergraduate) or ₱500,000.00 (graduate)
- Enrollment in non-priority programs or private (non-SUC) institutions
- Academic failure or dismissal from the SUC

#### Required Documents (hidden operational requirements)
- Official SRA Certification confirming applicant as child/dependent of a sugarcane worker or small sugarcane farmer
- Certificate of Good Moral Character
- Notice of Admission / Certificate of Registration from participating SUC
- Academic Record: Form 138 / SF9 (for SHS), Certified True Copy of Grades for latest semester (for college), or TOR & Diploma (for graduate applicants)
- Proof of Income: Latest Income Tax Return (ITR) or BIR Certificate of Tax Exemption (Income \le ₱400,000 for undergrad; \le ₱500,000 for grad)

#### Recommended Schema / Fields
```json
{ "education_level": ["College", "Graduate"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": null, "income_limit": 400000, "sectoral_restriction": "SRA_CERTIFIED_SUGARCANE_WORKER_DEPENDENT", "priority_courses": ["AGRICULTURE", "AGRICULTURAL_ENGINEERING", "CHEMICAL_ENGINEERING", "SUGAR_TECHNOLOGY"], "school_type": ["SUC"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "annual_notice", "close": "annual_notice"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "return_service_required": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Missing Sectoral Restriction Risk: The live database lacks an explicit tag for SRA
- **Verification:** Verified | Confidence: 98/100
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Selection ranked 70% Academic + 30% Income; passing GWA required for retention)) differs from renewal Maintain GWA (Maintain passing GWA per semester as prescribed by SUC retention policies)

---

### CHED Scholarship Program for Future Statisticians (Estatistikolar) (ID: 119)

#### Identity / Affiliations
- **Provider:** Commission on Higher Education (CHED) in cooperation with the Philippine Statistics Authority (PSA)
- **Category:** Government / National / Undergraduate / Merit-and-Need / Priority Field
- **Website:** https://legacy.ched.gov.ph/estatistikolar/
- **Portal:** CHED Regional Office Online estatistikolar portals (e.g., https://bit.ly/2026EstatistikolarApplicationPortal)
- **Guidelines:** CHED Memorandum Order (CMO) No. 14, s. 2025; Memorandum OED No. 1064, s. 2026
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Education Level:** Undergraduate / College
- **Eligible Year Levels:** 1st, 2nd, 3rd, and 4th Year - Incoming Freshman Only?: No
- **Incoming Freshman Only:** No
- **Existing College Students:** Yes
- **Graduate Students:** No
- **Current Enrollment:** Enrolled or accepted in BS Statistics, BS Applied Statistics, or PSA-identified statistics programs in private HEIs with Government Recognition (GR) or SUCs/LUCs with COPC/IR
- **Academic Requirements:** SHS GWA of at least 85.00% or equivalent for incoming freshmen; minimum college GWA of 80.00% or equivalent for 2nd to 4th-year college students
- **Minimum GWA:** 85.00% (Incoming Freshmen / Grade 12); 80.00% (Ongoing 2nd–4th Year College Students)
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** Combined annual gross income of parents or legal guardians must not exceed ₱500,000.00
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE ("covers college Filipino students regardless of age...")
- **School / Consortium Restrictions:** Private HEIs with Government Recognition (GR), State Universities and Colleges (SUCs), or Local Universities and Colleges (LUCs) with IR/COPC
- **Course Restrictions:** Bachelor of Science in Statistics, Bachelor of Science in Applied Statistics, or programs specifically identified by the Philippine Statistics Authority (PSA)
- **Sectoral / Hidden Requirements:** Special equity groups (PWDs under RA 7279, Magna Carta for Poor under RA 11291, NCIP IPs, DHSUD Underprivileged/Homeless, First-Generation students) receive +5 bonus points in ranking
- **Good Moral:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Other Official Rules / Conflicts:** Ranking criteria: 70% Academic Performance + 30% Annual Gross Income (+5 equity bonus points). Must execute a notarized scholarship contract (Annex B-2).

#### Timing
- **Who May Apply:** SHS graduating students, incoming 1st-year college students, and ongoing 2nd, 3rd, and 4th-year college students enrolled in BS Statistics/Applied Statistics
- **Freshmen:** : Yes
- **Sophomores:** : Yes
- **Juniors:** : Yes
- **Seniors:** : Yes
- **Graduates:** : No
- **Reapply:** : Yes
- **Opening:** June 22, 2026 (for AY 2026–2027 intake) / June 15 for prior cycles
- **Closing:** July 31, 2026 (for AY 2026–2027 intake) / August 15 for prior cycles
- **Cycle:** Annual
- **AY Covered:** AY 2026–2027 (77 national slots authorized under CEB Res. 374-2026) ### 6. Benefits

#### Benefits (catalog)
- **Tuition:** SUCs/LUCs: Covered under Free Higher Education (RA 10931); Private HEIs: Up to ₱40,000.00 per AY (₱20,000.00 per semester) TOSF coverage
- **Monthly Stipend:** ₱7,000.00 per month (₱35,000.00 per semester = ₱70,000.00 per 10-month AY)
- **Allowance:** Integrated into monthly stipend
- **Return Service:** Maintain minimum GWA of 80% during study; complete degree within prescribed period; no explicit mandatory post-grad public service years specified in CMO 14 s. 2025 contract, but scholar must adhere to contract terms

#### Renewal
- **Maintain GWA:** Maintain a minimum General Weighted Average (GWA) of at least 80.00% or equivalent each semester - Regular Load: Carry regular academic load per term based on curriculum
- **Regular Load:** Carry regular academic load per term based on curriculum
- **No Failures:** Maintain regular academic standing per CHEDRO monitoring

#### Disqualifying / Conflicts
- Enrollment in non-statistics degree programs
- Combined parent gross annual income exceeding ₱500,000.00
- Freshmen SHS GWA below 85.00% or ongoing college GWA below 80.00%
- Unauthorized shifting, school transfer, or unexcused Leave of Absence

#### Required Documents (hidden operational requirements)
- Fully accomplished online Estatistikolar Application Form (Annex A)
- Proof of Citizenship: Birth Certificate issued by NSO/PSA
- Academic Record: Form 138/SF9 (GWA \ge 85% for freshmen) or Certified True Copy of Grades for latest semester (GWA \ge 80% for 2nd–4th year)
- Proof of Income: Latest Income Tax Return (ITR) of parents/guardian, BIR Certificate of Tax Exemption/Non-Filer, OFW Contract/Proof of Income, or Social Case Study Report (Income \le ₱500,000)
- Special Equity Proof (if applicable): DHSUD/MSWDO Indigent Certificate, NCIP IP Certificate, PWD ID, or Social Case Study for First-Gen/Magna Carta for Poor

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 85.00, "renewal_gwa": 80.00, "income_limit": 500000, "priority_courses": ["BSSTATISTICS", "BSAPPLIEDSTATISTICS"], "degree_program_restricted": ["Bachelor of Science in Statistics", "Bachelor of Science in Applied Statistics"], "school_type": ["SUC", "LUC", "Private HEI with Government Recognition"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "06-22", "close": "07-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "return_service_required": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Missing Degree Constraint Risk: Recommending Estatistikolar to general science or
- **Verification:** Verified | Confidence: 98/100
- **Contradictions:**
  - Entry min_gwa (85.00% (Incoming Freshmen / Grade 12); 80.00% (Ongoing 2nd–4th Year College Students)) differs from renewal Maintain GWA (Maintain a minimum General Weighted Average (GWA) of at least 80.00% or equivalent each semester - Regular Load: Carry regular academic load per term based on curriculum)

---

### Scholarships for Staff and Instructors' Knowledge Advancement Program (SIKAP) (ID: 120)

#### Identity / Affiliations
- **Provider:** Commission on Higher Education (CHED)
- **Category:** Government / National / Graduate / Faculty Development / Institutional Capacity Building
- **Website:** https://sikap.ched.gov.ph
- **Portal:** SIKAP Online Portal (https://sikap.ched.gov.ph)
- **Guidelines:** CHED Memorandum Order (CMO) No. 06, s. 2020; CMO No. 28, s. 2021 (Revised Guidelines for SIKAP Grant)
- **Status:** Active

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Education Level:** Graduate (Master's and Doctorate degree levels)
- **Eligible Year Levels:** Incoming and ongoing Master's and Doctoral graduate students
- **Incoming Freshman Only:** No
- **Existing College Students:** Ineligible (Restricted to post-baccalaureate graduate students)
- **Graduate Students:** Yes (Primary target cohort)
- **Current Enrollment:** Must be admitted or enrolled in a Master's or Doctoral program at a CHED-recognized Delivering Higher Education Institution (DHEI)
- **Academic Requirements:** Bachelor's degree (for Master's track) or Master's degree (for Doctorate track); official endorsement from sending HEI
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Governed by DHEI graduate admission and retention standards)
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE (Income uncapped; targeted at employed HEI personnel)
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE (Subject to sending HEI retirement policies)
- **School / Consortium Restrictions:** Restricted strictly to CHED-recognized Delivering Higher Education Institutions (DHEIs) offering authorized graduate programs
- **Course Restrictions:** Graduate degree programs in priority disciplines identified by CHED (e.g., STEAM, Teacher Education, Social Sciences, Health Sciences)
- **Sectoral / Hidden Requirements:** Must be an active full-time or part-time faculty member or non-teaching personnel of a recognized Philippine HEI (sending HEI)
- **Good Moral:** Required (Endorsement by sending HEI President/Head)
- **Health:** Physically and mentally fit for graduate study
- **Other Official Rules / Conflicts:** Requires a tripartite scholarship contract between CHED, Scholar, Sending HEI, and DHEI. Full-time contractual or Contract of Service faculty are eligible under Package B.

#### Timing
- **Who May Apply:** Active HEI faculty and non-teaching personnel pursuing Master's or Doctoral degrees
- **Freshmen:** : Ineligible (Undergraduate freshmen cannot apply)
- **Sophomores:** : Ineligible
- **Juniors:** : Ineligible
- **Seniors:** : Ineligible
- **Graduates:** : Yes (Bachelor's or Master's degree holders entering/enrolled in
- **Reapply:** : Yes
- **Opening:** Set annually per CHED call for applications
- **Closing:** Announced per submission cycle
- **Cycle:** Annual / Semestral intake
- **AY Covered:** AY 2025–2026 / AY 2026–2027

#### Benefits (catalog)
- **Tuition:** 100% coverage of Actual Tuition and Other School Fees (TOSF) paid directly to the DHEI
- **Monthly Stipend:** Living allowance based on study track (Full-Time vs Part-Time Package A/B): Master's up to ₱25,000.00–₱30,000.00/month; Doctorate up to ₱35,000.00–₱40,000.00/month
- **Allowance:** Learning materials, connectivity, and book allowance provided per term
- **Return Service:** Mandatory return service rendered to the sending HEI (1 to 2 years of service for every 1 year of scholarship availed)

#### Renewal
- **Maintain GWA:** Maintain required passing GWA per DHEI graduate retention rules
- **Regular Load:** Full-time or approved part-time credit load per approved curriculum plan
- **No Failures:** Zero failing or incomplete grades in graduate coursework

#### Disqualifying / Conflicts
- Non-employment as HEI faculty or non-teaching personnel
- Enrollment in non-DHEI or non-approved graduate programs
- Academic failure, unexcused dropping, or expulsion from the DHEI
- Failure to secure official endorsement from the sending HEI

#### Required Documents (hidden operational requirements)
- SIKAP Application Form and Plantilla / Employment Verification from Sending HEI
- Official Nomination and Endorsement Letter from Sending HEI President/Head
- Proof of Admission / Registration in a CHED-recognized DHEI
- Certified True Copy of Transcript of Records (TOR) for previous degrees
- Curriculum Vitae (CV) and Research Concept Paper / Dissertation Work Plan
- Certificate of Good Moral Character / Clearance from sending institution

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1, 2, 3], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": null, "income_limit": null, "sectoral_restriction": "HEI_FACULTY_OR_NON_TEACHING_STAFF", "priority_courses": ["CHED_APPROVED_GRADUATE_PROGRAMS"], "school_type": ["DHEI"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "annual_call", "close": "annual_call"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "return_service_required": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Target User Misclassification Risk: In the production database, ID 120 lists levels:
- **Verification:** Verified | Confidence: 98/100
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Governed by DHEI graduate admission and retention standards)) differs from renewal Maintain GWA (Maintain required passing GWA per DHEI graduate retention rules)

---

## SOURCE: `DATABASE_V3_GROUPC_UNNIVERSITIES.pdf`

**Scholarships in this PDF:** 19

### Ateneo Senior High School Financial Aid Grant1 (ID: 18)

#### Identity / Affiliations
- **Provider:** Ateneo de Manila University (Ateneo Senior High School / Office of Admission and Aid)1
- **Category:** Institutional / Secondary Education / Need-and-Merit1
- **Website:** https://www.ateneo.edu/ashs/admissions/scholarships-financial-aid1
- **Portal:** Integrated into the Ateneo Senior High School Admission and Financial Aid Portal1
- **Guidelines:** Ateneo Senior High School Financial Aid Guidelines and Primer1
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen4.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** High School (Grade 11 entry)1.
- **Eligible Year Levels:** Grade 111.
- **Incoming Freshman Only:** Yes (Senior High School Grade 11 entry)1.
- **Existing College Students:** Ineligible1.
- **Graduate Students:** Ineligible1.
- **Current Enrollment:** Must be a graduating Grade 10 student eligible for admission to Ateneo Senior High School1.
- **Academic Requirements:** High academic performance in Junior High School with strong conduct marks1.
- **Minimum GWA:** 90.00% (or equivalent high scholastic standing in JHS)3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** Family gross annual income must not exceed PHP 400,000.003.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Open to graduates of public, parochial, and private Junior High Schools1.
- **Course Restrictions:** Applicable to all Ateneo Senior High School academic strands (STEM, ABM, HUMSS, GA)1.
- **Sectoral / Hidden Requirements:** Priority given to public and parochial high school completers1.
- **Good Moral:** Required (Certificate of Good Moral Character from JHS Principal)2.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Application for financial aid is evaluated independently of the academic admission decision6.

#### Timing
- **Who May Apply:** Graduating Grade 10 Junior High School students1.
- **Freshmen:** : No (restricted to incoming Grade 11 SHS applicants)1.
- **Sophomores:** : No.
- **Juniors:** : No.
- **Seniors:** : No.
- **Graduates:** : No.
- **Reapply:** : No.
- **Opening:** Announced alongside the ASHS admission cycle (typically September)2.
- **Closing:** Concurrent with the ASHS admission deadline (typically November/December)2.
- **Cycle:** Annual.
- **AY Covered:** AY 2026–20272.

#### Benefits (catalog)
- **Tuition:** 100%, 75%, 50%, or 25% waiver of tuition and matriculation fees4.
- **Monthly Stipend:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Allowance:** Food and student learning allowance provided based on evaluated need4.
- **Return Service:** None required3.

#### Renewal
- **Maintain GWA:** Must maintain required academic and conduct marks specified by ASHS OAA2.
- **Regular Load:** Full-time credit enrollment in assigned SHS strand2.
- **No Failures:** Zero failing marks or major disciplinary infractions7.

#### Disqualifying / Conflicts
- Combined parent annual gross income exceeding PHP 400,000.003.
- Submission of fraudulent income documents or altered report cards2.
- Incurring failing grades or severe behavioral reprimands7.

#### Required Documents (hidden operational requirements)
- Parent's Personal Letter detailing household background and financial hardship2.
- Father's and Mother's Income Tax Return (ITR), Certificate of Employment, or BIR Tax Exemption2.
- Utility bills (electricity, water, telephone) for the last three months2.
- Grade 10 Report Card / Form 1382.
- Certificate of Good Moral Character2.

#### Recommended Schema / Fields
```json
{ "education_level": ["High School"], "eligible_year_levels": [11], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": 90.00, "income_limit": 400000, "school_type": ["Public JHS", "Parochial JHS", "Private JHS"], "partner_school_restricted": false, "citizenship": "Filipino", "application_window": {"open": "09-01", "close": "11-15"}, "deadline_type": "estimated", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: System presenting scholarship to Grade 10 students intending to enroll in
- **Verification:** Verified3. | Confidence: n/a
- **Contradictions:**
  - Entry min_gwa (90.00% (or equivalent high scholastic standing in JHS)3.) differs from renewal Maintain GWA (Must maintain required academic and conduct marks specified by ASHS OAA2.)

---

### Philippine Normal University Institutional Scholarship Program3 (ID: 23)

#### Identity / Affiliations
- **Provider:** Philippine Normal University3
- **Category:** Institutional / Teacher Education / Need-and-Merit3
- **Website:** https://pnu.edu.ph3
- **Portal:** PNU Office of Student Affairs and Student Services (OSASS) Portal3
- **Guidelines:** PNU Student Handbook and OSASS Scholarship Guidelines3
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Filipino citizen5.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** College (Undergraduate Teacher Education)3.
- **Eligible Year Levels:** Years 1, 2, 3, and 43.
- **Incoming Freshman Only:** No3.
- **Existing College Students:** Eligible3.
- **Graduate Students:** Ineligible for undergraduate institutional track3.
- **Current Enrollment:** Enrolled in a Bachelor of Secondary or Elementary Education program at PNU9.
- **Academic Requirements:** Minimum GWA of 90.00% (or 2.00 PNU scale) with no failing grades3.
- **Minimum GWA:** 90.00%3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** Combined family gross annual income must not exceed PHP 400,000.003.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to Philippine Normal University campuses5.
- **Course Restrictions:** Bachelor of Secondary Education, Bachelor of Elementary Education, Early Childhood Education9.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Good Moral:** Required10.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Must maintain full academic load each semester11.

#### Timing
- **Who May Apply:** Enrolled undergraduate students in teacher education programs at PNU5.
- **Freshmen:** : Yes9.
- **Sophomores:** : Yes9.
- **Juniors:** : Yes3.
- **Seniors:** : Yes3.
- **Graduates:** : No.
- **Reapply:** : Yes.
- **Opening:** Set per semester during registration week3.
- **Closing:** Set per semester (typically 2 weeks after class commencement)3.
- **Cycle:** Semestral.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Full waiver of remaining tuition and matriculation fees3.
- **Monthly Stipend:** PHP 3,000.00 per month during active academic terms3.
- **Allowance:** PHP 30,000.00 total annual stipend allowance3.
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Maintain a minimum semestral GWA of 90.00% (2.00 or better)3.
- **Regular Load:** Full-time course load per academic term11.
- **No Failures:** Zero dropped, incomplete, or failing marks11.

#### Disqualifying / Conflicts
- GWA falling below 90.00% or incurring an incomplete/failing grade3.
- Parent annual gross income exceeding PHP 400,000.003.
- Carrying an underload without prior academic deanship approval11.

#### Required Documents (hidden operational requirements)
- Duly accomplished PNU OSASS Scholarship Application Form3.
- Official Transcript of Records or Certified True Copy of Grades for preceding term9.
- Certificate of Enrollment / Registration Form showing full load10.
- Parents' Income Tax Return or BIR Certificate of Tax Exemption9.
- Certificate of Good Moral Character10.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 90.00, "income_limit": 400000, "school_type": ["SUC"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "08-15", "close": "09-15"}, "deadline_type": "estimated", "cycle_type": "semester", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Recommending program to non-PNU education majors.
- **Verification:** Verified3. | Confidence: 92/100.
- **Contradictions:**
  - Entry min_gwa (90.00%3.) differs from renewal Maintain GWA (Maintain a minimum semestral GWA of 90.00% (2.00 or better)3.)

---

### UP Presidential Scholarship Program12 (ID: 24)

#### Identity / Affiliations
- **Provider:** University of the Philippines System3
- **Category:** Institutional / System-wide / Merit-and-Need3
- **Website:** https://up.edu.ph / https://osfa.upd.edu.ph3
- **Portal:** Integrated into the UP Student Learning Assistance System (SLAS Online)12
- **Guidelines:** UP System Policy on System Scholarships; UP Gazette Vol. XXXIV12
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen12.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** College (Undergraduate)3.
- **Eligible Year Levels:** Years 1, 2, 3, 4, and 53.
- **Incoming Freshman Only:** No12.
- **Existing College Students:** Eligible12.
- **Graduate Students:** Ineligible for undergraduate Presidential Scholarship (separate Graduate Presidential Fund exists)13.
- **Current Enrollment:** Must be officially enrolled in a degree program in any UP constituent university12.
- **Academic Requirements:** Outstanding scholastic record with a General Weighted Average (GWA) of at least 1.75 (or 95% equivalent)3.
- **Minimum GWA:** 1.75 on the UP grading scale (95.00% equivalent)3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** Family gross annual income must not exceed PHP 400,000.003.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to UP Constituent Universities (UPD, UPLB, UPM, UPV, UPC, UPMin, UPOU, UP Tacloban)12.
- **Course Restrictions:** Open across all undergraduate degree programs12.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Good Moral:** Required12.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Number of awards is limited by annual vacant slot allocations across constituent units12.

#### Timing
- **Who May Apply:** Enrolled UP undergraduate students12.
- **Freshmen:** : Yes (after earning initial term grades or based on UPCAT
- **Sophomores:** : Yes12.
- **Juniors:** : Yes12.
- **Seniors:** : Yes12.
- **Graduates:** : No.
- **Reapply:** : Yes.
- **Opening:** Announced annually by OSFA at the start of the academic year (typically September)12.
- **Closing:** Set per annual call (typically October)12.
- **Cycle:** Annual.
- **AY Covered:** AY 2025–2026 / AY 2026–202712.

#### Benefits (catalog)
- **Tuition:** 100% tuition and miscellaneous fees coverage (under RA 10931 / UP GIAP framework)12.
- **Monthly Stipend:** PHP 6,000.00 per month3.
- **Allowance:** Book allowance of PHP 5,000.00 per semester12.
- **Return Service:** None required3.

#### Renewal
- **Maintain GWA:** Maintain a cumulative GWA of 1.75 or better each academic term12.
- **Regular Load:** Enrolled in a full academic load (at least 15 units per semester)12.
- **No Failures:** Zero failing grades (5.0), unremoved 4.0, or unremoved Incomplete (INC) marks7.

#### Disqualifying / Conflicts
- GWA dropping below 1.75 or incurring a grade of 5.012.
- Dropping below full-time unit load without prior deanship authorization12.
- Family gross income exceeding PHP 400,000.003.

#### Required Documents (hidden operational requirements)
- UP Form 5 / Official Certificate of Registration12.
- Certified True Copy of Grades / Transcript showing GWA <= 1.7512.
- Parents' Income Tax Return or BIR Certificate of Tax Exemption12.
- True Copy of Birth Certificate12.
- Certificate of Good Moral Character12.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 95.00, "income_limit": 400000, "school_type": ["SUC"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "09-01", "close": "10-15"}, "deadline_type": "estimated", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Grade conversion error between percentage scales (95%) and UP decimal scale
- **Verification:** Verified3. | Confidence: 91/100.
- **Contradictions:**
  - Entry min_gwa (1.75 on the UP grading scale (95.00% equivalent)3.) differs from renewal Maintain GWA (Maintain a cumulative GWA of 1.75 or better each academic term12.)

---

### Ateneo de Manila University College Financial Aid Grant2 (ID: 40)

#### Identity / Affiliations
- **Provider:** Ateneo de Manila University (Office of Admission and Aid)2
- **Category:** Institutional / University / Need-based2
- **Website:** https://www.ateneo.edu/college/scholarships2
- **Portal:** Integrated into the Ateneo College Application Portal2
- **Guidelines:** Ateneo Financial Aid Application Primer and Regulations2
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen5.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** College (Undergraduate)2.
- **Eligible Year Levels:** Years 1, 2, 3, 4, and 52.
- **Incoming Freshman Only:** No2.
- **Existing College Students:** Eligible (via upperclassmen financial aid application)2.
- **Graduate Students:** Ineligible for undergraduate track2.
- **Current Enrollment:** Accepted or currently enrolled in an undergraduate degree program at Ateneo de Manila University2.
- **Academic Requirements:** Passing performance in the Ateneo College Entrance Test (ACET) and good academic standing6.
- **Minimum GWA:** 78.00% (or passing QPI standard for retention)3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** Combined gross annual income of parents must not exceed PHP 500,000.003.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to Ateneo de Manila University (Loyola Heights Campus)2.
- **Course Restrictions:** Open across all undergraduate degree programs6.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Good Moral:** Required2.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Application for financial aid does not influence admission decisions6.

#### Timing
- **Who May Apply:** Incoming college freshmen, transferees, and ongoing Ateneo undergraduate students2.
- **Freshmen:** : Yes2.
- **Sophomores:** : Yes2.
- **Juniors:** : Yes2.
- **Seniors:** : Yes2.
- **Graduates:** : No2.
- **Reapply:** : Yes2.
- **Opening:** Concurrent with college admission opening (typically August/September)2.
- **Closing:** October 15 (for SY 2027–2028: Thursday, 15 October 2026)2.
- **Cycle:** Annual.
- **AY Covered:** AY 2026–2027 / AY 2027–20282.

#### Benefits (catalog)
- **Tuition:** 100%, 75%, 50%, or 25% coverage of tuition and fees4.
- **Monthly Stipend:** PHP 3,000.00 per month (integrated into Student Learning Allowance)3.
- **Allowance:** Food allowance provided based on assessed need4.
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Maintain required term QPI specified by the Office of Admission and Aid2.
- **Regular Load:** Full-time credit enrollment per semester2.
- **No Failures:** Zero failing grades (F) or disciplinary probation7.

#### Disqualifying / Conflicts
- Parent annual gross income exceeding PHP 500,000.003.
- Failure to submit all required supporting financial documents by October 152.
- Incurring academic probation or serious disciplinary sanctions7.

#### Required Documents (hidden operational requirements)
- Parents' Personal Letter detailing family background and financial situation2.
- Certificate of Employment and Compensation or 2025 Annual Income Tax Return (ITR) / BIR Form 23162.
- Pay slips for the last two (2) months2.
- Utility bills (electricity, water, telephone) for the last three months2.
- Residence photos and house tour video2.
- Two (2) Scholarship Recommendation Forms submitted via go.ateneo.edu/scholarship-recommendations2.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": false, "minimum_gwa": 78.00, "income_limit": 500000, "school_type": ["Private"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "08-01", "close": "10-15"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Students waiting for ACET admission results before submitting financial aid
- **Verification:** Verified3. | Confidence: 96/100.
- **Contradictions:**
  - Entry min_gwa (78.00% (or passing QPI standard for retention)3.) differs from renewal Maintain GWA (Maintain required term QPI specified by the Office of Admission and Aid2.)

---

### Ateneo Director's List Scholarship4 (ID: 41)

#### Identity / Affiliations
- **Provider:** Ateneo de Manila University3
- **Category:** Institutional / University / Merit-based2
- **Website:** https://www.ateneo.edu/college/scholarships/programs6
- **Portal:** Automatic consideration via the Ateneo College Entrance Test (ACET)4
- **Guidelines:** Ateneo Office of Admission and Aid Merit Guidelines6
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen5.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** College (Undergraduate entry)3.
- **Eligible Year Levels:** Year 1 (Incoming Freshmen)3.
- **Incoming Freshman Only:** Yes6.
- **Existing College Students:** Ineligible for initial award6.
- **Graduate Students:** Ineligible6.
- **Current Enrollment:** Must be an accepted incoming freshman in any undergraduate degree program at Ateneo de Manila University6.
- **Academic Requirements:** Exceptional performance in the ACET and distinguished high school academic and co-curricular record4.
- **Minimum GWA:** 83.00% (or top ACET ranking equivalent)3.
- **Alt Class Rank:** Awarded to top 150 ACET applicants4.
- **Income Ceilings:** Uncapped (Merit-based award independent of family income)3.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to Ateneo de Manila University6.
- **Course Restrictions:** Any undergraduate degree program of choice6.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Good Moral:** Required2.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Awarded automatically by the University Committee on Admission and Aid; no separate application form required4.

#### Timing
- **Who May Apply:** Incoming college freshmen taking the ACET4.
- **Freshmen:** : No (awarded prior to freshman entry)6.
- **Sophomores:** : No.
- **Juniors:** : No.
- **Seniors:** : No.
- **Graduates:** : No.
- **Reapply:** : No.
- **Opening:** Automatic evaluation upon filing ACET application4.
- **Closing:** Concurrent with ACET registration closing2.
- **Cycle:** Annual.
- **AY Covered:** AY 2026–20276.

#### Benefits (catalog)
- **Tuition:** PHP 100,000.00 annual fixed scholarship grant applicable toward tuition and fees4.
- **Monthly Stipend:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Allowance:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Maintain required annual Quality Point Index (QPI) set by the OAA6.
- **Regular Load:** Full-time academic credit load per semester2.
- **No Failures:** No failing grades or disciplinary sanctions7.

#### Disqualifying / Conflicts
- Declining admission to Ateneo de Manila University6.
- Failure to maintain required retention QPI6.
- Severe disciplinary infraction or honor code violation7.

#### Required Documents (hidden operational requirements)
- Ateneo College Application Form and ACET Examination Permit2.
- High School Transcript of Records / Form 1382.
- High School Principal / Counselor Recommendation Form2.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": 83.00, "income_limit": null, "school_type": ["Private"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "08-01", "close": "11-15"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Users attempting to submit a separate application form for Director's List.
- **Verification:** Verified3. | Confidence: 98/100.
- **Contradictions:**
  - Entry min_gwa (83.00% (or top ACET ranking equivalent)3.) differs from renewal Maintain GWA (Maintain required annual Quality Point Index (QPI) set by the OAA6.)

---

### Ateneo Law School Financial Aid Program3 (ID: 42)

#### Identity / Affiliations
- **Provider:** Ateneo Law School (Ateneo de Manila University)3
- **Category:** Institutional / Graduate / Law / Merit-and-Need3
- **Website:** https://www.ateneo.edu / https://law.ateneo.edu3
- **Portal:** Integrated into the Ateneo Law School Admissions & Financial Aid Portal3
- **Guidelines:** Ateneo Law School Financial Aid Policy and Guidelines3
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen5.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** Graduate (Juris Doctor Program)3.
- **Eligible Year Levels:** Years 1, 2, 3, and 4 (Juris Doctor)3.
- **Incoming Freshman Only:** No3.
- **Existing College Students:** Ineligible (Restricted to law students)3.
- **Graduate Students:** Yes (Juris Doctor is a professional law degree)3.
- **Current Enrollment:** Must be admitted or enrolled in the Juris Doctor program at Ateneo Law School3.
- **Academic Requirements:** Bachelor's degree completion, passing the Ateneo Law Admission Test (ALAT), and maintaining satisfactory academic standing3.
- **Minimum GWA:** 82.00% (or equivalent law school QPI requirement)3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** Combined family gross annual income must not exceed PHP 600,000.003.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to Ateneo Law School (Rockwell Campus)3.
- **Course Restrictions:** Juris Doctor (JD) degree program3.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Good Moral:** Required2.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Must reapply annually for financial grant continuation3.

#### Timing
- **Who May Apply:** Incoming 1st-year Juris Doctor students and ongoing Ateneo Law students3.
- **Freshmen:** : Yes (1st year JD students)3.
- **Sophomores:** : Yes (2nd year JD students)3.
- **Juniors:** : Yes (3rd year JD students)3.
- **Seniors:** : Yes (4th year JD students)3.
- **Graduates:** : Yes (Bachelor's degree graduates entering law school)3.
- **Reapply:** : Yes3.
- **Opening:** Announced alongside law school admission results (typically May)3.
- **Closing:** Set per annual law school calendar (typically June/July)3.
- **Cycle:** Annual.
- **AY Covered:** AY 2025–2026 / AY 2026–20273.

#### Benefits (catalog)
- **Tuition:** Partial to 100% tuition and fee waiver3.
- **Monthly Stipend:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Allowance:** Book allowance provided for full-grant recipients3.
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Must maintain required Quality Point Index (QPI) specified by Ateneo Law School3.
- **Regular Load:** Full-time law enrollment per semester19.
- **No Failures:** Zero failing marks (F) or unremoved incomplete grades in law subjects7.

#### Disqualifying / Conflicts
- Family gross annual income exceeding PHP 600,000.003.
- Academic failure or dropping below required law school QPI7.
- Honor code violation or disciplinary action by Ateneo Law School7.

#### Required Documents (hidden operational requirements)
- Ateneo Law School Financial Aid Application Form2.
- Latest Income Tax Return (ITR) of applicant, parents, or spouse2.
- Official Transcript of Records (TOR) from pre-law Bachelor's degree2.
- Certificate of Employment and pay slips (if employed)2.
- Certificate of Good Moral Character2.

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 82.00, "income_limit": 600000, "degree_program_restricted": ["Juris Doctor"], "school_type": ["Private"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "05-01", "close": "06-30"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Displaying scholarship to undergraduate pre-law students.
- **Verification:** Verified3. | Confidence: 96/100.
- **Contradictions:**
  - Entry min_gwa (82.00% (or equivalent law school QPI requirement)3.) differs from renewal Maintain GWA (Must maintain required Quality Point Index (QPI) specified by Ateneo Law School3.)

---

### DLSU Star Scholars Program20 (ID: 43)

#### Identity / Affiliations
- **Provider:** De La Salle University3
- **Category:** Institutional / University / Premier Merit-based3
- **Website:** https://www.dlsu.edu.ph/scholarships/23
- **Portal:** Automatic screening of top DCAT takers followed by invitation/interview20
- **Guidelines:** DLSU Office of Admissions and Scholarships (OAS) Star Scholars Guidelines20
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen20.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** College (Undergraduate entry)3.
- **Eligible Year Levels:** Year 1 (Incoming Freshmen)3.
- **Incoming Freshman Only:** Yes20.
- **Existing College Students:** Ineligible for initial award20.
- **Graduate Students:** Ineligible for initial entry (includes post-undergrad graduate grant)20.
- **Current Enrollment:** Top-ranked applicant accepted into any undergraduate program at DLSU20.
- **Academic Requirements:** Top performance in the DLSU College Admission Test (DCAT) and successful interview evaluation20.
- **Minimum GWA:** 90.00% (or top DCAT score equivalent)3.
- **Alt Class Rank:** Selected among top DCAT examinees nationwide20.
- **Income Ceilings:** Uncapped (Merit-based award)3.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to De La Salle University (Manila and Laguna campuses)20.
- **Course Restrictions:** Open across all undergraduate programs (including BS Human Biology and ladderized master's)20.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Good Moral:** Required20.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Scholars receive continuous faculty mentorship from University Fellows throughout residency20.

#### Timing
- **Who May Apply:** Top-performing examinees in the DLSU College Admission Test20.
- **Freshmen:** : No (awarded prior to freshman entry)20.
- **Sophomores:** : No.
- **Juniors:** : No.
- **Seniors:** : No.
- **Graduates:** : No.
- **Reapply:** : No.
- **Opening:** Automatic consideration upon taking the DCAT20.
- **Closing:** Interview screening completed prior to confirmation period (May/June)22.
- **Cycle:** Annual.
- **AY Covered:** AY 2026–202722.

#### Benefits (catalog)
- **Tuition:** Full 100% waiver of tuition, miscellaneous, and laboratory fees20.
- **Monthly Stipend:** PHP 8,000.00 per month (living and accommodation stipend)3.
- **Allowance:** Coverage for modest accommodation, meals, and books20.
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Maintain required Term GPA (TGPA) and Cumulative GPA (CGPA) specified by OAS24.
- **Regular Load:** Full-time credit load per trimester20.
- **No Failures:** Zero failing marks or withdrawn subjects24.

#### Disqualifying / Conflicts
- Failure to maintain required CGPA retention standard24.
- Incurring a failing or withdrawn grade24.
- Disciplinary sanction or violation of the DLSU Student Handbook24.

#### Required Documents (hidden operational requirements)
- DLSU College Admission Test (DCAT) Application and Results20.
- Senior High School Report Card / Form 13822.
- Recommendation letter from SHS Principal/Counselor20.
- University Fellows Interview Evaluation20.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": 90.00, "income_limit": null, "school_type": ["Private"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "01-15", "close": "05-17"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Displaying Star Scholars program to students with average DCAT scores.
- **Verification:** Verified3. | Confidence: 90/100.
- **Contradictions:**
  - Entry min_gwa (90.00% (or top DCAT score equivalent)3.) differs from renewal Maintain GWA (Maintain required Term GPA (TGPA) and Cumulative GPA (CGPA) specified by OAS24.)

---

### DLSU Archer Achievers Scholarship Program23 (ID: 44)

#### Identity / Affiliations
- **Provider:** De La Salle University3
- **Category:** Institutional / University / Merit-based3
- **Website:** https://www.dlsu.edu.ph/scholarship/archer-achiever-scholarship/23
- **Portal:** Automatic award based on DCAT results (No separate application form)22
- **Guidelines:** DLSU OAS Archer Achievers Guidelines23
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen23.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** College (Undergraduate entry)3.
- **Eligible Year Levels:** Year 1 (Incoming Freshmen)3.
- **Incoming Freshman Only:** Yes23.
- **Existing College Students:** Ineligible23.
- **Graduate Students:** Ineligible23.
- **Current Enrollment:** Enrolled in a Philippine private, public, or science high school at the time of application to DLSU23.
- **Academic Requirements:** Among top examinees in the DCAT based on the Weighted Admission Index23.
- **Minimum GWA:** 83.00% (or top Weighted Admission Index score)3.
- **Alt Class Rank:** Top percentile rank in DCAT examinee cohort23.
- **Income Ceilings:** Uncapped (Merit-based award)3.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to De La Salle University23.
- **Course Restrictions:** Open across all undergraduate programs (including ladderized BS/MS and BS Human Bio)23.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Good Moral:** Required23.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Grantees no longer undergo an interview process, but may choose to interview for scholarship upgrades (e.g., STAR, Vaugirard, Gokongwei)22.

#### Timing
- **Who May Apply:** Top DCAT examinees graduating from Philippine high schools23.
- **Freshmen:** : No (automatically awarded upon college admission)23.
- **Sophomores:** : No.
- **Juniors:** : No.
- **Seniors:** : No.
- **Graduates:** : No.
- **Reapply:** : No.
- **Opening:** Automatic evaluation upon taking the DCAT22.
- **Closing:** Official notification letter sent via email prior to confirmation23.
- **Cycle:** Annual.
- **AY Covered:** AY 2025–2026 / AY 2026–202722.

#### Benefits (catalog)
- **Tuition:** 100% waiver of tuition, miscellaneous, and other fees from term 1 through graduation23.
- **Monthly Stipend:** None (Stipends are strictly NOT part of Archer Achiever benefits)25.
- **Allowance:** None25.
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Maintain required Term GPA (TGPA) and Cumulative GPA (CGPA) per trimester24.
- **Regular Load:** Full-time credit enrollment23.
- **No Failures:** Zero failing grades or unapproved course withdrawals24.

#### Disqualifying / Conflicts
- Failure to meet required trimester CGPA retention threshold24.
- Incurring failing or withdrawn marks24.
- Misconduct violating DLSU disciplinary standards24.

#### Required Documents (hidden operational requirements)
- DLSU College Admission Test (DCAT) Application23.
- Official Senior High School Transcript / Form 13825.
- Official Archer Achiever Award Letter issued by DLSU OAS23.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": 83.00, "income_limit": null, "school_type": ["Private"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "01-15", "close": "05-17"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Matching engine displaying Archer Achievers as including a monthly living stipend.
- **Verification:** Verified3. | Confidence: 98/100.
- **Contradictions:**
  - Entry min_gwa (83.00% (or top Weighted Admission Index score)3.) differs from renewal Maintain GWA (Maintain required Term GPA (TGPA) and Cumulative GPA (CGPA) per trimester24.)

---

### UST San Martin de Porres Equity Scholarship26 (ID: 45)

#### Identity / Affiliations
- **Provider:** University of Santo Tomas (Office for Student Affairs)26
- **Category:** Institutional / University / Need-based / Equity3
- **Website:** https://manila.ust.edu.ph/osawebapp/osainfo-scholarshipoffered26
- **Portal:** UST OSA Scholarship Application and Assistance (SAAF) Submission Portal26
- **Guidelines:** UST Office for Student Affairs Scholarship Manual26
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen5.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** College (Undergraduate)3.
- **Eligible Year Levels:** Years 1, 2, 3, 4, and 53.
- **Incoming Freshman Only:** No26.
- **Existing College Students:** Eligible26.
- **Graduate Students:** Ineligible for undergraduate equity track26.
- **Current Enrollment:** Must be officially enrolled in an undergraduate degree program at the University of Santo Tomas26.
- **Academic Requirements:** Passing academic record with a General Weighted Average (GWA) of at least 85.00% (2.25 UST scale)3.
- **Minimum GWA:** 85.00%3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** Combined family gross annual income must not exceed PHP 300,000.003.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to the University of Santo Tomas (España, Manila campus)26.
- **Course Restrictions:** Open across all UST faculties, colleges, and institutes26.
- **Sectoral / Hidden Requirements:** Special consideration for OWWA dependents, PD577 beneficiaries, and indigent candidates26.
- **Good Moral:** Required (Good Moral Certificate issued by UST OSA)26.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Must submit complete financial indigency documents via the OSA SAAF portal26.

#### Timing
- **Who May Apply:** Enrolled UST undergraduate students in need of financial assistance26.
- **Freshmen:** : Yes26.
- **Sophomores:** : Yes26.
- **Juniors:** : Yes26.
- **Seniors:** : Yes26.
- **Graduates:** : No.
- **Reapply:** : Yes.
- **Opening:** Announced by UST OSA per semester/academic year26.
- **Closing:** Set per term calendar26.
- **Cycle:** Annual / Semestral renewal.
- **AY Covered:** AY 2025–2026 / AY 2026–202726.

#### Benefits (catalog)
- **Tuition:** Partial to 100% waiver of tuition fees (average annual grant value PHP 45,000.00)3.
- **Monthly Stipend:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Allowance:** Integrated into tuition discount structure3.
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Maintain a minimum semestral GWA of 85.00% (2.25)3.
- **Regular Load:** Enrolled in full term load per UST curriculum26.
- **No Failures:** Zero failing grades or unremoved 3.0/INC marks7.

#### Disqualifying / Conflicts
- Family gross annual income exceeding PHP 300,000.003.
- Incurring failing grades or academic probation7.
- Behavioral reprimand or disciplinary sanction by UST Student Conduct Board26.

#### Required Documents (hidden operational requirements)
- UST OSA SAAF Application Form26.
- Official Transcript of Records / Grade Report showing GWA >= 85.00%3.
- Parents' Income Tax Return (ITR), BIR Tax Exemption, or Barangay Certificate of Indigency26.
- Certificate of Good Moral Character26.
- Electric and water utility bills for the last 3 months2.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 85.00, "income_limit": 300000, "school_type": ["Private"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "08-15", "close": "09-30"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Recommending program to students attending non-UST campuses or non-UST
- **Verification:** Verified3. | Confidence: 98/100.
- **Contradictions:**
  - Entry min_gwa (85.00%3.) differs from renewal Maintain GWA (Maintain a minimum semestral GWA of 85.00% (2.25)3.)

---

### Mindanao State University System Admission and Scholarship Examination (MSU-SASE) Academic Scholarship3 (ID: 46)

#### Identity / Affiliations
- **Provider:** Mindanao State University System3
- **Category:** Institutional / System-wide / Merit-based3
- **Website:** https://sase.msuiit.edu.ph/ / https://www.msumain.edu.ph3
- **Portal:** Integrated into the MSU-SASE Online Application System27
- **Guidelines:** MSU System SASE Scholarship Regulations and Policy Manual27
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen5.
- **Residency / Destination:** Resident of regions covered by the MSU System (BARMM, Regions IX, X, XI, XII, XIII, CARAGA, and Palawan)3.
- **Education Level:** College (Undergraduate entry)3.
- **Eligible Year Levels:** Year 1 (Incoming Freshmen)3.
- **Incoming Freshman Only:** Yes27.
- **Existing College Students:** Ineligible27.
- **Graduate Students:** Ineligible27.
- **Current Enrollment:** Must take the MSU-SASE and qualify for admission into any MSU campus (Main Marawi, IIT, Gensan, Maguindanao, Naawan, Sulu, Tawi-Tawi, Buug)27.
- **Academic Requirements:** Top score ranking in the annual MSU-SASE27.
- **Minimum GWA:** 85.00% (or equivalent top SASE percentile score)3.
- **Alt Class Rank:** Selected based on national SASE score ranking tiers27.
- **Income Ceilings:** Uncapped (Merit-based award)3.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to MSU System campuses27.
- **Course Restrictions:** Open across all undergraduate degree programs offered by the MSU System27.
- **Sectoral / Hidden Requirements:** Special slots for Indigenous Cultural Communities and Bangsamoro constituents27.
- **Good Moral:** Required27.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Must enroll in the MSU campus assigned based on SASE qualification27.

#### Timing
- **Who May Apply:** Graduating Senior High School students registering for the MSU-SASE27.
- **Freshmen:** : No (awarded strictly upon SASE entry)27.
- **Sophomores:** : No.
- **Juniors:** : No.
- **Seniors:** : No.
- **Graduates:** : No.
- **Reapply:** : No.
- **Opening:** SASE registration opens annually in September/October27.
- **Closing:** SASE registration closes in December/January; exam administered in November/February27.
- **Cycle:** Annual.
- **AY Covered:** AY 2026–202727.

#### Benefits (catalog)
- **Tuition:** 100% tuition and registration fee waiver at all MSU campuses3.
- **Monthly Stipend:** Semestral living allowance provided3.
- **Allowance:** Total annual stipend grant value of PHP 20,000.003.
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Maintain required Grade Point Average (GPA) per semester set by MSU System policy27.
- **Regular Load:** Full-time academic credit enrollment27.
- **No Failures:** Zero failing marks (5.0) in any academic subject27.

#### Disqualifying / Conflicts
- Failing to meet SASE cut-off score for academic scholarship tier27.
- Dropping below required semestral GPA retention mark27.
- Transferring to a non-MSU institution27.

#### Required Documents (hidden operational requirements)
- MSU-SASE Application Form and Exam Permit27.
- Certified True Copy of Grade 11 and Grade 12 Report Cards27.
- Certificate of Good Moral Character27.
- PSA Birth Certificate27.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": 85.00, "income_limit": null, "regions": ["BARMM", "Region IX - Zamboanga Peninsula", "Region X - Northern Mindanao", "Region XI - Davao", "Region XII - Soccsksargen", "Region XIII - Caraga"], "school_type": ["SUC"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "09-15", "close": "01-15"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Recommending scholarship to upperclassmen or transfer students.
- **Verification:** Verified3. | Confidence: 95/100.
- **Contradictions:**
  - Entry min_gwa (85.00% (or equivalent top SASE percentile score)3.) differs from renewal Maintain GWA (Maintain required Grade Point Average (GPA) per semester set by MSU System policy27.)

---

### PUP Entrance Scholarship Program29 (ID: 68)

#### Identity / Affiliations
- **Provider:** Polytechnic University of the Philippines (Office of Scholarship and Financial Assistance - OSFA)29
- **Category:** Institutional / State University / Equity-and-Merit3
- **Website:** https://www.pup.edu.ph/studentservices/osfa/29
- **Portal:** PUP OSFA Walk-in / Online Scholarship Portal29
- **Guidelines:** PUP Citizen's Charter; PUP OSFA Entrance Scholarship Guidelines30
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen30.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** College (Undergraduate entry)3.
- **Eligible Year Levels:** Year 1 (Incoming Freshmen)3.
- **Incoming Freshman Only:** Yes30.
- **Existing College Students:** Ineligible (Upperclassmen apply for Resident Scholarship instead)30.
- **Graduate Students:** Ineligible29.
- **Current Enrollment:** Must pass the PUP College Entrance Test (PUPCET) and enroll as a first-year student30.
- **Academic Requirements:** High scholastic or specialized achievement under recognized qualification categories30.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Governed by category qualification)30.
- **Alt Class Rank:** Top 10 bracket of graduating class of at least 500 graduates from a public high school30.
- **Income Ceilings:** Uncapped for academic/artist tracks; indigent income criteria for First Gen/Indigent track30.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to the Polytechnic University of the Philippines (Main Sta. Mesa and branches/campuses)9.
- **Course Restrictions:** Open across all undergraduate degree programs30.
- **Sectoral / Hidden Requirements:** Encompasses 11 official categories: (1) Public HS Top 10 (>=500 grads); (2) Cultural Artist; (3) Student Athlete; (4) Creative Media Artist; (5) Campus Journalist; (6) Differently-abled / PWD; (7) ALS Graduate; (8) Indigenous Peoples (IP); (9) Solo Parent; (10) Sangguniang Kabataan (SK) Official; (11) First Generation / Indigent Student30.
- **Good Moral:** Required (Certificate of Good Moral Character)31.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Scholars receive formal "Entrance Scholar of PUP" certification and endorsement to corporate CSR grantors30.

#### Timing
- **Who May Apply:** Incoming first-year students qualifying under any of the 11 official categories30.
- **Freshmen:** : Yes (during initial entry term)30.
- **Sophomores:** : No.
- **Juniors:** : No.
- **Seniors:** : No.
- **Graduates:** : No.
- **Reapply:** : No.
- **Opening:** Concurrent with freshmen enrollment schedule30.
- **Closing:** Specified per enrollment period by PUP OSFA30.
- **Cycle:** Annual.
- **AY Covered:** AY 2025–2026 / AY 2026–202729.

#### Benefits (catalog)
- **Tuition:** 100% waiver of tuition and other school fees (under RA 10931 Universal Access)30.
- **Monthly Stipend:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Allowance:** Endorsement to private corporate/foundation grantors for external stipends29.
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Must transition to PUP Resident Scholarship (President's Lister GWA >= 1.50 or Dean's Lister GWA >= 1.75)33.
- **Regular Load:** Full-time academic load per term30.
- **No Failures:** No grade lower than 2.50 in any subject33.

#### Disqualifying / Conflicts
- Failure to submit principal's sealed certification of category qualification30.
- Failing grade or mark below 2.50 in any term33.
- Submission of false credentials34.

#### Required Documents (hidden operational requirements)
- Certification from SHS Principal (with dry seal) attesting to category (e.g., Top 10 of >=500 grads, Campus Journalist, Cultural Artist)30.
- Form 138 / Grade 12 Senior High School Report Card31.
- Certificate of Good Moral Character31.
- PSA Birth Certificate31.
- Category Proof (e.g., NCIP Certificate for IP, PWD ID, SK Oath of Office, ALS Rating)12.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": null, "rank_cutoff_alternative": 10, "income_limit": null, "school_type": ["SUC"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "06-01", "close": "08-31"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": false, "first_time_only": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Recommending program to public high school top 10 graduates whose graduating
- **Verification:** Verified3. | Confidence: n/a
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Governed by category qualification)30.) differs from renewal Maintain GWA (Must transition to PUP Resident Scholarship (President's Lister GWA >= 1.50 or Dean's Lister GWA >= 1.75)33.)

---

### PUP Student Assistantship Program29 (ID: 69)

#### Identity / Affiliations
- **Provider:** Polytechnic University of the Philippines (Office of Scholarship and Financial Assistance - OSFA)29
- **Category:** Institutional / State University / Student Employment / Need-based3
- **Website:** https://www.pup.edu.ph/studentservices/osfa/services33
- **Portal:** PUP OSFA Office (Rm W119) / Submission of Endorsement Form (PUP-SAEF-5-OFSS-015)29
- **Guidelines:** PUP Citizen's Charter; PUP Student Assistantship Regulations30
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen30.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** College (Undergraduate)3.
- **Eligible Year Levels:** Years 2, 3, 4, and 530.
- **Incoming Freshman Only:** No30.
- **Existing College Students:** Yes (Requires at least 2nd-year standing)30.
- **Graduate Students:** Ineligible29.
- **Current Enrollment:** Must be currently enrolled as a regular student with at least two semesters (1 year) of residency at PUP30.
- **Academic Requirements:** Passed all enrolled subjects in the preceding semester30.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Requires 100% passing rate in prior term)30.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** NOT SPECIFIED IN OFFICIAL SOURCE (Targeted at financially needy regular students)29.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to PUP Main Campus and constituent branches29.
- **Course Restrictions:** Open across all undergraduate academic programs30.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Good Moral:** Required31.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Must be officially endorsed by the head of the PUP office/department to be served30.

#### Timing
- **Who May Apply:** Regular 2nd, 3rd, 4th, and 5th year PUP undergraduate students30.
- **Freshmen:** : No (Requires at least 2nd-year standing and 1 year
- **Sophomores:** : Yes30.
- **Juniors:** : Yes30.
- **Seniors:** : Yes30.
- **Graduates:** : No.
- **Reapply:** : Yes (Subject to semestral renewal)30.
- **Opening:** One week after the Adjustment Period of each semester30.
- **Closing:** Set per semestral notice by PUP OSFA30.
- **Cycle:** Semestral renewal.
- **AY Covered:** AY 2025–2026 / AY 2026–202729.

#### Benefits (catalog)
- **Tuition:** None (Tuition is already covered under RA 10931)35.
- **Monthly Stipend:** Hourly compensation of PHP 25.00 / hour31.
- **Allowance:** Maximum monthly compensation of PHP 2,500.00 (based on max 100 hours/month)31.
- **Return Service:** Work commitment of up to 24 hours per week or 100 hours per month31.

#### Renewal
- **Maintain GWA:** Must pass 100% of enrolled units in the preceding semester30.
- **Regular Load:** Maintain regular student status per semester30.
- **No Failures:** Zero failing grades in any subject30.

#### Disqualifying / Conflicts
- Incurring a failing, dropped, or incomplete mark in the preceding term30.
- Irregular student status or year level lower than 2nd Year30.
- Exceeding the maximum limit of 24 work hours per week or 100 hours per month31.

#### Required Documents (hidden operational requirements)
- Student Assistantship Endorsement Form (PUP-SAEF-5-OFSS-015) signed by Office Head29.
- Official Certificate of Registration (Registration Certificate) for current term30.
- Copy of Grades / Transcript for the preceding semester30.
- Student Personal Data Sheet29.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": null, "income_limit": null, "school_type": ["SUC"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "09-15", "close": "10-15"}, "deadline_type": "exact", "cycle_type": "semester", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Displaying assistantship vacancies to 1st-year freshmen.
- **Verification:** Verified3. | Confidence: 96/100.
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Requires 100% passing rate in prior term)30.) differs from renewal Maintain GWA (Must pass 100% of enrolled units in the preceding semester30.)

---

### UP College of Law Scholarship Program17 (ID: 70)

#### Identity / Affiliations
- **Provider:** UP College of Law (University of the Philippines Diliman)17
- **Category:** Institutional / Graduate / Professional Law / Need-and-Equity3
- **Website:** https://law.upd.edu.ph/call-for-scholarship-applications-ay-2025-2026/17
- **Portal:** Integrated UP Law Online Scholarship Application System17
- **Guidelines:** UP College of Law Scholarship Announcement and Guidelines17
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen12.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** Graduate (Juris Doctor Program)3.
- **Eligible Year Levels:** Years 1, 2, 3, and 4 (Juris Doctor)3.
- **Incoming Freshman Only:** No17.
- **Existing College Students:** Ineligible (Restricted to law students)17.
- **Graduate Students:** Yes (Juris Doctor professional program)17.
- **Current Enrollment:** Must be a bona fide Juris Doctor student at UP College of Law17.
- **Academic Requirements:** Need is the primary selection criterion; academic merit is secondary17.
- **Minimum GWA:** NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated holistically based on hardship)17.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** Evaluated based on Income Tax Return and household asset verification form17.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to UP College of Law (Diliman and BGC campuses)17.
- **Course Restrictions:** Juris Doctor (JD) degree program17.
- **Sectoral / Hidden Requirements:** Diversity considerations explicitly prioritized: LGBTQIA+ individuals, members of Indigenous Peoples (IP) communities, Persons with Disabilities (PWDs), single parents, and aspiring first-generation lawyers17.
- **Good Moral:** Required17.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Applicants must forego other active scholarship awards upon acceptance to UP Law Scholarship17. Background checks and home asset inspections are conducted17.

#### Timing
- **Who May Apply:** All bona fide Juris Doctor students at UP College of Law17.
- **Freshmen:** : Yes (1st year JD students)17.
- **Sophomores:** : Yes (2nd year JD students)17.
- **Juniors:** : Yes (3rd year JD students)17.
- **Seniors:** : Yes (4th year JD students)17.
- **Graduates:** : Yes (LAE applicants receiving application fee waivers)17.
- **Reapply:** : Yes17.
- **Opening:** June 30 annually17.
- **Closing:** July 20 annually (Deadlines strictly applied)17.
- **Cycle:** Annual.
- **AY Covered:** AY 2025–2026 / AY 2026–202717.

#### Benefits (catalog)
- **Tuition:** 100% waiver of tuition and miscellaneous fees17.
- **Monthly Stipend:** PHP 10,000.00 per month for 3 to 4 months per semester (Tier 1 & Tier 2 scholars)17.
- **Allowance:** Internet and book allowance set at PHP 10,000.00 per semester17.
- **Return Service:** Scholars render student service assistance to the UP College of Law17.

#### Renewal
- **Maintain GWA:** Maintain good academic standing per UP Law academic retention rules17.
- **Regular Load:** Full-time credit enrollment in Juris Doctor curriculum17.
- **No Failures:** Compliance with law deanship retention rules17.

#### Disqualifying / Conflicts
- Holding another active scholarship award without submitting an official withdrawal letter17.
- Misrepresentation during household asset inspection or background check17.
- Failure to submit all required ITRs/photos before the strict July 20 deadline17.

#### Required Documents (hidden operational requirements)
- Accomplished UP Law Online Scholarship Application Form17.
- Letter of Intent detailing financial hardship, family dynamics, and personal circumstances17.
- Latest Income Tax Return (ITR) of applicant, spouse, parents, or supporting siblings17.
- Household Asset Photos (front of home, living room, kitchen, bedroom, and major appliances)17.
- Landbank Account Details for stipend disbursement17.

#### Recommended Schema / Fields
```json
{ "education_level": ["Graduate"], "eligible_year_levels": [1, 2, 3, 4], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": null, "income_limit": null, "degree_program_restricted": ["Juris Doctor"], "school_type": ["SUC"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "06-30", "close": "07-20"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "return_service_required": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: System assuming Socialized Tuition System (STS) discount precludes UP Law
- **Verification:** Verified3. | Confidence: 95/100.
- **Contradictions:**
  - Entry min_gwa (NOT SPECIFIED IN OFFICIAL SOURCE (Evaluated holistically based on hardship)17.) differs from renewal Maintain GWA (Maintain good academic standing per UP Law academic retention rules17.)

---

### Ateneo Freshman Merit Scholarship (AFMS)4 (ID: 104)

#### Identity / Affiliations
- **Provider:** Ateneo de Manila University3
- **Category:** Institutional / University / Premier Merit-based2
- **Website:** https://www.ateneo.edu/college/scholarships/programs6
- **Portal:** Automatic consideration via the Ateneo College Entrance Test (ACET)4
- **Guidelines:** Ateneo Office of Admission and Aid Merit Guidelines6
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen5.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** College (Undergraduate entry)3.
- **Eligible Year Levels:** Year 1 (Incoming Freshmen)3.
- **Incoming Freshman Only:** Yes4.
- **Existing College Students:** Ineligible6.
- **Graduate Students:** Ineligible6.
- **Current Enrollment:** Must be a top-ranked applicant accepted into any undergraduate degree program at Ateneo de Manila University6.
- **Academic Requirements:** Exceptional ACET score ranking, outstanding high school academic performance, and demonstrated leadership roles4.
- **Minimum GWA:** 90.00% (or top 50 ACET examinee rank)3.
- **Alt Class Rank:** Ranked within the top 50 applicants nationwide4.
- **Income Ceilings:** Uncapped (Merit-based award independent of family income)3.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to Ateneo de Manila University (Loyola Heights)6.
- **Course Restrictions:** Scholars may choose any undergraduate degree program of their choice6.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Good Moral:** Required2.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Awarded automatically; no separate application form required4.

#### Timing
- **Who May Apply:** High school seniors registering for the ACET4.
- **Freshmen:** : No (awarded strictly upon freshman admission)6.
- **Sophomores:** : No.
- **Juniors:** : No.
- **Seniors:** : No.
- **Graduates:** : No.
- **Reapply:** : No.
- **Opening:** Automatic evaluation upon filing ACET application4.
- **Closing:** Concurrent with ACET application deadline2.
- **Cycle:** Annual.
- **AY Covered:** AY 2026–20276.

#### Benefits (catalog)
- **Tuition:** Full 100% waiver of tuition and matriculation fees for the entire duration of the chosen undergraduate degree4.
- **Monthly Stipend:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Allowance:** Annual book and learning allowance provided4.
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Maintain required annual Quality Point Index (QPI) set by OAA for merit scholars6.
- **Regular Load:** Full-time credit enrollment per semester2.
- **No Failures:** Zero failing marks or unremoved incomplete grades7.

#### Disqualifying / Conflicts
- Declining enrollment at Ateneo de Manila University6.
- Falling below the required merit QPI retention mark6.
- Major disciplinary sanction or violation of university rules7.

#### Required Documents (hidden operational requirements)
- Ateneo College Application Form and ACET Permit2.
- Senior High School Transcript of Records / Form 1382.
- Principal / Guidance Counselor Endorsement Form attesting to leadership roles2.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": 90.00, "income_limit": null, "school_type": ["Private"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "08-01", "close": "11-15"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Users misinterpreting AFMS as requiring a separate application form from ACET.
- **Verification:** Verified3. | Confidence: 98/100.
- **Contradictions:**
  - Entry min_gwa (90.00% (or top 50 ACET examinee rank)3.) differs from renewal Maintain GWA (Maintain required annual Quality Point Index (QPI) set by OAA for merit scholars6.)

---

### Ateneo Magis Scholarship4 (ID: 105)

#### Identity / Affiliations
- **Provider:** Ateneo de Manila University3
- **Category:** Institutional / University / Full-Ride Need-and-Merit3
- **Website:** https://www.ateneo.edu/college/scholarships/programs6
- **Portal:** Selected from among qualified Ateneo Financial Aid applicants4
- **Guidelines:** Ateneo Office of Admission and Aid Magis Guidelines6
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen5.
- **Residency / Destination:** Applicants are selected across 4 geographic regions: NCR, Luzon, Visayas, and Mindanao4.
- **Education Level:** College (Undergraduate entry)3.
- **Eligible Year Levels:** Year 1 (Incoming Freshmen)3.
- **Incoming Freshman Only:** Yes4.
- **Existing College Students:** Ineligible for initial award6.
- **Graduate Students:** Ineligible6.
- **Current Enrollment:** Must apply for Financial Aid and be admitted to an undergraduate degree program at Ateneo de Manila University6.
- **Academic Requirements:** Outstanding scholastic achievement in Senior High School and high ACET performance4.
- **Minimum GWA:** 85.00% (or top financial aid applicant standing)3.
- **Alt Class Rank:** Selected as the top financial aid recipient in the respective geographic island group4.
- **Income Ceilings:** Family gross annual income must demonstrate severe financial constraint (capped at PHP 250,000.00)3.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to Ateneo de Manila University6.
- **Course Restrictions:** Open across all 4- and 5-year undergraduate degree programs4.
- **Sectoral / Hidden Requirements:** Underprivileged candidates with potential for servant leadership4.
- **Good Moral:** Required2.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Only applicants who qualify for an Ateneo Financial Aid Grant are considered for the Magis Scholarship4.

#### Timing
- **Who May Apply:** Incoming college freshmen applying for Ateneo Financial Aid4.
- **Freshmen:** : No (awarded upon freshman entrance)6.
- **Sophomores:** : No.
- **Juniors:** : No.
- **Seniors:** : No.
- **Graduates:** : No.
- **Reapply:** : No.
- **Opening:** Concurrent with Ateneo Financial Aid Application opening (August)2.
- **Closing:** October 15 (Financial Aid submission deadline)2.
- **Cycle:** Annual.
- **AY Covered:** AY 2025–2026 / AY 2026–20274.

#### Benefits (catalog)
- **Tuition:** 100% waiver of tuition and matriculation fees for any 4- or 5-year course4.
- **Monthly Stipend:** PHP 4,000.00 per month (food and living allowance)3.
- **Allowance:** Student learning, books, printing, and school supplies allowance4.
- **Return Service:** None required3.

#### Renewal
- **Maintain GWA:** Maintain required QPI standard set by OAA6.
- **Regular Load:** Full-time credit enrollment2.
- **No Failures:** Zero failing grades7.

#### Disqualifying / Conflicts
- Failure to qualify for an Ateneo Financial Aid Grant4.
- Parent annual gross income exceeding PHP 250,000.003.
- Severe disciplinary infraction or academic failure7.

#### Required Documents (hidden operational requirements)
- Complete Ateneo Financial Aid Application Package (Parents' letter, ITR, pay slips, utility bills)2.
- Residence Photos and House Tour Video2.
- High School Transcript of Records / Form 1382.
- Two (2) Recommendation Forms2.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": 85.00, "income_limit": 250000, "school_type": ["Private"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "08-01", "close": "10-15"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Displaying Magis Scholarship to candidates who did not complete the prerequisite
- **Verification:** Verified3. | Confidence: 98/100.
- **Contradictions:**
  - Entry min_gwa (85.00% (or top financial aid applicant standing)3.) differs from renewal Maintain GWA (Maintain required QPI standard set by OAA6.)

---

### St. La Salle Financial Assistance Grant21 (ID: 106)

#### Identity / Affiliations
- **Provider:** De La Salle University (Office of Admissions and Scholarships)21
- **Category:** Institutional / University / Need-based3
- **Website:** https://www.dlsu.edu.ph/admissions/scholarships/22
- **Portal:** Integrated DLSU OAS Financial Assistance Online Portal22
- **Guidelines:** DLSU St. La Salle Financial Assistance FAQs & Guidelines AY 2026–202722
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen21.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** College (Undergraduate)3.
- **Eligible Year Levels:** Years 1, 2, 3, 4, and 53.
- **Incoming Freshman Only:** No22.
- **Existing College Students:** Eligible (Separate application calls for current students)22.
- **Graduate Students:** Ineligible for undergraduate track (Separate St. Mutien Marie Grant exists)20.
- **Current Enrollment:** Must pass the DLSU College Admissions Test (DCAT) or be an ongoing regular DLSU undergraduate22.
- **Academic Requirements:** Evaluated based on high school academic competence and DCAT score22.
- **Minimum GWA:** 85.00%3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** Structured into 3 tiered income brackets: Bracket A (< PHP 450,000: 100% tuition + stipend); Bracket B (PHP 450,000–1,000,000: 100% tuition); Bracket C (PHP 1,000,001–1,800,000: Partial tuition waiver)22.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to De La Salle University (Manila and Laguna campuses)22.
- **Course Restrictions:** Open across all undergraduate degree programs22.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Good Moral:** Required22.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Grantees awarded 100% waivers are exempted from paying the PHP 10,000 reservation fee22.

#### Timing
- **Who May Apply:** DCAT examinees, Special DCAT examinees, and ongoing DLSU undergraduate students22.
- **Freshmen:** : Yes22.
- **Sophomores:** : Yes22.
- **Juniors:** : Yes22.
- **Seniors:** : Yes22.
- **Graduates:** : No22.
- **Reapply:** : Yes22.
- **Opening:** April 17 for DCAT applicants; May 26 for Special DCAT applicants22.
- **Closing:** May 17 for DCAT applicants; June 1 for Special DCAT applicants (No extensions)22.
- **Cycle:** Annual / Semestral.
- **AY Covered:** AY 2026–202722.

#### Benefits (catalog)
- **Tuition:** Full 100% or partial tuition and fees waiver depending on income bracket22.
- **Monthly Stipend:** PHP 3,500.00 per month (awarded to Bracket A scholars with family income < PHP 450k)3.
- **Allowance:** Integrated into monthly stipend package22.
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Maintain required Term GPA and Cumulative GPA per trimester22.
- **Regular Load:** Enrolled in full-time credit load22.
- **No Failures:** Zero failing marks or unapproved course withdrawals24.

#### Disqualifying / Conflicts
- Combined family gross annual income exceeding PHP 1,800,000.0022.
- Dropping below required trimester GPA retention mark24.
- Major disciplinary infraction or submission of falsified ITRs22.

#### Required Documents (hidden operational requirements)
- Accomplished St. La Salle Financial Assistance Online Application Form22.
- Parents' Income Tax Return (ITR), BIR Certificate of Tax Exemption, or Employment Contract22.
- Electric and water utility bills for the last 3 months22.
- High School Transcript of Records / Report Cards22.
- Letter of Explanation addressed to OAS Director for any missing document22.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": false, "minimum_gwa": 85.00, "income_limit": 1800000, "school_type": ["Private"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "04-17", "close": "05-17"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": false, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Engine disqualifying applicants earning between PHP 700,000 and PHP 1,800,000
- **Verification:** Verified3. | Confidence: 96/100.
- **Contradictions:**
  - Entry min_gwa (85.00%3.) differs from renewal Maintain GWA (Maintain required Term GPA and Cumulative GPA per trimester22.)

---

### DLSU Vaugirard Scholarship Program20 (ID: 107)

#### Identity / Affiliations
- **Provider:** De La Salle University3
- **Category:** Institutional / University / Merit-and-Need / Public School Track3
- **Website:** https://www.dlsu.edu.ph/admissions/scholarships/20
- **Portal:** Selected from top DCAT examinees graduating from public/science high schools (Screening/interview)20
- **Guidelines:** DLSU OAS Vaugirard Scholarship Guidelines20
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen20.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** College (Undergraduate entry)3.
- **Eligible Year Levels:** Year 1 (Incoming Freshmen)3.
- **Incoming Freshman Only:** Yes20.
- **Existing College Students:** Ineligible20.
- **Graduate Students:** Ineligible20.
- **Current Enrollment:** Must be a graduating student from a Philippine Public or Science High School accepted to DLSU20.
- **Academic Requirements:** Among top examinees in the DLSU College Admission Test (DCAT)20.
- **Minimum GWA:** 88.00% (or top DCAT score equivalent)3.
- **Alt Class Rank:** Selected by University Committee screening from top public/science DCAT examinees20.
- **Income Ceilings:** Combined family gross annual income must not exceed PHP 300,000.003.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to graduates of Philippine Public High Schools and Science High Schools enrolling at DLSU20.
- **Course Restrictions:** Open across all undergraduate degree programs20.
- **Sectoral / Hidden Requirements:** Public and Science High School completers20.
- **Good Moral:** Required20.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Candidates are invited for committee screening; cash incentives are awarded to scholars graduating with Latin honors20.

#### Timing
- **Who May Apply:** Graduating public and science high school seniors taking the DCAT20.
- **Freshmen:** : No (awarded upon freshman entry)20.
- **Sophomores:** : No.
- **Juniors:** : No.
- **Seniors:** : No.
- **Graduates:** : No.
- **Reapply:** : No.
- **Opening:** Automatic screening upon DCAT administration20.
- **Closing:** Committee interviews conducted in April/May prior to confirmation20.
- **Cycle:** Annual.
- **AY Covered:** AY 2026–202722.

#### Benefits (catalog)
- **Tuition:** 100% waiver of tuition, miscellaneous, and laboratory fees throughout stay at DLSU20.
- **Monthly Stipend:** PHP 4,000.00 per month (monthly living stipend)3.
- **Allowance:** Modest accommodation and allowance coverage20.
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Maintain required trimester GPA retention mark set by OAS24.
- **Regular Load:** Full-time credit enrollment per trimester20.
- **No Failures:** Zero failing grades24.

#### Disqualifying / Conflicts
- High school origin from a private non-science institution20.
- Parent gross annual income exceeding PHP 300,000.003.
- Failure to maintain trimester GPA retention standard24.

#### Required Documents (hidden operational requirements)
- DCAT Application Form and Results20.
- Public / Science High School Form 138 / Transcript20.
- Parents' Income Tax Return or BIR Tax Exemption Certificate12.
- Certificate of Good Moral Character20.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1], "incoming_year_only": true, "requires_current_enrollment": false, "minimum_gwa": 88.00, "income_limit": 300000, "school_type": ["Public High School", "Science High School"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "01-15", "close": "05-17"}, "deadline_type": "exact", "cycle_type": "annual", "renewable": true, "first_time_only": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Matching engine displaying Vaugirard to private non-science high school graduates.
- **Verification:** Verified3. | Confidence: 98/100.
- **Contradictions:**
  - Entry min_gwa (88.00% (or top DCAT score equivalent)3.) differs from renewal Maintain GWA (Maintain required trimester GPA retention mark set by OAS24.)

---

### UST San Lorenzo Ruiz Student Assistance Scholarship26 (ID: 108)

#### Identity / Affiliations
- **Provider:** University of Santo Tomas (Office for Student Affairs)26
- **Category:** Institutional / University / Student Employment / Need-based3
- **Website:** https://manila.ust.edu.ph/osawebapp/osainfo-scholarshipoffered26
- **Portal:** UST OSA SAAF Portal26
- **Guidelines:** UST Office for Student Affairs San Lorenzo Ruiz Guidelines26
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen5.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** College (Undergraduate)3.
- **Eligible Year Levels:** Years 1, 2, 3, 4, and 53.
- **Incoming Freshman Only:** No26.
- **Existing College Students:** Eligible26.
- **Graduate Students:** Ineligible26.
- **Current Enrollment:** Must be officially enrolled in an undergraduate degree program at the University of Santo Tomas26.
- **Academic Requirements:** Passing academic record with a General Weighted Average (GWA) of at least 82.00% (2.50 UST scale)3.
- **Minimum GWA:** 82.00%3.
- **Alt Class Rank:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Income Ceilings:** Combined family gross annual income must not exceed PHP 250,000.003.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to the University of Santo Tomas (España, Manila)26.
- **Course Restrictions:** Open across all UST faculties, colleges, and institutes26.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Good Moral:** Required (Certificate of Good Moral Character from OSA)26.
- **Health:** Physically and mentally fit to perform student assistant duties26.
- **Other Official Rules / Conflicts:** Willingness to render twenty (20) to thirty (30) hours per week of service in assigned university offices26.

#### Timing
- **Who May Apply:** Enrolled UST undergraduate students seeking work-study aid26.
- **Freshmen:** : Yes26.
- **Sophomores:** : Yes26.
- **Juniors:** : Yes26.
- **Seniors:** : Yes26.
- **Graduates:** : No.
- **Reapply:** : Yes (Semestral renewal)26.
- **Opening:** Announced by UST OSA at the start of each semester26.
- **Closing:** Set per semestral notice26.
- **Cycle:** Semestral.
- **AY Covered:** AY 2025–2026 / AY 2026–202726.

#### Benefits (catalog)
- **Tuition:** Full or partial tuition and fees discount3.
- **Monthly Stipend:** Hourly compensation or semestral stipend allowance (total value up to PHP 60,000.00/year)3.
- **Allowance:** Integrated into work-study stipend package3.
- **Return Service:** Render 20 to 30 hours per week of service in assigned UST unit26.

#### Renewal
- **Maintain GWA:** Maintain a minimum semestral GWA of 82.00% (2.50)3.
- **Regular Load:** Enrolled in full term credit load26.
- **No Failures:** Zero failing marks7.

#### Disqualifying / Conflicts
- Family gross annual income exceeding PHP 250,000.003.
- Failure to render the required 20–30 hours of weekly service26.
- Academic failure or disciplinary violation7.

#### Required Documents (hidden operational requirements)
- UST OSA SAAF Application Form for San Lorenzo Ruiz Scholarship26.
- Official Grade Report / Transcript showing GWA >= 82.00%3.
- Parents' Income Tax Return (ITR) or Barangay Certificate of Indigency26.
- UST Health Service Medical Clearance26.
- Endorsement Form from assigned UST office supervisor26.

#### Recommended Schema / Fields
```json
{ "education_level": ["College"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 82.00, "income_limit": 250000, "school_type": ["Private"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "08-15", "close": "09-30"}, "deadline_type": "exact", "cycle_type": "semester", "renewable": true, "first_time_only": false, "return_service_required": true, "needs_manual_review": true }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Enrolling students who cannot commit 20–30 hours per week due to heavy
- **Verification:** Verified3. | Confidence: 96/100.
- **Contradictions:**
  - Entry min_gwa (82.00%3.) differs from renewal Maintain GWA (Maintain a minimum semestral GWA of 82.00% (2.50)3.)

---

### UST Santo Tomas Academic Scholarship26 (ID: 109)

#### Identity / Affiliations
- **Provider:** University of Santo Tomas (Office for Student Affairs)26
- **Category:** Institutional / University / Merit-based3
- **Website:** https://manila.ust.edu.ph/osawebapp/osainfo-scholarshipoffered26
- **Portal:** Integrated UST OSA Scholarship Portal / Faculty Dean's Office Endorsement26
- **Guidelines:** UST Office for Student Affairs Academic Scholarship Manual26
- **Status:** Active3

#### Hard Eligibility Rules
- **Citizenship:** Natural-born or naturalized Filipino citizen5.
- **Residency / Destination:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Education Level:** High School (SHS), College, and Graduate (LEAPMed, Faculty of Civil Law, Faculty of Medicine and Surgery)26.
- **Eligible Year Levels:** All year levels corresponding to the program26.
- **Incoming Freshman Only:** No (Covers incoming freshmen Valedictorians/Salutatorians and ongoing Dean's Listers)4.
- **Existing College Students:** Eligible (Awarded per semester based on Dean's List ranking)26.
- **Graduate Students:** Eligible (Applicable to Civil Law and Medicine and Surgery)26.
- **Current Enrollment:** Must be officially enrolled in UST in Senior High School, College, LEAPMed, Law, or Medicine26.
- **Academic Requirements:** Valedictorian or Salutatorian status for incoming freshmen; Top 1 or Top 2 rank in the college/faculty for upperclassmen4.
- **Minimum GWA:** 88.00% (or Dean's List Top 1/Top 2 rank cutoff)3.
- **Alt Class Rank:** Rank 1 (100% waiver) or Rank 2 (50% waiver) in the academic department/batch4.
- **Income Ceilings:** Uncapped (Merit-based award independent of income)3.
- **Age Restrictions:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **School / Consortium Restrictions:** Restricted strictly to the University of Santo Tomas26.
- **Course Restrictions:** Open across all UST faculties, colleges, institutes, and professional schools26.
- **Sectoral / Hidden Requirements:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Good Moral:** Required26.
- **Health:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Other Official Rules / Conflicts:** Application requires certification of academic rank from the High School Principal or College Registrar4.

#### Timing
- **Who May Apply:** Incoming freshmen (Valedictorians/Salutatorians) and ongoing UST top-ranked students4.
- **Freshmen:** : Yes26.
- **Sophomores:** : Yes26.
- **Juniors:** : Yes26.
- **Seniors:** : Yes26.
- **Graduates:** : Yes (Civil Law and Medicine students)26.
- **Reapply:** : Yes (Evaluated every semester based on term rank)26.
- **Opening:** Announced by UST OSA at the start of each term26.
- **Closing:** Set per semestral deadline26.
- **Cycle:** Semestral.
- **AY Covered:** AY 2025–2026 / AY 2026–202726.

#### Benefits (catalog)
- **Tuition:** 100% tuition waiver for Rank 1 / Valedictorians; 50% tuition waiver for Rank 2 / Salutatorians4.
- **Monthly Stipend:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Allowance:** NOT SPECIFIED IN OFFICIAL SOURCE.
- **Return Service:** None3.

#### Renewal
- **Maintain GWA:** Must maintain Top 1 or Top 2 academic ranking in the department each semester4.
- **Regular Load:** Enrolled in full term credit load26.
- **No Failures:** Zero failing grades, 3.0 marks, or incomplete grades7.

#### Disqualifying / Conflicts
- Losing Top 1 or Top 2 rank in the academic batch/department4.
- Incurring an incomplete, dropped, or failing grade7.
- Disciplinary sanction issued by UST OSA26.

#### Required Documents (hidden operational requirements)
- UST OSA SAAF Application Form for Santo Tomas Academic Scholarship26.
- High School Principal's Certification of Valedictorian/Salutatorian status (for Freshmen)4.
- Official Transcript / Registrar Certification of Top 1 or Top 2 Rank in Department (for Upperclassmen)26.
- Certificate of Good Moral Character26.

#### Recommended Schema / Fields
```json
{ "education_level": ["Senior High School", "College", "Graduate"], "eligible_year_levels": [1, 2, 3, 4, 5], "incoming_year_only": false, "requires_current_enrollment": true, "minimum_gwa": 88.00, "rank_cutoff_alternative": 2, "income_limit": null, "school_type": ["Private"], "partner_school_restricted": true, "citizenship": "Filipino", "application_window": {"open": "08-15", "close": "09-30"}, "deadline_type": "exact", "cycle_type": "semester", "renewable": true, "first_time_only": false, "needs_manual_review": false }
```

#### FP/FN Risks & Contradictions
- **Matching Risks:** ● Risk: Recommending scholarship to general Dean's Listers who are ranked outside the
- **Verification:** Verified3. | Confidence: 95/100.
- **Contradictions:**
  - Entry min_gwa (88.00% (or Dean's List Top 1/Top 2 rank cutoff)3.) differs from renewal Maintain GWA (Must maintain Top 1 or Top 2 academic ranking in the department each semester4.)

---
