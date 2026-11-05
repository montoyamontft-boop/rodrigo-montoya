#!/usr/bin/env python3
"""Builds index.html from page.html.

  {{BULLSVG}}      the logo's bull as a flat SVG, the fallback inside every 3D stage (no WebGL, no script)
  {{BULLDATA}}     bull.json, for vendor/bull3d.js (the three.js sculpture, bundled from src/bull3d.js)
  <script src="vendor/x.js"></script>  inlined, so index.html stands alone
  url("fonts/x.woff2")                 inlined as data: URIs (file:// blocks font files)
Run `npm run bundle` first when src/bull3d.js changes.
"""
import base64
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
B = json.loads((HERE / "bull.json").read_text())


def bull_svg(cls: str) -> str:
    polys = []
    for name, ps in B["cuts"].items():
        polys += [f'<polygon data-cut="{name}" points="{p}"/>' for p in ps]
    polys += [f'<polygon data-cut="chamberete" points="{p}"/>' for p in B["chamberete"]]
    polys += [f'<polygon points="{p}"/>' for p in B["rest"]]
    return f'<svg class="{cls}" viewBox="{B["viewBox"]}" aria-hidden="true" focusable="false">' + "".join(polys) + "</svg>"


# what each photograph shows (alt text and caption); credits come from assets/credits.json
PHOTOS = {
    "band-1": ("Cortes de res con hueso colgados en una cámara de maduración, con etiquetas", "Grasa, hueso y tiempo"),
    "band-2": ("Picaña dorándose bajo una llama al rojo vivo", ""),
    "band-3": ("Piezas de res madurando en una vitrina refrigerada", ""),
    "band-4": ("Tomahawks sobre la parrilla encendida", ""),
    "step-1": ("Pintura de El Greco: un muchacho sopla una brasa para encender una vela", ""),
    "step-2": ("Detalle del marmoleo blanco dentro de un corte de res", ""),
    "step-3": ("Filetes gruesos sobre una parrilla con carbón encendido", ""),
    "visit": ("Picañas asándose sobre un lecho de carbón al rojo", "Picaña sobre el carbón encendido."),
}
CREDITS = {c["slot"]: c for c in json.loads((HERE / "assets/credits.json").read_text())}
PHOTOS = {k: v for k, v in PHOTOS.items() if f"{{{{ALT {k}}}}}" in (HERE / "page.html").read_text(encoding="utf-8")}
SUCURSAL = ""
BANDCAP = "Nuestro rib eye; junto a él, picaña bajo la llama, cortes madurando en cámara y tomahawks sobre la parrilla."

src = (HERE / "page.html").read_text(encoding="utf-8")
for slot, (alt, cap) in PHOTOS.items():
    w, h = CREDITS[slot]["size"]
    src = src.replace("{{ALT %s}}" % slot, alt).replace("{{CAP %s}}" % slot, cap).replace("{{W %s}}" % slot, str(w)).replace("{{H %s}}" % slot, str(h))
src = src.replace("{{SUCURSAL}}", SUCURSAL).replace("{{BANDCAP}}", BANDCAP)
src = src.replace("{{CREDITS}}", "".join(
    f'<li><a href="{c["source"]}" rel="noopener">{c["title"].rsplit(".", 1)[0]}</a>, {c["creator"]} · {c["license"]}</li>' for c in CREDITS.values()))
src = src.replace("{{BULLSVG}}", bull_svg("bull-flat"))
src = src.replace("{{BULLDATA}}", json.dumps(B, separators=(",", ":")))
src = re.sub(r'<script src="vendor/([\w.-]+)"></script>',
             lambda m: "<script>" + (HERE / "vendor" / m.group(1)).read_text(encoding="utf-8").replace("</script", "<\\/script") + "</script>", src)
for f in sorted((HERE / "fonts").glob("*.woff2")):
    src = src.replace(f'url("fonts/{f.name}")', 'url("data:font/woff2;base64,' + base64.b64encode(f.read_bytes()).decode() + '")')
(HERE / "index.html").write_text(src, encoding="utf-8")
print("index.html", len(src) // 1024, "KB")
