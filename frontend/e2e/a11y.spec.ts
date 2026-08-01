import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import type { Page } from "@playwright/test";
import { loginViaUi } from "./helpers/auth";

const AXE_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"] as const;

const PUBLIC_ROUTES = [
  "/",
  "/login",
  "/register",
  "/scholarships/search",
  "/faq",
  "/scholarship-status",
  "/how-it-works",
] as const;

const AUTH_ROUTES = ["/dashboard", "/profile-builder", "/settings", "/applications"] as const;

async function assertNoSeriousOrCriticalViolations(page: Page) {
  const results = await new AxeBuilder({ page }).withTags([...AXE_TAGS]).analyze();
  const blocking = results.violations.filter((v) =>
    ["serious", "critical"].includes(v.impact ?? "")
  );
  expect(blocking, JSON.stringify(blocking, null, 2)).toHaveLength(0);
}

async function waitForPageStable(page: Page) {
  await page.waitForLoadState("domcontentloaded");
  await page.waitForFunction(() => {
    const link = document.querySelector('a[href="/register"]');
    if (!link) return true;
    let el: Element | null = link;
    while (el) {
      const opacity = parseFloat(window.getComputedStyle(el).opacity);
      if (opacity < 0.99) return false;
      el = el.parentElement;
    }
    return true;
  });
  // Framer-motion Reveal on landing uses a 500ms easeOut transition.
  await page.waitForTimeout(550);
}

async function waitForRouteReady(page: Page) {
  await page.locator('[aria-busy="true"]').first().waitFor({ state: "detached", timeout: 30_000 }).catch(() => {});
  await page.locator("#main-content").waitFor({ state: "visible", timeout: 30_000 });
  await waitForPageStable(page);
}

test.describe("axe accessibility scan (QA-04, hard gate)", () => {
  for (const route of PUBLIC_ROUTES) {
    test(`public ${route} has no serious/critical violations`, async ({ page }) => {
      await page.goto(route);
      await waitForPageStable(page);
      await assertNoSeriousOrCriticalViolations(page);
    });
  }

  for (const route of AUTH_ROUTES) {
    test(`auth ${route} has no serious/critical violations`, async ({ page }) => {
      await loginViaUi(page);
      await page.goto(route);
      await waitForRouteReady(page);
      await assertNoSeriousOrCriticalViolations(page);
    });
  }

  test("scholarship detail (public) has no serious/critical violations", async ({ page }) => {
    await page.goto("/scholarships/search");
    const detailLink = page.getByRole("link", { name: /view details/i }).first();
    if (await detailLink.isVisible({ timeout: 10_000 }).catch(() => false)) {
      await detailLink.click();
    } else {
      await page.goto("/scholarship/1");
    }
    await assertNoSeriousOrCriticalViolations(page);
  });
});
