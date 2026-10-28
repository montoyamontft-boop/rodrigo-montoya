(() => {
  'use strict';

  const D = window.CHINOIN;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const slug = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
    .replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  /* ---------- Íconos (equivalentes a los del menú original) ---------- */
  const ICON = {
    file: '<svg viewBox="0 0 24 24"><path d="M6 2h8l6 6v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2Zm7 1.5V9h5.5L13 3.5ZM11 11v3H8v2h3v3h2v-3h3v-2h-3v-3h-2Z" fill-rule="evenodd"/></svg>',
    house: '<svg viewBox="0 0 24 24"><path d="M12 2.5 1.5 11.2l1.3 1.5L4 11.7V21h16v-9.3l1.2 1 1.3-1.5L19 8.3V4h-3v1.8L12 2.5Zm-1 9V14H8.5v2H11v2.5h2V16h2.5v-2H13v-2.5h-2Z" fill-rule="evenodd"/></svg>',
    apple: '<svg viewBox="0 0 24 24"><path d="M15.6 2.2c.1 1.2-.4 2.3-1.1 3.1-.8.8-1.8 1.3-2.8 1.2-.1-1.1.4-2.3 1.1-3 .8-.8 1.9-1.3 2.8-1.3ZM12 8.2c1-.5 2.4-1 3.6-1 2 0 3.6 1.1 4.4 2.7-3.7 2-3 7 .6 8.3-.9 2.2-2.6 4.6-4.4 4.6-1.4 0-1.8-.8-3.6-.8s-2.3.8-3.6.8C6.4 22.8 3.4 18.2 3.4 13.6c0-3.6 2.3-6.4 5.2-6.4 1.3 0 2.5.6 3.4 1Z"/></svg>',
    teeth: '<svg viewBox="0 0 24 24"><path d="M5 6h14a3 3 0 0 1 3 3v6a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3V9a3 3 0 0 1 3-3Zm.5 2.5a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1a1 1 0 0 0-1-1h-1Zm4 0a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1a1 1 0 0 0-1-1h-1Zm4 0a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1a1 1 0 0 0-1-1h-1Zm4 0a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1a1 1 0 0 0-1-1h-1Zm-12 4a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1a1 1 0 0 0-1-1h-1Zm4 0a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1a1 1 0 0 0-1-1h-1Zm4 0a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1a1 1 0 0 0-1-1h-1Zm4 0a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1v-1a1 1 0 0 0-1-1h-1Z" fill-rule="evenodd"/></svg>',
    paw: '<svg viewBox="0 0 24 24"><ellipse cx="5" cy="10.5" rx="2.2" ry="2.8"/><ellipse cx="9.3" cy="5.8" rx="2.3" ry="3"/><ellipse cx="14.7" cy="5.8" rx="2.3" ry="3"/><ellipse cx="19" cy="10.5" rx="2.2" ry="2.8"/><path d="M12 11c2.4 0 4 2.3 5.4 4.4 1 1.6.9 3.8-.9 4.6-1.4.6-2.8-.4-4.5-.4s-3.1 1-4.5.4c-1.8-.8-1.9-3-.9-4.6C8 13.3 9.6 11 12 11Z"/></svg>',
    chev: '<svg viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg>',
    arrow: '<svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    diag: '<svg viewBox="0 0 24 24"><path d="M7 17 17 7M8 7h9v9"/></svg>',
    down: '<svg viewBox="0 0 24 24"><path d="M12 5v14M6 13l6 6 6-6"/></svg>',
    info: '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm-1 9v6h2v-6h-2Zm0-4v2h2V7h-2Z" fill-rule="evenodd"/></svg>'
  };

  // Índices derivados del contenido
  const groups = D.productGroups.map((src) => {
    const g = { ...src, route: `#/productos/${src.key}` };
    g.categories = src.categories.map((c) => ({ label: c, slug: slug(c), group: g, route: `#/productos/${slug(c)}` }));
    return g;
  });
  const categories = groups.flatMap((g) => g.categories);
  const findCategory = (s) => categories.find((c) => c.slug === s);
  const findGroup = (s) => groups.find((g) => g.key === s);
  const productsIn = (s) => D.products.filter((p) => p.category === s);

  const disc = (cls, style) => `<span class="disc ${cls || ''}" style="${style}"></span>`;
  const capsule = (style) => `<span class="capsule" style="${style}"></span>`;

  /* ============================================================
     Header: navegación de escritorio, mega menú y menú móvil
     ============================================================ */
  function megaHTML() {
    const [areas, cuidado, ...rest] = groups;
    const col = (g) => `
      <div class="mega-group">
        <span class="icon-bubble">${ICON[g.icon]}</span>
        <h3><a href="${g.route}">${g.label}</a></h3>
        ${g.categories.length ? `<ul>${g.categories.map((c) => `<li><a href="${c.route}">${c.label}</a></li>`).join('')}</ul>` : ''}
      </div>`;
    return `
      <div class="mega" role="menu">
        <div class="mega-stack">${col(areas)}${rest.map(col).join('')}</div>
        ${col(cuidado)}
        <a class="mega-feature" href="#/productos">
          ${disc('glass float', 'width:150px;height:150px;top:-40px;right:-30px;--dur:7s')}
          ${capsule('width:120px;height:44px;top:70px;right:40px;rotate:-30deg')}
          <h4>Todo el <em>catálogo</em></h4>
          <p>Explora las líneas de producto de CHINOIN.</p>
          <span class="btn light" style="align-self:flex-start">Ver productos <span class="arrow">${ICON.arrow}</span></span>
        </a>
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
        ? groups.map((g) => `<h4><a href="${g.route}" style="padding:0;color:inherit;font-size:inherit">${g.label}</a></h4>${g.categories.map((c) => `<a href="${c.route}">${c.label}</a>`).join('')}`).join('')
        : item.items.map((s) => `<a href="${s.route}">${s.label}</a>`).join('');
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
    const cols = D.nav.filter((n) => !n.href).map((n) => {
      const links = n.mega ? groups.map((g) => ({ label: g.label, route: g.route })) : n.items;
      return `<div><h4>${n.label}</h4><ul>${links.map((l) => `<li><a href="${l.route}">${l.label}</a></li>`).join('')}</ul></div>`;
    }).join('');
    $('.footer-cols').innerHTML = cols;
    $('[data-year]').textContent = new Date().getFullYear();
  }

  /* ============================================================
     Vistas
     ============================================================ */
  function heroScene() {
    // Composición de discos y cápsulas en tres profundidades para el parallax.
    return `
      <div class="hero-scene" aria-hidden="true">
        <div class="layer" data-depth="10">
          ${disc('float', 'width:min(34vw,460px);height:min(34vw,460px);left:52%;top:16%;--dur:11s;--dy:-30px;--r1:12deg')}
          ${disc('glass float', 'width:180px;height:180px;left:86%;top:58%;--dur:8s;--dy:24px')}
        </div>
        <div class="layer" data-depth="26">
          ${disc('glass float', 'width:min(26vw,340px);height:min(26vw,340px);left:70%;top:6%;--dur:9s;--dx:-20px;--r1:-10deg')}
          ${capsule('width:min(22vw,280px);height:min(8vw,100px);left:58%;top:66%;rotate:-28deg')}
        </div>
        <div class="layer" data-depth="48">
          ${disc('float', 'width:90px;height:90px;left:48%;top:12%;--dur:6s;--dy:18px')}
          ${capsule('width:150px;height:54px;left:88%;top:28%;rotate:52deg')}
          ${disc('glass float', 'width:60px;height:60px;left:62%;top:52%;--dur:5s')}
        </div>
      </div>`;
  }

  function catCard(c, i, big) {
    return `
      <a class="cat-card${big ? ' big' : ''}" href="${c.route}" style="--i:${i}">
        <span class="idx">${String(i + 1).padStart(2, '0')}${c.group ? ' · ' + c.group.label : ''}</span>
        <span class="go">${ICON.diag}</span>
        <span class="capsule ghost-pill" aria-hidden="true"></span>
        <h3>${c.label}</h3>
      </a>`;
  }

  function viewHome() {
    const tabs = groups.map((g, i) => `<button class="tab" role="tab" aria-selected="${i === 0}" data-g="${g.key}">${ICON[g.icon]}<span>${g.label}</span></button>`).join('');
    const allCats = groups.flatMap((g) => g.categories).map((c) => `<a href="${c.route}">${c.label}</a>`).join('');
    const units = D.nav.find((n) => n.key === 'unidades').items;
    const about = D.nav.find((n) => n.key === 'nosotros').items;
    const contact = D.nav.find((n) => n.key === 'contacto').items;

    return `
      <section class="hero">
        <div class="hero-bg"></div>
        ${heroScene()}
        <div class="hero-grain"></div>
        <div class="wrap hero-inner">
          <div class="hero-copy">
            <span class="kicker">Laboratorio farmacéutico mexicano</span>
            <h1 class="h-display">
              <span class="line"><span>Ciencia mexicana</span></span>
              <span class="line"><span>para la <em>salud</em></span></span>
              <span class="line"><span>desde 1925.</span></span>
            </h1>
            <p class="hero-sub">Medicamentos para la salud humana y animal, desarrollados y fabricados en México.</p>
            <div class="hero-ctas">
              <a class="btn magnetic" href="#/productos">Ver productos <span class="arrow">${ICON.arrow}</span></a>
              <a class="btn ghost magnetic" href="portal-medico.html">Portal Médico</a>
            </div>
          </div>
          <div class="hero-side">
            <div class="stat-card solid"><div class="num" data-count="1925" data-plain>1925</div><div class="lbl"><span>Año de fundación</span></div></div>
            <div class="stat-card"><div class="num"><span data-count="${categories.length + groups.filter((g) => !g.categories.length).length}">0</span></div><div class="lbl"><span>Líneas de producto</span></div></div>
          </div>
        </div>
        <div class="hero-giant" aria-hidden="true" data-parallax="-0.12">100 años</div>
        <div class="hero-bar">
          <div class="wrap"><span>Áreas Terapéuticas · Cuidado de la salud · Benebióticos · Odontología · Veterinaria</span><a class="scroll-hint" href="#productos">Descubre más <i>${ICON.down}</i></a></div>
        </div>
      </section>
      <div class="marquee" aria-label="Categorías"><div class="marquee-track">${allCats}${allCats}</div></div>

      <section class="section" id="productos">
        <div class="wrap">
          <div class="section-head">
            <div class="reveal"><span class="kicker">Productos</span><h2 class="h-section">Encuentra tu <em>tratamiento</em></h2></div>
            <div class="tabs reveal" role="tablist" style="--d:.1s"><span class="tab-pill"></span>${tabs}</div>
          </div>
          <div class="cat-grid" id="cat-grid"></div>
        </div>
      </section>

      <section class="section about" id="nosotros">
        <div class="wrap">
          <div class="section-head">
            <div class="reveal"><span class="kicker">Nosotros</span><h2 class="h-section">Más de un siglo<br>de <em>compromiso</em></h2></div>
          </div>
          <div class="about-grid">
            ${about.map((a, i) => `
              <a class="about-card reveal" href="${a.route}" style="--d:${i * 0.1}s">
                ${i === 1 ? capsule('width:260px;height:96px;right:-50px;top:40px;rotate:-32deg') : disc(i ? '' : 'glass', `width:260px;height:260px;right:-70px;top:-60px`)}
                <span class="n">0${i + 1}</span>
                <div><h3>${a.label}</h3><span class="more">Conocer más <i>${ICON.diag}</i></span></div>
              </a>`).join('')}
          </div>
        </div>
      </section>

      <section class="section units" id="unidades">
        <div class="wrap">
          <div class="section-head">
            <div class="reveal"><span class="kicker">Unidades de Negocio</span><h2 class="h-section">Cinco formas de <em>llegar</em></h2></div>
          </div>
          <div class="unit-rail reveal">
            ${units.map((u, i) => `
              <a class="unit${i === 0 ? ' is-active' : ''}" href="${u.route}">
                ${disc('glass', '')}
                <span class="u-num">0${i + 1}</span>
                <div><h3>${u.label}</h3><span class="u-go">Ver más ${ICON.arrow}</span></div>
              </a>`).join('')}
          </div>
        </div>
      </section>

      <section class="portal-band">
        <div class="wrap">
          <div class="portal-card reveal">
            <div>
              <span class="kicker">Portal Médico</span>
              <h2 class="h-section">Un espacio para<br>profesionales de la <em>salud</em></h2>
              <p>Contenido disponible solo para usuarios registrados.</p>
              <a class="btn light magnetic" href="portal-medico.html">Iniciar sesión <span class="arrow">${ICON.arrow}</span></a>
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
            <div class="reveal"><span class="kicker">Contacto</span><h2 class="h-section">Hablemos</h2></div>
          </div>
          <div class="contact-grid">
            ${contact.map((c, i) => `
              <a class="contact-card reveal" href="${c.route}" style="--d:${i * 0.1}s">
                <span class="icon-bubble">${i ? ICON.file : ICON.house}</span>
                <div class="row"><h3>${c.label}</h3><span class="go">${ICON.diag}</span></div>
              </a>`).join('')}
          </div>
        </div>
      </section>`;
  }

  function mountHome() {
    const grid = $('#cat-grid');
    const pill = $('.tab-pill');
    const showGroup = (key) => {
      const g = findGroup(key);
      const list = g.categories.length ? g.categories : [{ label: g.label, route: g.route, group: null }];
      grid.innerHTML = list.map((c, i) => catCard(c, i, !g.categories.length)).join('');
      $$('.tab').forEach((t) => t.setAttribute('aria-selected', String(t.dataset.g === key)));
      movePill();
    };
    const movePill = () => {
      const t = $('.tab[aria-selected="true"]');
      if (!t || !pill) return;
      Object.assign(pill.style, { left: t.offsetLeft + 'px', top: t.offsetTop + 'px', width: t.offsetWidth + 'px', height: t.offsetHeight + 'px' });
    };
    $$('.tab').forEach((t) => t.addEventListener('click', () => showGroup(t.dataset.g)));
    addEventListener('resize', movePill);
    showGroup(groups[0].key);

    $$('.unit').forEach((u) => u.addEventListener('mouseenter', () => {
      $$('.unit').forEach((x) => x.classList.toggle('is-active', x === u));
    }));

    heroParallax();
    countUp();
  }

  function pageHero({ kicker, title, crumbs, siblings, current }) {
    return `
      <section class="page-hero">
        <div class="hero-bg"></div>
        <div class="hero-grain"></div>
        <div class="hero-scene" aria-hidden="true"><div class="layer" data-depth="20">
          ${disc('float', 'width:min(30vw,380px);height:min(30vw,380px);right:6%;top:24%;--dur:10s')}
          ${disc('glass float', 'width:160px;height:160px;right:26%;top:56%;--dur:7s;--dy:20px')}
          ${capsule('width:180px;height:64px;right:4%;top:70%;rotate:-26deg')}
        </div></div>
        <div class="wrap">
          <nav class="crumbs" aria-label="Ruta"><a href="#/">Inicio</a>${crumbs.map((c) => `<span aria-hidden="true">/</span>${c.route ? `<a href="${c.route}">${c.label}</a>` : `<span>${c.label}</span>`}`).join('')}</nav>
          <span class="kicker">${kicker}</span>
          <h1 class="h-display">${title}</h1>
          ${siblings ? `<div class="subnav">${siblings.map((s) => `<a href="${s.route}"${s.route === current ? ' aria-current="page"' : ''}>${s.label}</a>`).join('')}</div>` : ''}
        </div>
      </section>`;
  }

  const pendingNote = (what) => `
    <div class="pending reveal">
      <span class="icon-bubble">${ICON.info}</span>
      <div><strong>Contenido pendiente de cargar</strong><p>${what} se copiará tal cual desde chinoin.com.</p></div>
    </div>`;

  function productGrid(list) {
    if (!list.length) {
      return pendingNote('El catálogo y las fotos de producto de esta sección') +
        `<div class="product-grid" aria-hidden="true">${'<div class="product-card skeleton"><div class="shot"></div><div class="meta"><i></i><i></i></div></div>'.repeat(4)}</div>`;
    }
    return `<div class="product-grid">${list.map((p, i) => `
      <a class="product-card reveal" href="#/producto/${esc(p.id)}" style="--d:${(i % 4) * 0.06}s">
        <div class="shot"><img src="${esc(p.image)}" alt="${esc(p.name)}" loading="lazy"></div>
        <div class="meta"><h3>${esc(p.name)}</h3></div>
      </a>`).join('')}</div>`;
  }

  function viewProducts() {
    return pageHero({ kicker: 'Productos', title: 'Nuestros <em>productos</em>', crumbs: [{ label: 'Productos' }], siblings: groups.map((g) => ({ label: g.label, route: g.route })) }) + `
      <section class="page-body"><div class="wrap group-list">
        ${groups.map((g) => `
          <div>
            <div class="section-head reveal" style="margin-bottom:0">
              <div style="display:flex;gap:18px;align-items:center"><span class="icon-bubble">${ICON[g.icon]}</span><h2 class="h-section" style="margin:0;font-size:clamp(30px,3.6vw,52px)">${g.label}</h2></div>
              <a class="btn purple magnetic" href="${g.route}">Ver todo <span class="arrow">${ICON.arrow}</span></a>
            </div>
            ${g.categories.length ? `<div class="cat-grid">${g.categories.map((c, i) => catCard({ ...c, group: null }, i)).join('')}</div>` : ''}
          </div>`).join('')}
      </div></section>`;
  }

  function viewGroup(g) {
    const list = D.products.filter((p) => p.category === g.key || g.categories.some((c) => c.slug === p.category));
    return pageHero({ kicker: 'Productos', title: g.label, crumbs: [{ label: 'Productos', route: '#/productos' }, { label: g.label }], siblings: groups.map((x) => ({ label: x.label, route: x.route })), current: g.route }) + `
      <section class="page-body"><div class="wrap">
        ${g.categories.length ? `<div class="cat-grid" style="margin:0 0 60px">${g.categories.map((c, i) => catCard({ ...c, group: null }, i)).join('')}</div>` : ''}
        ${productGrid(list)}
      </div></section>`;
  }

  function viewCategory(c) {
    return pageHero({ kicker: c.group.label, title: c.label, crumbs: [{ label: 'Productos', route: '#/productos' }, { label: c.group.label, route: c.group.route }, { label: c.label }], siblings: c.group.categories, current: c.route }) + `
      <section class="page-body"><div class="wrap">${productGrid(productsIn(c.slug))}</div></section>`;
  }

  function viewProduct(p) {
    const c = findCategory(p.category);
    const g = c ? c.group : findGroup(p.category);
    return pageHero({ kicker: c ? c.label : (g ? g.label : 'Productos'), title: esc(p.name), crumbs: [{ label: 'Productos', route: '#/productos' }, ...(c ? [{ label: c.label, route: c.route }] : g ? [{ label: g.label, route: g.route }] : []), { label: esc(p.name) }] }) + `
      <section class="page-body"><div class="wrap product-detail">
        <div class="product-stage reveal"><img src="${esc(p.image)}" alt="${esc(p.name)}"></div>
        <div class="reveal" style="--d:.1s">
          <p class="prose">${esc(p.summary || '')}</p>
          ${p.buyUrl ? `<a class="btn magnetic" href="${esc(p.buyUrl)}" target="_blank" rel="noopener">Comprar <span class="arrow">${ICON.arrow}</span></a>` : ''}
        </div>
      </div></section>`;
  }

  function viewInfo(section, key) {
    const page = D.pages[section] && D.pages[section][key];
    if (!page) return null;
    const navItem = D.nav.find((n) => n.key === section);
    const route = `#/${section}/${key}`;
    const body = page.body.length
      ? `<div class="prose reveal">${page.body.map((p) => `<p>${esc(p)}</p>`).join('')}</div>`
      : pendingNote(`El texto de “${page.title}”`);
    return pageHero({ kicker: page.kicker, title: page.title, crumbs: [{ label: navItem.label }, { label: page.title }], siblings: navItem.items, current: route }) + `
      <section class="page-body"><div class="wrap" style="display:grid;gap:40px">${body}${formFor(key)}</div></section>`;
  }

  // Maqueta de formulario; el envío se conecta al mismo destino que usa chinoin.com.
  function formFor(key) {
    const f = (label, type = 'text', full) => `<div class="field${full ? ' full' : ''}"><label>${label}</label>${type === 'area' ? '<textarea></textarea>' : `<input type="${type}">`}</div>`;
    if (key === 'farmacovigilancia') {
      return `<form class="form-card reveal" data-demo>
        <h2 class="h-section" style="font-size:32px;margin:0 0 24px">Reporte de sospecha de reacción adversa</h2>
        <div class="form-grid">${f('Nombre')}${f('Correo', 'email')}${f('Teléfono', 'tel')}${f('Producto')}${f('Descripción del evento', 'area', true)}</div>
        <button class="btn" style="margin-top:24px" type="submit">Enviar reporte <span class="arrow">${ICON.arrow}</span></button>
      </form>`;
    }
    if (key === 'unete-al-equipo') {
      return `<form class="form-card reveal" data-demo>
        <h2 class="h-section" style="font-size:32px;margin:0 0 24px">Envíanos tus datos</h2>
        <div class="form-grid">${f('Nombre')}${f('Correo', 'email')}${f('Teléfono', 'tel')}${f('Área de interés')}${f('Mensaje', 'area', true)}</div>
        <button class="btn" style="margin-top:24px" type="submit">Enviar <span class="arrow">${ICON.arrow}</span></button>
      </form>`;
    }
    return '';
  }

  const view404 = () => pageHero({ kicker: 'Error 404', title: 'Página no <em>encontrada</em>', crumbs: [{ label: '404' }] }) +
    `<section class="page-body"><div class="wrap"><a class="btn" href="#/">Volver al inicio <span class="arrow">${ICON.arrow}</span></a></div></section>`;

  /* ============================================================
     Router
     ============================================================ */
  function resolve(hash) {
    const parts = hash.replace(/^#\/?/, '').split('/').filter(Boolean);
    const [a, b] = parts;
    if (!a) return { html: viewHome(), mount: mountHome, title: 'CHINOIN' };
    if (a === 'productos' && !b) return { html: viewProducts(), title: 'Productos' };
    if (a === 'productos') {
      const g = findGroup(b); if (g) return { html: viewGroup(g), title: g.label };
      const c = findCategory(b); if (c) return { html: viewCategory(c), title: c.label };
    }
    if (a === 'producto') {
      const p = D.products.find((x) => x.id === b); if (p) return { html: viewProduct(p), title: p.name };
    }
    if (['nosotros', 'unidades', 'contacto'].includes(a) && b) {
      const html = viewInfo(a, b); if (html) return { html, title: D.pages[a][b].title };
    }
    return { html: view404(), title: 'Página no encontrada' };
  }

  let first = true;
  function route() {
    // Anclas internas de la portada (#productos, #top…) solo desplazan.
    const anchor = location.hash && !location.hash.startsWith('#/') ? location.hash.slice(1) : null;
    if (anchor && document.getElementById(anchor)) return;
    const hash = anchor ? '#/' : location.hash;
    const go = () => {
      const r = resolve(hash);
      const view = $('#view');
      view.innerHTML = r.html;
      view.classList.remove('view-enter'); void view.offsetWidth; view.classList.add('view-enter');
      document.title = r.title === 'CHINOIN' ? 'CHINOIN' : `${r.title.replace(/<[^>]+>/g, '')} · CHINOIN`;
      const target = anchor && document.getElementById(anchor);
      if (target) target.scrollIntoView(); else scrollTo({ top: 0, behavior: 'instant' });
      if (r.mount) r.mount(); else heroParallax();
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
    $$('.reveal', root).forEach((el) => revealObs.observe(el));

    $$('form[data-demo]', root).forEach((f) => f.addEventListener('submit', (e) => {
      e.preventDefault();
      alert('Maqueta: el envío se conectará al mismo destino que usa chinoin.com.');
    }));
  }

  function heroParallax() {
    if (reduceMotion) return;
    const layers = $$('.hero-scene .layer');
    const hero = $('.hero, .page-hero');
    if (!hero || !layers.length) return;
    hero.addEventListener('pointermove', (e) => {
      const r = hero.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5;
      const y = (e.clientY - r.top) / r.height - 0.5;
      layers.forEach((l) => {
        const d = +l.dataset.depth;
        l.style.transform = `translate3d(${-x * d}px, ${-y * d}px, 0)`;
      });
    });
  }

  function countUp() {
    $$('[data-count]').forEach((el) => {
      if (el.hasAttribute('data-plain')) return;
      const end = +el.dataset.count;
      if (reduceMotion) { el.textContent = end; return; }
      const t0 = performance.now();
      const step = (t) => {
        const k = Math.min(1, (t - t0) / 1600);
        el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3)));
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    });
  }

  function globalFx() {
    // Brillo que sigue al cursor
    const glow = $('.cursor-glow');
    let gx = -999, gy = -999, tx = gx, ty = gy;
    addEventListener('pointermove', (e) => { tx = e.clientX; ty = e.clientY; }, { passive: true });
    const loop = () => {
      gx += (tx - gx) * 0.12; gy += (ty - gy) * 0.12;
      glow.style.transform = `translate3d(${gx}px, ${gy}px, 0)`;
      requestAnimationFrame(loop);
    };
    if (!reduceMotion) loop();

    // Foco de luz dentro de las tarjetas de categoría
    document.addEventListener('pointermove', (e) => {
      const card = e.target.closest && e.target.closest('.cat-card');
      if (!card) return;
      const r = card.getBoundingClientRect();
      card.style.setProperty('--mx', `${e.clientX - r.left}px`);
      card.style.setProperty('--my', `${e.clientY - r.top}px`);
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

    // Header que se oculta al bajar y reaparece al subir; parallax del texto gigante
    const header = $('.site-header');
    let lastY = scrollY;
    addEventListener('scroll', () => {
      const y = scrollY;
      header.classList.toggle('is-hidden', y > 200 && y > lastY && !$('.nav-item.is-open'));
      lastY = y;
      if (!reduceMotion) $$('[data-parallax]').forEach((el) => { el.style.transform = `translate3d(${y * +el.dataset.parallax}px,0,0)`; });
    }, { passive: true });
  }

  /* ---------- Arranque ---------- */
  document.body.insertAdjacentHTML('beforeend', '<div class="curtain" aria-hidden="true"></div>');
  renderNav();
  renderMobile();
  renderFooter();
  globalFx();
  addEventListener('hashchange', route);
  route();
})();
