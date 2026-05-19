import json
import re
from pathlib import Path

root = Path('.')
index = root / 'index.html'
video_map_path = root / 'assets' / 'video_mapping.json'
image_map_path = root / 'assets' / 'image_mapping.json'

with open(index, 'r', encoding='utf-8') as f:
    html = f.read()

mapping = {}
if video_map_path.exists():
    mapping.update(json.load(open(video_map_path, 'r', encoding='utf-8')))
if image_map_path.exists():
    mapping.update(json.load(open(image_map_path, 'r', encoding='utf-8')))

def replace_match(m):
    orig = m.group(0)
    quote = m.group(1)
    path = m.group(2)
    fname = Path(path).name
    if fname in mapping:
        return orig.replace(path, mapping[fname])
    return orig

# Replace src="..." and data-src="..." occurrences
html = re.sub(r'(src|data-src)=(\"|\')(.*?)\2', lambda mm: replace_match(re.match(r'(\"|\')(.*?)\2', mm.group(0))[0:1]) if False else re.sub(r'(src|data-src)=(\"|\')(.*?)\2', replace_match, mm.group(0)) , html)

# Simpler approach: iterate over mapping keys and replace bare filenames
for fname, url in mapping.items():
    html = html.replace(fname, url)

with open(index, 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated index.html with', len(mapping), 'mappings')
