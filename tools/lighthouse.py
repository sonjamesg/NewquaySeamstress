#!/usr/bin/env python3
"""Runs Lighthouse (mobile + desktop) on key pages and prints the four category scores.
Usage: python3 tools/lighthouse.py [base_url]   default https://newquayseamstress.com
Needs `npm install` (lighthouse) and a Chrome/Chromium (CHROME_PATH, or Playwright's Chromium)."""
import glob, json, os, subprocess, sys
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://newquayseamstress.com").rstrip("/")
PAGES = (os.environ.get("LH_PAGES") or "/,/trouser-jeans-alterations-newquay/,/prices/,/contact/").split(",")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
chrome = os.environ.get("CHROME_PATH") or (glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome")) or [None])[0]
os.makedirs(os.path.join(ROOT, ".cache", "lighthouse"), exist_ok=True)
rows = []
for form in ("mobile", "desktop"):
    for path in PAGES:
        out = os.path.join(ROOT, ".cache", "lighthouse", f"{form}{path.strip('/').replace('/', '_') or '_home'}.json")
        cmd = [os.path.join(ROOT, "node_modules", ".bin", "lighthouse"), BASE + path, "--quiet", "--output=json", f"--output-path={out}",
               "--chrome-flags=--headless=new --no-sandbox --disable-gpu", "--only-categories=performance,accessibility,best-practices,seo"]
        if form == "desktop": cmd.append("--preset=desktop")
        subprocess.run(cmd, env=dict(os.environ, CHROME_PATH=chrome or ""), capture_output=True, text=True, timeout=240)
        r = json.load(open(out))
        sc = {k: (round(v["score"] * 100) if v["score"] is not None else None) for k, v in r["categories"].items()}
        fails = [a["id"] for a in r["audits"].values() if a.get("score") is not None and a["score"] < 0.9 and a.get("scoreDisplayMode") in ("binary", "numeric", "metricSavings")]
        m = {k: r["audits"][k].get("displayValue", "n/a") for k in ("first-contentful-paint", "largest-contentful-paint", "total-blocking-time", "cumulative-layout-shift")}
        rows.append((form, path, sc, m, fails)); print(form, path, sc, m, "below 0.9:", fails, flush=True)
json.dump(rows, open(os.path.join(ROOT, ".cache", "lighthouse", "summary.json"), "w"), indent=1)
