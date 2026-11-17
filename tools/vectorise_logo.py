#!/usr/bin/env python3
"""Vectorise the raster logo into clean, transparent SVGs.
Usage: python3 tools/vectorise_logo.py source/logo-original.jpg [--threshold 110] [--scale 4] [--turd 40]
- Upscales the greyscale image (keeps the thin inline highlight in the lettering), thresholds the dark ink,
- removes parchment stains / burnt border by keeping only ink components that don't touch the outer margin,
- traces with vtracer (binary, spline) and fills with the ink colour sampled from the image.
Writes assets/logo.svg, assets/logo-light.svg, assets/img/favicon.svg, assets/img/logo.png,
deliverables/newquay-seamstress-logo.svg and prints the sampled palette."""
import sys, os, re, shutil, argparse, json
import numpy as np, vtracer
from PIL import Image, ImageFilter
from scipy import ndimage
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("--threshold", type=float, default=110)
ap.add_argument("--scale", type=int, default=3); ap.add_argument("--turd", type=int, default=40); ap.add_argument("--margin", type=float, default=0.06)
ap.add_argument("--light", default="#f4e9d3")
A = ap.parse_args()
im = Image.open(A.src).convert("RGB"); W, H = im.size; a = np.asarray(im).astype(int); g0 = a.mean(axis=2)
hexc = lambda c: "#%02x%02x%02x" % tuple(int(x) for x in c)

S = A.scale
g = np.asarray(im.convert("L").resize((W * S, H * S), Image.LANCZOS).filter(ImageFilter.GaussianBlur(S * 0.35))).astype(float)
mask = g < A.threshold
lab, n = ndimage.label(mask)
objs = ndimage.find_objects(lab); sizes = ndimage.sum(mask, lab, range(1, n + 1))
mx, my = int(W * S * A.margin), int(H * S * A.margin)
keep = np.zeros(n + 1, bool)
for i, sl in enumerate(objs, 1):
    y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
    if y0 < my or x0 < mx or y1 > H * S - my or x1 > W * S - mx: continue   # burnt border / edge stains
    if sizes[i - 1] < A.turd * S: continue                                  # specks
    keep[i] = True
clean = keep[lab]
bb_y, bb_x = np.where(clean); p = 12 * S
y0, y1, x0, x1 = max(bb_y.min() - p, 0), bb_y.max() + p, max(bb_x.min() - p, 0), bb_x.max() + p
clean = clean[y0:y1, x0:x1]
print(f"components kept {keep.sum()} of {n}; crop {x1-x0}x{y1-y0}")

# palette sampling (original resolution)
inkpix = a[(g0 > 10) & (g0 < 40)]; core = a[(g0 > 15) & (g0 < 60)]
ink = np.median(core, axis=0); ink_deep = np.median(inkpix, axis=0)
paper = np.median(a[(g0 > 215)], axis=0)
stain = np.median(a[(g0 > 120) & (g0 < 190)], axis=0)
tea = np.median(a[(g0 > 190) & (g0 < 215)], axis=0)
pal = {"ink": hexc(ink), "ink_deep": hexc(ink_deep), "parchment": hexc(paper), "tea_light": hexc(tea), "sepia_stain": hexc(stain)}
print("palette", json.dumps(pal))
json.dump(pal, open(os.path.join(ROOT, "source", "sampled-palette.json"), "w"), indent=2)

def trace(m, out, color):
    png = "/tmp/_trace.png"; Image.fromarray(np.where(m, 0, 255).astype("uint8")).convert("RGB").save(png)
    vtracer.convert_image_to_svg_py(png, out, colormode="binary", mode="spline", filter_speckle=8, corner_threshold=60,
                                    length_threshold=4.0, splice_threshold=45, path_precision=1)
    s = open(out).read(); h, w = m.shape
    s = re.sub(r'<\?xml[^>]*>\s*', "", s)
    s = re.sub(r'<svg[^>]*>', f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Newquay Seamstress" viewBox="0 0 {w} {h}" width="{w//S}" height="{h//S}">', s, count=1)
    s = re.sub(r'fill="#(?:000000|000)"', f'fill="{color}"', s)
    s = re.sub(r'<path[^>]*fill="#(?:ffffff|fff)"[^>]*/>', "", s, flags=re.I)
    open(out, "w").write(s); return s
os.makedirs(os.path.join(ROOT, "assets/img"), exist_ok=True); os.makedirs(os.path.join(ROOT, "deliverables"), exist_ok=True)
out = os.path.join(ROOT, "assets/logo.svg"); s = trace(clean, out, pal["ink"])
open(os.path.join(ROOT, "assets/logo-light.svg"), "w").write(s.replace(pal["ink"], A.light))
shutil.copy(out, os.path.join(ROOT, "deliverables/newquay-seamstress-logo.svg"))
shutil.copy(os.path.join(ROOT, "assets/logo-light.svg"), os.path.join(ROOT, "deliverables/newquay-seamstress-logo-light.svg"))
# favicon: the sewing machine = components in the top part of the logo that are not long thin rules
fl, fn = ndimage.label(clean); fobjs = ndimage.find_objects(fl); Hc = clean.shape[0]
ids = []
for i, sl in enumerate(fobjs, 1):
    h_, w_ = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
    if sl[0].stop < Hc * 0.36 and not (w_ > 6 * h_): ids.append(i)
mm = np.isin(fl, ids); yy, xx = np.where(mm)
mach = mm[yy.min():yy.max() + 1, xx.min():xx.max() + 1]
side = int(max(mach.shape) * 1.08); fav = np.zeros((side, side), bool)
oy, ox = (side - mach.shape[0]) // 2, (side - mach.shape[1]) // 2; fav[oy:oy + mach.shape[0], ox:ox + mach.shape[1]] = mach
trace(fav, os.path.join(ROOT, "assets/img/favicon.svg"), pal["ink"])
rgba = np.zeros((side, side, 4), "uint8"); rgba[fav] = list(np.array(ink, int)) + [255]
Image.fromarray(rgba).resize((512, 512), Image.LANCZOS).save(os.path.join(ROOT, "assets/img/logo.png"))
print("wrote logo.svg, logo-light.svg, favicon.svg, logo.png, deliverables/")
