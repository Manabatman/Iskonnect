import pathlib, re, json, sys
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\export\_pdf_extracts")

# ---- Parse Group A (V1) by Program Audit N ----
v1 = (base/"DATABASE_V1_GROUPA.txt").read_text(encoding="utf-8", errors="replace")
# Known mapping from TOC
group_a = [
    (54, "CHED Medical Scholarship and Return Service (MSRS)", "Program Audit 1"),
    (78, "GSIS Subsidy for STEM Program (GSSP)", "Program Audit 2"),
    (7, "GSIS Scholarship Program (GSP - Main Track)", "Program Audit 3"),
    (117, "CHED Scholarship Program for Coconut Farmers (CoScho)", "Program Audit 4"),
    (88, "Quezon City Scholarship Program (QCSP)", "Program Audit 5"),
]
# Note: QCSP also in LGU_PART2 - keep both sources, prefer detailed

group_b = [
    (73, "DOST-SEI S&T Undergraduate Scholarships", "Program Audit 1"),
    (130, "DOST-SEI Junior Level Science Scholarship (JLSS)", "Program Audit 2"),
    (76, "CHED Bagong Pilipinas Merit Scholarship Program (BPMSP)", "Program Audit 3"),
    (61, "Megaworld Foundation Scholarship Program", "Program Audit 4"),
    (10, "SM Foundation College Scholarship Program", "Program Audit 5"),
]

def split_audits(text, audits):
    # Find "Program Audit N:" positions
    positions = []
    for sid, title, label in audits:
        m = re.search(re.escape(label) + r"[^\n]*", text)
        if not m:
            # try softer
            m = re.search(r"Program Audit\s+\d+:[^\n]*", text)
        positions.append((m.start() if m else -1, sid, title, label))
    positions = [p for p in positions if p[0] >= 0]
    positions.sort()
    blocks = []
    for i, (pos, sid, title, label) in enumerate(positions):
        end = positions[i+1][0] if i+1 < len(positions) else len(text)
        blocks.append({"id": sid, "title": title, "source": label, "text": text[pos:end]})
    return blocks

# Better: find each audit by number in order
def extract_program_audits(text, pdf_name):
    matches = list(re.finditer(r"(?m)^Program Audit\s+(\d+):\s*(.+)$", text))
    out = []
    for i, m in enumerate(matches):
        end = matches[i+1].start() if i+1 < len(matches) else min(len(text), m.start()+25000)
        out.append({
            "audit_num": int(m.group(1)),
            "audit_title": m.group(2).strip()[:160],
            "text": text[m.start():end],
            "pdf": pdf_name,
        })
    return out

a_audits = extract_program_audits(v1, "V1_GROUPA")
v2 = (base/"DATABASE_V2_GROUPB.txt").read_text(encoding="utf-8", errors="replace")
b_audits = extract_program_audits(v2, "V2_GROUPB")
print("Group A audits:", [(a["audit_num"], a["audit_title"][:80]) for a in a_audits])
print("Group B audits:", [(a["audit_num"], a["audit_title"][:80]) for a in b_audits])

# Map known IDs
id_map_a = {1:54, 2:78, 3:7, 4:117, 5:88}
id_map_b = {1:73, 2:130, 3:76, 4:61, 5:10}
title_map_a = {1:"CHED MSRS", 2:"GSIS GSSP STEM", 3:"GSIS GSP Main", 4:"CHED CoScho", 5:"QCSP"}
title_map_b = {1:"DOST-SEI Undergraduate", 2:"DOST-SEI JLSS", 3:"CHED BPMSP", 4:"Megaworld Foundation", 5:"SM Foundation College"}

# Also load Group C raw with official names from Official Name bullets
raw_c = json.loads(pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\export\_rule_inventory_raw.json").read_text(encoding="utf-8"))

# Enrich C titles from Official Name in source files
def official_name_from_block(block):
    m = re.search(r"Official Name\s*:\s*(.+)", block)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()[:120]
    return None

# Rebuild C with better titles and full eligibility+other text
scholarships = {}  # id -> dict

for s in raw_c:
    # Prefer first occurrence; skip duplicate 72/75 from P2 if already present unless better title
    sid = s["id"]
    # re-read block from pdf using ID header
    pdf = base / s["source_pdf"].replace(".txt",".txt")
    # already have fields; get official name from full extract around ID
    scholarships.setdefault(sid, {
        "id": sid,
        "title": s["title"],
        "sources": [],
        "fields": s["fields"],
        "full_text": "",
    })
    scholarships[sid]["sources"].append(s["source_pdf"])

# Attach full text blocks for C from ID headers
for f in sorted(base.glob("DATABASE_V3_*.txt")):
    text = f.read_text(encoding="utf-8", errors="replace")
    headers = list(re.finditer(r"(?m)^([^\n]{5,140}?)\s*\(ID:\s*(\d+)\)\s*$", text))
    for i,h in enumerate(headers):
        sid = int(h.group(2))
        end = headers[i+1].start() if i+1 < len(headers) else len(text)
        block = text[h.start():end]
        on = official_name_from_block(block)
        if sid not in scholarships:
            scholarships[sid] = {"id":sid,"title":h.group(1).strip(),"sources":[],"fields":{},"full_text":""}
        if on:
            scholarships[sid]["title"] = on
        scholarships[sid]["full_text"] = block
        scholarships[sid]["sources"].append(f.name)

# Add A/B
for a in a_audits:
    sid = id_map_a.get(a["audit_num"])
    if not sid: continue
    scholarships[sid] = {
        "id": sid,
        "title": title_map_a[a["audit_num"]],
        "sources": [a["pdf"]],
        "fields": {},
        "full_text": a["text"],
    }
for a in b_audits:
    sid = id_map_b.get(a["audit_num"])
    if not sid: continue
    scholarships[sid] = {
        "id": sid,
        "title": title_map_b[a["audit_num"]],
        "sources": [a["pdf"]],
        "fields": {},
        "full_text": a["text"],
    }

print("Total unique scholarships with text:", len(scholarships))
print("IDs:", sorted(scholarships.keys()))

# Save combined corpus
out = pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\export\_scholarship_corpus.json")
# trim full_text for size in summary later; keep full for analysis
slim = []
for sid, s in sorted(scholarships.items()):
    slim.append({"id": sid, "title": s["title"], "sources": list(set(s["sources"])), "text_len": len(s["full_text"])})
print(json.dumps(slim, indent=2)[:5000])
out.write_text(json.dumps({str(k): {"id":v["id"],"title":v["title"],"sources":v["sources"],"full_text":v["full_text"],"fields":v.get("fields",{})} for k,v in scholarships.items()}, ensure_ascii=False), encoding="utf-8")
print("wrote corpus", out, "bytes", out.stat().st_size)
