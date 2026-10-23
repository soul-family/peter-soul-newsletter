(function () {
  'use strict';

  var MOBILE_BREAKPOINT = 720;
  var TABLET_BREAKPOINT = 1024;

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

  function isTablet() {
    return window.innerWidth > MOBILE_BREAKPOINT && window.innerWidth <= TABLET_BREAKPOINT;
  }

  function isCompact() {
    return isMobile() || isTablet();
  }

  function getWrapper() {
    return document.querySelector('.layout-wrapper');
  }

  function collapseSidebar() {
    var wrapper = getWrapper();
    wrapper.classList.remove('sidebar-expanded');
    wrapper.classList.remove('sidebar-pinned');
    setCookie('sidebarState', 'collapsed', 365);
  }

  function expandSidebar() {
    var wrapper = getWrapper();
    wrapper.classList.add('sidebar-expanded');
    setCookie('sidebarState', 'expanded', 365);
  }

  function toggleSidebar() {
    var wrapper = getWrapper();

    if (isTablet()) {
      var pinned = wrapper.classList.toggle('sidebar-pinned');
      setCookie('sidebarPinned', pinned ? 'pinned' : 'unpinned', 365);
      return;
    }

    if (isMobile()) {
      var open = wrapper.classList.toggle('sidebar-expanded');
      setCookie('sidebarState', open ? 'expanded' : 'collapsed', 365);
      return;
    }

    var isExpanded = wrapper.classList.toggle('sidebar-expanded');
    setCookie('sidebarState', isExpanded ? 'expanded' : 'collapsed', 365);
  }

  window.toggleNav = function () {
  var nav = document.querySelector('.topbar-nav');
  if (nav) {
    nav.classList.toggle('expanded');
  }
};

window.toggleRightSidebar = function () {
  var rightContent = document.querySelector('.right-content');
  if (rightContent) {
    rightContent.classList.toggle('open');
  }
};

window.toggleSidebar = toggleSidebar;

  function autoCollapseOnCompact() {
    var wrapper = getWrapper();
    if (isCompact()) {
      wrapper.classList.remove('sidebar-expanded');
      wrapper.classList.remove('sidebar-pinned');
    }
  }

  function handleResize() {
    var wrapper = getWrapper();
    var compact = isCompact();
    if (compact) {
      autoCollapseOnCompact();
    } else if (wrapper.classList.contains('sidebar-pinned')) {
      wrapper.classList.remove('sidebar-pinned');
      setCookie('sidebarPinned', 'unpinned', 365);
    }
  }

  function init() {
    var wrapper = getWrapper();
    var savedState = getCookie('sidebarState');

    if (isCompact()) {
      autoCollapseOnCompact();
    } else if (savedState === 'collapsed') {
      wrapper.classList.remove('sidebar-expanded');
    } else {
      wrapper.classList.add('sidebar-expanded');
    }

    var navLinks = wrapper.querySelectorAll('.sidebar-nav a[href]');
    for (var i = 0; i < navLinks.length; i++) {
      (function (link) {
        link.addEventListener('click', function () {
          if (isCompact()) {
            collapseSidebar();
          }
        });
      })(navLinks[i]);
    }

    var resizeTimer = null;
    window.addEventListener('resize', function () {
      if (resizeTimer) {
        clearTimeout(resizeTimer);
      }
      resizeTimer = setTimeout(handleResize, 150);
    });
i  }

  init();
})();
