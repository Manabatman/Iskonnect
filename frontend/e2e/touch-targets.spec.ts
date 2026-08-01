import { test, expect } from "@playwright/test";
import * as fs from "node:fs";
import * as path from "node:path";
import { loginViaUi } from "./helpers/auth";
import {
  collectTouchTargetViolations,
  MIN_TOUCH_PX,
  summarizeByRoute,
  type TouchTargetViolation,
} from "./helpers/touchTargets";
import {
  filterBlockingViolations,
  type TouchTargetAllowlist,
} from "./helpers/touchTargetAllowlist";

const ALLOWLIST_PATH = path.join(process.cwd(), "e2e", "touch-target-allowlist.json");
const allowlist = JSON.parse(fs.readFileSync(ALLOWLIST_PATH, "utf8")) as TouchTargetAllowlist;
const CAPTURE_ALLOWLIST = process.env.TOUCH_TARGET_CAPTURE_ALLOWLIST === "1";

const PUBLIC_ROUTES = ["/", "/login", "/register", "/scholarships/search", "/scholarship-status", "/faq"];
const AUTH_ROUTES = ["/dashboard", "/profile-builder", "/settings"];

function mergeAllowlistEntries(
  existing: TouchTargetAllowlist,
  violations: TouchTargetViolation[],
): TouchTargetAllowlist {
  const seen = new Set(existing.entries.map((entry) => `${entry.route}|${entry.text ?? ""}|${entry.selector ?? ""}`));
  const entries = [...existing.entries];
  for (const violation of violations) {
    const entry = {
      route: violation.route,
      text: violation.text,
      comment: "MOB-01 baseline debt — shrink during Phase 2 touch-target cleanup",
    };
    const key = `${entry.route}|${entry.text}|`;
    if (!seen.has(key)) {
      seen.add(key);
      entries.push(entry);
    }
  }
  return { ...existing, entries };
}

test.describe("Touch target audit (360px)", () => {
  test.use({ viewport: { width: 360, height: 640 } });

  const allViolations: TouchTargetViolation[] = [];

  test.describe("public routes", () => {
    for (const route of PUBLIC_ROUTES) {
      test(`audit ${route}`, async ({ page }) => {
        await page.goto(route, { waitUntil: "networkidle" });
        const violations = await collectTouchTargetViolations(page, route);
        allViolations.push(...violations);
        console.log(`[touch-audit] ${route}: ${violations.length} elements under ${MIN_TOUCH_PX}px`);
      });
    }
  });

  if (process.env.E2E_AUTH_EMAIL && process.env.E2E_AUTH_PASSWORD) {
    test.describe("authenticated routes", () => {
      for (const route of AUTH_ROUTES) {
        test(`audit auth ${route}`, async ({ page }) => {
          await loginViaUi(page);
          await page.goto(route, { waitUntil: "networkidle" });
          const violations = await collectTouchTargetViolations(page, route);
          allViolations.push(...violations);
          console.log(`[touch-audit] ${route}: ${violations.length} elements under ${MIN_TOUCH_PX}px`);
        });
      }
    });
  }

  test.afterAll(async () => {
    const blockingViolations = filterBlockingViolations(allViolations, allowlist);
    const summary = summarizeByRoute(allViolations);
    const blockingSummary = summarizeByRoute(blockingViolations);
    const outDir = path.join(process.cwd(), "e2e", "reports");
    fs.mkdirSync(outDir, { recursive: true });
    const payload = {
      capturedAt: new Date().toISOString(),
      viewport: { width: 360, height: 640 },
      minTouchPx: MIN_TOUCH_PX,
      routesAudited: [
        ...PUBLIC_ROUTES,
        ...(process.env.E2E_AUTH_EMAIL && process.env.E2E_AUTH_PASSWORD ? AUTH_ROUTES : []),
      ],
      summaryByRoute: summary,
      blockingByRoute: blockingSummary,
      allowlistedCount: allViolations.length - blockingViolations.length,
      totalViolations: allViolations.length,
      blockingViolations: blockingViolations.length,
      violations: allViolations,
      blocking: blockingViolations,
    };
    fs.writeFileSync(path.join(outDir, "touch-target-inventory.json"), JSON.stringify(payload, null, 2));
    const mdLines = [
      "# Touch target inventory (Phase 2 / MOB-01)",
      "",
      `Captured: ${payload.capturedAt}`,
      `Viewport: 360×640 | Minimum: ${MIN_TOUCH_PX}px`,
      "",
      "## Summary by route",
      "",
      "| Route | Violations (< 44px) | Blocking |",
      "| --- | --- | --- |",
      ...Object.entries(summary).map(
        ([r, c]) => `| ${r} | ${c} | ${blockingSummary[r] ?? 0} |`,
      ),
      "",
      `**Total:** ${allViolations.length} violations (${blockingViolations.length} blocking, ${payload.allowlistedCount} allowlisted).`,
      "",
      "Full detail: `frontend/e2e/reports/touch-target-inventory.json`",
      "",
    ];
    const docsPath = path.join(process.cwd(), "..", "docs", "engineering", "touch-target-inventory.md");
    fs.writeFileSync(docsPath, mdLines.join("\n"));

    if (CAPTURE_ALLOWLIST) {
      const merged = mergeAllowlistEntries(allowlist, allViolations);
      fs.writeFileSync(ALLOWLIST_PATH, `${JSON.stringify(merged, null, 2)}\n`);
      console.log(`[touch-audit] wrote ${merged.entries.length} allowlist entries to ${ALLOWLIST_PATH}`);
      return;
    }

    expect(
      blockingViolations,
      blockingViolations.length
        ? `Touch targets under ${MIN_TOUCH_PX}px (not allowlisted):\n${JSON.stringify(blockingViolations, null, 2)}`
        : undefined,
    ).toEqual([]);
  });
});
