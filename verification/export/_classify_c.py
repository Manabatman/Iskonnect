import pathlib, re, json, sys
from collections import defaultdict, Counter
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
raw = json.loads(pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\export\_rule_inventory_raw.json").read_text(encoding="utf-8"))

def is_not_specified(v):
    if not v: return True
    return "NOT SPECIFIED" in v.upper() or v.strip().upper() in ("N/A", "NONE", "NO", "-")

def is_yes(v):
    return bool(v) and re.match(r"(?i)^\s*yes\b", v.strip())

def is_no(v):
    return bool(v) and re.match(r"(?i)^\s*no\b", v.strip())

# Classify interesting rule signals
classes = defaultdict(list)  # class -> list of (id, title, evidence snippet)

for s in raw:
    sid, title, f = s["id"], s["title"], s["fields"]
    # dedupe later by id
    def add(cls, evidence):
        classes[cls].append((sid, title, evidence[:180]))

    # Citizenship Filipino
    cit = f.get("citizenship","")
    if cit and not is_not_specified(cit):
        if re.search(r"Filipino|Philippine", cit, re.I):
            add("citizenship_filipino_required", cit)
        if re.search(r"natural.?born", cit, re.I):
            add("citizenship_natural_born_required", cit)

    # Residency / LGU
    res = f.get("residency","")
    if res and not is_not_specified(res):
        add("residency_or_locality_required", res)

    # Education levels
    el = f.get("education_level","")
    if el and not is_not_specified(el):
        if re.search(r"Graduate|Master|PhD|Doctor", el, re.I):
            add("education_level_graduate", el)
        if re.search(r"Undergrad|College", el, re.I):
            add("education_level_undergraduate", el)
        if re.search(r"High School|Grade 11|SHS|Senior High", el, re.I):
            add("education_level_shs", el)
        if re.search(r"TVET|TESDA", el, re.I):
            add("education_level_tvet", el)

    # Year levels
    yl = f.get("eligible_year_levels","")
    if yl and not is_not_specified(yl):
        add("year_level_restriction", yl)

    # Incoming freshman
    inc = f.get("incoming_freshman_only","")
    if inc and not is_not_specified(inc):
        if is_yes(inc) or re.search(r"primary focus is incoming|strictly|exclusively incoming", inc, re.I):
            add("incoming_freshman_only_or_primary", inc)
        elif is_no(inc):
            add("incoming_freshman_not_required", inc)
        else:
            add("incoming_freshman_partial_or_conditional", inc)

    # Existing college / continuing
    ex = f.get("existing_college","")
    if ex and not is_not_specified(ex):
        if re.search(r"(?i)^\s*yes|eligible|allowed|limited", ex):
            add("continuing_students_allowed", ex)
        if re.search(r"(?i)ineligible|no\b|not eligible", ex):
            add("continuing_students_ineligible", ex)

    # Min GWA
    gwa = f.get("min_gwa","")
    if gwa and not is_not_specified(gwa):
        add("min_gwa_cutoff", gwa)

    # Alt class rank
    rank = f.get("alt_class_rank","")
    if rank and not is_not_specified(rank):
        add("alternative_class_rank", rank)

    # Income
    incm = f.get("income_ceilings","")
    if incm and not is_not_specified(incm):
        add("income_ceiling", incm)
        if re.search(r"salary grade|SG\s*-?\d", incm, re.I):
            add("parent_salary_grade_ceiling", incm)
        if re.search(r"per capita|Listahanan|4Ps", incm, re.I):
            add("income_proxy_listahanan_4ps_or_per_capita", incm)

    # Age
    age = f.get("age_restrictions","")
    if age and not is_not_specified(age):
        add("age_restriction", age)
        if re.search(r"born|birth|as of|before|after|April|January|March", age, re.I):
            add("age_as_of_birthdate_cutoff", age)

    # School restrictions
    sch = f.get("school_restrictions","")
    if sch and not is_not_specified(sch):
        add("school_or_institution_restriction", sch)
        if re.search(r"consortium|member universit|NSC|partner", sch, re.I):
            add("consortium_or_partner_school_lock", sch)
        if re.search(r"SUC|LUC|public", sch, re.I):
            add("public_suc_luc_category_restriction", sch)
        if re.search(r"private", sch, re.I):
            add("private_hei_restriction", sch)

    # Priority courses / field
    pc = f.get("priority_courses","")
    if pc and not is_not_specified(pc):
        add("field_or_course_restriction", pc)

    # Sectoral
    sec = f.get("sectoral","")
    if sec and not is_not_specified(sec):
        add("sectoral_or_affiliation_requirement", sec)
        if re.search(r"NCFRS|coconut", sec, re.I):
            add("sector_registry_NCFRS", sec)
        if re.search(r"RSBSA", sec, re.I):
            add("sector_registry_RSBSA", sec)
        if re.search(r"SRA|sugar", sec, re.I):
            add("sector_registry_SRA", sec)
        if re.search(r"4Ps|Listahanan", sec, re.I):
            add("priority_4ps_listahanan", sec)
        if re.search(r"IP|indigenous|NCIP|Lumad", sec, re.I):
            add("affiliation_indigenous_people", sec)
        if re.search(r"OFW|OWWA", sec, re.I):
            add("affiliation_ofw_dependent", sec)
        if re.search(r"GSIS|AFP|military|uniformed|PNP", sec, re.I):
            add("affiliation_military_or_gsis", sec)
        if re.search(r"PWD|disability", sec, re.I):
            add("equity_pwd", sec)
        if re.search(r"fisher|farmer", sec, re.I):
            add("affiliation_farmer_fisher", sec)
        if re.search(r"HEI staff|faculty|employee", sec, re.I):
            add("affiliation_hei_staff_or_faculty", sec)

    # Good moral / health - process not matching usually
    gm = f.get("good_moral","")
    if gm and not is_not_specified(gm) and re.search(r"required|yes|must", gm, re.I):
        add("good_moral_certificate_required", gm)
    he = f.get("health","")
    if he and not is_not_specified(he) and re.search(r"required|yes|medical|fit", he, re.I):
        add("health_or_medical_requirement", he)

    # Other rules - mine keywords
    oth = f.get("other_rules","") or ""
    academic = f.get("academic_requirements","") or ""
    enroll = f.get("enrollment_requirement","") or ""
    blob = " | ".join([oth, academic, enroll, sec, sch, inc, yl])

    if re.search(r"zero\s*\(?\s*0\s*\)?\s*earned|no earned (tertiary|college)|0 earned|without credited|no college unit|have not earned", blob, re.I):
        add("zero_prior_tertiary_units", blob)
    if re.search(r"transferee|shiftee", blob, re.I):
        if re.search(r"no transferee|transferees? (are )?not|ineligible.*transferee|transferees?/shiftees", blob, re.I):
            add("transferee_or_shiftee_barred", blob)
        else:
            add("transferee_or_shiftee_mentioned", blob)
    if re.search(r"cannot hold|not (be )?a beneficiary|concurrent|another (LGU |national |CHED |government )?scholarship|dual.?grant|one.?grant|enjoying another|already enjoying|other StuFAP|other national", blob, re.I):
        add("grant_exclusivity_or_non_concurrency", blob)
    if re.search(r"one scholar per family|only one (child|scholar|beneficiary) per (family|household)|per family", blob, re.I):
        add("one_scholar_per_family", blob)
    if re.search(r"work experience|years of (relevant )?work|post.?graduat.*work|professional experience", blob, re.I):
        add("min_work_experience", blob)
    if re.search(r"return service|service obligation", blob, re.I):
        add("return_service_obligation", blob)
    if re.search(r"must be single|single marital|unmarried", blob, re.I):
        add("marital_status_single_required", blob)
    if re.search(r"NMAT|board exam|qualifying exam|entrance exam", blob, re.I):
        add("exam_or_board_prerequisite", blob)
    if re.search(r"deceased|permanently incapacitated|casualty", blob, re.I):
        add("parent_deceased_or_incapacitated", blob)
    if re.search(r"Top\s*\d|top\s*\d+%|class rank|rank in class|graduating class", blob, re.I):
        add("class_rank_or_percentile_gate", blob)
    if re.search(r"no subject grade lower|no grade below|minimum subject", blob, re.I):
        add("per_subject_grade_floor", blob)
    if re.search(r"first undergraduate|first degree|no prior bachelor|have not yet earned a bachelor", blob, re.I):
        add("first_undergraduate_degree_only", blob)
    if re.search(r"lateral entr", blob, re.I):
        add("lateral_entry_rule", blob)

# Print summary
print("RULE CLASS COUNTS (from Group C structured + partial)")
for cls, items in sorted(classes.items(), key=lambda x: -len({i[0] for i in x[1]})):
    ids = sorted({i[0] for i in items})
    print(f"\n## {cls}  count={len(ids)} ids={ids}")
    for sid, title, ev in items[:3]:
        print(f"   - {sid}: {title[:50]} | {ev[:100]}")
