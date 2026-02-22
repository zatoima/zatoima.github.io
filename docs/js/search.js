// Search functionality
(function() {
  let searchData = null;
  const overlay = document.getElementById('search-overlay');
  const input = document.getElementById('search-input');
  const results = document.getElementById('search-results');
  const searchBtn = document.getElementById('search-btn');

  if (!overlay || !input || !results) return;

  function openSearch() {
    overlay.classList.add('active');
    input.value = '';
    results.innerHTML = '';
    input.focus();
  }

  function closeSearch() {
    overlay.classList.remove('active');
  }

  searchBtn.addEventListener('click', function(e) {
    e.preventDefault();
    openSearch();
  });

  overlay.addEventListener('click', function(e) {
    if (e.target === overlay) closeSearch();
  });

  document.addEventListener('keydown', function(e) {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      openSearch();
    }
    if (e.key === 'Escape') closeSearch();
  });

  async function loadSearchData() {
    if (searchData) return searchData;
    try {
      const res = await fetch('/index.json');
      searchData = await res.json();
      return searchData;
    } catch (e) {
      console.error('Failed to load search data:', e);
      return [];
    }
  }

  input.addEventListener('input', async function() {
    const query = this.value.trim().toLowerCase();
    if (query.length < 2) {
      results.innerHTML = '<div class="search-hint">2文字以上入力してください</div>';
      return;
    }

    const data = await loadSearchData();
    const keywords = query.split(/\s+/);

    const matched = data.filter(function(item) {
      const text = (item.title + ' ' + item.content + ' ' + (item.tags || []).join(' ')).toLowerCase();
      return keywords.every(function(kw) { return text.indexOf(kw) !== -1; });
    }).slice(0, 20);

    if (matched.length === 0) {
      results.innerHTML = '<div class="search-hint">見つかりませんでした</div>';
      return;
    }

    results.innerHTML = matched.map(function(item) {
      return '<a href="' + item.url + '" class="search-result-item">' +
        '<span class="search-result-title">' + escapeHtml(item.title) + '</span>' +
        '<span class="search-result-date">' + item.date + '</span>' +
        '</a>';
    }).join('');
  });

  function escapeHtml(text) {
    var div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
})();
