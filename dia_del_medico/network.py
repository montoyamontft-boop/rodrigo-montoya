"""Find the shield's own network in the page-3 photo: bright nodes and the
straight luminous lines that join them. Pulses of light later travel only
along these existing connections.

python network.py BG_4K.png OUT.json [DEBUG.png]
"""
import json, sys
import numpy as np
import cv2
from layout import SHIELD, CROSS


def detect(bg):
    """bg: page-3 plate (any scale, RGB uint8). Returns nodes (pt) and edges."""
    k = bg.shape[1] / 1920.0
    im = cv2.resize(bg, (1920, 1080), interpolation=cv2.INTER_AREA).astype(np.float32)
    L = im @ np.array([0.30, 0.55, 0.15], np.float32)
    hp = L - cv2.GaussianBlur(L, (0, 0), 4)
    yy, xx = np.mgrid[0:1080, 0:1920].astype(np.float32)
    cx, cy = SHIELD["center"]
    rx, ry = SHIELD["radii"]
    inside = ((xx - cx) / (rx * 0.92)) ** 2 + ((yy - cy) / (ry * 0.92)) ** 2 < 1
    v0, h0 = CROSS["v"], CROSS["h"]
    pad = 10
    cross = (((xx > v0[0] - pad) & (xx < v0[2] + pad) & (yy > v0[1] - pad) & (yy < v0[3] + pad)) |
             ((xx > h0[0] - pad) & (xx < h0[2] + pad) & (yy > h0[1] - pad) & (yy < h0[3] + pad)))
    sm = cv2.GaussianBlur(L, (0, 0), 1.6)
    peak = (sm >= cv2.dilate(sm, np.ones((13, 13), np.uint8))) & inside & ~cross
    hpp = cv2.GaussianBlur(hp, (0, 0), 1.2)
    cand = np.argwhere(peak & (hpp > 14))
    vals = hpp[cand[:, 0], cand[:, 1]]
    order = np.argsort(-vals)
    nodes = []
    for i in order:
        y, x = cand[i]
        if all((x - a) ** 2 + (y - b) ** 2 > 18 ** 2 for a, b in nodes):
            nodes.append((int(x), int(y)))
    # a connection exists where the high-pass stays bright all along the segment
    lin = np.maximum(cv2.GaussianBlur(hp, (0, 0), 0.8), 0)
    edges = []
    for i, (x0, y0) in enumerate(nodes):
        for j in range(i + 1, len(nodes)):
            x1, y1 = nodes[j]
            d = np.hypot(x1 - x0, y1 - y0)
            if d < 35 or d > 190:
                continue
            ts = np.linspace(0.12, 0.88, int(d / 3))
            px = x0 + (x1 - x0) * ts
            py = y0 + (y1 - y0) * ts
            # best of a 1px perpendicular jitter (lines are ~1-2 px wide)
            nx, ny = -(y1 - y0) / d, (x1 - x0) / d
            best = 0
            for o in (-1.2, 0, 1.2):
                s = cv2.remap(lin, (px + nx * o).astype(np.float32)[None], (py + ny * o).astype(np.float32)[None],
                              cv2.INTER_LINEAR)[0]
                best = max(best, np.percentile(s, 15))
            if best > 4.5:
                edges.append((i, j, float(d), float(best)))
    return [(x, y) for x, y in nodes], [(i, j) for i, j, _, _ in edges]


if __name__ == "__main__":
    bg = cv2.cvtColor(cv2.imread(sys.argv[1]), cv2.COLOR_BGR2RGB)
    nodes, edges = detect(bg)
    print(len(nodes), "nodes", len(edges), "edges")
    json.dump(dict(nodes=nodes, edges=edges), open(sys.argv[2], "w"))
    if len(sys.argv) > 3:
        im = cv2.resize(bg, (1920, 1080), interpolation=cv2.INTER_AREA)
        im = (im * 0.6).astype(np.uint8)
        for i, j in edges:
            cv2.line(im, nodes[i], nodes[j], (255, 60, 60), 1, cv2.LINE_AA)
        for x, y in nodes:
            cv2.circle(im, (x, y), 3, (255, 255, 0), -1)
        cv2.imwrite(sys.argv[3], cv2.cvtColor(im[100:1000, 0:900], cv2.COLOR_RGB2BGR))
