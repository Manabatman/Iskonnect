#!/usr/bin/env node
/**
 * TRUST-OPS — fail CI when student UI promises an unkeepable verification SLA.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const srcRoot = path.join(__dirname, "..", "src");

const SCAN_DIRS = ["pages", "components", "constants"];
const EXCLUDE_FILES = new Set([
  path.normalize("constants/errorCopy.ts"),
]);

/** Student-facing strings must not promise a fixed re-verification window. */
const FORBIDDEN_PATTERNS = [
  /verified within 30/i,
  /re-?verified every 30/i,
  /30[- ]day re-?verif/i,
  /every 30 days.*verif/i,
  /verif(?:ication|ied).*every 30 days/i,
  /30[- ]day freshness guarantee/i,
  /guarantee.*verified within/i,
  /re-?verif(?:y|ication) (?:sla|guarantee)/i,
];

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
    literals.push(m[2]);
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
    for (const text of extractStringLiterals(src)) {
      for (const pattern of FORBIDDEN_PATTERNS) {
        if (pattern.test(text)) {
          violations += 1;
          console.error(`${rel}: forbidden verification SLA string "${text.slice(0, 80)}${text.length > 80 ? "…" : ""}"`);
          break;
        }
      }
    }
  }
}

if (violations > 0) {
  console.error(`\nTRUST-OPS: ${violations} verification SLA promise(s) in student UI. Show per-listing dates instead.`);
  process.exit(1);
}

console.log("TRUST-OPS: no verification SLA promises in student UI paths.");
