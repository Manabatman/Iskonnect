import { describe, expect, it } from "vitest";
import { ERROR_COPY } from "./errorCopy";

const BANNED_STANDALONE = /^Something went wrong\.?$/i;

const COPY_LINT_SKIP = new Set(["AdminPage.tsx", "DesignSystemPage.tsx"]);

const pageSources = import.meta.glob<string>("../pages/**/*.tsx", {
  query: "?raw",
  import: "default",
  eager: true,
});

const landingSources = import.meta.glob<string>("../components/landing/**/*.tsx", {
  query: "?raw",
  import: "default",
  eager: true,
});

function fileBase(path: string): string {
  const parts = path.split(/[/\\]/);
  return parts[parts.length - 1] ?? path;
}

function hasBannedUserCopy(source: string): boolean {
  const strings = source.match(/(["'`])((?:\\.|(?!\1)[^\\])*)\1/g) ?? [];
  for (const literal of strings) {
    if (literal.includes("→")) return true;
    if (/—/.test(literal) && literal.replace(/\\./g, "").length > 5) return true;
  }
  return false;
}

describe("copy lint", () => {
  it("ERROR_COPY messages are never the banned standalone phrase", () => {
    for (const entry of Object.values(ERROR_COPY)) {
      expect(entry.message).not.toMatch(BANNED_STANDALONE);
      expect(entry.title).not.toMatch(BANNED_STANDALONE);
    }
  });

  it("student-facing pages avoid standalone 'Something went wrong'", () => {
    const offenders: string[] = [];
    for (const [path, text] of Object.entries(pageSources)) {
      if (/["'`]Something went wrong["'`]/.test(text)) {
        offenders.push(path);
      }
    }
    expect(offenders).toEqual([]);
  });

  it("student-facing source avoids em dashes and arrow link glyphs in JSX strings", () => {
    const offenders: string[] = [];
    for (const [path, text] of Object.entries({ ...pageSources, ...landingSources })) {
      if (COPY_LINT_SKIP.has(fileBase(path))) continue;
      if (hasBannedUserCopy(text)) {
        offenders.push(path);
      }
    }
    expect(offenders).toEqual([]);
  });
});
