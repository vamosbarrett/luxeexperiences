import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { fetchReels } from './fetch_reels.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from project root
app.use(express.static(path.resolve(__dirname, '..')));

// API endpoint to trigger fetching reels
app.get('/api/fetch-reels', async (req, res) => {
  try {
    const count = await fetchReels();
    res.json({ success: true, count });
  } catch (err) {
    console.error('Fetch reels error:', err);
    res.status(500).json({ success: false, error: String(err) });
  }
});

// Simple health
app.get('/api/health', (_req, res) => res.json({ ok: true }));

app.listen(PORT, async () => {
  console.log(`Dev server running on http://localhost:${PORT}`);
  // Run an initial fetch in background (don't block server)
  try {
    await fetchReels();
  } catch (err) {
    console.warn('Initial fetch failed:', err.message);
  }

  // Optionally refresh every 10 minutes
  setInterval(async () => {
    try {
      await fetchReels();
      console.log('Background fetch completed');
    } catch (err) {
      console.warn('Background fetch failed:', err.message);
    }
  }, 10 * 60 * 1000);
});
