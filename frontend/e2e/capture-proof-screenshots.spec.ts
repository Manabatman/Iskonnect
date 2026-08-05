/**
 * Capture landing proof-strip screenshots (Wave 6 / D-02).
 * Requires: API on :8000, preview on :4173 (or set BASE_URL).
 * Run: npm run preview (terminal 1) + uvicorn (terminal 2), then npm run capture:proof-screenshots
 */
import { mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { test } from "@playwright/test";
import { loginViaUi } from "./helpers/auth";

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT_DIR = join(__dirname, "..", "public", "landing", "screenshots");

const BASE_URL = process.env.PROOF_CAPTURE_BASE_URL ?? "http://127.0.0.1:4173";

test.describe.configure({ mode: "serial" });

test("capture proof strip screenshots", async ({ page, browserName }) => {
  test.skip(browserName !== "chromium", "Chromium only for consistent captures");
  mkdirSync(OUT_DIR, { recursive: true });

  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto(`${BASE_URL}/scholarships/search`);
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(800);
  await page.screenshot({ path: join(OUT_DIR, "search-filters.webp"), type: "webp", fullPage: false });

  await loginViaUi(page);
  await page.goto(`${BASE_URL}/dashboard`);
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(800);
  await page.screenshot({ path: join(OUT_DIR, "mobile-dashboard.webp"), type: "webp", fullPage: false });

  await page.goto(`${BASE_URL}/match/1`);
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(1200);
  await page.screenshot({ path: join(OUT_DIR, "match-results.webp"), type: "webp", fullPage: false });

  const analysisBtn = page.getByRole("button", { name: /why|match|analysis/i }).first();
  if (await analysisBtn.isVisible().catch(() => false)) {
    await analysisBtn.click();
    await page.waitForTimeout(500);
    await page.screenshot({ path: join(OUT_DIR, "match-breakdown.webp"), type: "webp", fullPage: false });
  } else {
    await page.screenshot({ path: join(OUT_DIR, "match-breakdown.webp"), type: "webp", fullPage: false });
  }
});
