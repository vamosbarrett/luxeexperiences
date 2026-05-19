"""
Upload all .mp4 files in the workspace root to Cloudinary and write a mapping file.

Usage:
  - Install requests: pip install requests
  - Set env vars: CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
  - Run: python scripts/upload_videos_cloudinary.py

Outputs:
  - assets/video_mapping.json -> { "local-filename.mp4": "https://.../uploaded.mp4", ... }

Notes:
  - Uploaded public_id will be the filename without extension. If that already exists in your Cloudinary account,
    Cloudinary will append a suffix unless you set "overwrite": "true" in the upload params.
"""
import os
import sys
import json
import glob
import requests

CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
API_KEY = os.environ.get('CLOUDINARY_API_KEY')
API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

if not (CLOUD_NAME and API_KEY and API_SECRET):
    print('Missing Cloudinary credentials. Please set CLOUDINARY_CLOUD_NAME, API_KEY, and API_SECRET.')
    sys.exit(1)

UPLOAD_URL = f'https://api.cloudinary.com/v1_1/{CLOUD_NAME}/video/upload'

mp4_files = sorted(glob.glob('*.mp4'))
if not mp4_files:
    print('No .mp4 files found in the workspace root.')
    sys.exit(0)

mapping = {}

for path in mp4_files:
    filename = os.path.basename(path)
    public_id = os.path.splitext(filename)[0]
    print(f'Uploading {filename} as public_id={public_id} ...')
    with open(path, 'rb') as fh:
        files = {'file': (filename, fh, 'video/mp4')}
        data = {'public_id': public_id, 'resource_type': 'video'}
        try:
            resp = requests.post(UPLOAD_URL, auth=(API_KEY, API_SECRET), files=files, data=data, timeout=120)
        except Exception as e:
            print('Upload failed for', filename, str(e))
            continue
        if resp.status_code != 200:
            print('Upload failed for', filename, resp.status_code, resp.text[:200])
            continue
        info = resp.json()
        secure_url = info.get('secure_url') or info.get('url')
        if secure_url:
            mapping[filename] = secure_url
            print('Uploaded:', secure_url)
        else:
            print('Upload succeeded but no url returned for', filename)

# ensure assets folder
os.makedirs('assets', exist_ok=True)
map_path = os.path.join('assets', 'video_mapping.json')
with open(map_path, 'w', encoding='utf-8') as mf:
    json.dump(mapping, mf, indent=2)

print(f'Wrote mapping for {len(mapping)} files to {map_path}')
print('Next: run the update-index script or ask me to update index.html with these URLs')