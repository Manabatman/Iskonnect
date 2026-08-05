import pathlib, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\export\_pdf_extracts")
# Search full extracts for key rule abstractions
needles = [
    "zero", "0 earned", "earned unit", "no college unit", "incoming",
    "Top 5", "Top 10", "class rank", "rank in class",
    "another scholarship", "cannot avail", "not a beneficiary", "concurrent",
    "NCFRS", "RSBSA", "SRA", "Listahanan", "4Ps",
    "one scholar", "per family", "household",
    "work experience", "years of work",
    "consortium", "partner university", "member university",
    "salary grade", "SG-",
    "must be single", "marital",
    "transferee", "shiftee", "lateral",
    "return service",
]
for txt in sorted(base.glob("DATABASE_*.txt")):
    content = txt.read_text(encoding="utf-8", errors="replace")
    print(f"\n##### {txt.name} #####")
    for n in needles:
        # count case insensitive
        c = len(re.findall(re.escape(n), content, flags=re.I))
        if c:
            print(f"  {n}: {c}")
