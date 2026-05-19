#!/usr/bin/env python3
"""
Upload referenced images (and videos if needed) from index.html to Cloudinary.
Writes/updates assets/image_mapping.json and assets/video_mapping.json.
Requires env vars: CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
"""
import os
import re
import json
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)

html = Path('index.html').read_text(encoding='utf-8')

# collect referenced filenames from arrays and src attributes
files = set()
for m in re.finditer(r"\[([^\]]+)\]", html, re.S):
    chunk = m.group(1)
    for s in re.findall(r"'([^']+\.(?:jpg|jpeg|png|webp|mp4))'", chunk):
        files.add(s)
for s in re.findall(r'src=["\']([^"\']+\.(?:jpg|jpeg|png|webp|mp4))["\']', html):
    files.add(Path(s).name)
for s in re.findall(r'data-src=["\']([^"\']+\.(?:jpg|jpeg|png|webp|mp4))["\']', html):
    files.add(Path(s).name)

files = {f for f in files if f}
print(f'Found {len(files)} referenced media files')

# load existing mappings
assets_dir = Path('assets')
if not assets_dir.exists():
    assets_dir.mkdir(parents=True)
video_map = assets_dir / 'video_mapping.json'
image_map = assets_dir / 'image_mapping.json'
mapping = {}
if video_map.exists():
    try:
        mapping.update(json.load(video_map.open(encoding='utf-8')))
    except Exception:
        pass
if image_map.exists():
    try:
        mapping.update(json.load(image_map.open(encoding='utf-8')))
    except Exception:
        pass

# cloudinary endpoints
CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
API_KEY = os.environ.get('CLOUDINARY_API_KEY')
API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')
if not (CLOUD_NAME and API_KEY and API_SECRET):
    print('Missing Cloudinary credentials in env.')
    raise SystemExit(1)

BASE = f'https://api.cloudinary.com/v1_1/{CLOUD_NAME}'
IMG_UPLOAD = f'{BASE}/image/upload'
VID_UPLOAD = f'{BASE}/video/upload'

uploaded = 0
for fname in sorted(files):
    if fname in mapping:
        continue
    # find local file
    local = Path(fname)
    if not local.exists():
        candidates = list(Path('.').rglob(fname))
        if candidates:
            local = candidates[0]
        else:
            print('Local file not found, skipping:', fname)
            continue
    public_id = Path(fname).stem
    ext = Path(fname).suffix.lower()
    upload_url = VID_UPLOAD if ext == '.mp4' else IMG_UPLOAD
    print('Uploading', str(local), '->', public_id)
    with open(local, 'rb') as fh:
        try:
            resp = requests.post(upload_url, auth=(API_KEY, API_SECRET), files={'file': (fname, fh)}, data={'public_id': public_id}, timeout=120)
        except Exception as e:
            print('Upload error', fname, e)
            continue
    if resp.status_code != 200:
        print('Upload failed', fname, resp.status_code, resp.text[:200])
        continue
    info = resp.json()
    url = info.get('secure_url') or info.get('url')
    if url:
        mapping[fname] = url
        uploaded += 1
        print('Uploaded OK:', fname)

# write mappings split by type
video_map_data = {k: v for k, v in mapping.items() if k.lower().endswith('.mp4')}
image_map_data = {k: v for k, v in mapping.items() if not k.lower().endswith('.mp4')}
if video_map_data:
    with open(video_map, 'w', encoding='utf-8') as f:
        json.dump(video_map_data, f, indent=2)
if image_map_data:
    with open(image_map, 'w', encoding='utf-8') as f:
        json.dump(image_map_data, f, indent=2)

print('Done. Uploaded', uploaded, 'new files')
