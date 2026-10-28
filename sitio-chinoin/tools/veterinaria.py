"""Genera js/veterinaria.js a partir de chinoinveterinaria.com/sitio (páginas ya descargadas).

Uso: python3 tools/veterinaria.py <carpeta_html> <carpeta_salida_imagenes> > js/veterinaria.js
Los textos se copian tal cual; las imágenes se listan para descargarlas y optimizarlas aparte.
"""
import json
import pathlib
import re
import sys
import unicodedata

from bs4 import BeautifulSoup

BASE = 'https://chinoinveterinaria.com/sitio/'
LINEAS = [
    ('pequenas-especies-farmaceutica', 'Pequeñas Especies', 'Farmacéutica'),
    ('pequenas-especies-oftalmico', 'Pequeñas Especies', 'Oftálmicos'),
    ('pequenas-especies-vacunas', 'Pequeñas Especies', 'Vacunas'),
    ('grandes-especies-farmaceutica', 'Grandes Especies', 'Farmacéutica'),
    ('grandes-especies-biologicos', 'Grandes Especies', 'Biológicos'),
]
ESPECIES = [('bovino', 'Bovinos'), ('ovino', 'Ovinos'), ('caprino', 'Caprinos'), ('porcino', 'Porcinos'),
            ('equino', 'Equinos'), ('Canino', 'Caninos'), ('felino', 'Felinos')]
IMAGES = set()


def slug(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def soup(d, name):
    raw = (d / name).read_bytes()
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        text = raw.decode('latin-1')
    s = BeautifulSoup(text, 'html.parser')
    for t in s(['script', 'style', 'noscript']):
        t.decompose()
    return s


def txt(el):
    return ' '.join(el.get_text(' ', strip=True).split()) if el else ''


def image(src):
    """Ruta local (assets/img/vet-prod/…) para una imagen del sitio veterinario."""
    if not src:
        return None
    src = src.strip()
    stem = slug(pathlib.Path(src).stem)
    if 'fondosmedicamentos' in src:
        stem = 'fondo-' + stem
    local = f'assets/img/vet-prod/{stem}.webp'
    IMAGES.add((src, local))
    return local


def main_content(s):
    for sel in ['nav', 'footer', '.bar', '.nav-container', '.notification']:
        for t in s.select(sel):
            t.decompose()
    return s.find('div', class_='main-container') or s.body


def linea(d, page, grupo, nombre):
    s = soup(d, page + '.html')
    m = main_content(s)
    items = []
    for it in m.select('.masonry__item'):
        a = it.find('a', href=True)
        img = it.find('img')
        span = it.find('span', class_=re.compile('h4'))
        lines = [x.strip() for x in span.get_text('\n').split('\n') if x.strip()] if span else []
        if not lines:
            continue  # tarjeta vacía en el original
        href = a['href'] if a else None
        if href in ('#', ''):
            href = None  # en el original este enlace no lleva a ningún lado
        items.append({
            'href': href,
            'img': image(img.get('src')) if img else None,
            'forma': txt(it.find('h5')),
            'name': lines[0] if lines else '',
            'sub': ' '.join(lines[1:]),
            'categoria': it.get('data-masonry-filter', '').strip(),
            'grupo': grupo, 'linea': nombre,
        })
    return items


def ficha(d, href):
    """Ficha de producto. Devuelve título, subtítulo, especies, imágenes y secciones en orden."""
    s = soup(d, href)
    m = main_content(s)
    out = {'secciones': [], 'especies': [], 'presentaciones': [], 'imagenes': []}
    head = m.find(class_='navegacion-producto')
    if head:
        hs = [txt(h) for h in head.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'span']) if txt(h)]
        hs = list(dict.fromkeys(hs))
        out['title'] = hs[0] if hs else ''
        out['subtitle'] = ' '.join(hs[1:])
        head.decompose()
    h1 = m.find('h1')
    # Plantilla antigua: título, una línea y una imagen con toda la información
    if not m.find('h2') and h1:
        out['title'] = txt(h1)
        out['subtitle'] = ' '.join(txt(p) for p in m.find_all('p') if txt(p) and '©' not in txt(p) and 'Â©' not in txt(p))
        out['imagenes'] = [image(i.get('src')) for i in m.find_all('img') if i.get('src')]
        out['tipo'] = 'imagen'
        return out
    out['tipo'] = 'secciones'
    # Especies del bloque "Uso"
    uso = next((h for h in m.find_all(['h2', 'h3']) if txt(h).lower().startswith('uso')), None)
    if uso:
        block = uso.find_parent('div').find_parent('div')
        norm = {'bovino': 'Bovinos', 'bovinos': 'Bovinos', 'ovinos': 'Ovinos', 'caprinos': 'Caprinos', 'porcinos': 'Porcinos',
                'equinos': 'Equinos', 'caninos': 'Caninos', 'felinos': 'Felinos'}
        out['especies'] = [norm.get(txt(p).lower(), txt(p)) for p in block.find_all('p') if txt(p)]
    # Presentaciones (imagen + texto)
    pres = next((h for h in m.find_all('h2') if txt(h).lower().startswith('presentaci')), None)
    if pres:
        cont = pres.find_parent('div').find_parent('div')
        for it in cont.select('.product, .masonry__item'):
            img = it.find('img')
            out['presentaciones'].append({'img': image(img.get('src')) if img else None, 'text': txt(it.find(['h3', 'h4', 'h5', 'p']))})
        cont.decompose()
    if uso:
        uso.find_parent('div').find_parent('div').decompose()
    # Resto: recorrido en orden; cada h2/h3 abre una sección
    current = None
    for el in m.find_all(['h2', 'h3', 'h4', 'p', 'li', 'div', 'td']):
        if el.name in ('h2', 'h3', 'h4'):
            t = txt(el).rstrip(':').strip()
            if not t:
                continue
            current = {'t': t, 'p': []}
            out['secciones'].append(current)
            continue
        if el.find(['p', 'li', 'div', 'h2', 'h3', 'h4', 'ul', 'table']):
            continue
        if el.find_parent(['li', 'p', 'h2', 'h3', 'h4']) and el.name in ('div', 'p'):
            continue
        t = txt(el)
        if not t or '©' in t or 'TODOS LOS DERECHOS' in t.upper() or t in ('Image', 'imagen'):
            continue
        if current is None:
            current = {'t': 'Descripción', 'p': []}
            out['secciones'].append(current)
        kind = 'li' if el.name == 'li' else 'p'
        if not current['p'] or current['p'][-1] != [kind, t]:
            current['p'].append([kind, t])
    out['secciones'] = [x for x in out['secciones'] if x['p']]
    return out


def textos(d):
    res = {}
    s = soup(d, 'index.html')
    m = main_content(s)
    res['inicio'] = [t for t in (txt(x) for x in m.find_all(['h1', 'h2', 'h3', 'h4', 'p'])) if t]
    s = soup(d, 'empresa.html')
    m = main_content(s)
    res['empresa'] = []
    for h in m.find_all('h2'):
        t = txt(h)
        if t.upper() == 'EMPRESA':
            continue
        sec = h.find_parent('section') or h.parent
        bg = sec.find('img')
        res['empresa'].append({'t': t, 'p': [txt(p) for p in sec.find_all('p') if txt(p)], 'img': image(bg.get('src')) if bg else None})
    s = soup(d, 'historia.html')
    m = main_content(s)
    res['historia'] = [{'year': txt(h), 'p': txt(h.find_next('p'))} for h in m.find_all('h4')]
    res['historiaImgs'] = [image(i.get('src')) for i in m.find_all('img') if 'Veterinaria' in (i.get('src') or '')]
    res['especiesImgs'] = {}
    for page, label in ESPECIES:
        sm = main_content(soup(d, page + '.html'))
        img = sm.find('img')
        res['especiesImgs'][label] = image(img.get('src')) if img else None
    return res


def decode_cf(hexstr):
    key = int(hexstr[:2], 16)
    return ''.join(chr(int(hexstr[i:i + 2], 16) ^ key) for i in range(2, len(hexstr), 2))


def contacto(d):
    raw = (d / 'index.html').read_text(encoding='utf-8', errors='ignore')
    mails = sorted({decode_cf(h) for h in re.findall(r'email-protection#([0-9a-f]+)', raw)})
    return [m.split('?')[0] for m in mails]


def main():
    d = pathlib.Path(sys.argv[1])
    productos, vistos = [], {}
    for page, grupo, nombre in LINEAS:
        for it in linea(d, page, grupo, nombre):
            key = it['href'] or it['name']
            if key in vistos:
                vistos[key]['lineas'].append(f'{grupo} · {nombre}')
                continue
            it['lineas'] = [f'{grupo} · {nombre}']
            it['id'] = slug(it['name'].replace('®', '') + ('-' + it['forma'] if it['forma'] else ''))
            vistos[key] = it
            productos.append(it)
    # Une tarjetas repetidas del mismo producto (p. ej. una sin enlace y otra con ficha)
    unidos = {}
    for p in list(productos):
        k = (slug(p['name'].replace('®', '')), slug(p['forma']))
        if k in unidos:
            q = unidos[k]
            keep, drop = (q, p) if q['href'] else (p, q)
            keep['lineas'] = list(dict.fromkeys(q['lineas'] + p['lineas']))
            if not drop['href'] and drop['img']:
                keep['img'] = drop['img']  # la tarjeta sin enlace trae el empaque nuevo
            productos.remove(drop)
            unidos[k] = keep
        else:
            unidos[k] = p
    hermanos = {}
    for p in productos:
        if p['categoria'] and p['categoria'] != 'Audio':
            hermanos.setdefault(p['linea'] + p['forma'], p['categoria'])
    for p in productos:
        if p['categoria'] == 'Audio':  # error de etiqueta en el original
            p['categoria'] = hermanos.get(p['linea'] + p['forma'], '')
    ids = {}
    for p in productos:
        ids[p['id']] = ids.get(p['id'], 0) + 1
        if ids[p['id']] > 1:
            p['id'] += f'-{ids[p["id"]]}'
        if p['href'] and (d / p['href']).exists():
            p['ficha'] = ficha(d, p['href'])
        p['url'] = BASE + p['href'] if p['href'] else None
    # Lanzamientos recientes de la portada
    s = soup(d, 'index.html')
    destacados = []
    for a in s.find_all('a', href=True):
        p = vistos.get(a['href'])
        if p and p in productos and a.get_text(strip=True) and p['id'] not in destacados:
            destacados.append(p['id'])
    puppy = next((p for p in productos if p['name'].startswith('PARASTIN PUPPY')), None)
    if puppy and puppy['id'] not in destacados:
        destacados.insert(0, puppy['id'])
    data = {'productos': productos, 'destacados': destacados, 'textos': textos(d), 'correos': contacto(d)}
    pathlib.Path(sys.argv[2]).write_text('\n'.join(f'{a}\t{b}' for a, b in sorted(IMAGES)), encoding='utf-8')
    print('/* Generado por tools/veterinaria.py a partir de chinoinveterinaria.com. No editar a mano. */')
    print('window.CHINOIN_VET = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';')


if __name__ == '__main__':
    main()
