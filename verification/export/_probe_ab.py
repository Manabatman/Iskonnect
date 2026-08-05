import pathlib, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
base = pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\export\_pdf_extracts")
for name in ["DATABASE_V1_GROUPA.txt", "DATABASE_V2_GROUPB.txt"]:
    t = base.joinpath(name).read_text(encoding="utf-8", errors="replace")
    print(f"\n######## {name} ########")
    # find ID patterns
    for m in re.finditer(r".{0,80}ID.{0,40}\d{1,3}.{0,80}", t):
        s = m.group(0).replace("\n"," ")
        if re.search(r"\bID\b", s):
            print(s[:160])
    print("--- TOC / section headers ---")
    for m in re.finditer(r"(?m)^(?:[0-9]+\.|Part |Section |Chapter |SCHOLARSHIP|Program |Canonical).{0,100}$", t):
        if len(m.group(0)) < 120:
            print(m.group(0)[:120])
