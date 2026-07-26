import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { OpportunityRoadmapDialog } from "./OpportunityRoadmapDialog";

describe("OpportunityRoadmapDialog", () => {
  it("lists coming-soon opportunity types when open", () => {
    const onOpenChange = vi.fn();
    render(
      <MemoryRouter>
        <OpportunityRoadmapDialog open onOpenChange={onOpenChange} />
      </MemoryRouter>
    );

    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(screen.getByText("Internships")).toBeInTheDocument();
    expect(screen.getByText("Research Grants")).toBeInTheDocument();
    expect(screen.queryByText("Scholarships")).not.toBeInTheDocument();
  });

  it("closes when Back to search is clicked", () => {
    const onOpenChange = vi.fn();
    render(
      <MemoryRouter>
        <OpportunityRoadmapDialog open onOpenChange={onOpenChange} />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /back to search/i }));
    expect(onOpenChange).toHaveBeenCalledWith(false);
  });
});
