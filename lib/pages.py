"""Loads content/pages/*.html (a JSON front-matter block between --- lines, then the page body)
and expands {{shortcodes}} in the body. Shortcode syntax: {{name}} or {{name arg|arg2|...}}."""
import os, re, json
from .config import launderama_html, ROOT, C, E, FAQS, AREAS, SERVICES, PRICE_CARD, ALL_FROM, cat_from, file_date
from .components.contact import tel_link, mail_link, call_btn, email_btn, address_html
from .components.icons import button_svg
from .components.images import picture, logo_picture
from .components.price_table import GUIDE_NOTE, price_table, price_teaser, sidebar
from .components.nav import nav

PAGES_DIR = os.path.join(ROOT, "content", "pages")
ORDER = ["home", "trouser-jeans-alterations-newquay", "zip-replacement-newquay", "clothing-repairs-newquay", "curtain-alterations-newquay",
         "prices", "about", "areas-we-serve", "faq", "contact", "thank-you", "404"]

def load_pages():
    pages = []
    names = [f[:-5] for f in os.listdir(PAGES_DIR) if f.endswith(".html")]
    for n in sorted(names, key=lambda n: ORDER.index(n) if n in ORDER else 99):
        path = os.path.join(PAGES_DIR, n + ".html")
        raw = open(path, encoding="utf-8").read()
        m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
        if not m: raise SystemExit(f"{path}: missing front matter")
        p = json.loads(m.group(1)); p["body_src"] = m.group(2); p["file"] = path; p["name"] = n
        deps = [path] + ([os.path.join(ROOT, "data", "prices.json")] if "price" in p["body_src"] or p.get("cats") else []) \
               + ([os.path.join(ROOT, "data", "faqs.json")] if "{{faqs" in p["body_src"] else [])
        p["lastmod"] = max(file_date(d) for d in deps)
        pages.append(p)
    return pages

def faqs_html(n=None):
    out = "".join(f"<details><summary>{E(f['q'])}</summary><div><p>{f['a'].replace('{{launderama}}', launderama_html())}</p></div></details>" for f in FAQS[: n or len(FAQS)])
    return f'<div class="faq">{out}</div>'

def crumbs_html(p):
    if not p["slug"] or p.get("noindex"): return ""
    mid = '<li><a href="/#services">Services</a></li>' if p.get("service") else ""
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li>{mid}<li aria-current="page">{E(p["crumb"])}</li></ol></nav>'

def service_cards():
    cards = [(s["slug"] + "/", s["fabric"], s["card_title"], s["card_blurb"], f"Guide from £{min(cat_from(c) for c in s['cats'])}", s["pin"]) for s in SERVICES]
    cards.append(("prices/", PRICE_CARD["fabric"], PRICE_CARD["title"], PRICE_CARD["blurb"], "See guide prices →", PRICE_CARD["pin"]))
    return "".join(f'<a class="swatch reveal" style="--pin:{pin}" href="/{h}"><div class="fab {f} pinked-bottom" aria-hidden="true"></div><h3>{E(t)}</h3><p>{E(d)}</p><span class="price-tag">{E(pr)}</span></a>'
                   for h, f, t, d, pr, pin in cards)

def people_html():
    return "".join(f'<article class="person reveal" id="{x["short"].lower()}"><span class="years">{E(x["years"])}<small>years</small></span><h3>{E(x["name"])}</h3><p class="role">{E(x["role"])}</p><p>{E(x["bio"])}</p></article>' for x in C["people"])

def enquiry_form():
    fa = C["form_action"]
    opts = "".join(f"<option>{E(s['nav'])}</option>" for s in SERVICES) + "<option>Something else</option>"
    action = f' action="{E(fa)}" method="POST"' if fa else f' data-email="{E(C["email"])}"'
    hidden = (f'<input type="hidden" name="_subject" value="New enquiry – Newquay Seamstress website">'
              f'<input type="hidden" name="_template" value="table">'
              f'<input type="hidden" name="_next" value="{C["site_url"].rstrip("/")}/thank-you/">'
              f'<input type="text" name="_honey" class="honey" tabindex="-1" autocomplete="off" aria-hidden="true">') if "formsubmit.co" in fa else ""
    return (f'<form class="form price-card" id="enquiry"{action}>{hidden}<h2>Send an enquiry</h2>'
            '<label for="f-name">Your name</label><input id="f-name" type="text" name="name" autocomplete="name" required>'
            '<label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel">'
            '<label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required>'
            f'<label for="f-service">What do you need?</label><select id="f-service" name="service">{opts}</select>'
            '<label for="f-msg">Tell us about the garment</label><textarea id="f-msg" name="message" rows="5" required></textarea>'
            '<div class="btn-row"><button class="btn" type="submit">Send enquiry</button></div>'
            f'<p class="small">Your message goes straight to {E(C["contact_name"])} by email. Prices are guide prices, confirmed at drop-off.</p></form>')

def render(p, A, src=None):
    def sc(m):
        name, _, arg = m.group(1).partition(" ")
        a = arg.split("|") if arg else []
        f = {
            "phone": lambda: tel_link(), "email": lambda: mail_link(), "phone_display": lambda: E(C["phone_display"]),
            "tel": lambda: tel_link(a[0] if a else "", a[1] if len(a) > 1 else None),
            "mail": lambda: mail_link(a[0] if a else "", a[1] if len(a) > 1 else None),
            "call_btn": lambda: call_btn(arg or "btn"), "email_btn": lambda: email_btn(arg or "btn alt"),
            "address": address_html, "from": lambda: str(cat_from(arg) if arg else ALL_FROM),
            "launderama": launderama_html, "std": lambda: E(C["turnaround_standard"]), "exp": lambda: E(C["turnaround_express"]), "express": lambda: str(C["express_surcharge"]),
            "img": lambda: picture(A, a[0], a[1], eager=len(a) > 2 and a[2] == "eager", sizes="(max-width:900px) 92vw, 540px" if len(a) > 2 else "(max-width:900px) 92vw, 560px"),
            "button": lambda: button_svg(arg),
            "hero_logo": lambda: logo_picture(A, "logo-hero", (360, 720), C["business_name"] + " vintage sewing machine logo", "hero-logo", eager=True, sizes="(max-width:600px) 78vw, 360px"), "guide_note": lambda: GUIDE_NOTE,
            "price_table": lambda: price_table(arg), "price_teaser": price_teaser, "sidebar": lambda: sidebar(arg.split(",") if arg else []),
            "faqs": lambda: faqs_html(int(arg) if arg else None), "crumbs": lambda: crumbs_html(p),
            "service_cards": service_cards, "people": people_html, "enquiry_form": enquiry_form,
            "area_badges": lambda: "".join(f'<li>{E(x["name"])}</li>' for x in AREAS),
            "area_list": lambda: "".join(f'<li class="reveal"><h3>Seamstress near {E(x["name"])}</h3><p>{E(x["blurb"])}</p></li>' for x in AREAS),
        }.get(name)
        if not f: raise SystemExit(f'{p["file"]}: unknown shortcode {{{{{m.group(1)}}}}}')
        return f()
    body = p["body_src"] if src is None else src
    for _ in range(3):                       # shortcodes may contain shortcodes (e.g. FAQ answers with {{phone}})
        nb = re.sub(r"\{\{([a-z_]+(?: [^{}]*)?)\}\}", sc, body)
        if nb == body: break
        body = nb
    return body
