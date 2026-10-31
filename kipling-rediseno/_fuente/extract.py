"""Extract every crawled kipling.edu.mx page into a structured content.json.

Texts are kept verbatim; only presentation attributes (style/class/ids) are dropped.
"""
import json, os, re, sys
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup, NavigableString, Comment

PAGES = sys.argv[1]
OUT = sys.argv[2]
BASE = sys.argv[3] if len(sys.argv) > 3 else 'https://www.kipling.edu.mx/'
index = json.load(open(os.path.join(PAGES, 'index.json')))

KEEP = {'p', 'div', 'span', 'strong', 'b', 'em', 'i', 'u', 'a', 'ul', 'ol', 'li', 'br', 'img',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table', 'thead', 'tbody', 'tr', 'td', 'th', 'iframe',
        'blockquote', 'sup', 'sub', 'hr', 'figure', 'figcaption'}
ATTRS = {'a': ['href', 'target'], 'img': ['src', 'alt', 'width', 'height'],
         'iframe': ['src', 'title', 'width', 'height', 'allow', 'allowfullscreen'],
         'td': ['colspan', 'rowspan'], 'th': ['colspan', 'rowspan']}


def cf_decode(hexstr):
    k = int(hexstr[:2], 16)
    return ''.join(chr(int(hexstr[i:i + 2], 16) ^ k) for i in range(2, len(hexstr), 2))


def fix_emails(root):
    for a in root.select('a[href*="/cdn-cgi/l/email-protection"]'):
        h = a.get('href', '')
        m = re.search(r'#([0-9a-f]+)$', h)
        sp = a.find(class_='__cf_email__')
        code = m.group(1) if m else (sp.get('data-cfemail') if sp else None)
        if code:
            mail = cf_decode(code)
            a['href'] = 'mailto:' + mail
            a.clear(); a.append(mail)
    for sp in root.select('.__cf_email__'):
        if sp.get('data-cfemail'):
            sp.replace_with(cf_decode(sp['data-cfemail']))


def abs_url(u, page):
    if not u:
        return u
    if u.startswith(('mailto:', 'tel:', 'javascript:', '#')):
        return u
    if u.startswith('//'):
        return 'https:' + u
    return urljoin(page, u)


def clean(el, page):
    """Return sanitized HTML string of el's children."""
    for c in el.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for t in el.find_all(['script', 'style', 'noscript', 'svg', 'link', 'meta', 'input', 'button', 'form']):
        t.decompose()
    for t in list(el.find_all(True)):
        if t.name not in KEEP:
            t.unwrap(); continue
        keep = ATTRS.get(t.name, [])
        for a in list(t.attrs):
            if a not in keep:
                del t[a]
        if t.name == 'a' and t.get('href'):
            t['href'] = abs_url(t['href'], page)
        if t.name in ('img', 'iframe') and t.get('src'):
            t['src'] = abs_url(t['src'], page)
        if t.name == 'span':
            t.unwrap()
    # drop empty divs/paragraphs (whitespace / nbsp only, no media)
    changed = True
    while changed:
        changed = False
        for t in el.find_all(['div', 'p', 'strong', 'em', 'b']):
            if not t.get_text(strip=True).replace('\xa0', '') and not t.find(['img', 'iframe', 'br', 'hr']):
                t.decompose(); changed = True
    html = el.decode_contents()
    html = re.sub(r'\n\s*\n+', '\n', html).strip()
    return html


def photos_block(b):
    out = {'type': 'photos', 'items': []}
    sc = b.find('script', class_='photo-show-json')
    if sc:
        d = json.loads(sc.string)
        out['mode'] = d.get('mode')
        for it in d.get('items', []):
            vs = sorted(it.get('versions', []), key=lambda v: v.get('width', 0))
            if not vs:
                continue
            big = vs[-1]
            mid = next((v for v in vs if v['width'] >= 1920), big)
            out['items'].append({'src': big['url'], 'w': big.get('width'), 'h': big.get('height'),
                                 'display': mid['url'], 'caption': it.get('caption', ''),
                                 'versions': [{'w': v['width'], 'url': v['url']} for v in vs],
                                 'alt': it.get('altText', '')})
    else:
        out['mode'] = 'stack'
        for sp in b.select('.stack-photo'):
            a = sp.find('a'); im = sp.find('img')
            if not im:
                continue
            cap = sp.find(class_=re.compile('caption'))
            out['items'].append({'src': a['href'] if a else im['src'], 'display': im['src'],
                                 'caption': cap.get_text(' ', strip=True) if cap else '',
                                 'alt': im.get('alt', '')})
    return out


def files_block(b, page):
    out = {'type': 'files', 'title': '', 'items': []}
    h = b.find(['h2', 'h3'])
    if h:
        out['title'] = h.get_text(' ', strip=True)
    for li in b.select('li.file-holder'):
        a = li.find('a', href=True)
        if not a:
            continue
        out['items'].append({'text': a.get_text(' ', strip=True), 'href': abs_url(a['href'], page),
                             'embed': bool(li.find('iframe', attrs={'data-pdf-embed': True}))})
    return out


def nav_block(b, page):
    items = []
    for li in b.select('nav > ul > li'):
        a = li.find('a', href=True)
        if not a:
            continue
        sub = []
        for sli in li.select('ul li'):
            sa = sli.find('a', href=True)
            if sa:
                sub.append({'text': sa.get_text(' ', strip=True), 'href': abs_url(sa['href'], page),
                            'current': 'current' in (sli.get('class') or [])})
        items.append({'text': a.get_text(' ', strip=True), 'href': abs_url(a['href'], page),
                      'current': 'current' in (li.get('class') or []), 'sub': sub})
    return {'type': 'nav', 'items': items}


def breadcrumb(main, page):
    bc = main.find(id='breadcrumbs')
    if not bc:
        return []
    out = []
    for p in bc.select('.breadcrumb-parent a'):
        out.append({'text': p.get_text(' ', strip=True), 'href': abs_url(p['href'], page)})
    cur = bc.select_one('.breadcrumb-current')
    if cur:
        out.append({'text': cur.get_text(' ', strip=True), 'href': None})
    return out


def extract_page(s, url):
    main = s.find(id='content_main')
    fix_emails(main)
    if main.find(id='login-form'):
        return {'kind': 'login'}
    h1 = main.find('h1', class_='pageTitle')
    rec = {'title': h1.get_text(' ', strip=True) if h1 else '', 'breadcrumb': breadcrumb(main, url)}
    news_list = main.find(class_='news-list')
    if news_list:
        rec['kind'] = 'news-list'
        arts = []
        for art in news_list.find_all('article'):
            a = art.find('a', class_='news-item-link')
            img = art.find('img')
            t = art.find(class_='title')
            sm = art.find(class_='summary')
            arts.append({'title': t.get_text(' ', strip=True) if t else '',
                         'summary': clean(sm, url) if sm else '',
                         'href': abs_url(a['href'], url) if a else None,
                         'img': abs_url(img['src'], url) if img else None,
                         'alert': bool(art.find(class_='public-alert-icon'))})
        rec['articles'] = arts
        pag = []
        p = main.find(id='pagination')
        if p:
            for a in p.find_all('a', href=True):
                pag.append({'text': a.get_text(' ', strip=True), 'href': abs_url(a['href'], url)})
        rec['pagination'] = pag
        return rec
    show = main.find(class_='show-news')
    if show:
        rec['kind'] = 'article'
        imgs = []
        for a in show.select('aside.attached-images a'):
            im = a.find('img')
            imgs.append({'src': abs_url(a['href'], url), 'thumb': abs_url(im['src'], url) if im else None,
                         'alt': im.get('alt', '') if im else ''})
        rec['images'] = imgs
        sm = show.select_one('.article-content .summary')
        rec['summary'] = clean(sm, url) if sm else ''
        body = show.select_one('.article-content .body')
        rec['body'] = clean(body, url) if body else ''
        return rec
    wrap = main.find(class_='pages-content-wrapper')
    rec['kind'] = 'page'
    rec['layout'] = [c for c in wrap.get('class', []) if c not in ('pages-content-wrapper', 'style-overwrite')][0] if wrap else ''
    blocks = []
    sidebar = []
    if wrap:
        for col in wrap.select('.pages-column'):
            target = sidebar if 'pages-right-column' in col.get('class', []) else blocks
            for b in col.find_all(class_='page-block', recursive=False):
                cls = b.get('class', [])
                if 'page-block-photos' in cls:
                    target.append(photos_block(b))
                elif 'page-block-files' in cls:
                    target.append(files_block(b, url))
                elif 'page-block-nav' in cls:
                    target.append(nav_block(b, url))
                elif 'page-block-text' in cls:
                    h = clean(b, url)
                    if h:
                        target.append({'type': 'text', 'html': h})
    rec['blocks'] = blocks
    rec['sidebar'] = sidebar
    return rec


def extract_home(s, url):
    main = s.find(id='content_main')
    fix_emails(main)
    home = {}
    modal = main.find(id='homepage_news_alert_modal')
    if modal:
        home['modal'] = {'title': modal.find(class_='title').get_text(' ', strip=True),
                         'summary': clean(modal.find(class_='summary'), url),
                         'cta': {'text': modal.select_one('.read-more a').get_text(' ', strip=True),
                                 'href': modal.select_one('.read-more a')['href']},
                         'dismiss': modal.find(id='dont-show-again').get_text(' ', strip=True)}
    sp = []
    for c in main.select('section.spotlight1-container'):
        img = c.find('img', class_='spotlight-image')
        sp.append({'title': c.find(class_='section-title').get_text(' ', strip=True),
                   'img': img['src'], 'alt': img.get('alt', ''),
                   'lines': [d.get_text(' ', strip=True) for d in c.select('.item-text div') if not d.find('div') and d.get_text(strip=True)]})
    home['spotlights'] = sp
    home['quicklinks'] = [{'text': a.get_text(' ', strip=True), 'href': abs_url(a['href'], url)}
                          for a in main.select('#quicklinks_fixed a')]
    nc = main.find(id='news_container')
    home['news'] = {'title': nc.find(class_='section-title').get_text(' ', strip=True),
                    'href': abs_url(nc.find(class_='section-title').find('a')['href'], url),
                    'items': [], 'more': {'text': nc.select_one('.read-more-link').get_text(strip=True),
                                          'href': abs_url(nc.select_one('.read-more-link')['href'], url)}}
    for art in nc.find_all('article'):
        im = art.find('img'); a = art.select_one('.item-name a')
        home['news']['items'].append({'title': a.get_text(' ', strip=True), 'href': abs_url(a['href'], url),
                                      'img': im['src'] if im else None})
    home['sections'] = []
    for a in main.select('#shuffle_qlinks a.mosaic-item'):
        m = re.search(r"url\('([^']+)'\)", a.get('style', ''))
        home['sections'].append({'title': a.get_text(' ', strip=True), 'href': a['href'], 'img': m.group(1) if m else None})
    home['gallery'] = []
    for d in main.select('#mosaic_container .mosaic-item'):
        m = re.search(r"url\('([^']+)'\)", d.get('style', ''))
        if m:
            home['gallery'].append(m.group(1))
    return home


def extract_chrome(s, url):
    nav = []
    for li in s.select('#sitenav_main > ul.nav-menu > li.nav-item'):
        a = li.find('a')
        item = {'text': a.get_text(' ', strip=True), 'href': abs_url(a.get('href'), url), 'sub': []}
        for sa in li.select('.sub-nav-item a'):
            item['sub'].append({'text': sa.get_text(' ', strip=True), 'href': abs_url(sa['href'], url)})
        nav.append(item)
    f = s.find(id='footer_main')
    fix_emails(f)
    foot = {'name': f.select_one('.footer-title').get_text(' ', strip=True), 'addresses': []}
    for ad in f.select('.footer-address'):
        blk = {'title': ad.find(class_='title-footer').get_text(' ', strip=True), 'items': [], 'images': []}
        for ib in ad.select('.footer-info-block'):
            a = ib.find('a')
            lines = [x.strip() for x in a.get_text('\n').split('\n') if x.strip()]
            blk['items'].append({'lines': lines, 'href': abs_url(a['href'], url),
                                 'kind': 'tel' if a['href'].startswith('tel') else ('map' if 'maps' in a['href'] else 'link')})
        for a in ad.find_all('a', recursive=False):
            im = a.find('img')
            if im:
                blk['images'].append({'href': abs_url(a['href'], url), 'src': abs_url(im['src'], url)})
        foot['addresses'].append(blk)
    tf = f.select_one('.text-footer')
    foot['legal'] = [x.strip() for x in tf.find(string=True, recursive=False).parent.get_text('\n').split('\n')
                     if x.strip() and 'Aviso' not in x]
    pa = tf.select_one('.footer-info-block a') or tf.find('a', href=True)
    foot['legal_privacy'] = {'text': pa.get_text(strip=True), 'href': abs_url(pa['href'], url)}
    foot['emails'] = [a['href'][7:] for a in f.select('.footer-row a[href^="mailto:"]')]
    lf = f.select_one('a.link-footer')
    foot['bottom_link'] = {'text': lf.get_text(strip=True), 'href': abs_url(lf['href'], url)}
    return {'nav': nav, 'footer': foot}


data = {'pages': {}, 'login': []}
for url, meta in index.items():
    if 'file' not in meta or url.endswith('rss?categoryid=14340'):
        continue
    s = BeautifulSoup(open(os.path.join(PAGES, meta['file']), encoding='utf-8').read(), 'lxml')
    if url == BASE:
        data['chrome'] = extract_chrome(s, url)
        s = BeautifulSoup(open(os.path.join(PAGES, meta['file']), encoding='utf-8').read(), 'lxml')
        data['home'] = extract_home(s, url)
        data['meta_description'] = s.find('meta', attrs={'name': 'description'})['content']
        continue
    rec = extract_page(s, url)
    if rec.get('title', '').startswith('404'):
        continue
    if rec['kind'] == 'login':
        data['login'].append(url)
        continue
    rec['doc_title'] = meta['title']
    data['pages'][url] = rec

json.dump(data, open(OUT, 'w'), indent=1, ensure_ascii=False)
print(len(data['pages']), 'pages;', 'login:', data['login'])
