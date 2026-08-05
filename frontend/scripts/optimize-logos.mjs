#!/usr/bin/env node
/**
 * Resize navbar logos to 2× display size (~160px wide) for retina.
 * Run from frontend/: node scripts/optimize-logos.mjs
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import sharp from "sharp";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..");
const outDir = path.join(root, "public", "images");
const TARGET_WIDTH = 160;

const LOGOS = ["logo-light.png", "logo-dark.png"];

async function main() {
  for (const name of LOGOS) {
    const src = path.join(outDir, name);
    if (!fs.existsSync(src)) {
      console.error(`Missing ${src}`);
      process.exit(1);
    }
    const meta = await sharp(src).metadata();
    const height = Math.round((meta.height / meta.width) * TARGET_WIDTH);
    const buffer = await sharp(src)
      .resize(TARGET_WIDTH, height, { fit: "inside", withoutEnlargement: true })
      .png({ compressionLevel: 9 })
      .toBuffer();
    fs.writeFileSync(src, buffer);
    console.log(`${name}: ${meta.width}x${meta.height} → ${TARGET_WIDTH}x${height} (${(buffer.length / 1024).toFixed(1)} KB)`);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
