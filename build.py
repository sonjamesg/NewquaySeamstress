#!/usr/bin/env python3
"""Builds the Newquay Seamstress website into ./docs (uploaded to Hostinger's public_html).

    python3 build.py            # build (minified)
    python3 build.py --pretty   # build without HTML minification (easier to read / validate)

Where things live (see README.md):
  data/       business details, prices, services, FAQs, areas (JSON)
  content/    one file per page: JSON front matter + HTML body with {{shortcodes}}
  lib/        the generator: components (header, footer, nav, mobile menu, CTA, price table, seam), schema, SEO head, outputs
  src/        CSS modules, JS modules, fonts, master images and icons
"""
import os, sys, shutil, re
from lib.config import ROOT, C, FAQS
from lib.assets import Assets
from lib.pages import load_pages, render
from lib.schema import graph, plain
from lib.head import head
from lib.outputs import write, md_name
from lib.components.header import header
from lib.components.footer import footer
from lib.components.cta import cta_band, call_bar

OUT = os.path.join(ROOT, "docs")
PRETTY = "--pretty" in sys.argv

def page_html(p, A, body):
    img = "vintage-sewing-machine-newquay-seamstress" if not p.get("img") else p["img"]
    ld = graph(p, f'{C["site_url"].rstrip("/")}/assets/img/{img}-1024.webp')
    md = None if p.get("noindex") else md_name(p)
    return (f'<!DOCTYPE html>\n<html lang="en-GB">\n<head>\n{head(p, A, ld, preload_hero=(p["slug"] == ""), md=md)}\n</head>\n<body>\n'
            f'{header(p["slug"], A)}\n<main id="main">\n{body}\n{"" if p.get("nocta") else cta_band()}\n</main>\n{footer()}\n{call_bar()}\n'
            f'<script src="/{A.js_file}" defer></script>\n</body>\n</html>\n')

def minify(h):
    import minify_html
    return minify_html.minify(h, minify_css=False, minify_js=False, keep_html_and_head_opening_tags=True, keep_closing_tags=True, keep_input_type_text_attr=True)

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    A = Assets(OUT).run()
    pages = load_pages()
    for f in FAQS: f["a_text"] = plain(render({"file": "data/faqs.json", "slug": "faq"}, A, f["a"]))
    rendered = {}
    for p in pages:
        body = render(p, A)
        rendered[p["name"]] = body
        html = page_html(p, A, body)
        if not PRETTY: html = minify(html)
        if p["slug"] == "404": path = os.path.join(OUT, "404.html")
        else:
            d = os.path.join(OUT, p["slug"]); os.makedirs(d, exist_ok=True); path = os.path.join(d, "index.html")
        open(path, "w", encoding="utf-8").write(html)
    write(OUT, pages, rendered)
    print(f"built {len(pages)} pages -> {OUT}  (critical CSS {len(A.critical_css)//1024} KB inline, lazy CSS /{A.lazy_css}, JS /{A.js_file})")

if __name__ == "__main__":
    build()
