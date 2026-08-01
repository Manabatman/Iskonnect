import { describe, expect, it } from "vitest";
import { ERROR_COPY, containsDevString, resolveUserErrorMessage } from "./errorCopy";

describe("ERROR_COPY", () => {
  it("every kind has title, message, and recovery action", () => {
    for (const entry of Object.values(ERROR_COPY)) {
      expect(entry.title.trim().length).toBeGreaterThan(0);
      expect(entry.message.trim().length).toBeGreaterThan(0);
      expect(entry.recoveryAction.trim().length).toBeGreaterThan(0);
    }
  });

  it("never uses the banned standalone phrase", () => {
    for (const entry of Object.values(ERROR_COPY)) {
      expect(entry.message).not.toBe("Something went wrong");
      expect(entry.title).not.toBe("Something went wrong");
    }
  });

  it("search_no_results names a recovery path", () => {
    expect(ERROR_COPY.search_no_results.message.toLowerCase()).toMatch(/filter/);
  });
});

describe("resolveUserErrorMessage", () => {
  it("maps fetch failures to student-safe network copy", () => {
    expect(resolveUserErrorMessage(new TypeError("Failed to fetch"))).toMatch(/temporary|try again/i);
  });

  it("strips dev strings from error messages", () => {
    expect(resolveUserErrorMessage(new Error("VITE_API_BASE_URL is missing"))).toBe(
      ERROR_COPY.generic.message,
    );
  });
});

describe("containsDevString", () => {
  it("flags localhost and env var patterns", () => {
    expect(containsDevString("http://localhost:5173")).toBe(true);
    expect(containsDevString("Check VITE_SENTRY_DSN")).toBe(true);
    expect(containsDevString("Please try again later.")).toBe(false);
  });
});
