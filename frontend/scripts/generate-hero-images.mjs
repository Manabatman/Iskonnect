#!/usr/bin/env node
/**
 * Generate responsive hero assets (AVIF + WebP + PNG fallback) from source PNGs.
 * Quality-first: do not aggressively compress for arbitrary byte budgets.
 * Run from frontend/: npm run generate:hero-images
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import sharp from "sharp";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..");
const outDir = path.join(root, "public", "images", "hero");

const VARIANTS = [
  { name: "hero-mobile", width: 768, height: 1024, portrait: true },
  { name: "hero-tablet", width: 1024, height: 768, portrait: false },
  { name: "hero-desktop", width: 1920, height: 1080, portrait: false },
];

const QUALITY = {
  avif: 68,
  webp: 82,
  png: 6, // sharp PNG compression level 0-9
};

const SOFT_WARN_BYTES = 500 * 1024;

function resolveSource(variant) {
  const png = path.join(outDir, `${variant.name}.png`);
  if (fs.existsSync(png)) return png;
  const legacy = path.join(outDir, "hero-1.jpg");
  if (fs.existsSync(legacy)) return legacy;
  console.error(`Missing source for ${variant.name}: expected ${png} or ${legacy}`);
  process.exit(1);
}

async function buildPipeline(source, meta, variant) {
  let img = sharp(source);
  if (variant.portrait && meta.width && meta.height) {
    const cropW = Math.round(meta.height * (variant.width / variant.height));
    const left = Math.max(0, Math.round((meta.width - cropW) / 2));
    img = img.extract({ left, top: 0, width: Math.min(cropW, meta.width - left), height: meta.height });
  }
  return img.resize(variant.width, variant.height, { fit: "cover", position: "centre" });
}

async function writeFormat(pipeline, outPath, format, variant) {
  let buffer;
  if (format === "avif") {
    buffer = await pipeline.clone().avif({ quality: QUALITY.avif, effort: 6 }).toBuffer();
  } else if (format === "webp") {
    buffer = await pipeline.clone().webp({ quality: QUALITY.webp }).toBuffer();
  } else {
    const pngMaxBytes = 1800 * 1024;
    let width = variant.width;
    do {
      const resized =
        width === variant.width
          ? pipeline
          : pipeline
              .clone()
              .resize(width, Math.round((variant.height * width) / variant.width), {
                fit: "cover",
                position: "centre",
              });
      buffer = await resized.png({ compressionLevel: 9 }).toBuffer();
      if (buffer.length <= pngMaxBytes || width <= Math.round(variant.width * 0.75)) break;
      width = Math.round(width * 0.92);
    } while (true);
  }
  fs.writeFileSync(outPath, buffer);
  return buffer.length;
}

async function main() {
  fs.mkdirSync(outDir, { recursive: true });
  let anyOverSoft = false;

  for (const variant of VARIANTS) {
    const source = resolveSource(variant);
    const meta = await sharp(source).metadata();
    console.log(`\n${variant.name} ← ${path.basename(source)} (${meta.width}x${meta.height})`);
    const pipeline = await buildPipeline(source, meta, variant);

    for (const format of ["avif", "webp", "png"]) {
      const outPath = path.join(outDir, `${variant.name}.${format}`);
      const bytes = await writeFormat(pipeline, outPath, format, variant);
      const kb = (bytes / 1024).toFixed(1);
      const warn = bytes > SOFT_WARN_BYTES ? " (soft budget warn)" : "";
      if (bytes > SOFT_WARN_BYTES) anyOverSoft = true;
      console.log(`  ${variant.name}.${format}: ${kb} KB${warn}`);
    }
  }

  if (anyOverSoft) {
    console.log("\nNote: some variants exceed 500 KB soft budget — acceptable if visual quality is preserved.");
  }
  console.log("\nDone.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
