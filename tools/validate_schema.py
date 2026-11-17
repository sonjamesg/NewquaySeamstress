#!/usr/bin/env python3
"""Validates the JSON-LD of every built page with the official Schema.org validator (validator.schema.org).
Usage: python3 tools/validate_schema.py   (after python3 build.py). Exits 1 on any error or warning."""
import time, glob, json, re, sys, urllib.request, urllib.parse
bad = 0
for f in sorted(glob.glob("docs/**/index.html", recursive=True)) + ["docs/404.html"]:
    s = open(f, encoding="utf-8").read()
    if 'http-equiv="refresh"' in s: continue
    data = urllib.parse.urlencode({"html": s}).encode()
    for attempt in range(6):
        try:
            r = urllib.request.urlopen(urllib.request.Request("https://validator.schema.org/validate", data=data), timeout=60).read().decode(); break
        except Exception as ex:
            time.sleep(4 + attempt * 4)
    else: raise SystemExit(f"validator unreachable for {f}")
    time.sleep(2)
    j = json.loads(r[r.index("{"):])
    errs = [(e.get("errorType"), e.get("args"), e.get("ownerSet")) for t in j.get("tripleGroups", []) for n in t.get("nodes", []) for e in n.get("errors", [])]
    types = sorted({t.get("type") for t in j.get("tripleGroups", [])})
    print(f"{f:55} errors={j.get('numObjects') and len(errs)} objects={j.get('numObjects')} totalErrors={j.get('totalNumErrors')} warnings={j.get('totalNumWarnings')} types={types}")
    for e in errs[:10]: print("   ", e)
    if j.get("totalNumErrors") or j.get("totalNumWarnings"): bad += 1
sys.exit(1 if bad else 0)
