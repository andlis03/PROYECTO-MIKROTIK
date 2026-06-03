(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var sidebarKey = 'sidebarCollapsed';
    var toggleButton = document.querySelector('[data-bs-target=".menu-text,#brandWrapper"]');
    var menuTexts = document.querySelectorAll('.menu-text');
    var brandWrapper = document.getElementById('brandWrapper');

    function setSidebarState(collapsed) {
      if (!brandWrapper || !menuTexts.length) return;
      if (collapsed) {
        brandWrapper.classList.remove('show');
        menuTexts.forEach(function (el) {
          el.classList.remove('show');
        });
        if (toggleButton) toggleButton.setAttribute('aria-expanded', 'false');
      } else {
        brandWrapper.classList.add('show');
        menuTexts.forEach(function (el) {
          el.classList.add('show');
        });
        if (toggleButton) toggleButton.setAttribute('aria-expanded', 'true');
      }
      localStorage.setItem(sidebarKey, collapsed ? 'true' : 'false');
    }

    if (localStorage.getItem(sidebarKey) === 'true') {
      setSidebarState(true);
    }

    if (brandWrapper) {
      brandWrapper.addEventListener('shown.bs.collapse', function () {
        localStorage.setItem(sidebarKey, 'false');
        if (toggleButton) toggleButton.setAttribute('aria-expanded', 'true');
      });

      brandWrapper.addEventListener('hidden.bs.collapse', function () {
        localStorage.setItem(sidebarKey, 'true');
        if (toggleButton) toggleButton.setAttribute('aria-expanded', 'false');
      });
    }
  });
})();
