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


def mini(cut: str) -> str:
    """Small bull for the cut list: one region lit."""
    return bull(f'class="mini" data-lit="{cut}"')


src = (HERE / "page.html").read_text(encoding="utf-8")
src = re.sub(r"\{\{BULL ([^}]*)\}\}", lambda m: bull(m.group(1)), src)
src = re.sub(r"\{\{BULLCLIP (\w+)\}\}", lambda m: bullclip(m.group(1)), src)
src = re.sub(r"\{\{BULLCLIPOBB (\w+)\}\}", lambda m: bullclip_obb(m.group(1)), src)
src = re.sub(r"\{\{MINI (\w+)\}\}", lambda m: mini(m.group(1)), src)
src = src.replace("{{VIEWBOX}}", VIEWBOX)
_vb = VIEWBOX.split()
src = src.replace("{{ASPECT}}", f"{_vb[2]} / {_vb[3]}")
# inline the fonts so the page also works opened straight from disk (file:// blocks font files)
import base64
for f in sorted((HERE / "fonts").glob("*.woff2")):
    data = base64.b64encode(f.read_bytes()).decode()
    src = src.replace(f'url("fonts/{f.name}")', f'url("data:font/woff2;base64,{data}")')
(HERE / "index.html").write_text(src, encoding="utf-8")
print("index.html", len(src), "bytes")
