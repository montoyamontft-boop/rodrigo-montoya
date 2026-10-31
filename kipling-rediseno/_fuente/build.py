"""Genera el sitio rediseñado de Kipling a partir de content.json.

Todos los textos, enlaces e imágenes provienen tal cual de www.kipling.edu.mx
(ver crawl.py / extract.py). Este script solo cambia la presentación.

    python3 build.py            # escribe ../index.html y ../paginas/*.html
"""
import hashlib, html, json, os, re, unicodedata
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
BASE = 'https://www.kipling.edu.mx'
D = json.load(open(os.path.join(HERE, 'content.json'), encoding='utf-8'))
# /apps/api/images/... answers with a redirect to the original file; point straight at it
_REDIR = os.path.join(HERE, 'redirecciones.json')
if os.path.exists(_REDIR):
    _txt = json.dumps(D, ensure_ascii=False)
    for _src, _dst in json.load(open(_REDIR)).items():
        _txt = _txt.replace(_src, _dst)
    D = json.loads(_txt)
CHROME, HOME, PAGES = D['chrome'], D['home'], D['pages']
esc = html.escape

# ---------------------------------------------------------------- url mapping
ALIASES = {
    BASE + '/apps/news/category/14340': BASE + '/apps/news/',
    BASE + '/apps/news/category/14340?pageIndex=1': BASE + '/apps/news/',
}


def slugify(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-') or 'pagina'


def content_key(p):
    return hashlib.md5(json.dumps([p.get('title'), p.get('blocks'), p.get('sidebar'), p.get('articles'),
                                   p.get('body')], sort_keys=True).encode()).hexdigest()


URL2SLUG, SLUG2URL, used = {}, {}, set()
by_key = {}
# shorter / prettier URLs first so they win the canonical slug
for url in sorted(PAGES, key=lambda u: (len(u), u)):
    p = PAGES[url]
    k = content_key(p)
    if k in by_key:
        URL2SLUG[url] = by_key[k]
        continue
    if p['kind'] == 'news-list':
        base = 'noticias' if 'pageIndex=2' not in url else 'noticias-2'
    else:
        parent = p['breadcrumb'][0]['text'] if len(p['breadcrumb']) > 1 else ''
        base = slugify(p['title'])
        if base in used and parent:
            base = slugify(parent) + '-' + base
    s, i = base, 2
    while s in used:
        s = f'{base}-{i}'; i += 1
    used.add(s)
    by_key[k] = s
    URL2SLUG[url] = s
    SLUG2URL[s] = url


def norm(u):
    if not u:
        return u
    u = u.replace('http://www.kipling.edu.mx', BASE).replace('https://kipling.edu.mx', BASE)
    return ALIASES.get(u, u)


SPA = False  # True while writing the single-file edition (every page lives in one HTML)


def home_href(root):
    return '#/' if SPA else root + 'index.html'


def link(u, root):
    """Map an original URL to its redesigned local page when we have it."""
    if not u:
        return u
    n = norm(u)
    if n in (BASE, BASE + '/'):
        return home_href(root)
    if n in URL2SLUG:
        return f'#/{URL2SLUG[n]}' if SPA else f'{root}paginas/{URL2SLUG[n]}.html'
    return u


YT = re.compile(r'(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{6,})')
MAP_EMBEDS = {}  # footer map link -> Google Maps embed (filled from the Ubicación page)


def viewer_attrs(u):
    """In-page viewers so videos, maps and PDFs open without leaving the site."""
    if not u:
        return ''
    m = YT.search(u)
    if m:
        return f' data-viewer="video" data-src="https://www.youtube-nocookie.com/embed/{m.group(1)}?autoplay=1&rel=0"'
    if u in MAP_EMBEDS:
        return f' data-viewer="map" data-src="{esc(MAP_EMBEDS[u])}"'
    if re.search(r'\.pdf$', u, re.I):
        return f' data-viewer="pdf" data-src="{esc(u)}"'
    return ''


def is_external(u):
    return bool(u) and u.startswith('http') and not u.startswith(BASE)


def is_image(u):
    return bool(u) and re.search(r'\.(jpe?g|png|gif|webp)$', u, re.I) is not None


def a_attrs(u, root, lightbox=None):
    href = link(u, root)
    attrs = f'href="{esc(href)}"'
    if lightbox and is_image(u):
        attrs += f' data-lightbox="{esc(lightbox)}"'
    elif href.startswith('http'):
        attrs += ' target="_blank" rel="noopener"' + viewer_attrs(href)
    return attrs


# ---------------------------------------------------------------- icons
ICONS = {
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'arrow-up-right': '<path d="M7 17 17 7M8 7h9v9"/>',
    'chev-down': '<path d="m6 9 6 6 6-6"/>',
    'chev-left': '<path d="m15 18-6-6 6-6"/>',
    'chev-right': '<path d="m9 18 6-6-6-6"/>',
    'search': '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    'close': '<path d="M18 6 6 18M6 6l12 12"/>',
    'phone': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    'pin': '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    'mail': '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    'file': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h6"/>',
    'cap': '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>',
    'card': '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20M6 15h4"/>',
    'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    'calendar': '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    'expand': '<path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/>',
    'lock': '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    'play': '<path d="m7 4 13 8-13 8z"/>',
    'pause': '<path d="M7 4h3v16H7zM14 4h3v16h-3z"/>',
    'up': '<path d="m6 15 6-6 6 6"/>',
}


def icon(name, cls='i'):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


# ---------------------------------------------------------------- chrome
LOGIN_URLS = set(D['login'])


def nav_html(root):
    out = []
    for i, item in enumerate(CHROME['nav']):
        text = esc(item['text'])
        if item['sub']:
            subs = ''.join(
                f'<li><a {a_attrs(s["href"], root)}><span>{esc(s["text"])}</span>{icon("arrow", "i i-sm")}</a></li>'
                for s in item['sub'])
            out.append(
                f'<li class="nav-item has-sub" data-nav>'
                f'<button class="nav-link" aria-expanded="false" aria-controls="sub-{i}">{text}{icon("chev-down", "i i-xs")}</button>'
                f'<div class="sub" id="sub-{i}"><div class="sub-inner"><p class="sub-title">{text}</p><ul>{subs}</ul></div></div></li>')
        elif item['text'].upper() == 'HACER UNA CITA':
            out.append(f'<li class="nav-item nav-cta"><a class="btn btn-cta" {a_attrs(item["href"], root)}>'
                       f'{icon("calendar", "i i-sm")}<span>{text}</span></a></li>')
        else:
            out.append(f'<li class="nav-item"><a class="nav-link" {a_attrs(item["href"], root)}>{text}</a></li>')
    return '<ul class="nav-menu">' + ''.join(out) + '</ul>'


def mobile_nav_html(root):
    out = []
    for i, item in enumerate(CHROME['nav']):
        text = esc(item['text'])
        if item['sub']:
            subs = ''.join(f'<li><a {a_attrs(s["href"], root)}>{esc(s["text"])}</a></li>' for s in item['sub'])
            out.append(f'<li class="m-item"><button class="m-link" aria-expanded="false">'
                       f'<span>{text}</span>{icon("chev-down", "i i-sm")}</button><div class="m-sub"><ul class="m-sub-inner">{subs}</ul></div></li>')
        elif item['text'].upper() == 'HACER UNA CITA':
            continue
        else:
            out.append(f'<li class="m-item"><a class="m-link" {a_attrs(item["href"], root)}><span>{text}</span>'
                       f'{icon("arrow", "i i-sm")}</a></li>')
    cita = next(n for n in CHROME['nav'] if n['text'].upper() == 'HACER UNA CITA')
    return (f'<ul class="m-menu">{"".join(out)}</ul>'
            f'<a class="btn btn-cta btn-block" {a_attrs(cita["href"], root)}>{icon("calendar", "i i-sm")}'
            f'<span>{esc(cita["text"])}</span></a>')


def header_html(root, solid=False):
    return f'''
<a class="skip" href="#contenido">Skip to main content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="site-header{' is-solid' if solid else ''}" data-header>
  <div class="header-inner">
    <a class="brand" href="{home_href(root)}" aria-label="{esc(CHROME['footer']['name'])}">
      <img class="brand-light" src="{root}assets/img/footer_logo.png" alt="{esc(CHROME['footer']['name'])}" width="2024" height="333">
      <img class="brand-color" src="{root}assets/img/header_logo.png" alt="" width="2024" height="388">
    </a>
    <nav class="site-nav" aria-label="Main Menu">{nav_html(root)}</nav>
    <div class="header-tools">
      <button class="icon-btn" data-search-open aria-label="Search">{icon('search')}</button>
      <button class="icon-btn burger" data-menu-open aria-label="Main Menu Toggle" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="drawer" data-drawer aria-hidden="true">
  <div class="drawer-panel" role="dialog" aria-modal="true" aria-label="Main Menu">
    <div class="drawer-head">
      <img src="{root}assets/img/header_logo.png" alt="{esc(CHROME['footer']['name'])}" width="2024" height="388">
      <button class="icon-btn" data-menu-close aria-label="Close">{icon('close')}</button>
    </div>
    <nav aria-label="Main Menu">{mobile_nav_html(root)}</nav>
  </div>
</div>
<div class="search" data-search aria-hidden="true">
  <button class="icon-btn search-close" data-search-close aria-label="Close">{icon('close')}</button>
  <div class="search-box">
    <form class="search-form" action="{BASE}/apps/search/" method="get" role="search" data-search-form>
      <label class="sr-only" for="site_search">Search</label>
      <input type="search" id="site_search" name="q" placeholder="Search this site" title="Search" autocomplete="off">
      <button type="submit" class="search-go" aria-label="Search">{icon('search')}</button>
    </form>
    <ol class="search-results" data-search-results aria-live="polite"></ol>
  </div>
</div>'''


def footer_html(root):
    f = CHROME['footer']
    cols = []
    for ad in f['addresses']:
        items = []
        for it in ad['items']:
            ic = {'map': 'pin', 'tel': 'phone', 'link': 'file'}[it['kind']]
            lines = '<br>'.join(esc(l) for l in it['lines'])
            items.append(f'<li><a {a_attrs(it["href"], root)}>{icon(ic, "i i-sm")}<span>{lines}</span></a></li>')
        imgs = ''.join(f'<a class="foot-banner" {a_attrs(im["href"], root)}><img src="{root}assets/img/{os.path.basename(im["src"])}" '
                       f'alt="" width="1333" height="250" loading="lazy"></a>' for im in ad['images'])
        cols.append(f'<div class="foot-col"><h3 class="foot-title">{esc(ad["title"])}</h3><ul class="foot-list">{"".join(items)}</ul>'
                    f'{f"<div class=foot-banners>{imgs}</div>" if imgs else ""}</div>')
    legal = '<br>'.join(esc(l) for l in f['legal'])
    mails = '<span class="sep">/</span>'.join(
        f'<a href="mailto:{esc(m)}">{icon("mail", "i i-sm")}<span>{esc(m)}</span></a>' for m in f['emails'])
    return f'''
<footer class="site-footer" id="footer">
  <div class="foot-bands" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="container foot-grid">
    <div class="foot-brand">
      <a href="{home_href(root)}"><img src="{root}assets/img/footer_logo.png" alt="{esc(f['name'])}" width="2024" height="333" loading="lazy"></a>
      <p class="foot-name">{esc(f['name'])}</p>
      <div class="foot-mails">{mails}</div>
    </div>
    {''.join(cols)}
    <div class="foot-col foot-legal">
      <p>{legal}</p>
      <p><a {a_attrs(f['legal_privacy']['href'], root)}>{icon('file', 'i i-sm')}<span>{esc(f['legal_privacy']['text'])}</span></a></p>
      <img class="ib-logo" src="{root}assets/img/ib-logo.png" alt="" width="494" height="485" loading="lazy">
    </div>
  </div>
  <div class="container foot-bottom">
    <a {a_attrs(f['bottom_link']['href'], root)}>{icon('pin', 'i i-sm')}<span>{esc(f['bottom_link']['text'])}</span></a>
    <button class="to-top" data-to-top aria-label="Top">{icon('up')}</button>
  </div>
</footer>'''


def mobile_cta(root):
    cita = next(n for n in CHROME['nav'] if n['text'].upper() == 'HACER UNA CITA')
    return (f'<a class="m-cta" {a_attrs(cita["href"], root)}>{icon("calendar", "i i-sm")}<span>{esc(cita["text"])}</span></a>')


VIEWER = f'''
<div class="viewer" data-viewer-box aria-hidden="true" role="dialog" aria-modal="true">
  <div class="viewer-card">
    <div class="viewer-bar">
      <a class="viewer-out" data-viewer-out href="#" target="_blank" rel="noopener">{icon('arrow-up-right', 'i i-sm')}</a>
      <button class="icon-btn" data-viewer-close aria-label="Close">{icon('close')}</button>
    </div>
    <div class="viewer-frame"></div>
  </div>
</div>'''

LIGHTBOX = f'''
<div class="lightbox" data-lb aria-hidden="true" role="dialog" aria-modal="true">
  <button class="icon-btn lb-close" data-lb-close aria-label="Close">{icon('close')}</button>
  <button class="icon-btn lb-prev" data-lb-prev aria-label="Previous">{icon('chev-left')}</button>
  <figure class="lb-stage"><img alt=""><figcaption></figcaption></figure>
  <button class="icon-btn lb-next" data-lb-next aria-label="Next">{icon('chev-right')}</button>
  <div class="lb-count"></div>
</div>'''


def page_shell(title, body, root, desc=None, solid=False, body_cls='', extra='', body_attrs=''):
    desc = desc or D['meta_description']
    return f'''<!DOCTYPE html>
<html lang="es" class="no-js">
<head>
<meta charset="utf-8">
<script>document.documentElement.classList.remove('no-js')</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#B40029">
<link rel="apple-touch-icon" sizes="180x180" href="{root}assets/img/apple-touch-icon.png">
<link rel="icon" type="image/png" href="{root}assets/img/favicon-32x32.png" sizes="32x32">
<link rel="icon" href="{root}assets/img/favicon.ico" type="image/x-icon">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://3.files.edl.io" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/kipling.css">
</head>
<body class="{body_cls}"{body_attrs}>
{header_html(root, solid)}
<main id="contenido">
{body}
</main>
{footer_html(root)}
{mobile_cta(root)}
{LIGHTBOX}
{VIEWER}
{extra}
<script src="{root}assets/js/kipling.js" defer></script>
</body>
</html>
'''


# ---------------------------------------------------------------- content helpers
def rich(html_in, root, gallery='content'):
    """Rewrite links of an extracted HTML fragment (text kept verbatim)."""
    s = BeautifulSoup(html_in, 'lxml')
    body = s.body or s
    for a in body.find_all('a', href=True):
        h = a['href']
        if a.find('img') and is_image(h):
            a['data-lightbox'] = gallery
            continue
        new = link(h, root)
        a['href'] = new
        if new.startswith('http'):
            a['target'] = '_blank'; a['rel'] = 'noopener'
            v = BeautifulSoup(f'<a{viewer_attrs(new)}></a>', 'lxml').a
            for k, val in v.attrs.items():
                a[k] = val
        elif 'target' in a.attrs:
            del a['target']
    # short lines made only of bold text act as section headings on the original site
    for el in body.find_all(['div', 'p']):
        kids = [c for c in el.contents if str(c).strip()]
        if len(kids) == 1 and getattr(kids[0], 'name', None) in ('strong', 'b') and not kids[0].find(['img', 'iframe']):
            if len(el.get_text(strip=True)) < 70:
                el['class'] = 'kicker'
    for im in body.find_all('img'):
        im['loading'] = 'lazy'; im['decoding'] = 'async'
        if not im.find_parent('a'):
            im['data-zoom'] = gallery
    for fr in body.find_all('iframe'):
        src = fr.get('src', '')
        w, h = fr.get('width'), fr.get('height')
        wrap = s.new_tag('div')
        if 'tfaforms.net' in src:
            fr['id'] = 'formassembly_form'
            fr['height'] = '1200'
            fr['title'] = 'Formulario de solicitud'
            wrap['class'] = 'embed embed-form'
        elif src.endswith('.pdf'):
            wrap['class'] = 'embed embed-pdf'
        else:
            wrap['class'] = 'embed embed-media'
            try:
                wrap['style'] = f'--ratio:{int(w)}/{int(h)}'
            except (TypeError, ValueError):
                pass
        if 'maps' in src:
            fr['title'] = fr.get('title') or 'Google Maps'
        elif 'vimeo' in src:
            fr['title'] = fr.get('title') or 'Vimeo'
            fr['allow'] = 'autoplay; fullscreen; picture-in-picture'
        fr['loading'] = 'lazy'
        for k in ('width',):
            if k in fr.attrs:
                del fr[k]
        fr.wrap(wrap)
    out = body.decode_contents()
    return out


def srcset(item):
    vs = item.get('versions')
    if not vs:
        return ''
    return ', '.join(f'{v["url"]} {v["w"]}w' for v in vs)


def photos_html(block, gid, hero=False):
    items = block['items']
    if not items:
        return ''
    maxw = max((i.get('w') or 2000) for i in items)
    # tiny images (logos / badges): a clean wall instead of a cinematic slider
    if block.get('mode') == 'rotate' and maxw < 800:
        cells = ''.join(f'<a class="logo-cell" href="{esc(i["src"])}" data-lightbox="{gid}">'
                        f'<img src="{esc(i["src"])}" alt="{esc(i["alt"])}" loading="lazy" decoding="async"'
                        f' width="{i.get("w") or ""}" height="{i.get("h") or ""}"></a>' for i in items)
        return f'<div class="logo-wall reveal">{cells}</div>'
    if block.get('mode') == 'rotate' and len(items) > 1:
        slides = []
        for n, i in enumerate(items):
            w, h = i.get('w') or 1600, i.get('h') or 1000
            ss = srcset(i)
            ss_attr = f' srcset="{ss}" sizes="(min-width: 1100px) 1100px, 100vw"' if ss else ''
            lazy = '' if (n == 0 and hero) else ' loading="lazy"'
            cap = f'<figcaption>{esc(i["caption"])}</figcaption>' if i['caption'] else ''
            label = esc(i['alt'] or i['caption'] or 'Imagen')
            slides.append(
                f'<figure class="slide{" is-active" if n == 0 else ""}" data-slide>'
                f'<div class="slide-blur" style="background-image:url(\'{esc(i["display"])}\')"></div>'
                f'<a href="{esc(i["src"])}" data-lightbox="{gid}" class="slide-link" aria-label="{label}">'
                f'<img src="{esc(i["display"])}"{ss_attr} alt="{esc(i["alt"])}" width="{w}" height="{h}"{lazy} decoding="async"></a>'
                f'{cap}</figure>')
        dots = ''.join(f'<button class="dot{" is-active" if n == 0 else ""}" data-dot="{n}" aria-label="{n + 1}"></button>'
                       for n in range(len(items)))
        return (f'<div class="slider reveal{" slider-hero" if hero else ""}" data-slider>'
                f'<div class="slides">{"".join(slides)}</div>'
                f'<div class="slider-ui"><button class="icon-btn" data-prev aria-label="Previous">{icon("chev-left")}</button>'
                f'<div class="dots">{dots}</div><span class="slider-count"><b>01</b> / {len(items):02d}</span>'
                f'<button class="icon-btn" data-next aria-label="Next">{icon("chev-right")}</button></div>'
                f'<div class="slider-bar"><span></span></div></div>')
    # stack / single photo: show complete image, never cropped
    figs = []
    for i in items:
        ss = srcset(i)
        ss_attr = f' srcset="{ss}" sizes="(min-width: 1100px) 900px, 100vw"' if ss else ''
        dims = f' width="{i["w"]}" height="{i["h"]}"' if i.get('w') else ''
        cap = f'<figcaption>{esc(i["caption"])}</figcaption>' if i['caption'] else ''
        figs.append(f'<figure class="photo"><a href="{esc(i["src"])}" data-lightbox="{gid}">'
                    f'<img src="{esc(i["display"])}"{ss_attr} alt="{esc(i["alt"])}" loading="lazy" decoding="async"{dims}>'
                    f'<span class="zoom">{icon("expand", "i i-sm")}</span></a>{cap}</figure>')
    cls = 'photos-grid' if len(items) > 1 else 'photos-single'
    return f'<div class="{cls} reveal">{"".join(figs)}</div>'


def files_html(block, root):
    cards = []
    embeds = []
    for f in block['items']:
        cards.append(f'<a class="doc" href="{esc(f["href"])}" target="_blank" rel="noopener"{viewer_attrs(f["href"])}>'
                     f'<span class="doc-ic">{icon("file")}<b>PDF</b></span><span class="doc-t">{esc(f["text"])}</span>'
                     f'{icon("arrow-up-right", "i i-sm doc-go")}</a>')
        if f.get('embed'):
            embeds.append(f'<div class="embed embed-pdf reveal"><iframe src="{esc(f["href"])}" title="{esc(f["text"])}" loading="lazy"></iframe></div>')
    title = f'<h3 class="docs-title">{esc(block["title"])}</h3>' if block.get('title') else ''
    return f'<div class="docs reveal">{title}<div class="doc-list">{"".join(cards)}</div></div>{"".join(embeds)}'


def side_nav_html(block, root):
    items = []
    for it in block['items']:
        cur = ' is-current' if it['current'] else ''
        sub = ''
        if it['sub']:
            sub = '<ul>' + ''.join(f'<li><a class="{"is-current" if s["current"] else ""}" {a_attrs(s["href"], root)}>{esc(s["text"])}</a></li>'
                                   for s in it['sub']) + '</ul>'
        items.append(f'<li><a class="{cur.strip()}" {a_attrs(it["href"], root)}>'
                     f'<span>{esc(it["text"])}</span>{icon("arrow", "i i-sm")}</a>{sub}</li>')
    return f'<nav class="side-nav" aria-label="Page Navigation"><ul>{"".join(items)}</ul></nav>'


def cta_card(root):
    m = HOME['modal']
    return (f'<div class="cta-card">'
            f'<div class="cta-bands" aria-hidden="true"><i></i><i></i><i></i></div>'
            f'<p class="eyebrow eyebrow-light">{esc(m["title"])}</p>'
            f'<div class="cta-text">{m["summary"]}</div>'
            f'<a class="btn btn-light" {a_attrs(m["cta"]["href"], root)}><span>{esc(m["cta"]["text"])}</span>{icon("arrow", "i i-sm")}</a></div>')


def banner_html(p, root, hero_block=None):
    crumbs = []
    bc = p.get('breadcrumb') or []
    crumbs.append(f'<a href="{home_href(root)}">{esc(CHROME["footer"]["name"])}</a>')
    for c in bc[:-1]:
        crumbs.append(f'<a {a_attrs(c["href"], root)}>{esc(c["text"])}</a>')
    if bc:
        crumbs.append(f'<span aria-current="page">{esc(bc[-1]["text"])}</span>')
    eyebrow = bc[0]['text'] if len(bc) > 1 else CHROME['footer']['name']
    bg = ''
    if hero_block:
        first = hero_block['items'][0]
        bg = f'<div class="banner-photo" style="background-image:url(\'{esc(first["display"])}\')"></div>'
    return f'''
<section class="banner{' banner-has-photo' if bg else ''}">
  {bg}
  <div class="banner-bands" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="container banner-inner">
    <nav class="crumbs" aria-label="Breadcrumb">{'<span class="sep">/</span>'.join(crumbs)}</nav>
    <p class="eyebrow eyebrow-light reveal">{esc(eyebrow)}</p>
    <h1 class="banner-title reveal" data-split>{esc(p['title'])}</h1>
  </div>
</section>'''


# ---------------------------------------------------------------- page kinds
def render_page(url, p, root='../'):
    blocks = p['blocks']
    sidebar = p['sidebar']
    hero_block = None
    if p['layout'] in ('full-hero', 'right-hero'):
        hero_block = next((b for b in blocks if b['type'] == 'photos' and b['items']), None)
    parts = []
    gid = 0
    for b in blocks:
        gid += 1
        if b['type'] == 'text':
            parts.append(f'<div class="prose reveal">{rich(b["html"], root, f"g{gid}")}</div>')
        elif b['type'] == 'photos':
            parts.append(photos_html(b, f'g{gid}', hero=b is hero_block))
        elif b['type'] == 'files':
            parts.append(files_html(b, root))
        elif b['type'] == 'nav':
            parts.append(side_nav_html(b, root))
    side_nav = ''.join(side_nav_html(b, root) for b in sidebar if b['type'] == 'nav')
    side_files = ''.join(files_html(b, root) for b in sidebar if b['type'] == 'files')
    side_photos = ''
    for b in sidebar:
        if b['type'] == 'photos' and b['items']:
            gid += 1
            side_photos += photos_html(b, f'g{gid}')
    has_side = bool(side_nav or side_files)
    body_main = ''.join(parts)
    if has_side:
        layout = f'''
<div class="container page-grid">
  <article class="page-main">{body_main}{side_photos}</article>
  <aside class="page-side">
    <div class="side-sticky">
      {f'<div class="side-card reveal"><p class="side-label">{esc(p["breadcrumb"][0]["text"]) if p["breadcrumb"] else ""}</p>{side_nav}</div>' if side_nav else ''}
      {side_files}
      {cta_card(root)}
    </div>
  </aside>
</div>'''
    else:
        wide = ' page-wide' if p['layout'] in ('full-width',) or any('tfaforms' in (b.get('html') or '') for b in blocks) else ''
        layout = f'<div class="container page-single{wide}"><article class="page-main">{body_main}{side_photos}</article></div>'
        if not any('tfaforms' in (b.get('html') or '') for b in blocks):
            layout += f'<div class="container page-cta">{cta_card(root)}</div>'
    needs_form = any('tfaforms' in (b.get('html') or '') for b in blocks)
    body = banner_html(p, root, hero_block) + f'<section class="page-body">{layout}</section>'
    if needs_form:
        body += '' if SPA else '<script src="https://nordangliaeducation.tfaforms.net/js/iframe_resize_helper.js" defer></script>'
    return body


def news_card(a, root, gid='news', big=False):
    img = a.get('img')
    summary = f'<div class="news-sum">{rich(a["summary"], root)}</div>' if a.get('summary') else ''
    href = a.get('href')
    attrs = a_attrs(href, root, lightbox=gid) if href else ''
    if not img:
        return (f'<article class="news-card news-feature reveal"><a {attrs}>'
                f'<div class="cta-bands" aria-hidden="true"><i></i><i></i><i></i></div>'
                f'{"<span class=badge>ALERTA</span>" if a.get("alert") else ""}'
                f'<h3 class="news-title">{esc(a["title"])}</h3>{summary}'
                f'<span class="news-go">{icon("arrow", "i")}</span></a></article>')
    return (f'<article class="news-card reveal"><a {attrs}>'
            f'<div class="news-img"><img src="{esc(img)}" alt="{esc(a["title"])}" loading="lazy" decoding="async"></div>'
            f'<div class="news-body"><h3 class="news-title">{esc(a["title"])}</h3>{summary}'
            f'<span class="news-go">{icon("arrow-up-right" if is_image(href) else "arrow", "i")}</span></div></a></article>')


def render_news(url, p, root='../'):
    cards = ''.join(news_card(a, root) for a in p['articles'])
    pag = ''
    if p['pagination']:
        cur = '2' if 'pageIndex=2' in url else '1'
        links = []
        nums = sorted({x['text'] for x in p['pagination'] if x['text'].isdigit()} | {cur})
        for x in p['pagination']:
            if not x['text'].isdigit():
                links.append((x['text'], x['href']))
        btns = []
        for t, h in links:
            if t in ('Atrás',):
                btns.append(f'<a class="pg" {a_attrs(h, root)}>{icon("chev-left", "i i-sm")}<span>{esc(t)}</span></a>')
        for n in nums:
            if n == cur:
                btns.append(f'<span class="pg is-current">{n}</span>')
            else:
                h = next(x['href'] for x in p['pagination'] if x['text'] == n)
                btns.append(f'<a class="pg" {a_attrs(h, root)}>{n}</a>')
        for t, h in links:
            if t not in ('Atrás',):
                btns.append(f'<a class="pg" {a_attrs(h, root)}><span>{esc(t)}</span>{icon("chev-right", "i i-sm")}</a>')
        pag = f'<nav class="pagination" aria-label="Pagination">{"".join(btns)}</nav>'
    return (banner_html(p, root) +
            f'<section class="page-body"><div class="container"><div class="news-grid news-grid-list">{cards}</div>{pag}</div></section>')


def render_article(url, p, root='../'):
    imgs = ''
    if p['images']:
        imgs = '<div class="photos-single reveal">' + ''.join(
            f'<figure class="photo"><a href="{esc(i["src"])}" data-lightbox="art"><img src="{esc(i["src"])}" alt="{esc(i["alt"])}" loading="lazy">'
            f'<span class="zoom">{icon("expand", "i i-sm")}</span></a></figure>' for i in p['images']) + '</div>'
    body = f'''
<div class="container page-single">
  <article class="page-main">
    {f'<div class="lead reveal">{rich(p["summary"], root)}</div>' if p['summary'] else ''}
    {imgs}
    <div class="prose reveal">{rich(p['body'], root, 'art')}</div>
  </article>
</div>
<div class="container page-cta">{cta_card(root)}</div>'''
    return banner_html(p, root) + f'<section class="page-body">{body}</section>'


# ---------------------------------------------------------------- home
QL_ICONS = ['cap', 'card', 'users']


def render_home(root=''):
    sp1, sp2 = HOME['spotlights'][0], HOME['spotlights'][1]
    m = HOME['modal']
    hist = CHROME['nav'][0]
    q_html = ''.join(
        f'<a class="ql reveal" {a_attrs(q["href"], root)} style="--d:{n * 90}ms">'
        f'<span class="ql-ic">{icon(QL_ICONS[n % 3])}</span><span class="ql-t">{esc(q["text"])}</span>'
        f'{icon("lock", "i i-xs ql-lock") if norm(q["href"]) in LOGIN_URLS else ""}'
        f'<span class="ql-go">{icon("arrow", "i i-sm")}</span></a>'
        for n, q in enumerate(HOME['quicklinks']))
    # news: reuse the listing data so each card carries its original summary
    listing = {a['title']: a for a in PAGES[BASE + '/apps/news/']['articles']}
    news = []
    for n in HOME['news']['items']:
        a = dict(listing.get(n['title'], {}))
        a.update({'title': n['title'], 'href': n['href'], 'img': n['img']})
        if a.get('img') is None:
            a['alert'] = True
        news.append(news_card(a, root, gid='home-news'))
    sections = ''.join(
        f'<a class="panel" {a_attrs(s["href"], root)} style="--i:{n}">'
        f'<span class="panel-img" style="background-image:url(\'{esc(s["img"])}\')"></span>'
        f'<span class="panel-shade"></span>'
        f'<span class="panel-num">{n + 1:02d}</span>'
        f'<span class="panel-title">{esc(s["title"])}</span>'
        f'<span class="panel-go">{icon("arrow-up-right", "i")}</span></a>'
        for n, s in enumerate(HOME['sections']))
    g = HOME['gallery']
    def row(imgs, rev=False):
        tiles = ''.join(f'<a class="tile" href="{esc(u)}" data-lightbox="galeria" aria-label="Gallery {i + 1}">'
                        f'<img src="{esc(u)}" alt="" loading="lazy" decoding="async"></a>' for i, u in imgs)
        return f'<div class="marquee{" marquee-rev" if rev else ""}"><div class="marquee-track">{tiles}{tiles.replace("data-lightbox", "aria-hidden=true tabindex=-1 data-lightbox-dup")}</div></div>'
    half = (len(g) + 1) // 2
    gal = row(list(enumerate(g))[:half]) + row(list(enumerate(g))[half:], rev=True)
    sec_label = next(n['text'] for n in CHROME['nav'] if n['text'] == 'Secciones')
    sp1_text = ' '.join(sp1['lines'])
    sp2_body, sp2_sig = sp2['lines'][0], sp2['lines'][1:]
    body = f'''
<section class="hero" data-hero>
  <div class="hero-media"><img src="{esc(sp1['img'])}" alt="{esc(sp1['alt'])}" fetchpriority="high"></div>
  <div class="hero-shade"></div>
  <div class="hero-bands" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="container hero-inner">
    <p class="eyebrow eyebrow-light hero-in" style="--d:.1s">Kipling School <span class="dotsep"></span> A Nord Anglia Education School</p>
    <h1 class="hero-title" data-split>{esc(sp1['title'])}</h1>
    <p class="hero-text hero-in" style="--d:.9s">{esc(sp1_text)}</p>
    <div class="hero-actions hero-in" style="--d:1.1s">
      <a class="btn btn-cta btn-lg" {a_attrs(m['cta']['href'], root)}><span>{esc(m['cta']['text'])}</span>{icon('arrow', 'i i-sm')}</a>
      <a class="btn btn-ghost btn-lg" {a_attrs(hist['sub'][0]['href'], root)}><span>{esc(hist['text'])}</span></a>
    </div>
  </div>
  <a class="scroll-cue" href="#accesos" aria-label="Scroll"><span></span></a>
</section>

<section class="quicklinks" id="accesos" aria-label="Quicklinks">
  <div class="container ql-grid">{q_html}</div>
</section>

<section class="section news-home">
  <div class="container">
    <div class="sec-head">
      <div>
        <p class="eyebrow reveal">{esc(CHROME['footer']['name'])}</p>
        <h2 class="sec-title reveal" data-split><a {a_attrs(HOME['news']['href'], root)}>{esc(HOME['news']['title'])}</a></h2>
      </div>
      <a class="link-more reveal" {a_attrs(HOME['news']['more']['href'], root)}><span>{esc(HOME['news']['more']['text'])}</span>{icon('arrow', 'i i-sm')}</a>
    </div>
    <div class="news-grid news-grid-home">{''.join(news)}</div>
  </div>
</section>

<section class="section welcome">
  <div class="container welcome-grid">
    <div class="welcome-media reveal">
      <div class="welcome-frame"><img src="{esc(sp2['img'])}" alt="{esc(sp2['alt'])}" loading="lazy" decoding="async"></div>
      <div class="welcome-deco" aria-hidden="true"></div>
    </div>
    <div class="welcome-copy">
      <h2 class="sec-title reveal" data-split>{esc(sp2['title'])}</h2>
      <blockquote class="welcome-quote reveal"><p>{esc(sp2_body)}</p></blockquote>
      <div class="signature reveal">
        <p class="sig-name">{esc(sp2_sig[0])}</p>
        <p class="sig-role">{esc(sp2_sig[1])}</p>
        <p class="sig-campus">{esc(sp2_sig[2])}</p>
      </div>
    </div>
  </div>
</section>

<section class="section sections-band">
  <div class="sections-bg" aria-hidden="true"><i></i><i></i><i></i></div>
  <div class="container">
    <div class="sec-head sec-head-light">
      <div>
        <p class="eyebrow eyebrow-light reveal">Kipling School</p>
        <h2 class="sec-title reveal" data-split>{esc(sec_label)}</h2>
      </div>
    </div>
    <div class="panels" data-panels>{sections}</div>
  </div>
</section>

<section class="gallery" aria-label="Gallery">{gal}</section>

<section class="section cta-band">
  <div class="container cta-band-inner reveal">
    <div>
      <p class="eyebrow">{esc(m['title'])}</p>
      <div class="cta-band-text">{m['summary']}</div>
    </div>
    <div class="cta-band-actions">
      <a class="btn btn-cta btn-lg" {a_attrs(m['cta']['href'], root)}><span>{esc(m['cta']['text'])}</span>{icon('arrow', 'i i-sm')}</a>
      <img class="cta-ib" src="{root}assets/img/ib-logo.png" alt="" width="494" height="485" loading="lazy">
    </div>
  </div>
</section>

<div class="modal" data-modal aria-hidden="true" role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <div class="modal-card">
    <div class="cta-bands" aria-hidden="true"><i></i><i></i><i></i></div>
    <button class="icon-btn modal-close" data-modal-close aria-label="Close">{icon('close')}</button>
    <img class="modal-logo" src="{root}assets/img/header_logo.png" alt="" width="2024" height="388">
    <h2 class="modal-title" id="modal-title">{esc(m['title'])}</h2>
    <div class="modal-text">{m['summary']}</div>
    <a class="btn btn-cta btn-lg" {a_attrs(m['cta']['href'], root)}><span>{esc(m['cta']['text'])}</span>{icon('arrow', 'i i-sm')}</a>
    <button class="modal-dismiss" data-modal-never>{esc(m['dismiss'])}</button>
  </div>
</div>'''
    return body


# ---------------------------------------------------------------- maps, search index, single-file edition
def load_map_embeds():
    ub = next((p for u, p in PAGES.items() if URL2SLUG.get(u, '').startswith('ubicacion')), None)
    if not ub:
        return
    srcs = re.findall(r'<iframe[^>]+src="([^"]+maps/embed[^"]+)"', ' '.join(b.get('html', '') for b in ub['blocks']))
    links = [it['href'] for ad in CHROME['footer']['addresses'] for it in ad['items'] if it['kind'] == 'map']
    for href, src in zip(links, srcs):
        MAP_EMBEDS[href] = html.unescape(src)


def page_bodies(root):
    yield '', D['chrome']['footer']['name'], 'is-home', render_home(root)
    for slug, url in SLUG2URL.items():
        p = PAGES[url]
        if p['kind'] == 'news-list':
            body = render_news(url, p, root)
        elif p['kind'] == 'article':
            body = render_article(url, p, root)
        else:
            body = render_page(url, p, root)
        yield slug, p['doc_title'], 'is-inner', body


def search_entry(slug, title, body, href):
    s = BeautifulSoup(body, 'lxml')
    for t in s.select('.cta-card, .modal, .crumbs, script'):
        t.decompose()
    h1 = s.find(['h1'])
    text = re.sub(r'\s+', ' ', s.get_text(' ')).strip()
    return {'t': h1.get_text(' ', strip=True) if h1 else title, 'u': href, 'x': text[:5000]}


def inline_assets(doc):
    import base64, mimetypes
    css = open(os.path.join(OUT, 'assets/css/kipling.css'), encoding='utf-8').read()
    js = open(os.path.join(OUT, 'assets/js/kipling.js'), encoding='utf-8').read()
    doc = doc.replace('<link rel="stylesheet" href="assets/css/kipling.css">', '<style>\n' + css + '\n</style>')
    doc = doc.replace('<script src="assets/js/kipling.js" defer></script>', '<script>\n' + js.replace('</script', '<\\/script') + '\n</script>')
    cache = {}

    def data(m):
        path = m.group(2)
        if path not in cache:
            mt = mimetypes.guess_type(path)[0] or 'image/x-icon'
            cache[path] = f'data:{mt};base64,' + base64.b64encode(open(os.path.join(OUT, path), 'rb').read()).decode()
        return f'{m.group(1)}="{cache[path]}"'
    doc = re.sub(r'(src|href)="(assets/img/[^"]+)"', data, doc)
    left = re.findall(r'(?:src|href)="(assets/[^"]+)"', doc)
    assert not left, left[:5]
    return doc


def build_single_file():
    global SPA
    SPA = True
    try:
        pages = list(page_bodies(''))
        index = [search_entry(slug, title, body, '#/' + slug) for slug, title, _, body in pages]
        tpls = ''.join(f'<template data-page="{slug}" data-title="{esc(title)}" data-cls="{cls}">{body}</template>'
                       for slug, title, cls, body in pages)
        extra = tpls + '<script>window.KIPLING_INDEX=' + json.dumps(index, ensure_ascii=False).replace('</', '<\\/') + ';</script>'
        home = pages[0]
        doc = page_shell(home[1], home[3], '', body_cls='is-home', extra=extra, body_attrs=' data-spa')
    finally:
        SPA = False
    doc = inline_assets(doc)
    stray = re.findall(r'href="((?:\.\./)?(?:paginas/[^"]+|index\.html))"', doc)
    assert not stray, stray[:5]
    open(os.path.join(OUT, 'kipling-completo.html'), 'w', encoding='utf-8').write(doc)
    return len(pages)


# ---------------------------------------------------------------- write
def main():
    load_map_embeds()
    os.makedirs(os.path.join(OUT, 'paginas'), exist_ok=True)
    for f in os.listdir(os.path.join(OUT, 'paginas')):
        if f.endswith('.html'):
            os.remove(os.path.join(OUT, 'paginas', f))
    home = page_shell(D['chrome']['footer']['name'], render_home(''), '', body_cls='is-home', body_attrs=' data-root=""')
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(home)
    n = 0
    for slug, url in SLUG2URL.items():
        p = PAGES[url]
        if p['kind'] == 'news-list':
            body = render_news(url, p)
        elif p['kind'] == 'article':
            body = render_article(url, p)
        else:
            body = render_page(url, p)
        open(os.path.join(OUT, 'paginas', slug + '.html'), 'w', encoding='utf-8').write(
            page_shell(p['doc_title'], body, '../', body_cls='is-inner', body_attrs=' data-root="../"'))
        n += 1
    json.dump({u: s for u, s in URL2SLUG.items()}, open(os.path.join(HERE, 'mapa-urls.json'), 'w'),
              indent=1, ensure_ascii=False)
    index = [search_entry(slug, title, body, 'index.html' if not slug else f'paginas/{slug}.html')
             for slug, title, _, body in page_bodies('')]
    open(os.path.join(OUT, 'assets/js/indice.js'), 'w', encoding='utf-8').write(
        '/* Índice de búsqueda generado por build.py */\nwindow.KIPLING_INDEX=' + json.dumps(index, ensure_ascii=False) + ';\n')
    print('index.html +', n, 'páginas; kipling-completo.html con', build_single_file(), 'páginas')


if __name__ == '__main__':
    main()
