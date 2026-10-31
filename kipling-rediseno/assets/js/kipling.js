/* Kipling School — interacciones del rediseño
   Funciona en el sitio de varias páginas y en la edición de un solo archivo
   (body[data-spa]), donde cada página vive en un <template> y se navega con #/página. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* sin almacenamiento */ } }
  };
  var session = {
    get: function (k) { try { return window.sessionStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.sessionStorage.setItem(k, v); } catch (e) { /* sin almacenamiento */ } }
  };
  var spa = document.body.hasAttribute('data-spa');
  var main = $('#contenido');

  /* ---------------------------------------------------- scroll lock */
  var locks = 0;
  function lock() { if (locks++ === 0) { document.body.style.overflow = 'hidden'; } }
  function unlock() { if (locks > 0 && --locks === 0) { document.body.style.overflow = ''; } }

  /* ---------------------------------------------------- header + progress */
  var header = $('[data-header]');
  var bar = $('.progress span');
  var mcta = $('.m-cta');
  var lastY = window.scrollY;
  var ticking = false;
  function onScroll() {
    var y = window.scrollY;
    var max = document.documentElement.scrollHeight - window.innerHeight;
    if (bar) { bar.style.setProperty('--p', max > 0 ? Math.min(1, y / max) : 0); }
    if (header) {
      header.classList.toggle('is-scrolled', y > 40);
      var openSub = $('.has-sub.is-open');
      header.classList.toggle('is-hidden', y > 500 && y > lastY + 4 && !openSub);
      if (y < lastY - 4) { header.classList.remove('is-hidden'); }
    }
    if (mcta) { mcta.classList.toggle('is-visible', y > window.innerHeight * 0.6); }
    var hero = $('[data-hero] .hero-media img');
    if (hero && !reduce && y < window.innerHeight * 1.2) { hero.style.setProperty('--py', (y * 0.25) + 'px'); }
    lastY = y;
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { window.requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });

  /* ---------------------------------------------------- desktop mega menu */
  function closeMenus() {
    $$('[data-nav].is-open').forEach(function (li) { li.classList.remove('is-open'); $('.nav-link', li).setAttribute('aria-expanded', 'false'); });
  }
  $$('[data-nav]').forEach(function (li) {
    var btn = $('.nav-link', li);
    var closeT;
    function open() {
      clearTimeout(closeT);
      $$('[data-nav].is-open').forEach(function (o) { if (o !== li) { o.classList.remove('is-open'); $('.nav-link', o).setAttribute('aria-expanded', 'false'); } });
      li.classList.add('is-open'); btn.setAttribute('aria-expanded', 'true');
    }
    function close() { li.classList.remove('is-open'); btn.setAttribute('aria-expanded', 'false'); }
    li.addEventListener('mouseenter', open);
    li.addEventListener('mouseleave', function () { closeT = setTimeout(close, 160); });
    btn.addEventListener('click', function (e) { e.preventDefault(); li.classList.contains('is-open') ? close() : open(); });
    li.addEventListener('focusout', function (e) { if (!li.contains(e.relatedTarget)) { close(); } });
    li.addEventListener('keydown', function (e) { if (e.key === 'Escape') { close(); btn.focus(); } });
  });
  document.addEventListener('click', function (e) {
    $$('[data-nav].is-open').forEach(function (li) { if (!li.contains(e.target)) { li.classList.remove('is-open'); $('.nav-link', li).setAttribute('aria-expanded', 'false'); } });
  });

  /* ---------------------------------------------------- mobile drawer */
  var drawer = $('[data-drawer]');
  var burger = $('[data-menu-open]');
  function openDrawer() { drawer.classList.add('is-open'); drawer.setAttribute('aria-hidden', 'false'); burger.setAttribute('aria-expanded', 'true'); lock(); setTimeout(function () { var f = $('[data-menu-close]', drawer); if (f) { f.focus(); } }, 50); }
  function closeDrawer(noFocus) { if (!drawer || !drawer.classList.contains('is-open')) { return; } drawer.classList.remove('is-open'); drawer.setAttribute('aria-hidden', 'true'); burger.setAttribute('aria-expanded', 'false'); unlock(); if (!noFocus) { burger.focus(); } }
  if (drawer && burger) {
    burger.addEventListener('click', openDrawer);
    $('[data-menu-close]', drawer).addEventListener('click', function () { closeDrawer(); });
    drawer.addEventListener('click', function (e) { if (e.target === drawer) { closeDrawer(); } });
    $$('.m-item > button.m-link', drawer).forEach(function (b) {
      b.addEventListener('click', function () {
        var item = b.parentNode;
        var open = !item.classList.contains('is-open');
        $$('.m-item.is-open', drawer).forEach(function (o) { o.classList.remove('is-open'); $('button.m-link', o).setAttribute('aria-expanded', 'false'); });
        item.classList.toggle('is-open', open);
        b.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    });
    window.addEventListener('resize', function () { if (window.innerWidth > 1080) { closeDrawer(true); } });
  }

  /* ---------------------------------------------------- search (índice local, no sale del sitio) */
  var search = $('[data-search]');
  var results = $('[data-search-results]');
  var sInput = search ? $('input', search) : null;
  var root = document.body.getAttribute('data-root') || '';
  function fold(t) { return (t || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  function loadIndex(cb) {
    if (window.KIPLING_INDEX) { cb(); return; }
    var s = document.createElement('script');
    s.src = root + 'assets/js/indice.js';
    s.onload = cb;
    document.head.appendChild(s);
  }
  function runSearch() {
    if (!results) { return []; }
    var q = fold(sInput.value).trim();
    results.innerHTML = '';
    if (q.length < 2 || !window.KIPLING_INDEX) { return []; }
    var terms = q.split(/\s+/);
    var hits = window.KIPLING_INDEX.map(function (p) {
      var t = fold(p.t), x = fold(p.x), score = 0;
      for (var i = 0; i < terms.length; i++) {
        var inT = t.indexOf(terms[i]) > -1, inX = x.indexOf(terms[i]) > -1;
        if (!inT && !inX) { return null; }
        score += (inT ? 10 : 0) + (inX ? 1 : 0);
      }
      return { p: p, score: score, at: x.indexOf(terms[0]) };
    }).filter(Boolean).sort(function (a, b) { return b.score - a.score; }).slice(0, 8);
    if (!hits.length) {
      var li = document.createElement('li'); li.className = 'search-empty'; li.textContent = 'Sin resultados';
      results.appendChild(li);
      return hits;
    }
    hits.forEach(function (h) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = spa ? h.p.u : root + h.p.u;
      var b = document.createElement('b'); b.textContent = h.p.t;
      var sn = document.createElement('span');
      var start = Math.max(0, h.at - 60);
      sn.textContent = (start > 0 ? '… ' : '') + h.p.x.substr(start, 170) + '…';
      a.appendChild(b); a.appendChild(sn); li.appendChild(a); results.appendChild(li);
    });
    return hits;
  }
  function openSearch() { search.classList.add('is-open'); search.setAttribute('aria-hidden', 'false'); lock(); loadIndex(runSearch); setTimeout(function () { sInput.focus(); }, 80); }
  function closeSearch() { if (!search || !search.classList.contains('is-open')) { return; } search.classList.remove('is-open'); search.setAttribute('aria-hidden', 'true'); unlock(); }
  if (search) {
    $$('[data-search-open]').forEach(function (b) { b.addEventListener('click', openSearch); });
    $('[data-search-close]', search).addEventListener('click', closeSearch);
    search.addEventListener('click', function (e) { if (e.target === search) { closeSearch(); } });
    sInput.addEventListener('input', runSearch);
    $('[data-search-form]', search).addEventListener('submit', function (e) {
      if (!window.KIPLING_INDEX) { return; }
      e.preventDefault();
      var first = $('a', results);
      if (first) { first.click(); }
    });
    results.addEventListener('click', function (e) { if (e.target.closest('a')) { closeSearch(); } });
  }

  /* ---------------------------------------------------- in-page viewer: video, map, pdf */
  var viewer = $('[data-viewer-box]');
  function openViewer(kind, src, href) {
    var frame = $('.viewer-frame', viewer);
    frame.innerHTML = '';
    var f = document.createElement('iframe');
    f.src = src;
    f.title = kind;
    f.setAttribute('allow', 'autoplay; fullscreen; picture-in-picture');
    f.setAttribute('allowfullscreen', '');
    frame.appendChild(f);
    viewer.className = 'viewer is-open viewer-' + kind;
    viewer.setAttribute('aria-hidden', 'false');
    $('[data-viewer-out]', viewer).href = href;
    lock();
    setTimeout(function () { $('[data-viewer-close]', viewer).focus(); }, 40);
  }
  function closeViewer() {
    if (!viewer || !viewer.classList.contains('is-open')) { return; }
    viewer.classList.remove('is-open'); viewer.setAttribute('aria-hidden', 'true');
    $('.viewer-frame', viewer).innerHTML = '';
    unlock();
  }
  if (viewer) {
    $('[data-viewer-close]', viewer).addEventListener('click', closeViewer);
    viewer.addEventListener('click', function (e) { if (e.target === viewer) { closeViewer(); } });
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[data-viewer]');
      if (!a || e.metaKey || e.ctrlKey || e.shiftKey) { return; }
      e.preventDefault();
      closeMenus(); closeDrawer(true);
      openViewer(a.getAttribute('data-viewer'), a.getAttribute('data-src'), a.getAttribute('href'));
    });
  }

  /* ---------------------------------------------------- lightbox */
  var lb = $('[data-lb]');
  var closeLb = function () {};
  if (lb) {
    var lbImg = $('.lb-stage img', lb);
    var lbCap = $('.lb-stage figcaption', lb);
    var lbCount = $('.lb-count', lb);
    var group = [], gi = 0, opener = null;
    var show = function (n) {
      gi = (n + group.length) % group.length;
      var it = group[gi];
      lbImg.classList.remove('is-loaded');
      lbImg.onload = function () { lbImg.classList.add('is-loaded'); };
      lbImg.src = it.src;
      lbImg.alt = it.alt || '';
      lbCap.textContent = it.cap || '';
      lbCount.textContent = (gi + 1) + ' / ' + group.length;
      if (lbImg.complete && lbImg.naturalWidth) { lbImg.classList.add('is-loaded'); }
    };
    var openLb = function (items, start, from) {
      group = items; opener = from;
      lb.classList.toggle('is-single', items.length < 2);
      lb.classList.add('is-open'); lb.setAttribute('aria-hidden', 'false'); lock();
      show(start);
      setTimeout(function () { $('[data-lb-close]', lb).focus(); }, 30);
    };
    closeLb = function () {
      if (!lb.classList.contains('is-open')) { return; }
      lb.classList.remove('is-open'); lb.setAttribute('aria-hidden', 'true'); unlock();
      lbImg.removeAttribute('src');
      if (opener && document.contains(opener)) { opener.focus(); }
    };
    document.addEventListener('click', function (e) {
      var a = e.target.closest('[data-lightbox], [data-lightbox-dup], img[data-zoom]');
      if (!a || e.metaKey || e.ctrlKey || e.shiftKey) { return; }
      e.preventDefault();
      var items, start = 0;
      if (a.matches('img[data-zoom]')) {
        var gz = a.getAttribute('data-zoom');
        var zs = $$('img[data-zoom="' + gz + '"]');
        items = zs.map(function (im) { return { src: im.currentSrc || im.src, alt: im.alt }; });
        start = zs.indexOf(a);
      } else {
        var g = a.getAttribute('data-lightbox') || a.getAttribute('data-lightbox-dup');
        var els = $$('[data-lightbox="' + g + '"]');
        if (a.hasAttribute('data-lightbox-dup')) {
          var href = a.getAttribute('href');
          a = els.filter(function (x) { return x.getAttribute('href') === href; })[0] || a;
        }
        items = els.map(function (x) {
          var im = x.querySelector('img');
          var fc = x.parentNode && x.parentNode.querySelector('figcaption');
          return { src: x.getAttribute('href'), alt: im ? im.alt : '', cap: fc ? fc.textContent : '' };
        });
        start = Math.max(0, els.indexOf(a));
      }
      openLb(items, start, a);
    });
    $('[data-lb-close]', lb).addEventListener('click', closeLb);
    $('[data-lb-prev]', lb).addEventListener('click', function () { show(gi - 1); });
    $('[data-lb-next]', lb).addEventListener('click', function () { show(gi + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lb-stage')) { closeLb(); } });
    var lx = null;
    lb.addEventListener('touchstart', function (e) { lx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (lx === null || group.length < 2) { return; }
      var dx = e.changedTouches[0].clientX - lx;
      if (Math.abs(dx) > 50) { show(gi + (dx < 0 ? 1 : -1)); }
      lx = null;
    });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-open')) { return; }
      if (e.key === 'ArrowRight') { show(gi + 1); }
      if (e.key === 'ArrowLeft') { show(gi - 1); }
    });
  }

  /* ==================================================== per-page behaviour */
  var cleanups = [];
  var modal = null;
  var MODAL_KEY = 'kipling-come-join-oculto';
  function openModal() { if (!modal || !document.contains(modal)) { return; } modal.classList.add('is-open'); modal.setAttribute('aria-hidden', 'false'); lock(); setTimeout(function () { $('[data-modal-close]', modal).focus(); }, 60); }
  function closeModal() { if (!modal || !modal.classList.contains('is-open')) { return; } modal.classList.remove('is-open'); modal.setAttribute('aria-hidden', 'true'); unlock(); }

  function initPage(scope) {
    /* split headings */
    $$('[data-split]', scope).forEach(function (el) {
      var target = el.querySelector('a') || el;
      var words = target.textContent.trim().split(/\s+/);
      target.textContent = '';
      words.forEach(function (w, i) {
        var outer = document.createElement('span'); outer.className = 'w';
        var inner = document.createElement('span'); inner.textContent = w; inner.style.setProperty('--wi', i);
        outer.appendChild(inner); target.appendChild(outer);
        if (i < words.length - 1) { target.appendChild(document.createTextNode(' ')); }
      });
      el.setAttribute('aria-label', words.join(' '));
    });

    /* reveal on scroll */
    var revealEls = $$('.reveal, [data-split], [data-panels]', scope);
    if ('IntersectionObserver' in window && !reduce) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
      revealEls.forEach(function (el) {
        var p = el.parentElement;
        if (p && el.classList.contains('reveal')) {
          var sib = Array.prototype.filter.call(p.children, function (c) { return c.classList.contains('reveal'); });
          var idx = sib.indexOf(el);
          if (idx > 0 && !el.style.getPropertyValue('--d')) { el.style.setProperty('--d', Math.min(idx * 90, 450) + 'ms'); }
        }
        io.observe(el);
      });
      $$('.hero [data-split]', scope).forEach(function (el) { requestAnimationFrame(function () { el.classList.add('is-in'); }); });
      cleanups.push(function () { io.disconnect(); });
    } else {
      revealEls.forEach(function (el) { el.classList.add('is-in'); });
    }

    /* section panels (espacio dinámico) */
    $$('[data-panels]', scope).forEach(function (wrap) {
      var panels = $$('.panel', wrap);
      var idx = 0, timer = null, hovering = false;
      function activate(i) {
        idx = (i + panels.length) % panels.length;
        panels.forEach(function (p, n) { p.classList.toggle('is-active', n === idx); });
      }
      function auto() {
        clearInterval(timer);
        if (reduce) { return; }
        timer = setInterval(function () { if (!hovering && !document.hidden) { activate(idx + 1); } }, 4200);
      }
      panels.forEach(function (p, n) {
        p.addEventListener('mouseenter', function () { hovering = true; activate(n); });
        p.addEventListener('mouseleave', function () { hovering = false; });
        p.addEventListener('focus', function () { activate(n); });
        // en pantallas táctiles: el primer toque abre el panel, el segundo sigue el enlace
        p.addEventListener('click', function (e) {
          if (!p.classList.contains('is-active')) { e.preventDefault(); activate(n); auto(); }
        });
      });
      activate(0);
      auto();
      cleanups.push(function () { clearInterval(timer); });
    });

    /* sliders */
    $$('[data-slider]', scope).forEach(function (sl) {
      var slides = $$('[data-slide]', sl);
      var dots = $$('[data-dot]', sl);
      var count = $('.slider-count b', sl);
      var barSpan = $('.slider-bar span', sl);
      var i = 0, timer = null, dur = 6000;
      sl.style.setProperty('--dur', dur + 'ms');
      function go(n) {
        i = (n + slides.length) % slides.length;
        slides.forEach(function (s, k) {
          s.classList.toggle('is-active', k === i);
          var img = $('img', s);
          if (img && (k === i || k === (i + 1) % slides.length)) { img.loading = 'eager'; }
        });
        dots.forEach(function (d, k) { d.classList.toggle('is-active', k === i); });
        if (count) { count.textContent = (i + 1 < 10 ? '0' : '') + (i + 1); }
        restart();
      }
      function restart() {
        clearTimeout(timer);
        if (barSpan) { sl.classList.remove('is-playing'); void barSpan.offsetWidth; }
        if (reduce || sl.matches(':hover') || !document.contains(sl)) { return; }
        sl.classList.add('is-playing');
        timer = setTimeout(function () { go(i + 1); }, dur);
      }
      $('[data-prev]', sl).addEventListener('click', function () { go(i - 1); });
      $('[data-next]', sl).addEventListener('click', function () { go(i + 1); });
      dots.forEach(function (d) { d.addEventListener('click', function () { go(+d.getAttribute('data-dot')); }); });
      sl.addEventListener('mouseenter', function () { clearTimeout(timer); sl.classList.remove('is-playing'); });
      sl.addEventListener('mouseleave', restart);
      var x0 = null;
      sl.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
      sl.addEventListener('touchend', function (e) {
        if (x0 === null) { return; }
        var dx = e.changedTouches[0].clientX - x0;
        if (Math.abs(dx) > 40) { go(i + (dx < 0 ? 1 : -1)); }
        x0 = null;
      });
      if ('IntersectionObserver' in window) {
        var so = new IntersectionObserver(function (en) { en[0].isIntersecting ? restart() : clearTimeout(timer); }, { threshold: 0.3 });
        so.observe(sl);
        cleanups.push(function () { so.disconnect(); });
      } else { restart(); }
      cleanups.push(function () { clearTimeout(timer); });
    });

    /* Come & Join (inicio) */
    modal = $('[data-modal]', scope);
    if (modal) {
      var m = modal;
      if (!store.get(MODAL_KEY) && !session.get(MODAL_KEY)) {
        var mt = setTimeout(openModal, 2600);
        cleanups.push(function () { clearTimeout(mt); });
      }
      $('[data-modal-close]', m).addEventListener('click', function () { session.set(MODAL_KEY, '1'); closeModal(); });
      $('[data-modal-never]', m).addEventListener('click', function () { store.set(MODAL_KEY, '1'); closeModal(); });
      m.addEventListener('click', function (e) { if (e.target === m) { session.set(MODAL_KEY, '1'); closeModal(); } });
      // el enlace "Agenda tu visita" del aviso navega dentro del sitio: cerrar primero
      $$('a', m).forEach(function (a) { a.addEventListener('click', function () { session.set(MODAL_KEY, '1'); closeModal(); }); });
    }

    /* broken image guard */
    $$('img', scope).forEach(function (im) {
      im.addEventListener('error', function () { var t = im.closest('.tile, .news-img, .logo-cell'); if (t) { t.classList.add('img-missing'); } });
    });

    /* formulario de solicitud (FormAssembly ajusta su altura con este script) */
    if ($('#formassembly_form', scope) && !window.__tfaHelper) {
      window.__tfaHelper = true;
      var s = document.createElement('script');
      s.src = 'https://nordangliaeducation.tfaforms.net/js/iframe_resize_helper.js';
      s.async = true;
      document.body.appendChild(s);
    }
  }

  /* ---------------------------------------------------- single-file router */
  var current = null;
  function render(slug) {
    var tpl = $('template[data-page="' + slug + '"]') || $('template[data-page=""]');
    if (!tpl) { return; }
    var key = tpl.getAttribute('data-page');
    if (key === current) { return; }
    current = key;
    cleanups.forEach(function (fn) { try { fn(); } catch (e) { /* ignore */ } });
    cleanups = [];
    closeModal(); closeLb(); closeViewer(); closeSearch(); closeDrawer(true); closeMenus();
    main.innerHTML = '';
    main.appendChild(document.importNode(tpl.content, true));
    document.title = tpl.getAttribute('data-title');
    document.body.className = tpl.getAttribute('data-cls');
    window.scrollTo(0, 0);
    if (header) { header.classList.remove('is-hidden'); }
    initPage(main);
    onScroll();
  }
  function route() {
    var h = window.location.hash;
    if (h && h.indexOf('#/') !== 0) { return; }
    render(h ? h.slice(2).split(/[?#]/)[0] : '');
  }

  /* in-page anchors (#accesos, #contenido) scroll without touching the route */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) { return; }
    var h = a.getAttribute('href');
    if (h.indexOf('#/') === 0 || h === '#') {
      if (h === '#' && !a.hasAttribute('data-viewer-out')) { e.preventDefault(); }
      return;
    }
    var t = document.getElementById(h.slice(1));
    if (t) { e.preventDefault(); t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' }); }
  });

  if (spa) {
    window.addEventListener('hashchange', route);
    route();
  } else {
    initPage(document);
  }
  onScroll();

  /* ---------------------------------------------------- escape key */
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') { return; }
    if (lb && lb.classList.contains('is-open')) { closeLb(); return; }
    if (viewer && viewer.classList.contains('is-open')) { closeViewer(); return; }
    if (modal && modal.classList.contains('is-open')) { session.set(MODAL_KEY, '1'); closeModal(); return; }
    if (search && search.classList.contains('is-open')) { closeSearch(); return; }
    if (drawer && drawer.classList.contains('is-open')) { closeDrawer(); }
  });

  /* ---------------------------------------------------- to top */
  $$('[data-to-top]').forEach(function (b) { b.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); }); });
})();
