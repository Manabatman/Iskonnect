import json, pathlib
from collections import Counter
root = pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\reports")
all_cands = []
for p in sorted(root.glob("*/schema_candidates.json")):
    data = json.loads(p.read_text(encoding="utf-8"))
    cat = p.parent.name
    for item in data:
        item = dict(item)
        item["_category"] = cat
        all_cands.append(item)
recs = Counter(i.get("recommendation") for i in all_cands)
print("RECOMMENDATION COUNTS:", dict(recs))
print("TOTAL CANDIDATES:", len(all_cands))
print()
for i, c in enumerate(all_cands, 1):
    rule = (c.get("observed_rule") or "").strip()
    if not rule:
        continue
    print(f"{i}. [{c['_category']}] rec={c.get('recommendation')} workaround={c.get('current_workaround')}")
    print(f"   {rule}")
    print(f"   ids={c.get('example_scholarship_ids')} freq={c.get('frequency_in_bundle')}")
    print()
