#!/usr/bin/env python3
"""Static site generator for Newquay Seamstress.
Edit site.config.json (business details + guide prices) then run:  python3 build.py
Output goes to ./docs (served by GitHub Pages)."""
import json, os, shutil, html, datetime, urllib.parse
from content import PAGES, FAQS, AREAS

ROOT = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(ROOT, "site.config.json"), encoding="utf-8"))
OUT = os.path.join(ROOT, "docs")
URL = C["site_url"].rstrip("/")
TODAY = datetime.date.today().isoformat()
E = html.escape

def is_ph(v): return isinstance(v, str) and v.strip().startswith("[")
def show(v):  return "" if is_ph(v) else E(v)
def obf(s): return "".join(f"&#{ord(ch)};" for ch in s)      # light anti-scraper encoding; still works without JS
def tel_link(cls="", label=None):
    return f'<a class="{cls}" href="tel:{C["phone_e164"]}">{E(label or C["phone_display"]).replace(" ", "&nbsp;")}</a>'
def mail_link(cls="", label=None):
    return f'<a class="{cls}" href="{obf("mailto:" + C["email"])}">{label or obf(C["email"])}</a>'
def address_html():
    parts = [E(C["locality"]) + ", " + E(C["region"]), E(C["dropoff_note"])]
    return "<br>".join(parts)
def hours_known(): return any(not is_ph(h) for d, h in C["opening_hours_display"])

def money(it):
    if "min" in it: return f"£{it['min']}–£{it['max']}"
    return ("From " if it.get("from") else "") + f"£{it['price']}"
def low(it): return it.get("min", it.get("price"))

CATS = {c["id"]: c for c in C["prices"]}
def cat_from(cid): return min(low(i) for i in CATS[cid]["items"])
ALL_FROM = min(cat_from(c) for c in CATS)

def offer(it):
    spec = {"@type": "PriceSpecification", "priceCurrency": "GBP", "minPrice": low(it),
            "description": "Guide price only. Final price confirmed at drop-off or consultation, depending on the garment and the work needed."}
    if "max" in it: spec["maxPrice"] = it["max"]
    o = {"@type": "Offer", "name": it["name"], "priceCurrency": "GBP", "priceSpecification": spec,
         "itemOffered": {"@type": "Service", "name": it["name"]}, "seller": {"@id": URL + "/#business"}}
    if it.get("note"): o["description"] = it["note"]
    return o

GUIDE_NOTE = ('<p class="guide-note" role="note"><svg class="btn-icon" style="width:34px;height:34px" viewBox="0 0 60 60" aria-hidden="true">'
  '<circle cx="30" cy="30" r="27" fill="#a87a3d"/><circle cx="30" cy="30" r="21" fill="none" stroke="#2a170f" stroke-width="1.5" stroke-dasharray="3 3"/>'
  '<circle cx="24" cy="24" r="3" fill="#2a170f"/><circle cx="36" cy="24" r="3" fill="#2a170f"/><circle cx="24" cy="36" r="3" fill="#2a170f"/><circle cx="36" cy="36" r="3" fill="#2a170f"/></svg>'
  '<span><strong>Guide prices only.</strong> Every garment is different, so your final price is confirmed at drop-off or consultation, '
  'depending on the garment and the work needed. Nothing is started until you have agreed the price.</span></p>')

def price_table(cid, heading_tag="h2", link_id=True):
    c = CATS[cid]
    rows = "".join(
        f'<tr><th scope="row">{E(i["name"])}' + (f'<span class="note">{E(i["note"])}</span>' if i.get("note") else "") +
        f'</th><td class="p">{E(money(i))}</td></tr>' for i in c["items"])
    idattr = f' id="{cid}"' if link_id else ""
    return (f'<div class="price-card pinked-bottom reveal"{idattr}><{heading_tag}>{E(c["name"])} <small class="eyebrow">guide prices</small></{heading_tag}>'
            f'<table class="price-table"><caption class="sr-only">{E(c["name"])} guide prices</caption>'
            f'<thead class="sr-only"><tr><th scope="col">Service</th><th scope="col">Guide price</th></tr></thead><tbody>{rows}</tbody></table></div>')

# ---------- SVG ornaments ----------
SPOOL = ('<svg viewBox="0 0 64 64" aria-hidden="true"><rect x="10" y="6" width="44" height="8" rx="2" fill="#6e4a2f"/><rect x="10" y="50" width="44" height="8" rx="2" fill="#6e4a2f"/>'
         '<rect x="15" y="14" width="34" height="36" fill="#7b2d26"/><g stroke="#5c1d19" stroke-width="1.4">' +
         "".join(f'<line x1="15" y1="{y}" x2="49" y2="{y+2}"/>' for y in range(16, 50, 4)) +
         '</g><path d="M49 30 C 58 34, 60 44, 54 52" fill="none" stroke="#7b2d26" stroke-width="1.5"/></svg>')
MACHINE = ('<svg class="machine-svg" viewBox="0 0 220 130" aria-hidden="true"><g fill="#e6d4b4">'
  '<path d="M20 112h180v10H20z"/><path d="M38 108c0-40 4-62 30-70h86c22 0 30 10 30 26v44h-20V66c0-8-4-12-12-12H78c-14 4-18 20-18 54z"/>'
  '<rect x="150" y="30" width="44" height="12" rx="4"/><rect x="62" y="84" width="10" height="24"/><rect x="64" y="104" width="6" height="8" fill="#a87a3d"/>'
  '<circle cx="196" cy="70" r="18" fill="none" stroke="#e6d4b4" stroke-width="5"/><circle cx="196" cy="70" r="4"/></g>'
  '<path d="M90 47c10-6 30-6 40 0" stroke="#a87a3d" stroke-width="2" fill="none"/><path d="M98 52c6-3 18-3 24 0" stroke="#a87a3d" stroke-width="1.5" fill="none"/>'
  '<path d="M20 126h180" stroke="#a87a3d" stroke-width="2" stroke-dasharray="6 5"/></svg>')
LOGO = ('<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="22" fill="#a87a3d"/><circle cx="24" cy="24" r="18" fill="none" stroke="#3a2216" stroke-width="1.5" stroke-dasharray="3 2.5"/>'
        '<circle cx="18" cy="18" r="3.2" fill="#3a2216"/><circle cx="30" cy="18" r="3.2" fill="#3a2216"/><circle cx="18" cy="30" r="3.2" fill="#3a2216"/><circle cx="30" cy="30" r="3.2" fill="#3a2216"/>'
        '<path d="M18 18L30 30M30 18L18 30" stroke="#7b2d26" stroke-width="1.6"/></svg>')
def button_svg(color):
    return (f'<svg class="btn-icon" viewBox="0 0 60 60" aria-hidden="true"><circle cx="30" cy="30" r="27" fill="{color}"/><circle cx="30" cy="30" r="27" fill="none" stroke="rgba(0,0,0,.25)" stroke-width="2"/>'
            '<circle cx="30" cy="30" r="20" fill="none" stroke="rgba(255,255,255,.5)" stroke-width="1.5" stroke-dasharray="3 3"/>'
            '<circle cx="24" cy="24" r="3.2" fill="rgba(0,0,0,.45)"/><circle cx="36" cy="24" r="3.2" fill="rgba(0,0,0,.45)"/><circle cx="24" cy="36" r="3.2" fill="rgba(0,0,0,.45)"/><circle cx="36" cy="36" r="3.2" fill="rgba(0,0,0,.45)"/>'
            '<path class="xstitch" d="M24 24L36 36M36 24L24 36"/></svg>')

# ---------- Structured data ----------
def business():
    addr = {"@type": "PostalAddress", "addressLocality": C["locality"], "addressRegion": C["region"], "addressCountry": C["country"]}
    people = [{"@type": "Person", "@id": f'{URL}/about/#{p["name"].split()[0].lower()}', "name": p["name"], "jobTitle": p["role"],
               "description": p["bio"], "worksFor": {"@id": URL + "/#business"},
               "hasOccupation": {"@type": "Occupation", "name": "Tailor" if i == 0 else "Seamstress",
                                 "experienceRequirements": f'{p["years"]} years'} } for i, p in enumerate(C["people"])]
    people[1]["relatedTo"] = {"@id": people[0]["@id"]}
    people[0]["knowsAbout"] = ["Tailoring", "Military uniform tailoring", "Clothing alterations", "Clothing repairs"]
    catalog = [{"@type": "OfferCatalog", "name": c["name"] + " (guide prices)", "itemListElement": [offer(i) for i in c["items"]]} for c in C["prices"]]
    b = {"@type": ["ProfessionalService", "LocalBusiness"], "@id": URL + "/#business", "name": C["business_name"],
         "description": "Mother-and-daughter seamstress and tailoring service in Newquay, Cornwall: clothing alterations, trouser and jeans hems, zip replacement, repairs, curtain shortening.",
         "url": URL + "/", "image": URL + "/assets/img/og-image.jpg", "logo": URL + "/assets/img/logo.png",
         "address": addr, "priceRange": f"Guide prices from £{ALL_FROM}", "currenciesAccepted": "GBP",
         "areaServed": [{"@type": "City", "name": a[0]} for a in AREAS],
         "founder": {"@id": people[0]["@id"]}, "employee": people,
         "knowsAbout": ["Clothing alterations", "Trouser hemming", "Jeans hemming", "Zip replacement", "Clothing repairs", "Curtain shortening"],
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Alterations, repairs & tailoring", "itemListElement": catalog}}
    if not is_ph(C["phone_e164"]): b["telephone"] = C.get("phone_schema", C["phone_e164"])
    if not is_ph(C["email"]): b["email"] = C["email"]
    if C["opening_hours_schema"]: b["openingHours"] = C["opening_hours_schema"]
    same = [C[k] for k in ("facebook_url", "instagram_url", "google_business_url") if not is_ph(C[k])]
    if same: b["sameAs"] = same
    return b

def graph(p):
    url = URL + "/" + (p["slug"] + "/" if p["slug"] else "")
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": URL + "/"}]
    if p["slug"]: items.append({"@type": "ListItem", "position": 2, "name": p["crumb"], "item": url})
    g = [{"@type": "WebSite", "@id": URL + "/#website", "url": URL + "/", "name": C["business_name"], "inLanguage": "en-GB", "publisher": {"@id": URL + "/#business"}},
         business(),
         {"@type": p.get("pagetype", "WebPage"), "@id": url + "#webpage", "url": url, "name": p["title"], "description": p["desc"], "inLanguage": "en-GB",
          "isPartOf": {"@id": URL + "/#website"}, "about": {"@id": URL + "/#business"}, "breadcrumb": {"@id": url + "#breadcrumb"},
          "primaryImageOfPage": {"@type": "ImageObject", "url": URL + "/assets/img/" + p.get("img", "hero-machine") + "-1024.webp"}, "dateModified": TODAY},
         {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": items}]
    if p.get("service"):
        s = {"@type": "Service", "@id": url + "#service", "name": p["service"], "serviceType": p["service"], "provider": {"@id": URL + "/#business"},
             "areaServed": [{"@type": "City", "name": a[0]} for a in AREAS], "url": url, "description": p["desc"]}
        offers = [offer(i) for cid in p.get("cats", []) for i in CATS[cid]["items"]]
        if offers: s["offers"] = offers
        else: s["offers"] = {"@type": "Offer", "description": "Price on consultation", "itemOffered": {"@type": "Service", "name": p["service"]}}
        g.append(s)
    if p.get("faq_schema"):
        g.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a_text(a)}} for q, a in FAQS]})
    return {"@context": "https://schema.org", "@graph": g}

def a_text(a):
    import re
    return re.sub(r"<[^>]+>", "", fill(a))

def fill(s):
    """Replace {tokens} in content with config values."""
    rep = {"{phone}": tel_link(), "{email}": mail_link(), "{express}": str(C["express_surcharge"]), "{std}": C["turnaround_standard"],
           "{exp}": C["turnaround_express"], "{from}": str(ALL_FROM)}
    for k, v in rep.items(): s = s.replace(k, v)
    return s

# ---------- Layout ----------
NAV = [("", "Home"), ("services", "Services", [
          ("trouser-jeans-alterations-newquay", "Trouser & jeans alterations"), ("zip-replacement-newquay", "Zip & button replacement"),
          ("clothing-repairs-newquay", "Clothing repairs & mending"), ("curtain-alterations-newquay", "Curtain shortening & home")]),
       ("prices", "Guide prices"), ("about", "Our story"), ("areas-we-serve", "Areas"), ("faq", "FAQ"), ("contact", "Contact")]

HAS_LOGO = os.path.exists(os.path.join(ROOT, "assets", "logo-light.svg"))
def header(p, pre):
    def li(slug, label):
        cur = ' aria-current="page"' if slug == p["slug"] else ""
        return f'<li><a href="{pre}{slug + "/" if slug else ""}"{cur}>{E(label)}</a></li>'
    items = []
    for n in NAV:
        if len(n) == 3:
            items.append(f'<li class="has-sub"><a href="{pre}#services" aria-haspopup="true">Services ▾</a><ul>' + "".join(li(s, l) for s, l in n[2]) + "</ul></li>")
        else: items.append(li(n[0], n[1]))
    items.append(f'<li class="nav-call">{tel_link("", "☎ " + C["phone_display"])}</li>')
    if p["slug"] == "": items[1] = items[1].replace(f'href="{pre}#services"', 'href="#services"')
    brand = (f'<a class="brand" href="{pre or "./"}" aria-label="{E(C["business_name"])} home"><img class="brand-logo" src="{pre}assets/img/logo-header.webp" alt="{E(C["business_name"])} logo" width="103" height="62"></a>' if HAS_LOGO else
             f'<a class="brand" href="{pre or "./"}" aria-label="{E(C["business_name"])} home">{LOGO}<span><b>{E(C["business_name"])}</b><small>Alterations · Repairs · Tailoring</small></span></a>')
    # ---- vintage mobile menu panel ----
    def mli(slug, label, i):
        cur = ' aria-current="page"' if slug == p["slug"] else ""
        return f'<li class="mi" style="--i:{i}"><a class="tag" href="{pre}{slug + "/" if slug else ""}"{cur}>{E(label)}</a></li>'
    mitems, i = [], 0
    for n in NAV:
        if len(n) == 3:
            subs = "".join(f'<li><a href="{pre}{s}/"' + (' aria-current="page"' if s == p["slug"] else "") + f'>{E(l)}</a></li>' for s, l in n[2])
            mitems.append(f'<li class="mi" style="--i:{i}"><button type="button" class="tag acc" aria-expanded="false" aria-controls="m-services">Services<span class="chev" aria-hidden="true"></span></button>'
                          f'<ul class="msub" id="m-services" hidden>{subs}</ul></li>')
        else: mitems.append(mli(n[0], n[1], i))
        i += 1
    panel = (f'<div class="mnav" id="mnav" role="dialog" aria-modal="true" aria-label="Site menu" hidden><div class="mnav-inner">'
             f'<img class="mnav-logo" src="{pre}assets/logo.svg" alt="{E(C["business_name"])}" width="180" height="108" loading="lazy">'
             f'<nav aria-label="Mobile"><ul class="mlist">{"".join(mitems)}</ul></nav>'
             f'<div class="mnav-cta" style="--i:{i}">{tel_link("btn mustard", "☎ Call Maxine")}{mail_link("btn alt", "✉ Email")}</div>'
             f'<p class="mnav-note">{E(C["dropoff_note"])}</p></div></div>')
    toggle = ('<button type="button" class="nav-toggle" aria-expanded="false" aria-controls="mnav">'
              '<span class="sr-only">Menu</span><span class="tbtn" aria-hidden="true"><i class="h h1"></i><i class="h h2"></i><i class="h h3"></i><i class="h h4"></i>'
              '<i class="th t1"></i><i class="th t2"></i></span><span class="tlabel" aria-hidden="true">Menu</span></button>')
    return (f'<a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="nav-bar">'
            f'{brand}{toggle}'
            f'<nav class="main-nav" id="main-nav" aria-label="Main"><ul>{"".join(items)}</ul></nav></div></header>{panel}')

def footer(pre):
    hours = "".join(f"<li>{d}: {E(h)}</li>" for d, h in C["opening_hours_display"] if not is_ph(h))
    last = (f'<div><h2>Opening hours</h2><ul>{hours}</ul></div>' if hours_known() else
            f'<div><h2>Get in touch</h2><p>{E(C["dropoff_note"])}</p><p class="btn-stack">{tel_link("btn mustard", "☎ Call " + C["phone_display"])}{mail_link("btn alt", "✉ Email Maxine")}</p></div>')
    svc = "".join(f'<li><a href="{pre}{s}/">{E(l)}</a></li>' for s, l in NAV[1][2])
    soc = "".join(f'<li><a href="{E(C[k])}" rel="noopener">{lbl}</a></li>' for k, lbl in (("facebook_url", "Facebook"), ("instagram_url", "Instagram"), ("google_business_url", "Google reviews")) if not is_ph(C[k]))
    return (f'<footer class="site-footer"><div class="wrap"><div class="foot-grid"><div>{MACHINE}<p><strong>{E(C["business_name"])}</strong><br>'
            f'Mother-and-daughter seamstresses in Newquay, Cornwall. Sylvia brings 50+ years of tailoring, including her career as a tailor at RAF St Mawgan.</p>'
            f'<address>{address_html()}<br>☎ {tel_link()}<br>✉ {mail_link()}</address></div>'
            f'<div><h2>Services</h2><ul>{svc}</ul></div>'
            f'<div><h2>Explore</h2><ul><li><a href="{pre}prices/">Guide price list</a></li><li><a href="{pre}about/">Sylvia &amp; Maxine</a></li><li><a href="{pre}areas-we-serve/">Areas we serve</a></li><li><a href="{pre}faq/">FAQ</a></li><li><a href="{pre}contact/">Contact &amp; drop-off</a></li>{soc}</ul></div>'
            f'{last}</div>'
            f'<div class="foot-base"><span>© {datetime.date.today().year} {E(C["business_name"])} · Newquay, Cornwall</span><span>All prices shown are guide prices, confirmed at drop-off or consultation.</span></div></div></footer>'
            f'<aside class="call-bar" aria-label="Quick contact">{tel_link("btn mustard", "☎ Call Maxine")}{mail_link("btn alt", "✉ Email")}</aside>')

def cta(pre):
    return (f'<section class="cta-band felt stitched"><div class="wrap reveal"><p class="script">Bring it in…</p><h2>Ready to love your clothes again?</h2>'
            f'<p>Wash it, bring it in and we will pin it, price it and stitch it. Standard turnaround is {E(C["turnaround_standard"])}, with express {E(C["turnaround_express"])} for an extra £{C["express_surcharge"]}.</p>'
            f'<div class="btn-row">{tel_link("btn mustard", "☎ Call " + C["phone_display"])}{mail_link("btn alt", "✉ Email Maxine")}<a class="btn" href="{pre}contact/">Send an enquiry</a></div></div></section>')

def crumbs(p, pre):
    if not p["slug"]: return ""
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{pre}">Home</a></li><li aria-current="page">{E(p["crumb"])}</li></ol></nav>'

import hashlib
def _ver(rel):
    return hashlib.sha1(open(os.path.join(ROOT, rel), "rb").read()).hexdigest()[:10]
VER_CSS, VER_JS, VER_ICO = _ver("assets/css/style.css"), _ver("assets/js/main.js"), _ver("assets/img/favicon.svg")

def page_html(p):
    pre = (URL + "/") if p["slug"] == "404" else ("../" if p["slug"] else "")
    url = URL + "/" + (p["slug"] + "/" if p["slug"] else "")
    img = URL + "/assets/img/og-image.jpg"
    body = fill(p["body"](pre, globals()))
    if HAS_LOGO and not p["slug"]:
        body = body.replace('<p class="eyebrow">Seamstress &amp; tailor', f'<img class="hero-logo" src="{pre}assets/logo.svg" alt="{E(C["business_name"])} vintage sewing machine logo" width="360" height="216" fetchpriority="high"><p class="eyebrow">Seamstress &amp; tailor', 1)
    ld = json.dumps(graph(p), ensure_ascii=False, separators=(",", ":"))
    preload = f'<link rel="preload" as="image" href="{pre}assets/img/hero-machine-1024.webp" imagesrcset="{pre}assets/img/hero-machine-600.webp 600w, {pre}assets/img/hero-machine-1024.webp 1024w" imagesizes="(max-width:900px) 92vw, 540px">' if not p["slug"] else ""
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(p["title"])}</title>
<meta name="description" content="{E(p["desc"])}">
{"" if p.get("noindex") else f'<link rel="canonical" href="{url}">'}
<meta name="robots" content="{"noindex" if p.get("noindex") else "index, follow, max-image-preview:large"}">
<meta name="geo.region" content="GB-CON"><meta name="geo.placename" content="Newquay">
<meta name="theme-color" content="#3a2216">
<meta property="og:type" content="website"><meta property="og:locale" content="en_GB"><meta property="og:site_name" content="{E(C["business_name"])}">
<meta property="og:title" content="{E(p["title"])}"><meta property="og:description" content="{E(p["desc"])}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Antique black and gold sewing machine with thread spools, tape measure and tweed swatches">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(p["title"])}"><meta name="twitter:description" content="{E(p["desc"])}"><meta name="twitter:image" content="{img}">
<link rel="icon" href="{pre}assets/img/favicon.ico?v={VER_ICO}" sizes="48x48"><link rel="icon" href="{pre}assets/img/favicon.svg?v={VER_ICO}" type="image/svg+xml"><link rel="apple-touch-icon" href="{pre}assets/img/apple-touch-icon.png?v={VER_ICO}"><link rel="manifest" href="{pre}site.webmanifest?v={VER_ICO}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Pinyon+Script&family=Playfair+Display:ital,wght@0,700;1,700&family=Special+Elite&display=swap">
{preload}
<link rel="stylesheet" href="{pre}assets/css/style.css?v={VER_CSS}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
{header(p, pre)}
<main id="main">
{body}
{"" if p.get("nocta") else cta(pre)}
</main>
{footer(pre)}
<script src="{pre}assets/js/main.js?v={VER_JS}" defer></script>
</body>
</html>
'''

REDIRECTS = {"wedding-dress-alterations-cornwall": "about/", "suit-tailoring-newquay": "about/", "bespoke-dressmaking-newquay": "about/"}

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    for p in PAGES:
        d = os.path.join(OUT, p["slug"]) if p["slug"] and p["slug"] != "404" else OUT
        os.makedirs(d, exist_ok=True)
        fn = "404.html" if p["slug"] == "404" else "index.html"
        if p["slug"] == "404": p = dict(p, slug="404")
        open(os.path.join(d, fn), "w", encoding="utf-8").write(page_html(p))
    # retired URLs (services no longer offered) -> permanent client-side redirect, noindex, excluded from sitemap
    for old, new in REDIRECTS.items():
        os.makedirs(os.path.join(OUT, old), exist_ok=True)
        tgt = f"{URL}/{new}"
        open(os.path.join(OUT, old, "index.html"), "w", encoding="utf-8").write(
            f'<!DOCTYPE html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n<title>Page moved | {E(C["business_name"])}</title>\n'
            f'<meta name="robots" content="noindex, follow">\n<link rel="canonical" href="{tgt}">\n<meta http-equiv="refresh" content="0; url={tgt}">\n'
            f'<script>location.replace("{tgt}")</script>\n</head>\n<body>\n<p>This page has moved. <a href="{tgt}">Continue to {E(C["business_name"])}</a>.</p>\n</body>\n</html>\n')
    urls = "".join(f'<url><loc>{URL}/{p["slug"] + "/" if p["slug"] else ""}</loc><lastmod>{TODAY}</lastmod><priority>{p.get("prio", "0.8")}</priority></url>'
                   for p in PAGES if not p.get("noindex"))
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {URL}/sitemap.xml\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    host = urllib.parse.urlparse(URL).netloc
    if not host.endswith("github.io"):   # Apache (Hostinger): force https + bare domain, real 301s for retired pages, caching
        rd = "".join(f"RewriteRule ^{o}/?$ /{n} [R=301,L]\n" for o, n in REDIRECTS.items())
        hd = host.replace(".", "\\.")
        open(os.path.join(OUT, ".htaccess"), "w").write(f"""Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html
RewriteEngine On
RewriteCond %{{HTTPS}} off [OR]
RewriteCond %{{HTTP_HOST}} ^www\\. [NC]
RewriteRule ^(.*)$ https://{host}/$1 [R=301,L]
RewriteRule ^(default\\.php|site\\.zip)$ - [R=404,L]
{rd}
<IfModule mod_headers.c>
Header always set Strict-Transport-Security "max-age=31536000"
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
<FilesMatch "\\.(css|js|svg|webp|png|jpg|ico|woff2)$">
Header set Cache-Control "public, max-age=31536000, immutable"
</FilesMatch>
<FilesMatch "\\.(html|xml|txt|webmanifest)$">
Header set Cache-Control "public, max-age=600"
</FilesMatch>
</IfModule>
<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/xml text/plain application/manifest+json
</IfModule>
AddType application/manifest+json .webmanifest
""")
    base = urllib.parse.urlparse(URL).path.rstrip("/") + "/"
    open(os.path.join(OUT, "site.webmanifest"), "w").write(json.dumps({"name": C["business_name"], "short_name": "Seamstress", "start_url": base, "scope": base,
        "display": "standalone", "background_color": "#f4e9d3", "theme_color": "#2f1d14",
        "icons": [{"src": base + "assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": base + "assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1))
    shutil.copy(os.path.join(ROOT, "assets/img/favicon.ico"), os.path.join(OUT, "favicon.ico"))
    print("built", len(PAGES), "pages ->", OUT)

if __name__ == "__main__":
    build()
