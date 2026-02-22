(function () {
  var overlay = document.createElement('div');
  overlay.className = 'lightbox-overlay';
  var lbImg = document.createElement('img');
  overlay.appendChild(lbImg);
  document.body.appendChild(overlay);

  overlay.addEventListener('click', function () {
    overlay.classList.remove('active');
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      overlay.classList.remove('active');
    }
  });

  var content = document.querySelector('.article-content');
  if (!content) return;

  var imgs = content.querySelectorAll('img');
  imgs.forEach(function (img) {
    img.addEventListener('click', function (e) {
      e.preventDefault();
      lbImg.src = img.src;
      lbImg.alt = img.alt || '';
      overlay.classList.add('active');
    });
  });
})();
