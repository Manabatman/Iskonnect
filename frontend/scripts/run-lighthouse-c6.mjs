#!/usr/bin/env node
/**
 * C6 Lighthouse mobile run — see docs/engineering/benchmarks/lighthouse-c6-runbook.md
 * Requires: production build, preview on :4173, Chrome/Edge installed.
 */
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const frontendRoot = path.join(__dirname, "..");
const outJson = path.join(frontendRoot, "..", "docs", "engineering", "benchmarks", "lighthouse-home-mobile-c6.json");
const url = process.env.LIGHTHOUSE_URL ?? "http://127.0.0.1:4173/";

const chromePaths = [
  process.env.CHROME_PATH,
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  "/usr/bin/google-chrome",
  "/usr/bin/chromium-browser",
].filter(Boolean);

const chromePath = chromePaths.find((p) => fs.existsSync(p));
const env = chromePath ? { ...process.env, CHROME_PATH: chromePath } : { ...process.env };

const args = [
  url,
  "--only-categories=performance,accessibility",
  "--form-factor=mobile",
  "--screenEmulation.mobile=true",
  "--throttling-method=simulate",
  "--output=json",
  `--output-path=${outJson}`,
  "--quiet",
];

console.log(`Lighthouse → ${url}`);
const result = spawnSync("npx", ["lighthouse", ...args], { cwd: frontendRoot, stdio: "inherit", env, shell: true });

if (result.status !== 0) {
  process.exit(result.status ?? 1);
}

const report = JSON.parse(fs.readFileSync(outJson, "utf8"));
const perf = report.categories?.performance?.score;
const a11y = report.categories?.accessibility?.score;
const lcp = report.audits?.["largest-contentful-paint"]?.numericValue;
const cls = report.audits?.["cumulative-layout-shift"]?.numericValue;

console.log("\n--- C6 summary ---");
console.log(`Performance: ${perf != null ? Math.round(perf * 100) : "—"}`);
console.log(`Accessibility: ${a11y != null ? Math.round(a11y * 100) : "—"}`);
console.log(`LCP (ms): ${lcp != null ? Math.round(lcp) : "—"}`);
console.log(`CLS: ${cls ?? "—"}`);
console.log(`Artifact: ${outJson}`);

const bundle = spawnSync("node", ["scripts/check-bundle-budget.mjs"], { cwd: frontendRoot, stdio: "inherit" });
process.exit(bundle.status ?? 0);
