#!/usr/bin/env node
/**
 * CLARITY-01 — fail CI when developer-facing strings appear in student UI paths.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const srcRoot = path.join(__dirname, "..", "src");

const SCAN_DIRS = ["pages", "components", "constants"];
const EXCLUDE_FILES = new Set([
  path.normalize("api/client.ts"),
  path.normalize("constants/errorCopy.ts"),
]);

const FORBIDDEN_IN_STRING = /(?:VITE_[A-Z0-9_]+|API_BASE_URL|localhost(?::\d+)?|127\.0\.0\.1)/;

function walk(dir) {
  const out = [];
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) out.push(...walk(p));
    else if (ent.name.endsWith(".tsx") || ent.name.endsWith(".ts")) out.push(p);
  }
  return out;
}

function extractStringLiterals(source) {
  const literals = [];
  const re = /(["'`])((?:\\.|(?!\1)[^\\])*)\1/g;
  let m;
  while ((m = re.exec(source)) !== null) {
    literals.push({ text: m[2], index: m.index });
  }
  return literals;
}

let violations = 0;

for (const relDir of SCAN_DIRS) {
  const absDir = path.join(srcRoot, relDir);
  if (!fs.existsSync(absDir)) continue;
  for (const file of walk(absDir)) {
    const rel = path.normalize(path.relative(srcRoot, file));
    if (EXCLUDE_FILES.has(rel) || rel.endsWith(".test.ts") || rel.endsWith(".test.tsx")) continue;

    const src = fs.readFileSync(file, "utf8");
    for (const { text } of extractStringLiterals(src)) {
      if (FORBIDDEN_IN_STRING.test(text)) {
        violations += 1;
        console.error(`${rel}: forbidden dev string in "${text.slice(0, 80)}${text.length > 80 ? "…" : ""}"`);
      }
    }
  }
}

if (violations > 0) {
  console.error(`\nCLARITY-01: ${violations} developer string(s) in student UI. Use errorCopy.ts instead.`);
  process.exit(1);
}

console.log("CLARITY-01: no developer strings in student UI paths.");
