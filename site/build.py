#!/usr/bin/env python3
"""Builds index.html from page.html by expanding the bull drawings.

The bull (the white bull of the shop's sign, divided into its cuts) is the page's one motif.
It appears inline several times; this script keeps one source of truth for its geometry.
  {{BULL class="..." style="..."}}   full bull, every cut a separate polygon with class r-<cut>
  {{BULLCLIP id}}                    the silhouette as a <clipPath>
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
VIEWBOX = "50 85 880 490"

CUTS = {
    "diezmillo": "232,176 330,128 420,140 412,266 240,290",
    "pecho": "240,290 412,266 404,396 300,372 258,346",
    "ribeye": "420,140 540,148 536,262 412,266",
    "costilla": "412,266 536,262 532,406 404,396",
    "newyork": "540,148 660,150 660,262 536,262",
    "arrachera": "536,262 660,262 660,400 532,406",
    "picana": "660,150 790,145 845,166 850,262 660,262",
    "bola": "660,262 850,262 845,166 872,202 880,300 864,420 782,396 660,400",
}
CHAMBERETE = [
    "292,362 344,378 338,470 298,470",
    "362,388 404,396 398,470 364,470",
    "760,398 812,402 804,470 768,470",
    "822,406 864,420 852,470 818,470",
]
REST = [  # head, horn, lower legs, tail tuft: not cuts
    "240,290 232,176 205,168 165,172 125,186 92,210 66,244 74,270 108,280 150,286 192,304",
    "205,170 196,140 178,114 152,98 170,126 180,152 182,172",
    "298,470 338,470 334,560 300,560",
    "364,470 398,470 396,560 366,560",
    "768,470 804,470 800,560 770,560",
    "818,470 852,470 848,560 820,560",
    "890,380 912,380 918,426 886,426",
]
TAIL = "M872,200 C904,240 910,310 900,384"


def bull(attrs: str) -> str:
    parts = []
    i = 0
    for name, pts in CUTS.items():
        parts.append(f'<polygon class="cut r-{name}" data-cut="{name}" style="--i:{i}" points="{pts}"/>')
        i += 1
    for pts in CHAMBERETE:
        parts.append(f'<polygon class="cut r-chamberete" data-cut="chamberete" style="--i:{i}" points="{pts}"/>')
    i += 1
    for pts in REST:
        parts.append(f'<polygon class="rest" style="--i:{i}" points="{pts}"/>')
    parts.append(f'<path class="tail" d="{TAIL}"/>')
    parts.append('<circle class="eye" cx="128" cy="222" r="9"/>')
    return (f'<svg {attrs} viewBox="{VIEWBOX}" aria-hidden="true" focusable="false">'
            + "".join(parts) + "</svg>")


def bullclip(cid: str) -> str:
    polys = list(CUTS.values()) + CHAMBERETE + REST
    inner = "".join(f'<polygon points="{p}"/>' for p in polys)
    return f'<clipPath id="{cid}">{inner}<path d="{TAIL}" stroke="#000" stroke-width="12" fill="none"/></clipPath>'


def mini(cut: str) -> str:
    """Small bull for the cut list: one region lit."""
    return bull(f'class="mini" data-lit="{cut}"')


src = (HERE / "page.html").read_text(encoding="utf-8")
src = re.sub(r"\{\{BULL ([^}]*)\}\}", lambda m: bull(m.group(1)), src)
src = re.sub(r"\{\{BULLCLIP (\w+)\}\}", lambda m: bullclip(m.group(1)), src)
src = re.sub(r"\{\{MINI (\w+)\}\}", lambda m: mini(m.group(1)), src)
src = src.replace("{{VIEWBOX}}", VIEWBOX)
# inline the fonts so the page also works opened straight from disk (file:// blocks font files)
import base64
for f in sorted((HERE / "fonts").glob("*.woff2")):
    data = base64.b64encode(f.read_bytes()).decode()
    src = src.replace(f'url("fonts/{f.name}")', f'url("data:font/woff2;base64,{data}")')
(HERE / "index.html").write_text(src, encoding="utf-8")
print("index.html", len(src), "bytes")
