/** Shared E2E credentials — must match app/scripts/seed_ci_e2e.py (RFC 2606 example.com for Pydantic EmailStr). */
export const E2E_USER = {
  email: "e2e-test@example.com",
  password: "E2eTestPass1!",
  name: "E2E Test Student",
};

export async function loginViaUi(
  page: import("@playwright/test").Page,
  email = E2E_USER.email,
  password = E2E_USER.password
) {
  await page.goto("/login");
  await page.getByLabel(/^email$/i).fill(email);
  await page.getByLabel(/^password$/i).fill(password);
  await page.getByRole("button", { name: /^sign in$/i }).click();
  await page.waitForURL(/\/(dashboard|profile-builder)/, { timeout: 60_000 });
}
