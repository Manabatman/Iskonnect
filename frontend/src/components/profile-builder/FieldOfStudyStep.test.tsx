/** @vitest-environment jsdom */
import { render } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { FieldOfStudyStep } from "./FieldOfStudyStep";
import { FIELDS_OF_STUDY_FALLBACK } from "../../constants/profileOptions";
import { INITIAL_STATE } from "./profileBuilderState";

vi.mock("../../api/client", () => ({
  apiFetch: vi.fn(() => Promise.reject(new Error("offline"))),
}));

describe("FieldOfStudyStep", () => {
  it("renders static fallback options when profile-options is unavailable", async () => {
    const onChange = vi.fn();
    render(
      <FieldOfStudyStep
        state={INITIAL_STATE}
        onChange={onChange}
      />
    );

    const select = document.getElementById("pb-field_of_study_broad") as HTMLSelectElement;
    expect(select).toBeTruthy();
    const values = Array.from(select.options).map((o) => o.value);
    expect(values).toContain("Law");
    expect(values).toContain("Architecture");
    expect(values).toContain(FIELDS_OF_STUDY_FALLBACK[1].options[0].value);
  });
});
