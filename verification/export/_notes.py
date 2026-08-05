import json, pathlib
root = pathlib.Path(r"c:\Iskonnect\scholarship-match\verification\reports")
for p in sorted(root.glob("*/important_notes.json")):
    data = json.loads(p.read_text(encoding="utf-8"))
    print(f"\n===== {p.parent.name} ({len(data) if isinstance(data,list) else 'obj'}) =====")
    if isinstance(data, list):
        for n in data[:15]:
            if isinstance(n, dict):
                print("-", (n.get("note") or n.get("text") or n.get("important_note") or str(n))[:300])
            else:
                print("-", str(n)[:300])
    else:
        print(str(data)[:800])
