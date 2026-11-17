// Enquiry form: posts to FormSubmit (no backend). Shows a sending state and guards double submits.
// If no form action is configured it falls back to opening an email with the details filled in.
export function initForm(){
  var f = document.getElementById('enquiry'); if (!f) return;
  if (f.getAttribute('action')) {
    f.addEventListener('submit', function(){
      var b = f.querySelector('button[type=submit]');
      if (b) { b.disabled = true; b.textContent = 'Sending…'; }
    });
    return;
  }
  f.addEventListener('submit', function(ev){
    ev.preventDefault();
    var d = new FormData(f), to = f.dataset.email || '';
    var body = 'Name: ' + d.get('name') + '\nPhone: ' + d.get('phone') + '\nService: ' + d.get('service') + '\n\n' + d.get('message');
    location.href = 'mailto:' + to + '?subject=' + encodeURIComponent('Alteration enquiry: ' + d.get('service')) + '&body=' + encodeURIComponent(body);
  });
}
