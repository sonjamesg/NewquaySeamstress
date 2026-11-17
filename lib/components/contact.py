import re
"""Phone / email links and buttons. Email is lightly entity-encoded against scrapers but still works without JS."""
from ..config import C, E, obf
from .icons import PHONE, MAIL

def _nbsp(h):   # spaces in phone-link text must be non-breaking (keeps numbers on one line)
    return re.sub(r">([^<]*)", lambda m: ">" + m.group(1).replace(" ", "&nbsp;"), ">" + h)[1:]
def tel_link(cls="", label=None):
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="tel:{C["phone_e164"]}">{_nbsp(label or E(C["phone_display"]))}</a>'
def mail_link(cls="", label=None):
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="{obf("mailto:" + C["email"])}">{label or obf(C["email"])}</a>'
def call_btn(cls="btn", text=None):
    return tel_link(cls, PHONE + E(text or "Call " + C["phone_display"]))
def email_btn(cls="btn alt", text=None):
    return mail_link(cls, MAIL + E(text or "Email " + C["contact_name"]))
def address_html():
    return E(C["locality"]) + ", " + E(C["region"]) + "<br>" + E(C["dropoff_note"])
