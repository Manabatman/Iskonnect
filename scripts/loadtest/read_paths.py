"""
Read-path load test for ISKONNECT public beta validation.

Simulates concurrent users hitting health, search, list, and detail endpoints.
Run against a warmed Render instance (hit /health first).

Usage:
  python scripts/loadtest/read_paths.py --base-url https://your-api.onrender.com
  python scripts/loadtest/read_paths.py --base-url https://your-api.onrender.com --users 30 50 100
  python scripts/loadtest/read_paths.py --base-url http://127.0.0.1:8000 --users 10
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


DEFAULT_USERS = (30, 50, 100)
THINK_TIME_SEC = 1.5


@dataclass
class RequestSample:
    path: str
    status: int | None
    latency_ms: float
    error: str | None = None


@dataclass
class RampResult:
    virtual_users: int
    total_requests: int
    errors: int
    error_rate_pct: float
    avg_ms: float
    p95_ms: float
    samples: list[RequestSample] = field(default_factory=list)


def _fetch(base_url: str, path: str, timeout: float = 30.0) -> RequestSample:
    url = base_url.rstrip("/") + path
    started = time.perf_counter()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Iskonnect-LoadTest/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = int(getattr(resp, "status", resp.getcode()))
            latency_ms = (time.perf_counter() - started) * 1000
            return RequestSample(path=path, status=status, latency_ms=latency_ms)
    except urllib.error.HTTPError as e:
        latency_ms = (time.perf_counter() - started) * 1000
        return RequestSample(path=path, status=e.code, latency_ms=latency_ms, error=str(e))
    except Exception as e:
        latency_ms = (time.perf_counter() - started) * 1000
        return RequestSample(path=path, status=None, latency_ms=latency_ms, error=str(e))


def _user_session(base_url: int | str, scholarship_ids: list[int]) -> list[RequestSample]:
    """One virtual user session: warm paths with think time."""
    base = str(base_url)
    paths = [
        "/health",
        "/api/v1/scholarships/search?q=ched&limit=20",
        "/api/v1/scholarships?limit=25",
    ]
    if scholarship_ids:
        sid = scholarship_ids[0]
        paths.append(f"/api/v1/scholarships/{sid}")

    out: list[RequestSample] = []
    for path in paths:
        out.append(_fetch(base, path))
        time.sleep(THINK_TIME_SEC)
    return out


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = max(0, int(len(ordered) * 0.95) - 1)
    return ordered[idx]


def run_ramp(base_url: str, virtual_users: int, scholarship_ids: list[int]) -> RampResult:
    # Warm instance before measuring.
    _fetch(base_url, "/health")

    samples: list[RequestSample] = []
    with ThreadPoolExecutor(max_workers=virtual_users) as pool:
        futures = [pool.submit(_user_session, base_url, scholarship_ids) for _ in range(virtual_users)]
        for fut in as_completed(futures):
            samples.extend(fut.result())

    latencies = [s.latency_ms for s in samples]
    errors = sum(1 for s in samples if s.status is None or s.status >= 400)
    total = len(samples)
    return RampResult(
        virtual_users=virtual_users,
        total_requests=total,
        errors=errors,
        error_rate_pct=round(100.0 * errors / total, 2) if total else 0.0,
        avg_ms=round(statistics.mean(latencies), 1) if latencies else 0.0,
        p95_ms=round(_p95(latencies), 1),
        samples=samples,
    )


def _discover_scholarship_ids(base_url: str, limit: int = 5) -> list[int]:
    sample = _fetch(base_url, f"/api/v1/scholarships?limit={limit}")
    if sample.status != 200:
        return []
    try:
        url = base_url.rstrip("/") + f"/api/v1/scholarships?limit={limit}"
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        items = data if isinstance(data, list) else data.get("results") or data.get("items") or []
        return [int(x["id"]) for x in items if isinstance(x, dict) and x.get("id")]
    except Exception:
        return []


def main() -> None:
    parser = argparse.ArgumentParser(description="ISKONNECT read-path load test")
    parser.add_argument("--base-url", required=True, help="API base URL (no trailing slash)")
    parser.add_argument("--users", nargs="+", type=int, default=list(DEFAULT_USERS))
    parser.add_argument("--report", default="scripts/loadtest/results.json")
    args = parser.parse_args()

    scholarship_ids = _discover_scholarship_ids(args.base_url)
    payload: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base_url": args.base_url,
        "think_time_sec": THINK_TIME_SEC,
        "scholarship_ids_sample": scholarship_ids,
        "ramps": [],
        "recommendation": "",
    }

    print(f"Warming {args.base_url} …")
    warm = _fetch(args.base_url, "/health")
    print(f"  /health -> {warm.status} ({warm.latency_ms:.0f} ms)")

    for vu in args.users:
        print(f"Ramp: {vu} virtual users …")
        result = run_ramp(args.base_url, vu, scholarship_ids)
        print(
            f"  requests={result.total_requests} errors={result.errors} "
            f"error_rate={result.error_rate_pct}% avg={result.avg_ms}ms p95={result.p95_ms}ms"
        )
        payload["ramps"].append(
            {
                "virtual_users": result.virtual_users,
                "total_requests": result.total_requests,
                "errors": result.errors,
                "error_rate_pct": result.error_rate_pct,
                "avg_ms": result.avg_ms,
                "p95_ms": result.p95_ms,
            }
        )

    # Evidence-backed recommendation for 30-person university session.
    r30 = next((r for r in payload["ramps"] if r["virtual_users"] == 30), payload["ramps"][0] if payload["ramps"] else None)
    if r30 and r30["error_rate_pct"] <= 1.0 and r30["p95_ms"] <= 3000:
        payload["recommendation"] = (
            "A 30-person concurrent read session is likely acceptable on the warmed free-tier instance "
            f"(p95 {r30['p95_ms']} ms, error rate {r30['error_rate_pct']}%). "
            "Monitor Render CPU/memory and Supabase pooler during real sessions."
        )
    elif r30:
        payload["recommendation"] = (
            f"30 concurrent users showed p95 {r30['p95_ms']} ms with {r30['error_rate_pct']}% errors. "
            "Upgrade Render tier or add caching before advertising large university sessions."
        )
    else:
        payload["recommendation"] = "No ramp data collected."

    report_path = args.report
    Path = __import__("pathlib").Path
    Path(report_path).parent.mkdir(parents=True, exist_ok=True)
    Path(report_path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nRecommendation: {payload['recommendation']}")
    print(f"Results written to {report_path}")


if __name__ == "__main__":
    main()
