#!/usr/bin/env python3
"""
Simple logo optimizer using Pillow.
Usage: python scripts/optimize_logo_py.py input_path output_base
Produces PNGs (transparent where near-white) at multiple sizes in assets/brand
"""
import sys
from PIL import Image
import os

def make_transparent(img, threshold=240):
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        r,g,b,a = item
        if r>threshold and g>threshold and b>threshold:
            newData.append((255,255,255,0))
        else:
            newData.append((r,g,b,a))
    img.putdata(newData)
    return img


def main():
    if len(sys.argv)<3:
        print("Usage: python scripts/optimize_logo_py.py input_path output_base")
        sys.exit(2)
    inp = sys.argv[1]
    base = sys.argv[2]
    outdir = os.path.join(os.getcwd(), 'assets', 'brand')
    os.makedirs(outdir, exist_ok=True)

    img = Image.open(inp)
    img = img.convert('RGBA')
    img_t = make_transparent(img, threshold=240)

    sizes = [64,120,240,480]
    for s in sizes:
        out = os.path.join(outdir, f"{base}-{s}.png")
        imr = img_t.copy()
        # resize while keeping aspect ratio
        imr.thumbnail((s, s), Image.LANCZOS)
        imr.save(out, format='PNG', optimize=True)
        print('Wrote', out)

    out_full = os.path.join(outdir, f"{base}.png")
    img_t.thumbnail((480,480), Image.LANCZOS)
    img_t.save(out_full, format='PNG', optimize=True)
    print('Wrote', out_full)

    # Also create a base64 data URL for the 240px asset
    try:
        import base64
        with open(os.path.join(outdir, f"{base}-240.png"),'rb') as f:
            b = base64.b64encode(f.read()).decode('ascii')
        with open(os.path.join(outdir, f"{base}-240.dataurl.txt"),'w',encoding='utf-8') as df:
            df.write('data:image/png;base64,'+b)
        print('Wrote dataurl', os.path.join(outdir, f"{base}-240.dataurl.txt"))
    except Exception:
        pass

if __name__=='__main__':
    main()
