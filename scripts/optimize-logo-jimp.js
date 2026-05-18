#!/usr/bin/env node
// Fallback logo optimizer using jimp (pure JS, works on older Node versions)
// Usage: node scripts/optimize-logo-jimp.js [inputPath] [outputBaseName]

const path = require('path');
const fs = require('fs');

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error('Usage: node scripts/optimize-logo-jimp.js [inputPath] [outputBaseName]');
    process.exit(2);
  }
  const Jimp = require('jimp');
  const input = args[0];
  const base = args[1];
  const outDir = path.join(process.cwd(), 'assets', 'brand');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  try {
    const image = await Jimp.read(input);
    const sizes = [64, 120, 240, 480];
    for (const sz of sizes) {
      const copy = image.clone();
      copy.contain(sz, Jimp.AUTO, Jimp.HORIZONTAL_ALIGN_CENTER | Jimp.VERTICAL_ALIGN_MIDDLE);
      const outPath = path.join(outDir, `${base}-${sz}.png`);
      await copy.quality(90).writeAsync(outPath);
      console.log('Wrote', outPath);
    }
    // also write a full-size PNG (resized to 480 width)
    const outPath = path.join(outDir, `${base}.png`);
    await image.clone().resize(480, Jimp.AUTO).quality(90).writeAsync(outPath);
    console.log('Wrote', outPath);
    console.log('Done. Files in assets/brand. Note: this script does not remove complex backgrounds.');
  } catch (err) {
    console.error('Error:', err);
    process.exit(1);
  }
}

main();
