"""Genera js/marcas.js con la información de los sitios de cada marca de venta libre.

Uso: python3 tools/marcas.py <carpeta_con_sitios_descargados> <lista_imagenes.txt> > js/marcas.js
Carpeta: una subcarpeta por sitio (antiflu-des.mx, anara.mx, feel360.mx, gotinalmar.mx, scabisan.com, topron.mx).
Los textos se copian tal cual; los enlaces de compra son los que publica cada marca.
"""
import json
import pathlib
import re
import sys
import urllib.parse

from bs4 import BeautifulSoup

IMAGES = set()

TIENDAS = {
    'farmaciasguadalajara.com': 'Farmacias Guadalajara', 'fahorro.com': 'Farmacias del Ahorro',
    'benavides.com.mx': 'Farmacias Benavides', 'farmaciasbazar.com': 'Farmacias Bazar', 'farmaciasisseg.com.mx': 'Farmacias ISSEG',
    'farmaciasroma.com': 'Farmacias Roma', 'farmaciaslamasbarata.com': 'Farmacias La Más Barata', 'gusher.com.mx': 'Gusher',
    'klyns.mx': "Klyn's", 'farmaciaspurex.com': 'Farmacias Purex', 'heb.com.mx': 'HEB', 'soriana.com': 'Soriana',
    'lacomer.com.mx': 'La Comer', 'chedraui.com.mx': 'Chedraui', 'farmaciasanpablo.com.mx': 'Farmacia San Pablo',
    'sanborns.com.mx': 'Sanborns', 'farmaciasespecializadas.com': 'Farmacias Especializadas', 'grupofarmapronto.com': 'Farmapronto',
    'calimax.com.mx': 'Calimax', 'yza.mx': 'Farmacias YZA', 'amazon.com.mx': 'Amazon',
}


def soup(path):
    s = BeautifulSoup(pathlib.Path(path).read_text(encoding='utf-8', errors='ignore'), 'html.parser')
    for t in s(['script', 'style', 'noscript', 'svg']):
        t.decompose()
    return s


def txt(el):
    return ' '.join(el.get_text(' ', strip=True).split()) if el else ''


def tienda(href):
    host = urllib.parse.urlparse(href).netloc.lower().replace('www.', '').replace('tienda.', '')
    for dom, name in TIENDAS.items():
        if host.endswith(dom):
            return name
    return None


def comprar(*paths):
    """Enlaces a tiendas, en el orden en que aparecen en las páginas de la marca."""
    out, seen = [], set()
    for p in paths:
        for a in soup(p).find_all('a', href=True):
            h = a['href'].strip()
            name = tienda(h)
            if name and name not in seen:
                seen.add(name)
                out.append({'tienda': name, 'href': h})
    return out


def image(base, src):
    if not src:
        return None
    url = urllib.parse.urljoin(base, src)
    stem = re.sub(r'[^a-z0-9]+', '-', pathlib.Path(urllib.parse.urlparse(url).path).stem.lower()).strip('-')
    local = f'assets/img/marcas/{urllib.parse.urlparse(url).netloc.replace("www.", "").split(".")[0]}-{stem}.webp'
    IMAGES.add((url, local))
    return local


def secciones(root, base, start=None, stop=None, heads=('h4',), skip=()):
    """Recorre el contenido en orden; cada encabezado abre una sección."""
    out, cur, on = [], None, start is None
    for el in root.find_all(list(heads) + ['p', 'li', 'img']):
        if el.name == 'img':
            if stop and stop(el):
                break
            if on and cur is not None:
                cur['items'].append(['img', image(base, el.get('src'))])
            continue
        t = txt(el)
        if not on:
            if el.name in heads and t == start:
                on = True
            else:
                continue
        if el.name in heads:
            cur = {'t': t, 'items': []}
            out.append(cur)
            continue
        if el.name == 'p' and el.find_parent('li'):
            continue
        if not t or t in skip or cur is None:
            continue
        cur['items'].append(['li' if el.name == 'li' else 'p', t])
    return [s for s in out if s['items']]


# Textos que el sitio de Antiflu-Des publica como imagen (transcritos tal cual)
TEXTO_EN_IMAGEN = {
    'amantadina-1': 'Amantadina, Clorfenamina, Paracetamol.',
    'amantadina-2': 'En el tratamiento y prevención de la gripe o influenza causada por virus susceptibles a la Amantadina. '
                    'También alivia los síntomas que la acompañan, como fiebre, dolor muscular, escurrimiento nasal, dolor de cabeza y malestar general.',
}


def antiflu(d):
    base = 'https://antiflu-des.mx/'
    skip = {'Presentación | Denominación Genérica | Indicaciones terapéuticas',
            'Vía de administración | Dosis y modo de empleo | Uso en el embarazo y lactancia',
            'Contraindicaciones | Precauciones y advertencias | Uso pediátrico | Reacciones adversas'}
    stop = lambda el: 'prod-super' in (el.get('src') or '')  # noqa: E731
    fichas = {}
    for page, pid in [('antiflu_des', 'antiflu-des-capsulas'), ('antiflu_des_jr', 'antiflu-des-jarabe'),
                      ('antiflu_des_pediatrico', 'antiflu-des-pediatrico')]:
        s = soup(d / f'{page}.html')
        hero = next((i for i in s.find_all('img') if 'hero' in (i.get('src') or '')), None)
        secs = secciones(s.body, base, start='Presentación', stop=stop, skip=skip)
        for sec in secs:
            for it in sec['items']:
                key = next((k for k in TEXTO_EN_IMAGEN if it[0] == 'img' and k in (it[1] or '')), None)
                if key:
                    it[:] = ['p', TEXTO_EN_IMAGEN[key]]
        fichas[pid] = {'secciones': secs,
                       'img': image(base, hero.get('src')) if hero else None}
    return {'nombre': 'Antiflu-Des®', 'sitio': 'https://antiflu-des.mx/', 'comprar': comprar(d / 'comprar.html'), 'fichas': fichas}


def anara(d):
    base = 'https://anara.mx/'
    s = soup(d / 'anara_html.html')
    fichas = {}
    for h in s.find_all('h4'):
        t = txt(h)
        pid = {'Anara ® tabletas': 'anara-tabletas', 'Anara ® solución (gotas)': 'anara-solucion', 'Anara ® Jarabe': 'anara-jarabe'}.get(t)
        if pid:
            fichas[pid] = {'secciones': [{'t': 'Dosis', 'items': [['p', txt(h.find_next('p'))]]}]}
    ventajas = [txt(h) for h in s.find_all('h2') if txt(h).split(' ')[0].isupper() and txt(h) != 'Beneficios' and 'Ventajas' not in txt(h)]
    beneficios = [txt(p) for p in s.find_all('p') if p.find_previous('h2') and txt(p.find_previous('h2')) == 'Beneficios']
    comunes = [{'t': 'Ventajas con Anara®', 'items': [['li', v] for v in ventajas]},
               {'t': 'Beneficios', 'items': [['li', b] for b in beneficios if b]}]
    for f in fichas.values():
        f['secciones'] += comunes
    fichas['anara-solucion'] = fichas.get('anara-solucion', {'secciones': comunes})
    return {'nombre': 'Anara®', 'sitio': 'https://anara.mx/', 'comprar': comprar(d / 'donde_comprar_html.html', d / 'index.html'), 'fichas': fichas}


def topron(d):
    s = soup(d / 'topron_html.html')
    ps = [txt(p) for p in s.find_all('p')]
    caps = next((p for p in ps if p.startswith('Cápsulas')), '')
    susp = next((p for p in ps if p.startswith('Suspensión')), '')
    legal = next((p for p in ps if p.startswith('Es propiedad')), '')
    nota = [['p', legal]] if legal else []
    return {'nombre': 'Topron®', 'sitio': 'https://topron.mx/', 'comprar': comprar(d / 'donde_comprar_html.html', d / 'index.html'),
            'fichas': {'topron-capsulas': {'secciones': [{'t': 'Presentación y dosis', 'items': [['p', caps]]}, {'t': 'Información legal', 'items': nota}]},
                       'topron-suspension': {'secciones': [{'t': 'Presentación y dosis', 'items': [['p', susp]]}, {'t': 'Información legal', 'items': nota}]}}}


def feel(d):
    fichas = {}
    for page, pid in [('feel360', 'feel-360-tabletas'), ('feel360_des', 'feel-360-des-tabletas')]:
        s = soup(d / f'{page}.html')
        f = s.find(lambda t: t.name in ('h5', 'h4') and 'Formulaci' in txt(t))
        items = []
        if f:
            box = f.parent
            while box is not None and len(txt(box)) < 400:
                box = box.parent
            for el in box.find_all(['li', 'p']):
                t = txt(el)
                half = len(t) // 2
                if t and t[:half].strip() == t[half:].strip():
                    continue  # lema animado que el sitio escribe dos veces
                if t and ['li' if el.name == 'li' else 'p', t] not in items:
                    items.append(['li' if el.name == 'li' else 'p', t])
        fichas[pid] = {'secciones': [{'t': 'Formulación e información del producto', 'items': items}]}
    return {'nombre': 'Feel 360®', 'sitio': 'https://feel360.mx/',
            'comprar': comprar(d / 'feel360.html', d / 'feel360_des.html', d / 'index.html'), 'fichas': fichas}


def gotinal(d):
    s = soup(d / 'index.html')
    def bloque(titulo, hasta):
        h = s.find(lambda t: t.name == 'h2' and txt(t) == titulo)
        items, el = [], h
        while el is not None:
            el = el.find_next(['h2', 'p'])
            if el is None or (el.name == 'h2' and txt(el) == hasta):
                break
            t = txt(el)
            if ['p', t] in items or t == titulo:
                break  # el sitio repite el bloque (versión móvil); hasta aquí llega
            if (el.name == 'p' and t and len(t) > 25) or (el.name == 'h2' and t):
                items.append(['p', t])
        return items
    tec = s.find(lambda t: t.name == 'p' and txt(t) == 'LA TECNOLOGÍA DEL DISPOSITIVO')
    disp = []
    if tec:
        el = tec
        for _ in range(8):
            el = el.find_next('p')
            if el is None or txt(el).startswith('Conoce más'):
                break
            t = txt(el)
            if t == 'y':
                continue
            if t.endswith('componentes bioactivos de'):
                # en el original la frase termina con los logotipos de ambos productos
                t += ' Gotinal® Mar SOFT y Gotinal® Mar DEFENSE.'
                disp.append(['p', t])
                disp.append(['li', 'No hay necesidad de añadir gas a la fórmula'])
                continue
            disp.append(['li' if len(t) < 70 else 'p', t])
    legal = [['p', txt(p)] for p in s.find_all('p') if re.match(r'^(Permiso|Registro Sanitario|GOTINAL ® Mar)', txt(p))]
    soft = [{'t': 'Agua de Mar Nasal con Manzanilla y Aloe Vera', 'items': bloque('Agua de Mar Nasal con Manzanilla y Aloe Vera', 'Agua de Mar Nasal con Xilitol')}]
    defense = [{'t': 'Agua de Mar Nasal con Xilitol', 'items': bloque('Agua de Mar Nasal con Xilitol', 'DÓNDE COMPRAR')}]
    reg = {'t': 'Información legal', 'items': legal}
    soft.append({'t': 'La tecnología del dispositivo', 'items': disp})
    defense.append({'t': 'La tecnología del dispositivo', 'items': disp})
    return {'nombre': 'Gotinal® Mar', 'sitio': 'https://gotinalmar.mx/', 'comprar': comprar(d / 'index.html'),
            'fichas': {'gotinal-mar-soft': {'secciones': soft + [reg]}, 'gotinal-mar-defense': {'secciones': defense + [reg]}}}


def scabisan(d):
    s = soup(d / 'indicaciones.html')
    secs = []
    for h in s.find_all('h2'):
        t = txt(h)
        if t not in ('Sobre Scabisan® shampoo', 'Precauciones'):
            continue
        items, el = [], h
        while True:
            el = el.find_next(['h2', 'p'])
            if el is None or el.name == 'h2':
                break
            if txt(el):
                items.append(['p', txt(el)])
        secs.append({'t': 'Indicaciones' if t.startswith('Sobre') else t, 'items': items})
    idx = soup(d / 'index.html')
    pasos = []
    for h in idx.find_all('h3'):
        t = txt(h)
        if re.match(r'^\d\.', t):
            p = h.find_next('p')
            pasos.append(['li', f'{t}: {txt(p)}'] if not t.startswith('5') else ['li', t])
            if t.startswith('5'):
                el = h
                for _ in range(6):
                    el = el.find_next('p')
                    if not el or not txt(el).startswith('-'):
                        break
                    pasos.append(['li', txt(el).lstrip('- ').strip()])
    legal = next((txt(p) for p in idx.find_all('p') if 'PERMISO' in txt(p)), '')
    secs.insert(0, {'t': 'Modo de uso', 'items': pasos})
    if legal:
        secs.append({'t': 'Información legal', 'items': [['p', legal]]})
    return {'nombre': 'Scabisan® Shampoo', 'sitio': 'https://scabisan.com/', 'comprar': comprar(d / 'index.html', d / 'indicaciones.html'),
            'fichas': {'scabisan-shampoo': {'secciones': secs}}}


def main():
    d = pathlib.Path(sys.argv[1])
    marcas = {
        'antiflu-des': antiflu(d / 'antiflu-des.mx'),
        'anara': anara(d / 'anara.mx'),
        'feel-360': feel(d / 'feel360.mx'),
        'gotinal-mar': gotinal(d / 'gotinalmar.mx'),
        'scabisan': scabisan(d / 'scabisan.com'),
        'topron': topron(d / 'topron.mx'),
    }
    pathlib.Path(sys.argv[2]).write_text('\n'.join(f'{a}\t{b}' for a, b in sorted(IMAGES)), encoding='utf-8')
    print('/* Generado por tools/marcas.py a partir de los sitios de cada marca. No editar a mano. */')
    print('window.CHINOIN_MARCAS = ' + json.dumps(marcas, ensure_ascii=False, indent=1) + ';')


if __name__ == '__main__':
    main()
