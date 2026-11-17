// Vintage mobile menu (focus trap, Esc to close, body scroll lock, Services accordion)
// and the sticky mobile call bar (hides while scrolling down, returns when scrolling up).
export function initNav(){
  var t=document.querySelector('.nav-toggle'),m=document.getElementById('mnav'),hdr=document.querySelector('.site-header'),root=document.documentElement,sy=0,closeT;
  function focusables(){return [t].concat([].slice.call(m.querySelectorAll('a[href],button:not([disabled])')).filter(function(e){return e.offsetParent!==null;}));}
  function openM(){clearTimeout(closeT);root.style.setProperty('--hdr',(hdr?hdr.offsetHeight:92)+'px');sy=window.pageYOffset;m.hidden=false;
    document.body.style.position='fixed';document.body.style.top=(-sy)+'px';document.body.style.left='0';document.body.style.right='0';root.classList.add('menu-open');
    requestAnimationFrame(function(){requestAnimationFrame(function(){m.classList.add('open');});});t.setAttribute('aria-expanded','true');var lb=t.querySelector('.tlabel');if(lb)lb.textContent='Close';
    setTimeout(function(){var f=m.querySelector('.tag');if(f)f.focus({preventScroll:true});},120);}
  function closeM(back){m.classList.remove('open');t.setAttribute('aria-expanded','false');var lb=t.querySelector('.tlabel');if(lb)lb.textContent='Menu';root.classList.remove('menu-open');
    document.body.style.position='';document.body.style.top='';document.body.style.left='';document.body.style.right='';window.scrollTo(0,sy);
    closeT=setTimeout(function(){m.hidden=true;},520);if(back!==false)t.focus({preventScroll:true});}
  if(t&&m){
    t.addEventListener('click',function(){t.getAttribute('aria-expanded')==='true'?closeM():openM();});
    document.addEventListener('keydown',function(e){if(t.getAttribute('aria-expanded')!=='true')return;
      if(e.key==='Escape'){e.preventDefault();closeM();return;}
      if(e.key==='Tab'){var f=focusables(),first=f[0],last=f[f.length-1];
        if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
        else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}}});
    m.addEventListener('click',function(e){var a=e.target.closest('a');if(a&&a.getAttribute('href').indexOf('#')===-1)closeM(false);});
    var acc=m.querySelector('.acc');if(acc){acc.addEventListener('click',function(){var s=document.getElementById(acc.getAttribute('aria-controls')),o=acc.getAttribute('aria-expanded')==='true';acc.setAttribute('aria-expanded',String(!o));s.hidden=o;});}
    window.addEventListener('resize',function(){if(window.innerWidth>960&&t.getAttribute('aria-expanded')==='true')closeM(false);});
  }
}

export function initCallBar(){
  var bar = document.querySelector('.call-bar'); if (!bar) return;
  var last = window.pageYOffset, ticking = false;
  function update(){
    ticking = false;
    var y = window.pageYOffset, max = document.documentElement.scrollHeight - window.innerHeight;
    if (y > last + 6 && y > 200 && y < max - 80) bar.classList.add('hide');
    else if (y < last - 6 || y >= max - 80 || y <= 200) bar.classList.remove('hide');
    last = y;
  }
  window.addEventListener('scroll', function(){ if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
}
