import { render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

vi.mock("../contexts/AuthContext", () => ({
  useAuth: () => ({ user: null, loading: false }),
}));

vi.mock("../hooks/usePublicStats", () => ({
  usePublicStats: () => ({ verified_listing_count: 77, provider_count: 63 }),
}));

vi.mock("../components/landing/Reveal", () => ({
  Reveal: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

import { LANDING_SECTION_ORDER, LandingPage } from "./LandingPage";

describe("LandingPage (C4)", () => {
  it("renders sections in §11.6 order", () => {
    render(
      <MemoryRouter>
        <LandingPage />
      </MemoryRouter>
    );
    const page = screen.getByTestId("landing-page");
    const ids = within(page)
      .getAllByTestId(/landing-/)
      .map((el) => el.getAttribute("data-testid")?.replace("landing-", "") ?? "");
    expect(ids).toEqual([...LANDING_SECTION_ORDER]);
  });

  it("hero has exactly one primary CTA button", () => {
    render(
      <MemoryRouter>
        <LandingPage />
      </MemoryRouter>
    );
    expect(screen.getAllByTestId("hero-primary-cta")).toHaveLength(1);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent(/actually eligible/i);
  });
});
