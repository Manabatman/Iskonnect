import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { ScholarshipSearchPage } from "./ScholarshipSearchPage";

vi.mock("../contexts/AuthContext", () => ({
  useAuth: () => ({ user: null, authHeaders: () => ({}) }),
}));

vi.mock("../hooks/useScholarshipSearch", () => ({
  useScholarshipSearch: () => ({
    query: "",
    setQuery: vi.fn(),
    filters: {},
    page: 1,
    setPage: vi.fn(),
    results: [],
    total: 0,
    totalPages: 0,
    loading: false,
    error: null,
    usingCached: false,
    suggestions: [],
    suggestionsOpen: false,
    setSuggestionsOpen: vi.fn(),
    highlightIndex: -1,
    suggestionsRef: { current: null },
    handleSuggestionSelect: vi.fn(),
    handleSearchSubmit: vi.fn((e: Event) => e.preventDefault()),
    handleKeyDown: vi.fn(),
    handleFiltersChange: vi.fn(),
  }),
}));

describe("ScholarshipSearchPage", () => {
  it("shows active opportunity type and opens roadmap dialog", () => {
    render(
      <MemoryRouter>
        <ScholarshipSearchPage />
      </MemoryRouter>
    );

    expect(screen.getByText("Scholarships")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /more opportunity types/i }));
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(screen.getByText("More opportunity types")).toBeInTheDocument();
  });
});
