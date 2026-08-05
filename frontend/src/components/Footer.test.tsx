import { describe, expect, it } from "vitest";
import {
  footerCompanyLinks,
  footerLegalLinks,
  footerProductLinks,
  footerTransparencyLinks,
} from "../components/Footer";

const PUBLIC_ROUTES = new Set([
  "/",
  "/login",
  "/register",
  "/how-it-works",
  "/how-matching-works",
  "/how-we-verify",
  "/scholarships/search",
  "/contact",
  "/scholarship-status",
  "/faq",
  "/about",
  "/terms",
  "/privacy",
  "/changelog",
  "/forgot-password",
  "/why-iskonnect",
  "/settings",
  "/transparency",
]);

describe("footer link integrity (C5)", () => {
  const primaryLinks = [...footerProductLinks, ...footerCompanyLinks, ...footerTransparencyLinks];
  const allLinks = [...primaryLinks, ...footerLegalLinks];

  it("every footer link targets a known public route", () => {
    for (const { to } of allLinks) {
      expect(PUBLIC_ROUTES.has(to), `unknown footer route: ${to}`).toBe(true);
    }
  });

  it("has no duplicate footer paths in primary columns", () => {
    const paths = primaryLinks.map((l) => l.to);
    expect(new Set(paths).size).toBe(paths.length);
  });

  it("legal footer links target known public routes", () => {
    for (const { to } of footerLegalLinks) {
      expect(PUBLIC_ROUTES.has(to), `unknown legal footer route: ${to}`).toBe(true);
    }
  });
});
