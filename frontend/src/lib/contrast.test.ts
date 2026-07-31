import { describe, expect, it } from "vitest";
import pairs from "../styles/tokens/contrast-pairs.json";
import { assertContrastPairs, contrastRatio, type ContrastPair } from "./contrast";

describe("DS-11 contrast pairs", () => {
  it("meets WCAG AA for documented token pairs", () => {
    expect(() => assertContrastPairs(pairs as ContrastPair[])).not.toThrow();
  });

  it("computes ratio for primary on background", () => {
    const ratio = contrastRatio("hsl(221 83% 53%)", "hsl(0 0% 100%)");
    expect(ratio).toBeGreaterThanOrEqual(4.5);
  });
});
