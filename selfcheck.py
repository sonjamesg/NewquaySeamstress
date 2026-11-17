"""Self-check: JSON-LD parses, one <h1>, unique titles/descriptions, internal links resolve, every page linked, alt text on images."""
import html, glob, json, os, re, sys, urllib.parse
C = json.load(open("site.config.json")); URL = C["site_url"].rstrip("/")
pages = sorted(glob.glob("docs/**/*.html", recursive=True)); redirects = []; bad = 0; linked = set(); titles = {}; descs = {}
for f in pages:
    s = open(f, encoding="utf-8").read()
    if 'http-equiv="refresh"' in s: redirects.append(f); continue
    for blob in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            d = json.loads(blob); types = [n["@type"] for n in d["@graph"]]
        except Exception as e: print("BAD JSON-LD", f, e); bad += 1
    h1 = len(re.findall(r"<h1[ >]", s))
    if h1 != 1 and "404" not in f: print("H1 count", h1, f); bad += 1
    t = re.search(r"<title>(.*?)</title>", s).group(1); d = re.search(r'name="description" content="(.*?)"', s).group(1)
    titles.setdefault(t, []).append(f); descs.setdefault(d, []).append(f)
    for img in re.findall(r"<img[^>]*>", s):
        if not re.search(r'alt="[^"]+"', img): print("missing alt", f); bad += 1
    base = os.path.dirname(f)
    for href in [html.unescape(h) for h in re.findall(r'href="([^"]+)"', s)]:
        if href.startswith(("http", "mailto:", "tel:", "#")) and not href.startswith(URL): continue
        h = href.split("#")[0].split("?")[0]
        p = h.replace(URL + "/", "docs/") if h.startswith(URL) else os.path.normpath(os.path.join(base, h))
        p = urllib.parse.unquote(p)
        target = os.path.join(p, "index.html") if os.path.isdir(p) else p
        if not os.path.exists(target): print("BROKEN", f, href); bad += 1
        else: linked.add(os.path.normpath(target))
for k, v in list(titles.items()) + list(descs.items()):
    if len(v) > 1: print("DUPLICATE", k, v); bad += 1
for f in pages:
    if f in redirects: continue
    if os.path.normpath(f) not in linked and "404" not in f and "thank-you" not in f: print("ORPHAN", f); bad += 1
sm = open("docs/sitemap.xml").read(); print("sitemap urls:", sm.count("<loc>"))
for r in ("wedding-dress-alterations-cornwall", "suit-tailoring-newquay", "bespoke-dressmaking-newquay"):
    if r in sm: print("RETIRED URL IN SITEMAP", r); bad += 1
print("pages:", len(pages) - len(redirects), "redirect stubs:", len(redirects), "problems:", bad); sys.exit(1 if bad else 0)
