"""Extrae, sin cambiar el texto, las fichas de producto y el aviso de privacidad de chinoin.com.

Uso: python3 tools/fichas.py <carpeta_con_html_descargado> > js/fichas.js
Conserva solo etiquetas de contenido (títulos, párrafos, listas, tablas, énfasis y enlaces).
"""
import json
import pathlib
import re
import sys

from bs4 import BeautifulSoup, Comment, NavigableString

KEEP = {'h2', 'h3', 'h4', 'h5', 'p', 'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tr', 'td', 'th',
        'strong', 'b', 'em', 'i', 'sup', 'sub', 'br', 'a'}
DROP = {'script', 'style', 'noscript', 'svg', 'img', 'form', 'button', 'iframe', 'input'}


def clean(node):
    for c in node.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for t in node.find_all(DROP):
        t.decompose()
    for t in node.find_all(True):
        if t.name not in KEEP:
            t.unwrap()
            continue
        href = t.get('href') if t.name == 'a' else None
        t.attrs = {}
        if t.name == 'td' or t.name == 'th':
            pass
        if href and re.match(r'^(mailto:|https?://)', href):
            t['href'] = href
            if href.startswith('http'):
                t['target'] = '_blank'
                t['rel'] = 'noopener'
        elif t.name == 'a':
            t.unwrap()
    # quita etiquetas vacías
    for t in node.find_all(True):
        if t.name not in ('br', 'td', 'th') and not t.get_text(strip=True):
            t.decompose()
    html = node.decode_contents()
    html = re.sub(r'\s+', ' ', html)
    html = re.sub(r'>\s+<', '><', html)
    return html.strip()


def load_main(path):
    s = BeautifulSoup(pathlib.Path(path).read_text(encoding='utf-8'), 'html.parser')
    return s.find('main')


def accordion_by_h2(path):
    """Páginas con varias presentaciones: cada h2 seguido de un acordeón de secciones."""
    main = load_main(path)
    res, current = {}, None
    for el in main.find_all(['h2', 'div']):
        if el.name == 'h2':
            current = el.get_text(' ', strip=True)
            res[current] = []
        elif 'gb-accordion-macro-item' in (el.get('class') or []) and current:
            h3 = el.find('h3')
            title = h3.get_text(' ', strip=True)
            h3.decompose()
            res[current].append({'t': title, 'html': clean(el)})
    return res


def sections_by_h3(path):
    """Fichas largas (IPP): corta el contenido en cada h3."""
    main = load_main(path)
    h1 = main.find('h1')
    if h1:
        h1.decompose()
    html = clean(main)
    parts = re.split(r'<h3>(.*?)</h3>', html)
    intro = BeautifulSoup(parts[0], 'html.parser').get_text(' ', strip=True)
    secs = [{'t': BeautifulSoup(parts[i], 'html.parser').get_text(' ', strip=True), 'html': parts[i + 1].strip()}
            for i in range(1, len(parts), 2)]
    return intro, secs


def whole(path):
    main = load_main(path)
    h1 = main.find('h1')
    if h1:
        h1.decompose()
    return clean(main)


def main():
    d = pathlib.Path(sys.argv[1])
    neo = accordion_by_h2(d / 'neoseverin.html')
    sca = accordion_by_h2(d / 'scabisan.html')
    fichas = {
        'neoseverin-tabletas': {'tipo': 'resumen', 'secciones': neo['Neoseverin tabletas']},
        'neoseverin-suspension': {'tipo': 'resumen', 'secciones': neo['Neoseverin suspensión']},
        'scabisan-crema': {'tipo': 'resumen', 'secciones': sca['Scabisan crema']},
        'scabisan-emulsion': {'tipo': 'resumen', 'secciones': sca['Scabisan emulsión']},
    }
    for key, page in [('neoseverin-suspension-ipp', 'neoseverin-suspension'), ('sunderin-tableta', 'sunderin-tableta'),
                      ('zymir-ab-suspension', 'zymir-ab-suspension')]:
        intro, secs = sections_by_h3(d / f'{page}.html')
        fichas[key] = {'tipo': 'ipp', 'intro': intro, 'secciones': secs}
    aviso = whole(d / 'aviso-de-privacidad.html')
    print('/* Generado por tools/fichas.py a partir de chinoin.com. No editar a mano. */')
    print('window.CHINOIN_FICHAS = ' + json.dumps(fichas, ensure_ascii=False, indent=1) + ';')
    print('window.CHINOIN_AVISO = ' + json.dumps(aviso, ensure_ascii=False) + ';')


if __name__ == '__main__':
    main()
