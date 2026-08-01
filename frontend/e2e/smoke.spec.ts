import { test, expect } from "@playwright/test";
import { E2E_USER, loginViaUi } from "./helpers/auth";

test.describe("Phase 3 smoke paths (QA-02)", () => {
  test("public search loads and shows results area", async ({ page }) => {
    await page.goto("/scholarships/search");
    await expect(page.getByRole("heading", { name: /search opportunities/i })).toBeVisible();
    await expect(page.getByLabel(/search scholarship names/i)).toBeVisible();
  });

  test("login reaches dashboard for seeded user", async ({ page }) => {
    await loginViaUi(page);
    await expect(page.getByText(new RegExp(E2E_USER.name, "i"))).toBeVisible({ timeout: 30_000 });
  });

  test("authenticated search page loads", async ({ page }) => {
    await loginViaUi(page);
    await page.goto("/scholarships/search");
    await expect(page.getByRole("heading", { name: /search opportunities/i })).toBeVisible();
  });

  test("settings page loads when authenticated", async ({ page }) => {
    await loginViaUi(page);
    await page.goto("/settings");
    await expect(page.getByRole("heading", { name: /settings/i })).toBeVisible();
  });

  test("theme toggle persists across reload", async ({ page }) => {
    await page.goto("/");
    const toggle = page.getByRole("button", { name: /switch to dark mode|switch to light mode/i });
    if (await toggle.isVisible()) {
      await toggle.click();
    }
    const htmlClass = await page.locator("html").getAttribute("class");
    await page.reload();
    const htmlClassAfter = await page.locator("html").getAttribute("class");
    expect(htmlClassAfter).toBe(htmlClass);
  });

  test("register page renders", async ({ page }) => {
    await page.goto("/register");
    await expect(page.getByRole("heading", { name: /create your account/i })).toBeVisible();
  });

  test("available opportunity slug redirects to scholarship search", async ({ page }) => {
    await page.goto("/opportunities/scholarships");
    await expect(page).toHaveURL(/\/scholarships\/search$/);
    await expect(page.getByRole("heading", { name: /search opportunities/i })).toBeVisible();
  });
});
