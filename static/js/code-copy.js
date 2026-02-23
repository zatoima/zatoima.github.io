// Code block copy button
(function () {
  var blocks = document.querySelectorAll('.article-content pre');
  blocks.forEach(function (block) {
    // Skip if already has a button
    if (block.querySelector('.code-copy-btn')) return;

    var wrapper = document.createElement('div');
    wrapper.className = 'code-block-wrapper';
    block.parentNode.insertBefore(wrapper, block);
    wrapper.appendChild(block);

    // Language label
    var code = block.querySelector('code');
    if (code) {
      var cls = code.className || '';
      var match = cls.match(/language-(\w+)/);
      if (match) {
        var label = document.createElement('span');
        label.className = 'code-lang-label';
        label.textContent = match[1];
        wrapper.appendChild(label);
      }
    }

    // Wrap toggle button
    var wrapBtn = document.createElement('button');
    wrapBtn.className = 'code-wrap-btn';
    wrapBtn.textContent = 'Wrap';
    wrapBtn.setAttribute('aria-label', 'Toggle word wrap');
    wrapper.appendChild(wrapBtn);

    wrapBtn.addEventListener('click', function () {
      block.classList.toggle('wrapped');
      wrapBtn.classList.toggle('active');
    });

    // Copy button
    var btn = document.createElement('button');
    btn.className = 'code-copy-btn';
    btn.textContent = 'Copy';
    btn.setAttribute('aria-label', 'Copy code');
    wrapper.appendChild(btn);

    btn.addEventListener('click', function () {
      var code = block.querySelector('code');
      var text = code ? code.textContent : block.textContent;
      navigator.clipboard.writeText(text).then(function () {
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(function () {
          btn.textContent = 'Copy';
          btn.classList.remove('copied');
        }, 2000);
      });
    });
  });
})();
