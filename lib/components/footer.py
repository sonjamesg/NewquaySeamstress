"""Site footer."""
import datetime
from ..config import C, E, is_ph, SERVICES
from .contact import tel_link, mail_link, call_btn, email_btn, address_html
from .icons import MACHINE, PHONE, MAIL, PIN

def footer():
    hours = "".join(f"<li>{d}: {E(h)}</li>" for d, h in C["opening_hours_display"] if not is_ph(h))
    last = (f'<div><h2>Opening hours</h2><ul>{hours}</ul></div>' if hours else
            f'<div><h2>Get in touch</h2><p>{E(C["dropoff_note"])}</p><p class="btn-stack">{call_btn("btn mustard")}{email_btn("btn alt")}</p></div>')
    svc = "".join(f'<li><a href="/{s["slug"]}/">{E(s["nav"])}</a></li>' for s in SERVICES)
    soc = "".join(f'<li><a href="{E(C[k])}" rel="noopener">{lbl}</a></li>' for k, lbl in (("facebook_url", "Facebook"), ("instagram_url", "Instagram"), ("google_business_url", "Google reviews")) if not is_ph(C[k]))
    return (f'<footer class="site-footer"><div class="wrap"><div class="foot-grid"><div>{MACHINE}<p><strong>{E(C["business_name"])}</strong><br>'
            f'Mother-and-daughter seamstresses in Newquay, Cornwall. Sylvia brings 50+ years of tailoring, including her career as a tailor at RAF St Mawgan.</p>'
            f'<address>{PIN} {address_html()}<br>{PHONE} {tel_link()}<br>{MAIL} {mail_link()}</address></div>'
            f'<div><h2>Services</h2><ul>{svc}</ul></div>'
            f'<div><h2>Explore</h2><ul><li><a href="/prices/">Guide price list</a></li><li><a href="/about/">Sylvia &amp; Maxine</a></li><li><a href="/areas-we-serve/">Areas we serve</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/contact/">Contact &amp; drop-off</a></li>{soc}</ul></div>'
            f'{last}</div>'
            f'<div class="foot-base"><span>© {datetime.date.today().year} {E(C["business_name"])} · Newquay, Cornwall</span><span>All prices shown are guide prices, confirmed at drop-off or consultation.</span></div></div></footer>')
