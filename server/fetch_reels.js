/*
Node script to fetch recent reels (video posts) from an Instagram Business/Creator account
using the Facebook Graph API (Instagram Graph API).

Requirements:
- Node 18+
- An Instagram Business or Creator account connected to a Facebook Page
- A Facebook App with `instagram_basic` and `pages_read_engagement` permissions approved
- A long-lived access token for the Facebook app

This script fetches recent media, filters for reels (video media), and writes a simple
JSON list to `data/reels.json`.

Usage:
1. Set environment variables:
   - IG_BUSINESS_ACCOUNT_ID (the Instagram Business Account ID)
   - FB_GRAPH_TOKEN (a valid access token with required scopes)
2. Run: node fetch_reels.js

The output file will be: ../data/reels.json (relative to this script)
*/

import fs from 'fs/promises';
import path from 'path';
import fetch from 'node-fetch';
import { fileURLToPath } from 'url';

const IG_ACCOUNT_ID = process.env.IG_BUSINESS_ACCOUNT_ID;
const ACCESS_TOKEN = process.env.FB_GRAPH_TOKEN;

if (!IG_ACCOUNT_ID || !ACCESS_TOKEN) {
  console.error('Missing IG_BUSINESS_ACCOUNT_ID or FB_GRAPH_TOKEN environment variable.');
  process.exit(1);
}

const OUT_DIR = path.resolve(new URL('..', import.meta.url).pathname, 'data');
const OUT_FILE = path.join(OUT_DIR, 'reels.json');

async function ensureOutDir() {
  try {
    await fs.mkdir(OUT_DIR, { recursive: true });
  } catch (e) {
    // ignore
  }
}

export async function fetchReels() {
  // We will request the recent media and request fields: id, caption, media_type, media_url, permalink, timestamp
  const fields = ['id', 'caption', 'media_type', 'media_url', 'permalink', 'timestamp', 'username'];
  const url = `https://graph.facebook.com/v17.0/${IG_ACCOUNT_ID}/media?fields=${fields.join(',')}&access_token=${ACCESS_TOKEN}&limit=50`;

  const res = await fetch(url);
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`Graph API error: ${res.status} ${txt}`);
  }

  const json = await res.json();
  const items = (json.data || []).filter(item => item.media_type === 'VIDEO' || item.media_type === 'CAROUSEL_VIDEO');

  // map to minimal structure
  const mapped = items.map(i => ({
    id: i.id,
    caption: i.caption || '',
    media_url: i.media_url || '',
    permalink: i.permalink,
    timestamp: i.timestamp,
    author: i.username || ''
  }));

  await ensureOutDir();
  await fs.writeFile(OUT_FILE, JSON.stringify(mapped, null, 2), 'utf8');
  console.log(`Wrote ${mapped.length} reel(s) to ${OUT_FILE}`);
  return mapped.length;
}

// Allow script to be run directly as well as imported
const __filename = fileURLToPath(import.meta.url);
if (process.argv[1] === __filename) {
  fetchReels().catch(err => {
    console.error(err);
    process.exit(1);
  });
}
