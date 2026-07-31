import { describe, expect, it } from "vitest";
import { validateEmail } from "./validateEmail";

describe("validateEmail", () => {
  it("accepts valid addresses", () => {
    expect(validateEmail("user@gmail.com").valid).toBe(true);
  });

  it("rejects missing @", () => {
    expect(validateEmail("usergmail.com").valid).toBe(false);
  });

  it("suggests common domain typos", () => {
    const r = validateEmail("user@gmial.com");
    expect(r.valid).toBe(false);
    expect(r.suggestion).toBe("user@gmail.com");
  });
});
