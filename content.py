import html as _h
"""Page copy for Newquay Seamstress. Tokens like {phone} are filled from site.config.json by build.py."""

AREAS = [
    ("Newquay", "Our home town. Drop-offs from Pentire, Porth, Lusty Glaze, Trenance, Tretherras and the town centre."),
    ("St Columb Major", "A short drive inland along the A39 corridor, ideal for hems and zips on the way into town."),
    ("St Mawgan & Mawgan Porth", "Close to RAF St Mawgan, where Sylvia spent her career as a military tailor."),
    ("Crantock", "Just across the Gannel. Popular for jeans hems and curtain shortening for holiday lets."),
    ("St Newlyn East", "A few miles south of Newquay, an easy hop for repairs and alterations."),
    ("Quintrell Downs", "On the doorstep. Bring trousers, jeans and coats with broken zips."),
    ("Perranporth", "Wetsuit-and-jeans country. Zip replacement and seam repairs are our everyday work."),
    ("St Austell", "Worth the drive in from mid Cornwall for jeans hems, zips and curtain shortening."),
    ("Truro", "Cornwall's city. Customers bring trousers, coats and curtains to us for alterations and repairs."),
    ("Padstow & Wadebridge", "Up the coast. Holiday-let curtains and cushion zips are a speciality worth the trip."),
    ("Indian Queens & St Dennis", "A quick run down the A30 for everyday alterations and mending."),
    ("Holywell Bay & Cubert", "Small jobs welcome, from a single button to a full set of trouser hems."),
]

def img(pre, name, alt, cls="", eager=False, sizes="(max-width:900px) 92vw, 560px"):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="{pre}assets/img/{name}-1024.webp" srcset="{pre}assets/img/{name}-600.webp 600w, {pre}assets/img/{name}-1024.webp 1024w" '
            f'sizes="{sizes}" width="1024" height="768" alt="{alt}" {load}>')

FAQS = [
    ("How much do alterations cost in Newquay?",
     "Our <a href=\"../prices/\">guide prices</a> start from £3 for a button and £10 for a standard jeans hem. Trouser hems are a guide £12, zip replacements from £15 and curtain shortening from £20 per pair. These are guide prices only: the final price is confirmed at drop-off or consultation, depending on the garment and the work needed."),
    ("How long do alterations take?",
     "Standard turnaround is {std}. If you need it sooner, our express service turns most jobs around in {exp} for an extra £{express}."),
    ("Do my clothes or curtains need to be washed first?",
     "Yes please. We can only work on clean items, so garments and curtains must be freshly washed before drop-off. It keeps the workroom (and everyone else's clothes) clean and means hems are measured on fabric that has already shrunk."),
    ("Can you pin my hem when I drop off?",
     "Yes. We are happy to pin hems at drop-off, so bring the shoes you will wear with trousers or a dress. Alternatively you can pin or measure your preferred length at home and we will work to that."),
    ("Can you shorten jeans and keep the original hem?",
     "Yes. A jeans hem keeping the original factory hem (so the worn, faded edge stays) has a guide price of £15. A standard jeans hem is a guide £10."),
    ("Do zip replacements include the zip?",
     "Trouser and skirt zip replacement (guide £15) includes a standard zip, and jeans zip replacement (guide £18) includes a heavy-duty metal zip. Coat and jacket zips start from £25 plus the cost of the specialist zip, as these vary in length and type."),
    ("Is there a minimum charge?",
     "Yes, the minimum repair charge is £8. Buttons are the exception: replacing or restitching a button is a guide £3, or 3 for £7."),
    ("Do you shorten curtains, including lined and blackout curtains?",
     "Yes. Shortening unlined curtains starts from £20 per pair and lined or blackout curtains from £32 per pair. We also replace cushion cover zips (guide £12)."),
    ("Who will be working on my clothes?",
     "Sylvia Pauline Tippett, a tailor with more than 50 years' experience who spent her career as a tailor at RAF St Mawgan, and her daughter Maxine Jennings, who has worked alongside her for over three years. <a href=\"../about/\">Meet them</a>."),
    ("Where are you and which areas do you cover?",
     "We are based in Newquay ({address}, {postcode}). Customers bring work to us from across Cornwall, including St Columb, Crantock, St Newlyn East, Perranporth, St Austell and Truro. <a href=\"../areas-we-serve/\">See all areas</a>."),
    ("How do I book?",
     "Call us on {phone}, email {email} or use the <a href=\"../contact/\">contact form</a> to arrange a drop-off."),
]

def faq_block(items, pre):
    out = []
    for q, a in items:
        a = a.replace('href="../', f'href="{pre}')
        out.append(f"<details><summary>{q}</summary><div><p>{a}</p></div></details>")
    return '<div class="faq">' + "".join(out) + "</div>"

def side(pre, g, cats=None, consult=False):
    C = g["C"]
    parts = []
    if cats:
        rows = "".join(f'<li>{g["E"](i["name"])} — <strong>{g["money"](i)}</strong></li>' for c in cats for i in g["CATS"][c]["items"][:6])
        parts.append(f'<div class="side-card"><h2>Guide prices</h2><ul>{rows}</ul><p style="margin:.8rem 0 0;font-size:.88rem">Guide prices only. Final price confirmed at drop-off.</p><p style="margin:.5rem 0 0"><a href="{pre}prices/">Full guide price list →</a></p></div>')
    if consult:
        parts.append(f'<div class="side-card"><h2>Price on consultation</h2><p>Every gown and suit is different, so we price this work after a fitting and a proper look at the garment or design.</p><p><a href="{pre}contact/">Book a consultation →</a></p></div>')
    parts.append(f'<div class="side-card rose"><h2>Good to know</h2><ul><li>Clean, freshly washed items only</li><li>Hems pinned at drop-off, or pin at home</li><li>Standard {C["turnaround_standard"]}</li><li>Express {C["turnaround_express"]} +£{C["express_surcharge"]}</li></ul><p style="margin:.8rem 0 0">☎ {g["show"](C["phone_display"])}</p></div>')
    others = "".join(f'<li><a href="{pre}{s}/">{g["E"](l)}</a></li>' for s, l in g["NAV"][1][2])
    parts.append(f'<div class="side-card"><h2>All services</h2><ul>{others}</ul></div>')
    return '<aside class="sidebar">' + "".join(parts) + "</aside>"

def hero(p, pre, eyebrow, lede, consult=False):
    book = "Book a consultation" if consult else "Book a drop-off"
    return (f'<header class="page-hero"><div class="wrap">{{CRUMBS}}<p class="eyebrow">{eyebrow}</p><h1>{p["h1"]}</h1><p class="lede">{lede}</p>'
            f'<div class="btn-row"><a class="btn" href="{pre}contact/">{book}</a><a class="btn alt" href="{pre}prices/">Guide prices</a></div></div></header>')

def svc_page(p, eyebrow, lede, prose, cats=None, consult=False):
    def body(pre, g):
        h = hero(p, pre, eyebrow, lede, consult).replace("{CRUMBS}", g["crumbs"](p, pre))
        tables = "".join(g["price_table"](c, "h2") for c in (cats or []))
        extra = (f'<h2>Guide prices for this service</h2>{g["GUIDE_NOTE"]}{tables}' if cats else "")
        return (h + f'<section class="linen snip-host"><!--SNIP--><div class="wrap content"><article class="prose">{prose(pre, g)}{extra}</article>{side(pre, g, cats, consult)}</div></section>')
    return body

# ---------------- HOME ----------------
def home(pre, g):
    C, E = g["C"], g["E"]
    sw = [
        ("trouser-jeans-alterations-newquay", "f-denim", "Trouser &amp; jeans alterations", "Hems, original-hem jeans, turn-ups, waists taken in and legs tapered.", f"Guide from £{g['cat_from']('trousers')}", "#8a5c36"),
        ("zip-replacement-newquay", "f-mustard", "Zips &amp; buttons", "Trouser, skirt, jeans and coat zips, buttons restitched and new buttonholes.", "Guide from £3", "#7b2d26"),
        ("clothing-repairs-newquay", "f-tweed", "Repairs &amp; mending", "Split seams, small tears, patches and pocket bags, mended neatly.", f"Guide from £{g['cat_from']('repairs')}", "#a87a3d"),
        ("curtain-alterations-newquay", "f-velvet", "Curtains &amp; home", "Unlined, lined and blackout curtains shortened, cushion zips replaced.", f"Guide from £{g['cat_from']('curtains')}", "#7b2d26"),
        ("prices", "f-paper", "The full price list", "Every guide price in one place, plus express and drop-off notes.", "See guide prices →", "#8a5c36"),
    ]
    cards = "".join(f'<a class="swatch reveal" style="--pin:{pin}" href="{pre}{s}/"><div class="fab {f} pinked-bottom" aria-hidden="true"></div><h3>{t}</h3><p>{d}</p><span class="price-tag">{pr}</span></a>' for s, f, t, d, pr, pin in sw)
    top = [("trousers", 0), ("trousers", 2), ("zips", 0), ("zips", 1), ("repairs", 1), ("curtains", 0)]
    teaser = "".join(f'<tr><th scope="row">{E(g["CATS"][c]["items"][i]["name"])}</th><td class="p">{g["money"](g["CATS"][c]["items"][i])}</td></tr>' for c, i in top)
    faqs = faq_block(FAQS[:4], pre)
    s, m = C["people"]
    return f'''
<section class="hero"><span class="pattern-label" style="top:18px;left:4%">Pattern piece no. 1 · cut 2 · place on fold</span>
<div class="wrap hero-grid">
<div class="reveal in">
<p class="eyebrow">Seamstress &amp; tailor · Newquay, Cornwall</p>
<h1><span class="script">Mended with care,</span>Clothing Alterations &amp; Repairs in Newquay</h1>
<p class="lede">A mother-and-daughter sewing room led by <strong>Sylvia Tippett</strong>, a tailor with <strong>50+ years' experience</strong> who spent her career as a <strong>tailor at RAF St Mawgan</strong>, and her daughter <strong>Maxine</strong>. Hems, zips, repairs, mending and curtains, finished to the standard of a military tailor.</p>
<div class="btn-row"><a class="btn" href="{pre}contact/">Book a drop-off</a><a class="btn alt" href="{pre}prices/">Guide prices from £{{from}}</a></div>
<ul class="badges"><li>✂ 50+ years' tailoring</li><li>✪ Ex-RAF St Mawgan tailor</li><li>♥ Mother &amp; daughter</li><li>⏱ Express {E(C["turnaround_express"])}</li></ul>
</div>
<figure class="hero-photo reveal in">{img(pre, "hero-machine", "Antique black and gold Singer-style sewing machine on a walnut table with thread spools, tape measure, pincushion and tweed swatches", eager=True)}</figure>
</div>
<svg class="hero-stitch draw" viewBox="0 0 1200 40" preserveAspectRatio="none" aria-hidden="true"><path d="M0 20 Q 150 0 300 20 T 600 20 T 900 20 T 1200 20"/></svg>
</section>

<section class="tweed stitched" aria-labelledby="heritage-h"><div class="wrap split">
<figure class="polaroid reveal">{img(pre, "heritage-tailor", "Vintage tailor's workshop with a green wool military-style jacket on a dress form, tape measure and cast-iron sewing machine")}<figcaption>Half a century of tailoring</figcaption></figure>
<div class="reveal"><p class="eyebrow">Our heritage</p><h2 id="heritage-h">Military-standard tailoring, passed from mother to daughter</h2>
<p>For more than 50 years Sylvia worked as a tailor for the military at <strong>RAF St Mawgan</strong>, just up the road from Newquay. Uniforms leave no room for "near enough": every hem level, every seam straight, every button where it should be. That is the standard she brings to your jeans, your coats and your curtains.</p>
<p>Over her career Sylvia has also made ball gowns, suits and wedding dresses, so she knows exactly how garments are put together. Today she works with her daughter <strong>Maxine Jennings</strong>, who has spent over three years at her side learning those skills, so the craft carries on in Newquay.</p>
<ul class="stat-row"><li class="stat"><b>{E(s["years"])}</b><span>years Sylvia has tailored</span></li><li class="stat"><b>RAF</b><span>St Mawgan tailor</span></li><li class="stat"><b>{E(m["years"])}</b><span>years Maxine at her side</span></li></ul>
<a class="btn mustard" href="{pre}about/">Read our story</a></div></div></section>

<section id="services" class="snip-host" aria-labelledby="svc-h"><!--SNIP--><div class="wrap">
<div class="section-head reveal"><p class="script">Pick your fabric</p><h2 id="svc-h">Sewing services in Newquay</h2><p>From a single button to a pair of blackout curtains, with clear guide prices for everything we do.</p></div>
<div class="swatches">{cards}</div></div></section>

<section class="denim stitched" aria-labelledby="craft-h"><div class="wrap split">
<div class="reveal"><p class="eyebrow">Everyday clothes, military standard</p><h2 id="craft-h">The small jobs, done properly</h2>
<p>A jeans hem that keeps its faded factory edge. A coat zip set in dead straight. A split seam re-sewn so it never splits again. Our work is everyday alterations and repairs, and we finish every one with the precision Sylvia learned as a military tailor.</p>
<ul><li><a href="{pre}trouser-jeans-alterations-newquay/">Trouser &amp; jeans alterations</a></li><li><a href="{pre}zip-replacement-newquay/">Zip &amp; button replacement</a></li><li><a href="{pre}clothing-repairs-newquay/">Clothing repairs &amp; mending</a></li><li><a href="{pre}curtain-alterations-newquay/">Curtain shortening &amp; home</a></li></ul></div>
<figure class="polaroid reveal" style="transform:rotate(2deg)">{img(pre, "jeans-flatlay", "Tailor's workbench with folded denim jeans chalk-marked for hemming, brass zip, tin of vintage buttons, tape measure and pins on pattern paper")}<figcaption>Chalked, pinned &amp; ready</figcaption></figure>
</div></section>

<section class="linen snip-host" aria-labelledby="price-h"><!--SNIP--><div class="wrap split">
<div class="reveal"><p class="eyebrow">Honest pricing</p><h2 id="price-h">Popular guide prices</h2>
<p>We publish our guide prices so you know roughly what to expect before you walk in. The full list covers trousers and jeans, zips and fastenings, repairs and curtains.</p>
{g["GUIDE_NOTE"]}<a class="btn" href="{pre}prices/">See every guide price</a></div>
<div class="price-card pinked-bottom reveal"><h3>Most asked-for <small class="eyebrow">guide prices</small></h3><table class="price-table"><caption class="sr-only">Popular guide prices</caption><tbody>{teaser}</tbody></table></div>
</div></section>

<section aria-labelledby="how-h"><div class="wrap">
<div class="section-head reveal"><p class="script">Simple as that</p><h2 id="how-h">How it works</h2></div>
<ul class="notions">
<li class="reveal spin-hover">{g["button_svg"]("#7b2d26")}<div><h3>1. Wash it</h3><p>Clean items only, so please freshly wash garments and curtains before drop-off.</p></div></li>
<li class="reveal spin-hover">{g["button_svg"]("#8a5c36")}<div><h3>2. Pin it</h3><p>We are happy to pin hems at drop-off, or pin or measure your preferred length at home.</p></div></li>
<li class="reveal spin-hover">{g["button_svg"]("#a87a3d")}<div><h3>3. We stitch it</h3><p>Your price is confirmed at drop-off. Standard turnaround {E(C["turnaround_standard"])}.</p></div></li>
<li class="reveal spin-hover">{g["button_svg"]("#6a2420")}<div><h3>Need it fast?</h3><p>Express service in {E(C["turnaround_express"])} for an extra £{C["express_surcharge"]}.</p></div></li>
</ul></div></section>

<section class="linen" aria-labelledby="areas-h"><div class="wrap">
<div class="section-head reveal"><p class="eyebrow">Around Newquay</p><h2 id="areas-h">Your local seamstress across mid &amp; north Cornwall</h2>
<p>Based in Newquay, with customers from St Columb, St Mawgan, Crantock, St Newlyn East, Perranporth, St Austell, Truro and beyond. <a href="{pre}areas-we-serve/">See the areas we serve</a>.</p></div>
<ul class="badges" style="justify-content:center">{"".join(f'<li>📍 {_h.escape(n)}</li>' for n, d in AREAS)}</ul>
</div></section>

<section class="snip-host" aria-labelledby="faq-h"><!--SNIP--><div class="wrap" style="max-width:860px">
<div class="section-head reveal"><p class="script">You asked</p><h2 id="faq-h">Alterations questions</h2></div>
{faqs}<p style="text-align:center;margin-top:1.5rem"><a class="btn alt" href="{pre}faq/">All FAQs</a></p></div></section>
'''

# ---------------- SERVICE PROSE ----------------
def p_trousers(pre, g):
    return f'''
<h2>Trouser hems, jeans hems and fitting in Newquay</h2>
<p>Trousers and jeans are the bread and butter of any sewing room, and they are where a tailor's training shows. A hem that sits a few millimetres off, a blind stitch that puckers, or a jeans hem that loses its faded edge are all things you notice every time you get dressed. Sylvia learned to hem uniform trousers to military standard at RAF St Mawgan, and that is how every pair is finished here.</p>
{img(pre, "jeans-flatlay", "Denim jeans with a chalked hem line beside a brass zip, vintage buttons, tape measure and tailor's chalk", "")}
<h2>What we do</h2>
<ul>
<li><strong>Standard jeans hem</strong>: shortened and re-stitched with matching heavy thread.</li>
<li><strong>Jeans hem keeping the original factory hem</strong>: the worn, faded hem is kept and re-attached higher up, so your jeans look untouched.</li>
<li><strong>Trouser hems, plain or blind stitch</strong>: an invisible finish for work trousers and smart trousers.</li>
<li><strong>Lined trouser hems and turn-ups</strong>: lining and outer shortened separately so they hang properly.</li>
<li><strong>Take in the waist or taper the legs</strong>: for standard trousers and for jeans, including heavier denim.</li>
</ul>
<h2>Getting the length right</h2>
<p>We are happy to pin your hems at drop-off. Bring the shoes you will wear with them, because a trainer and a heeled boot need very different lengths. If it is easier, pin or measure your preferred length at home and we will work to that. Please bring trousers and jeans freshly washed: we only work on clean items, and pre-washed denim will not shrink after we have hemmed it.</p>
<h2>How long does it take?</h2>
<p>Standard turnaround is {{std}}. Need them for a wedding, an interview or a trip? Express turnaround is {{exp}} for an extra £{{express}}.</p>
<p>Looking for something else? See <a href="{pre}zip-replacement-newquay/">jeans zip replacement</a> or <a href="{pre}clothing-repairs-newquay/">pocket and seam repairs</a>.</p>'''

def p_zips(pre, g):
    return f'''
<h2>Broken zip? Do not throw it away</h2>
<p>A broken zip is the most common reason a favourite coat or pair of jeans ends up at the back of the wardrobe, and it is one of the most satisfying repairs we do. A zip that is set in properly, with straight stitching and the teeth hidden where they should be, makes a garment feel new again.</p>
<h2>Zip replacement we offer</h2>
<ul>
<li><strong>Trouser and skirt zips</strong>: guide price includes a standard zip.</li>
<li><strong>Jeans zips</strong>: guide price includes a heavy-duty metal zip, because jeans need one.</li>
<li><strong>Coat and jacket zips</strong>: from the guide price plus the cost of the specialist zip (open-ended, two-way and chunky outdoor zips vary in length and type).</li>
<li><strong>Cushion cover zips</strong>: see <a href="{pre}curtain-alterations-newquay/">curtains &amp; home</a>.</li>
</ul>
<h2>Buttons and buttonholes</h2>
<p>Lost a button or have one hanging by a thread? Button replacement or restitching is a guide £3 each, or 3 for £7. We can also add a <strong>new machine buttonhole</strong>, which is handy when a button has been moved after taking a waistband in.</p>
<h2>Before you drop off</h2>
<p>Please wash the garment first, as we only work on clean items. If you have a particular zip colour or the original spare button, bring it along. Standard turnaround is {{std}}, or {{exp}} express for an extra £{{express}}.</p>
<p>Related: <a href="{pre}trouser-jeans-alterations-newquay/">jeans hems and tapering</a> · <a href="{pre}clothing-repairs-newquay/">clothing repairs</a></p>'''

def p_repairs(pre, g):
    return f'''
<h2>Mending that makes clothes last</h2>
<p>The most sustainable garment is the one already in your wardrobe. A split seam, a small tear or a hole in a pocket lining is usually a quick fix, and a neat repair can add years to a jacket, a pair of work trousers or a much-loved jumper. Newquay is hard on clothes, from salt, sand and wetsuit-changing in car parks, and we see plenty of it.</p>
{img(pre, "hero-machine", "Vintage black sewing machine with gold decals, coloured thread spools and tweed fabric swatches")}
<h2>Repairs we carry out</h2>
<ul>
<li><strong>Split seam restitching</strong>: side seams, seat seams, underarms and crotch seams re-sewn and reinforced.</li>
<li><strong>Small tear and patch repairs</strong>: neat repairs or patches on everyday clothes and workwear.</li>
<li><strong>Pocket bag repair or replacement</strong>: worn-through trouser and coat pockets rebuilt so you stop losing your keys.</li>
<li><strong>Buttons</strong>: replaced or restitched, guide £3 each or 3 for £7.</li>
</ul>
<p>Our minimum repair charge is £8. If you are not sure whether something can be saved, bring it in. We would rather tell you honestly at drop-off than charge for a repair that will not last.</p>
<h2>Clean items, please</h2>
<p>Garments must be freshly washed before drop-off. Standard turnaround is {{std}}, with express {{exp}} for an extra £{{express}}.</p>
<p>See also: <a href="{pre}zip-replacement-newquay/">zip replacement</a> · <a href="{pre}trouser-jeans-alterations-newquay/">trouser alterations</a></p>'''

def p_curtains(pre, g):
    return f'''
<h2>Curtains shortened to fit, without buying new</h2>
<p>New windows, a move, or a bargain pair that is just a little too long: shortening curtains is far cheaper than replacing them, and done properly nobody can tell. We shorten unlined curtains and lined or blackout curtains, keeping hems straight, linings hanging correctly and weights in place.</p>
{img(pre, "curtains", "Teal velvet and cream linen curtains pinned for a new hem on a wooden table, with tape measure, shears and a floral cushion")}
<h2>Curtain and home services</h2>
<ul>
<li><strong>Shorten unlined curtains</strong>: per pair, guide price from £20.</li>
<li><strong>Shorten lined or blackout curtains</strong>: per pair, guide price from £32. Lining and face fabric are shortened separately.</li>
<li><strong>Cushion cover zip replacement</strong>: guide £12, great for sofa cushions and holiday-let soft furnishings.</li>
</ul>
<h2>Measuring your curtains</h2>
<p>Measure from the top of the curtain (or the hook position) to where you want the hem to finish, and note whether you want them to just clear the floor, sit on the sill or puddle. Please bring curtains freshly washed: we can only work on clean items, and washing first avoids shrinkage after shortening.</p>
<h2>For holiday lets and second homes</h2>
<p>Newquay, Crantock and Padstow are full of holiday lets with tired soft furnishings. Shortening curtains and replacing broken cushion zips between seasons is an easy way to freshen a property. Standard turnaround is {{std}}, or express {{exp}} for an extra £{{express}}.</p>'''

# ---------------- OTHER PAGES ----------------
def prices_page(p):
    def body(pre, g):
        C = g["C"]
        h = (f'<header class="page-hero"><div class="wrap">{g["crumbs"](p, pre)}<p class="eyebrow">Guide price list</p><h1>{p["h1"]}</h1>'
             f'<p class="lede">Clear guide prices for everyday alterations in Newquay, from £{{from}}. Final prices are confirmed at drop-off or consultation, depending on the garment and the work needed.</p></div></header>')
        tables = "".join(g["price_table"](c["id"], "h2") for c in C["prices"])
        return h + f'''<section class="linen"><div class="wrap">{g["GUIDE_NOTE"]}
<div class="price-cols">{tables}
<div class="price-card pinked-bottom reveal" id="good-to-know"><h2>Good to know</h2>
<table class="price-table"><tbody>
<tr><th scope="row">Clean items only<span class="note">Garments and curtains must be freshly washed before drop-off.</span></th><td class="p"></td></tr>
<tr><th scope="row">Pinning &amp; fitting<span class="note">Happy to pin hems at drop-off, or pin or measure your preferred length at home.</span></th><td class="p"></td></tr>
<tr><th scope="row">Standard turnaround</th><td class="p">{C["turnaround_standard"]}</td></tr>
<tr><th scope="row">Express turnaround ({C["turnaround_express"]})</th><td class="p">+£{C["express_surcharge"]}</td></tr>
</tbody></table></div>
</div>
<p>Prices quoted in pounds sterling. See the service pages for detail: <a href="{pre}trouser-jeans-alterations-newquay/">trousers &amp; jeans</a> · <a href="{pre}zip-replacement-newquay/">zips &amp; buttons</a> · <a href="{pre}clothing-repairs-newquay/">repairs</a> · <a href="{pre}curtain-alterations-newquay/">curtains</a>.</p>
</div></section>'''
    return body

def about_page(p):
    def body(pre, g):
        C, E = g["C"], g["E"]
        people = "".join(f'<article class="person reveal" id="{x["name"].split()[0].lower()}"><span class="years">{E(x["years"])}<small>years</small></span><h3>{E(x["name"])}</h3><p class="role">{E(x["role"])}</p><p>{E(x["bio"])}</p></article>' for x in C["people"])
        h = (f'<header class="page-hero"><div class="wrap">{g["crumbs"](p, pre)}<p class="eyebrow">Our story</p><h1>{p["h1"]}</h1>'
             f'<p class="lede">A military tailor with more than 50 years at the cutting table, and the daughter learning every stitch from her.</p></div></header>')
        return h + f'''<section class="linen"><div class="wrap split">
<div class="prose reveal"><h2>Fifty years of tailoring at RAF St Mawgan</h2>
<p>Sylvia Pauline Tippett was a tailor at RAF St Mawgan, near Newquay, working for the military for over 50 years. Military tailoring is unforgiving: uniforms are worn on parade, inspected closely and expected to last. Hems must be level, seams straight and every detail regulation-correct. Half a century of that work builds a level of precision you can see in the finish.</p>
<p>Sylvia's skill reaches well beyond uniforms: over her career she has made ball gowns, suits and wedding dresses, and that understanding of how garments are constructed is what lets her alter them so well, from a simple pair of jeans to a layered bridal gown.</p>
<h2>Mother and daughter</h2>
<p>Maxine Jennings is Sylvia's daughter. For more than three years she has worked alongside her mum, learning her skills and standards at the sewing machine, so the craft continues in Newquay for the next generation of customers.</p></div>
<figure class="polaroid reveal">{img(pre, "heritage-tailor", "Vintage tailoring workshop with a green wool uniform-style jacket on a dress form and an old cast-iron sewing machine")}<figcaption>Precision, stitch by stitch</figcaption></figure>
</div></section>
<section><div class="wrap"><div class="section-head reveal"><p class="script">Meet the makers</p><h2>Sylvia &amp; Maxine</h2></div><div class="people">{people}</div></div></section>
<section class="tweed stitched"><div class="wrap"><div class="section-head reveal"><h2>What that means for you</h2></div>
<ul class="notions">
<li class="reveal">{g["button_svg"]("#a87a3d")}<div><h3>Precision</h3><p>Military-standard finishing on everyday alterations.</p></div></li>
<li class="reveal">{g["button_svg"]("#7b2d26")}<div><h3>Construction know-how</h3><p>Half a century of knowing how garments are built, applied to every hem and seam.</p></div></li>
<li class="reveal">{g["button_svg"]("#8a5c36")}<div><h3>Honest advice</h3><p>Clear guide prices, confirmed at drop-off before work starts.</p></div></li>
<li class="reveal">{g["button_svg"]("#e6d4b4")}<div><h3>Local</h3><p>Based in Newquay, a short trip from St Mawgan, Crantock and St Columb.</p></div></li>
</ul></div></section>'''
    return body

def areas_page(p):
    def body(pre, g):
        items = "".join(f"<li class=\"reveal\"><h3>Seamstress near {_h.escape(n)}</h3><p>{d}</p></li>" for n, d in AREAS)
        h = (f'<header class="page-hero"><div class="wrap">{g["crumbs"](p, pre)}<p class="eyebrow">Areas we serve</p><h1>{p["h1"]}</h1>'
             f'<p class="lede">We are based in Newquay and welcome drop-offs and fittings from across mid and north Cornwall.</p></div></header>')
        return h + f'''<section class="linen"><div class="wrap">
<ul class="area-list">{items}</ul>
<div class="prose" style="max-width:820px;margin:3rem auto 0">
<h2>Alterations near you, without the trip to the city</h2>
<p>Whether you are in St Columb Major, Crantock, Perranporth or further afield in St Austell or Truro, every service is available from our Newquay base: <a href="{pre}trouser-jeans-alterations-newquay/">trouser and jeans alterations</a>, <a href="{pre}zip-replacement-newquay/">zip replacement</a>, <a href="{pre}clothing-repairs-newquay/">repairs and mending</a> and <a href="{pre}curtain-alterations-newquay/">curtain shortening</a>.</p>
<p>Drop-off address: {{address}}, Newquay {{postcode}}. Call {{phone}} to arrange a time.</p></div></div></section>'''
    return body

def faq_page(p):
    def body(pre, g):
        h = (f'<header class="page-hero"><div class="wrap">{g["crumbs"](p, pre)}<p class="eyebrow">FAQ</p><h1>{p["h1"]}</h1>'
             f'<p class="lede">Prices, turnaround, washing, pinning and how to book. Everything people ask before bringing work in.</p></div></header>')
        return h + f'<section class="linen"><div class="wrap" style="max-width:880px">{faq_block(FAQS, pre)}</div></section>'
    return body

def contact_page(p):
    def body(pre, g):
        C, show, E = g["C"], g["show"], g["E"]
        hours = "".join(f"<tr><th scope=\"row\">{d}</th><td>{show(h)}</td></tr>" for d, h in C["opening_hours_display"])
        opts = "".join(f"<option>{g['E'](l)}</option>" for s, l in g["NAV"][1][2]) + "<option>Something else</option>"
        action = f' action="{E(C["form_action"])}" method="post"' if C["form_action"] else ""
        tel = f'<a href="tel:{E(C["phone_e164"])}">{E(C["phone_display"])}</a>' if not g["is_ph"](C["phone_e164"]) else show(C["phone_display"])
        mail = f'<a href="mailto:{E(C["email"])}">{E(C["email"])}</a>' if not g["is_ph"](C["email"]) else show(C["email"])
        mp = f'<p><a href="{E(C["map_link"])}" rel="noopener">Open in Google Maps →</a></p>' if not g["is_ph"](C["map_link"]) else f'<p>{show(C["map_link"])}</p>'
        h = (f'<header class="page-hero"><div class="wrap">{g["crumbs"](p, pre)}<p class="eyebrow">Contact &amp; drop-off</p><h1>{p["h1"]}</h1>'
             f'<p class="lede">Call, email or send an enquiry to arrange a drop-off. Please bring items freshly washed.</p></div></header>')
        return h + f'''<section class="linen"><div class="wrap contact-grid">
<div class="side-card"><h2>Find us</h2><address style="font-style:normal">{show(C["street_address"])}<br>{E(C["locality"])}, {E(C["region"])}<br>{show(C["postcode"])}</address>
<p>☎ {tel}<br>✉ {mail}</p>{mp}
<h3>Opening hours</h3><table class="hours"><tbody>{hours}</tbody></table></div>
<form class="form price-card" id="enquiry" data-email="{E(C["email"])}"{action}>
<h2>Send an enquiry</h2>
<label for="f-name">Your name</label><input id="f-name" type="text" name="name" autocomplete="name" required>
<label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel">
<label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email">
<label for="f-service">What do you need?</label><select id="f-service" name="service">{opts}</select>
<label for="f-msg">Tell us about the garment</label><textarea id="f-msg" name="message" rows="5" required></textarea>
<div class="btn-row"><button class="btn" type="submit">Send enquiry</button></div>
<p style="font-size:.88rem;margin-top:1rem">Prices are guide prices, confirmed at drop-off or consultation.</p>
</form></div></section>'''
    return body

def notfound(p):
    def body(pre, g):
        return (f'<section class="page-hero"><div class="wrap" style="text-align:center"><p class="script">Oops, a dropped stitch</p><h1>Page not found</h1>'
                f'<p class="lede" style="margin:0 auto 1.5rem">That page has come unpicked. Try the <a href="{g["URL"]}/">home page</a> or our <a href="{g["URL"]}/prices/">guide prices</a>.</p></div></section>')
    return body

def _svc(slug, crumb, title, desc, h1, service, eyebrow, lede, prose, cats=None, consult=False, img="hero-machine"):
    p = {"slug": slug, "crumb": crumb, "title": title, "desc": desc, "h1": h1, "service": service, "cats": cats or [], "img": img, "prio": "0.9"}
    p["body"] = svc_page(p, eyebrow, lede, prose, cats, consult)
    return p

PAGES = []
_home = {"slug": "", "crumb": "Home", "title": "Seamstress Newquay | Clothing Alterations & Repairs",
         "desc": "Newquay seamstress & ex-RAF St Mawgan tailor, 50+ years' experience. Hems, zips, repairs & curtains, guide prices from £3.",
         "h1": "", "prio": "1.0", "body": home}
PAGES.append(_home)
PAGES += [
 _svc("trouser-jeans-alterations-newquay", "Trouser & Jeans Alterations",
      "Trouser & Jeans Alterations Newquay | Guide from £10",
      "Jeans and trouser hems in Newquay, guide prices from £10. Original-hem jeans, blind-stitch, turn-ups, waists taken in & legs tapered by a 50-year tailor.",
      "Trouser &amp; Jeans Alterations in Newquay", "Trouser and jeans alterations", "Hems · tapering · waists",
      "Jeans hems (including keeping the original factory hem), plain and blind-stitched trouser hems, turn-ups, waists taken in and legs tapered. Guide prices from £10.",
      p_trousers, ["trousers"], img="jeans-flatlay"),
 _svc("zip-replacement-newquay", "Zip & Button Replacement",
      "Zip Replacement Newquay | Jeans & Coat Zips, Guide from £15",
      "Zip replacement in Newquay: trouser & skirt zips guide £15, jeans £18, coats from £25. Buttons from £3. Guide prices, confirmed at drop-off.",
      "Zip Replacement &amp; Buttons in Newquay", "Zip replacement and button repair", "Zips · buttons · buttonholes",
      "Trouser, skirt, jeans, coat and jacket zips replaced, buttons restitched and new machine buttonholes. Guide prices from £3.",
      p_zips, ["zips"], img="jeans-flatlay"),
 _svc("clothing-repairs-newquay", "Clothing Repairs & Mending",
      "Clothing Repairs & Mending Newquay | Guide from £8",
      "Clothing repairs in Newquay: split seams, small tears, patches and pocket bags mended by an ex-military tailor. Guide prices from £8, confirmed at drop-off.",
      "Clothing Repairs &amp; Mending in Newquay", "Clothing repairs and mending", "Seams · tears · patches · pockets",
      "Split seams restitched, small tears and patches repaired, pocket bags rebuilt and buttons sewn back on. Guide prices from £8.",
      p_repairs, ["repairs"]),
 _svc("curtain-alterations-newquay", "Curtain Shortening & Home",
      "Curtain Shortening Newquay | Guide Prices from £20",
      "Curtains shortened in Newquay: unlined from £20 a pair, lined & blackout from £32 (guide prices). Cushion zips replaced, guide £12. Ideal for holiday lets.",
      "Curtain Shortening &amp; Alterations in Newquay", "Curtain shortening and soft furnishing alterations", "Curtains · cushions · home",
      "Unlined, lined and blackout curtains shortened per pair, and cushion cover zips replaced. Guide prices from £12.",
      p_curtains, ["curtains"], img="curtains"),
]
_pr = {"slug": "prices", "crumb": "Guide Prices", "title": "Alteration Guide Prices Newquay | Newquay Seamstress",
       "desc": "Guide prices for alterations in Newquay: jeans hems from £10, trouser hems £12, zips from £15, repairs from £8, curtains from £20, confirmed at drop-off.",
       "h1": "Alteration &amp; Repair Guide Prices", "pagetype": "WebPage", "prio": "0.9"}
_pr["body"] = prices_page(_pr)
_ab = {"slug": "about", "crumb": "Our Story", "title": "About Sylvia & Maxine | Ex-RAF Tailor, Newquay",
       "desc": "Meet Sylvia Tippett, a tailor at RAF St Mawgan for over 50 years, and her daughter Maxine Jennings: Newquay's mother-and-daughter seamstresses.",
       "h1": "A Military Tailor &amp; Her Daughter", "pagetype": "AboutPage", "img": "heritage-tailor", "prio": "0.8"}
_ab["body"] = about_page(_ab)
_ar = {"slug": "areas-we-serve", "crumb": "Areas We Serve", "title": "Seamstress Near Newquay | St Columb, Crantock & Truro",
       "desc": "Clothing alterations & repairs from our Newquay base for St Columb, St Mawgan, Crantock, St Newlyn East, Perranporth, St Austell, Truro & Padstow.",
       "h1": "Seamstress for Newquay &amp; Surrounding Areas", "prio": "0.8"}
_ar["body"] = areas_page(_ar)
_fq = {"slug": "faq", "crumb": "FAQ", "title": "Alterations FAQ Newquay | Prices & Turnaround",
       "desc": "Answers on alteration guide prices, 3–5 day turnaround, 24–48 hour express, washing, pinning hems, zips and curtain shortening in Newquay.",
       "h1": "Frequently Asked Questions", "pagetype": "FAQPage_holder", "faq_schema": True, "prio": "0.7"}
_fq["pagetype"] = "WebPage"
_fq["body"] = faq_page(_fq)
_ct = {"slug": "contact", "crumb": "Contact", "title": "Contact Newquay Seamstress | Book an Alteration or Fitting",
       "desc": "Book a drop-off or a fitting with Newquay Seamstress. Clothing alterations, zips, repairs and curtain shortening in Newquay, Cornwall.",
       "h1": "Contact &amp; Book a Drop-off", "pagetype": "ContactPage", "prio": "0.8", "nocta": True}
_ct["body"] = contact_page(_ct)
_nf = {"slug": "404", "crumb": "Not found", "title": "Page not found | Newquay Seamstress", "desc": "Page not found.", "h1": "", "noindex": True}
_nf["body"] = notfound(_nf)
PAGES += [_pr, _ab, _ar, _fq, _ct, _nf]
