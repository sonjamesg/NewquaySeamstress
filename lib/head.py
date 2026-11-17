"""<head>: title, description, canonical, hreflang, robots, Open Graph / Twitter, icons, preloads,
inlined critical CSS, non-blocking stylesheet, JSON-LD."""
import json
from .config import C, E, URL, page_url

OG_ALT = "Newquay Seamstress logo: a vintage sewing machine above the name, on aged parchment with a stitched border"

def head(p, A, ld, preload_hero=False, md=None):
    url = page_url(p["slug"])
    og = URL + "/" + A.og_image
    idx = not p.get("noindex")
    links = []
    if idx:
        links += [f'<link rel="canonical" href="{url}">', f'<link rel="alternate" hreflang="en-GB" href="{url}">', f'<link rel="alternate" hreflang="x-default" href="{url}">']
        if md: links.append(f'<link rel="alternate" type="text/markdown" href="{URL}/{md}" title="Markdown version">')
    pre = [f'<link rel="preload" href="{A.url("assets/fonts/playfair-display-700.woff2")}" as="font" type="font/woff2" crossorigin>',
           f'<link rel="preload" href="{A.url("assets/fonts/lora-var.woff2")}" as="font" type="font/woff2" crossorigin>']
    if preload_hero:
        n = "vintage-sewing-machine-newquay-seamstress"
        pre.append(f'<link rel="preload" as="image" type="image/avif" href="{A.url(f"assets/img/{n}-1024.avif")}" imagesrcset="' + ", ".join(f'{A.url(f"assets/img/{n}-{w}.avif")} {w}w' for w in (480, 768, 1024)) +
                   '" imagesizes="(max-width:900px) 92vw, 540px" fetchpriority="high">')
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(p["title"])}</title>
<meta name="description" content="{E(p["desc"])}">
<meta name="robots" content="{"index, follow, max-image-preview:large, max-snippet:-1" if idx else "noindex, follow"}">
{chr(10).join(links)}
<meta name="theme-color" content="#2f1d14">
<meta name="author" content="{E(C["business_name"])}">
<meta name="geo.region" content="GB-CON"><meta name="geo.placename" content="Newquay, Cornwall"><meta name="geo.position" content="{C["geo"]["latitude"]};{C["geo"]["longitude"]}"><meta name="ICBM" content="{C["geo"]["latitude"]}, {C["geo"]["longitude"]}">
<meta property="og:type" content="website"><meta property="og:locale" content="en_GB"><meta property="og:site_name" content="{E(C["business_name"])}">
<meta property="og:title" content="{E(p["title"])}"><meta property="og:description" content="{E(p["desc"])}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{og}"><meta property="og:image:secure_url" content="{og}"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{OG_ALT}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(p["title"])}"><meta name="twitter:description" content="{E(p["desc"])}"><meta name="twitter:image" content="{og}"><meta name="twitter:image:alt" content="{OG_ALT}">
<link rel="icon" href="{A.url("assets/img/favicon.ico")}" sizes="48x48"><link rel="icon" href="{A.url("assets/img/favicon.svg")}" type="image/svg+xml"><link rel="apple-touch-icon" href="{A.url("assets/img/apple-touch-icon.png")}"><link rel="manifest" href="/site.webmanifest">
{chr(10).join(pre)}
<style>{A.critical_css}</style>
<link rel="stylesheet" href="/{A.lazy_css}" media="print" id="lazy-css"><noscript><link rel="stylesheet" href="/{A.lazy_css}"></noscript>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}</script>'''
