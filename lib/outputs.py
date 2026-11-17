"""Site-wide files: sitemap.xml, robots.txt, llms.txt, llms-full.txt, per-page Markdown, .htaccess,
web manifest and redirect stubs for retired URLs."""
import os, re, json, urllib.parse
from .config import C, URL, TODAY, PRICES, SERVICES, FAQS, money, ALL_FROM, page_url

REDIRECTS = {"wedding-dress-alterations-cornwall": "about/", "suit-tailoring-newquay": "about/", "bespoke-dressmaking-newquay": "about/"}

def md_name(p): return (p["slug"] or "index") + ".md"

def to_markdown(html):
    from markdownify import markdownify
    from bs4 import BeautifulSoup
    s = BeautifulSoup(html, "html.parser")
    for t in s(["svg", "script", "style", "noscript", "form", "aside"]): t.decompose()
    for t in s.select("nav.crumbs, .sr-only:not(thead), .pattern-label, caption"): t.decompose()
    for t in s.select("span.note"): t.string = " (" + t.get_text() + ")"
    for t in s.select("h1 .script"): t.string = t.get_text() + " "
    for t in s.select(".reveal, .in"): pass
    for pic in s.find_all("picture"):
        img = pic.find("img"); pic.replace_with(img) if img else pic.decompose()
    for img in s.find_all("img"):
        src = img.get("src", "")
        img["src"] = urllib.parse.urljoin(URL + "/", src.split("?")[0])
    for a in s.find_all("a"):
        h = a.get("href", "")
        if h.startswith("/"): a["href"] = URL + h
    md = markdownify(str(s), heading_style="ATX", bullets="-", strip=["span", "small", "address", "figure", "figcaption", "details", "summary", "div", "section", "article", "header", "nav"] )
    md = "\n".join(l.rstrip() for l in md.split("\n"))
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return md

def write(out, pages, rendered):
    W = lambda rel, s: open(os.path.join(out, rel), "w", encoding="utf-8").write(s)
    idx = [p for p in pages if not p.get("noindex")]
    # sitemap with lastmod
    W("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      "".join(f'<url><loc>{page_url(p["slug"])}</loc><lastmod>{p["lastmod"]}</lastmod><priority>{p.get("prio", "0.8")}</priority></url>\n' for p in idx) + "</urlset>\n")
    W("robots.txt", f"# {C['business_name']} – {URL}\nUser-agent: *\nAllow: /\n\n"
      f"# LLM-friendly overview of this site (llmstxt.org): {URL}/llms.txt\n# Full plain-text content and guide prices: {URL}/llms-full.txt\n\n"
      f"Sitemap: {URL}/sitemap.xml\n")
    # markdown copies of every indexable page
    mds = {}
    for p in idx:
        body = to_markdown(rendered[p["name"]])
        h1 = re.search(r"^# .*$", body, re.M)
        head = (h1.group(0) + "\n\n") if h1 else ""
        if h1: body = body.replace(h1.group(0), "", 1).strip()
        md = re.sub(r"\n{3,}", "\n\n", f"{head}> {p['desc']}\n\nSource: {page_url(p['slug'])}\n\n" + body)
        mds[p["name"]] = md; W(md_name(p), md + "\n")
    # llms.txt (llmstxt.org: H1, blockquote summary, then H2 sections of links with notes)
    def li(p, note=None): return f"- [{p['crumb'] if p['slug'] else 'Home'}]({URL}/{md_name(p)}): {note or p['desc']}"
    by = {p["slug"]: p for p in idx}
    svc = [by[s["slug"]] for s in SERVICES]
    people = "; ".join(f"{x['name']} ({x['role']}, {x['years']} years)" for x in C["people"])
    llms = (f"# {C['business_name']}\n\n> {C['tagline']}. A mother-and-daughter seamstress business: {people}. "
            f"Sylvia was a tailor at RAF St Mawgan. Guide prices from £{ALL_FROM}; final prices are confirmed at drop-off. Phone {C['phone_display']}, email {C['email']}. "
            f"Based in {C['locality']}, {C['region']} (drop-off by arrangement).\n\n"
            "Every page below is also available as HTML at the same path without the .md suffix. Services are only those listed here: trouser and jeans alterations, zips and buttons, repairs and mending, curtains and soft furnishings.\n\n"
            "## Services\n\n" + "\n".join(li(p) for p in svc) +
            "\n\n## Prices & booking\n\n" + "\n".join(li(by[s]) for s in ("prices", "contact", "faq")) +
            "\n\n## About\n\n" + "\n".join(li(by[s]) for s in ("", "about", "areas-we-serve")) +
            f"\n\n## Optional\n\n- [Full content]({URL}/llms-full.txt): every page and the full guide price list as plain text\n- [Sitemap]({URL}/sitemap.xml): all indexable URLs\n")
    W("llms.txt", llms)
    prices = "\n\n".join(f"### {c['name']}\n\n" + "\n".join(f"- {i['name']}: {money(i)}" + (f" ({i['note']})" if i.get("note") else "") for i in c["items"]) for c in PRICES)
    full = (f"# {C['business_name']} – full site content\n\n> {C['tagline']}. Generated {TODAY} from {URL}/\n\n"
            f"## Guide prices (GBP)\n\nAll prices are guide prices. The final price is confirmed at drop-off or consultation, depending on the garment and the work needed. "
            f"Standard turnaround {C['turnaround_standard']}; express {C['turnaround_express']} for an extra £{C['express_surcharge']}. Clean items only.\n\n{prices}\n\n"
            "## Contact\n\n" + f"- Phone: {C['phone_display']} ({C['phone_e164']})\n- Email: {C['email']}\n- Location: {C['locality']}, {C['region']}. {C['dropoff_note']}\n\n" +
            "\n\n---\n\n".join(re.sub(r"^# ", "## ", mds[p["name"]], count=1).replace("\n## ", "\n### ").replace("\n### ", "\n### ") for p in idx) + "\n")
    W("llms-full.txt", full)
    # web manifest
    W("site.webmanifest", json.dumps({"name": C["business_name"], "short_name": "Seamstress", "description": C["tagline"], "start_url": "/", "scope": "/", "lang": "en-GB",
        "display": "standalone", "background_color": "#f4e9d3", "theme_color": "#2f1d14",
        "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}, indent=1))
    # retired URLs: real 301s in .htaccess, plus meta-refresh stubs for hosts without .htaccess
    for old, new in REDIRECTS.items():
        os.makedirs(os.path.join(out, old), exist_ok=True); tgt = f"{URL}/{new}"
        W(os.path.join(old, "index.html"), f'<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"><title>Page moved | {C["business_name"]}</title><meta name="robots" content="noindex, follow"><link rel="canonical" href="{tgt}"><meta http-equiv="refresh" content="0; url={tgt}"></head><body><p>This page has moved. <a href="{tgt}">Continue to {C["business_name"]}</a>.</p></body></html>\n')
    W(".htaccess", htaccess())

def htaccess():
    host = urllib.parse.urlparse(URL).netloc
    rd = "".join(f"RewriteRule ^{o}/?$ /{n} [R=301,L]\n" for o, n in REDIRECTS.items())
    csp = ("default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; "
           "form-action 'self' https://formsubmit.co; frame-ancestors 'self'; base-uri 'self'; object-src 'none'; upgrade-insecure-requests")
    return f"""# Generated by build.py – edit lib/outputs.py, not this file.
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html
AddDefaultCharset utf-8
AddType application/manifest+json .webmanifest
AddType text/markdown .md
AddType text/plain .txt
AddType image/avif .avif
AddType font/woff2 .woff2

RewriteEngine On
# https + bare domain
RewriteCond %{{HTTPS}} off [OR]
RewriteCond %{{HTTP_HOST}} ^www\\. [NC]
RewriteRule ^(.*)$ https://{host}/$1 [R=301,L]
# leftovers from the Hostinger placeholder site
RewriteRule ^(default\\.php|site\\.zip)$ - [R=404,L]
# retired service pages
{rd}
# ---- compression ----
<IfModule mod_brotli.c>
AddOutputFilterByType BROTLI_COMPRESS text/html text/plain text/css text/markdown application/javascript application/json application/ld+json image/svg+xml application/xml application/manifest+json
</IfModule>
<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/plain text/css text/markdown application/javascript application/json application/ld+json image/svg+xml application/xml application/manifest+json
</IfModule>

<IfModule mod_headers.c>
# ---- security ----
Header always set Strict-Transport-Security "max-age=31536000"
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
Header always set Cross-Origin-Opener-Policy "same-origin"
Header always set Content-Security-Policy "{csp}"
# ---- caching: every asset URL is content-hashed (file name or ?v=), so it can be cached for a year ----
<FilesMatch "\\.(css|js|svg|webp|avif|png|jpg|ico|woff2)$">
Header set Cache-Control "public, max-age=31536000, immutable"
</FilesMatch>
<FilesMatch "\\.(html|xml|txt|md|webmanifest)$">
Header set Cache-Control "public, max-age=0, must-revalidate"
</FilesMatch>
</IfModule>
"""
