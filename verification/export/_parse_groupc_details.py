#!/usr/bin/env python3
"""Parse Group C extracted PDF text into structured scholarship detail blocks."""
from pathlib import Path
import re
import json

RAW = Path(r"c:\Iskonnect\scholarship-match\verification\export\_groupc_extracted_raw.txt")
OUT_MD = Path(r"c:\Iskonnect\scholarship-match\verification\export\_GROUPC_IMPLEMENTATION_DETAILS.md")
OUT_JSON = Path(r"c:\Iskonnect\scholarship-match\verification\export\_GROUPC_IMPLEMENTATION_DETAILS.json")

SECTION_KEYS = [
    "1. Scholarship Identity",
    "2. Purpose",
    "3. Official Eligibility Requirements",
    "4. Application Timing",
    "5. Application Window",
    "6. Benefits",
    "7. Required Documents",
    "8. Renewal Requirements",
    "9. Disqualifying Conditions",
    "10. Temporal Eligibility Matrix",
    "11. Structured Eligibility Matrix",
    "12. Production Database Mapping",
    "13. Matching Risks",
    "14. Verification Summary",
]

# Capture through next bullet/section; do NOT use `$` with re.M (end-of-line).
BULLET_END = r"(?=\n\s*[●•]|\n\d+\.\s+[A-Z]|\n--- PAGE|\Z)"
FIELD_PATTERNS = {
    "official_name": rf"Official Name:\s*(.+?){BULLET_END}",
    "provider": rf"Provider:\s*(.+?){BULLET_END}",
    "category": rf"Category:\s*(.+?){BULLET_END}",
    "website": rf"Official Website:\s*(.+?){BULLET_END}",
    "portal": rf"Application Portal:\s*(.+?){BULLET_END}",
    "guidelines": rf"Official Guidelines:\s*(.+?){BULLET_END}",
    "status": rf"Current Status:\s*(.+?){BULLET_END}",
    "citizenship": rf"Citizenship:\s*(.+?){BULLET_END}",
    "residency": rf"Residency:\s*(.+?){BULLET_END}",
    "education_level": rf"Education Level:\s*(.+?){BULLET_END}",
    "eligible_year_levels": rf"Eligible Year Levels:\s*(.+?){BULLET_END}",
    "incoming_freshman_only": rf"Incoming Freshman Only\?:\s*(.+?){BULLET_END}",
    "existing_college": rf"Existing College Students\?:\s*(.+?){BULLET_END}",
    "graduate_students": rf"Graduate Students\?:\s*(.+?){BULLET_END}",
    "current_enrollment": rf"Current Enrollment Requirement:\s*(.+?){BULLET_END}",
    "academic_requirements": rf"Academic Requirements:\s*(.+?){BULLET_END}",
    "minimum_gwa": rf"Minimum GWA:\s*(.+?){BULLET_END}",
    "alt_class_rank": rf"Alternative Class Rank:\s*(.+?){BULLET_END}",
    "income_ceilings": rf"Income Ceilings:\s*(.+?){BULLET_END}",
    "age_restrictions": rf"Age Restrictions:\s*(.+?){BULLET_END}",
    "school_restrictions": rf"School Restrictions:\s*(.+?){BULLET_END}",
    "priority_courses": rf"Priority Courses:\s*(.+?){BULLET_END}",
    "sectoral": rf"Sectoral Requirements:\s*(.+?){BULLET_END}",
    "good_moral": rf"Good Moral:\s*(.+?){BULLET_END}",
    "health": rf"Health Requirements:\s*(.+?){BULLET_END}",
    "other_rules": rf"Other Official Rules:\s*(.+?){BULLET_END}",
    "work_experience": rf"Work Experience:\s*(.+?){BULLET_END}",
    "who_may_apply": rf"Who May Apply:\s*(.+?){BULLET_END}",
    "opening_date": rf"Opening Date:\s*(.+?){BULLET_END}",
    "closing_date": rf"Closing Date:\s*(.+?){BULLET_END}",
    "application_cycle": rf"Application Cycle:\s*(.+?){BULLET_END}",
    "ay_covered": rf"Current AY Covered:\s*(.+?){BULLET_END}",
    "tuition": rf"Tuition:\s*(.+?){BULLET_END}",
    "monthly_stipend": rf"Monthly Stipend:\s*(.+?){BULLET_END}",
    "allowance": rf"(?:^|\n)\s*[●•]?\s*Allowance:\s*(.+?){BULLET_END}",
    "return_service": rf"Return Service:\s*(.+?){BULLET_END}",
    "renewal_gwa": rf"Maintain GWA:\s*(.+?){BULLET_END}",
    "regular_load": rf"Regular Load:\s*(.+?){BULLET_END}",
    "no_failures": rf"No Failures:\s*(.+?){BULLET_END}",
    "matching_risks": r"13\. Matching Risks\s*(.+?)(?:\n14\. Verification Summary|$)",
    "verification_status": r"Verification Status:\s*(.+?)(?:\n|$)",
    "confidence": r"Overall Confidence Score:\s*(.+?)(?:\n|$)",
    "db_mapping_json": r"(?:12\.\s*)?Production Database Mapping\s*(?:JSON\s*)?(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})",
}


def split_by_source(raw: str):
    parts = re.split(r"={80}\nSOURCE PDF: (.+?)\n={80}\n", raw)
    # parts[0] is preamble, then pairs of (name, content)
    sources = []
    i = 1
    while i < len(parts):
        sources.append((parts[i], parts[i + 1]))
        i += 2
    return sources


def find_scholarships(text: str):
    """Split text into scholarship blocks by '(ID: N)' headers.

    Prefer markers that are followed (within ~800 chars) by '1. Scholarship Identity'
    so we skip incidental ID mentions in tables/DDL. If that yields nothing, fall back
    to all (ID: N) occurrences that look like headers.
    """
    all_id_markers = list(re.finditer(
        r"(?P<title>(?:[^\n]+\n){0,4}[^\n]{2,160}?)\s*\(ID:\s*(?P<id>\d+)\)",
        text,
    ))
    markers = []
    seen_ids = set()
    for m in all_id_markers:
        sid = int(m.group("id"))
        window = text[m.end(): m.end() + 900]
        # Skip systemic/DDL mentions that aren't scholarship identity sections
        if "1. Scholarship Identity" not in window and "Scholarship Identity" not in window:
            # still accept if Official Name appears soon (some PDFs omit numbering)
            if "Official Name:" not in window[:500]:
                continue
        if sid in seen_ids:
            # keep first occurrence as the canonical block start
            continue
        seen_ids.add(sid)
        markers.append(m)

    scholarships = []
    for idx, m in enumerate(markers):
        start = m.start()
        end = markers[idx + 1].start() if idx + 1 < len(markers) else len(text)
        # Don't bleed into migration/architecture appendices of other programs:
        # cut at next clear scholarship identity if present earlier
        block = text[start:end]
        title = re.sub(r"\s+", " ", m.group("title")).strip(" -•●")
        title = re.sub(r"--- PAGE \d+ ---", "", title).strip()
        # Prefer last line-ish as title
        if len(title) > 120:
            title = title[-120:].lstrip(" -–—|")
        scholarships.append({
            "id": int(m.group("id")),
            "title_header": title,
            "raw_block": block,
        })
    return scholarships


def extract_fields(block: str) -> dict:
    # Remove page markers and zero-width / artifact chars before field capture.
    block = re.sub(r"\n?--- PAGE \d+ ---\n?", "\n", block)
    block = re.sub(
        r"\[span_?\s*\d+\]\s*\(\s*start_?\s*span\s*\)\s*\[span_?\s*\d+\]\s*\(\s*end_?\s*span\s*\)",
        "",
        block,
        flags=re.I,
    )
    block = re.sub(r"\[span_[^\]]*\]\([^)]*\)", "", block)  # residual span tokens
    block = block.replace("\u200b", "").replace("\ufeff", "")
    out = {}
    for key, pat in FIELD_PATTERNS.items():
        m = re.search(pat, block, flags=re.I | re.M | re.S)
        if m:
            val = m.group(1).strip()
            val = re.sub(r"\s+", " ", val).strip()
            out[key] = val
    # Disqualifying conditions as bullet list
    dm = re.search(
        r"9\. Disqualifying Conditions\s*(.+?)(?:\n10\. Temporal|\n11\. Structured|$)",
        block,
        flags=re.S,
    )
    if dm:
        bullets = re.findall(r"[●•\-]\s*(.+?)(?=\n[●•\-]|\n\d+\.|\n---|\Z)", dm.group(1), flags=re.S)
        if not bullets:
            bullets = [ln.strip(" ●•-\t") for ln in dm.group(1).splitlines() if ln.strip() and not ln.strip().startswith("--")]
        out["disqualifying_conditions"] = [re.sub(r"\s+", " ", b).strip() for b in bullets if b.strip()][:20]

    # Required documents
    docs_m = re.search(
        r"7\. Required Documents\s*(.+?)(?:\n8\. Renewal|\n9\. Disqualifying|$)",
        block,
        flags=re.S,
    )
    if docs_m:
        docs = re.findall(r"\d+\.\s*(.+?)(?=\n\d+\.|\n8\.|\n---|\Z)", docs_m.group(1), flags=re.S)
        out["required_documents"] = [re.sub(r"\s+", " ", d).strip() for d in docs if d.strip()][:25]

    # Timing yes/no fields
    for label, key in [
        ("Can current freshmen apply?", "can_freshmen"),
        ("Can current sophomores apply?", "can_sophomores"),
        ("Can current juniors apply?", "can_juniors"),
        ("Can current seniors apply?", "can_seniors"),
        ("Can graduates apply?", "can_graduates"),
        ("Can previous applicants reapply?", "can_reapply"),
    ]:
        m = re.search(re.escape(label) + r"\s*(.+?)(?:\n|$)", block)
        if m:
            out[key] = re.sub(r"\s+", " ", m.group(1)).strip()

    # Clean JSON mapping if present
    if "db_mapping_json" not in out:
        jm = re.search(
            r"Production Database Mapping[\s\S]{0,200}?(\{\s*\"education_level\"[\s\S]*?\n\})",
            block,
            flags=re.I,
        )
        if jm:
            out["db_mapping_json"] = jm.group(1)

    if "db_mapping_json" in out:
        j = out["db_mapping_json"]
        j = re.sub(
            r"\[span_?\s*\d+\]\s*\(\s*start_?\s*span\s*\)\s*\[span_?\s*\d+\]\s*\(\s*end_?\s*span\s*\)",
            "",
            j,
            flags=re.I,
        )
        j = re.sub(r"\[span_[^\]]*\]\([^)]*\)", "", j)
        j = re.sub(r"\s+", " ", j).strip()
        # Repair identifiers split by removed span artifacts
        j = re.sub(r"([A-Za-z0-9])\s+(_[A-Za-z])", r"\1\2", j)  # year _only
        j = re.sub(r"([A-Z])\s+([A-Z_])", r"\1\2", j)  # ELECTRIC AL_ / EDU CATION
        out["db_mapping_json"] = j
        try:
            out["db_mapping"] = json.loads(j)
        except Exception:
            try:
                fixed = j.replace("t rue", "true").replace("fal se", "false")
                out["db_mapping"] = json.loads(fixed)
                out["db_mapping_json"] = fixed
            except Exception:
                out["db_mapping"] = None

    return out


def to_markdown(sources_data: list) -> str:
    lines = [
        "# Group C Verification PDFs — Implementation Details Extraction",
        "",
        "Exhaustive hard-rule extraction for matching/catalog implications. Structured by source PDF then by scholarship.",
        "",
    ]
    for src, scholarships in sources_data:
        lines.append(f"## SOURCE: `{src}`")
        lines.append("")
        lines.append(f"**Scholarships in this PDF:** {len(scholarships)}")
        lines.append("")
        for s in scholarships:
            f = s["fields"]
            name = f.get("official_name") or s["title_header"]
            lines.append(f"### {name} (ID: {s['id']})")
            lines.append("")
            lines.append("#### Identity / Affiliations")
            lines.append(f"- **Provider:** {f.get('provider', 'NOT EXTRACTED')}")
            lines.append(f"- **Category:** {f.get('category', 'NOT EXTRACTED')}")
            lines.append(f"- **Website:** {f.get('website', 'NOT EXTRACTED')}")
            lines.append(f"- **Portal:** {f.get('portal', 'NOT EXTRACTED')}")
            lines.append(f"- **Guidelines:** {f.get('guidelines', 'NOT EXTRACTED')}")
            lines.append(f"- **Status:** {f.get('status', 'NOT EXTRACTED')}")
            lines.append("")
            lines.append("#### Hard Eligibility Rules")
            for k, label in [
                ("citizenship", "Citizenship"),
                ("residency", "Residency / Destination"),
                ("education_level", "Education Level"),
                ("eligible_year_levels", "Eligible Year Levels"),
                ("incoming_freshman_only", "Incoming Freshman Only"),
                ("existing_college", "Existing College Students"),
                ("graduate_students", "Graduate Students"),
                ("current_enrollment", "Current Enrollment"),
                ("academic_requirements", "Academic Requirements"),
                ("minimum_gwa", "Minimum GWA"),
                ("alt_class_rank", "Alt Class Rank"),
                ("income_ceilings", "Income Ceilings"),
                ("age_restrictions", "Age Restrictions"),
                ("school_restrictions", "School / Consortium Restrictions"),
                ("priority_courses", "Course Restrictions"),
                ("sectoral", "Sectoral / Hidden Requirements"),
                ("work_experience", "Work Experience"),
                ("good_moral", "Good Moral"),
                ("health", "Health"),
                ("other_rules", "Other Official Rules / Conflicts"),
            ]:
                if k in f:
                    lines.append(f"- **{label}:** {f[k]}")
            lines.append("")
            lines.append("#### Timing")
            for k, label in [
                ("who_may_apply", "Who May Apply"),
                ("can_freshmen", "Freshmen"),
                ("can_sophomores", "Sophomores"),
                ("can_juniors", "Juniors"),
                ("can_seniors", "Seniors"),
                ("can_graduates", "Graduates"),
                ("can_reapply", "Reapply"),
                ("opening_date", "Opening"),
                ("closing_date", "Closing"),
                ("application_cycle", "Cycle"),
                ("ay_covered", "AY Covered"),
            ]:
                if k in f:
                    lines.append(f"- **{label}:** {f[k]}")
            lines.append("")
            lines.append("#### Benefits (catalog)")
            for k, label in [
                ("tuition", "Tuition"),
                ("monthly_stipend", "Monthly Stipend"),
                ("allowance", "Allowance"),
                ("return_service", "Return Service"),
            ]:
                if k in f:
                    lines.append(f"- **{label}:** {f[k]}")
            lines.append("")
            lines.append("#### Renewal")
            for k, label in [
                ("renewal_gwa", "Maintain GWA"),
                ("regular_load", "Regular Load"),
                ("no_failures", "No Failures"),
            ]:
                if k in f:
                    lines.append(f"- **{label}:** {f[k]}")
            lines.append("")
            if f.get("disqualifying_conditions"):
                lines.append("#### Disqualifying / Conflicts")
                for d in f["disqualifying_conditions"]:
                    lines.append(f"- {d}")
                lines.append("")
            if f.get("required_documents"):
                lines.append("#### Required Documents (hidden operational requirements)")
                for d in f["required_documents"]:
                    lines.append(f"- {d}")
                lines.append("")
            lines.append("#### Recommended Schema / Fields")
            if f.get("db_mapping_json"):
                lines.append("```json")
                lines.append(f["db_mapping_json"])
                lines.append("```")
            else:
                lines.append("_No Production Database Mapping JSON extracted._")
            lines.append("")
            lines.append("#### FP/FN Risks & Contradictions")
            lines.append(f"- **Matching Risks:** {f.get('matching_risks', 'NOT EXTRACTED')}")
            lines.append(f"- **Verification:** {f.get('verification_status', 'n/a')} | Confidence: {f.get('confidence', 'n/a')}")
            # Highlight contradictions between entry GWA and renewal GWA, income, etc.
            contradictions = []
            if f.get("minimum_gwa") and f.get("renewal_gwa"):
                if f["minimum_gwa"] != f["renewal_gwa"]:
                    contradictions.append(
                        f"Entry min_gwa ({f['minimum_gwa']}) differs from renewal Maintain GWA ({f['renewal_gwa']})"
                    )
            if "NOT SPECIFIED" in str(f.get("minimum_gwa", "")) and "live" in str(f.get("minimum_gwa", "")).lower():
                contradictions.append(f"Live DB GWA vs official NOT SPECIFIED: {f['minimum_gwa']}")
            if contradictions:
                lines.append("- **Contradictions:**")
                for c in contradictions:
                    lines.append(f"  - {c}")
            lines.append("")
            lines.append("---")
            lines.append("")
    return "\n".join(lines)


def main():
    raw = RAW.read_text(encoding="utf-8")
    sources = split_by_source(raw)
    sources_data = []
    all_json = []
    for src, text in sources:
        scholarships = find_scholarships(text)
        enriched = []
        for s in scholarships:
            fields = extract_fields(s["raw_block"])
            s["fields"] = fields
            enriched.append(s)
            all_json.append({
                "source_pdf": src,
                "id": s["id"],
                "title_header": s["title_header"],
                **{k: v for k, v in fields.items() if k != "raw_block"},
            })
        sources_data.append((src, enriched))
        print(f"{src}: {len(enriched)} scholarships -> IDs {[x['id'] for x in enriched]}")

    md = to_markdown(sources_data)
    OUT_MD.write_text(md, encoding="utf-8")
    OUT_JSON.write_text(json.dumps(all_json, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT_MD} ({OUT_MD.stat().st_size} bytes)")
    print(f"Wrote {OUT_JSON} ({OUT_JSON.stat().st_size} bytes)")
    print(f"Total scholarships: {len(all_json)}")

if __name__ == "__main__":
    main()
