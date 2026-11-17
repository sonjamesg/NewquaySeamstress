"""Site header: skip link, logo, desktop nav, mobile toggle + panel."""
from ..config import C, E
from .images import logo_picture
from .nav import desktop_nav
from .mobile_menu import TOGGLE, panel

def header(cur, A):
    brand = (f'<a class="brand" href="/" aria-label="{E(C["business_name"])} home">'
             + logo_picture(A, "logo-header", (103, 206), f'{C["business_name"]} logo', "brand-logo", eager=True) + "</a>")
    return (f'<a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="nav-bar">{brand}{TOGGLE}{desktop_nav(cur)}</div></header>'
            + panel(cur, A))
