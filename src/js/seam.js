// Scroll-sewn seam: a straight vertical machine stitch down the left edge, needle leading.
// Plain SVG line + stroke-dasharray in a fixed layer moved with a transform.
// No masks and no CSS scroll-timelines, so it behaves the same in Safari and Chrome.
export function initSeam(){
  var NS = 'http://www.w3.org/2000/svg', loop, sc = 1, svg, g, seam, halo, guide, needle, x = 20, startY = 90, endY = 0, step = 20, lastN = -1, ticking = false;
  function el(n, a){ var e = document.createElementNS(NS, n); for (var k in a) e.setAttribute(k, a[k]); return e; }
  function build(){
    var w = window.innerWidth, mobile = w < 700, gutter = (w - Math.min(1180, w)) / 2;
    x = mobile ? 9 : (gutter > 80 ? Math.round(Math.max(24, Math.min(gutter * 0.45, 72))) : 14);
    var S = mobile ? 10 : 14, G = mobile ? 7 : 9; step = S + G;
    var hdr = document.querySelector('.site-header'); startY = (hdr ? hdr.offsetHeight : 80) + 12;
    endY = document.documentElement.scrollHeight - 40;
    if (!svg) {
      svg = el('svg', { 'class': 'thread-layer', 'aria-hidden': 'true', focusable: 'false' });
      var defs = el('defs', {}), lg = el('linearGradient', { id: 'steel', x1: '0', x2: '1', y1: '0', y2: '0' });
      lg.appendChild(el('stop', { offset: '0', 'stop-color': '#8d8780' })); lg.appendChild(el('stop', { offset: '.45', 'stop-color': '#f4f1ec' })); lg.appendChild(el('stop', { offset: '1', 'stop-color': '#6f6a64' }));
      defs.appendChild(lg); svg.appendChild(defs);
      g = el('g', {});
      guide = el('line', { 'class': 'guide' }); halo = el('line', { 'class': 'thread-halo' }); seam = el('line', { 'class': 'thread' });
      needle = el('g', { 'class': 'needle' });
      var bob = el('g', { 'class': 'needle-bob' });
      loop = el('path', { 'class': 'needle-thread' }); bob.appendChild(loop);
      bob.appendChild(el('path', { 'class': 'needle-steel', d: 'M-3 -50 Q0 -55 3 -50 L2.6 16 L0 28 L-2.6 16 Z' }));
      bob.appendChild(el('ellipse', { 'class': 'needle-eye', cx: 0, cy: -41, rx: 1.1, ry: 4.6 }));
      needle.appendChild(bob);
      g.appendChild(guide); g.appendChild(halo); g.appendChild(seam); g.appendChild(needle); svg.appendChild(g);
      document.body.appendChild(svg);
    }
    // tight lane (no wide side gutter): tuck the thread loop so it stays inside the seam lane and never crosses the content
    var tight = gutter <= 80;
    loop.setAttribute('d', tight ? 'M0 -40 C 6 -45, 7 -31, 3 -24 S -2 2, 0 10' : 'M0 -40 C 14 -50, 22 -26, 9 -16 S -3 4, 0 10');
    sc = tight && mobile ? .85 : 1;
    [guide, halo, seam].forEach(function(l){ l.setAttribute('x1', x); l.setAttribute('x2', x); l.setAttribute('y1', startY); });
    guide.setAttribute('y2', endY);
    seam.setAttribute('stroke-dasharray', S + ' ' + G); halo.setAttribute('stroke-dasharray', S + ' ' + G);
    lastN = -1; update();
  }
  function update(){
    ticking = false;
    var sy = window.pageYOffset || document.documentElement.scrollTop, vh = window.innerHeight;
    var tip = Math.min(endY, Math.max(startY, sy + vh * 0.6));
    var n = Math.floor((tip - startY) / step), y = startY + n * step;
    if (n !== lastN) { seam.setAttribute('y2', y); halo.setAttribute('y2', y); lastN = n; }
    g.setAttribute('transform', 'translate(0 ' + (-sy) + ')');
    needle.setAttribute('transform', 'translate(' + x + ' ' + y + ')' + (sc !== 1 ? ' scale(' + sc + ')' : ''));
    needle.style.opacity = tip >= endY ? 0 : 1;
  }
  function onScroll(){ if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  function init(){
    build();
    window.addEventListener('scroll', onScroll, { passive: true });
    var rt; window.addEventListener('resize', function(){ clearTimeout(rt); rt = setTimeout(build, 200); });
    if ('ResizeObserver' in window) { var last = endY; new ResizeObserver(function(){ var h = document.documentElement.scrollHeight - 40; if (Math.abs(h - last) > 50) { last = h; build(); } }).observe(document.body); }
  }
  if (document.readyState === 'complete') init(); else window.addEventListener('load', init);
}
