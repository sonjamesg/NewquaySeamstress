"""Inline SVG icons (no emoji glyphs, so they look the same on every device)."""
PHONE = ('<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>')
MAIL = ('<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M3.5 5.5h17v13h-17z"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="m3.8 6 8.2 7 8.2-7"/></svg>')
PIN = ('<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>')

def button_svg(color):
    """A four-hole sewing button that 'stitches itself on' when revealed (see 30-animations.css)."""
    return (f'<svg class="btn-icon" viewBox="0 0 60 60" aria-hidden="true"><circle cx="30" cy="30" r="27" fill="{color}"/><circle cx="30" cy="30" r="27" fill="none" stroke="rgba(0,0,0,.25)" stroke-width="2"/>'
            '<circle cx="30" cy="30" r="20" fill="none" stroke="rgba(255,255,255,.5)" stroke-width="1.5" stroke-dasharray="3 3"/>'
            '<circle cx="24" cy="24" r="3.2" fill="rgba(0,0,0,.45)"/><circle cx="36" cy="24" r="3.2" fill="rgba(0,0,0,.45)"/><circle cx="24" cy="36" r="3.2" fill="rgba(0,0,0,.45)"/><circle cx="36" cy="36" r="3.2" fill="rgba(0,0,0,.45)"/>'
            '<path class="xstitch" d="M24 24L36 36M36 24L24 36"/></svg>')

MACHINE = ('<svg class="machine-svg" viewBox="0 0 220 130" aria-hidden="true"><g fill="#e6d4b4">'
  '<path d="M20 112h180v10H20z"/><path d="M38 108c0-40 4-62 30-70h86c22 0 30 10 30 26v44h-20V66c0-8-4-12-12-12H78c-14 4-18 20-18 54z"/>'
  '<rect x="150" y="30" width="44" height="12" rx="4"/><rect x="62" y="84" width="10" height="24"/><rect x="64" y="104" width="6" height="8" fill="#a87a3d"/>'
  '<circle cx="196" cy="70" r="18" fill="none" stroke="#e6d4b4" stroke-width="5"/><circle cx="196" cy="70" r="4"/></g>'
  '<path d="M90 47c10-6 30-6 40 0" stroke="#a87a3d" stroke-width="2" fill="none"/><path d="M98 52c6-3 18-3 24 0" stroke="#a87a3d" stroke-width="1.5" fill="none"/>'
  '<path d="M20 126h180" stroke="#a87a3d" stroke-width="2" stroke-dasharray="6 5"/></svg>')
