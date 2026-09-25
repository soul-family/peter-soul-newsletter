(function () {
  'use strict';

  var MOBILE_BREAKPOINT = 720;

  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
  }

  function setCookie(name, value, days) {
    var expires = '';
    if (days) {
      var date = new Date();
      date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
      expires = '; expires=' + date.toUTCString();
    }
    document.cookie = name + '=' + value + expires + ';path=/';
  }

  function isMobile() {
    return window.innerWidth <= MOBILE_BREAKPOINT;
  }

  function collapseSidebar() {
    document.querySelector('.layout-wrapper').classList.remove('sidebar-expanded');
    setCookie('sidebarState', 'collapsed', 365);
  }

  function expandSidebar() {
    document.querySelector('.layout-wrapper').classList.add('sidebar-expanded');
    setCookie('sidebarState', 'expanded', 365);
  }

  window.toggleSidebar = function () {
    var wrapper = document.querySelector('.layout-wrapper');
    var isExpanded = wrapper.classList.toggle('sidebar-expanded');
    setCookie('sidebarState', isExpanded ? 'expanded' : 'collapsed', 365);
  };

  function init() {
    var wrapper = document.querySelector('.layout-wrapper');
    var savedState = getCookie('sidebarState');
    var startCollapsed = savedState === 'collapsed';

    if (startCollapsed) {
      wrapper.classList.remove('sidebar-expanded');
    } else {
      wrapper.classList.add('sidebar-expanded');
    }

    if (isMobile()) {
      var navLinks = wrapper.querySelectorAll('.sidebar-nav a[href]');
      for (var i = 0; i < navLinks.length; i++) {
        (function (link) {
          link.addEventListener('click', function () {
            collapseSidebar();
          });
        })(navLinks[i]);
      }
    }

    markCurrentPage();
  }

  function normalizePath(path) {
    if (path !== '/' && path.endsWith('/')) {
      return path.slice(0, -1);
    }
    return path;
  }

  function markCurrentPage() {
    var currentPath = normalizePath(window.location.pathname);
    var navLinks = document.querySelectorAll('.sidebar-nav a[href]');
    for (var i = 0; i < navLinks.length; i++) {
      var link = navLinks[i];
      var href = link.getAttribute('href');
      var linkPath = normalizePath(new URL(href, window.location.origin).pathname);
      if (currentPath === linkPath) {
        link.classList.add('nav-current');
        link.removeAttribute('href');
        link.style.pointerEvents = 'none';
        link.style.cursor = 'default';
      }
    }
  }

  init();
})();
