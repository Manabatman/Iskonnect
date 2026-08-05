import fitz, pathlib, re
base = pathlib.Path(r"c:\Iskonnect\scholarship-match\verification")
out_dir = base / "export" / "_pdf_extracts"
out_dir.mkdir(exist_ok=True)
summaries = []
for pdf in sorted(base.glob("DATABASE_*.pdf")):
    doc = fitz.open(pdf)
    text = "\n".join(page.get_text() for page in doc)
    out = out_dir / (pdf.stem + ".txt")
    out.write_text(text, encoding="utf-8")
    # Extract headings / schema-ish keywords
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    keywords = ["incoming", "year", "renewal", "OR ", "AND ", "schema", "gap", "eligibility", "compound", "sector", "track", "mutual", "concurrent", "return service", "Listahanan", "4Ps", "affiliation", "graduating", "freshman", "transferee"]
    hits = []
    for ln in lines:
        low = ln.lower()
        if any(k.lower() in low for k in keywords) and len(ln) < 220:
            hits.append(ln)
    summaries.append((pdf.name, doc.page_count, len(text), hits[:40]))
    print(f"OK {pdf.name} pages={doc.page_count} chars={len(text)} keyword_hits={len(hits)}")

# Write a keyword digest
digest = []
for name, pages, chars, hits in summaries:
    digest.append(f"\n===== {name} ({pages}p, {chars}c) =====\n")
    digest.extend(hits)
(out_dir / "_keyword_digest.txt").write_text("\n".join(digest), encoding="utf-8")
print("digest written")
