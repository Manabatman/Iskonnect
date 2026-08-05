import pathlib, re, json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\export\_pdf_extracts")
files = sorted(base.glob("DATABASE_*.txt"))
print("files", len(files))
for f in files:
    t = f.read_text(encoding="utf-8", errors="replace")
    print(f"\n===== {f.name} len={len(t)} =====")
    # print structure: headings looking like Scholarship / ID / Record
    for m in re.finditer(r"(?m)^(?:Scholarship|Program|Record|ID|Database ID|Canonical|Title|Official Name).{0,120}$", t):
        pass
    # Find ID patterns
    ids = re.findall(r"(?:ID|id|Scholarship ID|Record ID|Database ID)\s*[:#]?\s*(\d{1,3})\b", t)
    print("id mentions sample", ids[:30], "count", len(ids))
    # First 2500 chars to see structure
    print(t[:2500])
