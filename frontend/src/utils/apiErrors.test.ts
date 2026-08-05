import { describe, expect, it } from "vitest";
import { isChunkLoadError, parseApiDetail } from "./apiErrors";

describe("parseApiDetail", () => {
  it("returns string detail as-is", () => {
    expect(parseApiDetail("Invalid email or password")).toBe("Invalid email or password");
  });

  it("extracts msg from FastAPI validation array", () => {
    expect(parseApiDetail([{ type: "value_error", msg: "Password must be at least 10 characters", loc: ["body", "password"] }])).toBe(
      "Password must be at least 10 characters",
    );
  });

  it("never returns [object Object]", () => {
    expect(parseApiDetail([{ loc: ["body"], type: "missing" }])).toBe("Something went wrong. Please try again.");
  });

  it("uses fallback for HTTP status-only strings", () => {
    expect(parseApiDetail("(403)", "Access denied")).toBe("Access denied");
  });
});

describe("isChunkLoadError", () => {
  it("detects ChunkLoadError", () => {
    const err = new Error("Loading chunk 123 failed");
    err.name = "ChunkLoadError";
    expect(isChunkLoadError(err)).toBe(true);
  });

  it("detects dynamic import failure message", () => {
    expect(isChunkLoadError(new Error("Failed to fetch dynamically imported module"))).toBe(true);
  });
});
