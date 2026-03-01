(function() {
  'use strict';

  var STORAGE_KEY = 'preferred-lang';
  var stored = localStorage.getItem(STORAGE_KEY);

  // If user already has a preference, respect it
  if (stored) return;

  // If already on /en/ path, user explicitly navigated there
  if (window.location.pathname.startsWith('/en/')) {
    localStorage.setItem(STORAGE_KEY, 'en');
    return;
  }

  // Detect browser language
  var browserLang = navigator.language || navigator.userLanguage || 'ja';

  // If browser language is Japanese, stay on current page
  if (browserLang.startsWith('ja')) {
    localStorage.setItem(STORAGE_KEY, 'ja');
    return;
  }

  // Non-Japanese browser - redirect to English home
  localStorage.setItem(STORAGE_KEY, 'en');
  window.location.href = '/en/';
})();
