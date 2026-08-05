import type { ComponentProps } from "react";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { MatchAnalysisModal } from "./MatchAnalysisModal";
import type { EligibilityExplanation, MatchResult } from "../types";

const baseMatch: MatchResult = {
  id: 1,
  title: "Test Scholarship",
  score: 85,
  link: null,
  description: "",
  regions: [],
  min_age: null,
  max_age: null,
};

const sampleExplanation: EligibilityExplanation = {
  status: "not_eligible_yet",
  status_label: "Not Eligible Yet",
  summary: "You could become eligible after reaching your next year level or when applications reopen.",
  reason: "If you become an incoming 3rd-year student, you may qualify.",
  application_window: "open",
  next_action: "Keep this on your radar for when you advance",
  requirements: [
    { key: "citizenship", label: "Citizenship (Filipino)", result: "met", evidence: "Your citizenship: Filipino" },
    {
      key: "year_level",
      label: "Year level (3)",
      result: "unmet",
      evidence: "Your year level: 2",
      changeable: "changeable",
      change_hint: "If you become an incoming 3rd-year student, you may qualify.",
    },
  ],
};

function renderModal(props: ComponentProps<typeof MatchAnalysisModal>) {
  return render(
    <MemoryRouter>
      <MatchAnalysisModal {...props} />
    </MemoryRouter>,
  );
}

describe("MatchAnalysisModal", () => {
  it("renders backend summary and status label verbatim", () => {
    renderModal({
      match: baseMatch,
      open: true,
      onOpenChange: () => {},
      explanation: sampleExplanation,
      notCalculated: true,
    });

    expect(screen.getByText("Not Eligible Yet")).toBeInTheDocument();
    expect(
      screen.getByText(
        "You could become eligible after reaching your next year level or when applications reopen.",
      ),
    ).toBeInTheDocument();
    expect(screen.getByText("Your eligibility")).toBeInTheDocument();
  });

  it("groups requirements into met and unmet sections", () => {
    renderModal({
      match: baseMatch,
      open: true,
      onOpenChange: () => {},
      explanation: sampleExplanation,
      notCalculated: true,
    });

    expect(screen.getByText("Requirements you already meet")).toBeInTheDocument();
    expect(screen.getByText("Requirements you don't currently meet")).toBeInTheDocument();
    expect(screen.getByText("Citizenship (Filipino)")).toBeInTheDocument();
    expect(screen.getAllByText("If you become an incoming 3rd-year student, you may qualify.").length).toBeGreaterThan(0);
  });

  it("does not show Not calculated yet dead-end when explanation is present", () => {
    renderModal({
      match: baseMatch,
      open: true,
      onOpenChange: () => {},
      explanation: sampleExplanation,
      notCalculated: true,
    });

    expect(screen.queryByText("Not calculated yet")).not.toBeInTheDocument();
    expect(screen.getByText(/Fit score not available/)).toBeInTheDocument();
  });

  it("shows fixed blocker copy from backend", () => {
    const blocked: EligibilityExplanation = {
      ...sampleExplanation,
      status: "currently_not_eligible",
      status_label: "Currently Not Eligible",
      summary: "One or more permanent eligibility requirements are not met.",
      requirements: [
        {
          key: "citizenship",
          label: "Citizenship (Filipino)",
          result: "unmet",
          changeable: "fixed",
          blocker_explanation:
            "Only Filipino citizens are eligible. Based on the program rules, this requirement cannot be changed.",
        },
      ],
    };

    renderModal({
      match: baseMatch,
      open: true,
      onOpenChange: () => {},
      explanation: blocked,
      notCalculated: true,
    });

    expect(
      screen.getByText(/Based on the program rules, this requirement cannot be changed/),
    ).toBeInTheDocument();
  });

  it("shows Availability in Match Results when catalog is pending", () => {
    const pending: EligibilityExplanation = {
      ...sampleExplanation,
      status: "eligible_now",
      status_label: "Eligible Now",
      summary: "You currently meet the requirements and applications are open.",
      catalog_status: "recommendation_pending",
      catalog_message:
        "This scholarship is not yet included in automated recommendations while we complete and validate its catalog information.",
    };

    renderModal({
      match: baseMatch,
      open: true,
      onOpenChange: () => {},
      explanation: pending,
      notCalculated: true,
    });

    expect(screen.getByText("Availability in Match Results")).toBeInTheDocument();
    expect(
      screen.getByText(/not yet included in automated recommendations/),
    ).toBeInTheDocument();
  });
});
