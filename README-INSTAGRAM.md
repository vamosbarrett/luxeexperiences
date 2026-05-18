Luxe Experiences — Instagram Reels Integration

Overview

This project includes a frontend that will dynamically load Instagram Reels from a JSON file (`data/reels.json`). For automated, up-to-date content you can use the included Node script to fetch reels from the Instagram Graph API and write `data/reels.json`.

Files added

- `server/fetch_reels.js` — Node script to fetch recent media from the Instagram Graph API and write `data/reels.json`.
- `data/reels.sample.json` — Example JSON showing the expected format.

Quick setup

1. Install Node (18+ recommended).
2. Create a Facebook App and obtain an access token with `instagram_basic` and related permissions. Follow Facebook documentation:
   https://developers.facebook.com/docs/instagram-api

3. Connect your Instagram Business/Creator account to a Facebook Page and get the Instagram Account ID.

4. Set environment variables and run the script:

```bash
# macOS / Linux
export IG_BUSINESS_ACCOUNT_ID=YOUR_IG_ACCOUNT_ID
export FB_GRAPH_TOKEN=YOUR_LONG_LIVED_ACCESS_TOKEN
node server/fetch_reels.js

# Windows (PowerShell)
$env:IG_BUSINESS_ACCOUNT_ID = 'YOUR_IG_ACCOUNT_ID'
$env:FB_GRAPH_TOKEN = 'YOUR_LONG_LIVED_ACCESS_TOKEN'
node server/fetch_reels.js
```

5. Serve the folder with a simple static server (so `fetch('/data/reels.json')` works). Example using `serve` or `http-server`:

```bash
# install one if you don't have it
npm install -g serve
# from project root
serve .
```

6. Open the site in a browser at the local server URL (e.g., `http://localhost:3000`). The Reels rail will load `data/reels.json` and populate randomly.

Notes & limitations

- Instagram's embedding and API require appropriate tokens and permissions; this script only demonstrates how to fetch media via the Graph API.
- For public embedding to work automatically on the frontend, Instagram may require you to use official oEmbed endpoints or ensure `instgrm.Embeds.process()` is called — this page already loads Instagram's embed script and calls `process()` after injecting content.
- If you prefer a server-rendered approach (recommended for production), use the fetcher to produce HTML server-side instead of client-side injection.

If you'd like, I can also:
- Add an Express-based dev server that runs the fetcher and serves the static files with a single command.
- Wire authentication helpers to refresh long-lived tokens (server-side).
