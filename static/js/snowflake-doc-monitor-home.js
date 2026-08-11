(function () {
  var section = document.getElementById('snowflake-doc-monitor-summary');
  if (!section) return;

  function setText(name, value) {
    var target = section.querySelector('[data-monitor-field="' + name + '"]');
    if (target) target.textContent = value;
  }

  fetch('/snowflake-monitor/summary.json', { cache: 'no-store' })
    .then(function (response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.json();
    })
    .then(function (data) {
      setText('updated_date', data.updated_date);
      setText('new_features', data.new_features);
      setText('compared_pages', data.compared_pages);
      setText('active_pages', data.active_pages);
      setText('headline', data.headline);
      setText('summary', data.summary);
      section.classList.add('is-loaded');
    })
    .catch(function () {
      setText('summary', '最新情報を取得できませんでした。モニターページで確認してください。');
      section.classList.add('is-loaded');
    });
})();
