#!/usr/bin/env node
/**
 * DS-17 — fail CI when new raw Tailwind palette utilities appear in migrated paths.
 * DS-10 spacing — report off-scale spacing utilities (report-only until Wave 9).
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..", "frontend", "src");

const GUARDED_DIRS = ["components/ui", "pages/LoginPage.tsx", "components/LifecycleStatusBadge.tsx", "components/QualificationStatusBadge.tsx"];

const FORBIDDEN = /\b(?:bg|text|border)-(?:slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d{2,3}\b/g;

/** Allowed Tailwind spacing scale steps (DS-10). */
const ALLOWED_SPACING = new Set(["0", "px", "0.5", "1", "1.5", "2", "3", "4", "5", "6", "8", "12", "16", "24", "32"]);

/** Semantic layout tokens from tailwind.config.js — not numeric scale steps. */
const SEMANTIC_SPACING = new Set([
  "page-gutter",
  "section-gap",
  "card-padding",
  "stack-gap",
  "nav-mobile",
  "sidebar",
  "bottom-nav",
]);

const SPACING_PREFIXES =
  "(?:p|px|py|pt|pb|pl|pr|ps|pe|m|mx|my|mt|mb|ml|mr|ms|me|gap|gap-x|gap-y|space-x|space-y|inset|inset-x|inset-y|top|bottom|left|right|scroll-m|scroll-mx|scroll-my|scroll-mt|scroll-mb|scroll-ml|scroll-mr|scroll-p|scroll-px|scroll-py|scroll-pt|scroll-pb|scroll-pl|scroll-pr)";

const SPACING_UTILITY = new RegExp(`\\b-?${SPACING_PREFIXES}-(\\[(?:[^\\]]+)\\]|\\d+(?:\\.\\d+)?|px)\\b`, "g");

let paletteViolations = 0;

for (const rel of GUARDED_DIRS) {
  const abs = path.join(root, rel);
  const files = fs.statSync(abs).isDirectory() ? walk(abs) : [abs];
  for (const file of files) {
    if (!file.endsWith(".tsx") && !file.endsWith(".ts")) continue;
    const src = fs.readFileSync(file, "utf8");
    const matches = src.match(FORBIDDEN);
    if (matches?.length) {
      paletteViolations += matches.length;
      console.error(`${path.relative(root, file)}: ${[...new Set(matches)].join(", ")}`);
    }
  }
}

if (paletteViolations > 0) {
  console.error(`\nDS-17: ${paletteViolations} raw palette utility(ies) in guarded paths. Use semantic tokens.`);
  process.exit(1);
}

console.log("DS-17: guarded paths clean.");

const spacingViolations = [];
for (const file of walk(root)) {
  if (!file.endsWith(".tsx") && !file.endsWith(".ts")) continue;
  const src = fs.readFileSync(file, "utf8");
  for (const match of src.matchAll(SPACING_UTILITY)) {
    const value = match[1];
    const utility = match[0].replace(/^\-?/, "");
    if (value.startsWith("[")) {
      spacingViolations.push({ file: path.relative(root, file), utility, reason: "arbitrary value" });
      continue;
    }
    if (!ALLOWED_SPACING.has(value) && !SEMANTIC_SPACING.has(value)) {
      spacingViolations.push({ file: path.relative(root, file), utility, reason: `off-scale step "${value}"` });
    }
  }
}

const spacingEnforced = process.env.SPACING_LINT === "enforced";

if (spacingViolations.length > 0) {
  const grouped = new Map();
  for (const v of spacingViolations) {
    const key = `${v.file}: ${v.utility} (${v.reason})`;
    grouped.set(key, (grouped.get(key) ?? 0) + 1);
  }
  console.warn(`\nDS-10 spacing (${spacingEnforced ? "enforced" : "report-only"}): ${spacingViolations.length} violation(s):`);
  for (const [msg, count] of grouped) {
    console.warn(count > 1 ? `  ${msg} ×${count}` : `  ${msg}`);
  }
  if (spacingEnforced) {
    process.exit(1);
  }
} else {
  console.log("DS-10: spacing scale clean.");
}

function walk(dir) {
  const out = [];
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) out.push(...walk(p));
    else out.push(p);
  }
  return out;
}
