import pathlib, re, json, sys
from collections import OrderedDict
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

corpus = json.loads(pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\export\_scholarship_corpus.json").read_text(encoding="utf-8"))
raw_c = json.loads(pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\export\_rule_inventory_raw.json").read_text(encoding="utf-8"))

# Prefer structured fields for Group C ids
fields_by_id = {}
for s in raw_c:
    fields_by_id[s["id"]] = s["fields"]
    # keep official title if better
    if s["id"] in corpus and s.get("fields"):
        pass

def not_spec(v):
    if v is None: return True
    u = v.upper()
    return "NOT SPECIFIED" in u or u.strip() in ("", "N/A", "NONE", "-")

def clean_title(t):
    t = re.sub(r"\s+", " ", t or "").strip()
    t = re.sub(r"\d+$", "", t).strip()  # trailing footnote nums
    return t[:100]

def eligibility_slice(text):
    """Prefer Official Eligibility through Renewal/Disqualifying end."""
    if not text:
        return ""
    m = re.search(r"Official Eligibility Requirements(.*?)(?:\n8\.\s+Renewal|\n9\.\s+Disqualifying|\n10\.\s+Temporal|\n4\.\s+Application Timing|\nProduction Database|\nMatching Risks|\Z)", text, re.S|re.I)
    if m:
        return m.group(1)
    # include disqualifying if present separately
    m2 = re.search(r"Disqualifying Conditions(.*?)(?:\n10\.\s+Temporal|\n11\.\s+Structured|\n12\.\s+Production|\Z)", text, re.S|re.I)
    elig = m.group(0) if m else text[:8000]
    if m2:
        elig += "\n" + m2.group(1)
    return elig

# Build per-scholarship analysis blob = eligibility slice + structured fields
profiles = {}
for sid, s in corpus.items():
    sid_i = int(sid)
    elig = eligibility_slice(s.get("full_text") or "")
    f = fields_by_id.get(sid_i) or s.get("fields") or {}
    field_lines = "\n".join(f"{k}: {v}" for k,v in f.items())
    profiles[sid_i] = {
        "id": sid_i,
        "title": clean_title(s.get("title") or ""),
        "elig": elig,
        "fields": f,
        "blob": elig + "\n" + field_lines,
    }

# Precise rule class definitions using field-aware logic where possible

def add(inv, key, sid, note=""):
    inv[key]["ids"].add(sid)
    if note:
        inv[key]["notes"][sid] = note[:160]

inv = OrderedDict()

def ensure(key, label, desc):
    if key not in inv:
        inv[key] = {"label": label, "desc": desc, "ids": set(), "notes": {}}

# Define classes
CLASSES = [
("RC01","Citizenship — Filipino required","Applicant must be Filipino (natural-born and/or naturalized)."),
("RC02","Citizenship — natural-born only","Stricter natural-born-only citizenship (when explicitly exclusive)."),
("RC03","Local residency / LGU locality","Must reside in a city/municipality/province (LGU or locality gate)."),
("RC04","Education level / academic stage","Eligible education stage (SHS/College/TVET/Graduate/MD)."),
("RC05","Year-level window","Explicit eligible year levels or year window."),
("RC06","Incoming / entry-stage only","Restricted to incoming freshman / grade-entry / not yet enrolled."),
("RC07","Zero prior tertiary units","Must have earned zero college/tertiary/vocational units."),
("RC08","Continuing / mid-program entry window","Open to continuing students at specific years (not freshman-only); may bar first-years or upper years."),
("RC09","Transferee/shiftee barred","Transferees or shiftees with credited units ineligible."),
("RC10","Lateral entry allowed","Ongoing students with earned units may enter (esp. graduate)."),
("RC11","Minimum GWA cutoff","Numeric GWA/GPA minimum at entry."),
("RC12","Class rank / Top-N gate","Class rank or Top N/% used as academic gate or alternative."),
("RC13","Compound academic OR (GWA or rank)","Explicit OR between GWA threshold and class rank/Top-N."),
("RC14","Per-subject grade floor","No failing grades / subject minima at entry or retention-as-entry."),
("RC15","Household income ceiling","Numeric annual household/parental income cap."),
("RC16","Uncapped merit / need-exempt track","Merit (or similar) track with no income ceiling."),
("RC17","4Ps / Listahanan / per-capita need proxy","Need assessed via 4Ps/Listahanan or per-capita poverty proxies."),
("RC18","Parent salary-grade ceiling","Parent GSIS/civil-service salary grade upper bound."),
("RC19","Numeric age bounds","Min/max age in years (not birthdate-specific)."),
("RC20","Birthdate as-of cutoff","Eligibility by birthdate relative to a fixed/intake date."),
("RC21","Named school / consortium / partner lock","Must enroll in named partner/consortium schools."),
("RC22","School category (SUC/LUC/public/private/COE)","Restriction by school category/accreditation class."),
("RC23","Field / priority course restriction","Restricted to priority fields/courses/strands."),
("RC24","Sector registry — NCFRS","NCFRS coconut farmer (or dependent) registration required."),
("RC25","Sector registry — RSBSA","RSBSA farmer/fisher registration required."),
("RC26","Sector registry — SRA","SRA sugarcane farmer registration/certification required."),
("RC27","Affiliation — OFW/OWWA","OFW member or dependent affiliation required."),
("RC28","Affiliation — military/AFP/uniformed","Military/AFP/uniformed dependent (or casualty) affiliation."),
("RC29","Affiliation — GSIS/SSS member dependent","GSIS or SSS member-dependent affiliation."),
("RC30","Affiliation — IP / NCIP","Indigenous Peoples / NCIP certification."),
("RC31","Affiliation — HEI faculty/staff/educator","Must be HEI faculty/staff/educator (or dependent barred from bank staff etc. as inverse)."),
("RC32","Equity groups — PWD / solo parent / underprivileged / GIDA","Equity priority or reserved-slot groups."),
("RC33","Parent deceased or permanently incapacitated","Parent status deceased/incapacitated as eligibility gate."),
("RC34","Grant exclusivity — national StuFAP/government","Cannot concurrently hold other national government scholarships/StuFAPs."),
("RC35","Grant exclusivity — LGU","Cannot concurrently hold another LGU scholarship."),
("RC36","One scholar per family/household","Household/family cap of one scholar."),
("RC37","Minimum work experience","Minimum years of work/professional experience."),
("RC38","Marital status — single required","Must be single/unmarried."),
("RC39","Exam / NMAT / qualifying exam prerequisite","Must take/pass entrance, NMAT, or provider qualifying exam."),
("RC40","Prior bachelor's / degree required","Completed bachelor's (or equivalent) required for entry."),
("RC41","First undergraduate degree only","Must be pursuing first UG degree."),
("RC42","Return service commitment","Return service obligation as condition of award/eligibility."),
("RC43","Full-time study / employment bar","Must study full-time; employment/practice barred while on grant."),
("RC44","Good moral / character certification","Good moral or NBI/character required (process gate often)."),
("RC45","Health / medical fitness","Medical fitness/health clearance required."),
("RC46","Voter registration","Applicant/parent voter registration required."),
("RC47","Multi-track rule split (merit vs need/other)","Single catalog program with divergent track rules."),
("RC48","Municipal residency duration","Minimum years of local residency (e.g., 4 years)."),
("RC49","Fisherfolk / farmer occupation affiliation (non-registry or local list)","Parent fisherfolk/farmer affiliation via local registry/list (not only RSBSA)."),
("RC50","Employee/dependent exclusion (sponsor conflict)","Children of sponsor employees ineligible."),
]

for key,label,desc in CLASSES:
    ensure(key,label,desc)

for sid, p in profiles.items():
    f = p["fields"]
    blob = p["blob"]
    elig = p["elig"]

    # RC01 citizenship Filipino
    cit = f.get("citizenship") or ""
    if (cit and not not_spec(cit) and re.search(r"Filipino", cit, re.I)) or re.search(r"Filipino citizen", elig, re.I):
        add(inv,"RC01",sid)
    if re.search(r"natural-born Filipino(?! citizen residing)|must be a natural-born Filipino(?! or)", blob, re.I) and not re.search(r"natural-born or naturalized", blob, re.I):
        add(inv,"RC02",sid)

    # RC03 residency
    res = f.get("residency") or ""
    if (res and not not_spec(res)) or re.search(r"Proof of Residency|resident of|bona fide resident|QCitizen|must reside", elig, re.I):
        if res and not not_spec(res):
            add(inv,"RC03",sid, res)
        elif re.search(r"Proof of Residency|resident of|bona fide resident|QCitizen|must reside", elig, re.I):
            add(inv,"RC03",sid)

    # RC04 education level
    el = f.get("education_level") or ""
    if (el and not not_spec(el)) or re.search(r"Education Level\s*:", elig, re.I):
        add(inv,"RC04",sid)

    # RC05 year levels
    yl = f.get("eligible_year_levels") or ""
    if (yl and not not_spec(yl)) or re.search(r"Eligible Year Levels?\s*:", elig, re.I):
        add(inv,"RC05",sid)

    # RC06 incoming only — Yes, or explicit exclusive incoming
    inc = f.get("incoming_freshman_only") or ""
    if re.match(r"(?i)^\s*Yes\b", inc.strip()) or re.search(r"Incoming Freshman Only\??\s*:\s*Yes", elig, re.I) or re.search(r"Incoming college freshmen only|incoming first-year college student\.|Who May Apply:\s*Incoming college freshmen only", elig, re.I):
        add(inv,"RC06",sid, inc or "incoming only")

    # RC07 zero units
    if re.search(r"zero\s*\(?\s*0\s*\)?\s*(?:earned\s+)?(?:post-secondary|college|tertiary|vocational)?\s*units|earned zero\s*\(?\s*0\s*\)?\s*units|0 Tertiary Units|has NOT earned any|no earned tertiary|must have earned zero|possession of earned tertiary", blob, re.I):
        add(inv,"RC07",sid)

    # RC08 continuing window — Megaworld-like, JLSS year 2, Aboitiz year 2
    if re.search(r"Incoming Freshmen are strictly barred|Junior Level Science|Open to Incoming Freshmen.*Incoming Sophomores|restricted exclusively to Year 2|2nd[- ]year students", blob, re.I):
        add(inv,"RC08",sid)

    # RC09 transferee bar
    if re.search(r"transferees? or shiftees?.*ineligible|No\s*\(\s*\"?Applicants who are transferees|Can transferees or shiftees apply\?:\s*No|transferees?/shiftees? with credited", blob, re.I):
        add(inv,"RC09",sid)

    # RC10 lateral
    if re.search(r"Lateral entry", blob, re.I):
        add(inv,"RC10",sid)

    # RC11 min GWA — field or explicit minimum
    gwa = f.get("min_gwa") or ""
    if (gwa and not not_spec(gwa) and re.search(r"\d", gwa)) or re.search(r"Minimum GWA\s*:\s*(?!NOT SPECIFIED).*\d|GWA of at least\s*\d|GWA\s*(?:of )?(?:≥|>=)\s*\d|overall GWA of at least", blob, re.I):
        add(inv,"RC11",sid)

    # RC12 class rank when NOT not-specified
    rank = f.get("alt_class_rank") or ""
    if (rank and not not_spec(rank)) or re.search(r"Alternative Class Rank\s*:\s*(?!NOT SPECIFIED)(?=.*\d|.*Top)|Top\s*\d+\s*% of|Top\s*(?:Five|5|10|20)\b|class rank", elig, re.I):
        # avoid matching ONLY the label with NOT SPECIFIED
        if rank and not not_spec(rank):
            add(inv,"RC12",sid, rank)
        elif re.search(r"Top\s*\d|Top\s*Five|class rank|Overall Rank", elig, re.I) and not re.search(r"Alternative Class Rank\s*:\s*NOT SPECIFIED", elig, re.I):
            add(inv,"RC12",sid)
        elif re.search(r"Alternative Class Rank\s*:\s*(?!NOT SPECIFIED).{0,80}(Top|\d)", elig, re.I):
            add(inv,"RC12",sid)

    # RC13 OR academic
    if re.search(r"Top\s*(?:Five|5).{0,40}\bOR\b.{0,40}GWA|GWA.{0,40}\bOR\b.{0,40}Top\s*(?:Five|5)|95%.*Top\s*5|Top\s*5.*95|gwa\s*>=\s*95.*class_rank|minimum_gwa:\s*95\.00 \(or top 5", blob, re.I):
        add(inv,"RC13",sid)

    # RC14 per-subject floor
    if re.search(r"no subject grade lower|no grade below|zero failing grades|with no failing|no conditional or failing|at least 80% grade in all|no failing, incomplete", blob, re.I):
        add(inv,"RC14",sid)

    # RC15 income ceiling — field or explicit not exceed
    incm = f.get("income_ceilings") or ""
    if (incm and not not_spec(incm) and re.search(r"\d|PHP|₱|exceed", incm, re.I)) or re.search(r"Income Ceilings?\s*:\s*(?!NOT SPECIFIED).{0,120}\d|income must not exceed|gross (?:annual )?income.{0,40}not exceed|income_limit:\s*\d", blob, re.I):
        add(inv,"RC15",sid)

    # RC16 uncapped merit
    if re.search(r"Uncapped \(Merit\)|no income ceiling|Income is uncapped|Merit.*Uncapped|uncapped", blob, re.I):
        add(inv,"RC16",sid)

    # RC17 4Ps/Listahanan
    if re.search(r"Listahanan|Listahan|4Ps|Pantawid|per capita", blob, re.I):
        add(inv,"RC17",sid)

    # RC18 salary grade
    if re.search(r"Salary Grade\s*\d+|SG\s*\d+|salary grade", blob, re.I):
        add(inv,"RC18",sid)

    # RC19 age numeric - field age_restrictions with digits, exclude NOT SPECIFIED
    age = f.get("age_restrictions") or ""
    if (age and not not_spec(age) and re.search(r"\d", age)) or re.search(r"Age Restrictions?\s*:\s*(?!NOT SPECIFIED).{0,80}\d|under \d+ years|above \d+ years|aged \d+", elig, re.I):
        if not re.search(r"born (?:on or )?(?:after|before)", age, re.I):
            add(inv,"RC19",sid, age[:80] if age else "")

    # RC20 birthdate
    if re.search(r"born (?:on or )?(?:after|before)|Born on or after", blob, re.I):
        add(inv,"RC20",sid)

    # RC21 named schools / consortium / partner
    sch = f.get("school_restrictions") or ""
    if re.search(r"consortium|partner (?:school|universit|HEI|SUC)|Megaworld Foundation's \d+ partner|SM Foundation Partner|National Science Consortium|ERDT Consortium|CBPSME Consortium|designated Partner|participating SUCs or designated", blob, re.I):
        add(inv,"RC21",sid)

    # RC22 school category
    if re.search(r"\bSUCs?\b|\bLUCs?\b|State Universities and Colleges|private HEIs|public schools|Autonomous or Deregulated|COE/COD|FAAP Level", blob, re.I):
        add(inv,"RC22",sid)

    # RC23 field
    pc = f.get("priority_courses") or ""
    if (pc and not not_spec(pc)) or re.search(r"Priority Courses?\s*:\s*(?!NOT SPECIFIED|Applicable to all|Any )|priority (?:S&T |STEM )?fields|STEM degree|Doctor of Medicine", elig, re.I):
        add(inv,"RC23",sid)

    # Registries
    if re.search(r"\bNCFRS\b", blob):
        add(inv,"RC24",sid)
    if re.search(r"\bRSBSA\b", blob):
        add(inv,"RC25",sid)
    if re.search(r"Sugar Regulatory Administration|\bSRA\b.*sugar|sugarcane", blob, re.I):
        add(inv,"RC26",sid)

    # Affiliations
    if re.search(r"\bOWWA\b|OFW (?:member|Dependent|parent)|child of an active OWWA|overseas Filipino worker", blob, re.I):
        add(inv,"RC27",sid)
    if re.search(r"AFPEBSO|child of active.*AFP|military personnel|KIA|AFPSLAI", blob, re.I):
        add(inv,"RC28",sid)
    if re.search(r"GSIS member|dependent of active GSIS|\bSSS\b member", blob, re.I):
        add(inv,"RC29",sid)
    if re.search(r"\bNCIP\b|Indigenous Peoples|\bIP\b certificate|Lumad", blob, re.I):
        add(inv,"RC30",sid)
    if re.search(r"plantilla faculty|HEI faculty|Science or Mathematics teacher|faculty member of an eligible", blob, re.I):
        add(inv,"RC31",sid)
    if re.search(r"\bPWD\b|Solo Parent|underprivileged|\bGIDA\b|Person with Disability", blob, re.I):
        add(inv,"RC32",sid)
    if re.search(r"deceased|permanently incapacitated", blob, re.I):
        add(inv,"RC33",sid)

    # Exclusivity
    if re.search(r"national government(?:-funded)?|other StuFAP|CHED Scholarship Programs|Dual enjoyment of major (?:national )?government|Affidavit of No Existing Scholarship|not be beneficiaries of TES|cannot hold.*government scholarship", blob, re.I):
        add(inv,"RC34",sid)
    if re.search(r"another LGU|other LGU|lgu_exclusivity|other local (?:government )?scholarship|enjoying another", blob, re.I):
        add(inv,"RC35",sid)
    if re.search(r"One-Scholar-One-Family|One Child Per Family|one scholar per (?:family|household)|only one (?:child|scholar|beneficiary|grantee) per (?:family|household|sponsor)", blob, re.I):
        add(inv,"RC36",sid)

    # Work exp
    if re.search(r"work experience|years of (?:relevant )?work|professional experience|at least two \(?2\)? years.*(work|experience)", blob, re.I):
        add(inv,"RC37",sid)

    # Marital
    if re.search(r"single marital status|must be single|unmarried", blob, re.I):
        add(inv,"RC38",sid)

    # Exam - only if eligibility/prereq not just document list noise: look for NMAT required, qualifying examination required
    if re.search(r"\bNMAT\b|DOST-SEI Undergraduate Exam|qualifying examination|must take.*exam|Scholarship Examination", elig, re.I):
        add(inv,"RC39",sid)

    # Prior degree
    if re.search(r"Bachelor'?s Degree|completed Bachelor|must possess a .*degree|holder of a bachelor|post-baccalaureate", blob, re.I):
        add(inv,"RC40",sid)

    # First UG
    if re.search(r"first undergraduate degree", blob, re.I):
        add(inv,"RC41",sid)

    # Return service - from eligibility/benefits commitment
    if re.search(r"return service|Service Agreement|Service Contract|service obligation", elig, re.I) or (f.get("other_rules") and re.search(r"return service", f.get("other_rules",""), re.I)):
        add(inv,"RC42",sid)

    # Full-time / employment bar
    if re.search(r"full-time student|must NOT be employed|not be employed or practicing", blob, re.I):
        add(inv,"RC43",sid)

    # Good moral - Required in eligibility
    gm = f.get("good_moral") or ""
    if (gm and not not_spec(gm) and re.search(r"Required|Yes|must", gm, re.I)) or re.search(r"Good Moral\s*:\s*Required", elig, re.I):
        add(inv,"RC44",sid)

    # Health
    he = f.get("health") or ""
    if (he and not not_spec(he) and re.search(r"Required|Yes|medical|fit", he, re.I)) or re.search(r"medically fit|medical certificate|physical examination", elig, re.I):
        add(inv,"RC45",sid)

    # Voter
    if re.search(r"voter(?:'s)? registration|registered voter", blob, re.I):
        add(inv,"RC46",sid)

    # Multi-track
    if re.search(r"RA 7687.*Merit|Merit.*RA 7687|two tracks|BPMSP Track|CMSP Track|Economic Track|Academic Scholarship Track|QC Excel", blob, re.I):
        add(inv,"RC47",sid)

    # Municipal residency duration
    if re.search(r"resident of the municipality for at least|residency >= \d|at least four \(?4\)? years", blob, re.I):
        add(inv,"RC48",sid)

    # Fisherfolk local
    if re.search(r"registered fisherfolk|fisherfolk listed|small farmer or fisherfolk", blob, re.I):
        add(inv,"RC49",sid)

    # Employee exclusion
    if re.search(r"must NOT be a child or dependent of a .{0,40}employee|children of employees are ineligible|Security Bank employee", blob, re.I):
        add(inv,"RC50",sid)

# Manual force-add for known critical from Group A/B if missed
MANUAL = {
    "RC07": [73,76,10],  # SM is incoming only - units implied; keep 73,76 for sure
    "RC06": [73,76,10,117,78],
    "RC13": [76],
    "RC24": [117],
    "RC18": [78],
    "RC35": [88],
    "RC08": [130,75,61],
    "RC21": [61,10,133,134,135],
    "RC34": [5,66,54,117,73],
    "RC09": [76],
    "RC47": [73,76,88],
    "RC12": [73,76,31,88],
    "RC39": [73,130,54],
}
for key, ids in MANUAL.items():
    for sid in ids:
        if sid in profiles:
            add(inv,key,sid,"manual_canonical")

# Support mapping vs current schema / proposed architecture
SUPPORT = {
"RC01": ("yes","yes","atomic+logic","citizenship_required already"),
"RC02": ("partial","yes","atomic+logic","citizenship enum needs natural_born value"),
"RC03": ("yes","yes","data","eligible_cities/regions + residency_required"),
"RC04": ("yes","yes","data","eligible_levels"),
"RC05": ("yes","yes","data","eligible_year_levels"),
"RC06": ("partial","yes","data+logic","eligible_enrollment_status=incoming_freshman; backfill"),
"RC07": ("no","yes","atomic+logic","max_prior_tertiary_units + prior_tertiary_units"),
"RC08": ("partial","yes","data+logic","year_levels + enrollment_status combinations"),
"RC09": ("partial","yes","policy+logic","entry.allow_transferee=false in eligibility_policy"),
"RC10": ("partial","yes","policy+data","lateral allowed via enrollment/year; document in policy"),
"RC11": ("yes","yes","data","min_gwa_normalized"),
"RC12": ("no","yes","atomic+policy+logic","class_rank/size on student; rank ops in policy"),
"RC13": ("no","yes","policy+logic","academic_any_of"),
"RC14": ("no","partial","policy","usually process/retention; optional entry predicate"),
"RC15": ("yes","yes","data","max_income_threshold — needs remediation"),
"RC16": ("partial","yes","data+logic","null income + scholarship_type/track; track split RC47"),
"RC17": ("partial","yes","data+logic","priority_groups + is_4ps_listahanan; members_only"),
"RC18": ("no","yes","atomic+logic","parent_salary_grade student field + policy/max"),
"RC19": ("yes","yes","data","min_age/max_age"),
"RC20": ("no","yes","policy+logic","age_as_of in eligibility_policy"),
"RC21": ("yes","yes","data","eligible_schools — must populate"),
"RC22": ("yes","yes","data","eligible_school_categories/types"),
"RC23": ("yes","yes","data","eligible_courses_psced/specific"),
"RC24": ("partial","yes","taxonomy+logic","sector_registries + members_only"),
"RC25": ("partial","yes","taxonomy+logic","sector_registries + members_only"),
"RC26": ("partial","yes","taxonomy+logic","sector_registries + members_only"),
"RC27": ("yes","yes","data+logic","is_ofw_dependent + priority_groups/members_only"),
"RC28": ("yes","yes","data+logic","is_military_dependent + members_only"),
"RC29": ("yes","yes","data+logic","is_gsis_dependent + members_only"),
"RC30": ("yes","yes","data+logic","is_indigenous_people + members_only"),
"RC31": ("no","yes","atomic+logic","profile faculty/staff flag + members_only/policy"),
"RC32": ("yes","yes","data+logic","equity flags + priority_groups"),
"RC33": ("no","yes","atomic+logic","parent_status enum on profile + policy/members"),
"RC34": ("no","yes","atomic+logic","conflict_scopes national_stufap"),
"RC35": ("no","yes","atomic+logic","conflict_scopes lgu_grant"),
"RC36": ("no","partial","policy+explain","disclosure until household graph; no fake hard gate"),
"RC37": ("no","yes","atomic+logic","min_work_experience_years"),
"RC38": ("no","yes","atomic+logic","marital_status"),
"RC39": ("partial","partial","data+explain","has_qualifying_exam exists; hard gate only if profile has exam status"),
"RC40": ("partial","yes","data+logic","education_level Graduate + prior degree flag"),
"RC41": ("no","yes","policy+logic","first_degree_only in policy"),
"RC42": ("partial","yes","data+explain","has_return_service; details in policy"),
"RC43": ("no","partial","policy","post-award condition; soft/explain unless profile employment contradicts"),
"RC44": ("no","partial","explain","process requirement; not hard match v1"),
"RC45": ("no","partial","explain","process requirement; not hard match v1"),
"RC46": ("no","partial","policy+explain","optional profile flag; LGU-specific"),
"RC47": ("no","yes","data+model","split catalog rows or track objects under parent"),
"RC48": ("no","yes","policy+logic","min_residency_years in policy"),
"RC49": ("partial","yes","taxonomy+logic","fisher/farmer flags + local registry tags"),
"RC50": ("no","partial","policy+explain","sponsor-employee exclusion; rare"),
}

# Serialize
out_obj = OrderedDict()
for key, meta in inv.items():
    ids = sorted(meta["ids"])
    cur, prop, impl, note = SUPPORT[key]
    out_obj[key] = {
        "label": meta["label"],
        "description": meta["desc"],
        "count": len(ids),
        "scholarship_ids": ids,
        "scholarships": [{"id": i, "title": profiles[i]["title"]} for i in ids if i in profiles],
        "current_schema_supported": cur,
        "proposed_architecture_supported": prop,
        "implementation_needs": impl,
        "implementation_note": note,
    }

path = pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\export\_rule_class_inventory_v2.json")
path.write_text(json.dumps(out_obj, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Scholarships in corpus: {len(profiles)}")
print(f"{'ID':<8}{'N':>4}  {'Cur':<8}{'Prop':<8}{'Impl':<22} Label")
for key, o in out_obj.items():
    print(f"{key:<8}{o['count']:>4}  {o['current_schema_supported']:<8}{o['proposed_architecture_supported']:<8}{o['implementation_needs']:<22} {o['label']}")

# coverage check critical
for sid in [73,76,10,61,130,54,117,78,7,88,5,66]:
    hits = [k for k,o in out_obj.items() if sid in o['scholarship_ids']]
    print(f"ID {sid} classes ({len(hits)}): {', '.join(hits)}")
