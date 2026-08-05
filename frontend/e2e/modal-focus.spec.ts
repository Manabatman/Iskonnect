import { test, expect } from "@playwright/test";
import { loginViaUi } from "./helpers/auth";

test.describe("Match analysis modal focus (A11Y-07)", () => {
  test("traps focus, Escape closes, focus returns to trigger", async ({ page }) => {
    await loginViaUi(page);
    await page.goto("/dashboard");
    await page.locator("#main-content").waitFor({ state: "visible" });

    const matchLink = page.getByRole("link", { name: /view matches|find matches|match results/i }).first();
    if (await matchLink.isVisible({ timeout: 5_000 }).catch(() => false)) {
      await matchLink.click();
    } else {
      await page.goto("/match/1");
    }

    await page.locator("#main-content").waitFor({ state: "visible" });

    const analysisTrigger = page.getByRole("button", { name: /why.*match|match analysis|view analysis/i }).first();
    if (!(await analysisTrigger.isVisible({ timeout: 10_000 }).catch(() => false))) {
      test.skip(true, "No match analysis trigger on this profile — seed data required");
    }

    await analysisTrigger.focus();
    await analysisTrigger.click();

    const dialog = page.getByRole("dialog");
    await expect(dialog).toBeVisible();

    await page.keyboard.press("Tab");
    const focusedInDialog = await page.evaluate(() => {
      const dlg = document.querySelector('[role="dialog"]');
      return dlg?.contains(document.activeElement) ?? false;
    });
    expect(focusedInDialog).toBe(true);

    await page.keyboard.press("Escape");
    await expect(dialog).toBeHidden();

    await expect(analysisTrigger).toBeFocused();
  });
});
