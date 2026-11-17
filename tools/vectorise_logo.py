#!/usr/bin/env python3
"""Vectorise the raster logo into clean SVGs (transparent background).
Usage: python3 tools/vectorise_logo.py path/to/logo.jpg
Writes assets/logo.svg (sampled ink colour), assets/logo-light.svg (cream, for dark backgrounds),
assets/img/favicon.svg + assets/img/logo.png (sewing machine only), deliverables/newquay-seamstress-logo.svg,
and prints the colours sampled from the image."""
import sys, os, re, shutil
import numpy as np, vtracer
from PIL import Image, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = sys.argv[1]
im = Image.open(src).convert("RGB"); W, H = im.size
a = np.asarray(im).astype(float); g = a.mean(axis=2)
# Otsu threshold, then bias darker so tea stains are excluded
hist = np.bincount(g.astype(int).ravel(), minlength=256); tot = g.size; sb = 0; wb = 0; best = (0, 0); sm = (np.arange(256) * hist).sum()
for t in range(256):
    wb += hist[t]
    if not wb or wb == tot: continue
    sb += t * hist[t]; mb = sb / wb; mf = (sm - sb) / (tot - wb); v = wb * (tot - wb) * (mb - mf) ** 2
    if v > best[0]: best = (v, t)
T = best[1] * 0.85
mask = g < T
ink = np.median(a[mask], axis=0).astype(int); paper = np.median(a[~mask], axis=0).astype(int)
dark_paper = np.percentile(a[~mask], 15, axis=0).astype(int)
hexc = lambda c: "#%02x%02x%02x" % tuple(int(x) for x in c)
print("threshold", round(T), "ink", hexc(ink), "parchment", hexc(paper), "tea-stain", hexc(dark_paper))
m = Image.fromarray(np.where(mask, 0, 255).astype("uint8")).filter(ImageFilter.MedianFilter(5))
m = m.resize((W * 2, H * 2), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 0 if v < 128 else 255)
bb = Image.eval(m, lambda v: 255 - v).getbbox(); pad = 24
m = m.crop((max(bb[0] - pad, 0), max(bb[1] - pad, 0), min(bb[2] + pad, m.size[0]), min(bb[3] + pad, m.size[1])))
tmp = "/tmp/_logo_mask.png"; m.convert("RGB").save(tmp)
def trace(png, out, color):
    vtracer.convert_image_to_svg_py(png, out, colormode="binary", mode="spline", filter_speckle=12, corner_threshold=60, length_threshold=4.0, splice_threshold=45, path_precision=2)
    s = open(out).read()
    s = re.sub(r'fill="#(?:000000|000)"', f'fill="{color}"', s)
    s = re.sub(r'<path[^>]*fill="#(?:ffffff|fff|FFFFFF)"[^>]*/>', "", s)
    s = s.replace("<svg ", f'<svg role="img" aria-label="Newquay Seamstress" viewBox="0 0 {Image.open(png).size[0]} {Image.open(png).size[1]}" ', 1)
    open(out, "w").write(s)
os.makedirs(os.path.join(ROOT, "assets/img"), exist_ok=True); os.makedirs(os.path.join(ROOT, "deliverables"), exist_ok=True)
out = os.path.join(ROOT, "assets/logo.svg"); trace(tmp, out, hexc(ink))
light = open(out).read().replace(hexc(ink), "#f1e5c9"); open(os.path.join(ROOT, "assets/logo-light.svg"), "w").write(light)
shutil.copy(out, os.path.join(ROOT, "deliverables/newquay-seamstress-logo.svg"))
# favicon: the topmost block of ink rows (the sewing machine)
H = m.size[1]
rows = (np.asarray(m) < 128).sum(axis=1) > 2; ys = np.where(rows)[0]; top = ys[0]; end = top
gap = int(H * 0.02)
for y in ys:
    if y - end > gap: break
    end = y
cols = np.where((np.asarray(m)[top:end] < 128).sum(axis=0) > 0)[0]
box = (max(cols[0] - 20, 0), max(top - 20, 0), cols[-1] + 20, end + 20)
side = max(box[2] - box[0], box[3] - box[1]); cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2
sq = m.crop((cx - side // 2, cy - side // 2, cx + side // 2, cy + side // 2)); sq.convert("RGB").save("/tmp/_fav.png")
fav = os.path.join(ROOT, "assets/img/favicon.svg"); trace("/tmp/_fav.png", fav, hexc(ink))
rgba = Image.new("RGBA", sq.size, (0, 0, 0, 0)); inkimg = Image.new("RGBA", sq.size, tuple(ink) + (255,)); rgba.paste(inkimg, mask=sq.point(lambda v: 255 - v))
rgba.resize((512, 512), Image.LANCZOS).save(os.path.join(ROOT, "assets/img/logo.png"))
print("wrote", out, "logo-light.svg, favicon.svg, logo.png, deliverables/newquay-seamstress-logo.svg")
