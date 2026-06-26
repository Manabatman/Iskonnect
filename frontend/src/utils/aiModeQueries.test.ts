import { describe, expect, it } from "vitest";
import {
  buildCareerRoadmapQuery,
  buildReviewCenterAiModeQuery,
  normalizePhilippinesLocation,
} from "./aiModeQueries";

describe("normalizePhilippinesLocation", () => {
  it("defaults empty to Philippines", () => {
    expect(normalizePhilippinesLocation("")).toBe("Philippines");
  });

  it("strips trailing Philippines duplicate", () => {
    expect(normalizePhilippinesLocation("Quezon City, Philippines")).toBe("Quezon City");
    expect(normalizePhilippinesLocation("Philippines Philippines")).toBe("Philippines");
  });
});

describe("buildReviewCenterAiModeQuery", () => {
  it("includes exam focus without double Philippines", () => {
    const q = buildReviewCenterAiModeQuery("Quezon City, Philippines", "UPCAT");
    expect(q).toContain("UPCAT review centers near Quezon City, Philippines");
    expect(q).not.toMatch(/Philippines Philippines/);
  });

  it("uses Philippines when location empty", () => {
    const q = buildReviewCenterAiModeQuery("", null);
    expect(q).toContain("near Philippines.");
  });
});

describe("buildCareerRoadmapQuery", () => {
  it("structures career query for Philippines", () => {
    const q = buildCareerRoadmapQuery("civil engineer", "College / University");
    expect(q).toContain("Career roadmap for civil engineer in the Philippines");
    expect(q).toContain("college or university student");
    expect(q).not.toMatch(/Philippines Philippines/);
  });
});
