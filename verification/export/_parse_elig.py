import pathlib, re, json, sys
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\export\_pdf_extracts")

# Extract scholarship blocks: title with (ID: N) or ID N patterns
id_title_re = re.compile(
    r"(?P<title>[^\n]{5,160}?)\s*\(ID:\s*(?P<id>\d+)\)|"
    r"(?:Database\s+)?ID\s+(?P<id2>\d+)\s*\n\s*(?P<title2>[^\n]{5,160})",
    re.I
)

# Also bullet eligibility fields
field_patterns = {
    "citizenship": r"Citizenship\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z][a-z].*?:|\Z)",
    "residency": r"Residency\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z]|\Z)",
    "education_level": r"Education Level\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z]|\Z)",
    "eligible_year_levels": r"Eligible Year Levels?\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z]|\Z)",
    "incoming_freshman_only": r"Incoming Freshman Only\??\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z]|\Z)",
    "existing_college": r"Existing College Students\??\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z]|\Z)",
    "graduate_students": r"Graduate Students\??\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z]|\Z)",
    "enrollment_requirement": r"Current Enrollment Requirement\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z]|\Z)",
    "academic_requirements": r"Academic Requirements\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z]|\Z)",
    "min_gwa": r"Minimum GWA\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z]|\Z)",
    "alt_class_rank": r"Alternative Class Rank\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z]|\Z)",
    "income_ceilings": r"Income Ceilings?\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z]|\Z)",
    "age_restrictions": r"Age Restrictions?\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z]|\Z)",
    "school_restrictions": r"School Restrictions?\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z]|\Z)",
    "priority_courses": r"Priority Courses?\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z]|\Z)",
    "sectoral": r"Sectoral Requirements?\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z]|\Z)",
    "good_moral": r"Good Moral\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z]|\Z)",
    "health": r"Health Requirements?\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*[A-Z]|\Z)",
    "other_rules": r"Other Official Rules?\s*:\s*(.+?)(?=\n\s*[●\-]|\n\s*\d+\.|\n\s*[A-Z][a-z]+ Timing|\Z)",
}

scholarships = []
for f in sorted(base.glob("DATABASE_*.txt")):
    text = f.read_text(encoding="utf-8", errors="replace")
    # Find all ID: N headers
    headers = list(re.finditer(r"(?m)^([^\n]{5,140}?)\s*\(ID:\s*(\d+)\)\s*$", text))
    if not headers:
        headers = list(re.finditer(r"(?m)^([^\n]{5,140}?)\s*\(ID\s*(\d+)\)\s*$", text))
    # Also "ID 3" table style
    for m in re.finditer(r"(?m)^ID\s+(\d+)\s*$", text):
        # get following title-ish lines
        pass
    print(f"{f.name}: structured (ID: N) headers = {len(headers)}")
    for i, h in enumerate(headers):
        title = h.group(1).strip(" ●\-")
        sid = int(h.group(2))
        start = h.end()
        end = headers[i+1].start() if i+1 < len(headers) else len(text)
        block = text[start:end]
        # Get eligibility section if present
        elig = block
        m_elig = re.search(r"Official Eligibility Requirements(.*?)(?:\n\d+\.\s+Application|\n4\.\s+Application|\n5\.\s+|\Z)", block, re.S|re.I)
        if m_elig:
            elig = m_elig.group(1)
        fields = {}
        for k, pat in field_patterns.items():
            mm = re.search(pat, elig, re.S|re.I)
            if mm:
                val = re.sub(r"\s+", " ", mm.group(1)).strip(" ●\-\t ")
                # truncate
                fields[k] = val[:400]
        scholarships.append({
            "id": sid,
            "title": title[:120],
            "source_pdf": f.name,
            "fields": fields,
            "block_len": len(block),
            "has_elig_section": bool(m_elig),
        })

print("TOTAL structured scholarships", len(scholarships))
print("unique ids", len({s['id'] for s in scholarships}))
# show ones without many fields
for s in scholarships:
    print(f"  ID {s['id']}: {s['title'][:70]} fields={len(s['fields'])} elig={s['has_elig_section']} pdf={s['source_pdf'][:40]}")

out = pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\export\_rule_inventory_raw.json")
out.write_text(json.dumps(scholarships, indent=2, ensure_ascii=False), encoding="utf-8")
print("wrote", out)
