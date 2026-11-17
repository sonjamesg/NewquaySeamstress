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
