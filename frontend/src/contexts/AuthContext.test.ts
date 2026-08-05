import { describe, expect, it } from "vitest";
import { getPostAuthPath, userFromTokenPayload } from "./AuthContext";

describe("userFromTokenPayload", () => {
  it("maps login response fields to AuthUser", () => {
    const user = userFromTokenPayload({
      user_id: 1,
      email: "a@b.com",
      role: "student",
      email_verified: true,
      require_email_verification: false,
      has_profile: true,
    });
    expect(user).toEqual({
      id: 1,
      email: "a@b.com",
      role: "student",
      emailVerified: true,
      requireEmailVerification: false,
      hasProfile: true,
    });
  });
});

describe("getPostAuthPath", () => {
  const base = userFromTokenPayload({
    user_id: 1,
    email: "a@b.com",
    has_profile: false,
  });

  it("routes users without a profile to profile builder", () => {
    expect(getPostAuthPath(base)).toBe("/profile-builder");
  });

  it("routes users with a profile to dashboard", () => {
    expect(getPostAuthPath({ ...base, hasProfile: true })).toBe("/dashboard");
  });

  it("prefers returnTo when provided", () => {
    expect(getPostAuthPath(base, "/settings")).toBe("/settings");
  });
});
