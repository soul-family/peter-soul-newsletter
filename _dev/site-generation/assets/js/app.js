;(function () {
  'use strict'

  var main = document.querySelector('.main-content')
  if (!main || !window.fetch || !window.history || !window.DOMParser) {
    return
  }

  var requestId = 0

  function normalizePath(value) {
    var path = value
    try {
      path = new URL(value, window.location.origin).pathname
    } catch (error) {
      path = value
    }
    path = path.replace(/\/index\.html$/i, '/')
    path = path.replace(/\.md$/i, '')
    if (path.length > 1) {
      path = path.replace(/\/+$/, '')
    }
    try {
      path = decodeURIComponent(path)
    } catch (error) {
      return path
    }
    return path
  }

  function linkPath(link) {
    return normalizePath(link.getAttribute('href'))
  }

  function setCurrent(items, currentClass) {
    for (var i = 0; i < items.length; i++) {
      var item = items[i]
      if (item.getAttribute('data-current') === 'true') {
        item.classList.add(currentClass)
        item.setAttribute('aria-current', 'page')
      } else {
        item.classList.remove(currentClass)
        item.removeAttribute('aria-current')
      }
    }
  }

  function updateNavigation(path) {
    var current = normalizePath(path)
    var links = document.querySelectorAll('.sidebar-nav a[href]')
    for (var i = 0; i < links.length; i++) {
      links[i].setAttribute('data-current', linkPath(links[i]) === current ? 'true' : 'false')
    }
    setCurrent(links, 'nav-current')
  }

  function getHueForPath(doc, path) {
    var bars = doc.querySelectorAll('.left-bar')
    if (!bars.length) {
      return null
    }
    var bar = bars[0]
    var style = bar.getAttribute('style') || ''
    var match = style.match(/--sidebar-bg:\s*hsl\(([-0-9.]+)/i)
    if (match) {
      return match[1]
    }
    var className = bar.className || ''
    var bgMatch = className.match(/bg-([0-9]+)/)
    if (bgMatch) {
      var bgIndex = parseInt(bgMatch[1], 10) - 1
      return (bgIndex * 137) % 360
    }
    return null
  }

  function updateNewsletter(path, doc) {
    var current = normalizePath(path)
    var items = document.querySelectorAll('.newsletter-list .nl-item')
    for (var i = 0; i < items.length; i++) {
      var link = items[i].querySelector('a.nl-title')
      items[i].setAttribute('data-current', link && linkPath(link) === current ? 'true' : 'false')
    }
    setCurrent(items, 'nl-current')

    var yearLinks = document.querySelectorAll('.year-jump a')
    if (!yearLinks.length) {
      return
    }
    var currentItem = document.querySelector('.newsletter-list .nl-item.nl-current')
    var year = null
    if (currentItem) {
      var group = currentItem.closest('.nl-year-group')
      if (group) {
        year = group.getAttribute('id')
      }
    }
    if (!year && doc) {
      var docItem = doc.querySelector('.newsletter-list .nl-item.nl-current')
      if (docItem) {
        var docGroup = docItem.closest('.nl-year-group')
        if (docGroup) {
          year = docGroup.getAttribute('id')
        }
      }
    }
    var hue = null
    if (doc) {
      hue = getHueForPath(doc, path)
    }
    if (hue === null) {
      var bar = document.querySelector('.left-bar')
      if (bar) {
        var style = bar.getAttribute('style') || ''
        var match = style.match(/--sidebar-bg:\s*hsl\(([-0-9.]+)/i)
        if (match) {
          hue = match[1]
        }
      }
    }
    for (var j = 0; j < yearLinks.length; j++) {
      var linkYear = yearLinks[j].getAttribute('href')
      if (year && linkYear && linkYear === '#' + year) {
        yearLinks[j].classList.add('year-current')
        if (hue !== null) {
          yearLinks[j].style.setProperty('--year-color', 'hsl(' + hue + ', 60%, 80%)')
        } else {
          yearLinks[j].style.removeProperty('--year-color')
        }
      } else {
        yearLinks[j].classList.remove('year-current')
        yearLinks[j].style.removeProperty('--year-color')
      }
    }
  }

  function updateLeftBar(doc) {
    var currentBar = document.querySelector('.left-bar')
    var nextBar = doc.querySelector('.left-bar')
    if (!currentBar || !nextBar) {
      return
    }

    currentBar.className = nextBar.className

    var nextStyle = nextBar.getAttribute('style')
    if (nextStyle) {
      currentBar.setAttribute('style', nextStyle)
    } else {
      currentBar.removeAttribute('style')
    }

    var currentImages = currentBar.querySelector('.header-images')
    var nextImages = nextBar.querySelector('.header-images')
    if (currentImages && nextImages) {
      currentImages.innerHTML = nextImages.innerHTML
    }
  }

  function scrollToTarget(hash) {
    if (hash) {
      var id = hash.slice(1)
      try {
        id = decodeURIComponent(id)
      } catch (error) {
        id = hash.slice(1)
      }
      var target = document.getElementById(id)
      if (target) {
        target.scrollIntoView()
        return
      }
    }
    window.scrollTo(0, 0)
  }

  function applyPage(doc, url) {
    var nextMain = doc.querySelector('.main-content')
    if (!nextMain) {
      window.location.href = url
      return false
    }

    main.innerHTML = nextMain.innerHTML

    if (doc.title) {
      document.title = doc.title
    }

    updateLeftBar(doc)
    updateNavigation(url.pathname)
    updateNewsletter(url.pathname, doc)
    scrollToTarget(url.hash)

    var heading = main.querySelector('.post-title')
    if (heading) {
      heading.setAttribute('tabindex', '-1')
      heading.focus({ preventScroll: true })
    }

    return true
  }

  function load(url, pushState) {
    var id = ++requestId

    fetch(url.href, { credentials: 'same-origin' })
      .then(function (response) {
        if (!response.ok) {
          throw new Error('Request failed')
        }
        return response.text()
      })
      .then(function (html) {
        if (id !== requestId) {
          return
        }
        var doc = new DOMParser().parseFromString(html, 'text/html')
        if (!applyPage(doc, url)) {
          return
        }
        if (pushState) {
          history.pushState({ url: url.href }, '', url.href)
        }
        updateNewsletter(url.pathname, doc)
      })
      .catch(function () {
        if (id === requestId) {
          window.location.href = url.href
        }
      })
  }

  function navigableUrl(link) {
    if (!link || link.hasAttribute('download')) {
      return null
    }

    var target = link.getAttribute('target')
    if (target && target !== '_self') {
      return null
    }

    var href = link.getAttribute('href')
    if (!href || href.charAt(0) === '#' || /^(mailto:|tel:|javascript:)/i.test(href)) {
      return null
    }

    var url
    try {
      url = new URL(href, window.location.href)
    } catch (error) {
      return null
    }

    if (url.origin !== window.location.origin || !/^https?:$/.test(url.protocol)) {
      return null
    }

    if (/\.(pdf|jpe?g|png|gif|svg|webp|zip|mp4|mp3|webm|txt|xml|json)$/i.test(url.pathname)) {
      return null
    }

    if (normalizePath(url.pathname) === normalizePath(window.location.pathname) && url.search === window.location.search) {
      return null
    }

    return url
  }

  document.addEventListener('click', function (event) {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
      return
    }

    var link = event.target.closest ? event.target.closest('a') : null
    var url = navigableUrl(link)
    if (!url) {
      return
    }

    event.preventDefault()

    var rightContent = document.querySelector('.right-content')
    if (rightContent) {
      rightContent.classList.remove('open')
    }

    load(url, true)
  })

  window.addEventListener('popstate', function () {
    load(new URL(window.location.href), false)
  })

  updateNavigation(window.location.pathname)
  updateNewsletter(window.location.pathname, document)
})()
