#!/usr/bin/env python3
"""Traces the bull of the shop's logo (assets/logo.png) into the cut polygons the page draws.

The logo's own facets (head, dewlap, shoulder, belly, haunch) are kept as they are; the larger
facets are split further along a few straight cuts so every butcher's cut on the page has its
region. Output: bull.json, read by build.py.  Needs: pip install opencv-python-headless shapely
"""
import json
from pathlib import Path

import cv2
import numpy as np
from shapely.geometry import LineString, Polygon, box
from shapely.ops import unary_union

HERE = Path(__file__).parent
S = 4                     # trace at 4x the logo's pixels
OX, OY = 60 * S, 30 * S   # crop origin: coordinates below are in this cropped, 4x frame
GAP = 13                  # width of the extra cuts, matching the logo's own facet lines

img = cv2.imread(str(HERE / "assets/logo.png"), cv2.IMREAD_UNCHANGED)
g = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2GRAY)
g = cv2.resize(g, None, fx=S, fy=S, interpolation=cv2.INTER_CUBIC)
mask = (g > 140).astype(np.uint8)
mask[184 * S:, :] = 0     # everything from the rule under the bull down is lettering
mask[:, : 60 * S] = 0

n, lab, stats, cent = cv2.connectedComponentsWithStats(mask, 8)


def poly_of(ids):
    m = np.isin(lab, ids).astype(np.uint8) * 255
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    polys = []
    for c in cs:
        if cv2.contourArea(c) < 150:
            continue
        c = cv2.approxPolyDP(c, 1.6, True)[:, 0, :].astype(float)
        c[:, 0] -= OX
        c[:, 1] -= OY
        polys.append(Polygon(c).buffer(0))
    return unary_union(polys)


# components by position (centroids in the cropped frame), independent of label order
def comp_at(x, y):
    i = lab[int(y + OY), int(x + OX)]
    assert i, (x, y)
    return i


HORN_L, HORN_R = comp_at(120, 120), comp_at(282, 125)
HEAD, DEWLAP = comp_at(200, 220), comp_at(190, 380)
SHOULDER, BELLY, HAUNCH = comp_at(280, 440), comp_at(420, 520), comp_at(560, 480)

head = poly_of([HEAD])
horns = poly_of([HORN_L, HORN_R])
dewlap = poly_of([DEWLAP])
shoulder = poly_of([SHOULDER])
belly = poly_of([BELLY])
haunch = poly_of([HAUNCH])


def cut(shape, *lines):
    """Split a facet along straight cuts, leaving a gap like the logo's lines."""
    knife = unary_union([LineString(l).buffer(GAP / 2, cap_style=2) for l in lines])
    parts = shape.difference(knife)
    return sorted(getattr(parts, "geoms", [parts]), key=lambda p: -p.area)


def pick(parts, x, y):
    from shapely.geometry import Point
    pt = Point(x, y)
    return min(parts, key=lambda p: p.distance(pt))


# shoulder: chuck at the front, rib eye along the back, the front leg's shank below
sh = cut(shoulder, [(100, 560), (440, 475)], [(255, 200), (350, 540)])
diezmillo = pick(sh, 240, 450)
ribeye = pick(sh, 330, 350)
front_leg = pick(sh, 185, 595)

# belly: loin along the back, short ribs in the middle, the skirt at the bottom
be = cut(belly, [(280, 505), (600, 435)], [(230, 575), (620, 548)])
newyork = pick(be, 440, 430)
costilla = pick(be, 430, 520)
arrachera = pick(be, 430, 595)
belly_legs = []

# haunch: the tail, the rump cap on top, the round, the hind shank
tail_box = box(560, 300, 700, 470)
tail = haunch.intersection(tail_box)
rump = haunch.difference(tail_box.buffer(GAP / 2))
ha = cut(rump, [(455, 445), (580, 470)], [(540, 560), (640, 545)])
picana = pick(ha, 500, 425)
bola = pick(ha, 530, 510)
hind_leg = pick(ha, 600, 590)

CUTS = {
    "diezmillo": diezmillo, "pecho": dewlap, "ribeye": ribeye, "costilla": costilla,
    "newyork": newyork, "arrachera": arrachera, "picana": picana, "bola": bola,
}
CHAMBERETE = [front_leg, hind_leg]
REST = [head, horns, tail] + belly_legs


def pts(geom):
    geoms = getattr(geom, "geoms", [geom])
    out = []
    for gm in geoms:
        if gm.area < 60:
            continue
        gm = gm.simplify(0.8)
        out.append(" ".join(f"{x:.0f},{y:.0f}" for x, y in list(gm.exterior.coords)[:-1]))
    return out


allg = unary_union(list(CUTS.values()) + CHAMBERETE + REST)
x0, y0, x1, y1 = allg.bounds
data = {
    "viewBox": f"{x0 - 6:.0f} {y0 - 6:.0f} {x1 - x0 + 12:.0f} {y1 - y0 + 12:.0f}",
    "cuts": {k: pts(v) for k, v in CUTS.items()},
    "chamberete": [p for g_ in CHAMBERETE for p in pts(g_)],
    "rest": [p for g_ in REST for p in pts(g_)],
    "eye": None,
}
(HERE / "bull.json").write_text(json.dumps(data, indent=1))
print(data["viewBox"], {k: len(v) for k, v in data["cuts"].items()}, len(data["chamberete"]), len(data["rest"]))
