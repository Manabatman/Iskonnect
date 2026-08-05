import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter, Navigate, Route, Routes, useLocation } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

vi.mock("../components/BackNavLink", () => ({
  BackNavLink: () => null,
}));

import { ScholarshipStatusPage } from "./ScholarshipStatusPage";

function LocationProbe() {
  const location = useLocation();
  return (
    <div data-testid="location">
      {location.pathname}
      {location.hash}
    </div>
  );
}

function TrustRedirectRoutes() {
  return (
    <Routes>
      <Route path="/how-matching-works" element={<LocationProbe />} />
      <Route path="/transparency" element={<Navigate to="/how-matching-works" replace />} />
      <Route path="/match-methodology" element={<Navigate to="/how-matching-works#methodology" replace />} />
      <Route path="/why-iskonnect" element={<Navigate to="/how-matching-works#why" replace />} />
    </Routes>
  );
}

describe("trust page redirects (C2)", () => {
  it("redirects /transparency to /how-matching-works", () => {
    render(
      <MemoryRouter initialEntries={["/transparency"]}>
        <TrustRedirectRoutes />
      </MemoryRouter>
    );
    expect(screen.getByTestId("location")).toHaveTextContent("/how-matching-works");
  });

  it("redirects /match-methodology to consolidated matching page", () => {
    render(
      <MemoryRouter initialEntries={["/match-methodology"]}>
        <TrustRedirectRoutes />
      </MemoryRouter>
    );
    expect(screen.getByTestId("location")).toHaveTextContent("/how-matching-works#methodology");
  });

  it("redirects /why-iskonnect to mission section", () => {
    render(
      <MemoryRouter initialEntries={["/why-iskonnect"]}>
        <TrustRedirectRoutes />
      </MemoryRouter>
    );
    expect(screen.getByTestId("location")).toHaveTextContent("/how-matching-works#why");
  });
});

describe("ScholarshipStatusPage (C3)", () => {
  it("shows disclaimer without interaction", () => {
    render(
      <MemoryRouter>
        <ScholarshipStatusPage />
      </MemoryRouter>
    );
    expect(screen.getByTestId("status-guide-disclaimer")).toBeVisible();
    expect(screen.getByText(/does not guarantee funding/i)).toBeInTheDocument();
  });

  it("renders scannable summary labels for lifecycle statuses", () => {
    render(
      <MemoryRouter>
        <ScholarshipStatusPage />
      </MemoryRouter>
    );
    expect(screen.getAllByText("Open now").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Needs verification").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Past cycle").length).toBeGreaterThan(0);
  });

  it("accordion expands on summary click", () => {
    render(
      <MemoryRouter>
        <ScholarshipStatusPage />
      </MemoryRouter>
    );
    const openSummary = screen.getAllByText("Open now")[0].closest("summary");
    expect(openSummary).toBeTruthy();
    fireEvent.click(openSummary!);
    expect(screen.getByText(/Review requirements, gather documents/i)).toBeInTheDocument();
  });
});
