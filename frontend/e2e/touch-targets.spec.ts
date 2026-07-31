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

const AUTH_ROUTES = ["/dashboard", "/profile-builder", "/settings"];

test.describe("Touch target audit (360px)", () => {
  test.use({ viewport: { width: 360, height: 640 } });

  const allViolations: TouchTargetViolation[] = [];

  for (const route of PUBLIC_ROUTES) {
    test(`audit ${route}`, async ({ page }) => {
      await page.goto(route, { waitUntil: "networkidle" });
      const violations = await collectTouchTargetViolations(page, route);
      allViolations.push(...violations);
      console.log(`[touch-audit] ${route}: ${violations.length} elements under ${MIN_TOUCH_PX}px`);
    });
  }

  const authEmail = process.env.E2E_AUTH_EMAIL;
  const authPassword = process.env.E2E_AUTH_PASSWORD;

  if (authEmail && authPassword) {
    test.beforeAll(async ({ browser }) => {
      const page = await browser.newPage();
      await page.goto("/login", { waitUntil: "networkidle" });
      await page.fill("#email", authEmail);
      await page.fill("#password", authPassword);
      await page.getByRole("button", { name: /sign in/i }).click();
      await page.waitForURL(/\/(dashboard|profile-builder)/, { timeout: 30_000 });
      await page.context().storageState({ path: "e2e/.auth/user.json" });
      await page.close();
    });

    test.use({ storageState: "e2e/.auth/user.json" });

    for (const route of AUTH_ROUTES) {
      test(`audit auth ${route}`, async ({ page }) => {
        await page.goto(route, { waitUntil: "networkidle" });
        const violations = await collectTouchTargetViolations(page, route);
        allViolations.push(...violations);
        console.log(`[touch-audit] ${route}: ${violations.length} elements under ${MIN_TOUCH_PX}px`);
      });
    }
  }

  test.afterAll(async () => {
    const summary = summarizeByRoute(allViolations);
    const outDir = path.join(process.cwd(), "e2e", "reports");
    fs.mkdirSync(outDir, { recursive: true });
    const payload = {
      capturedAt: new Date().toISOString(),
      viewport: { width: 360, height: 640 },
      minTouchPx: MIN_TOUCH_PX,
      routesAudited: [...PUBLIC_ROUTES, ...(authEmail && authPassword ? AUTH_ROUTES : [])],
      summaryByRoute: summary,
      totalViolations: allViolations.length,
      violations: allViolations,
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
