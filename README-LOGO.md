Logo optimization helper

Usage:

- Install dependencies:

```bash
npm install sharp
```

- Run the script (will output files to `assets/brand`):

```bash
npm run optimize-logo
```

Notes:
- The script resizes the provided JPG and writes PNGs and a WebP. It attempts a basic flatten/transparent output; for precise background removal use a dedicated tool (remove.bg, Adobe) or provide a source with a clear background.
