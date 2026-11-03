#!/usr/bin/env python3
"""Builds index.html from page.html by expanding the bull drawings.

The bull (the bull of the shop's logo, its facets divided into cuts) is the page's one motif.
It appears inline several times; this script keeps one source of truth for its geometry.
  {{BULL class="..." style="..."}}   full bull, every cut a separate polygon with class r-<cut>
  {{BULLCLIP id}}                    the silhouette as a <clipPath>
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
# The geometry is traced from the logo's own bull by trace_logo.py (its facets, split into cuts).
_B = json.loads((HERE / "bull.json").read_text())
VIEWBOX = _B["viewBox"]
CUTS = _B["cuts"]            # cut name -> list of polygons
CHAMBERETE = _B["chamberete"]
REST = _B["rest"]            # horns, head, tail: not cuts


def bull(attrs: str) -> str:
    parts = []
    i = 0
    for name, polys in CUTS.items():
        for pts in polys:
            parts.append(f'<polygon class="cut r-{name}" data-cut="{name}" style="--i:{i}" points="{pts}"/>')
        i += 1
    for pts in CHAMBERETE:
        parts.append(f'<polygon class="cut r-chamberete" data-cut="chamberete" style="--i:{i}" points="{pts}"/>')
    i += 1
    for pts in REST:
        parts.append(f'<polygon class="rest" style="--i:{i}" points="{pts}"/>')
    return (f'<svg {attrs} viewBox="{VIEWBOX}" aria-hidden="true" focusable="false">'
            + "".join(parts) + "</svg>")


def _all_polys():
    return [p for polys in CUTS.values() for p in polys] + CHAMBERETE + REST


def bullclip(cid: str) -> str:
    inner = "".join(f'<polygon points="{p}"/>' for p in _all_polys())
    return f'<clipPath id="{cid}">{inner}</clipPath>'


def bullclip_obb(cid: str) -> str:
    """The silhouette in objectBoundingBox units, for clipping an HTML box of the bull's proportions."""
    x0, y0, w, h = (float(v) for v in VIEWBOX.split())
    def norm(pts):
        out = []
        for pair in pts.split():
            x, y = (float(v) for v in pair.split(","))
            out.append(f"{(x - x0) / w:.4f},{(y - y0) / h:.4f}")
        return " ".join(out)
    inner = "".join(f'<polygon points="{norm(p)}"/>' for p in _all_polys())
    return f'<clipPath id="{cid}" clipPathUnits="objectBoundingBox">{inner}</clipPath>'


def _area_centroid(pts):
    xy = [tuple(float(v) for v in p.split(",")) for p in pts.split()]
    a = cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(xy, xy[1:] + xy[:1]):
        f = x0 * y1 - x1 * y0
        a += f; cx += (x0 + x1) * f; cy += (y0 + y1) * f
    a *= 0.5
    return abs(a), cx / (6 * a), cy / (6 * a)


def cut_centres():
    """Centre of each cut's largest facet, in viewBox units."""
    out = {}
    groups = dict(CUTS); groups["chamberete"] = CHAMBERETE
    for name, polys in groups.items():
        a, x, y = max(_area_centroid(p) for p in polys)
        out[name] = (x, y)
    return out


NAMES = {"diezmillo": "Diezmillo", "pecho": "Pecho", "ribeye": "Rib eye", "costilla": "Costilla",
         "newyork": "New York", "arrachera": "Arrachera", "picana": "Picaña", "bola": "Bola",
         "chamberete": "Chamberete"}


def labels() -> str:
    x0, y0, w, h = (float(v) for v in VIEWBOX.split())
    html = []
    for name, (x, y) in cut_centres().items():
        html.append(f'<a class="desp-label" href="#c-{name}" data-cut="{name}" style="left:{(x - x0) / w * 100:.2f}%;top:{(y - y0) / h * 100:.2f}%"><span>{NAMES[name]}</span></a>')
    return "".join(html)


def explode_data() -> str:
    """Per-cut push away from the bull's centre, for the despiece scene."""
    x0, y0, w, h = (float(v) for v in VIEWBOX.split())
    cx, cy = x0 + w * 0.5, y0 + h * 0.55
    K = 0.62
    d = {n: [round((x - cx) * K, 1), round((y - cy) * K, 1)] for n, (x, y) in cut_centres().items()}
    d["rest"] = [round((x0 + w * 0.3 - cx) * K * 0.7, 1), round((y0 + h * 0.2 - cy) * K * 0.7, 1)]
    return json.dumps(d)


def mini(cut: str) -> str:
    """Small bull for the cut list: one region lit."""
    return bull(f'class="mini" data-lit="{cut}"')


src = (HERE / "page.html").read_text(encoding="utf-8")
src = re.sub(r"\{\{BULL ([^}]*)\}\}", lambda m: bull(m.group(1)), src)
src = re.sub(r"\{\{BULLCLIP (\w+)\}\}", lambda m: bullclip(m.group(1)), src)
src = re.sub(r"\{\{BULLCLIPOBB (\w+)\}\}", lambda m: bullclip_obb(m.group(1)), src)
src = src.replace("{{LABELS}}", labels()).replace("{{EXPLODE}}", explode_data())
src = re.sub(r"\{\{MINI (\w+)\}\}", lambda m: mini(m.group(1)), src)
src = src.replace("{{VIEWBOX}}", VIEWBOX)
_vb = VIEWBOX.split()
src = src.replace("{{ASPECT}}", f"{_vb[2]} / {_vb[3]}")
# inline the vendored scripts and styles so index.html stands alone
src = re.sub(r'<script src="vendor/([\w.-]+)"></script>', lambda m: "<script>" + (HERE / "vendor" / m.group(1)).read_text(encoding="utf-8").replace("</script", "<\\/script") + "</script>", src)
src = re.sub(r'<link rel="stylesheet" href="vendor/([\w.-]+)">', lambda m: "<style>" + (HERE / "vendor" / m.group(1)).read_text(encoding="utf-8") + "</style>", src)
# inline the fonts so the page also works opened straight from disk (file:// blocks font files)
import base64
for f in sorted((HERE / "fonts").glob("*.woff2")):
    data = base64.b64encode(f.read_bytes()).decode()
    src = src.replace(f'url("fonts/{f.name}")', f'url("data:font/woff2;base64,{data}")')
(HERE / "index.html").write_text(src, encoding="utf-8")
print("index.html", len(src), "bytes")
