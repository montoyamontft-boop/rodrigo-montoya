(() => {
  'use strict';

  const D = window.CHINOIN;
  const CAT = window.CHINOIN_CATALOGO || [];
  const FICHAS = window.CHINOIN_FICHAS || {};
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const norm = (s) => String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

  /* ---------- Íconos (equivalentes a los del menú original) ---------- */
  const ICON = {
    file: '<svg viewBox="0 0 24 24" class="fill"><path d="M6 2h8l6 6v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2Zm7 1.5V9h5.5L13 3.5ZM11 11v3H8v2h3v3h2v-3h3v-2h-3v-3h-2Z" fill-rule="evenodd"/></svg>',
    house: '<svg viewBox="0 0 24 24" class="fill"><path d="M12 2.5 1.5 11.2l1.3 1.5L4 11.7V21h16v-9.3l1.2 1 1.3-1.5L19 8.3V4h-3v1.8L12 2.5Zm-1 9V14H8.5v2H11v2.5h2V16h2.5v-2H13v-2.5h-2Z" fill-rule="evenodd"/></svg>',
    apple: '<svg viewBox="0 0 24 24" class="fill"><path d="M15.6 2.2c.1 1.2-.4 2.3-1.1 3.1-.8.8-1.8 1.3-2.8 1.2-.1-1.1.4-2.3 1.1-3 .8-.8 1.9-1.3 2.8-1.3ZM12 8.2c1-.5 2.4-1 3.6-1 2 0 3.6 1.1 4.4 2.7-3.7 2-3 7 .6 8.3-.9 2.2-2.6 4.6-4.4 4.6-1.4 0-1.8-.8-3.6-.8s-2.3.8-3.6.8C6.4 22.8 3.4 18.2 3.4 13.6c0-3.6 2.3-6.4 5.2-6.4 1.3 0 2.5.6 3.4 1Z"/></svg>',
    teeth: '<svg viewBox="0 0 24 24" class="fill"><path d="M5 6h14a3 3 0 0 1 3 3v6a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3V9a3 3 0 0 1 3-3Zm.5 2.5a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1a1 1 0 0 0-1-1h-1Zm4 0a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1a1 1 0 0 0-1-1h-1Zm4 0a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1a1 1 0 0 0-1-1h-1Zm4 0a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1a1 1 0 0 0-1-1h-1Zm-12 4a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1a1 1 0 0 0-1-1h-1Zm4 0a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1a1 1 0 0 0-1-1h-1Zm4 0a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1a1 1 0 0 0-1-1h-1Zm4 0a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1a1 1 0 0 0-1-1h-1Z" fill-rule="evenodd"/></svg>',
    paw: '<svg viewBox="0 0 24 24" class="fill"><ellipse cx="5" cy="10.5" rx="2.2" ry="2.8"/><ellipse cx="9.3" cy="5.8" rx="2.3" ry="3"/><ellipse cx="14.7" cy="5.8" rx="2.3" ry="3"/><ellipse cx="19" cy="10.5" rx="2.2" ry="2.8"/><path d="M12 11c2.4 0 4 2.3 5.4 4.4 1 1.6.9 3.8-.9 4.6-1.4.6-2.8-.4-4.5-.4s-3.1 1-4.5.4c-1.8-.8-1.9-3-.9-4.6C8 13.3 9.6 11 12 11Z"/></svg>',
    chev: '<svg viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg>',
    arrow: '<svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    back: '<svg viewBox="0 0 24 24"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>',
    diag: '<svg viewBox="0 0 24 24"><path d="M7 17 17 7M8 7h9v9"/></svg>',
    down: '<svg viewBox="0 0 24 24"><path d="M12 5v14M6 13l6 6 6-6"/></svg>',
    ext: '<svg viewBox="0 0 24 24"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>',
    lock: '<svg viewBox="0 0 24 24"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>',
    search: '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    close: '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></svg>',
    phone: '<svg viewBox="0 0 24 24"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2Z"/></svg>',
    mail: '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    pin: '<svg viewBox="0 0 24 24"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    book: '<svg viewBox="0 0 24 24"><path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2V5Z"/><path d="M4 19a2 2 0 0 1 2-2h13"/></svg>',
    play: '<svg viewBox="0 0 24 24" class="fill"><path d="M8 5v14l11-7z"/></svg>',
    alert: '<svg viewBox="0 0 24 24"><path d="M12 3 2 21h20L12 3Z"/><path d="M12 10v5M12 18h.01"/></svg>',
    info: '<svg viewBox="0 0 24 24" class="fill"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm-1 9v6h2v-6h-2Zm0-4v2h2V7h-2Z" fill-rule="evenodd"/></svg>',
    linkedin: '<svg viewBox="0 0 24 24" class="fill"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9.75h4V21H3V9.75Zm6.5 0h3.8v1.6h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1V21h-4v-4.95c0-1.18-.02-2.7-1.65-2.7-1.65 0-1.9 1.29-1.9 2.62V21h-4V9.75Z"/></svg>',
    x: '<svg viewBox="0 0 24 24" class="fill"><path d="M17.8 3h3.1l-6.8 7.8 8 10.2h-6.3l-4.9-6.4L5.3 21H2.2l7.3-8.3L1.9 3h6.4l4.4 5.9L17.8 3Zm-1.1 16.2h1.7L7.4 4.7H5.6l11.1 14.5Z"/></svg>',
    facebook: '<svg viewBox="0 0 24 24" class="fill"><path d="M14 8.5V6.8c0-.8.2-1.3 1.4-1.3H17V2.2C16.6 2.1 15.4 2 14.1 2 11.3 2 9.6 3.7 9.6 6.6v1.9H6.8v3.7h2.8V22H14v-9.8h2.8l.4-3.7H14Z"/></svg>',
    youtube: '<svg viewBox="0 0 24 24" class="fill"><path d="M23 12s0-3.6-.46-5.33a2.78 2.78 0 0 0-1.95-1.96C18.88 4.25 12 4.25 12 4.25s-6.88 0-8.59.46a2.78 2.78 0 0 0-1.95 1.96C1 8.4 1 12 1 12s0 3.6.46 5.33a2.78 2.78 0 0 0 1.95 1.96c1.71.46 8.59.46 8.59.46s6.88 0 8.59-.46a2.78 2.78 0 0 0 1.95-1.96C23 15.6 23 12 23 12Zm-13.25 3.27V8.73L15.5 12l-5.75 3.27Z"/></svg>'
  };

  /* ---------- Índices del catálogo ---------- */
  const GRUPOS = ['Cuidado de la salud', 'Áreas Terapéuticas', 'Probióticos', 'Odontología'];
  const PADECIMIENTOS = D.cuidado.cards;
  const padLabel = (id) => (PADECIMIENTOS.find((p) => p.id === id) || {}).label || id;
  const findProduct = (id) => CAT.find((p) => p.id === id);
  const host = (u) => { try { return new URL(u).hostname.replace(/^www\./, ''); } catch (e) { return ''; } };

  // Qué hace el botón de cada producto, según a dónde lleva en el sitio original.
  function destino(p) {
    const h = p.href;
    if (D.fichasPorProducto[p.id]) return { tipo: 'ficha', fichas: D.fichasPorProducto[p.id] };
    if (!h) return { tipo: 'ninguno' };
    if (/chinoin\.com\/es\/gelan-plus/.test(h)) return { tipo: 'roto', href: h };
    if (/chinoin\.com/.test(h)) return { tipo: 'registro', href: h };
    return { tipo: 'externo', href: h, sitio: host(h) };
  }

  const disc = (cls, style) => `<span class="disc ${cls || ''}" style="${style}"></span>`;
  const capsule = (style) => `<span class="capsule" style="${style}"></span>`;
  const img = (src, alt, cls = '', extra = '') => `<img src="${esc(src)}" alt="${esc(alt)}" loading="lazy" decoding="async" class="${cls}" ${extra}>`;
  const ext = (href, html, cls = '') => `<a href="${esc(href)}" target="_blank" rel="noopener" class="${cls}">${html}</a>`;

  /* ============================================================
     Header, mega menú y menú móvil
     ============================================================ */
  function megaHTML() {
    const col = (g) => `
      <div class="mega-group">
        <span class="icon-bubble">${ICON[g.icon]}</span>
        <h3><a href="${g.route}">${g.label}</a></h3>
        ${g.items.length ? `<ul>${g.items.map((c) => `<li><a href="${c.route}">${c.label}</a></li>`).join('')}</ul>` : ''}
      </div>`;
    const [areas, bene, odonto, vet, cuidado] = D.megaGroups;
    return `
      <div class="mega" role="menu">
        <div class="mega-stack">${col(areas)}${col(bene)}${col(odonto)}${col(vet)}</div>
        ${col(cuidado)}
        <a class="mega-feature" href="${D.megaPromo.route}">
          ${disc('glass float', 'width:150px;height:150px;top:-40px;right:-30px;--dur:7s')}
          <img class="mega-100" src="${D.megaPromo.img}" alt="logo 100 chinoin">
          <p>${D.megaPromo.text}</p>
          <span class="btn light" style="align-self:flex-start">Conoce nuestra historia <span class="arrow">${ICON.arrow}</span></span>
        </a>
        <a class="mega-all" href="#/catalogo">${ICON.search} Ver todo el catálogo de productos ${ICON.arrow}</a>
      </div>`;
  }

  function renderNav() {
    const nav = $('.main-nav');
    nav.innerHTML = D.nav.map((item) => {
      if (item.href) return `<div class="nav-item"><a class="nav-link portal" href="${item.href}">${item.label}</a></div>`;
      const panel = item.mega ? megaHTML() : `
        <div class="dropdown" role="menu">
          ${item.items.map((s) => `<a role="menuitem" href="${s.route}">${s.label}${ICON.arrow}</a>`).join('')}
        </div>`;
      return `
        <div class="nav-item" data-key="${item.key}">
          <button class="nav-link" aria-expanded="false" aria-haspopup="true">${item.label}${ICON.chev}</button>
          ${panel}
        </div>`;
    }).join('');

    let closeTimer;
    const items = $$('.nav-item[data-key]', nav);
    const close = (except) => items.forEach((i) => {
      if (i === except) return;
      i.classList.remove('is-open');
      $('.nav-link', i).setAttribute('aria-expanded', 'false');
    });
    const open = (i) => { close(i); i.classList.add('is-open'); $('.nav-link', i).setAttribute('aria-expanded', 'true'); };
    items.forEach((i) => {
      i.addEventListener('mouseenter', () => { clearTimeout(closeTimer); open(i); });
      i.addEventListener('mouseleave', () => { closeTimer = setTimeout(() => close(), 220); });
      $('.nav-link', i).addEventListener('click', () => (i.classList.contains('is-open') ? close() : open(i)));
      i.addEventListener('click', (e) => { if (e.target.closest('a')) close(); });
    });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
    document.addEventListener('click', (e) => { if (!e.target.closest('.main-nav')) close(); });
  }

  function renderMobile() {
    const menu = $('#mobile-menu');
    const toggle = $('.menu-toggle');
    menu.innerHTML = D.nav.map((item) => {
      if (item.href) return `<a class="portal" href="${item.href}">${item.label}</a>`;
      const inner = item.mega
        ? `<a href="#/catalogo"><strong>Catálogo de productos</strong></a>` + D.megaGroups.map((g) => `<h4><a href="${g.route}">${g.label}</a></h4>${g.items.map((c) => `<a href="${c.route}">${c.label}</a>`).join('')}`).join('')
        : (item.route ? `<a href="${item.route}"><strong>${item.label}</strong></a>` : '') + item.items.map((s) => `<a href="${s.route}">${s.label}</a>`).join('');
      return `<details><summary>${item.label}${ICON.chev}</summary><div class="m-sub">${inner}</div></details>`;
    }).join('');
    const set = (on) => {
      menu.hidden = !on;
      toggle.setAttribute('aria-expanded', String(on));
      toggle.setAttribute('aria-label', on ? 'Cerrar menú' : 'Abrir menú');
      document.body.style.overflow = on ? 'hidden' : '';
    };
    toggle.addEventListener('click', () => set(menu.hidden));
    menu.addEventListener('click', (e) => { if (e.target.closest('a')) set(false); });
    matchMedia('(min-width: 1021px)').addEventListener('change', (e) => e.matches && set(false));
  }

  function renderFooter() {
    const F = D.footer;
    $('.site-footer').innerHTML = `
      <div class="wrap footer-grid">
        <div class="footer-brand">
          <img src="${F.logo}" alt="CHINOIN Experiencia que da vida" width="140" height="140">
          <p>${F.about}</p>
          <div class="social">${D.links.social.map((s) => ext(s.href, ICON[s.icon], 'social-link" aria-label="' + s.label)).join('')}</div>
        </div>
        ${F.cols.map((c) => `<div><h4>${c.title}</h4><ul>${c.links.map((l) => `<li><a href="${l.route}">${l.label}</a></li>`).join('')}</ul></div>`).join('')}
        <div class="footer-contact">
          ${F.direcciones.map((d) => `<p><strong>${d.title}</strong> ${d.text}</p>`).join('')}
          <p>${F.tel}</p>
          <p><a href="mailto:${F.email}">${F.email}</a></p>
        </div>
      </div>
      <div class="wrap footer-base">
        <span>${F.copy}</span>
        <span class="cofepris">${F.cofepris}</span>
        <span><a href="#/contacto">Contacto</a> · <a href="#/aviso-de-privacidad">Aviso de Privacidad</a></span>
      </div>`;
  }

  /* ============================================================
     Piezas compartidas
     ============================================================ */
  function heroScene(dense) {
    return `
      <div class="hero-scene" aria-hidden="true">
        <div class="layer" data-depth="10">
          ${disc('float', 'width:min(34vw,460px);height:min(34vw,460px);left:54%;top:14%;--dur:11s;--dy:-30px;--r1:12deg')}
          ${dense ? disc('glass float', 'width:180px;height:180px;left:86%;top:58%;--dur:8s;--dy:24px') : ''}
        </div>
        <div class="layer" data-depth="26">
          ${disc('glass float', 'width:min(26vw,340px);height:min(26vw,340px);left:72%;top:4%;--dur:9s;--dx:-20px;--r1:-10deg')}
          ${capsule('width:min(22vw,280px);height:min(8vw,100px);left:60%;top:64%;rotate:-28deg')}
        </div>
        <div class="layer" data-depth="48">
          ${disc('float', 'width:90px;height:90px;left:50%;top:10%;--dur:6s;--dy:18px')}
          ${dense ? capsule('width:150px;height:54px;left:88%;top:28%;rotate:52deg') : ''}
          ${disc('glass float', 'width:60px;height:60px;left:64%;top:50%;--dur:5s')}
        </div>
      </div>`;
  }

  // Encabezado de página interna; usa la foto de encabezado del original cuando existe.
  function pageHero({ kicker, title, intro, crumbs = [], photo, sub, compact }) {
    return `
      <section class="page-hero${photo ? ' has-photo' : ''}${compact ? ' compact' : ''}">
        ${photo ? `<div class="ph-photo" style="background-image:url('${photo}')"></div>` : ''}
        <div class="hero-bg"></div>
        <div class="hero-grain"></div>
        ${photo ? '' : heroScene(false)}
        <div class="wrap">
          <nav class="crumbs" aria-label="Ruta"><a href="#/">Inicio</a>${crumbs.map((c) => `<span aria-hidden="true">/</span>${c.route ? `<a href="${c.route}">${c.label}</a>` : `<span>${c.label}</span>`}`).join('')}</nav>
          ${kicker ? `<span class="kicker">${kicker}</span>` : ''}
          <h1 class="h-display">${title}</h1>
          ${intro ? `<p class="page-intro">${intro}</p>` : ''}
          ${sub || ''}
        </div>
      </section>`;
  }

  const subnav = (items, current) => `<div class="subnav">${items.map((s) => `<a href="${s.route}"${s.route === current ? ' aria-current="page"' : ''}>${s.label}</a>`).join('')}</div>`;

  const pendingNote = (title, text) => `
    <div class="pending reveal">
      <span class="icon-bubble">${ICON.info}</span>
      <div><strong>${title}</strong><p>${text}</p></div>
    </div>`;

  function productCard(p, i = 0) {
    const d = destino(p);
    const badge = d.tipo === 'registro' ? `<span class="pc-badge">${ICON.lock} Profesionales de la salud</span>`
      : d.tipo === 'externo' ? `<span class="pc-badge ext">${ICON.ext} ${esc(d.sitio)}</span>`
        : d.tipo === 'ficha' ? `<span class="pc-badge info">${ICON.file} Ficha completa</span>` : '';
    return `
      <a class="product-card" href="#/producto/${p.id}" style="--i:${i}" data-id="${p.id}">
        <div class="shot">${img(p.img, p.name)}</div>
        <div class="meta">
          <div class="pc-tags">${[...p.padecimientos.map(padLabel), ...p.grupos].slice(0, 2).map((t) => `<span>${esc(t)}</span>`).join('')}</div>
          <h3>${esc(p.name)}</h3>
          ${badge}
        </div>
        <span class="pc-go">${ICON.arrow}</span>
      </a>`;
  }

  /* ============================================================
     Portada
     ============================================================ */
  function viewHome() {
    const H = D.home;
    const units = D.unidades.items;
    const featured = ['antiflu-des-capsulas', 'troferit-jarabe', 'neoseverin-tabletas', 'topron-capsulas', 'anara-tabletas', 'gelan-plus-gel', 'scabisan-shampoo', 'feel-360-tabletas', 'gotinal-mar-defense', 'benei-g-capsulas', 'flexakocs-capsulas', 'alin-depot']
      .map(findProduct).filter(Boolean);
    const pads = PADECIMIENTOS.map((p) => `<a href="#/${p.id}">${p.label}</a>`).join('');

    return `
      <section class="hero">
        <div class="hero-bg"></div>
        ${heroScene(true)}
        <div class="hero-grain"></div>
        <div class="wrap hero-inner">
          <div class="hero-copy">
            <span class="kicker">CHINOIN® · 100 años</span>
            <h1 class="h-display">
              <span class="line"><span>Farmacéutica</span></span>
              <span class="line"><span><em>Mexicana</em></span></span>
            </h1>
            <p class="hero-sub">${H.intro}</p>
            <div class="hero-ctas">
              <a class="btn magnetic" href="#/catalogo">Catálogo de productos <span class="arrow">${ICON.arrow}</span></a>
              <a class="btn ghost magnetic" href="portal-medico.html">Portal Médico</a>
            </div>
          </div>
          <div class="hero-side">
            <div class="stat-card solid"><div class="num"><span data-count="100">100</span></div><div class="lbl"><span>años de historia</span></div></div>
            <div class="stat-card"><div class="num"><span data-count="3">3</span></div><div class="lbl"><span>plantas: CDMX, Aguascalientes y Colombia</span></div></div>
          </div>
        </div>
        <div class="hero-giant" aria-hidden="true" data-parallax="-0.12">100 años</div>
        <div class="hero-bar">
          <div class="wrap"><span>${D.megaPromo.text}</span><a class="scroll-hint" href="#banners">Descubre más <i>${ICON.down}</i></a></div>
        </div>
      </section>
      <div class="marquee" aria-label="Padecimientos"><div class="marquee-track">${pads}${pads}${pads}</div></div>

      <section class="banners" id="banners">
        <div class="wrap">
          <div class="slider reveal" data-slider>
            <div class="slides">${H.banners.map((b, i) => `<${b.route ? `a href="${b.route}"` : 'div'} class="slide${i ? '' : ' is-active'}">${img(b.img, b.alt, '', i ? '' : 'loading="eager"')}</${b.route ? 'a' : 'div'}>`).join('')}</div>
            <div class="slider-ui">
              <button class="sl-prev" aria-label="Anterior">${ICON.back}</button>
              <div class="sl-dots">${H.banners.map((_, i) => `<button aria-label="Banner ${i + 1}"${i ? '' : ' aria-current="true"'}><i></i></button>`).join('')}</div>
              <button class="sl-next" aria-label="Siguiente">${ICON.arrow}</button>
            </div>
          </div>
        </div>
      </section>

      <section class="section qa">
        <div class="wrap qa-grid">
          <div class="qa-visual reveal">
            <div class="qa-ring">${img(H.experienciaImg, 'chinoin-experiencia')}</div>
          </div>
          <div>
            <span class="kicker reveal">Nosotros</span>
            <h2 class="h-section reveal">${H.h1.replace('Mexicana', '<em>Mexicana</em>')}</h2>
            <div class="qa-list">
              ${H.preguntas.map((q, i) => `
                <details class="qa-item reveal" style="--d:${i * 0.08}s"${i === 0 ? ' open' : ''}>
                  <summary><span class="qa-n">0${i + 1}</span><span>${q.q}</span><i>${ICON.chev}</i></summary>
                  <p>${q.a}</p>
                </details>`).join('')}
            </div>
          </div>
        </div>
      </section>

      <section class="section pillars">
        <div class="wrap pillars-grid">
          <div>
            <span class="kicker reveal">Círculo Dorado</span>
            <h2 class="h-section reveal">${H.pilares.title.replace('pilares', '<em>pilares</em>')}</h2>
            ${H.pilares.p.map((p) => `<p class="lead reveal">${p}</p>`).join('')}
          </div>
          <div class="wheel reveal" data-wheel>
            <div class="wheel-core">${img('assets/chinoin-simbolo.png', 'CHINOIN')}<span data-wheel-label>${H.pilares.items[0].label}</span></div>
            ${H.pilares.items.map((p, i) => `<${p.route ? `a href="${p.route}"` : 'button type="button"'} class="wheel-item${i ? '' : ' is-active'}" style="--a:${i * 72 - 90}deg" data-i="${i}"><span>${p.label}</span></${p.route ? 'a' : 'button'}>`).join('')}
            <svg class="wheel-ring" viewBox="0 0 200 200" aria-hidden="true"><circle cx="100" cy="100" r="86"/></svg>
          </div>
        </div>
      </section>

      <section class="section shelf" id="productos">
        <div class="wrap">
          <div class="section-head">
            <div class="reveal"><span class="kicker">Productos</span><h2 class="h-section">Conoce nuestro <em>catálogo</em></h2></div>
            <a class="btn purple magnetic reveal" href="#/catalogo">Ver todo el catálogo <span class="arrow">${ICON.arrow}</span></a>
          </div>
        </div>
        <div class="rail" data-rail>
          <div class="rail-track">${featured.map((p, i) => productCard(p, i)).join('')}</div>
        </div>
        <div class="wrap">
          <div class="quick-cats">
            ${D.megaGroups.map((g) => `<a class="quick-cat reveal" href="${g.route}"><span class="icon-bubble">${ICON[g.icon]}</span><span>${g.label}</span>${ICON.arrow}</a>`).join('')}
          </div>
        </div>
      </section>

      <section class="section presence">
        <div class="wrap presence-grid">
          <div class="presence-map reveal">${img(H.presencia.img, 'chinoin-en-america')}
            <span class="ping" style="left:41%;top:52%"></span><span class="ping" style="left:47%;top:55%;--d:.6s"></span><span class="ping" style="left:60%;top:73%;--d:1.2s"></span>
          </div>
          <div>
            <span class="kicker reveal">${H.presencia.title}</span>
            <h2 class="h-section reveal"><em>Presencia</em> en México y Latinoamérica</h2>
            ${H.presencia.p.map((p) => `<p class="lead reveal">${p}</p>`).join('')}
            <div class="presence-stats reveal">
              <div><b data-count="3">3</b><span>plantas</span></div>
              <div><b data-count="8">8</b><span>países en Centro y Sudamérica</span></div>
              <div><b data-count="100">100</b><span>años de experiencia</span></div>
            </div>
          </div>
        </div>
      </section>

      <section class="section history">
        <div class="wrap history-grid">
          <div class="history-copy">
            <span class="kicker reveal">Desde 1925</span>
            <h2 class="h-section reveal">${H.historia.title.replace('historia', '<em>historia</em>')}</h2>
            <p class="lead reveal">${D.libro100.p}</p>
            <div class="reveal" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:26px">
              <a class="btn magnetic" href="#/libro-100">Libro 100 años <span class="arrow">${ICON.arrow}</span></a>
              <button class="btn ghost-dark" type="button" data-lightbox="${H.historia.img}">Ver línea del tiempo completa</button>
            </div>
          </div>
          <div class="history-scroll reveal" data-autoscroll>
            ${img(H.historia.img, 'infografia-timeline')}
          </div>
        </div>
      </section>

      <section class="section golden">
        <div class="wrap golden-grid">
          <div class="golden-img reveal"><span class="golden-halo" aria-hidden="true"></span>${img(H.circulo.img, 'circulo-dorado-chinoin', 'float')}</div>
          <div>
            <span class="kicker reveal">Nuestra razón de ser</span>
            <h2 class="h-section reveal">El círculo <em>dorado</em> Chinoin®</h2>
            ${H.circulo.p.map((p) => `<p class="lead reveal">${p}</p>`).join('')}
          </div>
        </div>
      </section>

      <section class="section units" id="unidades">
        <div class="wrap">
          <div class="section-head">
            <div class="reveal"><span class="kicker">Unidades de Negocio</span><h2 class="h-section">Unidades de <em>Negocio</em></h2></div>
            <a class="btn light magnetic reveal" href="#/unidades-de-negocio">Ver todas <span class="arrow">${ICON.arrow}</span></a>
          </div>
          <div class="unit-rail reveal">
            ${units.map((u, i) => `
              <a class="unit${i === 0 ? ' is-active' : ''}" href="#/unidades-de-negocio/${u.id}">
                <span class="unit-photo" style="background-image:url('${u.img}')"></span>
                <span class="u-num">0${i + 1}</span>
                <div><h3>${u.title}</h3><span class="u-go">Ver más ${ICON.arrow}</span></div>
              </a>`).join('')}
          </div>
        </div>
      </section>

      <section class="portal-band">
        <div class="wrap">
          <div class="portal-card reveal">
            <div>
              <span class="kicker">Portal Médico</span>
              <h2 class="h-section">Portal <em>Médico</em></h2>
              <p>La página que estás intentando visualizar solo está disponible para usuarios registrados.</p>
              <div style="display:flex;gap:12px;flex-wrap:wrap">
                <a class="btn light magnetic" href="portal-medico.html">Iniciar sesión <span class="arrow">${ICON.arrow}</span></a>
                <a class="btn ghost magnetic" href="#/biblioteca-virtual">Biblioteca virtual</a>
              </div>
            </div>
            <div class="portal-visual" aria-hidden="true">
              ${disc('float', 'width:220px;height:220px;left:10%;top:10%;--dur:8s')}
              ${disc('glass float', 'width:170px;height:170px;left:45%;top:35%;--dur:6s;--dy:20px')}
              ${capsule('width:200px;height:72px;left:30%;top:0;rotate:22deg')}
            </div>
          </div>
        </div>
      </section>

      <section class="section" id="contacto" style="padding-top:0">
        <div class="wrap">
          <div class="section-head">
            <div class="reveal"><span class="kicker">Contacto</span><h2 class="h-section">Contáctanos</h2></div>
          </div>
          <div class="contact-grid three">
            <a class="contact-card reveal" href="#/contacto"><span class="icon-bubble">${ICON.mail}</span><div class="row"><h3>Contacto</h3><span class="go">${ICON.diag}</span></div></a>
            <a class="contact-card reveal" href="#/unete-al-equipo" style="--d:.08s"><span class="icon-bubble">${ICON.house}</span><div class="row"><h3>Únete al equipo</h3><span class="go">${ICON.diag}</span></div></a>
            <a class="contact-card reveal" href="#/farmacovigilancia" style="--d:.16s"><span class="icon-bubble">${ICON.file}</span><div class="row"><h3>Farmacovigilancia</h3><span class="go">${ICON.diag}</span></div></a>
          </div>
        </div>
      </section>`;
  }

  function mountHome() {
    // Unidades: acordeón horizontal
    $$('.unit').forEach((u) => u.addEventListener('mouseenter', () => $$('.unit').forEach((x) => x.classList.toggle('is-active', x === u))));

    // Rueda de pilares: rota sola y responde al mouse
    const wheel = $('[data-wheel]');
    if (wheel) {
      const items = $$('.wheel-item', wheel);
      const label = $('[data-wheel-label]', wheel);
      let i = 0, timer;
      const set = (n) => {
        i = n;
        items.forEach((x, k) => x.classList.toggle('is-active', k === n));
        label.textContent = D.home.pilares.items[n].label;
        label.classList.remove('pop'); void label.offsetWidth; label.classList.add('pop');
      };
      const play = () => { clearInterval(timer); if (!reduceMotion) timer = setInterval(() => set((i + 1) % items.length), 2200); };
      items.forEach((x, k) => {
        x.addEventListener('mouseenter', () => { clearInterval(timer); set(k); });
        x.addEventListener('focus', () => { clearInterval(timer); set(k); });
      });
      wheel.addEventListener('mouseleave', play);
      play();
    }
  }

  /* ============================================================
     Catálogo
     ============================================================ */
  const catState = { grupos: new Set(), pads: new Set(), q: '' };

  function viewCatalogo(params) {
    if (params.grupo) { catState.grupos = new Set([params.grupo]); catState.pads.clear(); }
    const chip = (kind, value, label) => `<button type="button" class="chip" data-kind="${kind}" data-value="${esc(value)}" aria-pressed="false">${label}</button>`;
    return pageHero({
      kicker: 'Conoce nuestro', title: 'Catálogo de <em>productos</em>',
      intro: 'Haz click en cada imagen para obtener información detallada de cada uno de los productos de la familia Chinoin®.',
      crumbs: [{ label: 'Productos' }]
    }) + `
      <section class="catalog">
        <div class="wrap catalog-grid">
          <aside class="filters" aria-label="Filtros">
            <h3>Filtrar por:</h3>
            <label class="search">${ICON.search}<input type="search" placeholder="Buscar producto" aria-label="Buscar producto" data-q value="${esc(catState.q)}"></label>
            <div class="f-group"><span>Categorías</span><div class="chips">${GRUPOS.map((g) => chip('grupo', g, g)).join('')}</div></div>
            <div class="f-group"><span>Padecimiento</span><div class="chips">${PADECIMIENTOS.map((p) => chip('pad', p.id, p.label)).join('')}</div></div>
            <button type="button" class="clear" data-clear>Borrar todos los filtros</button>
          </aside>
          <div>
            <div class="results-bar"><span data-count-results></span></div>
            <div class="product-grid" data-grid>${CAT.map((p, i) => productCard(p, i)).join('')}</div>
            <div class="empty" hidden>No hay productos con estos filtros. <button type="button" data-clear>Borrar todos los filtros</button></div>
          </div>
        </div>
      </section>`;
  }

  function mountCatalogo() {
    const grid = $('[data-grid]');
    const cards = $$('.product-card', grid);
    const count = $('[data-count-results]');
    const q = $('[data-q]');
    const sync = () => {
      $$('.chip').forEach((c) => {
        const on = (c.dataset.kind === 'grupo' ? catState.grupos : catState.pads).has(c.dataset.value);
        c.setAttribute('aria-pressed', String(on));
      });
    };
    const apply = (animate = true) => {
      // FLIP: guarda posiciones, filtra y anima el reacomodo
      const first = new Map(cards.map((c) => [c, c.getBoundingClientRect()]));
      let n = 0;
      cards.forEach((c) => {
        const p = findProduct(c.dataset.id);
        const okG = !catState.grupos.size || p.grupos.some((g) => catState.grupos.has(g));
        const okP = !catState.pads.size || p.padecimientos.some((x) => catState.pads.has(x));
        const okQ = !catState.q || norm(p.name + ' ' + p.padecimientos.map(padLabel).join(' ') + ' ' + p.grupos.join(' ')).includes(norm(catState.q));
        const show = okG && okP && okQ;
        c.hidden = !show;
        if (show) n++;
      });
      count.textContent = `${n} ${n === 1 ? 'producto' : 'productos'}`;
      $('.empty').hidden = n > 0;
      if (!animate || reduceMotion) return;
      cards.forEach((c) => {
        if (c.hidden) return;
        const a = first.get(c), b = c.getBoundingClientRect();
        if (!a.width) { c.animate([{ opacity: 0, transform: 'scale(.92)' }, { opacity: 1, transform: 'none' }], { duration: 450, easing: 'cubic-bezier(.2,.8,.2,1)' }); return; }
        const dx = a.left - b.left, dy = a.top - b.top;
        if (dx || dy) c.animate([{ transform: `translate(${dx}px,${dy}px)` }, { transform: 'none' }], { duration: 500, easing: 'cubic-bezier(.2,.8,.2,1)' });
      });
    };
    $$('.chip').forEach((c) => c.addEventListener('click', () => {
      const set = c.dataset.kind === 'grupo' ? catState.grupos : catState.pads;
      set.has(c.dataset.value) ? set.delete(c.dataset.value) : set.add(c.dataset.value);
      sync(); apply();
    }));
    q.addEventListener('input', () => { catState.q = q.value.trim(); apply(); });
    $$('[data-clear]').forEach((b) => b.addEventListener('click', () => { catState.grupos.clear(); catState.pads.clear(); catState.q = ''; q.value = ''; sync(); apply(); }));
    sync(); apply(false);
  }

  /* ============================================================
     Producto
     ============================================================ */
  function fichaAccordion(key, open = 0) {
    const f = FICHAS[key];
    if (!f) return '';
    return `<div class="ficha" data-ficha>${f.secciones.map((s, i) => `
      <details class="ficha-item"${i < open ? ' open' : ''}>
        <summary><span>${esc(s.t)}</span><i>${ICON.chev}</i></summary>
        <div class="ficha-body">${s.html}</div>
      </details>`).join('')}</div>`;
  }

  function viewProducto(id) {
    const p = findProduct(id);
    if (!p) return null;
    const d = destino(p);
    const pad = p.padecimientos[0];
    const crumbs = [{ label: 'Productos', route: '#/catalogo' }];
    if (pad) crumbs.push({ label: padLabel(pad), route: `#/${pad}` });
    const related = CAT.filter((x) => x.id !== p.id && (x.padecimientos.some((y) => p.padecimientos.includes(y)) || x.name.split(' ')[0] === p.name.split(' ')[0])).slice(0, 6);
    if (related.length < 3) related.push(...CAT.filter((x) => x.id !== p.id && !related.includes(x) && x.grupos.some((g) => p.grupos.includes(g))).slice(0, 4 - related.length));

    let action = '';
    if (d.tipo === 'externo') {
      action = `
        <div class="buy-box">
          <p class="buy-title">Información, presentaciones y dónde encontrarlo</p>
          ${ext(d.href, `Ver más en ${esc(d.sitio)} <span class="arrow">${ICON.ext}</span>`, 'btn magnetic big')}
          <p class="buy-note">Se abre el sitio oficial de la marca en una pestaña nueva.</p>
        </div>`;
    } else if (d.tipo === 'registro') {
      action = `
        <div class="buy-box locked">
          <p class="buy-title">${ICON.lock} Información para profesionales de la salud</p>
          <p>La página que estás intentando ver solo está disponible para usuarios registrados.</p>
          <a class="btn purple magnetic big" href="portal-medico.html">Iniciar sesión <span class="arrow">${ICON.arrow}</span></a>
        </div>`;
    } else if (d.tipo === 'ficha') {
      action = `
        <div class="buy-box">
          <p class="buy-title">Ficha del producto</p>
          <a class="btn magnetic big" href="#ficha" data-scroll>Ver información completa <span class="arrow">${ICON.down}</span></a>
        </div>`;
    }

    const tabs = d.tipo === 'ficha' ? d.fichas : [];
    const tabLabel = (k) => FICHAS[k] && FICHAS[k].tipo === 'ipp' ? 'Información amplia para prescribir' : 'Información del producto';

    return `
      <section class="product-hero">
        <div class="hero-bg soft"></div>
        <div class="wrap">
          <nav class="crumbs dark" aria-label="Ruta"><a href="#/">Inicio</a>${crumbs.map((c) => `<span aria-hidden="true">/</span><a href="${c.route}">${c.label}</a>`).join('')}<span aria-hidden="true">/</span><span>${esc(p.name)}</span></nav>
          <div class="product-detail">
            <div class="product-stage" data-stage>
              ${disc('glass float', 'width:38%;height:38%;right:-6%;top:-4%;--dur:8s')}
              ${disc('float', 'width:16%;height:16%;left:6%;bottom:10%;--dur:6s;opacity:.85')}
              ${img(p.img, p.name, 'stage-img', 'loading="eager"')}
            </div>
            <div class="product-info">
              <div class="pc-tags big">${p.grupos.map((g) => `<span>${g}</span>`).join('')}${p.padecimientos.map((x) => `<a href="#/${x}">${padLabel(x)}</a>`).join('')}</div>
              <h1 class="h-display product-name">${esc(p.name)}</h1>
              ${action}
              <ul class="help-links">
                <li><a href="#/farmacovigilancia">${ICON.alert} Reportar una sospecha de reacción adversa</a></li>
                <li><a href="#/catalogo">${ICON.back} Regresar al catálogo</a></li>
              </ul>
            </div>
          </div>
        </div>
      </section>
      ${tabs.length ? `
      <section class="ficha-section" id="ficha">
        <div class="wrap">
          <div class="ficha-tabs" role="tablist">${tabs.map((k, i) => `<button role="tab" aria-selected="${!i}" data-tab="${k}">${tabLabel(k)}</button>`).join('')}</div>
          ${tabs.map((k, i) => `<div class="ficha-panel" data-panel="${k}"${i ? ' hidden' : ''}>${fichaAccordion(k, 3)}</div>`).join('')}
        </div>
      </section>` : ''}
      ${related.length ? `
      <section class="section related">
        <div class="wrap"><div class="section-head"><div class="reveal"><span class="kicker">También te puede interesar</span><h2 class="h-section">Productos <em>relacionados</em></h2></div></div></div>
        <div class="rail" data-rail><div class="rail-track">${related.map((x, i) => productCard(x, i)).join('')}</div></div>
      </section>` : ''}`;
  }

  function mountProducto() {
    $$('[data-tab]').forEach((t) => t.addEventListener('click', () => {
      $$('[data-tab]').forEach((x) => x.setAttribute('aria-selected', String(x === t)));
      $$('[data-panel]').forEach((p) => { p.hidden = p.dataset.panel !== t.dataset.tab; });
    }));
    const stage = $('[data-stage]');
    if (stage && !reduceMotion) {
      const im = $('.stage-img', stage);
      stage.addEventListener('pointermove', (e) => {
        const r = stage.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        im.style.transform = `perspective(900px) rotateY(${x * 18}deg) rotateX(${-y * 14}deg) scale(1.04)`;
      });
      stage.addEventListener('pointerleave', () => { im.style.transform = ''; });
    }
  }

  function viewFichaSuelta(id) {
    const f = D.fichasSueltas.find((x) => x.id === id);
    if (!f) return null;
    return pageHero({ kicker: 'Información amplia para prescribir', title: esc(f.name), crumbs: [{ label: 'Productos', route: '#/catalogo' }, { label: esc(f.name) }], compact: true }) + `
      <section class="ficha-section"><div class="wrap">${fichaAccordion(f.ficha, 3)}</div></section>`;
  }

  /* ============================================================
     Portafolios y listados
     ============================================================ */
  function logoCard(it, i) {
    const p = it.prod && findProduct(it.prod);
    const inner = `
      <div class="logo-box">${img(it.logo, it.name)}</div>
      <div class="logo-meta"><h3>${it.name}${it.sub ? ` <small>${it.sub}</small>` : ''}</h3>${p || it.href ? `<span class="lm-go">Ver más ${ICON.arrow}</span>` : ''}</div>`;
    if (p) return `<a class="logo-card reveal" style="--d:${(i % 4) * 0.06}s" href="#/producto/${p.id}">${inner}</a>`;
    if (it.href) return `<a class="logo-card reveal" style="--d:${(i % 4) * 0.06}s" href="portal-medico.html" title="Solo para usuarios registrados">${inner}</a>`;
    return `<div class="logo-card reveal static" style="--d:${(i % 4) * 0.06}s">${inner}</div>`;
  }

  function viewPortafolio(key, opts = {}) {
    const P = D.portafolios[key];
    if (!P) return null;
    const isArea = !['odontologia', 'probioticos'].includes(key);
    const crumbs = isArea ? [{ label: 'Áreas Terapéuticas', route: '#/medicamentos-prescripcion' }, { label: P.title }] : [{ label: 'Productos', route: '#/catalogo' }, { label: P.title }];
    const siblings = isArea ? D.prescripcion.cards : null;
    const route = opts.route;
    const related = opts.grupo ? CAT.filter((p) => p.grupos.includes(opts.grupo)) : [];
    return pageHero({
      kicker: P.kicker || 'Portafolio de productos', title: P.title, intro: P.intro, crumbs,
      sub: siblings ? subnav(siblings.map((c) => ({ label: c.label, route: c.route })), route) : ''
    }) + `
      <section class="page-body">
        <div class="wrap">
          <div class="logo-grid">${P.items.map(logoCard).join('')}</div>
          ${related.length ? `
            <div class="section-head" style="margin-top:80px"><div class="reveal"><span class="kicker">Presentaciones</span><h2 class="h-section">Productos de <em>${P.title.toLowerCase()}</em></h2></div></div>
            <div class="product-grid">${related.map((p, i) => productCard(p, i)).join('')}</div>` : ''}
        </div>
      </section>`;
  }

  function viewPrescripcion() {
    const P = D.prescripcion;
    return pageHero({ kicker: P.kicker, title: 'Medicamentos de <em>prescripción</em>', intro: P.intro, crumbs: [{ label: 'Productos', route: '#/catalogo' }, { label: P.kicker }] }) + `
      <section class="page-body"><div class="wrap">
        <div class="photo-cards">${P.cards.map((c, i) => `
          <a class="photo-card reveal" href="${c.route}" style="--d:${(i % 4) * 0.06}s">
            <span class="pcard-img">${img(c.img, c.label)}</span>
            <span class="pcard-meta"><span class="pcard-n">0${i + 1}</span><h3>${c.label}</h3><span class="lm-go">Ver medicamentos ${ICON.arrow}</span></span>
          </a>`).join('')}</div>
        <div class="section-head" style="margin-top:90px"><div class="reveal"><span class="kicker">Presentaciones</span><h2 class="h-section">Productos de <em>prescripción</em></h2></div></div>
        <div class="product-grid">${CAT.filter((p) => p.grupos.includes('Áreas Terapéuticas')).map((p, i) => productCard(p, i)).join('')}</div>
      </div></section>`;
  }

  function viewCuidado() {
    const C = D.cuidado;
    return pageHero({ kicker: C.kicker, title: 'Medicamentos de <em>venta libre</em>', intro: C.intro, crumbs: [{ label: 'Productos', route: '#/catalogo' }, { label: C.kicker }] }) + `
      <section class="page-body"><div class="wrap">
        <div class="photo-cards">${C.cards.map((c, i) => {
          const n = CAT.filter((p) => p.padecimientos.includes(c.id)).length;
          return `
          <a class="photo-card reveal" href="#/${c.id}" style="--d:${(i % 4) * 0.06}s">
            <span class="pcard-img">${img(c.img, c.label)}</span>
            <span class="pcard-meta"><span class="pcard-n">${n} ${n === 1 ? 'producto' : 'productos'}</span><h3>${c.label}</h3><span class="lm-go">Ver medicamentos ${ICON.arrow}</span></span>
          </a>`;
        }).join('')}</div>
      </div></section>`;
  }

  function viewPadecimiento(id) {
    const c = PADECIMIENTOS.find((p) => p.id === id);
    if (!c) return null;
    const list = CAT.filter((p) => p.padecimientos.includes(id));
    return pageHero({
      kicker: 'Medicamentos', title: c.label, crumbs: [{ label: 'Cuidado de la salud', route: '#/cuidado-de-la-salud' }, { label: c.label }],
      photo: c.img, sub: subnav(PADECIMIENTOS.map((p) => ({ label: p.label, route: `#/${p.id}` })), `#/${id}`)
    }) + `
      <section class="page-body"><div class="wrap">
        <div class="product-grid">${list.map((p, i) => productCard(p, i)).join('')}</div>
        <a class="back-link" href="#/cuidado-de-la-salud">${ICON.back} Regresar al catálogo</a>
      </div></section>`;
  }

  /* ============================================================
     Nosotros
     ============================================================ */
  const nosotrosNav = (route) => subnav(D.nav[0].items, route);

  function viewCalidad() {
    const C = D.calidad;
    return pageHero({ kicker: 'Nosotros', title: 'Le damos gran valor a la <em>Calidad</em>', crumbs: [{ label: 'Nosotros' }, { label: 'Calidad' }], photo: C.header, sub: nosotrosNav('#/calidad-chinoin') }) + `
      <section class="page-body"><div class="wrap split-2">
        <div>
          <h2 class="h-section reveal" style="font-size:clamp(28px,3vw,44px)">${C.lead}</h2>
          <p class="lead reveal">${C.p}</p>
          <div class="cert reveal">
            ${img(C.cert.img, 'industria-limpia', 'cert-badge')}
            <p>${C.cert.html}</p>
          </div>
        </div>
        <figure class="framed reveal">${img(C.img.src, 'Chinoin innovación en medicamentos de calidad')}<figcaption>${C.img.caption}</figcaption></figure>
      </div></section>`;
  }

  function viewResponsabilidad() {
    const R = D.responsabilidad;
    return pageHero({ kicker: 'Nosotros', title: 'Le damos gran valor a la <em>Responsabilidad Social</em>', crumbs: [{ label: 'Nosotros' }, { label: 'Responsabilidad Social' }], photo: R.header, sub: nosotrosNav('#/responsabilidad-social') }) + `
      <section class="page-body"><div class="wrap">
        <p class="lead big reveal">${R.intro}</p>
        <div class="axes">${R.ejes.map((e, i) => `
          <div class="axis reveal" style="--d:${i * 0.1}s"><span class="axis-n">0${i + 1}</span>${img(e.img, e.label)}<h3>${e.label}</h3></div>`).join('')}</div>
      </div></section>
      <section class="section neutral">
        <div class="wrap split-2">
          <div>
            <span class="kicker reveal">Programa</span>
            <h2 class="h-section reveal">Programa <em>Neutralízate</em></h2>
            ${R.programa.p.map((p) => `<p class="lead reveal">${p}</p>`).join('')}
          </div>
          <div class="stack">${R.programa.items.map((it, i) => `
            <article class="badge-card reveal" style="--d:${i * 0.1}s">
              ${img(it.img, it.title)}
              <div><h3>${it.title}</h3>${it.p.map((p) => `<p>${p}</p>`).join('')}</div>
            </article>`).join('')}</div>
        </div>
      </section>`;
  }

  function viewTecnologia() {
    const T = D.tecnologia;
    return pageHero({ kicker: 'Nosotros', title: 'Le damos un gran valor a la <em>Tecnología</em>', crumbs: [{ label: 'Nosotros' }, { label: 'Tecnología' }], photo: T.header, sub: nosotrosNav('#/tecnologia') }) + `
      <section class="page-body"><div class="wrap split-2">
        <div>
          <span class="kicker reveal">01</span>
          <h2 class="h-section reveal">${T.instalaciones.title}</h2>
          ${T.instalaciones.p.map((p) => `<p class="lead reveal">${p}</p>`).join('')}
          <div class="pill-list reveal">${T.instalaciones.items.map((x) => `<span>${x}</span>`).join('')}</div>
        </div>
        <div class="gallery reveal" data-gallery>
          ${T.instalaciones.gallery.map((g, i) => `<button type="button" class="g-item${i === 0 ? ' big' : ''}" data-lightbox="${g.src}" ${g.video ? `data-video="${g.video}"` : ''}>${img(g.src, g.alt)}${g.video ? `<span class="play">${ICON.play}</span>` : ''}</button>`).join('')}
        </div>
      </div></section>
      <section class="section equip">
        <div class="wrap">
          <span class="kicker reveal">02</span>
          <h2 class="h-section reveal">${T.equipamiento.title}</h2>
          <p class="lead reveal">${T.equipamiento.p}</p>
          <div class="equip-grid">${T.equipamiento.items.map((x, i) => `<div class="equip-item reveal" style="--d:${(i % 4) * 0.06}s"><span>${String(i + 1).padStart(2, '0')}</span><h3>${x}</h3></div>`).join('')}</div>
        </div>
      </section>
      <section class="section innov">
        <div class="wrap">
          <span class="kicker reveal">03</span>
          <h2 class="h-section reveal">${T.innovacion.title}</h2>
          <div class="innov-grid">${T.innovacion.items.map((x, i) => `
            <div class="innov-item reveal" style="--d:${(i % 3) * 0.08}s">
              ${img(x.img, '')}
              <p>${x.html}</p>
              ${x.list ? `<ul>${x.list.map((l) => `<li>${l}</li>`).join('')}</ul>` : ''}
            </div>`).join('')}</div>
          <p class="closing reveal">${T.innovacion.closing}</p>
        </div>
      </section>`;
  }

  /* ============================================================
     Unidades de negocio
     ============================================================ */
  function viewUnidades() {
    const U = D.unidades;
    return pageHero({ kicker: 'Nosotros', title: U.title.replace('Negocio', '<em>Negocio</em>'), crumbs: [{ label: U.title }], photo: U.header,
      sub: `<div class="subnav">${U.items.map((u) => `<a href="#/unidades-de-negocio/${u.id}" data-spy="${u.id}">${u.title}</a>`).join('')}</div>` }) + `
      <section class="page-body units-page"><div class="wrap">
        ${U.items.map((u, i) => `
          <article class="unit-block${i % 2 ? ' flip' : ''}${u.wide ? ' wide' : ''}" id="u-${u.id}">
            <div class="ub-img reveal">${img(u.img, u.title)}</div>
            <div class="ub-copy">
              <span class="kicker reveal">0${i + 1}</span>
              <h2 class="h-section reveal">${u.title}</h2>
              ${u.lead ? `<p class="ub-lead reveal">${u.lead}</p>` : ''}
              ${u.p.map((p) => `<p class="lead reveal">${p}</p>`).join('')}
              ${u.list ? `<ul class="check-list reveal">${u.list.map((l) => `<li>${l}</li>`).join('')}</ul>` : ''}
            </div>
          </article>`).join('')}
      </div></section>`;
  }

  function mountUnidades(anchor) {
    if (anchor) {
      const el = document.getElementById('u-' + anchor);
      if (el) setTimeout(() => el.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' }), 60);
    }
    const links = $$('[data-spy]');
    const obs = new IntersectionObserver((es) => es.forEach((e) => {
      if (e.isIntersecting) links.forEach((l) => l.toggleAttribute('aria-current', l.dataset.spy === e.target.id.slice(2)));
    }), { rootMargin: '-45% 0px -50% 0px' });
    $$('.unit-block').forEach((b) => obs.observe(b));
    links.forEach((l) => l.addEventListener('click', (e) => {
      e.preventDefault();
      history.replaceState(null, '', l.getAttribute('href'));
      document.getElementById('u-' + l.dataset.spy).scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth' });
    }));
  }

  /* ============================================================
     Contacto, Farmacovigilancia, Únete
     ============================================================ */
  const contactoNav = (route) => subnav([{ label: 'Contacto', route: '#/contacto' }, ...D.nav[3].items], route);

  function viewContacto() {
    const C = D.contacto;
    return pageHero({ kicker: 'Contacto', title: C.title, crumbs: [{ label: 'Contacto' }], photo: C.header, sub: contactoNav('#/contacto') }) + `
      <section class="page-body"><div class="wrap">
        <div class="sedes">${C.sedes.map((s, i) => `
          <article class="sede reveal" style="--d:${i * 0.1}s">
            <span class="icon-bubble">${ICON.pin}</span>
            <h2>${s.title}</h2>
            ${s.lines.map((l) => `<p>${l}</p>`).join('')}
            <div class="sede-tel">${s.tel.map((t) => t.href ? `<a href="${t.href}">${ICON.phone}<span><small>${t.label}</small>${t.value}</span></a>` : `<span class="t">${ICON.phone}<span><small>${t.label}</small>${t.value}</span></span>`).join('')}</div>
          </article>`).join('')}</div>
        <div class="section-head" style="margin-top:80px"><div class="reveal"><span class="kicker">Correos</span><h2 class="h-section">${C.directorioTitle}</h2></div>
          <label class="search reveal">${ICON.search}<input type="search" placeholder="Buscar área" aria-label="Buscar área" data-dir-q></label></div>
        <div class="directory">${C.directorio.map(([a, m], i) => `
          <a class="dir-item reveal" style="--d:${(i % 4) * 0.05}s" href="mailto:${m}" data-dir="${esc(norm(a + ' ' + m))}">
            <span class="dir-area">${a}</span><span class="dir-mail">${ICON.mail}${m}</span>
          </a>`).join('')}</div>
      </div></section>`;
  }

  function mountContacto() {
    const q = $('[data-dir-q]');
    q && q.addEventListener('input', () => {
      const v = norm(q.value.trim());
      $$('.dir-item').forEach((d) => { d.hidden = v && !d.dataset.dir.includes(v); });
    });
  }

  function formField(f) {
    const id = 'f-' + f.name;
    const req = f.req ? ' required' : '';
    const label = `<label for="${id}">${f.label}${f.req ? '<span class="req">*</span>' : ''}</label>`;
    let control;
    if (f.type === 'textarea') control = `<textarea id="${id}" name="${f.name}"${req}></textarea>`;
    else if (f.type === 'select') control = `<select id="${id}" name="${f.name}"${req}><option value="">Selecciona</option>${f.options.map((o) => `<option>${o}</option>`).join('')}</select>`;
    else control = `<input id="${id}" name="${f.name}" type="${f.type}"${req}>`;
    return `<div class="field${f.full || f.type === 'textarea' ? ' full' : ''}">${label}${control}</div>`;
  }

  function viewFarmacovigilancia() {
    const F = D.farmacovigilancia;
    return pageHero({ kicker: 'Contacto', title: F.title, crumbs: [{ label: 'Contacto', route: '#/contacto' }, { label: F.title }], photo: F.header, sub: contactoNav('#/farmacovigilancia') }) + `
      <section class="page-body"><div class="wrap">
        <p class="lead big reveal">${F.intro}</p>
        <div class="vias">${F.vias.map((v, i) => `
          <a class="via reveal" style="--d:${i * 0.08}s" href="${v.href}">
            <span class="icon-bubble">${v.href.startsWith('mailto') ? ICON.mail : ICON.phone}</span>
            <small>${v.label}</small><strong>${v.value}</strong>
          </a>`).join('')}</div>
        <form class="form-card stepper reveal" data-demo novalidate>
          <h2 class="h-section" style="font-size:clamp(28px,3vw,40px);margin:0 0 8px">${F.formTitle}</h2>
          <ol class="steps">${F.form.groups.map((g, i) => `<li${i ? '' : ' class="is-active"'}><span>${i + 1}</span>${g.title.replace(':', '')}</li>`).join('')}</ol>
          ${F.form.groups.map((g, i) => `
            <fieldset class="step"${i ? ' hidden' : ''}>
              <legend>${g.title}</legend>
              <div class="form-grid">${g.fields.map(formField).join('')}</div>
            </fieldset>`).join('')}
          <div class="form-nav">
            <button type="button" class="btn ghost-dark" data-prev hidden>${ICON.back} Anterior</button>
            <button type="button" class="btn" data-next>Siguiente <span class="arrow">${ICON.arrow}</span></button>
            <button type="submit" class="btn" data-submit hidden>${F.form.submit} <span class="arrow">${ICON.arrow}</span></button>
          </div>
          <p class="form-done" hidden>${F.form.gracias}</p>
        </form>
      </div></section>`;
  }

  function mountStepper() {
    const form = $('form.stepper');
    if (!form) return;
    const steps = $$('.step', form), marks = $$('.steps li', form);
    const prev = $('[data-prev]', form), next = $('[data-next]', form), submit = $('[data-submit]', form);
    let i = 0;
    const show = (n) => {
      i = n;
      steps.forEach((s, k) => { s.hidden = k !== n; });
      marks.forEach((m, k) => { m.classList.toggle('is-active', k === n); m.classList.toggle('is-done', k < n); });
      prev.hidden = n === 0; next.hidden = n === steps.length - 1; submit.hidden = n !== steps.length - 1;
      if (!reduceMotion) steps[n].animate([{ opacity: 0, transform: 'translateX(24px)' }, { opacity: 1, transform: 'none' }], { duration: 400, easing: 'cubic-bezier(.2,.8,.2,1)' });
    };
    const valid = () => {
      const bad = $$('[required]', steps[i]).filter((f) => !f.value.trim() || (f.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value)));
      $$('.field', steps[i]).forEach((f) => f.classList.remove('invalid'));
      bad.forEach((f) => f.closest('.field').classList.add('invalid'));
      if (bad[0]) bad[0].focus();
      return !bad.length;
    };
    next.addEventListener('click', () => valid() && show(i + 1));
    prev.addEventListener('click', () => show(i - 1));
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!valid()) return;
      // Maqueta: en producción se envía al mismo formulario de HubSpot que usa chinoin.com (ver data.js).
      $$('.step, .steps, .form-nav', form).forEach((x) => { x.hidden = true; });
      $('.form-done', form).hidden = false;
    });
    show(0);
  }

  function viewUnete() {
    const U = D.unete;
    return pageHero({ kicker: 'Contacto', title: U.title, crumbs: [{ label: 'Contacto', route: '#/contacto' }, { label: U.title }], sub: contactoNav('#/unete-al-equipo') }) + `
      <section class="page-body"><div class="wrap" style="display:grid;gap:40px">
        ${pendingNote('Texto pendiente de cargar', 'La página chinoin.com/es/unete-al-equipo no se pudo leer desde este entorno; su texto y su formulario se copiarán de la captura.')}
        <div class="vias two">${U.contactos.map(([a, m], i) => `
          <a class="via reveal" style="--d:${i * 0.08}s" href="mailto:${m}"><span class="icon-bubble">${ICON.mail}</span><small>${a}</small><strong>${m}</strong></a>`).join('')}</div>
      </div></section>`;
  }

  /* ============================================================
     Biblioteca, 100 años, Aviso de privacidad
     ============================================================ */
  function viewBiblioteca() {
    const B = D.biblioteca;
    return pageHero({ kicker: 'Portal Médico', title: 'Biblioteca <em>Virtual</em>', crumbs: [{ label: B.title }] }) + `
      <section class="page-body"><div class="wrap">
        <div class="books">${B.items.map((b, i) => `
          <a class="book reveal" style="--d:${(i % 5) * 0.06}s" href="${b.pdf}" target="_blank" rel="noopener">
            <span class="book-cover">${img(b.img, b.title)}</span>
            <h3>${b.title}</h3>
            <span class="lm-go">${ICON.book} Leer</span>
          </a>`).join('')}</div>
      </div></section>`;
  }

  function viewLibro100() {
    const L = D.libro100;
    return `
      <section class="banner-hero">${img(L.banner, 'Banner-100-años', '', 'loading="eager"')}</section>
      <section class="page-body"><div class="wrap">
        <div class="split-2">
          <div><span class="kicker reveal">100 años</span><h2 class="h-section reveal">${L.title.replace('historia', '<em>historia</em>')}</h2><p class="lead reveal">${L.p}</p>
            <a class="btn magnetic reveal" href="${L.libro}" target="_blank" rel="noopener">Abrir el libro <span class="arrow">${ICON.ext}</span></a></div>
          <div class="mosaic reveal">${L.fotos.map((f, i) => `<button type="button" class="m${i}" data-lightbox="${f}">${img(f, 'Chinoin-' + (i + 1))}</button>`).join('')}</div>
        </div>
        <div class="flipbook reveal"><iframe src="${L.libro}" title="Libro 100 años CHINOIN" loading="lazy" allowfullscreen></iframe></div>
      </div></section>`;
  }

  function viewAviso() {
    return pageHero({ kicker: 'Legal', title: 'Aviso de <em>privacidad</em>', crumbs: [{ label: 'Aviso de Privacidad' }], compact: true }) + `
      <section class="page-body"><div class="wrap"><div class="prose legal">${window.CHINOIN_AVISO || ''}</div></div></section>`;
  }

  /* ============================================================
     Veterinaria
     ============================================================ */
  const VET = window.CHINOIN_VET || { productos: [], destacados: [], textos: {} };
  const V = D.veterinaria;
  const vetFind = (id) => VET.productos.find((p) => p.id === id);
  const lineaId = (p) => V.lineas.filter((l) => p.lineas.includes(`${l.grupo} · ${l.linea}`)).map((l) => l.id);
  const especiesDe = (p) => (p.ficha && p.ficha.especies) || [];
  const cap = (s) => { const t = String(s || '').toLocaleLowerCase('es'); return t.charAt(0).toLocaleUpperCase('es') + t.slice(1); };
  const especieImg = (label) => (VET.textos.especiesImgs || {})[label];

  function vetCard(p, i = 0) {
    const esp = especiesDe(p);
    return `
      <a class="product-card vet-card" href="#/veterinaria/producto/${p.id}" style="--i:${i}" data-vid="${p.id}">
        <div class="shot">${img(p.img, p.name)}</div>
        <div class="meta">
          <div class="pc-tags"><span>${esc(cap(p.forma))}</span>${p.categoria ? `<span>${esc(cap(p.categoria))}</span>` : ''}</div>
          <h3>${esc(p.name)}</h3>
          ${p.sub ? `<p class="vc-sub">${esc(cap(p.sub))}</p>` : ''}
          ${esp.length ? `<span class="vc-species">${ICON.paw} ${esp.join(' · ')}</span>` : ''}
        </div>
        <span class="pc-go">${ICON.arrow}</span>
      </a>`;
  }

  const vetHeroCrumbs = (extra = []) => `<nav class="crumbs dark" aria-label="Ruta"><a href="#/">Inicio</a><span aria-hidden="true">/</span><a href="#/veterinaria">Veterinaria</a>${extra.map((c) => `<span aria-hidden="true">/</span>${c.route ? `<a href="${c.route}">${c.label}</a>` : `<span>${c.label}</span>`}`).join('')}</nav>`;

  function viewVeterinaria() {
    const g = V.fotos.galeria;
    const T = VET.textos;
    const feat = VET.destacados.map(vetFind).filter(Boolean);
    const grupos = [...new Set(V.lineas.map((l) => l.grupo))];
    return `
      <section class="vet-hero">
        <div class="vet-blob b1"></div><div class="vet-blob b2"></div>
        <div class="paws" aria-hidden="true">${Array.from({ length: 9 }, (_, i) => `<i style="--i:${i}">${ICON.paw}</i>`).join('')}</div>
        <div class="wrap vet-hero-grid">
          <div>
            ${vetHeroCrumbs()}
            <span class="kicker">CHINOIN® Veterinaria · ${V.firma}</span>
            <h1 class="h-display vet-title">${V.title}</h1>
            <p class="vet-slogan">${V.slogan}</p>
            <p class="vet-lead">${V.intro}</p>
            <div class="hero-ctas">
              <a class="btn magnetic big" href="#/veterinaria/productos">${V.cta} <span class="arrow">${ICON.arrow}</span></a>
              <a class="btn ghost-dark magnetic" href="#vet-especies" data-scroll>Buscar por especie</a>
            </div>
          </div>
          <div class="vet-photo">
            <div class="vet-photo-frame">${img(V.fotos.hero, 'Perro corgi', '', 'loading="eager"')}</div>
            <span class="vet-sticker s1">${ICON.paw}</span>
            <span class="vet-sticker s2">♥</span>
            <span class="vet-count"><b data-count="${VET.productos.length}">${VET.productos.length}</b> productos para la salud animal</span>
          </div>
        </div>
      </section>
      <section class="vet-strip" aria-hidden="true">
        <div class="vet-track">${[...g, ...g].map((f, i) => `<span class="vet-pic" style="--r:${(i % 2 ? 1 : -1) * (2 + (i % 3))}deg">${img(f, '')}</span>`).join('')}</div>
      </section>

      <section class="section vet-body" id="vet-especies">
        <div class="wrap">
          <div class="section-head"><div class="reveal"><span class="kicker">Menú anatómicos</span><h2 class="h-section">¿Para quién <em>buscas?</em></h2></div></div>
          <div class="species">${V.especies.map((e, i) => {
            const n = VET.productos.filter((p) => especiesDe(p).includes(e.label)).length;
            return `<a class="specie reveal" style="--d:${i * 0.05}s" href="#/veterinaria/especie/${e.id}">
              <span class="sp-img">${img(especieImg(e.label), e.label)}</span>
              <strong>${e.label}</strong>${n ? `<small>${n} ${n === 1 ? 'producto' : 'productos'}</small>` : ''}
            </a>`;
          }).join('')}</div>
        </div>
      </section>

      <section class="section vet-launch">
        <div class="wrap"><div class="section-head">
          <div class="reveal"><span class="kicker">Novedades</span><h2 class="h-section">${V.lanzamientos.replace('recientes', '<em>recientes</em>')}</h2></div>
          <a class="btn purple magnetic reveal" href="#/veterinaria/productos">Ver todos <span class="arrow">${ICON.arrow}</span></a>
        </div></div>
        <div class="rail" data-rail><div class="rail-track">${feat.map((p, i) => vetCard(p, i)).join('')}</div></div>
      </section>

      <section class="section vet-body">
        <div class="wrap">
          <div class="section-head"><div class="reveal"><span class="kicker">Líneas</span><h2 class="h-section">Nuestras <em>líneas</em></h2></div></div>
          <div class="vet-lines">${grupos.map((gr) => `
            <div class="vet-group reveal">
              <h3>Línea de ${gr}</h3>
              <div class="vet-group-links">${V.lineas.filter((l) => l.grupo === gr).map((l) => {
                const list = VET.productos.filter((p) => lineaId(p).includes(l.id));
                return `<a href="#/veterinaria/linea/${l.id}" class="vline">
                  <span class="vline-shots">${list.slice(0, 3).map((p) => img(p.img, '')).join('')}</span>
                  <span class="vline-meta"><strong>${l.linea}</strong><small>${list.length} productos</small></span>${ICON.arrow}
                </a>`;
              }).join('')}</div>
            </div>`).join('')}</div>
        </div>
      </section>

      <section class="section vet-values">
        <div class="wrap">
          <div class="vet-values-grid">${V.pilares.map((x, i) => `
            <article class="vval reveal" style="--d:${i * 0.06}s"><span class="vval-n">0${i + 1}</span><h3>${x.t}</h3><p>${x.p}</p></article>`).join('')}</div>
        </div>
      </section>

      <section class="section vet-history">
        <div class="wrap">
          <div class="section-head"><div class="reveal"><span class="kicker">Historia</span><h2 class="h-section">${V.historiaTitle.replace('CRECIENDO', '<em>creciendo</em>').replace('92 AÑOS', '92 años')}</h2></div></div>
        </div>
        <div class="vtimeline" data-rail>
          <div class="vt-track">${(T.historia || []).map((h, i) => `
            <article class="vt-item reveal" style="--d:${(i % 4) * 0.06}s"><span class="vt-year">${h.year}</span><p>${h.p}</p></article>`).join('')}</div>
        </div>
      </section>

      <section class="section vet-company">
        <div class="wrap">
          <div class="section-head"><div class="reveal"><span class="kicker">Empresa</span><h2 class="h-section">Nuestra <em>empresa</em></h2></div></div>
          <div class="vco" data-vco>
            <div class="vco-tabs" role="tablist">${(T.empresa || []).map((e, i) => `<button role="tab" aria-selected="${!i}" data-vco-tab="${i}">${e.t}</button>`).join('')}</div>
            <div class="vco-stage">${(T.empresa || []).map((e, i) => `
              <article class="vco-panel" data-vco-panel="${i}"${i ? ' hidden' : ''}>
                <div class="vco-img">${img(e.img, e.t, '', 'loading="eager"')}</div>
                <div class="vco-text"><h3>${e.t}</h3>${e.p.map((p) => `<p>${p}</p>`).join('')}</div>
              </article>`).join('')}</div>
          </div>
        </div>
      </section>

      <section class="section vet-contact">
        <div class="wrap vet-contact-grid">
          <div class="vapp reveal">
            <span class="kicker">Herramienta para médicos veterinarios</span>
            <h2 class="h-section">${V.app.title.replace('Dolor', '<em>Dolor</em>')}</h2>
            <p class="lead">${V.app.sub}</p>
            <div class="hero-ctas">
              ${ext(V.app.href, `Ingresar <span class="arrow">${ICON.ext}</span>`, 'btn magnetic')}
              ${V.app.stores.map((s) => ext(s.href, s.label, 'btn ghost-dark magnetic')).join('')}
            </div>
          </div>
          <div class="vcontact reveal">
            <h3>Contacto</h3>
            <a href="${V.contacto.ventas.href}">${ICON.phone}<span><small>${V.contacto.ventas.label}</small>${V.contacto.ventas.value}</span></a>
            <a href="${V.contacto.gerencia.href}">${ICON.phone}<span><small>${V.contacto.gerencia.label}</small>${V.contacto.gerencia.value}</span></a>
            <a href="mailto:${V.contacto.email}">${ICON.mail}<span><small>Email</small>${V.contacto.email}</span></a>
            <p>${ICON.pin} ${V.contacto.direccion}</p>
            <div class="social">${V.social.map((s) => ext(s.href, ICON[s.icon || 'facebook'], 'social-link" aria-label="' + s.label)).join('')}</div>
          </div>
        </div>
      </section>`;
  }

  function mountVeterinaria() {
    const tabs = $$('[data-vco-tab]');
    let i = 0, timer;
    const show = (n) => {
      i = n;
      tabs.forEach((t, k) => t.setAttribute('aria-selected', String(k === n)));
      $$('[data-vco-panel]').forEach((p, k) => {
        p.hidden = k !== n;
        if (k === n && !reduceMotion) p.animate([{ opacity: 0, transform: 'translateY(16px)' }, { opacity: 1, transform: 'none' }], { duration: 500, easing: 'cubic-bezier(.2,.8,.2,1)' });
      });
    };
    tabs.forEach((t, k) => t.addEventListener('click', () => { clearInterval(timer); show(k); }));
    if (!reduceMotion && tabs.length) timer = setInterval(() => { if (!document.body.contains(tabs[0])) return clearInterval(timer); show((i + 1) % tabs.length); }, 6000);
  }

  // Catálogo veterinario (todas, por línea o por especie)
  const vetState = { lineas: new Set(), especies: new Set(), cats: new Set(), q: '' };

  function viewVetProductos(kind, id) {
    vetState.lineas.clear(); vetState.especies.clear(); vetState.cats.clear(); vetState.q = '';
    let title = 'Productos <em>veterinarios</em>', kicker = 'Veterinaria', photo = null, crumb = 'Productos';
    if (kind === 'linea') {
      const l = V.lineas.find((x) => x.id === id); if (!l) return null;
      vetState.lineas.add(id); title = `${l.linea} <em>· ${l.grupo}</em>`; kicker = `Línea de ${l.grupo}`; crumb = `${l.grupo} · ${l.linea}`;
    }
    if (kind === 'especie') {
      const e = V.especies.find((x) => x.id === id); if (!e) return null;
      vetState.especies.add(e.label); title = e.label; kicker = 'Menú anatómicos'; photo = especieImg(e.label); crumb = e.label;
    }
    const cats = [...new Set(VET.productos.map((p) => cap(p.categoria)).filter(Boolean))].sort();
    const chip = (k, v, label) => `<button type="button" class="chip" data-vk="${k}" data-value="${esc(v)}" aria-pressed="false">${label}</button>`;
    return `
      <section class="vet-head${photo ? ' with-photo' : ''}">
        ${photo ? `<div class="vet-head-photo">${img(photo, title)}</div>` : ''}
        <div class="wrap">
          ${vetHeroCrumbs([{ label: crumb }])}
          <span class="kicker">${kicker}</span>
          <h1 class="h-display">${title}</h1>
          ${kind === 'especie' ? `<p class="vet-lead">Productos cuya ficha indica uso en ${title.toLowerCase()}. La ficha de cada producto detalla especies, dosis y advertencias.</p>` : `<p class="vet-lead">${V.intro}</p>`}
        </div>
      </section>
      <section class="catalog vet-body">
        <div class="wrap catalog-grid">
          <aside class="filters" aria-label="Filtros">
            <h3>Filtrar por:</h3>
            <label class="search">${ICON.search}<input type="search" placeholder="Buscar producto o principio activo" aria-label="Buscar producto" data-vq></label>
            <div class="f-group"><span>Línea</span><div class="chips">${V.lineas.map((l) => chip('linea', l.id, `${l.grupo.split(' ')[0]} · ${l.linea}`)).join('')}</div></div>
            <div class="f-group"><span>Especie</span><div class="chips">${V.especies.map((e) => chip('especie', e.label, e.label)).join('')}</div></div>
            <div class="f-group"><span>Categoría</span><div class="chips">${cats.map((c) => chip('cat', c, c)).join('')}</div></div>
            <button type="button" class="clear" data-vclear>Borrar todos los filtros</button>
          </aside>
          <div>
            <div class="results-bar"><span data-vcount></span></div>
            <div class="product-grid" data-vgrid>${VET.productos.map((p, i) => vetCard(p, i)).join('')}</div>
            <div class="empty" hidden>No hay productos con estos filtros. <button type="button" data-vclear>Borrar todos los filtros</button></div>
          </div>
        </div>
      </section>`;
  }

  function mountVetProductos() {
    const cards = $$('[data-vgrid] .product-card');
    const q = $('[data-vq]');
    const sets = { linea: vetState.lineas, especie: vetState.especies, cat: vetState.cats };
    const sync = () => $$('[data-vk]').forEach((c) => c.setAttribute('aria-pressed', String(sets[c.dataset.vk].has(c.dataset.value))));
    const apply = (animate = true) => {
      const first = new Map(cards.map((c) => [c, c.getBoundingClientRect()]));
      let n = 0;
      cards.forEach((c) => {
        const p = vetFind(c.dataset.vid);
        const ok = (!vetState.lineas.size || lineaId(p).some((x) => vetState.lineas.has(x)))
          && (!vetState.especies.size || especiesDe(p).some((x) => vetState.especies.has(x)))
          && (!vetState.cats.size || vetState.cats.has(cap(p.categoria)))
          && (!vetState.q || norm([p.name, p.sub, p.forma, p.categoria].join(' ')).includes(norm(vetState.q)));
        c.hidden = !ok; if (ok) n++;
      });
      $('[data-vcount]').textContent = `${n} ${n === 1 ? 'producto' : 'productos'}`;
      $('.empty').hidden = n > 0;
      if (!animate || reduceMotion) return;
      cards.forEach((c) => {
        if (c.hidden) return;
        const a = first.get(c), b = c.getBoundingClientRect();
        if (!a.width) { c.animate([{ opacity: 0, transform: 'scale(.92)' }, { opacity: 1, transform: 'none' }], { duration: 450, easing: 'cubic-bezier(.2,.8,.2,1)' }); return; }
        const dx = a.left - b.left, dy = a.top - b.top;
        if (dx || dy) c.animate([{ transform: `translate(${dx}px,${dy}px)` }, { transform: 'none' }], { duration: 500, easing: 'cubic-bezier(.2,.8,.2,1)' });
      });
    };
    $$('[data-vk]').forEach((c) => c.addEventListener('click', () => {
      const s = sets[c.dataset.vk];
      s.has(c.dataset.value) ? s.delete(c.dataset.value) : s.add(c.dataset.value);
      sync(); apply();
    }));
    q.addEventListener('input', () => { vetState.q = q.value.trim(); apply(); });
    $$('[data-vclear]').forEach((b) => b.addEventListener('click', () => { Object.values(sets).forEach((s) => s.clear()); vetState.q = ''; q.value = ''; sync(); apply(); }));
    sync(); apply(false);
  }

  function viewVetProducto(id) {
    const p = vetFind(id);
    if (!p) return null;
    const f = p.ficha || {};
    const esp = especiesDe(p);
    const fondo = (f.imagenes || [])[0];
    const related = VET.productos.filter((x) => x.id !== p.id && (x.name.split(' ')[0] === p.name.split(' ')[0] || (x.categoria === p.categoria && lineaId(x).some((l) => lineaId(p).includes(l))))).slice(0, 8);
    const lid = lineaId(p)[0];
    const l = V.lineas.find((x) => x.id === lid);
    return `
      <section class="product-hero vet-product">
        <div class="hero-bg soft vet"></div>
        <div class="wrap">
          ${vetHeroCrumbs([...(l ? [{ label: `${l.grupo} · ${l.linea}`, route: `#/veterinaria/linea/${l.id}` }] : []), { label: esc(p.name) }])}
          <div class="product-detail">
            <div class="product-stage" data-stage>
              ${disc('glass float', 'width:38%;height:38%;right:-6%;top:-4%;--dur:8s')}
              <span class="stage-paw" aria-hidden="true">${ICON.paw}</span>
              ${img(p.img, p.name, 'stage-img', 'loading="eager"')}
            </div>
            <div class="product-info">
              <div class="pc-tags big"><span>${esc(cap(p.forma))}</span>${p.categoria ? `<span>${esc(cap(p.categoria))}</span>` : ''}${p.lineas.map((x) => `<span class="ln">${x}</span>`).join('')}</div>
              <h1 class="h-display product-name">${esc(f.title || p.name)}</h1>
              ${f.subtitle || p.sub ? `<p class="vet-sub">${esc(f.subtitle || cap(p.sub))}</p>` : ''}
              ${esp.length ? `<div class="vet-uso"><span>Uso</span>${esp.map((e) => { const s = V.especies.find((x) => x.label === e); return s ? `<a href="#/veterinaria/especie/${s.id}">${img(especieImg(e), e)}${e}</a>` : `<span>${e}</span>`; }).join('')}</div>` : ''}
              <div class="buy-box">
                <p class="buy-title">${ICON.info} ¿Dudas sobre este producto?</p>
                <div class="hero-ctas">
                  <a class="btn magnetic" href="${V.contacto.ventas.href}">${V.contacto.ventas.label}: ${V.contacto.ventas.value}</a>
                  <a class="btn ghost-dark magnetic" href="mailto:${V.contacto.email}?subject=${encodeURIComponent(p.name)}">${ICON.mail} Gerencia médica</a>
                </div>
                ${p.url ? `<p class="buy-note">${ext(p.url, `Ver ficha en chinoinveterinaria.com ${ICON.ext}`, 'inline-ext')}</p>` : ''}
              </div>
              <ul class="help-links"><li><a href="#/veterinaria/productos">${ICON.back} Regresar a los productos</a></li></ul>
            </div>
          </div>
        </div>
      </section>
      ${fondo ? `<section class="vet-fondo"><div class="wrap"><button type="button" class="vet-fondo-img reveal" data-lightbox="${fondo}">${img(fondo, p.name)}</button></div></section>` : ''}
      ${(f.secciones || []).length ? `
      <section class="ficha-section" id="ficha"><div class="wrap">
        <div class="ficha">${f.secciones.map((s, i) => `
          <details class="ficha-item"${i < 3 ? ' open' : ''}>
            <summary><span>${esc(s.t)}</span><i>${ICON.chev}</i></summary>
            <div class="ficha-body">${(() => {
              let out = '', inList = false;
              s.p.forEach(([k, t]) => {
                if (k === 'li' && !inList) { out += '<ul>'; inList = true; }
                if (k !== 'li' && inList) { out += '</ul>'; inList = false; }
                out += k === 'li' ? `<li>${esc(t)}</li>` : `<p>${esc(t)}</p>`;
              });
              return out + (inList ? '</ul>' : '');
            })()}</div>
          </details>`).join('')}</div>
        ${(f.presentaciones || []).length ? `<h2 class="h-section" style="font-size:clamp(28px,3vw,40px);margin:50px 0 20px">Presentación</h2>
          <div class="vet-pres">${f.presentaciones.map((x) => `<figure class="reveal">${x.img ? img(x.img, x.text) : ''}<figcaption>${esc(x.text)}</figcaption></figure>`).join('')}</div>` : ''}
      </div></section>` : ''}
      ${related.length ? `
      <section class="section related vet-body">
        <div class="wrap"><div class="section-head"><div class="reveal"><span class="kicker">También te puede interesar</span><h2 class="h-section">Productos <em>relacionados</em></h2></div></div></div>
        <div class="rail" data-rail><div class="rail-track">${related.map((x, i) => vetCard(x, i)).join('')}</div></div>
      </section>` : ''}`;
  }

  const view404 = () => pageHero({ kicker: 'Error 404', title: 'Página no <em>encontrada</em>', crumbs: [{ label: '404' }], compact: true }) +
    `<section class="page-body"><div class="wrap"><a class="btn" href="#/">Volver al inicio <span class="arrow">${ICON.arrow}</span></a></div></section>`;

  /* ============================================================
     Router (mismas direcciones que chinoin.com/es)
     ============================================================ */
  const PORTAFOLIO_RUTAS = {
    'portafolio-respiratorios': 'respiratorios', 'portafolio-gastrointestinales': 'gastrointestinales', 'portafolio-ginecologicos': 'ginecologicos',
    'portafolio-cardiovasculares': 'cardiovasculares', 'portafolio-musculo-esqueleticos': 'musculo-esqueleticos',
    'portafolio-corticoesteroides': 'corticoesteroides', 'portafolio-hierros': 'hierros'
  };

  function resolve(hash) {
    const [a, b] = hash.replace(/^#\/?/, '').split('/').filter(Boolean);
    const page = (html, title, mount) => ({ html, title, mount });
    if (!a) return page(viewHome(), 'CHINOIN', mountHome);
    switch (a) {
      case 'catalogo': return page(viewCatalogo({}), 'Catálogo de productos', mountCatalogo);
      case 'producto': { const h = viewProducto(b); if (h) return page(h, findProduct(b).name, mountProducto); break; }
      case 'ficha': { const h = viewFichaSuelta(b); if (h) return page(h, D.fichasSueltas.find((x) => x.id === b).name); break; }
      case 'medicamentos-prescripcion': return page(viewPrescripcion(), 'Medicamentos de prescripción');
      case 'cuidado-de-la-salud': return page(viewCuidado(), 'Medicamentos de venta libre');
      case 'probioticos': return page(viewPortafolio('probioticos', { grupo: 'Probióticos' }), 'Probióticos');
      case 'odontologia': return page(viewPortafolio('odontologia', { grupo: 'Odontología' }), 'Odontología');
      case 'veterinaria': {
        if (!b) return page(viewVeterinaria(), 'Veterinaria', mountVeterinaria);
        const c = hash.replace(/^#\/?/, '').split('/').filter(Boolean)[2];
        if (b === 'productos') return page(viewVetProductos('todos'), 'Productos veterinarios', mountVetProductos);
        if (b === 'linea' || b === 'especie') { const h = viewVetProductos(b, c); if (h) return page(h, 'Veterinaria', mountVetProductos); }
        if (b === 'producto') { const h = viewVetProducto(c); if (h) return page(h, vetFind(c).name, mountProducto); }
        break;
      }
      case 'calidad-chinoin': return page(viewCalidad(), 'Calidad');
      case 'responsabilidad-social': return page(viewResponsabilidad(), 'Responsabilidad Social');
      case 'tecnologia': return page(viewTecnologia(), 'Tecnología');
      case 'unidades-de-negocio': return page(viewUnidades(), 'Unidades de Negocio', () => mountUnidades(b));
      case 'contacto': return page(viewContacto(), 'Contacto', mountContacto);
      case 'farmacovigilancia': return page(viewFarmacovigilancia(), 'Farmacovigilancia', mountStepper);
      case 'unete-al-equipo': return page(viewUnete(), 'Únete al equipo');
      case 'biblioteca-virtual': return page(viewBiblioteca(), 'Biblioteca Virtual');
      case 'libro-100': return page(viewLibro100(), '100 años');
      case 'aviso-de-privacidad': return page(viewAviso(), 'Aviso de Privacidad');
      default:
        if (PORTAFOLIO_RUTAS[a]) return page(viewPortafolio(PORTAFOLIO_RUTAS[a], { route: '#/' + a }), D.portafolios[PORTAFOLIO_RUTAS[a]].title);
        if (PADECIMIENTOS.some((p) => p.id === a)) return page(viewPadecimiento(a), padLabel(a));
    }
    return page(view404(), 'Página no encontrada');
  }

  let first = true;
  let lastBase = null;
  function route() {
    const anchor = location.hash && !location.hash.startsWith('#/') ? location.hash.slice(1) : null;
    if (anchor && document.getElementById(anchor)) return;
    const hash = anchor ? '#/' : (location.hash || '#/');
    // Dentro de Unidades de negocio solo se desplaza, sin recargar la vista
    const base = hash.split('/').slice(0, 2).join('/');
    if (!first && base === '#/unidades-de-negocio' && lastBase === base) { mountUnidades(hash.split('/')[2]); return; }
    lastBase = base;
    const go = () => {
      const r = resolve(hash);
      const view = $('#view');
      view.innerHTML = r.html;
      view.classList.remove('view-enter'); void view.offsetWidth; view.classList.add('view-enter');
      document.title = r.title === 'CHINOIN' ? 'CHINOIN® · Farmacéutica Mexicana' : `${String(r.title).replace(/<[^>]+>/g, '')} · CHINOIN®`;
      const target = anchor && document.getElementById(anchor);
      if (target) target.scrollIntoView(); else scrollTo({ top: 0, behavior: 'instant' });
      if (r.mount) r.mount();
      enhance(view);
      if (!first) view.focus({ preventScroll: true });
      first = false;
    };
    if (first || reduceMotion) return go();
    const curtain = $('.curtain');
    curtain.classList.remove('run'); void curtain.offsetWidth; curtain.classList.add('run');
    setTimeout(go, 420);
  }

  /* ============================================================
     Interacción y movimiento
     ============================================================ */
  let revealObs;
  function enhance(root) {
    revealObs && revealObs.disconnect();
    revealObs = new IntersectionObserver((entries) => entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add('in'); revealObs.unobserve(e.target); }
    }), { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    splitWords(root);
    $$('.reveal, .split', root).forEach((el) => revealObs.observe(el));
    heroParallax();
    countUp(root);
    sliders(root);
    rails(root);
    autoScroll(root);
    $$('form[data-demo]:not(.stepper)', root).forEach((f) => f.addEventListener('submit', (e) => e.preventDefault()));
    $$('[data-scroll]', root).forEach((a) => a.addEventListener('click', (e) => {
      e.preventDefault();
      const t = document.querySelector(a.getAttribute('href'));
      t && t.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth' });
    }));
  }

  // Divide los títulos en palabras para revelarlas una por una.
  function splitWords(root) {
    $$('.h-section, .page-hero .h-display', root).forEach((h) => {
      if (h.dataset.split) return;
      h.dataset.split = '1';
      let i = 0;
      const wrap = () => {
        const w = document.createElement('span');
        w.className = 'wm';
        const inner = document.createElement('span');
        inner.className = 'w';
        inner.style.setProperty('--w', i++);
        w.appendChild(inner);
        return [w, inner];
      };
      [...h.childNodes].forEach((n) => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach((part) => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
            const [w, inner] = wrap(); inner.textContent = part; frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') {
          const [w, inner] = wrap(); n.replaceWith(w); inner.appendChild(n);
        }
      });
      if (!h.closest('.reveal')) h.classList.add('split');
    });
  }

  function heroParallax() {
    if (reduceMotion) return;
    const hero = $('.hero, .page-hero');
    const layers = hero ? $$('.hero-scene .layer', hero) : [];
    if (!layers.length) return;
    hero.addEventListener('pointermove', (e) => {
      const r = hero.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5;
      const y = (e.clientY - r.top) / r.height - 0.5;
      layers.forEach((l) => { const d = +l.dataset.depth; l.style.transform = `translate3d(${-x * d}px, ${-y * d}px, 0)`; });
    });
  }

  function countUp(root) {
    const obs = new IntersectionObserver((es) => es.forEach((e) => {
      if (!e.isIntersecting) return;
      obs.unobserve(e.target);
      const el = e.target, end = +el.dataset.count;
      if (reduceMotion) { el.textContent = end; return; }
      const t0 = performance.now();
      const step = (t) => {
        const k = Math.min(1, (t - t0) / 1600);
        el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3)));
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    }), { threshold: 0.5 });
    $$('[data-count]', root).forEach((el) => obs.observe(el));
  }

  // Carrusel de banners con avance automático
  function sliders(root) {
    $$('[data-slider]', root).forEach((s) => {
      const slides = $$('.slide', s), dots = $$('.sl-dots button', s);
      let i = 0, timer;
      const go = (n) => {
        i = (n + slides.length) % slides.length;
        slides.forEach((x, k) => x.classList.toggle('is-active', k === i));
        dots.forEach((d, k) => d.toggleAttribute('aria-current', k === i));
        restart();
      };
      const restart = () => { clearInterval(timer); if (!reduceMotion) timer = setInterval(() => go(i + 1), 5200); };
      $('.sl-prev', s).addEventListener('click', () => go(i - 1));
      $('.sl-next', s).addEventListener('click', () => go(i + 1));
      dots.forEach((d, k) => d.addEventListener('click', () => go(k)));
      let x0 = null;
      s.addEventListener('pointerdown', (e) => { x0 = e.clientX; });
      s.addEventListener('pointerup', (e) => { if (x0 !== null && Math.abs(e.clientX - x0) > 40) go(i + (e.clientX < x0 ? 1 : -1)); x0 = null; });
      restart();
    });
  }

  // Rieles horizontales que se arrastran con el mouse y avanzan con la rueda
  function rails(root) {
    $$('[data-rail]', root).forEach((r) => {
      let down = false, sx = 0, sl = 0, moved = false;
      r.addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse') return; down = true; moved = false; sx = e.clientX; sl = r.scrollLeft; r.classList.add('dragging'); });
      addEventListener('pointerup', () => { down = false; r.classList.remove('dragging'); });
      r.addEventListener('pointermove', (e) => { if (!down) return; const dx = e.clientX - sx; if (Math.abs(dx) > 4) moved = true; r.scrollLeft = sl - dx; });
      r.addEventListener('click', (e) => { if (moved) { e.preventDefault(); e.stopPropagation(); } }, true);
    });
  }

  // La línea del tiempo se desplaza sola dentro de su marco
  function autoScroll(root) {
    $$('[data-autoscroll]', root).forEach((box) => {
      if (reduceMotion) return;
      let hover = false, y = 0;
      box.addEventListener('pointerenter', () => { hover = true; });
      box.addEventListener('pointerleave', () => { hover = false; y = box.scrollTop; });
      const tick = () => {
        if (!box.isConnected) return;
        if (!hover && box.getBoundingClientRect().top < innerHeight) {
          y += 0.45;
          if (y >= box.scrollHeight - box.clientHeight) y = 0;
          box.scrollTop = y;
        }
        requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  }

  // Visor de imágenes a pantalla completa
  function lightbox() {
    document.body.insertAdjacentHTML('beforeend', `<div class="lightbox" hidden><button class="lb-close" aria-label="Cerrar">${ICON.close}</button><div class="lb-stage"></div></div>`);
    const lb = $('.lightbox'), stage = $('.lb-stage', lb);
    const close = () => { lb.hidden = true; stage.innerHTML = ''; document.body.style.overflow = ''; };
    document.addEventListener('click', (e) => {
      const t = e.target.closest('[data-lightbox]');
      if (!t) return;
      if (t.dataset.video) { open(t.dataset.video, '_blank', 'noopener'); return; }
      stage.innerHTML = `<img src="${t.dataset.lightbox}" alt="">`;
      lb.hidden = false; document.body.style.overflow = 'hidden';
      stage.classList.toggle('tall', /timeline/.test(t.dataset.lightbox));
    });
    lb.addEventListener('click', (e) => { if (e.target === lb || e.target.closest('.lb-close')) close(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !lb.hidden) close(); });
  }

  // Etiqueta del cursor según lo que hay debajo
  const CURSOR_LABELS = [
    ['.product-card, .photo-card, .logo-card:not(.static), .unit, .contact-card, .mega-feature, .book, .specie, .vline', 'Ver'],
    ['[data-rail]', 'Arrastra'],
    ['[data-lightbox]', 'Ampliar'],
    ['.marquee a', 'Ir']
  ];

  function globalFx() {
    const glow = $('.cursor-glow');
    const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
    document.body.insertAdjacentHTML('beforeend', '<div class="cursor" aria-hidden="true"><span class="cursor-ring"><b></b></span><span class="cursor-dot"></span></div><div class="progress" aria-hidden="true"></div>');
    const cursor = $('.cursor'), ring = $('.cursor-ring'), dot = $('.cursor-dot');
    let gx = -999, gy = -999, rx = gx, ry = gy, tx = gx, ty = gy;
    if (fine && !reduceMotion) document.documentElement.classList.add('has-cursor');
    addEventListener('pointermove', (e) => {
      tx = e.clientX; ty = e.clientY;
      dot.style.transform = `translate3d(${tx}px, ${ty}px, 0)`;
      const t = e.target.closest ? e.target : null;
      const hit = t && CURSOR_LABELS.find(([sel]) => t.closest(sel));
      cursor.classList.toggle('is-label', !!hit);
      cursor.classList.toggle('is-link', !hit && !!(t && t.closest('a, button, summary, label')));
      cursor.classList.toggle('on-dark', !!(t && t.closest('.hero, .page-hero, .units, .site-footer, .portal-card, .marquee, .innov')));
      if (hit) $('b', ring).textContent = hit[1];
    }, { passive: true });
    document.addEventListener('pointerdown', () => cursor.classList.add('is-down'));
    document.addEventListener('pointerup', () => cursor.classList.remove('is-down'));
    document.documentElement.addEventListener('pointerleave', () => cursor.classList.add('is-hidden'));
    document.documentElement.addEventListener('pointerenter', () => cursor.classList.remove('is-hidden'));
    const loop = () => {
      gx += (tx - gx) * 0.08; gy += (ty - gy) * 0.08;
      rx += (tx - rx) * 0.2; ry += (ty - ry) * 0.2;
      glow.style.transform = `translate3d(${gx}px, ${gy}px, 0)`;
      ring.style.transform = `translate3d(${rx}px, ${ry}px, 0)`;
      requestAnimationFrame(loop);
    };
    if (!reduceMotion) loop();

    // Inclinación 3D de las tarjetas
    const TILT = '.contact-card, .stat-card, .product-card, .portal-card, .photo-card, .logo-card:not(.static), .book, .sede, .via, .badge-card';
    let tilted = null;
    document.addEventListener('pointermove', (e) => {
      if (reduceMotion || !fine) return;
      const card = e.target.closest && e.target.closest(TILT);
      if (tilted && tilted !== card) { tilted.style.transform = ''; tilted.classList.remove('is-tilt'); }
      tilted = card;
      if (!card || card.closest('.dragging')) return;
      const r = card.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5;
      const y = (e.clientY - r.top) / r.height - 0.5;
      const k = card.classList.contains('portal-card') ? 3 : 8;
      card.classList.add('is-tilt');
      card.style.transform = `perspective(1000px) rotateX(${-y * k}deg) rotateY(${x * k}deg) translateY(-6px)`;
      card.style.setProperty('--gx', `${(x + 0.5) * 100}%`);
      card.style.setProperty('--gy', `${(y + 0.5) * 100}%`);
    }, { passive: true });

    // Botones magnéticos
    if (!reduceMotion) {
      document.addEventListener('pointermove', (e) => {
        const b = e.target.closest && e.target.closest('.magnetic');
        $$('.magnetic.is-pulled').forEach((x) => { if (x !== b) { x.style.transform = ''; x.classList.remove('is-pulled'); } });
        if (!b) return;
        const r = b.getBoundingClientRect();
        b.classList.add('is-pulled');
        b.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * 0.18}px, ${(e.clientY - r.top - r.height / 2) * 0.3}px)`;
      }, { passive: true });
    }

    // Scroll: header, barra de progreso, portada, marquee y círculo dorado
    const header = $('.site-header');
    const progress = $('.progress');
    let lastY = scrollY, velocity = 0, ticking = false;
    const onScroll = () => {
      ticking = false;
      const y = scrollY;
      velocity = y - lastY;
      header.classList.toggle('is-hidden', y > 200 && velocity > 0 && !$('.nav-item.is-open'));
      header.classList.toggle('is-scrolled', y > 40);
      lastY = y;
      const max = document.documentElement.scrollHeight - innerHeight;
      progress.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
      if (reduceMotion) return;
      $$('[data-parallax]').forEach((el) => { el.style.transform = `translate3d(${y * +el.dataset.parallax}px,0,0)`; });
      const hero = $('.hero, .page-hero');
      if (hero) {
        const h = hero.offsetHeight;
        const p = Math.min(1, Math.max(0, y / h));
        const scene = $('.hero-scene', hero);
        const copy = $('.hero-inner, .page-hero > .wrap', hero);
        const photo = $('.ph-photo', hero);
        if (scene) scene.style.transform = `translate3d(0, ${y * 0.3}px, 0) scale(${1 + p * 0.18})`;
        if (photo) photo.style.transform = `translate3d(0, ${y * 0.35}px, 0) scale(${1.05 + p * 0.1})`;
        if (copy) { copy.style.transform = `translate3d(0, ${y * -0.08}px, 0)`; copy.style.opacity = String(Math.max(0, 1 - p * 2)); }
      }
      const track = $('.marquee-track');
      const anim = track && track.getAnimations && track.getAnimations()[0];
      if (anim) {
        anim.playbackRate = Math.min(6, 1 + Math.abs(velocity) * 0.12) * (velocity < 0 ? -1 : 1);
        clearTimeout(onScroll.t);
        onScroll.t = setTimeout(() => { anim.playbackRate = 1; }, 160);
      }
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  }

  // Pantalla de carga con el logo original
  function preloader() {
    if (reduceMotion) { document.documentElement.classList.add('loaded'); return; }
    document.body.insertAdjacentHTML('afterbegin', `
      <div class="preloader" aria-hidden="true">
        <div class="pl-inner">
          <img src="${$('.brand img').getAttribute('src')}" alt="">
          <span class="pl-bar"><i></i></span>
          <span class="pl-count">0</span>
        </div>
      </div>`);
    const pl = $('.preloader');
    const count = $('.pl-count', pl);
    const t0 = performance.now();
    const tick = (t) => {
      const k = Math.min(1, (t - t0) / 1100);
      count.textContent = Math.round(k * 100);
      if (k < 1) return requestAnimationFrame(tick);
      pl.classList.add('done');
      document.documentElement.classList.add('loaded');
      setTimeout(() => pl.remove(), 1100);
    };
    requestAnimationFrame(tick);
  }

  /* ---------- Arranque ---------- */
  document.body.insertAdjacentHTML('beforeend', '<div class="curtain" aria-hidden="true"></div>');
  renderNav();
  renderMobile();
  renderFooter();
  preloader();
  globalFx();
  lightbox();
  addEventListener('hashchange', route);
  route();
})();
