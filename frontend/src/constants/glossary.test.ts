import { describe, expect, it } from "vitest";
import { GLOSSARY } from "./glossary";

describe("GLOSSARY", () => {
  it("includes core product terms scholarship, match, and profile", () => {
    expect(GLOSSARY.scholarship.definition.length).toBeGreaterThan(20);
    expect(GLOSSARY.match.definition.length).toBeGreaterThan(20);
    expect(GLOSSARY.profile.definition.length).toBeGreaterThan(20);
  });

  it("expands abbreviations on first use in GWA entry", () => {
    expect(GLOSSARY.GWA.definition).toMatch(/General Weighted Average/i);
  });

  it("every entry has term and definition", () => {
    for (const entry of Object.values(GLOSSARY)) {
      expect(entry.term.trim().length).toBeGreaterThan(0);
      expect(entry.definition.trim().length).toBeGreaterThan(10);
    }
  });
});
