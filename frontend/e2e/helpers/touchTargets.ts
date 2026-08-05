import type { Page } from "@playwright/test";

export const MIN_TOUCH_PX = 44;

export type TouchTargetViolation = {
  route: string;
  tag: string;
  text: string;
  width: number;
  height: number;
  selector: string;
};

const INTERACTIVE_SELECTOR =
  'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [role="button"], [role="link"], [role="tab"], [role="menuitem"], summary';

export async function collectTouchTargetViolations(
  page: Page,
  route: string,
  minPx = MIN_TOUCH_PX,
): Promise<TouchTargetViolation[]> {
  const violations: TouchTargetViolation[] = [];
  const handles = await page.locator(INTERACTIVE_SELECTOR).elementHandles();
  let index = 0;
  for (const handle of handles) {
    const box = await handle.boundingBox();
    if (!box || box.width === 0 || box.height === 0) {
      await handle.dispose();
      continue;
    }
    const visible = await handle.isVisible();
    if (!visible) {
      await handle.dispose();
      continue;
    }
    const tag = (await handle.evaluate((el) => el.tagName.toLowerCase())) ?? "unknown";
    const text = (
      await handle.evaluate((el) => (el.textContent ?? "").trim().slice(0, 60))
    ).replace(/\s+/g, " ");
    if (box.width < minPx || box.height < minPx) {
      violations.push({
        route,
        tag,
        text,
        width: Math.round(box.width),
        height: Math.round(box.height),
        selector: `${tag}[data-touch-audit="${index}"]`,
      });
    }
    await handle.evaluate((el, i) => el.setAttribute("data-touch-audit", String(i)), index);
    index += 1;
    await handle.dispose();
  }
  return violations;
}

export function summarizeByRoute(violations: TouchTargetViolation[]): Record<string, number> {
  const counts: Record<string, number> = {};
  for (const v of violations) {
    counts[v.route] = (counts[v.route] ?? 0) + 1;
  }
  return counts;
}
