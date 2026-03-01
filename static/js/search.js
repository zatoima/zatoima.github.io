// Search functionality
(function() {
  var searchData = null;
  var overlay = document.getElementById('search-overlay');
  var input = document.getElementById('search-input');
  var results = document.getElementById('search-results');
  var searchBtn = document.getElementById('search-btn');

  if (!overlay || !input || !results) return;

  var minCharsMsg = input ? input.getAttribute('data-min-chars') || 'Enter at least 2 characters' : 'Enter at least 2 characters';
  var noResultsMsg = input ? input.getAttribute('data-no-results') || 'No results found' : 'No results found';

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

  function loadSearchData() {
    if (searchData) return Promise.resolve(searchData);
    var lang = document.documentElement.lang || 'ja';
    var searchUrl = (lang === 'ja' || !lang) ? '/index.json' : '/' + lang + '/index.json';
    return fetch(searchUrl)
      .then(function(res) { return res.json(); })
      .then(function(data) { searchData = data; return searchData; })
      .catch(function(e) { console.error('Failed to load search data:', e); return []; });
  }

  input.addEventListener('input', function() {
    var query = this.value.trim().toLowerCase();
    if (query.length < 2) {
      results.innerHTML = '<div class="search-hint">' + minCharsMsg + '</div>';
      return;
    }

    loadSearchData().then(function(data) {
      var keywords = query.split(/\s+/);

      var matched = data.filter(function(item) {
        var text = (item.title + ' ' + item.content + ' ' + (item.tags || []).join(' ')).toLowerCase();
        return keywords.every(function(kw) { return text.indexOf(kw) !== -1; });
      }).slice(0, 20);

      if (matched.length === 0) {
        results.innerHTML = '<div class="search-hint">' + noResultsMsg + '</div>';
        return;
      }

      results.innerHTML = matched.map(function(item) {
        return '<a href="' + item.url + '" class="search-result-item">' +
          '<span class="search-result-title">' + escapeHtml(item.title) + '</span>' +
          '<span class="search-result-date">' + item.date + '</span>' +
          '</a>';
      }).join('');
    });
  });

  function escapeHtml(text) {
    var div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
})();
