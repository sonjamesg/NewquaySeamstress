"""JSON-LD: one @graph per page with every node @id-linked:
business (LocalBusiness + ProfessionalService), its logo, Sylvia & Maxine (Person), WebSite,
the page (WebPage / AboutPage / ContactPage / FAQPage / CollectionPage), BreadcrumbList,
Service + OfferCatalog of guide-price Offers on service pages, and the full catalog on /prices/."""
import re
from .config import C, URL, CATS, PRICES, SERVICES, FAQS, AREAS, is_ph, low, page_url, ALL_FROM

BIZ, SITE, LOGO = URL + "/#business", URL + "/#website", URL + "/#logo"
CATALOG = URL + "/prices/#catalog"
GUIDE = "Guide price only. The final price is confirmed at drop-off or consultation, depending on the garment and the work needed."
def ref(i): return {"@id": i}
def person_id(p): return f'{URL}/about/#{p["short"].lower()}'
def svc_id(slug): return page_url(slug) + "#service"
def plain(html): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()

def area_served():
    out = []
    for a in AREAS:
        for n in a["name"].split(" & "):
            out.append({"@type": "Place", "name": f"{n}, Cornwall"})
    return out

def offer(it, svc_slug=None):
    spec = {"@type": "PriceSpecification", "priceCurrency": "GBP", "minPrice": low(it), "description": GUIDE}
    if "max" in it: spec["maxPrice"] = it["max"]
    o = {"@type": "Offer", "name": it["name"], "priceCurrency": "GBP", "priceSpecification": spec, "seller": ref(BIZ),
         "itemOffered": ref(svc_id(svc_slug)) if svc_slug else {"@type": "Service", "name": it["name"]}, "description": it.get("note") or GUIDE}
    return o

def cat_service(cid):
    for s in SERVICES:
        if cid in s["cats"]: return s["slug"]

def catalog_for(cids, cid_id=None):
    return [{"@type": "OfferCatalog", "@id": page_url("prices") + "#" + c, "name": CATS[c]["name"] + " (guide prices)",
             "itemListElement": [offer(i, cat_service(c)) for i in CATS[c]["items"]]} for c in cids]

def people():
    out = []
    for i, p in enumerate(C["people"]):
        n = {"@type": "Person", "@id": person_id(p), "name": p["name"], "givenName": p["name"].split()[0], "familyName": p["name"].split()[-1],
             "jobTitle": p["role"], "description": p["bio"], "worksFor": ref(BIZ), "url": URL + "/about/#" + p["short"].lower(),
             "hasOccupation": {"@type": "Occupation", "name": "Tailor" if i == 0 else "Seamstress", "experienceRequirements": f'{p["years"]} years',
                               "occupationLocation": {"@type": "City", "name": "Newquay"}}}
        if i == 0:
            n["knowsAbout"] = ["Tailoring", "Military uniform tailoring", "Clothing alterations", "Clothing repairs", "Dressmaking"]
            n["children"] = ref(person_id(C["people"][1]))
        else:
            n["parent"] = ref(person_id(C["people"][0])); n["knowsAbout"] = ["Clothing alterations", "Clothing repairs", "Sewing"]
        out.append(n)
    return out

def business():
    b = {"@type": ["LocalBusiness", "ProfessionalService"], "@id": BIZ, "name": C["business_name"],
         "alternateName": "Newquay Seamstress – alterations & repairs", "slogan": C["tagline"],
         "description": "Mother-and-daughter seamstress and tailoring service in Newquay, Cornwall: clothing alterations, trouser and jeans hems, zip replacement, repairs and mending, and curtain shortening. Led by Sylvia Tippett, a former RAF St Mawgan tailor with 50+ years' experience.",
         "url": URL + "/", "logo": ref(LOGO), "image": [URL + "/assets/img/og-newquay-seamstress.jpg", URL + "/assets/img/vintage-sewing-machine-newquay-seamstress-1024.webp"],
         "address": {"@type": "PostalAddress", "addressLocality": C["locality"], "addressRegion": C["region"], "addressCountry": C["country"]},
         "geo": {"@type": "GeoCoordinates", "latitude": C["geo"]["latitude"], "longitude": C["geo"]["longitude"]},
         "areaServed": area_served(), "priceRange": f"Guide prices from £{ALL_FROM}", "currenciesAccepted": "GBP",
         "founder": ref(person_id(C["people"][0])), "employee": [ref(person_id(p)) for p in C["people"]],
         "knowsAbout": ["Clothing alterations", "Trouser hemming", "Jeans hemming", "Zip replacement", "Clothing repairs", "Curtain shortening"],
         "hasOfferCatalog": ref(CATALOG), "makesOffer": [{"@type": "Offer", "itemOffered": ref(svc_id(s["slug"]))} for s in SERVICES]}
    if not is_ph(C["phone_e164"]): b["telephone"] = C.get("phone_schema", C["phone_e164"])
    if not is_ph(C["email"]): b["email"] = C["email"]
    b["contactPoint"] = {"@type": "ContactPoint", "contactType": "customer service", "telephone": b.get("telephone"), "email": b.get("email"), "areaServed": "GB", "availableLanguage": "en-GB"}
    if C["opening_hours_schema"]: b["openingHours"] = C["opening_hours_schema"]
    same = [C[k] for k in ("facebook_url", "instagram_url", "google_business_url") if not is_ph(C[k])]
    if same: b["sameAs"] = same
    return b

PAGE_TYPES = {"about": "AboutPage", "contact": "ContactPage", "faq": "FAQPage", "prices": "CollectionPage"}

def graph(p, img_url):
    url = page_url(p["slug"])
    crumbs = [("Home", URL + "/")]
    if p.get("service"): crumbs.append(("Services", URL + "/#services"))
    if p["slug"]: crumbs.append((p["crumb"], url))
    g = [{"@type": "WebSite", "@id": SITE, "url": URL + "/", "name": C["business_name"], "description": C["tagline"], "inLanguage": "en-GB", "publisher": ref(BIZ)},
         {"@type": "ImageObject", "@id": LOGO, "url": URL + "/assets/img/logo-512.png", "contentUrl": URL + "/assets/img/logo-512.png", "width": 512, "height": 512, "caption": C["business_name"] + " logo"},
         business(), *people()]
    page = {"@type": PAGE_TYPES.get(p["slug"], "WebPage"), "@id": url + "#webpage", "url": url, "name": p["title"], "description": p["desc"], "inLanguage": "en-GB",
            "isPartOf": ref(SITE), "about": ref(BIZ), "publisher": ref(BIZ), "breadcrumb": ref(url + "#breadcrumb"),
            "primaryImageOfPage": {"@type": "ImageObject", "url": img_url}, "dateModified": p["lastmod"]}
    g.append(page)
    g.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]})
    if p.get("service"):
        s = {"@type": "Service", "@id": url + "#service", "name": p["service"], "serviceType": p["service"], "provider": ref(BIZ),
             "areaServed": area_served(), "url": url, "description": p["desc"], "mainEntityOfPage": ref(url + "#webpage"),
             "hasOfferCatalog": {"@type": "OfferCatalog", "name": p["service"] + " guide prices", "itemListElement": catalog_for(p.get("cats", []))}}
        g.append(s); page["mainEntity"] = ref(s["@id"])
    if p["slug"] == "prices":
        g.append({"@type": "OfferCatalog", "@id": CATALOG, "name": "Alterations, repairs & curtains – guide prices", "url": url,
                  "description": GUIDE, "itemListElement": catalog_for([c["id"] for c in PRICES])})
        page["mainEntity"] = ref(CATALOG)
    if p["slug"] == "faq":
        page["mainEntity"] = [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a_text"]}} for f in FAQS]
    if p["slug"] == "about": page["mainEntity"] = [ref(person_id(x)) for x in C["people"]]
    if p["slug"] in ("contact", ""): page["mainEntity"] = ref(BIZ)
    return {"@context": "https://schema.org", "@graph": g}
