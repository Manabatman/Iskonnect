"""
Empirical evaluation runner for the Iskonnect matching engine.

Exercises TWO paths over the same synthetic dataset and compares them against an
independent oracle:
  - CORE: app.matching.match_service.MatchService (dict in / dict out)
  - PROD: app.api.v1.matches._prefilter_scholarships_query (SQL) -> MatchService

Outputs a full metrics report (confusion matrix, recall/precision, breakdowns,
ranking quality, explanation quality, and cause attribution).
"""

from __future__ import annotations

import json
import math
import os
from collections import defaultdict

os.environ.setdefault("RUN_MIGRATIONS_ON_STARTUP", "false")
os.environ.setdefault("DATABASE_URL", "sqlite://")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models
from app.db import Base
from app.matching.match_service import MatchService
from app.api.v1.matches import _prefilter_scholarships_query
from app.api.v1.scholarships import _scholarship_to_response

from eval.generate_data import generate_profiles, generate_scholarships
from eval.oracle import is_eligible

_JSON_LIST_FIELDS = [
    "eligible_levels", "eligible_regions", "eligible_cities", "eligible_school_types",
    "eligible_courses_psced", "eligible_courses_specific", "priority_groups",
    "needs_tags", "required_documents", "preferred_extracurriculars", "preferred_awards",
]


def _income_bracket(inc):
    if inc is None:
        return "unknown"
    if inc <= 250_000:
        return "below_250k"
    if inc <= 400_000:
        return "250k_400k"
    if inc <= 500_000:
        return "400k_500k"
    return "above_500k"


def _build_db(scholarships):
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = Session()
    from datetime import date
    for s in scholarships:
        kwargs = {}
        for k, v in s.items():
            if k.startswith("gt_"):
                continue
            if k in _JSON_LIST_FIELDS:
                kwargs[k] = json.dumps(v) if v is not None else None
            elif k in ("application_deadline", "application_open_date", "last_open_date", "last_close_date"):
                kwargs[k] = date.fromisoformat(v) if isinstance(v, str) else v
            else:
                kwargs[k] = v
        db.add(models.Scholarship(**kwargs))
    db.commit()
    return db


def _engine_eligible_ids_core(svc, profile, scholarships):
    results, _diag = svc.get_matches(profile, scholarships)
    return {r["id"] for r in results}, results


def _engine_eligible_ids_prod(svc, db, profile):
    rows = _prefilter_scholarships_query(db, profile).all()
    dicts = [_scholarship_to_response(r) for r in rows]
    results, _diag = svc.get_matches(profile, dicts)
    return {r["id"] for r in results}, results


def _attribute_fn_cause(profile, sch):
    """Why might the engine have missed an oracle-eligible scholarship? (path-neutral)"""
    from eval.oracle import _bucket
    regions = [r for r in (sch.get("eligible_regions") or []) if r]
    if regions:
        literal = (profile.get("region") or "")
        # alias typed by student that is not a literal substring of any stored region
        if literal and not any(literal.strip().lower() in str(r).strip().lower() for r in regions):
            return "region_normalization_gap"
    levels = [str(x).strip().lower() for x in (sch.get("eligible_levels") or []) if x]
    praw = (profile.get("education_level") or "").strip().lower()
    if levels and praw:
        pbucket = _bucket(praw)
        lbuckets = {_bucket(x) for x in levels}
        if praw not in levels and pbucket in lbuckets:
            # correct bucket matches, but engine normalization (level_map / SQL exact) misses it
            if pbucket == "senior high":
                return "level_seniorhigh_synonym_gap"
            return "level_subtype_exact_gap"
    spec = [c for c in (sch.get("eligible_courses_specific") or []) if c]
    psced = [c for c in (sch.get("eligible_courses_psced") or []) if c]
    if spec and not psced:
        prefs = [str(p).strip().lower() for p in (profile.get("preferred_courses") or []) if p]
        if not prefs:
            return "field_broad_not_bridged_to_specific (hard filter)"
    return "other"


def _attribute_fp_cause(profile, sch):
    """Why might the engine have included an oracle-ineligible scholarship?"""
    if sch.get("members_only"):
        return "priority_exclusive_not_filtered (hard filter gap)"
    psced = [str(c).strip().lower() for c in (sch.get("eligible_courses_psced") or []) if c]
    spec = [str(c).strip().lower() for c in (sch.get("eligible_courses_specific") or []) if c]
    if psced or spec:
        return "field_substring_overmatch (hard filter)"
    levels = [str(x).strip().lower() for x in (sch.get("eligible_levels") or []) if x]
    if levels:
        return "level_overmatch"
    regions = [r for r in (sch.get("eligible_regions") or []) if r]
    if regions:
        return "region_overmatch"
    return "other"


def _ranking_metrics(profile, results, oracle_ids):
    """precision@10, nDCG@20, deadline ordering correctness using engine's active list."""
    active = [r for r in results if not r.get("deadline_passed")]
    rel = [1 if r["id"] in oracle_ids else 0 for r in active]
    p_at_10 = sum(rel[:10]) / min(10, len(rel)) if rel else None

    def dcg(xs):
        return sum(x / math.log2(i + 2) for i, x in enumerate(xs))
    ndcg = None
    if rel:
        ideal = sorted(rel, reverse=True)
        idcg = dcg(ideal[:20])
        ndcg = (dcg(rel[:20]) / idcg) if idcg > 0 else None

    # deadline ordering: every deadline-passed must come after every active
    last_active_idx = max((i for i, r in enumerate(results) if not r.get("deadline_passed")), default=-1)
    first_passed_idx = min((i for i, r in enumerate(results) if r.get("deadline_passed")), default=len(results))
    deadline_ok = first_passed_idx > last_active_idx
    return p_at_10, ndcg, deadline_ok


def _explanation_quality(profile, results, oracle_ids):
    """Coverage (non-empty explanation+breakdown) and coherence (no false claims)."""
    covered = 0
    coherent = 0
    total = 0
    false_claims = 0
    for r in results:
        if r.get("deadline_passed"):
            continue
        total += 1
        expl = r.get("explanation") or []
        bd = r.get("breakdown") or {}
        if expl:
            covered += 1
        # coherence: does it claim region/field match when oracle says ineligible on that axis?
        text = " ".join(expl).lower()
        claim_region = ("region match" in text) or ("lgu/city match" in text) or ("island group match" in text)
        claim_field = ("course/field alignment" in text) or ("partial course alignment" in text)
        bad = False
        if claim_region and r["id"] not in oracle_ids:
            # only count as false if region was the failing axis is hard; approximate: ineligible + claims geo
            bad = True
        if claim_field and r["id"] not in oracle_ids:
            bad = True
        if bad:
            false_claims += 1
        else:
            coherent += 1
    return {
        "rows": total,
        "coverage": covered / total if total else None,
        "coherence": coherent / total if total else None,
        "false_claim_rows": false_claims,
    }


def evaluate(path_name, eligible_fn, profiles, scholarships, results_fn):
    sch_by_id = {s["id"]: s for s in scholarships}
    all_ids = set(sch_by_id)

    TP = FP = FN = TN = 0
    per_student_recall = []
    recall_by = {"region": defaultdict(lambda: [0, 0]), "field": defaultdict(lambda: [0, 0]),
                 "level": defaultdict(lambda: [0, 0]), "income": defaultdict(lambda: [0, 0])}
    fn_causes = defaultdict(int)
    fp_causes = defaultdict(int)
    fn_examples = []
    fp_examples = []
    other_pairs: list[dict] = []
    p10s = []
    ndcgs = []
    deadline_oks = []
    expl_cov = []
    expl_coh = []
    expl_false = 0

    for p in profiles:
        oracle_ids = {sid for sid, s in sch_by_id.items() if is_eligible(p, s)}
        eng_ids, results = results_fn(p)

        tp = len(oracle_ids & eng_ids)
        fn = len(oracle_ids - eng_ids)
        fp = len(eng_ids - oracle_ids)
        tn = len(all_ids) - tp - fn - fp
        TP += tp; FN += fn; FP += fp; TN += tn

        rec = tp / (tp + fn) if (tp + fn) else 1.0
        per_student_recall.append(rec)

        # breakdowns (recall = TP/(TP+FN) aggregated)
        region = p.get("gt_region_canonical", "?")
        field = p.get("field_of_study_broad") or "incomplete"
        from eval.oracle import _bucket
        level = _bucket(p.get("education_level")) or "incomplete"
        income = _income_bracket(p.get("household_income_annual"))
        recall_by["region"][region][0] += tp
        recall_by["region"][region][1] += (tp + fn)
        recall_by["field"][field][0] += tp
        recall_by["field"][field][1] += (tp + fn)
        recall_by["level"][level][0] += tp
        recall_by["level"][level][1] += (tp + fn)
        recall_by["income"][income][0] += tp
        recall_by["income"][income][1] += (tp + fn)

        for sid in (oracle_ids - eng_ids):
            cause = _attribute_fn_cause(p, sch_by_id[sid])
            fn_causes[cause] += 1
            if cause == "other":
                other_pairs.append({
                    "kind": "FN",
                    "profile_id": p["id"],
                    "scholarship_id": sid,
                    "scholarship_title": sch_by_id[sid].get("title"),
                })
            if len(fn_examples) < 12:
                fn_examples.append((p["id"], region, sch_by_id[sid]["title"], cause))
        for sid in (eng_ids - oracle_ids):
            cause = _attribute_fp_cause(p, sch_by_id[sid])
            fp_causes[cause] += 1
            if cause == "other":
                other_pairs.append({
                    "kind": "FP",
                    "profile_id": p["id"],
                    "scholarship_id": sid,
                    "scholarship_title": sch_by_id[sid].get("title"),
                })
            if len(fp_examples) < 12:
                fp_examples.append((p["id"], sch_by_id[sid]["title"], cause))

        p10, ndcg, dok = _ranking_metrics(p, results, oracle_ids)
        if p10 is not None:
            p10s.append(p10)
        if ndcg is not None:
            ndcgs.append(ndcg)
        deadline_oks.append(dok)
        eq = _explanation_quality(p, results, oracle_ids)
        if eq["coverage"] is not None:
            expl_cov.append(eq["coverage"])
        if eq["coherence"] is not None:
            expl_coh.append(eq["coherence"])
        expl_false += eq["false_claim_rows"]

    recall = TP / (TP + FN) if (TP + FN) else 0.0
    precision = TP / (TP + FP) if (TP + FP) else 0.0

    def _ratio_map(d):
        return {k: (v[0] / v[1] if v[1] else None, v[1]) for k, v in sorted(d.items())}

    return {
        "path": path_name,
        "confusion": {"TP": TP, "FP": FP, "FN": FN, "TN": TN},
        "recall": recall,
        "precision": precision,
        "macro_recall": sum(per_student_recall) / len(per_student_recall),
        "recall_by_region": _ratio_map(recall_by["region"]),
        "recall_by_field": _ratio_map(recall_by["field"]),
        "recall_by_level": _ratio_map(recall_by["level"]),
        "recall_by_income": _ratio_map(recall_by["income"]),
        "fn_causes": dict(sorted(fn_causes.items(), key=lambda x: -x[1])),
        "fp_causes": dict(sorted(fp_causes.items(), key=lambda x: -x[1])),
        "fn_examples": fn_examples,
        "fp_examples": fp_examples,
        "precision_at_10": sum(p10s) / len(p10s) if p10s else None,
        "ndcg_at_20": sum(ndcgs) / len(ndcgs) if ndcgs else None,
        "deadline_order_ok_rate": sum(1 for x in deadline_oks if x) / len(deadline_oks),
        "explanation_coverage": sum(expl_cov) / len(expl_cov) if expl_cov else None,
        "explanation_coherence": sum(expl_coh) / len(expl_coh) if expl_coh else None,
        "explanation_false_claim_rows": expl_false,
        "other_pairs": other_pairs,
    }


def _fmt_pct(x):
    return "n/a" if x is None else f"{x*100:.1f}%"


def run_full_evaluation() -> dict:
    """Run CORE + PROD evaluation; return report dict (for pytest regression gate)."""
    profiles = generate_profiles()
    scholarships = generate_scholarships()
    svc = MatchService()
    core = evaluate(
        "CORE",
        is_eligible,
        profiles,
        scholarships,
        lambda p: _engine_eligible_ids_core(svc, p, scholarships),
    )
    db = _build_db(scholarships)
    prod = evaluate(
        "PROD (SQL prefilter)",
        is_eligible,
        profiles,
        scholarships,
        lambda p: _engine_eligible_ids_prod(svc, db, p),
    )
    return {
        "core": core,
        "prod": prod,
        "dataset": {"profiles": len(profiles), "scholarships": len(scholarships)},
    }


def dump_other_causes(report: dict, out_path: str | None = None) -> list[dict]:
    """Collect FN/FP pairs attributed as 'other' for triage."""
    rows: list[dict] = []
    for path_key in ("core", "prod"):
        for item in report.get(path_key, {}).get("other_pairs", []):
            rows.append({"path": path_key, **item})
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2)
    return rows


def main():
    report = run_full_evaluation()
    profiles_n = report["dataset"]["profiles"]
    scholarships_n = report["dataset"]["scholarships"]
    print(f"Dataset: profiles={profiles_n} scholarships={scholarships_n} pairs={profiles_n * scholarships_n}")

    eval_dir = os.path.dirname(__file__)
    with open(os.path.join(eval_dir, "results.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)
    dump_other_causes(report, os.path.join(eval_dir, "other_causes.json"))

    for r in (report["core"], report["prod"]):
        print("\n" + "=" * 78)
        print(f"PATH: {r['path']}")
        c = r["confusion"]
        print(f"  Confusion: TP={c['TP']} FP={c['FP']} FN={c['FN']} TN={c['TN']}")
        print(f"  Recall (micro)={_fmt_pct(r['recall'])}  Precision={_fmt_pct(r['precision'])}  MacroRecall={_fmt_pct(r['macro_recall'])}")
        print(f"  precision@10={_fmt_pct(r['precision_at_10'])}  nDCG@20={_fmt_pct(r['ndcg_at_20'])}  deadline_order_ok={_fmt_pct(r['deadline_order_ok_rate'])}")
        print(f"  explanation coverage={_fmt_pct(r['explanation_coverage'])}  coherence={_fmt_pct(r['explanation_coherence'])}  false_claim_rows={r['explanation_false_claim_rows']}")
        print("  Recall by region:")
        for k, (v, n) in r["recall_by_region"].items():
            print(f"    {k:<32} {_fmt_pct(v):>7}  (eligible pairs={n})")
        print("  Recall by field:")
        for k, (v, n) in r["recall_by_field"].items():
            print(f"    {k:<32} {_fmt_pct(v):>7}  (eligible pairs={n})")
        print("  Recall by level:")
        for k, (v, n) in r["recall_by_level"].items():
            print(f"    {k:<32} {_fmt_pct(v):>7}  (eligible pairs={n})")
        print("  Recall by income bracket:")
        for k, (v, n) in r["recall_by_income"].items():
            print(f"    {k:<32} {_fmt_pct(v):>7}  (eligible pairs={n})")
        print("  FN causes (missed opportunities):")
        for k, v in r["fn_causes"].items():
            print(f"    {v:>5}  {k}")
        print("  FP causes (irrelevant matches):")
        for k, v in r["fp_causes"].items():
            print(f"    {v:>5}  {k}")
        print("  FN examples:")
        for ex in r["fn_examples"][:8]:
            print(f"    profile#{ex[0]} [{ex[1]}] missed '{ex[2]}' -> {ex[3]}")
        print("  FP examples:")
        for ex in r["fp_examples"][:8]:
            print(f"    profile#{ex[0]} got '{ex[1]}' -> {ex[2]}")


if __name__ == "__main__":
    main()
