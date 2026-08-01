import { describe, expect, it } from "vitest";
import {
  formatUiStateLabel,
  lifecycleStatusLabel,
  resolveApplicationStatus,
  statusGuideHref,
} from "./scholarshipStatus";

describe("scholarshipStatus", () => {
  it("resolves archived from is_active false", () => {
    expect(resolveApplicationStatus({ is_active: false })).toBe("archived");
    expect(lifecycleStatusLabel("archived")).toBe("No longer offered");
  });

  it("maps needs_review data_status to needs_verification", () => {
    expect(resolveApplicationStatus({ data_status: "needs_review" })).toBe("needs_verification");
  });

  it("maps eligibility_state to guide labels via formatUiStateLabel", () => {
    expect(formatUiStateLabel("eligible_soon")).toBe("Opening soon");
    expect(formatUiStateLabel("prepare_now")).toBe("Prepare ahead");
  });

  it("uses Past cycle label for previous_cycle", () => {
    expect(lifecycleStatusLabel("previous_cycle")).toBe("Past cycle");
  });

  it("uses Expected to reopen label for expected_reopen", () => {
    expect(lifecycleStatusLabel("expected_reopen")).toBe("Expected to reopen");
  });

  it("defaults unknown lifecycle to needs_verification, not open (TRUST-02)", () => {
    expect(resolveApplicationStatus({})).toBe("needs_verification");
    expect(resolveApplicationStatus({ application_status: null, data_status: null })).toBe(
      "needs_verification"
    );
  });

  it("statusGuideHref deep-links to anchor", () => {
    expect(statusGuideHref("needs_verification")).toBe("/scholarship-status#needs_verification");
  });
});
