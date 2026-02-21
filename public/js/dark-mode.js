// Dark mode toggle
(function() {
  var btn = document.getElementById('dark-mode-btn');
  if (!btn) return;

  function getPreferred() {
    var stored = localStorage.getItem('theme');
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function apply(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    btn.textContent = theme === 'dark' ? '☀️' : '🌙';
  }

  apply(getPreferred());

  btn.addEventListener('click', function() {
    var current = document.documentElement.getAttribute('data-theme');
    apply(current === 'dark' ? 'light' : 'dark');
  });
})();
