"""Guide-price tables, the guide-price note, the home page teaser and the service-page sidebar."""
from ..config import C, E, CATS, money, PRICE_TEASER, SERVICES
from .contact import call_btn, email_btn

GUIDE_NOTE = ('<p class="guide-note" role="note"><svg class="btn-icon" style="width:34px;height:34px" viewBox="0 0 60 60" aria-hidden="true">'
  '<circle cx="30" cy="30" r="27" fill="#a87a3d"/><circle cx="30" cy="30" r="21" fill="none" stroke="#2a170f" stroke-width="1.5" stroke-dasharray="3 3"/>'
  '<circle cx="24" cy="24" r="3" fill="#2a170f"/><circle cx="36" cy="24" r="3" fill="#2a170f"/><circle cx="24" cy="36" r="3" fill="#2a170f"/><circle cx="36" cy="36" r="3" fill="#2a170f"/></svg>'
  '<span><strong>Guide prices only.</strong> Every garment is different, so your final price is confirmed at drop-off or consultation, '
  'depending on the garment and the work needed. Nothing is started until you have agreed the price.</span></p>')

def price_table(cid, tag="h2"):
    c = CATS[cid]
    rows = "".join(f'<tr><th scope="row">{E(i["name"])}' + (f'<span class="note">{E(i["note"])}</span>' if i.get("note") else "") +
                   f'</th><td class="p">{E(money(i))}</td></tr>' for i in c["items"])
    return (f'<div class="price-card pinked-bottom reveal" id="{cid}"><{tag}>{E(c["name"])} <small class="eyebrow">guide prices</small></{tag}>'
            f'<table class="price-table"><caption class="sr-only">{E(c["name"])} guide prices</caption>'
            f'<thead class="sr-only"><tr><th scope="col">Service</th><th scope="col">Guide price</th></tr></thead><tbody>{rows}</tbody></table></div>')

def price_teaser():
    return "".join(f'<tr><th scope="row">{E(CATS[c]["items"][i]["name"])}</th><td class="p">{E(money(CATS[c]["items"][i]))}</td></tr>' for c, i in PRICE_TEASER)

def sidebar(cats):
    rows = "".join(f'<li>{E(i["name"])} — <strong>{E(money(i))}</strong></li>' for c in cats for i in CATS[c]["items"][:6])
    others = "".join(f'<li><a href="/{s["slug"]}/">{E(s["nav"])}</a></li>' for s in SERVICES)
    return ('<aside class="sidebar" aria-label="Service details">'
            f'<div class="side-card"><h2>Guide prices</h2><ul>{rows}</ul><p class="small">Guide prices only. Final price confirmed at drop-off.</p><p><a href="/prices/">Full guide price list →</a></p></div>'
            f'<div class="side-card rose"><h2>Good to know</h2><ul><li>Clean, freshly washed items only</li><li>Hems pinned at drop-off, or pin at home</li><li>Standard {E(C["turnaround_standard"])}</li><li>Express {E(C["turnaround_express"])} +£{C["express_surcharge"]}</li></ul>'
            f'<p class="btn-stack">{call_btn("btn mustard")}{email_btn("btn alt")}</p></div>'
            f'<div class="side-card"><h2>All services</h2><ul>{others}</ul></div></aside>')
