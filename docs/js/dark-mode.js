// Dark mode toggle (3-way: light / dark / system)
(function () {
  var btn = document.getElementById('dark-mode-btn');
  if (!btn) return;

  var dropdown = document.createElement('div');
  dropdown.className = 'theme-dropdown';
  dropdown.innerHTML =
    '<button class="theme-dropdown-item" data-theme-value="light">☀️ ライト</button>' +
    '<button class="theme-dropdown-item" data-theme-value="dark">🌙 ダーク</button>' +
    '<button class="theme-dropdown-item" data-theme-value="system">💻 システム</button>';
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
      btn.textContent = '💻';
    } else {
      btn.textContent = resolved === 'dark' ? '☀️' : '🌙';
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
