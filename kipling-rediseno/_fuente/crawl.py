"""Descarga las páginas públicas de un sitio Edlio de Kipling.

    python3 crawl.py https://www.kipling.edu.mx/ /tmp/satelite
    python3 crawl.py https://www.kiplingesmeralda.edu.mx/ /tmp/esmeralda
    python3 crawl.py https://www.kipling.mx/ /tmp/grupo --seeds /apps/pages/bachilleratointernacional /apps/pages/blog \
        --only 'uREC_ID=(1831034|4122469)|bachilleratointernacional|/apps/pages/blog' --depth 1
"""
import argparse, hashlib, json, os, re
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

ap = argparse.ArgumentParser()
ap.add_argument('base')
ap.add_argument('out')
ap.add_argument('--seeds', nargs='*', default=None)
ap.add_argument('--depth', type=int, default=2)
ap.add_argument('--limit', type=int, default=200)
ap.add_argument('--only', default=None, help='regex que deben cumplir las URLs a seguir')
args = ap.parse_args()

BASE = args.base.rstrip('/') + '/'
HOST = urlparse(BASE).netloc
bare = HOST[4:] if HOST.startswith('www.') else HOST
os.makedirs(args.out, exist_ok=True)
S = requests.Session()
S.headers['User-Agent'] = 'Mozilla/5.0'


def norm(u):
    u = u.split('#')[0]
    for pre in ('http://www.' + bare, 'https://' + bare, 'http://' + bare):
        if u.startswith(pre):
            u = 'https://www.' + bare + u[len(pre):]
    return u


seeds = [urljoin(BASE, s) for s in args.seeds] if args.seeds else [BASE]
seen, queue = {}, [(norm(s), 0) for s in seeds]
while queue and len(seen) < args.limit:
    u, d = queue.pop(0)
    if u in seen:
        continue
    try:
        r = S.get(u, timeout=30)
    except Exception as e:
        seen[u] = {'err': str(e)}
        continue
    if 'html' not in r.headers.get('content-type', ''):
        seen[u] = {'status': r.status_code, 'ct': r.headers.get('content-type', '')}
        continue
    fn = hashlib.md5(u.encode()).hexdigest()[:10] + '.html'
    open(os.path.join(args.out, fn), 'w').write(r.text)
    s = BeautifulSoup(r.text, 'lxml')
    t = s.title.string.strip() if s.title and s.title.string else ''
    seen[u] = {'status': r.status_code, 'file': fn, 'title': t, 'final': r.url}
    if d >= args.depth:
        continue
    links = []
    if d == 0 and not args.seeds:
        links += [a.get('href') for a in (s.find(id='sitenav_main') or s).find_all('a')]
    main = s.find(id='content_main') or s
    links += [a.get('href') for a in main.find_all('a')]
    if not args.seeds:
        links += [a.get('href') for a in (s.find('footer') or s).find_all('a')]
    for h in links:
        if not h or h.startswith(('javascript', 'tel:', 'mailto:', '/cdn-cgi')):
            continue
        v = norm(urljoin(u, h))
        if urlparse(v).netloc != 'www.' + bare or v in seen:
            continue
        if re.search(r'\.(pdf|jpe?g|png|docx?|heic)$', v, re.I) or 'rss' in v:
            continue
        if args.only and not re.search(args.only, v):
            continue
        queue.append((v, d + 1))
json.dump(seen, open(os.path.join(args.out, 'index.json'), 'w'), indent=1, ensure_ascii=False)
for k, v in seen.items():
    print(v.get('status'), v.get('title'), k)
