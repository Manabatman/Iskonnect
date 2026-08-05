#!/usr/bin/env node
/** Generate favicon, apple-touch-icon, and OG image from logo-light.png */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import sharp from "sharp";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..");
const images = path.join(root, "public", "images");
const logo = path.join(images, "logo-light.png");
const heroDesktop = path.join(images, "hero", "hero-desktop.avif");

async function main() {
  if (!fs.existsSync(logo)) {
    console.error("Missing logo-light.png — run optimize-logos first");
    process.exit(1);
  }

  await sharp(logo).resize(32, 32, { fit: "contain", background: { r: 255, g: 255, b: 255, alpha: 0 } }).png().toFile(path.join(images, "favicon-32.png"));
  await sharp(logo).resize(16, 16, { fit: "contain", background: { r: 255, g: 255, b: 255, alpha: 0 } }).png().toFile(path.join(images, "favicon-16.png"));
  await sharp(logo).resize(180, 180, { fit: "contain", background: { r: 255, g: 255, b: 255, alpha: 1 } }).png().toFile(path.join(images, "apple-touch-icon.png"));

  const ogSource = fs.existsSync(heroDesktop) ? heroDesktop : logo;
  await sharp(ogSource)
    .resize(1200, 630, { fit: "cover", position: "centre" })
    .jpeg({ quality: 82, mozjpeg: true })
    .toFile(path.join(images, "og-default.jpg"));

  // PNG fallback for OG meta (some crawlers prefer JPG; keep jpg as primary file)
  await sharp(path.join(images, "og-default.jpg")).png().toFile(path.join(images, "og-default.png"));

  console.log("Generated favicon-16.png, favicon-32.png, apple-touch-icon.png, og-default.jpg/png");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
