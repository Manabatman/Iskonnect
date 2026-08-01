#!/usr/bin/env node
/**
 * Bundle size budget gate (QA-06).
 * Run after `npm run build` from frontend/.
 */
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, extname } from "node:path";
import { gzipSync } from "node:zlib";

const DIST = join(process.cwd(), "dist");
const ASSETS = join(DIST, "assets");

const BUDGETS = {
  entryJsGzipKb: 120,
  vendorJsGzipKb: 420,
  largestRouteChunkGzipKb: 180,
};

function gzipSizeBytes(filePath) {
  const raw = readFileSync(filePath);
  return gzipSync(raw).length;
}

function listJsFiles(dir) {
  if (!statSync(dir, { throwIfNoEntry: false })?.isDirectory()) return [];
  return readdirSync(dir)
    .filter((f) => extname(f) === ".js")
    .map((f) => join(dir, f));
}

function kb(bytes) {
  return Math.round((bytes / 1024) * 10) / 10;
}

const jsFiles = listJsFiles(ASSETS);
if (!jsFiles.length) {
  console.error("No JS assets in dist/assets — run npm run build first.");
  process.exit(1);
}

const sized = jsFiles
  .map((path) => ({ path, gzip: gzipSizeBytes(path), name: path.split(/[/\\]/).pop() }))
  .sort((a, b) => b.gzip - a.gzip);

const entry = sized.find((f) => f.name.startsWith("index-")) ?? sized[0];
const vendor = sized.find((f) => f.name.startsWith("vendor-"));
const routeChunks = sized.filter(
  (f) =>
    !f.name.startsWith("index-") &&
    !f.name.startsWith("vendor-") &&
    !f.name.startsWith("radix-") &&
    !f.name.startsWith("framer-motion-") &&
    !f.name.startsWith("sentry-")
);
const largestRoute = routeChunks[0] ?? entry;

console.log("Bundle sizes (gzip):");
for (const f of sized.slice(0, 12)) {
  console.log(`  ${f.name}: ${kb(f.gzip)} KB`);
}

let failed = false;
if (kb(entry.gzip) > BUDGETS.entryJsGzipKb) {
  console.error(`FAIL: entry JS ${kb(entry.gzip)} KB > ${BUDGETS.entryJsGzipKb} KB budget`);
  failed = true;
}
if (vendor && kb(vendor.gzip) > BUDGETS.vendorJsGzipKb) {
  console.error(`FAIL: vendor JS ${kb(vendor.gzip)} KB > ${BUDGETS.vendorJsGzipKb} KB budget`);
  failed = true;
}
if (largestRoute && kb(largestRoute.gzip) > BUDGETS.largestRouteChunkGzipKb) {
  console.error(
    `FAIL: largest route chunk ${kb(largestRoute.gzip)} KB > ${BUDGETS.largestRouteChunkGzipKb} KB budget`
  );
  failed = true;
}

if (failed) process.exit(1);
console.log("Bundle budget OK (PERF-11 manualChunks ratchet).");
