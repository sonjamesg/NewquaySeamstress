"""Site navigation structure (desktop nav + footer + mobile menu all read from here)."""
from ..config import SERVICES, E
from .contact import tel_link
from .icons import PHONE
from ..config import C

def nav():
    return [("", "Home"), ("services", "Services", [(s["slug"], s["nav"]) for s in SERVICES]),
            ("prices", "Guide prices"), ("about", "Our story"), ("areas-we-serve", "Areas"), ("faq", "FAQ"), ("contact", "Contact")]

def href(slug): return "/" + (slug + "/" if slug else "")

def desktop_nav(cur):
    def li(slug, label):
        a = ' aria-current="page"' if slug == cur else ""
        return f'<li><a href="{href(slug)}"{a}>{E(label)}</a></li>'
    items = []
    for n in nav():
        if len(n) == 3:
            items.append('<li class="has-sub"><a href="/#services">Services ▾</a><ul>' + "".join(li(s, l) for s, l in n[2]) + "</ul></li>")
        else: items.append(li(n[0], n[1]))
    items.append(f'<li class="nav-call">{tel_link("", PHONE + " " + E(C["phone_display"]))}</li>')
    return f'<nav class="main-nav" id="main-nav" aria-label="Main"><ul>{"".join(items)}</ul></nav>'
