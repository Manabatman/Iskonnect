import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { ERROR_COPY } from "./errorCopy";

const BANNED_STANDALONE = /^Something went wrong\.?$/i;

function collectTsxFiles(dir: string, acc: string[] = []): string[] {
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    const stat = statSync(full);
    if (stat.isDirectory()) {
      if (name === "node_modules" || name === "dist") continue;
      collectTsxFiles(full, acc);
    } else if (/\.(tsx|ts)$/.test(name) && !name.endsWith(".test.ts") && !name.endsWith(".test.tsx")) {
      acc.push(full);
    }
  }
  return acc;
}

describe("copy lint", () => {
  it("ERROR_COPY messages are never the banned standalone phrase", () => {
    for (const entry of Object.values(ERROR_COPY)) {
      expect(entry.message).not.toMatch(BANNED_STANDALONE);
      expect(entry.title).not.toMatch(BANNED_STANDALONE);
    }
  });

  it("student-facing pages avoid standalone 'Something went wrong'", () => {
    const srcRoot = join(process.cwd(), "src", "pages");
    const files = collectTsxFiles(srcRoot);
    const offenders: string[] = [];
    for (const file of files) {
      const text = readFileSync(file, "utf8");
      if (/["'`]Something went wrong["'`]/.test(text)) {
        offenders.push(file);
      }
    }
    expect(offenders).toEqual([]);
  });
});
