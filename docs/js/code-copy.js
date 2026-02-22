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
