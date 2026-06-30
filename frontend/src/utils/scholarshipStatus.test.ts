import { describe, expect, it } from "vitest";
import {
  formatUiStateLabel,
  lifecycleStatusLabel,
  resolveApplicationStatus,
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
});
