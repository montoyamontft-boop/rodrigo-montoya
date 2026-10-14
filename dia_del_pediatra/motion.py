"""Día del Pediatra - animation and encoding.

usage:
  python motion.py LAYERS_DIR OUT.mp4 [--scale 1.0] [--workers 3] [--crf 14]
  python motion.py LAYERS_DIR --stills DIR --times 1.0,2.5 [--scale 0.5]

scale 1.0 -> 3840x2160, 0.5 -> 1920x1080. Constant 30 fps, no audio.

Every element comes from the PDF (build.py). The photos (with their arcs,
white rings and translucent diagonals flattened in) are only moved rigidly,
masked or re-timed - never redrawn; texts, cards, plecas, balloon, outlines
and logos are the original vector layers.
"""
import argparse, heapq, json, math, os, subprocess, sys
import numpy as np
import cv2
from PIL import Image
from skimage.morphology import skeletonize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from layout import ARC, ARC_BAND, RINGS, DRAW_FROM, BALLOON_TIP  # noqa: E402

FPS = 30
cv2.setNumThreads(1)


# ------------------------------------------------------------------ easing
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


EASE = {
    "lin": lambda p: p,
    "outQuint": lambda p: 1 - (1 - p) ** 5,
    "outQuart": lambda p: 1 - (1 - p) ** 4,
    "outCubic": lambda p: 1 - (1 - p) ** 3,
    "outExpo": lambda p: 1.0 if p >= 1 else 1 - 2 ** (-10 * p),
    "inOutCubic": lambda p: 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2,
    "inOutQuart": lambda p: 8 * p ** 4 if p < 0.5 else 1 - (-2 * p + 2) ** 4 / 2,
    "inOutSine": lambda p: -(math.cos(math.pi * p) - 1) / 2,
    "inCubic": lambda p: p ** 3,
    # soft arrival with a ~3 % overshoot - lively, never a bounce
    "outBack": lambda p: 1 + 2.1 * (p - 1) ** 3 + 1.1 * (p - 1) ** 2,
}


def ease(name, p):
    return EASE[name](clamp(p))


def sstep(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


# ------------------------------------------------------------------ timeline
# (name, start, duration). The next scene starts while the previous one is
# still on screen: it is revealed over it during REVEAL seconds.
SCENES = [("s1", 0.0, 9.3), ("s2", 7.9, 7.5), ("s3", 14.0, 12.0)]
REVEAL = {"s1": 2.2, "s2": 2.0, "s3": 1.5}
TOTAL = 26.0
EXIT = dict(lead=0.35, stagger=0.07, d=0.55, dx=22, dy=0)   # outgoing elements, pt

# Element choreography (scene-local seconds).
CHOREO = {
    "s1": {
        "line": dict(kind="draw", t=1.90, d=0.9),
        "dashes": dict(kind="fade", t=2.65, d=0.3, dx=-14),
        "contour": dict(kind="draw", t=1.95, d=1.1, ease="inOutCubic"),
        "surface": dict(kind="slide", t=2.55, d=0.75, dx=-16, dy=-15),
        "pequenos": dict(kind="slide_wipe", t=2.80, d=0.85, dx=-16, dy=-15),
        "grandes": dict(kind="glyphs", t=3.85, d=0.62, stagger=0.045),
    },
    "s2": {
        "octubre": dict(kind="rise", t=1.65, d=0.75),
        "pleca": dict(kind="hwipe", t=2.25, d=0.8),
        "dia": dict(kind="hwipe", t=2.37, d=0.8, dx=-10),
        "outline": dict(kind="draw", t=2.65, d=1.15, ease="inOutCubic", dx=14, dy=-8),
    },
    "s3": {
        "balloon": dict(kind="grow", t=1.25, d=0.85, s0=0.08),
        "outline": dict(kind="draw", t=1.55, d=1.0, ease="inOutCubic"),
        "r1": dict(kind="rise", t=2.35, d=0.7),
        "r2": dict(kind="rise", t=2.75, d=0.7),
        "r3": dict(kind="rise", t=3.15, d=0.7),
        "r4": dict(kind="rise", t=3.55, d=0.75),
        "zymir": dict(kind="fade", t=4.6, d=0.6, dy=14),
        "sunderin": dict(kind="fade", t=4.75, d=0.6, dy=14),
        "gabirol": dict(kind="fade", t=4.9, d=0.6, dy=14),
        "benel": dict(kind="fade", t=5.05, d=0.6, dy=14),
        "legend": dict(kind="fade", t=5.5, d=0.7),
    },
}

# Background depth: photo / near plane settles from a slight push-in, the
# pastel far plane drifts along the translucent diagonals; rings expand.
DEPTH = {
    "s1": dict(near_scale=1.03, near_off=(-6, 4), far_off=(-18, 18), ring_s0=0.9),
    "s2": dict(near_scale=1.03, near_off=(6, 4), far_off=(-16, 16), ring_s0=0.9),
    "s3": dict(near_scale=1.035, near_off=(0, 6), far_off=(-14, 14), ring_s0=0.9),
}
# A soft wave of presence travels outward across the rings now and then
RIPPLES = {"s1": [0.9, 4.6, 7.4], "s2": [0.6, 3.1, 5.9], "s3": [0.5, 3.8, 6.4, 9.0]}
RIPPLE_SPEED = 260.0    # pt / s
RIPPLE_WIDTH = 55.0     # pt
# Groups made of disjoint fills of one colour that meet edge to edge (the
# balloon's body and its side strips): their first slot becomes the union of
# all pieces (coverages add up exactly for disjoint shapes), so no
# anti-aliasing seam shows along the shared edges - in the PDF the purple
# outline hides it, here the balloon appears before its outline. The later
# pieces are kept only where the named layer (the outline) passes between
# them, which preserves the PDF's paint order.
SEAMLESS = {"s3": [("balloon", "outline")]}


# ------------------------------------------------------------------ layers
class Layer:
    def __init__(self, group, K, A, x, y):
        self.group, self.K, self.A, self.x, self.y = group, K, A, int(x), int(y)
        self.h, self.w = A.shape[:2]
        self.param = None
        self.anchor = None

    @classmethod
    def load(cls, d, L, scale):
        F = np.asarray(Image.open(os.path.join(d, L["file"] + "_F.png")), np.float32) / 255
        A = np.asarray(Image.open(os.path.join(d, L["file"] + "_A.png")), np.float32)
        x, y = L["x"] * scale, L["y"] * scale
        if scale != 1.0:
            fx, fy = math.floor(x), math.floor(y)
            w = int(math.ceil(x + L["w"] * scale)) - fx + 1
            h = int(math.ceil(y + L["h"] * scale)) - fy + 1
            M = np.float32([[scale, 0, x - fx], [0, scale, y - fy]])
            F = 1 - cv2.warpAffine(1 - F, M, (w, h), flags=cv2.INTER_AREA)
            A = cv2.warpAffine(A, M, (w, h), flags=cv2.INTER_AREA)
            x, y = fx, fy
        return cls(L["group"], 1 - F, A, x, y)


def composite(rgb, L, st, mask_fn=None):
    """rgb += m * (A - K * rgb), the layer transformed by st."""
    m = st["m"]
    if m <= 1e-3:
        return
    H, W = rgb.shape[:2]
    s, dx, dy = st.get("s", 1.0), st.get("dx", 0.0), st.get("dy", 0.0)
    ax, ay = st.get("anchor", (0, 0))
    ox = s * (L.x - ax) + ax + dx
    oy = s * (L.y - ay) + ay + dy
    ident = abs(s - 1) < 1e-6 and abs(ox - round(ox)) < 1e-4 and abs(oy - round(oy)) < 1e-4
    if ident:
        X0, Y0 = int(round(ox)), int(round(oy))
        X1, Y1 = X0 + L.w, Y0 + L.h
    else:
        X0, Y0 = math.floor(ox), math.floor(oy)
        X1, Y1 = math.ceil(ox + s * L.w) + 1, math.ceil(oy + s * L.h) + 1
    clip = st.get("clip")
    rx0, ry0, rx1, ry1 = max(X0, 0), max(Y0, 0), min(X1, W), min(Y1, H)
    if clip:
        rx0, ry0 = max(rx0, int(clip[0])), max(ry0, int(clip[1]))
        rx1, ry1 = min(rx1, int(math.ceil(clip[2]))), min(ry1, int(math.ceil(clip[3])))
    if rx1 <= rx0 or ry1 <= ry0:
        return
    Pc = None
    if ident:
        sx, sy = rx0 - X0, ry0 - Y0
        sl = (slice(sy, sy + ry1 - ry0), slice(sx, sx + rx1 - rx0))
        Kc, Ac = L.K[sl], L.A[sl]
        if L.param is not None:
            Pc = L.param[sl]
    else:
        M = np.float32([[s, 0, ox - rx0], [0, s, oy - ry0]])
        size = (rx1 - rx0, ry1 - ry0)
        Kc = cv2.warpAffine(L.K, M, size, flags=cv2.INTER_CUBIC)
        Ac = cv2.warpAffine(L.A, M, size, flags=cv2.INTER_CUBIC)
        if L.param is not None:
            Pc = cv2.warpAffine(L.param, M, size, flags=cv2.INTER_LINEAR, borderValue=1e9)
    f = m
    if mask_fn is not None:
        f = (mask_fn(rx0, ry0, rx1, ry1, Pc) * m)[..., None]
    reg = rgb[ry0:ry1, rx0:rx1]
    reg += f * (Ac - Kc * reg)


def draw_param(layers, start, k):
    """Arc length (pt), along the drawn shape itself, for every pixel of the
    given layers: skeleton of their union, geodesic distance from the
    skeleton point nearest to `start`, carried to each pixel by its nearest
    skeleton point. Closed shapes grow both ways from the start; separate
    pieces follow one another."""
    x0 = min(L.x for L in layers); y0 = min(L.y for L in layers)
    x1 = max(L.x + L.w for L in layers); y1 = max(L.y + L.h for L in layers)
    cov = np.zeros((y1 - y0, x1 - x0), np.float32)
    for L in layers:
        sl = (slice(L.y - y0, L.y - y0 + L.h), slice(L.x - x0, L.x - x0 + L.w))
        cov[sl] = np.maximum(cov[sl], L.K.max(-1))
    mask = cov > 0.25
    sk = skeletonize(mask)
    pts = np.argwhere(sk)
    idx = -np.ones(sk.shape, np.int64)
    idx[pts[:, 0], pts[:, 1]] = np.arange(len(pts))
    dist = np.full(len(pts), np.inf)
    sx, sy = start[0] * k - x0, start[1] * k - y0
    done = np.zeros(len(pts), bool)
    offset = 0.0
    last = np.array([sy, sx])
    nb = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while not done.all():
        rest = np.nonzero(~done)[0]
        d2 = ((pts[rest] - last) ** 2).sum(1)
        s0 = rest[np.argmin(d2)]
        offset += math.sqrt(d2.min()) if offset > 0 else 0.0
        dist[s0] = offset
        heap = [(offset, s0)]
        comp = []
        while heap:
            dd, i = heapq.heappop(heap)
            if done[i] or dd > dist[i]:
                continue
            done[i] = True
            comp.append(i)
            y, x = pts[i]
            for oy, ox in nb:
                yy, xx = y + oy, x + ox
                if 0 <= yy < sk.shape[0] and 0 <= xx < sk.shape[1]:
                    j = idx[yy, xx]
                    if j >= 0 and not done[j]:
                        nd = dd + (1.4142 if oy and ox else 1.0)
                        if nd < dist[j]:
                            dist[j] = nd
                            heapq.heappush(heap, (nd, j))
        far = comp[int(np.argmax(dist[comp]))]
        offset = dist[far]
        last = pts[far]
    # carry the skeleton distance to every pixel of the shape
    src = np.ones(sk.shape, np.uint8)
    src[sk] = 0
    _, lab = cv2.distanceTransformWithLabels(src, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    # label -> skeleton point: labels are numbered in scan order of the zero pixels
    zy, zx = np.nonzero(src == 0)
    lab_to_pt = np.zeros(lab.max() + 1, np.int64)
    lab_to_pt[lab[zy, zx]] = idx[zy, zx]
    P = (dist[lab_to_pt[lab]] / k).astype(np.float32)
    for L in layers:
        L.param = np.ascontiguousarray(P[L.y - y0:L.y - y0 + L.h, L.x - x0:L.x - x0 + L.w])
    return float(dist.max() / k)


# ------------------------------------------------------------------ scene
class Scene:
    def __init__(self, name, layers_dir, man, glyphs, scale):
        self.name, self.scale = name, scale
        self.k = k = 2.0 * scale
        bg = cv2.cvtColor(cv2.imread(os.path.join(layers_dir, f"{name}_bg.png")), cv2.COLOR_BGR2RGB)
        if scale != 1.0:
            bg = cv2.resize(bg, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        self.H, self.W = H, W = bg.shape[:2]
        self.bg = bg.astype(np.float32)
        ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
        self.gx, self.gy = xs, ys
        X, Y = xs / k, ys / k
        self.dur = {n: d for n, _, d in SCENES}[name]
        names = [n for n, _, _ in SCENES]
        i = names.index(name)
        self.exit_at = SCENES[i + 1][1] - SCENES[i][1] if i + 1 < len(SCENES) else None
        order = sorted(CHOREO[name], key=lambda g: CHOREO[name][g]["t"])
        self.rank = {g: j for j, g in enumerate(order)}

        # near plane: the photo inside its arc (s1, s2) / the bear and hands (s3)
        if name in ARC:
            cx, cy, R = ARC[name]
            r = np.hypot(X - cx, Y - cy)
            self.r_arc = r
            u = np.clip((r - (R + 6)) / 150.0, 0, 1)
            self.wnear = (1 - sstep(u)).astype(np.float32)
            self.near_anchor = (cx * k, cy * k)
            # what stands in for the photo before it is revealed: the pastel
            # around it, softly carried inwards (normalised blur) - no new image
            outside = r > R + 30
            # each row takes the pastel found just outside the arc on that row
            wash = self.bg.copy()
            for yy in range(H):
                cols = np.nonzero(outside[yy])[0]
                if len(cols):
                    x_edge = cols[0]
                    ref = self.bg[yy, x_edge:x_edge + int(20 * k)].mean(0)
                    wash[yy, :x_edge] = ref
            self.wash = cv2.GaussianBlur(wash, (0, 0), 40 * k)
        else:
            u = np.clip((1060 - X) / 160.0, 0, 1)
            self.wnear = (1 - sstep(u)).astype(np.float32)
            self.near_anchor = (1450 * k, 560 * k)
            self.r_arc = None
        # ring families: radial weight (1 inside the family, 0 a little beyond)
        self.rings = []
        hp = np.maximum(self.bg - cv2.GaussianBlur(self.bg, (0, 0), 4 * k), 0)
        for (c, rmax) in RINGS[name]:
            rr = np.hypot(X - c[0], Y - c[1])
            wr = (1 - sstep((rr - rmax) / 120.0)) * (1 - self.wnear)
            self.rings.append(dict(c=(c[0] * k, c[1] * k), r=rr.astype(np.float32),
                                   w=wr.astype(np.float32), rmax=rmax))
        ring_w = np.zeros((H, W), np.float32)
        for R_ in self.rings:
            ring_w = np.maximum(ring_w, R_["w"])
        # the white ring strokes themselves (fine bright detail inside ring zones)
        self.ring_hp = (hp.max(-1) * ring_w).astype(np.float32)
        self.ring_soft = cv2.GaussianBlur(self.bg, (0, 0), 6 * k)

        # layers
        self.layers = []
        for L in man:
            if L["group"] == "bg":
                continue
            self.layers.append(Layer.load(layers_dir, L, scale))
        self.split_glyphs(glyphs)
        self.boxes = {}
        for L in self.layers:
            b = self.boxes.get(L.group)
            nb = [L.x, L.y, L.x + L.w, L.y + L.h]
            self.boxes[L.group] = nb if b is None else [min(b[0], nb[0]), min(b[1], nb[1]),
                                                        max(b[2], nb[2]), max(b[3], nb[3])]
        self.layers_pdf = list(self.layers)
        self.seamless_until = -1.0
        for g, between in SEAMLESS.get(name, []):
            cb = CHOREO[name][between]
            self.seamless_until = max(self.seamless_until, cb["t"] + cb["d"])
            parts = [L for L in self.layers if L.group == g]
            first, rest = parts[0], parts[1:]
            x0 = min(L.x for L in parts); y0 = min(L.y for L in parts)
            x1 = max(L.x + L.w for L in parts); y1 = max(L.y + L.h for L in parts)
            Ks = np.zeros((y1 - y0, x1 - x0, 3), np.float32)
            As = np.zeros_like(Ks)
            for L in parts:
                sl = (slice(L.y - y0, L.y - y0 + L.h), slice(L.x - x0, L.x - x0 + L.w))
                Ks[sl] += L.K
                As[sl] += L.A
            K = np.minimum(Ks, 1)
            self.layers = [L for L in self.layers]
            self.layers[self.layers.index(first)] = Layer(g, K, As * (K / np.maximum(Ks, 1e-6)), x0, y0)
            mids = [L for L in self.layers if L.group == between]
            for j, L in enumerate(rest):
                L = Layer(L.group, L.K.copy(), L.A.copy(), L.x, L.y)
                self.layers[self.layers.index(rest[j])] = L
                keep = np.zeros((L.h, L.w), np.float32)
                for O in mids:
                    ox0, oy0 = max(L.x, O.x), max(L.y, O.y)
                    ox1, oy1 = min(L.x + L.w, O.x + O.w), min(L.y + L.h, O.y + O.h)
                    if ox1 > ox0 and oy1 > oy0:
                        keep[oy0 - L.y:oy1 - L.y, ox0 - L.x:ox1 - L.x] = np.maximum(
                            keep[oy0 - L.y:oy1 - L.y, ox0 - L.x:ox1 - L.x],
                            O.K[oy0 - O.y:oy1 - O.y, ox0 - O.x:ox1 - O.x].max(-1))
                keep = cv2.dilate((keep > 0.002).astype(np.uint8), np.ones((5, 5), np.uint8)).astype(np.float32)
                L.K = L.K * keep[..., None]
                L.A = L.A * keep[..., None]
        self.draw_len = {}
        for (scn, g), start in DRAW_FROM.items():
            if scn == name:
                self.draw_len[g] = draw_param([L for L in self.layers if L.group == g], start, k)

    def split_glyphs(self, glyphs):
        key = f"{self.name}/grandes"
        if key not in glyphs:
            return
        boxes = [[v * self.scale for v in b] for b in glyphs[key]]
        out = []
        for L in self.layers:
            if L.group != "grandes":
                out.append(L)
                continue
            cuts = [L.x]
            for a, b in zip(boxes, boxes[1:]):
                cuts.append(int(round((a[2] + b[0]) / 2)))
            cuts.append(L.x + L.w)
            for j, (c0, c1) in enumerate(zip(cuts, cuts[1:])):
                a, b = c0 - L.x, c1 - L.x
                g = Layer("grandes", L.K[:, a:b].copy(), L.A[:, a:b].copy(), c0, L.y)
                g.index = j
                bx = boxes[j]
                g.anchor = ((bx[0] + bx[2]) / 2, L.y + L.h)      # baseline centre
                out.append(g)
        self.layers = out
        self.nglyphs = len(boxes)

    # ---- background
    def background(self, t):
        k = self.k
        dp = DEPTH[self.name]
        e = 1 - ease("inOutSine", t / (0.7 * self.dur))
        e2 = 1 - ease("outCubic", t / (0.7 * self.dur))
        sN = 1 + (dp["near_scale"] - 1) * e2
        ax, ay = self.near_anchor
        nox, noy = dp["near_off"][0] * k * e, dp["near_off"][1] * k * e
        fox, foy = dp["far_off"][0] * k * e, dp["far_off"][1] * k * e
        w = self.wnear
        nx = (self.gx - ax - nox) / sN + ax
        ny = (self.gy - ay - noy) / sN + ay
        fx = self.gx - fox
        fy = self.gy - foy
        # rings open up delicately (radial scale about their own centre)
        er = ease("outCubic", t / 3.2)
        sr = dp["ring_s0"] + (1 - dp["ring_s0"]) * er
        for R_ in self.rings:
            cx, cy = R_["c"]
            wr = R_["w"]
            fx = fx + wr * ((self.gx - cx) / sr + cx - self.gx)
            fy = fy + wr * ((self.gy - cy) / sr + cy - self.gy)
        mx = w * nx + (1 - w) * fx
        my = w * ny + (1 - w) * fy
        rgb = cv2.remap(self.bg, mx, my, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        # a wave of presence passes outward across the rings
        acc = None
        for t0 in RIPPLES[self.name]:
            c = (t - t0) * RIPPLE_SPEED
            for R_ in self.rings:
                if c < -2 * RIPPLE_WIDTH or c > R_["rmax"] + 3 * RIPPLE_WIDTH:
                    continue
                b = np.exp(-((R_["r"] * sr - c) / RIPPLE_WIDTH) ** 2) * R_["w"]
                acc = b if acc is None else np.maximum(acc, b)
        if acc is not None:
            hpw = cv2.remap(self.ring_hp, mx, my, cv2.INTER_LINEAR)
            soft = cv2.remap(self.ring_soft, mx, my, cv2.INTER_LINEAR)
            # rings fade to the pastel under them and come back: a ripple
            f = (np.clip(hpw / 30.0, 0, 1) * acc * 0.6)[..., None]
            rgb = rgb + (soft - rgb) * f
        self.maps = (mx, my)
        return rgb

    # ---- foreground
    def state(self, g, t, L=None):
        st, mask = self.entry_state(g, t, L)
        ex = self.exit_at
        if ex is not None and g in self.rank:
            p = (t - (ex - EXIT["lead"] + self.rank[g] * EXIT["stagger"])) / EXIT["d"]
            if p > 0:
                e = ease("inOutCubic", p)
                k = self.k
                st = dict(st)
                st["m"] = st["m"] * (1 - e)
                st["dx"] = st.get("dx", 0) + EXIT["dx"] * k * e * e
                st["dy"] = st.get("dy", 0) + EXIT["dy"] * k * e * e
                st.pop("clip", None)
        return st, mask

    def entry_state(self, g, t, L):
        c = CHOREO[self.name].get(g)
        if c is None:
            return dict(m=1.0), None
        k = self.k
        bb = self.boxes[g]
        bw, bh = bb[2] - bb[0], bb[3] - bb[1]
        kind = c["kind"]
        t0, d = c["t"], c["d"]
        if kind == "glyphs":
            t0 += L.index * c["stagger"]
        p = (t - t0) / d
        if p <= 0:
            return dict(m=0.0), None
        p = clamp(p)
        pad = 4 * k
        clip = (bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad)
        cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
        e = ease("outQuint", p)
        if kind == "fade":
            return dict(m=ease("inOutSine", p), dx=c.get("dx", 0) * k * (1 - e),
                        dy=c.get("dy", 0) * k * (1 - e)), None
        if kind == "rise":
            return dict(m=ease("outCubic", p / 0.35), dy=0.85 * bh * (1 - e), clip=clip), None
        if kind == "slide":
            return dict(m=ease("outCubic", p / 0.45), dx=c["dx"] * k * (1 - e), dy=c["dy"] * k * (1 - e)), None
        if kind == "slide_wipe":
            q = ease("inOutCubic", p)
            fe = 0.25 * bw
            ox, oy = c["dx"] * k * (1 - e), c["dy"] * k * (1 - e)
            def mask(x0, y0, x1, y1, P, q=q, fe=fe, ox=ox):
                xs = np.arange(x0, x1, dtype=np.float32) + 0.5 - ox
                edge = bb[0] - fe + q * (bw + 2 * fe)
                m = sstep((edge - xs) / fe + 0.5)
                return np.broadcast_to(m[None, :], (y1 - y0, x1 - x0))
            return dict(m=1.0, dx=ox, dy=oy), (None if p >= 1 else mask)
        if kind == "hwipe":
            # horizontal mask, its edge slanted like the pleca's ends
            q = ease("inOutQuart", p)
            fe = 30 * k
            slant = 0.22
            ox = c.get("dx", 0) * k * (1 - e)
            def mask(x0, y0, x1, y1, P, q=q, fe=fe, ox=ox):
                xs = np.arange(x0, x1, dtype=np.float32)[None, :] + 0.5 - ox
                ys = np.arange(y0, y1, dtype=np.float32)[:, None] + 0.5
                span = bw + 2 * fe + slant * bh
                edge = bb[0] - fe + q * span - (bb[3] - ys) * slant
                return sstep((edge - xs) / fe + 0.5)
            return dict(m=1.0, dx=ox), (None if p >= 1 else mask)
        if kind == "glyphs":
            eb = ease("outBack", p)
            s = 0.55 + 0.45 * eb
            return dict(m=ease("outCubic", p / 0.3), s=s, anchor=L.anchor,
                        dy=36 * k * (1 - ease("outQuint", p))), None
        if kind == "grow":
            eb = ease("outBack", p)
            s0 = c.get("s0", 0.1)
            tip = (BALLOON_TIP[0] * k, BALLOON_TIP[1] * k)
            return dict(m=ease("outCubic", p / 0.25), s=s0 + (1 - s0) * eb, anchor=tip), None
        if kind == "draw":
            q = ease(c.get("ease", "inOutCubic"), p)
            total = self.draw_len[g] + 2
            Lc = q * total
            soft = 1.5 / k
            def mask(x0, y0, x1, y1, P, Lc=Lc, soft=soft):
                if P is None:
                    return np.ones((y1 - y0, x1 - x0), np.float32)
                return np.clip((Lc - P) / soft + 0.5, 0, 1)
            eo = ease("outQuint", clamp(p * 1.1))
            return dict(m=1.0, dx=c.get("dx", 0) * k * (1 - eo), dy=c.get("dy", 0) * k * (1 - eo)), mask
        raise ValueError(kind)

    def render(self, t):
        rgb = self.background(t)
        # once the outline covers the shared edges, back to the PDF's own pieces
        layers = self.layers if t < self.seamless_until else self.layers_pdf
        for L in layers:
            if L.group == "chinoin":
                continue
            st, mask = self.state(L.group, t, L)
            composite(rgb, L, st, mask)
        return rgb


# ------------------------------------------------------------------ transitions
def arc_reveal(prev, sc, rgb, t, dur):
    """The photo's own curved stroke leads: it travels out from the centre of
    its circle with the edge of the mask, revealing the photo behind it, stops
    exactly on its place, and the front carries on to unfold the rest."""
    k = sc.k
    cx, cy, R = ARC[sc.name]
    b0, b1 = ARC_BAND[sc.name]
    H, W = rgb.shape[:2]
    rmax = max(math.hypot(x - cx * k, y - cy * k) for x in (0, W) for y in (0, H)) / k
    r0 = 0.03 * R
    p = ease("inOutCubic", t / dur)
    # the arc travels out and lands on its place (half of the reveal), then
    # the front carries on beyond it at a soft edge - both continuous
    split = 0.5
    edge = R + b1
    if p < split:
        Rf = r0 + (edge - r0) * ease("outCubic", p / split)
    else:
        Rf = edge + (rmax + 240 - edge) * ease("inOutSine", (p - split) / (1 - split))
    Rb = min(Rf, edge)
    r = sc.r_arc
    fe = 3.0
    m_in = sstep((Rb - r) / fe + 0.5)
    m_out = sstep((Rf - r) / 220.0) if Rf > edge else 0.0
    m = np.where(r < edge, m_in, m_out)
    out = prev + (rgb - prev) * m[..., None]
    # 2) the travelling stroke: source pixels of the stroke shifted inwards
    if Rb < R + b1 - 0.5:
        shift = (R + b1) - Rb
        inner, outer = Rb - (b1 - b0), Rb
        band = (r > inner - 2) & (r < outer + 2)
        ys, xs = np.nonzero(band)
        if len(xs):
            y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
            rr = r[y0:y1, x0:x1]
            gx = sc.gx[y0:y1, x0:x1] - cx * k
            gy = sc.gy[y0:y1, x0:x1] - cy * k
            f = (rr + shift) / np.maximum(rr, 1e-3)
            mx, my = sc.maps
            sxm = cx * k + gx * f
            sym = cy * k + gy * f
            # follow the same background motion as the rest of the photo
            smx = cv2.remap(mx, sxm, sym, cv2.INTER_LINEAR)
            smy = cv2.remap(my, sxm, sym, cv2.INTER_LINEAR)
            src = cv2.remap(sc.bg, smx, smy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=-1)
            valid = (src[..., 0] >= 0) & (sxm >= 0) & (sxm < W - 1) & (sym >= 0) & (sym < H - 1)
            a = (sstep((rr - inner) / fe + 0.5) * sstep((outer - rr) / fe + 0.5) * valid)[..., None]
            reg = out[y0:y1, x0:x1]
            out[y0:y1, x0:x1] = reg + (np.maximum(src, 0) - reg) * a
    return out


def ripple_reveal(prev, sc, rgb, t, dur, center):
    """The rings of the previous scene open into the next one: concentric
    bands reveal it ahead of the main front, like the rings themselves."""
    k = sc.k
    H, W = rgb.shape[:2]
    cx, cy = center[0] * k, center[1] * k
    r = np.hypot(sc.gx - cx, sc.gy - cy) / k
    rmax = max(math.hypot(x - cx, y - cy) for x in (0, W) for y in (0, H)) / k
    p = ease("inOutCubic", t / dur)
    Rf = -120 + (rmax + 160) * p
    m = sstep((Rf - r) / 60.0 + 0.5)
    gap = 70.0
    for j in range(1, 4):
        c = Rf + j * gap
        wdt = 16.0 / j
        band = np.exp(-((r - c) / wdt) ** 2) * (0.85 - 0.2 * j) * clamp(Rf / 200 + 0.3)
        m = np.maximum(m, band)
    return prev + (rgb - prev) * m[..., None]


# ------------------------------------------------------------------ film
class Film:
    def __init__(self, layers_dir, scale):
        self.dir, self.scale = layers_dir, scale
        self.man = json.load(open(os.path.join(layers_dir, "manifest.json")))
        self.glyphs = json.load(open(os.path.join(layers_dir, "glyphs.json")))
        self.cache = {}
        self.W, self.H = int(3840 * scale), int(2160 * scale)
        ch = [L for L in self.man["s1"] if L["group"] == "chinoin"][0]
        self.chinoin = Layer.load(layers_dir, ch, scale)

    def scene(self, name):
        if name not in self.cache:
            if len(self.cache) >= 2:
                order = [n for n, _, _ in SCENES]
                far = max(self.cache, key=lambda n: abs(order.index(n) - order.index(name)))
                del self.cache[far]
            self.cache[name] = Scene(name, self.dir, self.man[name], self.glyphs, self.scale)
        return self.cache[name]

    def frame(self, T):
        idx = [i for i, (n, s, d) in enumerate(SCENES) if s <= T < s + d] or [len(SCENES) - 1]
        i = idx[-1]
        name, start, _ = SCENES[i]
        t = T - start
        sc = self.scene(name)
        rgb = sc.render(t)
        dur = REVEAL[name]
        if t < dur:
            if i == 0:
                prev = sc.wash.copy()
                # the wash is the scene's own pastel; the rings open with it
                prev = prev
            else:
                pn, ps, _ = SCENES[i - 1]
                prev = self.scene(pn).render(T - ps)
            if name in ARC:
                rgb = arc_reveal(prev, sc, rgb, t, dur)
            else:
                rgb = ripple_reveal(prev, sc, rgb, t, dur, RINGS["s2"][0][0])
        composite(rgb, self.chinoin, dict(m=1.0))
        return np.clip(rgb + 0.5, 0, 255).astype(np.uint8)


# ------------------------------------------------------------------ encode
_film = None


def _init(layers_dir, scale):
    global _film
    _film = Film(layers_dir, scale)


def _render(f):
    return _film.frame(f / FPS).tobytes()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("layers")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--crf", type=int, default=14)
    ap.add_argument("--preset", default="slow")
    ap.add_argument("--stills")
    ap.add_argument("--times")
    a = ap.parse_args()
    if a.stills:
        os.makedirs(a.stills, exist_ok=True)
        film = Film(a.layers, a.scale)
        for ts in a.times.split(","):
            T = float(ts)
            Image.fromarray(film.frame(T)).save(os.path.join(a.stills, f"t{T:07.3f}.png"))
        return
    n = int(round(TOTAL * FPS))
    W, H = int(3840 * a.scale), int(2160 * a.scale)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-vf", "scale=out_color_matrix=bt709:out_range=tv",
           "-c:v", "libx264", "-preset", a.preset, "-crf", str(a.crf),
           "-profile:v", "high", "-level", "5.2", "-pix_fmt", "yuv420p",
           "-g", "600", "-keyint_min", "30",
           "-force_key_frames", ",".join(str(s) for _, s, _ in SCENES),
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-color_range", "tv", "-movflags", "+faststart", a.out]
    print(f"{n} frames, {n / FPS:.2f}s, {W}x{H}", flush=True)
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    from multiprocessing import Pool
    with Pool(a.workers, initializer=_init, initargs=(a.layers, a.scale)) as pool:
        for f, buf in enumerate(pool.imap(_render, range(n), chunksize=4)):
            enc.stdin.write(buf)
            if f % 60 == 59:
                print(f"  {f + 1}/{n}", flush=True)
    enc.stdin.close()
    if enc.wait() != 0:
        raise RuntimeError("ffmpeg failed")
    print("wrote", a.out)


if __name__ == "__main__":
    main()
