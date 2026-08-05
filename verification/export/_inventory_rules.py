import pathlib, re, json, sys
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

corpus = json.loads(pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\export\_scholarship_corpus.json").read_text(encoding="utf-8"))

# Rule class detectors: (class_id, label, regexes) - match against full text
# Careful: only positive eligibility rules, not renewal/documents unless it's an eligibility gate

RULE_DEFS = [
  ("RC01_citizenship_filipino", "Filipino citizenship required", [r"Filipino citizen", r"Filipino citizenship", r"natural-born or naturalized Filipino"]),
  ("RC02_citizenship_natural_born_only", "Natural-born Filipino only (stricter)", [r"natural-born Filipino(?! or naturalized)", r"must be a natural-born Filipino"]),
  ("RC03_residency_lgu_or_locality", "Local residency / LGU locality required", [r"proof of residency", r"resident of", r"residency in", r"bona fide resident", r"QCitizen", r"registered voter of", r"must reside in"]),
  ("RC04_education_level_gate", "Education level / degree stage gate", [r"Education Level\s*:", r"Undergraduate", r"Graduate \(Master", r"Senior High School", r"TVET"]),
  ("RC05_year_level_restriction", "Eligible year-level restriction", [r"Eligible Year Levels?\s*:", r"Year 1", r"2nd[- ]year", r"incoming (Grade|Year|freshman)", r"eligible_year_levels"]),
  ("RC06_incoming_entry_only", "Incoming / entry-stage only (freshman or grade-entry)", [r"Incoming Freshman Only\??\s*:\s*Yes", r"strictly (?:for |restricted to )?incoming", r"incoming freshman only", r"Grade 11 entry", r"zero \(?0\)? earned", r"no earned tertiary", r"have not earned any college", r"no college units?", r"without credited (?:college|tertiary) units", r"no transferees?/shiftees? with credited"]),
  ("RC07_zero_prior_tertiary_units", "Zero prior tertiary units / no credited college units", [r"zero \(?0\)? earned", r"0 earned tertiary", r"no earned (?:tertiary|college) units", r"have not earned any (?:college|tertiary)", r"without credited", r"no college units prior", r"must not have earned"]),
  ("RC08_continuing_year_window", "Continuing students only / mid-program year window", [r"Incoming Freshmen are strictly barred", r"restricted exclusively to Year 2", r"only for (?:2nd|second)[- ]year", r"Junior Level", r"currently enrolled.*Year", r"ongoing (?:college|undergraduate) students"]),
  ("RC09_transferee_shiftee_bar", "Transferees/shiftees barred or restricted", [r"No transferees?/shiftees?", r"transferees? (?:are )?not eligible", r"shiftees? (?:are )?not", r"lateral entrants? (?:are )?not", r"ineligible.*transferee"]),
  ("RC10_lateral_entry_allowed", "Lateral entry allowed (graduate/ongoing)", [r"Lateral entry", r"ongoing graduate students with earned units"]),
  ("RC11_min_gwa_cutoff", "Minimum GWA / grade cutoff", [r"Minimum GWA\s*:", r"GWA\s*(?:of )?≥|GWA\s*>=|GWA of at least|GWA\s*≥", r"General Weighted Average"]),
  ("RC12_academic_or_class_rank", "Class rank / Top N% alternative or gate", [r"Alternative Class Rank\s*:\s*(?!NOT SPECIFIED)", r"Top\s*\d+\s*%", r"Top\s*\d+\b", r"class rank", r"graduating class"]),
  ("RC13_academic_any_of_gwa_or_rank", "Compound academic OR (GWA or rank)", [r"GWA.*\bOR\b.*(?:Top|rank)", r"(?:Top|rank).*\bOR\b.*GWA", r"either.*GWA.*or.*(?:rank|Top)", r"95%.*Top\s*5|Top\s*5.*95"]),
  ("RC14_per_subject_grade_floor", "Per-subject minimum grade floor", [r"no subject grade lower", r"no grade below", r"no failing grades", r"grades of at least", r"zero failing"]),
  ("RC15_income_annual_ceiling", "Household income annual ceiling", [r"Income Ceilings?\s*:\s*(?!NOT SPECIFIED)", r"annual (?:gross )?(?:family |household )?income", r"income must not exceed", r"income ceiling", r"₱\s*\d|PHP\s*\d"]),
  ("RC16_income_uncapped_merit_track", "Merit track with no income ceiling", [r"income is uncapped", r"no income ceiling", r"Merit \(no income", r"uncapped"]),
  ("RC17_income_proxy_4ps_listahanan", "Need gate via 4Ps/Listahanan/per-capita proxy", [r"Listahanan", r"Listahan", r"4Ps", r"per capita income", r"Pantawid"]),
  ("RC18_parent_salary_grade_ceiling", "Parent civil-service salary grade ceiling", [r"Salary Grade", r"SG\s*-?\s*\d+", r"salary grade"]),
  ("RC19_age_numeric_bounds", "Numeric min/max age bounds", [r"Age Restrictions?\s*:\s*(?!NOT SPECIFIED)", r"years of age", r"under \d+ years", r"above \d+ years", r"at least \d+ years old", r"max_age|min_age"]),
  ("RC20_age_birthdate_as_of", "Birthdate cutoff relative to intake date", [r"born (?:on or )?(?:after|before)", r"Born on or after", r"born after"]),
  ("RC21_school_list_or_consortium", "Named school / consortium / partner HEI lock", [r"consortium", r"member universit", r"partner (?:school|SUC|HEI|universit)", r"restricted strictly to", r"designated .* universit", r"NSC member"]),
  ("RC22_school_category_suc_luc_public", "School category restriction (SUC/LUC/public/private)", [r"State Universities and Colleges", r"\bSUCs?\b", r"\bLUCs?\b", r"public HEI", r"private HEI", r"CHED-recognized"]),
  ("RC23_field_of_study_restriction", "Field / priority course / PSCED restriction", [r"Priority Courses?\s*:\s*(?!NOT SPECIFIED)", r"priority (?:S&T |STEM )?fields", r"must be enrolled in", r"approved STEM", r"priority courses"]),
  ("RC24_sector_registry_NCFRS", "NCFRS coconut farmer registry", [r"\bNCFRS\b", r"coconut farmer"]),
  ("RC25_sector_registry_RSBSA", "RSBSA farmer/fisher registry", [r"\bRSBSA\b"]),
  ("RC26_sector_registry_SRA", "SRA sugarcane registry", [r"\bSRA\b", r"Sugar Regulatory Administration", r"sugarcane"]),
  ("RC27_affiliation_ofw_owwa", "OFW/OWWA membership or dependent affiliation", [r"\bOWWA\b", r"\bOFW\b", r"overseas Filipino"]),
  ("RC28_affiliation_military_afp", "Military / AFP / uniformed dependent affiliation", [r"\bAFP\b", r"military", r"AFPEBSO", r"KIA", r"uniformed service"]),
  ("RC29_affiliation_gsis_sss", "GSIS/SSS member dependent affiliation", [r"\bGSIS\b", r"\bSSS\b"]),
  ("RC30_affiliation_ip_ncip", "Indigenous Peoples / NCIP affiliation", [r"\bNCIP\b", r"Indigenous", r"\bIP\b", r"Lumad", r"ICCs?/IPs?"]),
  ("RC31_affiliation_hei_faculty_staff", "HEI faculty / staff / educator affiliation", [r"faculty member", r"HEI (?:staff|personnel|employee)", r"Science or Mathematics teacher", r"plantilla faculty", r"educator"]),
  ("RC32_equity_pwd_solo_underprivileged", "Equity priority groups (PWD/solo parent/underprivileged)", [r"\bPWD\b", r"Person with Disability", r"Solo Parent", r"underprivileged", r"GIDA"]),
  ("RC33_parent_deceased_or_incapacitated", "Parent deceased or permanently incapacitated", [r"deceased", r"permanently incapacitated", r"casualty"]),
  ("RC34_grant_exclusivity_national", "Non-concurrency with other national StuFAPs/grants", [r"national government-funded", r"other StuFAP", r"CHED Scholarship Programs \(CSPs\)", r"cannot hold.*national", r"not be beneficiaries of TES", r"not.*other.*government.*scholarship", r"Affidavit of No Existing Scholarship"]),
  ("RC35_grant_exclusivity_lgu", "Non-concurrency with other LGU grants", [r"another LGU", r"other LGU", r"enjoying another.*LGU", r"other local (?:government )?scholarship", r"duplicate.*LGU"]),
  ("RC36_one_scholar_per_family", "One scholar per family/household cap", [r"One-Scholar-One-Family", r"One Child Per Family", r"one scholar per (?:family|household)", r"only one (?:child|scholar|beneficiary|grantee) per (?:family|household|sponsor)"]),
  ("RC37_min_work_experience", "Minimum post-study work experience", [r"work experience", r"years of (?:relevant )?work", r"professional experience", r"post-graduation work", r"at least two \(?2\)? years"]),
  ("RC38_marital_status_single", "Single marital status required", [r"single marital status", r"must be single", r"unmarried"]),
  ("RC39_exam_board_nmat_prerequisite", "Entrance/board/NMAT/qualifying exam prerequisite", [r"\bNMAT\b", r"qualifying exam", r"entrance exam", r"board exam", r"DOST.*exam", r"scholarship examination"]),
  ("RC40_prior_degree_required", "Completed bachelor's / prior degree required", [r"completed Bachelor", r"bachelor'?s degree", r"must possess a .* degree", r"holder of a bachelor"]),
  ("RC41_first_ug_degree_only", "First undergraduate degree only", [r"first undergraduate degree", r"first degree", r"no prior bachelor", r"have not yet earned a bachelor"]),
  ("RC42_return_service_obligation", "Return service obligation (eligibility/commitment)", [r"return service", r"service obligation", r"Service Agreement", r"Service Contract"]),
  ("RC43_full_time_study_employment_bar", "Full-time study / employment bar while on grant", [r"full-time student", r"must NOT be employed", r"not be employed or practicing"]),
  ("RC44_good_moral_required", "Good moral / NBI character requirement", [r"Good Moral", r"NBI Clearance"]),
  ("RC45_health_medical_fit", "Health / medical fitness requirement", [r"Health Requirements?\s*:\s*(?!NOT SPECIFIED)", r"medically fit", r"medical certificate", r"physical examination"]),
  ("RC46_voter_registration", "Voter registration requirement", [r"voter(?:'s)? registration", r"registered voter"]),
  ("RC47_track_split_merit_vs_need", "Multi-track rules under one program (merit vs need)", [r"Merit.*RA 7687|RA 7687.*Merit", r"two tracks", r"Merit \(RA", r"separate Merit", r"Economic Track", r"Academic Track"]),
  ("RC48_partner_placement_university_lock", "Study-placement university lock for priority programs", [r"UP System only", r"ADMU only", r"DLSU only", r"study placement", r"must enroll in"]),
]

# Compile
compiled = [(cid, label, [re.compile(p, re.I) for p in pats]) for cid, label, pats in RULE_DEFS]

inventory = {}
for cid, label, regs in compiled:
    hits = []
    for sid, s in corpus.items():
        text = s.get("full_text") or ""
        # Also include structured fields if present
        fields = s.get("fields") or {}
        field_blob = "\n".join(f"{k}: {v}" for k,v in fields.items())
        blob = text + "\n" + field_blob
        if any(r.search(blob) for r in regs):
            hits.append({"id": int(sid), "title": re.sub(r"\s+", " ", s.get("title") or "").strip()[:90]})
    # dedupe by id
    uniq = {}
    for h in hits:
        uniq[h["id"]] = h
    inventory[cid] = {
        "label": label,
        "count": len(uniq),
        "scholarships": [uniq[i] for i in sorted(uniq)],
    }

# Print summary
for cid, data in inventory.items():
    print(f"{cid}\t{data['count']}\t{data['label']}")
    ids = ",".join(str(s['id']) for s in data['scholarships'][:25])
    print(f"  ids: {ids}{'...' if data['count']>25 else ''}")

out = pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\export\_rule_class_inventory.json")
out.write_text(json.dumps(inventory, indent=2, ensure_ascii=False), encoding="utf-8")
print("\nWrote", out)
print("Scholarships covered:", len(corpus))
print("Rule classes:", len(inventory))
