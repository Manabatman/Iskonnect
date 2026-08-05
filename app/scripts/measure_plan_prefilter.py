"""
Measure match-plan latency: full catalog scan vs SQL prefilter path (B13 / ADR-007).

Usage:
  python -m app.scripts.measure_plan_prefilter --iterations 20
  python -m app.scripts.measure_plan_prefilter --output docs/engineering/reports/b13-plan-prefilter-bench.json
"""

from __future__ import annotations

import argparse
import json
import statistics
import time
from pathlib import Path

from app.api.v1.matches import _prefilter_scholarships_query, _scholarship_rows_to_dicts
from app.api.v1.scholarships import get_cached_scholarship_dicts, _build_all_scholarship_dicts
from app.db import SessionLocal
from app.matching.match_service import MatchService
from app.scholarship_cache import invalidate_scholarship_cache
from app.utils.data_completeness import is_publishable

SAMPLE_PROFILE = {
    "education_level": "College",
    "region": "National Capital Region",
    "school_type": "Public",
    "household_income_annual": 250000,
    "gwa_normalized": 85,
    "field_of_study_broad": "STEM",
    "preferred_courses": ["BS Computer Science"],
}


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = max(0, int(len(ordered) * 0.95) - 1)
    return ordered[idx]


def _run_match_ms(scholarship_dicts: list[dict], iterations: int) -> list[float]:
    svc = MatchService()
    timings: list[float] = []
    for _ in range(iterations):
        start = time.perf_counter()
        svc.get_matches(SAMPLE_PROFILE, scholarship_dicts)
        timings.append((time.perf_counter() - start) * 1000)
    return timings


def measure(*, iterations: int = 20) -> dict:
    invalidate_scholarship_cache()
    db = SessionLocal()
    try:
        full_dicts = get_cached_scholarship_dicts(db)
        all_active = _build_all_scholarship_dicts(db, publishable_only=False)
        prefiltered_rows = _prefilter_scholarships_query(db, SAMPLE_PROFILE).all()
        prefiltered_dicts = [d for d in _scholarship_rows_to_dicts(prefiltered_rows) if is_publishable(d)]

        full_ms = _run_match_ms(full_dicts, iterations)
        prefilter_ms = _run_match_ms(prefiltered_dicts, iterations)
        all_active_ms = _run_match_ms(all_active, iterations)

        return {
            "iterations": iterations,
            "catalog_active_count": len(all_active),
            "catalog_publishable_count": len(full_dicts),
            "prefilter_candidate_count": len(prefiltered_dicts),
            "full_scan_ms": {
                "p50": round(statistics.median(full_ms), 2),
                "p95": round(_p95(full_ms), 2),
                "min": round(min(full_ms), 2),
                "max": round(max(full_ms), 2),
            },
            "prefilter_ms": {
                "p50": round(statistics.median(prefilter_ms), 2),
                "p95": round(_p95(prefilter_ms), 2),
                "min": round(min(prefilter_ms), 2),
                "max": round(max(prefilter_ms), 2),
            },
            "all_active_scan_ms": {
                "p50": round(statistics.median(all_active_ms), 2),
                "p95": round(_p95(all_active_ms), 2),
            },
            "profile": SAMPLE_PROFILE,
        }
    finally:
        db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark plan match path with/without SQL prefilter")
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--output", default=None, help="Write JSON results to path")
    args = parser.parse_args()

    result = measure(iterations=args.iterations)
    payload = json.dumps(result, indent=2)
    print(payload)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload, encoding="utf-8")


if __name__ == "__main__":
    main()
