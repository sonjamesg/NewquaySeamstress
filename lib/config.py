"""Loads every data file once and exposes small helpers shared by components."""
import json, os, html, datetime, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def _load(name): return json.load(open(os.path.join(ROOT, "data", name), encoding="utf-8"))

C = _load("site.config.json")                 # business details
PRICES = _load("prices.json")["categories"]   # guide price categories
_S = _load("services.json")
SERVICES = _S["services"]
PRICE_CARD = _S["price_list_card"]
PRICE_TEASER = _S["home_price_teaser"]
FAQS = _load("faqs.json")
AREAS = _load("areas.json")

URL = C["site_url"].rstrip("/")
TODAY = datetime.date.today().isoformat()
E = html.escape
CATS = {c["id"]: c for c in PRICES}

def is_ph(v): return isinstance(v, str) and v.strip().startswith("[")
def show(v): return "" if is_ph(v) else E(v)
def obf(s): return "".join(f"&#{ord(ch)};" for ch in s)   # light anti-scraper encoding; links still work without JS

def money(it):
    if "min" in it: return f"£{it['min']}–£{it['max']}"
    return ("From " if it.get("from") else "") + f"£{it['price']}"
def low(it): return it.get("min", it.get("price"))
def cat_from(cid): return min(low(i) for i in CATS[cid]["items"])
ALL_FROM = min(cat_from(c) for c in CATS)

def page_url(slug): return URL + "/" + (slug + "/" if slug else "")

def file_date(path):
    """Last-modified date for the sitemap: the file's last git commit, else its mtime."""
    try:
        d = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if d: return d
    except Exception: pass
    return datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()


def launderama_html():
    """Referral sentence linking to Newquay Launderama (data/site.config.json -> launderama)."""
    l = C["launderama"]
    return f'{E(l["before"])}<a href="{E(l["url"])}">{E(l["name"])}</a>{E(l["after"])}'
