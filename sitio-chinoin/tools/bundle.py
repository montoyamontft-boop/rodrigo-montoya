"""Empaqueta el sitio en un solo HTML autocontenido para vista previa.

Uso: python3 tools/bundle.py salida.html
Incrusta CSS, JS y el logo; el Portal Médico se abre como capa dentro de la misma página.
"""
import base64
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def read(p):
    return (ROOT / p).read_text(encoding='utf-8')


logo = 'data:image/png;base64,' + base64.b64encode((ROOT / 'assets/chinoin-logo.png').read_bytes()).decode()
css = read('css/styles.css')


def inline(page):
    page = page.replace('<link rel="stylesheet" href="css/styles.css">', f'<style>\n{css}\n</style>')
    return page.replace('assets/chinoin-logo.png', logo)


# Portal Médico: los enlaces de regreso navegan la página contenedora.
portal = inline(read('portal-medico.html'))
portal = portal.replace('href="index.html"', 'href="#/" onclick="parent.location.hash=\'#/\';return false"')

index = inline(read('index.html'))
scripts = '<script src="js/data.js"></script>\n  <script src="js/app.js"></script>'
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
app = read('js/app.js').replace("'portal-medico.html'", "'#/portal-medico'").replace('href="portal-medico.html"', 'href="#/portal-medico"')
data = read('js/data.js').replace("'portal-medico.html'", "'#/portal-medico'")
index = index.replace(scripts, f'<script>\n{data}\n</script>\n  <script>\n{app}\n</script>\n  {overlay}')

out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'chinoin-preview.html')
out.write_text(index, encoding='utf-8')
print(out, f'{out.stat().st_size / 1024:.0f} KB')
