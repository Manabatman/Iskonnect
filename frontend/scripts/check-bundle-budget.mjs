#!/usr/bin/env node
/**
 * Bundle size budget gate (QA-06) + image regression guard.
 * Run after `npm run build` from frontend/.
 */
import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join, extname, relative } from "node:path";
import { gzipSync } from "node:zlib";

const DIST = join(process.cwd(), "dist");
const ASSETS = join(DIST, "assets");
const PUBLIC = join(process.cwd(), "public");

const BUDGETS = {
  entryJsGzipKb: 120,
  vendorJsGzipKb: 420,
  largestRouteChunkGzipKb: 180,
};

const IMAGE_SOFT_WARN_KB = 500;
const IMAGE_HARD_FAIL_KB = 3072;
const IMAGE_EXTENSIONS = new Set([".png", ".jpg", ".jpeg", ".webp", ".avif", ".svg"]);

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

function walkImages(dir, acc = []) {
  if (!existsSync(dir)) return acc;
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    const st = statSync(full);
    if (st.isDirectory()) walkImages(full, acc);
    else if (IMAGE_EXTENSIONS.has(extname(name).toLowerCase())) acc.push(full);
  }
  return acc;
}

function kb(bytes) {
  return Math.round((bytes / 1024) * 10) / 10;
}

function checkPreloadTargets() {
  const indexPath = join(DIST, "index.html");
  if (!existsSync(indexPath)) {
    console.error("FAIL: dist/index.html missing — run npm run build first.");
    return true;
  }
  const html = readFileSync(indexPath, "utf8");
  const hrefs = [...html.matchAll(/rel="preload"[^>]+href="([^"]+)"/g)].map((m) => m[1]);
  let failed = false;
  for (const href of hrefs) {
    const rel = href.replace(/^\//, "");
    const target = join(DIST, rel);
    if (!existsSync(target)) {
      console.error(`FAIL: preload target missing in dist: ${href}`);
      failed = true;
    }
  }
  return failed;
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
    !f.name.startsWith("sentry-"),
);
const largestRoute = routeChunks[0] ?? entry;

console.log("Bundle sizes (gzip):");
for (const f of sized.slice(0, 12)) {
  console.log(`  ${f.name}: ${kb(f.gzip)} KB`);
}

let failed = checkPreloadTargets();

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
    `FAIL: largest route chunk ${kb(largestRoute.gzip)} KB > ${BUDGETS.largestRouteChunkGzipKb} KB budget`,
  );
  failed = true;
}

console.log("\nImage sizes (public/):");
for (const file of walkImages(PUBLIC)) {
  const bytes = statSync(file).size;
  const fileKb = kb(bytes);
  const rel = relative(PUBLIC, file).replace(/\\/g, "/");
  if (fileKb > IMAGE_HARD_FAIL_KB) {
    console.error(`FAIL: ${rel} is ${fileKb} KB (> ${IMAGE_HARD_FAIL_KB} KB hard limit)`);
    failed = true;
  } else if (fileKb > IMAGE_SOFT_WARN_KB) {
    console.warn(`WARN: ${rel} is ${fileKb} KB (soft budget ${IMAGE_SOFT_WARN_KB} KB)`);
  }
}

if (failed) process.exit(1);
console.log("Bundle budget OK (PERF-11 manualChunks ratchet).");
