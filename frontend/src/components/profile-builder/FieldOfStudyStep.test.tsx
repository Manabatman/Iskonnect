/** @vitest-environment jsdom */
import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { FieldOfStudyStep } from "./FieldOfStudyStep";
import { FIELDS_OF_STUDY_FALLBACK } from "../../constants/profileOptions";

vi.mock("../../api/client", () => ({
  apiFetch: vi.fn(() => Promise.reject(new Error("offline"))),
}));

describe("FieldOfStudyStep", () => {
  it("renders static fallback options when profile-options is unavailable", async () => {
    const onChange = vi.fn();
    render(
      <FieldOfStudyStep
        state={{
          field_of_study_broad: "",
          field_of_study_specific: "",
          preferred_course_1: "",
          preferred_course_2: "",
          preferred_course_3: "",
          extracurriculars: "",
          awards: "",
        }}
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
