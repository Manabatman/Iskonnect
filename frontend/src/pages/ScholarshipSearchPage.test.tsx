import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi, beforeEach } from "vitest";
import { ScholarshipSearchPage } from "./ScholarshipSearchPage";

const apiFetchMock = vi.fn();

vi.mock("../api/client", () => ({
  apiFetch: (...args: unknown[]) => apiFetchMock(...args),
}));

const authState = vi.hoisted(() => ({
  user: null as { id: number; email: string } | null,
}));

vi.mock("../contexts/AuthContext", () => ({
  useAuth: () => ({
    user: authState.user,
    authHeaders: () => ({ Authorization: "Bearer token" }),
  }),
}));

vi.mock("../hooks/useScholarshipSearch", () => ({
  useScholarshipSearch: () => ({
    query: "",
    setQuery: vi.fn(),
    filters: {},
    sortBy: "relevance" as const,
    setSortBy: vi.fn(),
    page: 1,
    setPage: vi.fn(),
    results: [
      {
        id: 42,
        title: "BPI Foundation Scholarship",
        link: null,
        description: "",
        regions: [],
        min_age: null,
        max_age: null,
      },
    ],
    total: 1,
    totalPages: 1,
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
    clearQuery: vi.fn(),
  }),
}));

vi.mock("../components/ScholarshipCardV2", () => ({
  ScholarshipCardV2: ({
    scholarship,
    onCheckMatch,
  }: {
    scholarship: { id: number };
    onCheckMatch?: (id: number) => void;
  }) => (
    <button type="button" onClick={() => onCheckMatch?.(scholarship.id)}>
      Check my match
    </button>
  ),
}));

vi.mock("../components/MatchAnalysisModal", () => ({
  MatchAnalysisModal: ({
    explanationLoading,
    explanation,
  }: {
    explanationLoading?: boolean;
    explanation?: { summary?: string } | null;
  }) => (
    <div data-testid="match-modal">
      {explanationLoading ? "loading" : explanation?.summary ?? "no-explanation"}
    </div>
  ),
}));

describe("ScholarshipSearchPage", () => {
  beforeEach(() => {
    apiFetchMock.mockReset();
    authState.user = null;
    apiFetchMock.mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({}),
    });
  });

  it("shows Scholarships heading and profile action when logged out", () => {
    render(
      <MemoryRouter>
        <ScholarshipSearchPage />
      </MemoryRouter>,
    );

    expect(screen.getByRole("heading", { level: 1, name: "Scholarships" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /complete your profile/i })).toBeInTheDocument();
  });

  it("fetches eligibility explanation when Check my match is clicked", async () => {
    authState.user = { id: 1, email: "test@example.com" };

    apiFetchMock.mockImplementation(async (url: string) => {
      if (url === "/api/v1/profiles/me") {
        return { ok: true, status: 200, json: async () => ({ id: 7 }) };
      }
      if (url.startsWith("/api/v1/plan/")) {
        return { ok: true, status: 200, json: async () => ({ matches: [] }) };
      }
      if (url.includes("/eligibility")) {
        return {
          ok: true,
          status: 200,
          json: async () => ({
            status: "not_eligible_yet",
            status_label: "Not Eligible Yet",
            summary: "Backend summary text.",
            application_window: "open",
            next_action: "Review",
            requirements: [],
          }),
        };
      }
      return { ok: false, status: 404, json: async () => ({}) };
    });

    render(
      <MemoryRouter>
        <ScholarshipSearchPage />
      </MemoryRouter>,
    );

    const button = screen.getByRole("button", { name: /check my match/i });
    fireEvent.click(button);

    await waitFor(() => {
      expect(apiFetchMock).toHaveBeenCalledWith(
        "/api/v1/scholarships/42/eligibility?profile_id=7",
        expect.objectContaining({ headers: expect.any(Object) }),
      );
    });

    await waitFor(() => {
      expect(screen.getByTestId("match-modal")).toHaveTextContent("Backend summary text.");
    });
  });
});
