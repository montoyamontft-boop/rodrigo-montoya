"""Empaqueta el sitio en un solo HTML autocontenido para vista previa.

Uso: python3 tools/bundle.py salida.html
Incrusta CSS, JS y el logo; el Portal Médico se abre como capa dentro de la misma página.
"""
import base64
import io
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def read(p):
    return (ROOT / p).read_text(encoding='utf-8')


css = read('css/styles.css')
MIME = {'.png': 'image/png', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.jpg': 'image/jpeg'}


def preview_bytes(path):
    """Para la vista previa las fotos van más ligeras (el sitio real usa las originales)."""
    if path.suffix != '.webp':
        return path.read_bytes()
    try:
        from PIL import Image
    except ImportError:
        return path.read_bytes()
    im = Image.open(path)
    limit = 1000 if im.width > 1500 else 640
    if im.width <= limit and path.stat().st_size < 60_000:
        return path.read_bytes()
    im.thumbnail((limit, limit * 4))
    buf = io.BytesIO()
    im.save(buf, 'WEBP', quality=72, method=4)
    return buf.getvalue()


def data_uris(text):
    """Sustituye cada ruta assets/… por la imagen incrustada."""
    def sub(m):
        path = ROOT / m.group(0)
        if not path.exists():
            return m.group(0)
        return f'data:{MIME[path.suffix]};base64,' + base64.b64encode(preview_bytes(path)).decode()
    return re.sub(r'assets/[A-Za-z0-9_./-]+\.(?:png|webp|svg|jpg)', sub, text)


def inline(page):
    page = page.replace('<link rel="stylesheet" href="css/styles.css">', f'<style>\n{css}\n</style>')
    return data_uris(page)


# Portal Médico: los enlaces de regreso navegan la página contenedora.
portal = inline(read('portal-medico.html'))
portal = re.sub(r'href="index\.html(#/[^"]*)?"',
                lambda m: f'href="#" onclick="parent.location.hash=\'{m.group(1) or "#/"}\';return false"', portal)

index = inline(read('index.html'))
scripts = ('<script src="js/data.js"></script>\n  <script src="js/catalogo.js"></script>\n'
           '  <script src="js/fichas.js"></script>\n  <script src="js/veterinaria.js"></script>\n'
           '  <script src="js/marcas.js"></script>\n  <script src="js/app.js"></script>')
overlay = f'''<script>
  (() => {{
    // Abre el Portal Médico como capa a pantalla completa.
    const frame = document.createElement('iframe');
    frame.title = 'Portal Médico';
    frame.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;border:0;z-index:200;background:#fff;display:none';
    frame.srcdoc = {json.dumps(portal).replace('</', '<\\/')};
    document.body.appendChild(frame);
    let last = '#/';
    const sync = (e) => {{
      if (location.hash === '#/portal-medico') {{
        frame.style.display = 'block';
        document.body.style.overflow = 'hidden';
        if (e) e.stopImmediatePropagation();
        return true;
      }}
      frame.style.display = 'none';
      document.body.style.overflow = '';
      last = location.hash;
    }};
    addEventListener('hashchange', sync, true);
    if (sync()) history.replaceState(null, '', last);
  }})();
  </script>'''
app = read('js/app.js').replace("'portal-medico.html'", "'#/portal-medico'").replace('href="portal-medico.html#acceso"', 'href="#/portal-medico"').replace('href="portal-medico.html"', 'href="#/portal-medico"')
data = data_uris(read('js/data.js').replace("'portal-medico.html'", "'#/portal-medico'"))
catalogo = data_uris(read('js/catalogo.js'))
vet = data_uris(read('js/veterinaria.js'))
marcas = data_uris(read('js/marcas.js'))
fichas = read('js/fichas.js')
app = data_uris(app)
js = '\n'.join(f'<script>\n{x}\n</script>' for x in (data, catalogo, fichas, vet, marcas, app))
index = index.replace(scripts, f'{js}\n  {overlay}')

out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'chinoin-preview.html')
out.write_text(index, encoding='utf-8')
print(out, f'{out.stat().st_size / 1024:.0f} KB')
