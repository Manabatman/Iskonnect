import { test, expect } from "@playwright/test";
import * as fs from "node:fs";
import * as path from "node:path";
import {
  collectTouchTargetViolations,
  MIN_TOUCH_PX,
  summarizeByRoute,
  type TouchTargetViolation,
} from "./helpers/touchTargets";

const PUBLIC_ROUTES = ["/", "/login", "/register", "/scholarships/search", "/scholarship-status", "/faq"];

test.describe("Touch target audit (360px)", () => {
  test.use({ viewport: { width: 360, height: 640 } });

  const allViolations: TouchTargetViolation[] = [];

  for (const route of PUBLIC_ROUTES) {
    test(`audit ${route}`, async ({ page }) => {
      await page.goto(route, { waitUntil: "networkidle" });
      const violations = await collectTouchTargetViolations(page, route);
      allViolations.push(...violations);
      // Informational only in P1-02 — inventory, not a hard gate yet
      console.log(`[touch-audit] ${route}: ${violations.length} elements under ${MIN_TOUCH_PX}px`);
    });
  }

  test.afterAll(async () => {
    const summary = summarizeByRoute(allViolations);
    const outDir = path.join(process.cwd(), "e2e", "reports");
    fs.mkdirSync(outDir, { recursive: true });
    const payload = {
      capturedAt: new Date().toISOString(),
      viewport: { width: 360, height: 640 },
      minTouchPx: MIN_TOUCH_PX,
      routesAudited: PUBLIC_ROUTES,
      summaryByRoute: summary,
      totalViolations: allViolations.length,
      violations: allViolations,
    };
    fs.writeFileSync(path.join(outDir, "touch-target-inventory.json"), JSON.stringify(payload, null, 2));
    const mdLines = [
      "# Touch target inventory (P1-02)",
      "",
      `Captured: ${payload.capturedAt}`,
      `Viewport: 360×640 | Minimum: ${MIN_TOUCH_PX}px`,
      "",
      "## Summary by route",
      "",
      "| Route | Violations (< 44px) |",
      "| --- | --- |",
      ...Object.entries(summary).map(([r, c]) => `| ${r} | ${c} |`),
      "",
      `**Total:** ${allViolations.length} violations across ${PUBLIC_ROUTES.length} public routes.`,
      "",
      "Full detail: `frontend/e2e/reports/touch-target-inventory.json`",
      "",
    ];
    const docsPath = path.join(process.cwd(), "..", "docs", "engineering", "touch-target-inventory.md");
    fs.writeFileSync(docsPath, mdLines.join("\n"));
    expect(allViolations.length).toBeGreaterThanOrEqual(0);
  });
});
