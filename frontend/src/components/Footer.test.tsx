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
  "/roadmap",
  "/success-stories",
  "/forgot-password",
]);

describe("footer link integrity (C5)", () => {
  const allLinks = [
    ...footerProductLinks,
    ...footerTransparencyLinks,
    ...footerCompanyLinks,
    ...footerLegalLinks,
  ];

  it("every footer link targets a known public route", () => {
    for (const { to } of allLinks) {
      expect(PUBLIC_ROUTES.has(to), `unknown footer route: ${to}`).toBe(true);
    }
  });

  it("has no duplicate footer paths", () => {
    const paths = allLinks.map((l) => l.to);
    expect(new Set(paths).size).toBe(paths.length);
  });
});
