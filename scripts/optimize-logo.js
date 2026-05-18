#!/usr/bin/env node
// Optimize and convert logo to transparent PNG(s) using sharp
// Usage: node scripts/optimize-logo.js [inputPath] [outputBaseName]
// Example: node scripts/optimize-logo.js "LUXE EXPERIENCE LOGO.jpg" logo

const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

async function run() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error('Usage: node scripts/optimize-logo.js [inputPath] [outputBaseName]');
    process.exit(2);
  }

  const input = args[0];
  const base = args[1];
  const outDir = path.join(process.cwd(), 'assets', 'brand');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  try {
    const img = sharp(input).flatten({ background: { r: 0, g: 0, b: 0, alpha: 0 } });

    // Produce multiple sizes
    const sizes = [64, 120, 240, 480];
    for (const sz of sizes) {
      const outPath = path.join(outDir, `${base}-${sz}.png`);
      await img
        .resize({ width: sz })
        .png({ quality: 90, compressionLevel: 9 })
        .toFile(outPath);
      console.log('Wrote', outPath);
    }

    // Also produce an optimized webp
    const webpOut = path.join(outDir, `${base}.webp`);
    await img
      .resize({ width: 480 })
      .webp({ quality: 85 })
      .toFile(webpOut);
    console.log('Wrote', webpOut);

    console.log('Done. Check the assets/brand folder. If you need background removal, consider using a dedicated background-removal tool or supplying a higher-contrast source image.');
  } catch (err) {
    console.error('Error processing image:', err);
    process.exit(1);
  }
}

run();
