import { describe, expect, it } from "vitest";
import { parseServerTiming } from "./perfTiming";

describe("parseServerTiming", () => {
  it("parses single metric", () => {
    expect(parseServerTiming("wall;dur=123.45")).toEqual({ wall: 123.45 });
  });

  it("parses multiple metrics", () => {
    const header = "db-lookup;dur=12.35, bcrypt;dur=180.50, wall;dur=200.00";
    expect(parseServerTiming(header)).toEqual({
      "db-lookup": 12.35,
      bcrypt: 180.5,
      wall: 200,
    });
  });

  it("returns empty object for null", () => {
    expect(parseServerTiming(null)).toEqual({});
  });
});
