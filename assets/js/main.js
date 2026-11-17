(function(){
  var t=document.querySelector('.nav-toggle'),n=document.getElementById('main-nav');
  if(t&&n){t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o)});}
  var els=document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    els.forEach(function(el){io.observe(el)});
  } else els.forEach(function(el){el.classList.add('in')});
  var f=document.getElementById('enquiry');
  if(f&&!f.getAttribute('action')){
    f.addEventListener('submit',function(ev){
      ev.preventDefault();var d=new FormData(f),to=f.dataset.email||'';
      var body='Name: '+d.get('name')+'\nPhone: '+d.get('phone')+'\nService: '+d.get('service')+'\n\n'+d.get('message');
      if(to.charAt(0)==='['){alert('The contact email has not been set up yet. Please call or visit us instead.');return;}
      location.href='mailto:'+to+'?subject='+encodeURIComponent('Alteration enquiry: '+d.get('service'))+'&body='+encodeURIComponent(body);
    });
  }
})();
/* ---- Scroll-sewn thread + scissors. Stitches are revealed with a stroke-dasharray built per stitch (no SVG mask),
   the layer is fixed and moved with a transform, scissors are HTML boxes moved with CSS transforms. ---- */
(function(){
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Scissors: cut when the section break is well into view
  var snips = document.querySelectorAll('.snip');
  if (snips.length) {
    if (!('IntersectionObserver' in window)) snips.forEach(function(s){ s.classList.add('go'); });
    else {
      var so = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting) { e.target.classList.add('go'); so.unobserve(e.target); } }); }, { rootMargin: '0px 0px -30% 0px', threshold: 0 });
      snips.forEach(function(s){ so.observe(s); });
    }
  }
  var NS = 'http://www.w3.org/2000/svg', svg, g, thread, halo, guide, needle, samples = [], L = 0, docH = 0, ticking = false, lastN = -1, STITCH = 12, GAP = 8;
  function el(n, a){ var e = document.createElementNS(NS, n); for (var k in a) e.setAttribute(k, a[k]); return e; }
  function dashes(n){ var s = ''; for (var i = 0; i < n; i++) s += STITCH + ' ' + GAP + ' '; return s + '0 ' + (L + 100); }
  function build(){
    var w = window.innerWidth, mobile = w < 700, wrapW = Math.min(1180, w), gutter = (w - wrapW) / 2, x0, x1;
    if (mobile) { x0 = 6; x1 = 16; STITCH = 9; GAP = 6; }
    else if (gutter > 80) { x0 = 26; x1 = Math.min(gutter - 16, 150); STITCH = 12; GAP = 8; }
    else { x0 = 10; x1 = 34; STITCH = 12; GAP = 8; }
    docH = document.documentElement.scrollHeight;
    var hdr = document.querySelector('.site-header'), startY = (hdr ? hdr.offsetHeight : 80) + 16;
    var pts = [], step = mobile ? 240 : 300;
    for (var y = startY, i = 0; y < docH - 60; y += step, i++) pts.push([i % 2 ? x1 : x0, y]);
    pts.push([x0, docH - 60]);
    var d = 'M' + pts[0][0] + ' ' + pts[0][1];
    for (var j = 1; j < pts.length; j++) { var p0 = pts[j-1], p1 = pts[j], my = (p1[1] - p0[1]) / 2;
      d += ' C' + p0[0] + ' ' + (p0[1] + my) + ' ' + p1[0] + ' ' + (p1[1] - my) + ' ' + p1[0] + ' ' + p1[1]; }
    if (!svg) {
      svg = el('svg', { 'class': 'thread-layer', 'aria-hidden': 'true', focusable: 'false' });
      var defs = el('defs', {}), lg = el('linearGradient', { id: 'steel', x1: '0', x2: '1', y1: '0', y2: '0' });
      lg.appendChild(el('stop', { offset: '0', 'stop-color': '#8d8780' })); lg.appendChild(el('stop', { offset: '.45', 'stop-color': '#f2efe9' })); lg.appendChild(el('stop', { offset: '1', 'stop-color': '#6f6a64' }));
      defs.appendChild(lg); svg.appendChild(defs);
      g = el('g', {});
      guide = el('path', { 'class': 'guide' }); halo = el('path', { 'class': 'thread-halo' }); thread = el('path', { 'class': 'thread' });
      needle = el('g', { 'class': 'needle' });
      needle.appendChild(el('path', { 'class': 'needle-thread', d: 'M0 -36 C 12 -46, 20 -24, 8 -14 S -4 2, 0 4' }));
      needle.appendChild(el('path', { 'class': 'needle-steel', d: 'M-2.6 -44 Q0 -48 2.6 -44 L2.2 14 L0 24 L-2.2 14 Z' }));
      needle.appendChild(el('ellipse', { 'class': 'needle-eye', cx: 0, cy: -36, rx: 1, ry: 4.2 }));
      g.appendChild(guide); g.appendChild(halo); g.appendChild(thread); g.appendChild(needle); svg.appendChild(g);
      document.body.appendChild(svg);
    }
    [guide, halo, thread].forEach(function(p){ p.setAttribute('d', d); });
    L = thread.getTotalLength(); lastN = -1;
    samples = []; var N = Math.max(240, Math.round(L / 10));
    for (var k = 0; k <= N; k++) { var a = thread.getPointAtLength(L * k / N), b = thread.getPointAtLength(Math.min(L, L * k / N + 3));
      samples.push([a.x, a.y, Math.atan2(b.y - a.y, b.x - a.x) * 57.29578 - 90, L * k / N]); }
    update();
  }
  function update(){
    ticking = false;
    var sy = window.pageYOffset || document.documentElement.scrollTop, vh = window.innerHeight, targetY = sy + vh * 0.6;
    var lo = 0, hi = samples.length - 1;
    while (lo < hi) { var mid = (lo + hi) >> 1; if (samples[mid][1] < targetY) lo = mid + 1; else hi = mid; }
    var s = samples[lo], n = Math.floor(s[3] / (STITCH + GAP));
    if (n !== lastN) { var da = dashes(n); thread.setAttribute('stroke-dasharray', da); halo.setAttribute('stroke-dasharray', da); lastN = n; }
    g.setAttribute('transform', 'translate(0 ' + (-sy) + ')');
    needle.setAttribute('transform', 'translate(' + s[0].toFixed(1) + ' ' + s[1].toFixed(1) + ') rotate(' + s[2].toFixed(1) + ')');
    needle.style.opacity = lo >= samples.length - 1 ? 0 : 1;
  }
  function onScroll(){ if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  function init(){
    build();
    window.addEventListener('scroll', onScroll, { passive: true });
    var rt; window.addEventListener('resize', function(){ clearTimeout(rt); rt = setTimeout(build, 200); });
    if ('ResizeObserver' in window) { var last = docH; new ResizeObserver(function(){ var h = document.documentElement.scrollHeight; if (Math.abs(h - last) > 50) { last = h; build(); } }).observe(document.body); }
  }
  if (document.readyState === 'complete') init(); else window.addEventListener('load', init);
})();
