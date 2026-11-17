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
/* ---- Scroll-sewn thread + scissors (transform/opacity + paint-only dashoffset; no layout work per frame) ---- */
(function(){
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Scissors: cut once when the section break scrolls into view
  var snips = document.querySelectorAll('.snip');
  if (snips.length) {
    if (reduce || !('IntersectionObserver' in window)) snips.forEach(function(s){ s.classList.add('go'); });
    else {
      var so = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting) { e.target.classList.add('go'); so.unobserve(e.target); } }); }, { rootMargin: '0px 0px -25% 0px' });
      snips.forEach(function(s){ so.observe(s); });
    }
  }
  // Thread that sews itself down the page
  var NS = 'http://www.w3.org/2000/svg', svg, g, maskPath, needle, samples = [], L = 0, docH = 0, ticking = false;
  function el(n, a){ var e = document.createElementNS(NS, n); for (var k in a) e.setAttribute(k, a[k]); return e; }
  function build(){
    var w = window.innerWidth, mobile = w < 700, wrapW = Math.min(1180, w), gutter = (w - wrapW) / 2;
    var x0, x1;
    if (mobile) { x0 = 5; x1 = 15; } else if (gutter > 70) { x0 = Math.max(18, gutter * 0.25); x1 = gutter - 14; } else { x0 = 8; x1 = 22; }
    docH = document.documentElement.scrollHeight;
    var startY = (document.querySelector('.site-header') || {offsetHeight: 80}).offsetHeight + 10;
    var pts = [], step = mobile ? 260 : 340, i = 0;
    for (var y = startY; y < docH - 40; y += step, i++) pts.push([i % 2 ? x1 : x0 + (i % 3) * (x1 - x0) * 0.15, y]);
    pts.push([x0, docH - 40]);
    var d = 'M' + pts[0][0] + ' ' + pts[0][1];
    for (var j = 1; j < pts.length; j++) {
      var p0 = pts[j - 1], p1 = pts[j], my = (p1[1] - p0[1]) / 2;
      d += ' C' + p0[0] + ' ' + (p0[1] + my) + ' ' + p1[0] + ' ' + (p1[1] - my) + ' ' + p1[0] + ' ' + p1[1];
    }
    if (!svg) {
      svg = el('svg', { 'class': 'thread-layer', 'aria-hidden': 'true', focusable: 'false' });
      var defs = el('defs', {}), mask = el('mask', { id: 'sewn', maskUnits: 'userSpaceOnUse', x: 0, y: 0, width: 400, height: 100000 });
      maskPath = el('path', { fill: 'none', stroke: '#fff', 'stroke-width': 8, 'stroke-linecap': 'round' });
      mask.appendChild(maskPath); defs.appendChild(mask); svg.appendChild(defs);
      g = el('g', {});
      g.appendChild(el('path', { 'class': 'thread-shadow', mask: 'url(#sewn)' }));
      g.appendChild(el('path', { 'class': 'thread', mask: 'url(#sewn)' }));
      needle = el('g', { 'class': 'needle' });
      needle.innerHTML = '<path d="M0 -26 L1.6 8 L0 12 L-1.6 8 Z" fill="#c9c4bb" stroke="#4a4540" stroke-width=".6"/><ellipse cx="0" cy="-20" rx=".9" ry="3" fill="#2f1d14"/>' +
        '<path d="M0 -20 C 6 -26, 10 -14, 4 -8" fill="none" stroke="var(--rose)" stroke-width="1.6"/>';
      g.appendChild(needle); svg.appendChild(g);
      document.body.appendChild(svg);
    }
    g.querySelectorAll('.thread,.thread-shadow').forEach(function(p){ p.setAttribute('d', d); });
    maskPath.setAttribute('d', d);
    L = maskPath.getTotalLength();
    maskPath.style.strokeDasharray = L + ' ' + L;
    samples = [];
    var N = Math.max(200, Math.round(L / 12));
    for (var k = 0; k <= N; k++) {
      var a = maskPath.getPointAtLength(L * k / N), b = maskPath.getPointAtLength(Math.min(L, L * k / N + 2));
      samples.push([a.x, a.y, Math.atan2(b.y - a.y, b.x - a.x) * 57.2958 - 90]);
    }
    update();
  }
  function update(){
    ticking = false;
    var sy = window.scrollY || window.pageYOffset, vh = window.innerHeight;
    var prog = reduce ? 1 : Math.min(1, Math.max(0, (sy + vh * 0.62) / docH));
    // keep the leading tip at ~62% of the viewport height: find sample whose y matches
    var targetY = reduce ? docH : sy + vh * 0.62, lo = 0, hi = samples.length - 1;
    while (lo < hi) { var mid = (lo + hi) >> 1; if (samples[mid][1] < targetY) lo = mid + 1; else hi = mid; }
    var s = samples[lo] || samples[samples.length - 1], len = L * lo / (samples.length - 1);
    maskPath.style.strokeDashoffset = (L - len);
    g.setAttribute('transform', 'translate(0 ' + (-sy) + ')');
    needle.setAttribute('transform', 'translate(' + s[0] + ' ' + s[1] + ') rotate(' + s[2] + ')');
    needle.style.opacity = (prog >= 1 || lo >= samples.length - 1) ? 0 : 1;
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
