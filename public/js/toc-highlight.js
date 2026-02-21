// TOC scroll-tracking highlight
(function () {
  const toc = document.querySelector('#TableOfContents');
  if (!toc) return;

  const links = toc.querySelectorAll('a');
  if (!links.length) return;

  const headings = [];
  links.forEach(function (link) {
    const id = decodeURIComponent(link.getAttribute('href').replace('#', ''));
    const heading = document.getElementById(id);
    if (heading) headings.push({ el: heading, link: link });
  });

  if (!headings.length) return;

  function updateActive() {
    var current = null;
    var scrollY = window.scrollY;

    for (var i = 0; i < headings.length; i++) {
      var top = headings[i].el.getBoundingClientRect().top + scrollY - 100;
      if (scrollY >= top) {
        current = headings[i];
      }
    }

    links.forEach(function (link) {
      link.classList.remove('toc-active');
    });

    if (current) {
      current.link.classList.add('toc-active');
    }
  }

  var ticking = false;
  window.addEventListener('scroll', function () {
    if (!ticking) {
      requestAnimationFrame(function () {
        updateActive();
        ticking = false;
      });
      ticking = true;
    }
  });

  updateActive();
})();
