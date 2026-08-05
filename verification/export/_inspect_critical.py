import pathlib, re, json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
corpus = json.loads(pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\export\_scholarship_corpus.json").read_text(encoding="utf-8"))

# Inspect critical IDs for zero-unit / incoming / exclusivity / rank wording
for sid in ["73","76","10","61","130","54","117","78","7","88","5","66","118","55","124","74","91","31","68"]:
    s = corpus[sid]
    text = s["full_text"]
    print(f"\n===== ID {sid}: {s['title'][:70]} =====")
    # extract eligibility section bullets-ish lines with key words
    keys = ["Incoming", "unit", "GWA", "Rank", "Income", "Age", "School", "Sector", "transferee", "shiftee", "concurrent", "another scholarship", "exclusiv", "NCFRS", "RSBSA", "SRA", "work experience", "Salary Grade", "single", "Top ", "zero", "earned", "OR "]
    for ln in text.splitlines():
        low = ln.lower()
        if any(k.lower() in low for k in keys) and 8 < len(ln.strip()) < 200:
            print(ln.strip()[:190])
