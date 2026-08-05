import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { OpportunityComingSoonPage } from "./OpportunityComingSoonPage";

function renderAt(path: string) {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route path="/opportunities/:typeSlug" element={<OpportunityComingSoonPage />} />
        <Route path="/scholarships/search" element={<h1>Search Opportunities</h1>} />
      </Routes>
    </MemoryRouter>,
  );
}

describe("OpportunityComingSoonPage", () => {
  it("redirects available scholarships slug to scholarship search", () => {
    renderAt("/opportunities/scholarships");
    expect(screen.getByRole("heading", { name: /search opportunities/i })).toBeInTheDocument();
  });

  it("shows journey page for unlaunched verticals", () => {
    renderAt("/opportunities/internships");
    expect(screen.getByRole("heading", { name: /internships on your opportunity journey/i })).toBeInTheDocument();
    expect(screen.getAllByText(/december 2026 to january 2027/i).length).toBeGreaterThan(0);
    expect(screen.getByRole("heading", { level: 2, name: /^your opportunity journey$/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /notify me/i })).toBeInTheDocument();
  });

  it("shows not found for unknown slugs", () => {
    renderAt("/opportunities/not-a-real-type");
    expect(screen.getByRole("heading", { name: /opportunity type not found/i })).toBeInTheDocument();
  });
});
