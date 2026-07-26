import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { PermanentDeleteScholarshipModal } from "./PermanentDeleteScholarshipModal";

describe("PermanentDeleteScholarshipModal", () => {
  it("shows irreversible warning and requires DELETE for inactive rows", () => {
    render(
      <PermanentDeleteScholarshipModal
        open
        onOpenChange={vi.fn()}
        scholarship={{ id: 5, title: "Test Scholarship", is_active: false }}
        authHeaders={() => ({})}
        onDeleted={vi.fn()}
      />
    );

    expect(screen.getByText(/permanently removed from the catalog/i)).toBeInTheDocument();
    expect(screen.getByText(/cannot be undone/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /delete permanently/i })).toBeDisabled();

    fireEvent.change(screen.getByPlaceholderText("DELETE"), { target: { value: "DELETE" } });
    expect(screen.getByRole("button", { name: /delete permanently/i })).not.toBeDisabled();
  });

  it("blocks delete when scholarship is still active", () => {
    render(
      <PermanentDeleteScholarshipModal
        open
        onOpenChange={vi.fn()}
        scholarship={{ id: 5, title: "Active Scholarship", is_active: true }}
        authHeaders={() => ({})}
        onDeleted={vi.fn()}
      />
    );

    expect(screen.getByText(/Deactivate this scholarship before permanent deletion/i)).toBeInTheDocument();
    expect(screen.queryByPlaceholderText("DELETE")).not.toBeInTheDocument();
  });
});
