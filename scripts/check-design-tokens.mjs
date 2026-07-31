#!/usr/bin/env node
/**
 * DS-17 — fail CI when new raw Tailwind palette utilities appear in migrated paths.
 * Allows primary/slate in legacy files; flags growth in components/ui and tokenized surfaces.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..", "frontend", "src");

const GUARDED_DIRS = ["components/ui", "pages/LoginPage.tsx", "components/LifecycleStatusBadge.tsx", "components/QualificationStatusBadge.tsx"];

const FORBIDDEN = /\b(?:bg|text|border)-(?:slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d{2,3}\b/g;

let violations = 0;

for (const rel of GUARDED_DIRS) {
  const abs = path.join(root, rel);
  const files = fs.statSync(abs).isDirectory()
    ? walk(abs)
    : [abs];
  for (const file of files) {
    if (!file.endsWith(".tsx") && !file.endsWith(".ts")) continue;
    const src = fs.readFileSync(file, "utf8");
    const matches = src.match(FORBIDDEN);
    if (matches?.length) {
      violations += matches.length;
      console.error(`${path.relative(root, file)}: ${[...new Set(matches)].join(", ")}`);
    }
  }
}

if (violations > 0) {
  console.error(`\nDS-17: ${violations} raw palette utility(ies) in guarded paths. Use semantic tokens.`);
  process.exit(1);
}

console.log("DS-17: guarded paths clean.");

function walk(dir) {
  const out = [];
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) out.push(...walk(p));
    else out.push(p);
  }
  return out;
}
