"""Call-to-action band (end of most pages) and the sticky mobile contact bar."""
from ..config import C, E
from .contact import call_btn, email_btn, tel_link, mail_link
from .icons import PHONE, MAIL

def cta_band():
    return (f'<section class="cta-band felt stitched"><div class="wrap reveal"><p class="script">Bring it in…</p><h2>Ready to love your clothes again?</h2>'
            f'<p>Wash it, bring it in and we will pin it, price it and stitch it. Standard turnaround is {E(C["turnaround_standard"])}, with express {E(C["turnaround_express"])} for an extra £{C["express_surcharge"]}.</p>'
            f'<div class="btn-row">{call_btn("btn mustard")}{email_btn("btn alt")}<a class="btn" href="/contact/">Send an enquiry</a></div></div></section>')

def call_bar():
    return (f'<aside class="call-bar" aria-label="Quick contact">{tel_link("cbtn call", PHONE + "<span>Call " + E(C["contact_name"]) + "</span>")}'
            f'{mail_link("cbtn mail", MAIL + "<span>Email</span>")}</aside>')
