# Newquay Seamstress website

A fast, static, SEO-focused site for a mother-and-daughter seamstress and tailoring business in Newquay, Cornwall.
It has a vintage haberdashery design (linen, tweed, denim and felt textures, stitched borders, pinking-shear edges and swing-tag buttons).

## Edit business details & prices
1. Open **`site.config.json`** and replace every value in `[square brackets]` (phone, email, address, postcode, hours, map and social links).
   Placeholders show on the page highlighted, and are left out of the structured data until filled.
   For hours, also fill `opening_hours_schema`, e.g. `["Mo-Fr 09:00-17:00","Sa 09:00-13:00"]`.
2. Prices are in the `prices` section (all shown as **guide prices**).
3. Copy and FAQs are in `content.py`.
4. Rebuild: `python3 build.py` → output in `docs/` (served by GitHub Pages). Check with `python3 selfcheck.py`.

## Custom domain
Set `site_url` in `site.config.json` to the new domain, rebuild, add a `docs/CNAME` file and configure the domain in the repo's Pages settings.
