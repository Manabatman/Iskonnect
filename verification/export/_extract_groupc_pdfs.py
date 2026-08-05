#!/usr/bin/env python3
"""Extract structured scholarship sections from Group C verification PDFs."""
from pathlib import Path
import re
import sys

ROOT = Path(r"c:\Iskonnect\scholarship-match\verification")
OUT = ROOT / "export" / "_groupc_extracted_raw.txt"

PDFS = [
    "DATABASE_V3_GROUPC_DOST_GRADUATE.pdf",
    "DATABASE_V3_GROUPC_INTERNATIONAL.pdf",
    "DATABASE_V3_GROUPC_LGU_PART1.pdf",
    "DATABASE_V3_GROUPC_LGU_PART2.pdf",
    "DATABASE_V3_GROUPC_OTHER_GOVERNMENT.pdf",
    "DATABASE_V3_GROUPC_PRIVATE_FOUNDATIONS_P1.pdf",
    "DATABASE_V3_GROUPC_PRIVATE_FOUNDATIONS_P2.pdf",
    "DATABASE_V3_GROUPC_UNIFAST_CHED.pdf",
    "DATABASE_V3_GROUPC_UNNIVERSITIES.pdf",
]

def extract_with_pypdf(path: Path) -> str:
    from pypdf import PdfReader
    reader = PdfReader(str(path))
    parts = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        parts.append(f"\n--- PAGE {i+1} ---\n{text}")
    return "\n".join(parts)

def extract_with_fitz(path: Path) -> str:
    import fitz
    doc = fitz.open(str(path))
    parts = []
    for i, page in enumerate(doc):
        text = page.get_text() or ""
        parts.append(f"\n--- PAGE {i+1} ---\n{text}")
    return "\n".join(parts)

def extract_with_pdfminer(path: Path) -> str:
    from pdfminer.high_level import extract_text
    return extract_text(str(path))

def get_extractor():
    try:
        import pypdf  # noqa
        return extract_with_pypdf, "pypdf"
    except ImportError:
        pass
    try:
        import fitz  # noqa
        return extract_with_fitz, "fitz"
    except ImportError:
        pass
    try:
        import pdfminer  # noqa
        return extract_with_pdfminer, "pdfminer"
    except ImportError:
        pass
    return None, None

def main():
    extractor, name = get_extractor()
    if not extractor:
        print("NO_PDF_LIB", file=sys.stderr)
        # try pip install
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf", "-q"])
        extractor, name = get_extractor()
        if not extractor:
            sys.exit("Failed to install PDF library")
    print(f"Using extractor: {name}")
    out_chunks = []
    for pdf_name in PDFS:
        path = ROOT / pdf_name
        print(f"Extracting {pdf_name}...")
        text = extractor(path)
        # Find scholarship headers
        headers = re.findall(
            r"(?:Official Name:|^\d+\.\s+Scholarship Identity|\(ID:\s*\d+\)|ID:\s*\d+)",
            text,
            flags=re.M,
        )
        print(f"  chars={len(text)} header-ish matches={len(headers)}")
        out_chunks.append(f"\n\n{'='*80}\nSOURCE PDF: {pdf_name}\n{'='*80}\n")
        out_chunks.append(text)
    OUT.write_text("".join(out_chunks), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
