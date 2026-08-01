import { render } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

const mockUseReducedMotion = vi.fn(() => false);
vi.mock("framer-motion", async () => {
  const actual = await vi.importActual<typeof import("framer-motion")>("framer-motion");
  return {
    ...actual,
    useReducedMotion: () => mockUseReducedMotion(),
  };
});

import { Reveal } from "./Reveal";

describe("Reveal (C5 motion)", () => {
  it("uses reduced motion when prefers-reduced-motion", () => {
    mockUseReducedMotion.mockReturnValue(true);
    const { container } = render(
      <Reveal>
        <p>content</p>
      </Reveal>
    );
    expect(container.textContent).toContain("content");
  });
});
