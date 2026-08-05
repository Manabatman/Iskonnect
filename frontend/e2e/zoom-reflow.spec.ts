import { test, expect } from "@playwright/test";
import { loginViaUi } from "./helpers/auth";

const REFLOW_ROUTES = ["/", "/scholarships/search", "/dashboard"] as const;

async function assertNoHorizontalOverflow(page: import("@playwright/test").Page) {
  const overflow = await page.evaluate(() => {
    const doc = document.documentElement;
    return doc.scrollWidth > doc.clientWidth + 1;
  });
  expect(overflow, "page should not require horizontal scroll").toBe(false);
}

for (const zoom of [1, 2, 4] as const) {
  test.describe(`zoom ${zoom * 100}% reflow (A11Y-13)`, () => {
    for (const route of REFLOW_ROUTES) {
      test(`${route} at ${zoom * 100}% has no horizontal overflow`, async ({ page }) => {
        await page.setViewportSize({ width: 320, height: 640 });
        if (route === "/dashboard") {
          await loginViaUi(page);
        }
        await page.goto(route);
        await page.locator("#main-content").waitFor({ state: "visible", timeout: 30_000 });
        await page.evaluate((z) => {
          document.documentElement.style.zoom = String(z);
        }, zoom);
        await assertNoHorizontalOverflow(page);
      });
    }
  });
}
