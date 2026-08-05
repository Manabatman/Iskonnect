"""
Regenerate persona golden match outputs (MATCH-03 / B2).

Usage:
  python -m app.scripts.regenerate_persona_goldens
  python -m app.scripts.regenerate_persona_goldens --persona maria_freshman_stem

Review the git diff before committing — goldens are a reviewed artifact (R-03).
Does not modify persona_catalog.json; update expected_status / ranking_invariants manually
or via --write-catalog after review.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from app.matching.eligibility_result import evaluate_eligibility
from app.matching.match_service import MatchService

REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = REPO_ROOT / "app" / "tests" / "fixtures" / "persona_catalog.json"
GOLDEN_DIR = REPO_ROOT / "app" / "tests" / "fixtures" / "golden"


def _load_catalog() -> dict:
    with CATALOG_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def _golden_row(result: dict) -> dict:
    return {
        "id": int(result["id"]),
        "title": result.get("title"),
        "qualification_status": result.get("qualification_status"),
        "final_score": float(result.get("final_score") if result.get("final_score") is not None else result.get("score", 0)),
        "deadline_passed": bool(result.get("deadline_passed")),
    }


def _ranked_results(profile: dict, scholarships: list[dict]) -> list[dict]:
    service = MatchService()
    results, _ = service.get_matches(profile, scholarships)
    return results


def _suggest_layers(persona: dict, scholarships: list[dict], ranked: list[dict]) -> dict:
    profile = persona["profile"]
    by_id = {int(r["id"]): r for r in ranked}
    rank_index = {int(r["id"]): idx for idx, r in enumerate(ranked)}

    expected_status: dict[str, str] = {}
    for sid in persona.get("must_include", []):
        row = by_id.get(int(sid))
        if row:
            expected_status[str(sid)] = row.get("qualification_status") or "qualified"

    expected_detail: dict[str, str] = {}
    detail_ids = set(persona.get("must_include", [])) | set(persona.get("must_exclude", []))
    for sid in detail_ids:
        sch = next(s for s in scholarships if s["id"] == sid)
        status = evaluate_eligibility(profile, sch).status.value
        ranked_status = (by_id.get(int(sid)) or {}).get("qualification_status")
        if ranked_status is None or status != ranked_status:
            expected_detail[str(sid)] = status

    invariants: list[dict[str, int]] = []
    includes = [int(sid) for sid in persona.get("must_include", []) if int(sid) in rank_index]
    for i in range(len(includes) - 1):
        above, below = includes[i], includes[i + 1]
        if rank_index[above] < rank_index[below]:
            invariants.append({"above": above, "below": below})

    if len(includes) >= 2 and not invariants:
        above, below = includes[0], includes[1]
        if rank_index[above] < rank_index[below]:
            invariants.append({"above": above, "below": below})

    if not invariants and len(ranked) >= 2:
        # Prefer an invariant that includes a must_include fixture when possible.
        includes_in_results = [int(sid) for sid in persona.get("must_include", []) if int(sid) in rank_index]
        if includes_in_results:
            anchor = includes_in_results[0]
            for other in (int(r["id"]) for r in ranked):
                if other == anchor:
                    continue
                if rank_index[anchor] < rank_index[other]:
                    invariants.append({"above": anchor, "below": other})
                    break
        if not invariants:
            top_a, top_b = int(ranked[0]["id"]), int(ranked[1]["id"])
            invariants.append({"above": top_a, "below": top_b})

    return {
        "expected_status": expected_status,
        "expected_detail_status": expected_detail,
        "ranking_invariants": invariants,
    }


def regenerate_persona(persona: dict, scholarships: list[dict], *, write: bool) -> dict:
    ranked = _ranked_results(persona["profile"], scholarships)
    payload = {
        "persona_id": persona["id"],
        "generated_on": date.today().isoformat(),
        "ordered_results": [_golden_row(r) for r in ranked],
    }
    if write:
        GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
        out_path = GOLDEN_DIR / f"{persona['id']}.json"
        out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    payload["_suggested_layers"] = _suggest_layers(persona, scholarships, ranked)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Regenerate persona golden match files")
    parser.add_argument("--persona", help="Regenerate one persona slug only")
    parser.add_argument(
        "--write-catalog",
        action="store_true",
        help="Merge suggested expected_status/detail/invariants into persona_catalog.json (review first)",
    )
    args = parser.parse_args()

    catalog = _load_catalog()
    scholarships = catalog["scholarships"]
    personas = catalog["personas"]
    if args.persona:
        personas = [p for p in personas if p["id"] == args.persona]
        if not personas:
            raise SystemExit(f"Unknown persona: {args.persona}")

    for persona in personas:
        result = regenerate_persona(persona, scholarships, write=True)
        print(f"Wrote {GOLDEN_DIR / (persona['id'] + '.json')} ({len(result['ordered_results'])} rows)")
        if args.write_catalog:
            persona.update(
                {
                    k: result["_suggested_layers"][k]
                    for k in ("expected_status", "expected_detail_status", "ranking_invariants")
                }
            )

    if args.write_catalog:
        CATALOG_PATH.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Updated {CATALOG_PATH}")


if __name__ == "__main__":
    main()
