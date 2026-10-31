/* Kipling School · Campus Satélite — interacciones del rediseño */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* sin almacenamiento */ } }
  };

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
  onScroll();

  /* ---------------------------------------------------- desktop mega menu */
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
  function closeDrawer() { if (!drawer.classList.contains('is-open')) { return; } drawer.classList.remove('is-open'); drawer.setAttribute('aria-hidden', 'true'); burger.setAttribute('aria-expanded', 'false'); unlock(); burger.focus(); }
  if (drawer && burger) {
    burger.addEventListener('click', openDrawer);
    $('[data-menu-close]', drawer).addEventListener('click', closeDrawer);
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
    window.addEventListener('resize', function () { if (window.innerWidth > 1080) { closeDrawer(); } });
  }

  /* ---------------------------------------------------- search */
  var search = $('[data-search]');
  function openSearch() { search.classList.add('is-open'); search.setAttribute('aria-hidden', 'false'); lock(); setTimeout(function () { $('input', search).focus(); }, 80); }
  function closeSearch() { if (!search.classList.contains('is-open')) { return; } search.classList.remove('is-open'); search.setAttribute('aria-hidden', 'true'); unlock(); }
  if (search) {
    $$('[data-search-open]').forEach(function (b) { b.addEventListener('click', openSearch); });
    $('[data-search-close]', search).addEventListener('click', closeSearch);
    search.addEventListener('click', function (e) { if (e.target === search) { closeSearch(); } });
  }

  /* ---------------------------------------------------- split headings */
  $$('[data-split]').forEach(function (el) {
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

  /* ---------------------------------------------------- reveal on scroll */
  var revealEls = $$('.reveal, [data-split], [data-panels]');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealEls.forEach(function (el) {
      // stagger siblings in grids
      var p = el.parentElement;
      if (p && el.classList.contains('reveal')) {
        var sib = Array.prototype.filter.call(p.children, function (c) { return c.classList.contains('reveal'); });
        var idx = sib.indexOf(el);
        if (idx > 0 && !el.style.getPropertyValue('--d')) { el.style.setProperty('--d', Math.min(idx * 90, 450) + 'ms'); }
      }
      io.observe(el);
    });
    // hero title animates immediately
    $$('.hero [data-split]').forEach(function (el) { requestAnimationFrame(function () { el.classList.add('is-in'); }); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------------------------------------------------- section panels (espacio dinámico) */
  $$('[data-panels]').forEach(function (wrap) {
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
      // on touch: first tap expands, second tap follows the link
      p.addEventListener('click', function (e) {
        if (!p.classList.contains('is-active')) { e.preventDefault(); activate(n); auto(); }
      });
    });
    activate(0);
    auto();
  });

  /* ---------------------------------------------------- sliders */
  $$('[data-slider]').forEach(function (sl) {
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
      if (reduce || sl.matches(':hover')) { return; }
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
      new IntersectionObserver(function (en) { en[0].isIntersecting ? restart() : clearTimeout(timer); }, { threshold: 0.3 }).observe(sl);
    } else { restart(); }
  });

  /* ---------------------------------------------------- lightbox */
  var lb = $('[data-lb]');
  var closeLb = function () {};
  if (lb) {
    var lbImg = $('.lb-stage img', lb);
    var lbCap = $('.lb-stage figcaption', lb);
    var lbCount = $('.lb-count', lb);
    var group = [], gi = 0, opener = null;
    function show(n) {
      gi = (n + group.length) % group.length;
      var it = group[gi];
      lbImg.classList.remove('is-loaded');
      lbImg.onload = function () { lbImg.classList.add('is-loaded'); };
      lbImg.src = it.src;
      lbImg.alt = it.alt || '';
      lbCap.textContent = it.cap || '';
      lbCount.textContent = (gi + 1) + ' / ' + group.length;
      if (lbImg.complete && lbImg.naturalWidth) { lbImg.classList.add('is-loaded'); }
    }
    function openLb(items, start, from) {
      group = items; opener = from;
      lb.classList.toggle('is-single', items.length < 2);
      lb.classList.add('is-open'); lb.setAttribute('aria-hidden', 'false'); lock();
      show(start);
      setTimeout(function () { $('[data-lb-close]', lb).focus(); }, 30);
    }
    closeLb = function () {
      if (!lb.classList.contains('is-open')) { return; }
      lb.classList.remove('is-open'); lb.setAttribute('aria-hidden', 'true'); unlock();
      lbImg.removeAttribute('src');
      if (opener) { opener.focus(); }
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

  /* ---------------------------------------------------- Come & Join modal (home) */
  var modal = $('[data-modal]');
  var KEY = 'kipling-come-join-oculto';
  function openModal() { modal.classList.add('is-open'); modal.setAttribute('aria-hidden', 'false'); lock(); setTimeout(function () { $('[data-modal-close]', modal).focus(); }, 60); }
  function closeModal() { if (!modal.classList.contains('is-open')) { return; } modal.classList.remove('is-open'); modal.setAttribute('aria-hidden', 'true'); unlock(); }
  if (modal) {
    if (!store.get(KEY) && !sessionSeen()) { setTimeout(openModal, 2600); }
    $('[data-modal-close]', modal).addEventListener('click', function () { markSession(); closeModal(); });
    $('[data-modal-never]', modal).addEventListener('click', function () { store.set(KEY, '1'); closeModal(); });
    modal.addEventListener('click', function (e) { if (e.target === modal) { markSession(); closeModal(); } });
  }
  function sessionSeen() { try { return window.sessionStorage.getItem(KEY) === '1'; } catch (e) { return false; } }
  function markSession() { try { window.sessionStorage.setItem(KEY, '1'); } catch (e) { /* sin almacenamiento */ } }

  /* ---------------------------------------------------- escape key */
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') { return; }
    if (lb && lb.classList.contains('is-open')) { closeLb(); return; }
    if (modal && modal.classList.contains('is-open')) { markSession(); closeModal(); return; }
    if (search && search.classList.contains('is-open')) { closeSearch(); return; }
    if (drawer && drawer.classList.contains('is-open')) { closeDrawer(); }
  });

  /* ---------------------------------------------------- to top */
  $$('[data-to-top]').forEach(function (b) { b.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); }); });

  /* ---------------------------------------------------- broken image guard */
  $$('img').forEach(function (im) {
    im.addEventListener('error', function () { var t = im.closest('.tile, .news-img, .logo-cell'); if (t) { t.classList.add('img-missing'); } });
  });
})();
