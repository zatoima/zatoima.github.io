// Dark mode toggle (3-way: light / dark / system)
(function () {
  var btn = document.getElementById('dark-mode-btn');
  if (!btn) return;

  var iconMoon = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  var iconSun = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
  var iconMonitor = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>';

  var iconSmallSun = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
  var iconSmallMoon = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  var iconSmallMonitor = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>';

  var dropdown = document.createElement('div');
  dropdown.className = 'theme-dropdown';
  dropdown.innerHTML =
    '<button class="theme-dropdown-item" data-theme-value="light">' + iconSmallSun + ' ライト</button>' +
    '<button class="theme-dropdown-item" data-theme-value="dark">' + iconSmallMoon + ' ダーク</button>' +
    '<button class="theme-dropdown-item" data-theme-value="system">' + iconSmallMonitor + ' システム</button>';
  btn.parentNode.appendChild(dropdown);

  function getStored() {
    return localStorage.getItem('theme') || 'system';
  }

  function resolveTheme(pref) {
    if (pref === 'system') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    return pref;
  }

  function apply(pref) {
    var resolved = resolveTheme(pref);
    document.documentElement.setAttribute('data-theme', resolved);
    localStorage.setItem('theme', pref);

    // Update button icon
    if (pref === 'system') {
      btn.innerHTML = iconMonitor;
    } else {
      btn.innerHTML = resolved === 'dark' ? iconMoon : iconSun;
    }

    // Update active state in dropdown
    var items = dropdown.querySelectorAll('.theme-dropdown-item');
    items.forEach(function (item) {
      item.classList.toggle('active', item.getAttribute('data-theme-value') === pref);
    });
  }

  apply(getStored());

  // Listen for system preference changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
    if (getStored() === 'system') {
      apply('system');
    }
  });

  // Toggle dropdown
  btn.addEventListener('click', function (e) {
    e.stopPropagation();
    dropdown.classList.toggle('open');
  });

  // Handle dropdown item clicks
  dropdown.addEventListener('click', function (e) {
    var item = e.target.closest('.theme-dropdown-item');
    if (!item) return;
    apply(item.getAttribute('data-theme-value'));
    dropdown.classList.remove('open');
  });

  // Close dropdown on outside click
  document.addEventListener('click', function () {
    dropdown.classList.remove('open');
  });
})();
