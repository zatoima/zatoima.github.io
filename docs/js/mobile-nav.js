// Mobile hamburger menu
(function() {
  var btn = document.getElementById('hamburger-btn');
  var nav = document.querySelector('.header-nav');
  var overlay = document.getElementById('nav-overlay');
  if (!btn || !nav) return;

  function toggle() {
    var isOpen = nav.classList.toggle('open');
    btn.classList.toggle('open', isOpen);
    if (overlay) overlay.classList.toggle('active', isOpen);
    document.body.style.overflow = isOpen ? 'hidden' : '';
  }

  function close() {
    nav.classList.remove('open');
    btn.classList.remove('open');
    if (overlay) overlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  btn.addEventListener('click', toggle);
  if (overlay) overlay.addEventListener('click', close);

  // Close on nav link click
  nav.querySelectorAll('a').forEach(function(a) {
    a.addEventListener('click', close);
  });
})();
