(function () {
  document.body.classList.add('monitor-page');

  document.body.insertAdjacentHTML('afterbegin', `
    <a href="#main" class="skip-link">メインコンテンツへスキップ</a>
    <header class="site-header">
      <div class="header-inner">
        <a href="/" class="site-logo">zatoima</a>
        <nav class="header-nav">
          <a href="/about/">About</a>
          <a href="/blog/">Blog</a>
          <a href="/index.xml">RSS</a>
          <a href="/other/">Other</a>
          <a href="/snowflake-monitor/" aria-current="page">Snowflake Monitor</a>
          <a href="/llms.txt" title="LLMs.txt - AI/LLM向けサイト情報">llms.txt</a>
        </nav>
        <div class="header-actions">
          <button id="search-btn" class="header-icon-btn" aria-label="検索">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
          </button>
          <button id="dark-mode-btn" class="header-icon-btn" aria-label="ダークモード切替" data-label-light="ライト" data-label-dark="ダーク" data-label-system="システム">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
          </button>
          <div class="lang-switcher">
            <button id="lang-btn" class="header-icon-btn" aria-label="言語を切り替え">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
            </button>
            <div id="lang-dropdown" class="lang-dropdown">
              <a href="/snowflake-monitor/" class="lang-dropdown-item active" lang="ja">日本語</a>
              <a href="/en/" class="lang-dropdown-item" lang="en">English</a>
            </div>
          </div>
          <button id="hamburger-btn" class="hamburger-btn" aria-label="メニュー"><span></span><span></span><span></span></button>
        </div>
      </div>
    </header>
    <div id="search-overlay" class="search-overlay">
      <div class="search-modal">
        <input type="text" id="search-input" class="search-input" placeholder="記事を検索... (Ctrl+K)" autocomplete="off" data-min-chars="2文字以上入力してください" data-no-results="見つかりませんでした">
        <div id="search-results" class="search-results"></div>
      </div>
    </div>
    <div id="nav-overlay" class="nav-overlay"></div>
  `);

  var content = document.querySelector('body > .wrap');
  if (content) content.id = 'main';

  document.body.insertAdjacentHTML('beforeend', `
    <footer class="site-footer">
      <div class="footer-inner">
        <div class="footer-links"><a href="/">Home</a><a href="/blog/">記事一覧</a><a href="/tags/">タグ一覧</a><a href="/about/">About</a></div>
        <div class="footer-copyright">Copyright © 2019, zatoima.</div>
        <div class="footer-disclaimer">memo blog. Hugo on GitHub Pages</div>
      </div>
    </footer>
  `);
})();
