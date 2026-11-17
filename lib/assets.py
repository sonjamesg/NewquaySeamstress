"""Asset pipeline: CSS + JS bundling/minifying (esbuild), fonts, responsive AVIF/WebP images,
svgo-optimised logos, the Open Graph card and favicons. Expensive outputs are cached in .cache/."""
import os, re, shutil, hashlib, subprocess, io
from PIL import Image, ImageDraw, ImageFilter
from .config import ROOT, C

SRC = os.path.join(ROOT, "src")
CACHE = os.path.join(ROOT, ".cache")
BIN = os.path.join(ROOT, "node_modules", ".bin")
IMG_WIDTHS = (480, 768, 1024)
# CSS modules that render above the fold are inlined into every page; the rest load without blocking.
CRITICAL_CSS = ["00-fonts.css", "01-tokens.css", "02-base.css", "03-layout.css", "04-textures.css", "05-header.css",
                "06-buttons.css", "07-hero.css", "08-mobile-menu.css", "09-cta-bar.css", "10-price.css"]
LAZY_CSS = ["20-components.css", "30-animations.css"]

def sha(b): return hashlib.sha1(b).hexdigest()[:10]
def _tool(name):
    p = os.path.join(BIN, name)
    if not os.path.exists(p): raise SystemExit(f"Missing {name}: run `npm install` in {ROOT} first.")
    return p

def esbuild(args, stdin=None):
    r = subprocess.run([_tool("esbuild")] + args, input=stdin, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr)
    return r.stdout

class Assets:
    def __init__(self, out):
        self.out = out
        self.v = {}            # asset path -> version hash, for ?v= cache busting
        os.makedirs(CACHE, exist_ok=True)

    def url(self, rel):        # "/assets/x" with ?v=hash
        return f"/{rel}?v={self.v[rel]}" if rel in self.v else f"/{rel}"

    def _write(self, rel, data):
        p = os.path.join(self.out, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "wb").write(data); self.v[rel] = sha(data)

    # ---- fonts ----
    def fonts(self):
        for f in sorted(os.listdir(os.path.join(SRC, "fonts"))):
            self._write("assets/fonts/" + f, open(os.path.join(SRC, "fonts", f), "rb").read())

    # ---- CSS ----
    def _css(self, files):
        src = "\n".join(open(os.path.join(SRC, "css", f), encoding="utf-8").read() for f in files)
        src = re.sub(r"\{\{font:([\w.-]+)\}\}", lambda m: self.url("assets/fonts/" + m.group(1)), src)
        return esbuild(["--loader=css", "--minify", "--target=safari13,chrome90,firefox90"], stdin=src).strip()
    def css(self):
        self.critical_css = self._css(CRITICAL_CSS)
        lazy = self._css(LAZY_CSS).encode()
        self.lazy_css = f"assets/css/site.{sha(lazy)}.css"
        self._write(self.lazy_css, lazy)

    # ---- JS ----
    def js(self):
        tmp = os.path.join(CACHE, "site.js")
        esbuild([os.path.join(SRC, "js", "main.js"), "--bundle", "--minify", "--format=iife", "--target=es2017,safari13", "--outfile=" + tmp])
        data = open(tmp, "rb").read()
        self.js_file = f"assets/js/site.{sha(data)}.js"
        self._write(self.js_file, data)

    # ---- photos: AVIF + WebP at several widths ----
    def images(self):
        self.photos = {}
        for f in sorted(os.listdir(os.path.join(SRC, "img"))):
            if not f.endswith(".webp"): continue
            name = f[:-5]; src = os.path.join(SRC, "img", f); im = Image.open(src).convert("RGB")
            self.photos[name] = im.size
            key = sha(open(src, "rb").read())
            for w in IMG_WIDTHS:
                h = round(im.height * w / im.width)
                for fmt, q in (("avif", 52), ("webp", 76)):
                    rel = f"assets/img/{name}-{w}.{fmt}"
                    cached = os.path.join(CACHE, f"{name}-{w}-{key}.{fmt}")
                    if not os.path.exists(cached):
                        im.resize((w, h), Image.LANCZOS).save(cached, fmt.upper(), quality=q, **({"method": 6} if fmt == "webp" else {"speed": 4}))
                    self._write(rel, open(cached, "rb").read())

    # ---- logos ----
    def logos(self):
        import cairosvg
        for name in ("logo.svg", "logo-light.svg"):
            src = os.path.join(SRC, "img", name)
            cached = os.path.join(CACHE, sha(open(src, "rb").read()) + "-" + name)
            if not os.path.exists(cached):
                subprocess.run([_tool("svgo"), src, "-o", cached, "--multipass", "-p", "1"], check=True, capture_output=True)
            self._write("assets/img/" + name, open(cached, "rb").read())
        # raster logos for the header (light ink on walnut) and the hero (dark ink), 1x + 2x
        for name, svg, widths in (("logo-header", "logo-light.svg", (103, 206)), ("logo-hero", "logo.svg", (360, 720))):
            src = os.path.join(SRC, "img", svg)
            for w in widths:
                for fmt in ("avif", "webp"):
                    cached = os.path.join(CACHE, f"{name}-{w}-{sha(open(src,'rb').read())}.{fmt}")
                    if not os.path.exists(cached):
                        png = cairosvg.svg2png(url=src, output_width=w * 2 if w < 200 else w)
                        im = Image.open(io.BytesIO(png)).convert("RGBA")
                        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
                        im.save(cached, fmt.upper(), quality=80 if fmt == "webp" else 60, **({"method": 6} if fmt == "webp" else {}))
                    self._write(f"assets/img/{name}-{w}.{fmt}", open(cached, "rb").read())
        self._write("assets/img/logo-512.png", open(os.path.join(SRC, "img", "logo-512.png"), "rb").read())

    # ---- Open Graph card: the logo on parchment, 1200x630 ----
    def og(self):
        import cairosvg, random
        rel = "assets/img/og-newquay-seamstress.jpg"
        src = os.path.join(SRC, "img", "logo.svg")
        cached = os.path.join(CACHE, "og-" + sha(open(src, "rb").read() + b"v3") + ".jpg")
        if not os.path.exists(cached):
            W, H = 1200, 630
            bg = Image.new("RGB", (W, H), (240, 226, 199))
            rnd = random.Random(7); px = bg.load()
            for y in range(H):              # subtle linen weave + paper noise
                for x in range(W):
                    r, g, b = px[x, y]; n = rnd.randint(-7, 7) + (-4 if x % 3 == 0 else 0) + (-3 if y % 3 == 0 else 0)
                    px[x, y] = (r + n, g + n, b + n)
            stain = Image.new("L", (W, H), 0); d = ImageDraw.Draw(stain)
            for cx, cy, rr in ((160, 120, 260), (1050, 520, 300), (980, 90, 160)): d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=40)
            stain = stain.filter(ImageFilter.GaussianBlur(90))
            bg = Image.composite(Image.new("RGB", (W, H), (205, 170, 130)), bg, stain)
            d = ImageDraw.Draw(bg)
            for i in range(0, W - 60, 22):   # stitched border
                d.line((30 + i, 26, 30 + i + 12, 26), fill=(123, 45, 38), width=3); d.line((30 + i, H - 26, 30 + i + 12, H - 26), fill=(123, 45, 38), width=3)
            for i in range(0, H - 60, 22):
                d.line((26, 30 + i, 26, 30 + i + 12), fill=(123, 45, 38), width=3); d.line((W - 26, 30 + i, W - 26, 30 + i + 12), fill=(123, 45, 38), width=3)
            logo = Image.open(io.BytesIO(cairosvg.svg2png(url=src, output_height=470))).convert("RGBA")
            bg.paste(logo, ((W - logo.width) // 2, 40), logo)
            try:
                from PIL import ImageFont
                ft = ImageFont.truetype(os.path.join(CACHE, "special-elite.ttf"), 30)
            except Exception:
                ft = None
            if ft is None:
                from fontTools.ttLib import TTFont
                t = TTFont(os.path.join(SRC, "fonts", "special-elite.woff2")); t.flavor = None; t.save(os.path.join(CACHE, "special-elite.ttf"))
                from PIL import ImageFont
                ft = ImageFont.truetype(os.path.join(CACHE, "special-elite.ttf"), 30)
            txt = "ALTERATIONS · REPAIRS · CURTAINS  —  NEWQUAY, CORNWALL"
            tw = d.textlength(txt, font=ft); d.text(((W - tw) / 2, 540), txt, fill=(47, 29, 20), font=ft)
            bg.save(cached, "JPEG", quality=86, optimize=True, progressive=True)
        self._write(rel, open(cached, "rb").read())
        self.og_image = rel

    # ---- favicons + manifest icons ----
    def icons(self):
        for f in os.listdir(os.path.join(SRC, "icons")):
            if f.startswith("favicon-") and f.endswith(".png"): continue
            self._write("assets/img/" + f, open(os.path.join(SRC, "icons", f), "rb").read())
        shutil.copy(os.path.join(SRC, "icons", "favicon.ico"), os.path.join(self.out, "favicon.ico"))

    def run(self):
        self.fonts(); self.css(); self.js(); self.images(); self.logos(); self.og(); self.icons()
        return self
