"""Responsive <picture>: AVIF + WebP srcsets with explicit width/height (no layout shift); lazy unless eager."""
from ..config import E

SIZES = "(max-width:900px) 92vw, 560px"
def picture(A, name, alt, eager=False, sizes=SIZES, cls=""):
    w0, h0 = A.photos[name]
    def srcset(fmt): return ", ".join(f'{A.url(f"assets/img/{name}-{w}.{fmt}")} {w}w' for w in (480, 768, 1024))
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}"><source type="image/webp" srcset="{srcset("webp")}" sizes="{sizes}">'
            f'<img{c} src="{A.url(f"assets/img/{name}-1024.webp")}" width="{w0}" height="{h0}" alt="{E(alt)}" {load}></picture>')

def logo_picture(A, name, widths, alt, cls, eager=False, sizes=None):
    w1, w2 = widths
    from PIL import Image
    import os
    p = os.path.join(A.out, f"assets/img/{name}-{w1}.webp"); h1 = Image.open(p).height
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    if sizes:   # width descriptors let the browser pick the smallest file that is sharp enough
        ss = lambda f: f'{A.url(f"assets/img/{name}-{w1}.{f}")} {w1}w, {A.url(f"assets/img/{name}-{w2}.{f}")} {w2}w'
        sz = f' sizes="{sizes}"'
    else:
        ss = lambda f: f'{A.url(f"assets/img/{name}-{w1}.{f}")} 1x, {A.url(f"assets/img/{name}-{w2}.{f}")} 2x'
        sz = ""
    return (f'<picture><source type="image/avif" srcset="{ss("avif")}"{sz}><img class="{cls}" src="{A.url(f"assets/img/{name}-{w1}.webp")}" '
            f'srcset="{ss("webp")}"{sz} width="{w1}" height="{h1}" alt="{E(alt)}" {load}></picture>')
