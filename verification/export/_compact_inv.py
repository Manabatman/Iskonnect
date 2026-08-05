import json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
corpus = json.loads(open(r"c:\Iskonnect\scholarship-match\verification\export\_scholarship_corpus.json", encoding="utf-8").read())
inv = json.loads(open(r"c:\Iskonnect\scholarship-match\verification\export\_rule_class_inventory_v2.json", encoding="utf-8").read())

for sid in ["55","124","27","28","29","95","85","86","87","118","100"]:
    t = corpus[sid]["full_text"]
    print(f"\nID {sid} {corpus[sid]['title'][:60]}")
    for pat in ["RSBSA","NCFRS","SRA","exclusiv","another scholarship","concurrent","single marital","fisherfolk","LGU"]:
        if re.search(pat, t, re.I):
            m = re.search(r".{0,60}"+pat+r".{0,80}", t, re.I)
            print(" ", pat, "=>", (m.group(0).replace("\n"," ") if m else "")[:140])

# Print compact inventory for plan embedding: small classes full list, large classes id-only
print("\n\n=== COMPACT FOR PLAN ===")
for key, o in inv.items():
    ids = o["scholarship_ids"]
    if o["count"] <= 15:
        titles = "; ".join(f"{s['id']} {s['title'][:40]}" for s in o["scholarships"])
        print(f"\n{key} ({o['count']}) [{o['current_schema_supported']}->{o['proposed_architecture_supported']}] {o['implementation_needs']}")
        print(f"  {o['label']}")
        print(f"  {titles}")
    else:
        print(f"\n{key} ({o['count']}) [{o['current_schema_supported']}->{o['proposed_architecture_supported']}] {o['implementation_needs']}")
        print(f"  {o['label']}")
        print(f"  ids: {ids}")
