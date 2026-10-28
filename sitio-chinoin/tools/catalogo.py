"""Genera js/catalogo.js con el catálogo de productos de chinoin.com/es/catalogo.

Uso: python3 tools/catalogo.py <carpeta_con_html_descargado> > js/catalogo.js
Nombres, categorías e imágenes salen tal cual del catálogo y de las páginas de cada padecimiento.
"""
import json
import os
import pathlib
import re
import sys
import unicodedata
import urllib.parse

from bs4 import BeautifulSoup


def slug(s):
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def img_file(src):
    name = urllib.parse.unquote(src.split('?')[0].split('/')[-1])
    stem, ext = os.path.splitext(name)
    stem = slug(stem)
    return f'assets/img/{stem}{ext if ext == ".svg" else ".webp"}'


def cards(path):
    s = BeautifulSoup(pathlib.Path(path).read_text(encoding='utf-8'), 'html.parser')
    main = s.find('main')
    out = []
    for h4 in main.find_all('h4'):
        # sube mientras el contenedor siga teniendo un solo producto
        card = h4
        while card.parent is not None and card.parent.name != 'main' and len(card.parent.find_all('h4')) == 1:
            card = card.parent
        img = card.find('img')
        tags = [d.get_text(' ', strip=True) for d in card.find_all('div')
                if not d.find(['div', 'h4', 'img', 'a']) and d.get_text(strip=True) and d.get_text(strip=True) != 'Ver más']
        # Solo el botón "Ver más": en el original algunos títulos enlazan a otro producto.
        link = next((a for a in card.find_all('a', href=True) if a.get_text(strip=True) == 'Ver más'), None)
        href = link['href'] if link else None
        if href and href.startswith('//'):
            href = 'https:' + href
        out.append({
            'name': ' '.join(h4.get_text(' ', strip=True).split()),
            'img': img_file(img.get('src')),
            'tags': list(dict.fromkeys(tags)),
            'href': href,
        })
    return out


GROUPS = {'Cuidado de la salud', 'Áreas Terapéuticas', 'Probióticos', 'Odontología'}
PADECIMIENTOS = {'Gripe y resfriado', 'Tos', 'Piojos', 'Acidez estomacal', 'Diarrea', 'Estreñimiento', 'Sarna',
                 'Fiebre y dolor'}


def main():
    d = pathlib.Path(sys.argv[1])
    catalog = cards(d / 'catalogo.html')
    by_name = {}
    for c in catalog:
        c['id'] = slug(c['name'].replace('®', ''))
        c['grupos'] = [t for t in c['tags'] if t in GROUPS]
        c['padecimientos'] = [slug(t) for t in c['tags'] if t in PADECIMIENTOS]
        by_name[c['id']] = c
    # Las páginas de cada padecimiento enlazan a veces a una página más específica
    # y tienen algún producto que no está en el catálogo general.
    for page in ['gripe-y-resfriado', 'tos', 'piojos', 'acidez-estomacal', 'diarrea', 'estrenimiento', 'sarna',
                 'fiebre-y-dolor']:
        for c in cards(d / f'{page}.html'):
            cid = slug(c['name'].replace('®', ''))
            if cid in by_name:
                if c['href'] and by_name[cid]['href'] and c['href'] != by_name[cid]['href'] and \
                        urllib.parse.urlparse(c['href']).netloc == urllib.parse.urlparse(by_name[cid]['href']).netloc:
                    by_name[cid]['href'] = c['href']
            else:
                c['id'] = cid
                c['grupos'] = ['Cuidado de la salud']
                c['padecimientos'] = [page]
                by_name[cid] = c
                catalog.append(c)
    for c in catalog:
        del c['tags']
    print('/* Generado por tools/catalogo.py a partir de chinoin.com/es/catalogo. No editar a mano. */')
    print('window.CHINOIN_CATALOGO = ' + json.dumps(catalog, ensure_ascii=False, indent=1) + ';')


if __name__ == '__main__':
    main()
