/**
 * k6 read-path load test (optional — requires k6 installed).
 *
 *   k6 run -e BASE_URL=https://your-api.onrender.com scripts/loadtest/read_paths.k6.js
 */
import http from "k6/http";
import { sleep, check } from "k6";

const BASE_URL = __ENV.BASE_URL || "http://127.0.0.1:8000";

export const options = {
  scenarios: {
    ramp_30: { executor: "constant-vus", vus: 30, duration: "2m", startTime: "0s" },
    ramp_50: { executor: "constant-vus", vus: 50, duration: "2m", startTime: "2m30s" },
    ramp_100: { executor: "constant-vus", vus: 100, duration: "2m", startTime: "5m" },
  },
  thresholds: {
    http_req_failed: ["rate<0.05"],
    http_req_duration: ["p(95)<5000"],
  },
};

export function setup() {
  http.get(`${BASE_URL}/health`);
  const list = http.get(`${BASE_URL}/api/v1/scholarships?limit=5`);
  let ids = [];
  try {
    const body = list.json();
    const items = Array.isArray(body) ? body : body.results || [];
    ids = items.map((x) => x.id).filter(Boolean);
  } catch (_) {
    /* ignore */
  }
  return { ids };
}

export default function (data) {
  const paths = [
    "/health",
    "/api/v1/scholarships/search?q=ched&limit=20",
    "/api/v1/scholarships?limit=25",
  ];
  if (data.ids && data.ids.length) {
    paths.push(`/api/v1/scholarships/${data.ids[0]}`);
  }
  for (const path of paths) {
    const res = http.get(`${BASE_URL}${path}`);
    check(res, { ok: (r) => r.status >= 200 && r.status < 400 });
    sleep(1.5);
  }
}
