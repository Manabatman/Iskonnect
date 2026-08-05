import pathlib, re
digest = pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\export\_pdf_extracts\_keyword_digest.txt").read_text(encoding="utf-8")
# Pull cross-cutting rule phrases
patterns = [
    r"zero.?unit",
    r"incoming",
    r"no earned",
    r"class rank|top\s*\d|top\s*5|top\s*10",
    r"exclusiv|cannot hold|not a beneficiary|concurrent|dual.?grant|one.?grant|another scholarship",
    r"NCFRS|RSBSA|SRA|Listahanan|4Ps",
    r"return service",
    r"work experience|years of",
    r"consortium|partner (school|university|HEI)",
    r"one scholar per family|one.?per.?family",
    r"marital|single status|must be single",
    r"salary grade|SG-\d|SG \d",
    r"lateral|transferee|shiftee",
    r"renewal|maintain",
]
text_low = digest.lower()
for p in patterns:
    hits = re.findall(p, digest, flags=re.I)
    print(f"{p}: {len(hits)} hits")

# Sample unique lines containing key abstractions
keys = ["zero", "Top ", "exclusiv", "NCFRS", "RSBSA", "work experience", "consortium", "per family", "Salary Grade", "transferee", "incoming", "earned unit", "OR "]
print("\n=== SAMPLE LINES ===")
for ln in digest.splitlines():
    if any(k.lower() in ln.lower() for k in keys) and 40 < len(ln) < 200:
        print(ln[:190])
