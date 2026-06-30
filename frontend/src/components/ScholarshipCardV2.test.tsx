import { describe, expect, it, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { ScholarshipCardV2 } from "./ScholarshipCardV2";
import type { ScholarshipInfo } from "../types";

vi.mock("./BookmarkButton", () => ({
  BookmarkButton: () => null,
}));

const baseScholarship: ScholarshipInfo = {
  id: 1,
  title: "Test Scholarship",
  provider: "CHED",
  link: "https://example.com/scholarship",
  description: "A test scholarship description.",
  regions: ["NCR"],
  min_age: null,
  max_age: null,
  provider_type: "Government",
};

function renderCard(scholarship: ScholarshipInfo) {
  return render(
    <MemoryRouter>
      <ScholarshipCardV2 scholarship={scholarship} />
    </MemoryRouter>
  );
}

describe("ScholarshipCardV2 image", () => {
  it("renders db image when image_url is set", () => {
    renderCard({
      ...baseScholarship,
      image_url: "https://cdn.example.com/s/1.webp",
      image_alt: "CHED banner",
    });
    const img = screen.getByRole("img", { name: "CHED banner" });
    expect(img).toHaveAttribute("src", "https://cdn.example.com/s/1.webp");
    expect(img).toHaveAttribute("loading", "lazy");
  });

  it("uses title as alt when image_alt missing", () => {
    renderCard({
      ...baseScholarship,
      image_url: "https://cdn.example.com/s/1.webp",
    });
    expect(screen.getByRole("img", { name: "Test Scholarship" })).toBeInTheDocument();
  });
});

describe("ScholarshipCardV2 lifecycle badge", () => {
  it("shows canonical Closed label for expired application_status", () => {
    renderCard({
      ...baseScholarship,
      application_status: "closed",
      data_status: "expired",
    });
    expect(screen.getByText("Closed")).toBeInTheDocument();
    expect(screen.queryByText("Expired")).not.toBeInTheDocument();
  });

  it("shows Needs verification for needs_verification status", () => {
    renderCard({
      ...baseScholarship,
      application_status: "needs_verification",
      data_status: "needs_review",
    });
    expect(screen.getAllByText("Needs verification").length).toBeGreaterThan(0);
  });
});
