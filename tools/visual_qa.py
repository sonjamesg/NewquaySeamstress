"""Full visual QA: full-length screenshots of every page at 1440/1280/430/390/360 in Chromium + WebKit, plus automated layout checks.
usage: python3 tools/visual_qa.py <base-url> <out-dir> [chromium|webkit ...]
WebKit on this box needs GIO_EXTRA_MODULES pointing at glib-networking's libgiognutls.so for HTTPS."""
import json, os, sys, re
from playwright.sync_api import sync_playwright
BASE, OUT = sys.argv[1].rstrip('/'), sys.argv[2]
ENGINES = sys.argv[3:] or ['chromium', 'webkit']
PAGES = {'home': '/', 'trousers': '/trouser-jeans-alterations-newquay/', 'zips': '/zip-replacement-newquay/', 'repairs': '/clothing-repairs-newquay/',
         'curtains': '/curtain-alterations-newquay/', 'prices': '/prices/', 'about': '/about/', 'areas': '/areas-we-serve/', 'faq': '/faq/',
         'contact': '/contact/', 'thank-you': '/thank-you/', '404': '/this-page-does-not-exist/'}
WIDTHS = {1440: 900, 1280: 800, 430: 932, 390: 844, 360: 780}
CHECK = r"""() => {
 const vw = document.documentElement.clientWidth, out = {vw, sw: document.documentElement.scrollWidth, wide: [], broken: [], ph: [], lane: [], small: [], bar: null};
 const vis = e => { const s = getComputedStyle(e), r = e.getBoundingClientRect(); return s.visibility !== 'hidden' && s.display !== 'none' && r.width > 0 && r.height > 0 && !e.closest('.sr-only,.mobile-menu,[hidden],.thread-layer'); };
 const name = e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/).join('.') : '');
 document.querySelectorAll('body *').forEach(e => { if (!vis(e)) return; const r = e.getBoundingClientRect(); if (r.right > vw + 1 && getComputedStyle(e).position !== 'fixed') out.wide.push(name(e) + ' ' + Math.round(r.right)); });
 document.querySelectorAll('img').forEach(i => { if (i.closest('.mobile-menu,[hidden]')) return; if (!i.complete || i.naturalWidth === 0) out.broken.push(i.currentSrc || i.src); });
 const txt = document.body.innerText; (txt.match(/.{0,30}(\[[^\]]*\]|\{\{|\}\}|\bTODO\b|\blorem\b|\bundefined\b|\bNaN\b|\bnull\b).{0,30}/gi) || []).forEach(m => out.ph.push(m));
 const lane = vw < 700 ? 22 : (((vw - Math.min(1180, vw)) / 2) > 80 ? Math.round(Math.max(24, Math.min(((vw - Math.min(1180, vw)) / 2) * .45, 72))) + 16 : 30);
 const hdr = document.querySelector('.site-header'), hb = hdr ? hdr.getBoundingClientRect().bottom + scrollY : 0;
 const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
 while (tw.nextNode()) { const n = tw.currentNode; if (!n.textContent.trim() || !n.parentElement || !vis(n.parentElement) || n.parentElement.closest('.site-header,.call-bar')) continue;
   const rg = document.createRange(); rg.selectNodeContents(n); for (const r of rg.getClientRects()) { if (r.width && r.left < lane && r.top + scrollY > hb) { out.lane.push(name(n.parentElement) + ' "' + n.textContent.trim().slice(0, 30) + '" L' + Math.round(r.left)); break; } } }
 if (vw < 700) document.querySelectorAll('a,button,input,select,textarea,summary').forEach(e => { if (!vis(e)) return; const r = e.getBoundingClientRect(); const inline = getComputedStyle(e).display === 'inline' && e.closest('p,li,td,dd,figcaption'); if (!inline && (r.height < 24 || r.width < 24)) out.small.push(name(e) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height)); });
 out.lane = [...new Set(out.lane)].slice(0, 8); out.wide = out.wide.slice(0, 8); out.small = [...new Set(out.small)].slice(0, 8); out.ph = [...new Set(out.ph)];
 return out; }"""
BAR = r"""() => { const b = document.querySelector('.call-bar'); if (!b || getComputedStyle(b).display === 'none') return null;
 const br = b.getBoundingClientRect(); const els = [...document.querySelectorAll('footer *')].filter(e => e.children.length === 0 && e.textContent.trim() && e.getBoundingClientRect().height);
 const last = els.length ? Math.max(...els.map(e => e.getBoundingClientRect().bottom)) : 0; return {barTop: Math.round(br.top), hidden: b.classList.contains('hide'), lastFooterText: Math.round(last), covered: !b.classList.contains('hide') && last > br.top + 1}; }"""
def settle(pg):
    pg.evaluate("document.fonts.ready")
    h = pg.evaluate("document.documentElement.scrollHeight")
    for y in range(0, h + 800, 500): pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(60)
    pg.wait_for_timeout(400)
os.makedirs(OUT, exist_ok=True); report = {}
with sync_playwright() as p:
    for eng in ENGINES:
        bt = getattr(p, eng); b = bt.launch(env={**os.environ, 'GIO_EXTRA_MODULES': '/tmp/gn/mods'}) if eng == 'webkit' else bt.launch()
        for w, h in WIDTHS.items():
            mob = w < 700
            ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2 if mob else 1, is_mobile=mob and eng == 'chromium', has_touch=mob)
            pg = ctx.new_page()
            for key, path in PAGES.items():
                pg.goto(BASE + path, wait_until='load'); settle(pg)
                bar = pg.evaluate(BAR)  # at the very bottom
                pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
                r = pg.evaluate(CHECK); r['bar'] = bar
                # full-length capture: draw the fixed call bar where it sits once scrolled to the end (bottom of the page)
                pg.add_style_tag(content="body{position:relative}.call-bar{position:absolute!important;bottom:0!important;transform:none!important}")
                pg.screenshot(path=f"{OUT}/{key}-{eng}-{w}.png", full_page=True)
                issues = {k: v for k, v in r.items() if k in ('wide', 'broken', 'ph', 'lane', 'small') and v}
                if r['sw'] > r['vw']: issues['hscroll'] = f"{r['sw']}>{r['vw']}"
                if bar and bar['covered']: issues['bar'] = bar
                report[f"{key}-{eng}-{w}"] = issues
                print(f"{key:9} {eng:8} {w:4} " + (json.dumps(issues) if issues else 'ok'), flush=True)
            if mob:
                pg.goto(BASE + '/', wait_until='load'); pg.evaluate("document.fonts.ready")
                pg.click('.nav-toggle'); pg.wait_for_timeout(900)
                pg.screenshot(path=f"{OUT}/menu-open-{eng}-{w}.png")
                m = pg.evaluate("""()=>{const d=document.documentElement;return {sw:d.scrollWidth,vw:d.clientWidth,exp:document.querySelector('.nav-toggle').getAttribute('aria-expanded'),focus:document.activeElement&&document.activeElement.className}}""")
                pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
                m['closed'] = pg.evaluate("document.querySelector('.nav-toggle').getAttribute('aria-expanded')")
                print(f"menu      {eng:8} {w:4} {m}", flush=True)
            ctx.close()
        b.close()
json.dump(report, open(f"{OUT}/qa-report-{'-'.join(ENGINES)}.json", 'w'), indent=1)
