(function() {
  'use strict';

  var btn = document.getElementById('lang-btn');
  if (!btn) return;

  var dropdown = document.getElementById('lang-dropdown');
  if (!dropdown) return;

  btn.addEventListener('click', function(e) {
    e.stopPropagation();
    dropdown.classList.toggle('open');
    // Close other dropdowns (dark mode)
    var themeDropdown = document.querySelector('.theme-dropdown');
    if (themeDropdown) themeDropdown.classList.remove('open');
  });

  // Close dropdown on outside click
  document.addEventListener('click', function() {
    dropdown.classList.remove('open');
  });

  // Update localStorage when switching language
  var links = dropdown.querySelectorAll('.lang-dropdown-item');
  for (var i = 0; i < links.length; i++) {
    links[i].addEventListener('click', function() {
      var lang = this.getAttribute('lang');
      if (lang) {
        localStorage.setItem('preferred-lang', lang);
      }
    });
  }
})();
