import fitz, pathlib
base = pathlib.Path(r"c:\Iskonnect\scholarship-match\verification")
nlm = list(base.glob("Production Matching*.pdf"))[0]
doc = fitz.open(nlm)
text = "\n".join(page.get_text() for page in doc)
out = base / "export" / "_extracted_notebooklm.txt"
out.write_text(text, encoding="utf-8")
print(f"pages={doc.page_count} chars={len(text)} -> {out}")
