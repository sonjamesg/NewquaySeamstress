"""Vintage mobile menu: thread-hole button toggle, full-screen fabric panel, sewn-label items,
Services accordion, Call / Email buttons. Behaviour lives in src/js/nav.js, styles in 08-mobile-menu.css."""
from ..config import C, E
from .nav import nav, href
from .contact import call_btn, email_btn

TOGGLE = ('<button type="button" class="nav-toggle" aria-expanded="false" aria-controls="mnav">'
          '<span class="sr-only">Menu</span><span class="tbtn" aria-hidden="true"><i class="h h1"></i><i class="h h2"></i><i class="h h3"></i><i class="h h4"></i>'
          '<i class="th t1"></i><i class="th t2"></i></span><span class="tlabel" aria-hidden="true">Menu</span></button>')

def panel(cur, A):
    items = []
    for i, n in enumerate(nav()):
        if len(n) == 3:
            subs = "".join(f'<li><a href="{href(s)}"' + (' aria-current="page"' if s == cur else "") + f'>{E(l)}</a></li>' for s, l in n[2])
            items.append(f'<li class="mi" style="--i:{i}"><button type="button" class="tag acc" aria-expanded="false" aria-controls="m-services">Services<span class="chev" aria-hidden="true"></span></button>'
                         f'<ul class="msub" id="m-services" hidden>{subs}</ul></li>')
        else:
            a = ' aria-current="page"' if n[0] == cur else ""
            items.append(f'<li class="mi" style="--i:{i}"><a class="tag" href="{href(n[0])}"{a}>{E(n[1])}</a></li>')
    return (f'<div class="mnav" id="mnav" role="dialog" aria-modal="true" aria-label="Site menu" hidden><div class="mnav-inner">'
            f'<img class="mnav-logo" src="{A.url("assets/img/logo.svg")}" alt="{E(C["business_name"])}" width="170" height="102" loading="lazy" decoding="async">'
            f'<nav aria-label="Mobile"><ul class="mlist">{"".join(items)}</ul></nav>'
            f'<div class="mnav-cta" style="--i:{len(items)}">{call_btn("btn mustard", "Call " + C["contact_name"])}{email_btn("btn alt", "Email")}</div>'
            f'<p class="mnav-note">{E(C["dropoff_note"])}</p></div></div>')
