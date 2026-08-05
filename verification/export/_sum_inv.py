import json
from collections import Counter
inv = json.loads(open(r"c:\Iskonnect\scholarship-match\verification\export\_rule_class_inventory_v2.json", encoding="utf-8").read())
cur = Counter(o["current_schema_supported"] for o in inv.values())
prop = Counter(o["proposed_architecture_supported"] for o in inv.values())
impl = Counter()
for o in inv.values():
    for part in o["implementation_needs"].replace("+", " ").split():
        impl[part] += 1
print("current", dict(cur))
print("proposed", dict(prop))
print("impl token freq", dict(impl))
# classes needing new atomic
for k,o in inv.items():
    if o["current_schema_supported"] == "no" and o["proposed_architecture_supported"] == "yes":
        print("GAP->COVERED", k, o["count"], o["label"], o["implementation_needs"])
