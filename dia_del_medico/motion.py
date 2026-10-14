"""Día del Médico - animation and encoding.

usage:
  python motion.py LAYERS_DIR OUT.mp4 [--scale 1.0] [--workers 3] [--crf 16]
  python motion.py LAYERS_DIR --stills DIR --times 1.0,2.5 [--scale 0.5]

scale 1.0 -> 3840x2160, 0.5 -> 1920x1080. Constant 30 fps, no audio.

Every element comes from the PDF (build.py): backgrounds are the original
photos, texts / quotes / frames / logos are the original vector layers.
Motion only moves, masks or lights what already exists.
"""
import argparse, json, math, os, subprocess, sys
import numpy as np
import cv2
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from layout import WAVES, WAVE_WIDTH, FRAME1, STROKE_TOP, STROKE_BOT, SHIELD, CROSS  # noqa: E402
import network  # noqa: E402

FPS = 30
cv2.setNumThreads(1)


# ------------------------------------------------------------------ easing
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


EASE = {
    "lin": lambda p: p,
    "outQuint": lambda p: 1 - (1 - p) ** 5,
    "outQuart": lambda p: 1 - (1 - p) ** 4,
    "outCubic": lambda p: 1 - (1 - p) ** 3,
    "outExpo": lambda p: 1.0 if p >= 1 else 1 - 2 ** (-10 * p),
    "inOutCubic": lambda p: 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2,
    "inOutQuart": lambda p: 8 * p ** 4 if p < 0.5 else 1 - (-2 * p + 2) ** 4 / 2,
    "inOutSine": lambda p: -(math.cos(math.pi * p) - 1) / 2,
    "inOutQuint": lambda p: 16 * p ** 5 if p < 0.5 else 1 - (-2 * p + 2) ** 5 / 2,
}


def ease(name, p):
    return EASE[name](clamp(p))


# ------------------------------------------------------------------ timeline
# Scenes overlap by REVEAL seconds: the incoming scene is revealed by its own
# wave while the outgoing one keeps moving underneath.
REVEAL = 1.4
SCENES = [("s1", 0.0, 10.4), ("s2", 9.0, 8.4), ("s3", 16.0, 10.0)]
EXIT = dict(lead=0.3, stagger=0.06, d=0.6, dx=26, dy=10)   # outgoing elements, pt
TOTAL = 26.0

# Element choreography, scene-local seconds. kinds:
#   rise / drop  - masked by its own box, slides in from below / above
#   slide        - masked, slides in from the left
#   wipe         - soft mask sweeping left -> right (script lines: glyphs intact)
#   wipe_d/wipe_u- soft mask top -> bottom / bottom -> top
#   pop / scale  - uniform scale to 1:1 about the centre (no overshoot)
#   fade         - opacity, optional small dy
#   stroke       - drawn along its own path (frames)
CHOREO = {
    "s1": {
        "panel": dict(kind="fade", t=1.35, d=1.3),
        "q1c": dict(kind="pop", t=1.15, d=0.6, s0=0.55),
        "q1g": dict(kind="rise", t=1.35, d=0.6),
        "frame": dict(kind="stroke", t=1.45, d=1.75),
        "l1": dict(kind="rise", t=2.35, d=0.85),
        "l2": dict(kind="wipe", t=3.05, d=1.0),
        "l3": dict(kind="wipe", t=3.95, d=1.0),
        "l4": dict(kind="slide", t=4.85, d=0.85),
        "l5": dict(kind="wipe", t=5.55, d=0.9),
        "q2c": dict(kind="pop", t=6.35, d=0.6, s0=0.55),
        "q2g": dict(kind="drop", t=6.55, d=0.6),
    },
    "s2": {
        "panel": dict(kind="fade", t=0.95, d=1.0),
        "n23": dict(kind="scale", t=1.2, d=0.7, s0=1.22),
        "q1": dict(kind="wipe_d", t=1.35, d=0.4),
        "stroke_top": dict(kind="stroke", t=1.5, d=1.15),
        "octubre": dict(kind="wipe", t=1.95, d=0.9),
        "dia": dict(kind="rise", t=2.45, d=0.85),
        "stroke_bot": dict(kind="stroke", t=2.2, d=1.05),
        "q2": dict(kind="wipe_u", t=3.15, d=0.4),
    },
    "s3": {
        "gracias": dict(kind="rise", t=2.75, d=0.9),
        "salud": dict(kind="wipe", t=3.6, d=1.25),
        "proposito": dict(kind="rise", t=4.75, d=1.0),
        "zymir": dict(kind="rise", t=6.0, d=0.7),
        "sunderin": dict(kind="rise", t=6.18, d=0.7),
        "gabirol": dict(kind="rise", t=6.36, d=0.7),
        "benel": dict(kind="rise", t=6.54, d=0.7),
        "legend": dict(kind="fade", t=7.05, d=0.7, dy=10),
    },
}

# Light travelling along each wave: (launch time, strength). Launches are tied
# to the entries, so the wave "carries" every message in.
PULSES = {
    "s1": [(0.2, 1.0), (2.2, 0.8), (2.95, 0.7), (3.85, 0.7), (4.75, 0.8), (5.45, 0.7),
           (6.3, 0.9), (7.6, 0.7), (8.5, 1.1)],
    "s2": [(-0.2, 1.0), (1.1, 0.9), (2.3, 0.7), (3.05, 1.4), (4.6, 0.6), (5.8, 0.8), (6.6, 1.1)],
    "s3": [(-0.2, 1.0), (0.8, 0.9), (2.6, 0.7), (3.5, 0.7), (4.65, 0.8), (5.9, 0.8),
           (7.4, 0.6), (8.6, 0.6)],
}
PULSE_SPEED = {"s1": 820.0, "s2": 900.0, "s3": 950.0}   # pt / s along the wave
PULSE_SIGMA = 95.0                                       # pt
FLOW_GAIN = 1.6

# Background depth: the 'near' plane (instruments / doctor side / shield)
# and the 'far' plane drift differently; both land exactly on the original.
#   near: (start scale, anchor pt, start offset pt); far: start offset pt
DEPTH = {
    "s1": dict(near_scale=1.045, near_anchor=(250, 760), near_off=(-12, 8), far_off=(14, -6), drift="all"),
    "s2": dict(near_scale=1.035, near_anchor=(520, 560), near_off=(-16, -6), far_off=(0, 0), drift="all"),
    "s3": dict(near_scale=1.05, near_anchor=SHIELD["center"], near_off=(0, 10), far_off=(14, 6), drift="all"),
}
UNDULATE = dict(amp=1.6, wavelength=280.0, period=3.2)   # pt, pt, s

# Scene 3: shield, cross and network
SHIELD_T = (0.95, 1.5)        # network reveal from the contact point (start, duration)
CROSS_T = (1.55, 0.85)        # cross arms grow from the centre as the front reaches it
NET_PULSES_FROM = 2.4


# ------------------------------------------------------------------ helpers
def polyline_fields(pts, W, H, k, step=8):
    """Arc position s (pt) of the nearest point on the polyline and the
    distance D (pt) to it, for every pixel. Computed coarse, upsampled."""
    w, h = W // step + 2, H // step + 2
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    X, Y = xs * step / k, ys * step / k
    best = np.full((h, w), 1e9, np.float32)
    S = np.zeros((h, w), np.float32)
    acc = 0.0
    n = len(pts) - 1
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        t = ((X - x0) * dx + (Y - y0) * dy) / (L * L)
        lo = -np.inf if i == 0 else 0.0
        hi = np.inf if i == n - 1 else 1.0
        t = np.clip(t, lo, hi)
        px, py = x0 + t * dx, y0 + t * dy
        d = np.hypot(X - px, Y - py)
        m = d < best
        best[m] = d[m]
        S[m] = (acc + t * L)[m]
        acc += L
    # s jumps where the nearest segment changes: smooth it so nothing driven by
    # it (reveal fronts, light bands) can show a hard or stepped edge
    S = cv2.GaussianBlur(S, (0, 0), 40 * k / step)
    up = lambda a: cv2.resize(a, (w * step, h * step), interpolation=cv2.INTER_CUBIC)[:H, :W]
    return up(S), up(best), acc


def glow(rgb, x, y, sigma, color, amp):
    """Additive soft light (used only for pulses / stroke heads)."""
    H, W = rgb.shape[:2]
    r = int(sigma * 3.5) + 1
    x0, x1 = max(0, int(x) - r), min(W, int(x) + r + 1)
    y0, y1 = max(0, int(y) - r), min(H, int(y) + r + 1)
    if x1 <= x0 or y1 <= y0:
        return
    xs = np.arange(x0, x1, dtype=np.float32) - x
    ys = np.arange(y0, y1, dtype=np.float32) - y
    g = np.exp(-(ys[:, None] ** 2 + xs[None, :] ** 2) / (2 * sigma * sigma)) * amp
    rgb[y0:y1, x0:x1] += g[..., None] * np.asarray(color, np.float32)


# ------------------------------------------------------------------ layers
class Layer:
    def __init__(self, d, L, scale):
        self.group = L["group"]
        F = np.asarray(Image.open(os.path.join(d, L["file"] + "_F.png")), np.float32) / 255
        A = np.asarray(Image.open(os.path.join(d, L["file"] + "_A.png")), np.float32)
        x, y = L["x"] * scale, L["y"] * scale
        if scale != 1.0:
            # resample onto the scaled grid with the exact sub-pixel origin
            fx, fy = math.floor(x), math.floor(y)
            w = int(math.ceil(x + L["w"] * scale)) - fx + 1
            h = int(math.ceil(y + L["h"] * scale)) - fy + 1
            M = np.float32([[scale, 0, x - fx], [0, scale, y - fy]])
            F = 1 - cv2.warpAffine(1 - F, M, (w, h), flags=cv2.INTER_AREA if scale < 1 else cv2.INTER_CUBIC)
            A = cv2.warpAffine(A, M, (w, h), flags=cv2.INTER_AREA if scale < 1 else cv2.INTER_CUBIC)
            x, y = fx, fy
        self.K = 1 - F          # how much of the backdrop the layer removes
        self.A = A              # what it adds
        self.x, self.y = int(x), int(y)
        self.h, self.w = A.shape[:2]
        self.param = None       # stroke parameter map (pt), set for frames


def composite(rgb, L, st, mask_fn=None):
    """rgb += m * (A - K * rgb) with the layer transformed by st."""
    m = st["m"]
    if m <= 1e-3:
        return
    H, W = rgb.shape[:2]
    s, dx, dy = st.get("s", 1.0), st.get("dx", 0.0), st.get("dy", 0.0)
    ax, ay = st.get("anchor", (0, 0))
    # screen = s * (p - a) + a + d   for layer pixel p (screen coords at rest)
    ox = s * (L.x - ax) + ax + dx
    oy = s * (L.y - ay) + ay + dy
    ident = abs(s - 1) < 1e-6 and abs(ox - round(ox)) < 1e-4 and abs(oy - round(oy)) < 1e-4
    if ident:
        X0, Y0 = int(round(ox)), int(round(oy))
        X1, Y1 = X0 + L.w, Y0 + L.h
    else:
        X0, Y0 = math.floor(ox), math.floor(oy)
        X1 = math.ceil(ox + s * L.w) + 1
        Y1 = math.ceil(oy + s * L.h) + 1
    clip = st.get("clip")
    rx0, ry0, rx1, ry1 = max(X0, 0), max(Y0, 0), min(X1, W), min(Y1, H)
    if clip:
        rx0, ry0 = max(rx0, int(clip[0])), max(ry0, int(clip[1]))
        rx1, ry1 = min(rx1, int(math.ceil(clip[2]))), min(ry1, int(math.ceil(clip[3])))
    if rx1 <= rx0 or ry1 <= ry0:
        return
    if ident:
        sx, sy = rx0 - int(round(ox)), ry0 - int(round(oy))
        Kc = L.K[sy:sy + ry1 - ry0, sx:sx + rx1 - rx0]
        Ac = L.A[sy:sy + ry1 - ry0, sx:sx + rx1 - rx0]
        Pc = None if L.param is None else L.param[sy:sy + ry1 - ry0, sx:sx + rx1 - rx0]
    else:
        M = np.float32([[s, 0, ox - rx0], [0, s, oy - ry0]])
        size = (rx1 - rx0, ry1 - ry0)
        Kc = cv2.warpAffine(L.K, M, size, flags=cv2.INTER_CUBIC)
        Ac = cv2.warpAffine(L.A, M, size, flags=cv2.INTER_CUBIC)
        Pc = None
    f = m
    if mask_fn is not None:
        f = mask_fn(rx0, ry0, rx1, ry1, Pc) * m
        f = f[..., None]
    reg = rgb[ry0:ry1, rx0:rx1]
    reg += f * (Ac - Kc * reg)


# ------------------------------------------------------------------ scene
class Scene:
    def __init__(self, name, layers_dir, man, scale):
        self.name, self.scale = name, scale
        self.k = 2.0 * scale                     # px per pt
        k = self.k
        bg = cv2.cvtColor(cv2.imread(os.path.join(layers_dir, f"{name}_bg.png")), cv2.COLOR_BGR2RGB)
        self.bg_u8_full = bg
        if scale != 1.0:
            bg = cv2.resize(bg, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        self.H, self.W = bg.shape[:2]
        H, W = self.H, self.W
        self.bg = bg.astype(np.float32)
        # fine light detail of the photo (dots, lines, nodes): what the pulses light up
        self.hp = np.maximum(self.bg - cv2.GaussianBlur(self.bg, (0, 0), 3.0 * k), 0)
        self.layers = [Layer(layers_dir, L, scale) for L in man if L["group"] != "bg"]
        self.boxes = {}
        for L in self.layers:
            b = self.boxes.get(L.group)
            nb = [L.x, L.y, L.x + L.w, L.y + L.h]
            self.boxes[L.group] = nb if b is None else [min(b[0], nb[0]), min(b[1], nb[1]),
                                                        max(b[2], nb[2]), max(b[3], nb[3])]
        # wave fields
        self.S, self.D, self.wlen = polyline_fields(WAVES[name], W, H, k)
        wid = WAVE_WIDTH[name]
        self.Z = np.exp(-(self.D / wid) ** 2).astype(np.float32)
        # reveal arrival field: runs along the wave first, then spreads out of it
        sn = np.clip(self.S / self.wlen, -0.15, 1.15)
        dn = self.D / (1.25 * max(W, H) / k)
        arr = 0.62 * sn + 0.85 * dn
        arr = cv2.resize(cv2.GaussianBlur(cv2.resize(arr, (W // 8, H // 8), interpolation=cv2.INTER_AREA),
                                          (0, 0), 30 * k / 8), (W, H), interpolation=cv2.INTER_CUBIC)
        self.arr = ((arr - arr.min()) / (arr.max() - arr.min())).astype(np.float32)
        # depth weight: 1 on the near plane
        ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
        self.gx, self.gy = xs, ys
        X, Y = xs / k, ys / k
        if name == "s1":
            self.wnear = 1 - np.clip((X - 1060) / 260, 0, 1) ** 2 * (3 - 2 * np.clip((X - 1060) / 260, 0, 1))
        elif name == "s2":
            u = np.clip((X - 1000) / 120, 0, 1)
            self.wnear = 1 - u * u * (3 - 2 * u)
        else:
            cx, cy = SHIELD["center"]
            rx, ry = SHIELD["radii"]
            r = np.sqrt(((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2)
            u = np.clip((r - 1.0) / 0.35, 0, 1)
            self.wnear = 1 - u * u * (3 - 2 * u)
        self.wnear = self.wnear.astype(np.float32)
        self.flow_n = None
        if name == "s1":
            self.und_dir = (1.0, 0.0)
        else:
            self.und_dir = (0.0, 1.0)
        self.setup_frames()
        if name == "s3":
            self.setup_shield(X, Y)
        self.dur = dict((n, d) for n, _, d in SCENES)[name]
        names = [n for n, _, _ in SCENES]
        i = names.index(name)
        self.exit_at = SCENES[i + 1][1] - SCENES[i][1] if i + 1 < len(SCENES) else None
        order = sorted(CHOREO[name], key=lambda g: CHOREO[name][g]["t"])
        self.rank = {g: j for j, g in enumerate(order)}

    # ---- strokes
    def setup_frames(self):
        k = self.k
        for L in self.layers:
            ys, xs = np.mgrid[0:L.h, 0:L.w].astype(np.float32)
            X, Y = (xs + L.x + 0.5) / k, (ys + L.y + 0.5) / k
            if L.group == "frame":
                L.param = self.frame1_param(X, Y)
            elif L.group == "stroke_top":
                L.param = poly_param(STROKE_TOP, X, Y)
            elif L.group == "stroke_bot":
                L.param = poly_param(STROKE_BOT, X, Y)

    @staticmethod
    def frame1_geom():
        x0, y0, x1, y1 = FRAME1["rect"]
        sx = FRAME1["start"][0]
        per = 2 * ((x1 - x0) + (y1 - y0))
        return x0, y0, x1, y1, sx, per

    def frame1_param(self, X, Y):
        x0, y0, x1, y1, sx, per = self.frame1_geom()
        dt, dr, db, dl = np.abs(Y - y0), np.abs(X - x1), np.abs(Y - y1), np.abs(X - x0)
        e = np.argmin(np.stack([dt, dr, db, dl]), 0)
        a = x1 - sx
        u = np.where(e == 0, np.where(X >= sx, X - sx, per - (sx - X)),
            np.where(e == 1, a + (Y - y0),
            np.where(e == 2, a + (y1 - y0) + (x1 - X),
                     a + (y1 - y0) + (x1 - x0) + (y1 - Y))))
        u = np.mod(u, per)
        return np.minimum(u, per - u).astype(np.float32)

    def frame1_point(self, u):
        x0, y0, x1, y1, sx, per = self.frame1_geom()
        u = u % per
        segs = [((sx, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)),
                ((x0, y1), (x0, y0)), ((x0, y0), (sx, y0))]
        return walk(segs, u)

    # ---- shield (page 3)
    def setup_shield(self, X, Y):
        k = self.k
        cx, cy = SHIELD["center"]
        rx, ry = SHIELD["radii"]
        # soft mask of the shield outline (rim included)
        poly = np.round(np.asarray(SHIELD["outline"], np.float32) * k).astype(np.int32)
        sz = np.zeros((self.H, self.W), np.uint8)
        cv2.fillPoly(sz, [poly], 255, lineType=cv2.LINE_AA)
        r = int(10 * k)
        sz = cv2.dilate(sz, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1)))
        self.SZ = cv2.GaussianBlur(sz.astype(np.float32) / 255, (0, 0), 12 * k)
        px, py = SHIELD["contact"]
        dc = np.hypot(X - px, Y - py)
        self.sarr = (dc / dc[self.SZ > 0.01].max()).astype(np.float32)
        # cross
        f = 2.5
        v, h = CROSS["v"], CROSS["h"]
        rect = lambda b: (np.clip((X - b[0]) / f + .5, 0, 1) * np.clip((b[2] - X) / f + .5, 0, 1) *
                          np.clip((Y - b[1]) / f + .5, 0, 1) * np.clip((b[3] - Y) / f + .5, 0, 1))
        self.CV = rect((v[0] - 3, v[1] - 3, v[2] + 3, v[3] + 3)).astype(np.float32)
        self.CH = rect((h[0] - 3, h[1] - 3, h[2] + 3, h[3] + 3)).astype(np.float32)
        self.CM = np.maximum(self.CV, self.CH)
        self.ccx, self.ccy = CROSS["center"]
        self.cvh = max(self.ccy - v[1], v[3] - self.ccy) + 4
        self.chw = max(self.ccx - h[0], h[2] - self.ccx) + 4
        self.Xpt, self.Ypt = X, Y
        # before it lights up, the shield is the same photo, dimmed
        self.pre = self.bg * 0.2 + cv2.GaussianBlur(self.bg, (0, 0), 40 * k) * 0.2
        bright = self.bg * self.CM[..., None]
        self.bloom = cv2.GaussianBlur(bright, (0, 0), 14 * k)
        # network graph (pt), pulses along existing connections
        nodes, edges = network.detect(self.bg_u8_full)
        self.nodes = np.asarray(nodes, np.float32)
        adj = {}
        for i, j in edges:
            adj.setdefault(i, []).append(j)
            adj.setdefault(j, []).append(i)
        rng = np.random.default_rng(23)
        self.netp = []
        starts = [i for i in adj if len(adj[i]) >= 2]
        t = NET_PULSES_FROM
        while t < 10.5:
            i = int(rng.choice(starts))
            path = [i]
            prev = None
            for _ in range(int(rng.integers(3, 6))):
                nxt = [j for j in adj[path[-1]] if j != prev and j not in path]
                if not nxt:
                    break
                prev = path[-1]
                path.append(int(rng.choice(nxt)))
            if len(path) >= 3:
                self.netp.append((t, path))
            t += float(rng.uniform(0.07, 0.16))

    def shield_state(self, t):
        mS = np.clip((ease("inOutSine", (t - SHIELD_T[0]) / SHIELD_T[1]) * 1.25 - self.sarr) / 0.25, 0, 1)
        p = ease("inOutCubic", (t - CROSS_T[0]) / CROSS_T[1])
        gv = np.clip((p * self.cvh - np.abs(self.Ypt - self.ccy)) / 3.0 + 0.5, 0, 1)
        gh = np.clip((p * self.chw - np.abs(self.Xpt - self.ccx)) / 3.0 + 0.5, 0, 1)
        # normalised by the arms' own soft edge, so a fully open cross is exactly 1
        mC = np.maximum(self.CV * gv, self.CH * gh) / np.maximum(self.CM, 1e-4)
        reveal = self.CM * mC + (1 - self.CM) * mS
        return mS, reveal, p

    # ---- background
    def background(self, t):
        """Moving original photo + light flowing along its own wave.
        Returns (rgb, hp) both already displaced."""
        k = self.k
        dp = DEPTH[self.name]
        e = 1 - ease("inOutSine", t / self.dur)          # 1 -> 0 over the scene
        e2 = 1 - ease("outCubic", t / (self.dur * 0.8))
        sN = 1 + (dp["near_scale"] - 1) * e2
        ax, ay = dp["near_anchor"][0] * k, dp["near_anchor"][1] * k
        nox, noy = dp["near_off"][0] * k * e, dp["near_off"][1] * k * e
        fox, foy = dp["far_off"][0] * k * e, dp["far_off"][1] * k * e
        w = self.wnear
        # inverse map: source = (screen - a - off) / s + a  on the near plane
        nx = (self.gx - ax - nox) / sN + ax
        ny = (self.gy - ay - noy) / sN + ay
        fx = self.gx - fox
        fy = self.gy - foy
        mx = w * nx + (1 - w) * fx
        my = w * ny + (1 - w) * fy
        # gentle undulation of the dot sheet along its own course
        U = UNDULATE
        ph = 2 * math.pi * (self.S / U["wavelength"] - t / U["period"])
        und = (U["amp"] * k) * np.sin(ph) * self.Z * (1 - 0.6 * w)
        mx -= und * self.und_dir[0]
        my -= und * self.und_dir[1]
        rgb = cv2.remap(self.bg, mx, my, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        hp = cv2.remap(self.hp, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        if self.name == "s3":
            pre = cv2.remap(self.pre, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            mS, reveal, pc = self.shield_state(t)
            R = 1 - self.SZ * (1 - reveal)
            rgb = pre + (rgb - pre) * R[..., None]
            # the reveal front lights up the network lines it passes
            front = 4 * mS * (1 - mS) * self.SZ * (1 - self.CM)
            rgb += hp * (front * 2.2)[..., None]
            # cross: brief bloom as the arms open, settling to the original
            if pc > 0:
                b = 0.75 * ease("outCubic", pc / 0.6) * math.exp(-max(0.0, t - (CROSS_T[0] + CROSS_T[1])) / 0.55)
                rgb += self.bloom * b
            hp = hp * R[..., None]
        # light flowing along the wave
        band = self.flow(t)
        if band is not None:
            rgb += hp * (band * FLOW_GAIN)[..., None]
        if self.name == "s3":
            self.net_pulses(rgb, hp, t)
        return rgb, hp

    def flow(self, t):
        sp = PULSE_SPEED[self.name]
        acc = None
        sig = PULSE_SIGMA
        for t0, g in PULSES[self.name]:
            c = (t - t0) * sp - 2.5 * sig
            if c < -3 * sig or c > self.wlen + 3 * sig:
                continue
            b = g * np.exp(-((self.S - c) / sig) ** 2)
            acc = b if acc is None else acc + b
        if acc is None:
            return None
        return acc * self.Z

    def net_pulses(self, rgb, hp, t):
        k = self.k
        speed = 170.0   # pt/s
        for t0, path in self.netp:
            if t < t0:
                continue
            pts = self.nodes[path]
            seg = np.hypot(*(pts[1:] - pts[:-1]).T)
            total = seg.sum()
            d = (t - t0) * speed
            if d > total:
                continue
            i = int(np.searchsorted(np.cumsum(seg), d))
            i = min(i, len(seg) - 1)
            u = (d - (np.cumsum(seg)[i] - seg[i])) / seg[i]
            x, y = pts[i] + (pts[i + 1] - pts[i]) * u
            life = d / total
            a = math.sin(math.pi * life) ** 0.6
            X, Y = x * k, y * k
            sig = 7 * k
            r = int(sig * 3)
            x0, x1 = max(0, int(X) - r), min(self.W, int(X) + r + 1)
            y0, y1 = max(0, int(Y) - r), min(self.H, int(Y) + r + 1)
            gx = np.arange(x0, x1, dtype=np.float32) - X
            gy = np.arange(y0, y1, dtype=np.float32) - Y
            g = np.exp(-(gy[:, None] ** 2 + gx[None, :] ** 2) / (2 * sig * sig))
            rgb[y0:y1, x0:x1] += hp[y0:y1, x0:x1] * (g * 4.0 * a)[..., None]
            glow(rgb, X, Y, 2.2 * k, (210, 245, 255), 0.55 * a)

    # ---- foreground
    def state(self, g, t):
        st, mask = self.entry_state(g, t)
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
                if "stroke" in st:
                    st["p"] = 1.0
        return st, mask

    def entry_state(self, g, t):
        c = CHOREO[self.name].get(g)
        if c is None:
            return dict(m=1.0), None
        k = self.k
        bb = self.boxes[g]
        bw, bh = bb[2] - bb[0], bb[3] - bb[1]
        p = (t - c["t"]) / c["d"]
        if p <= 0:
            return dict(m=0.0), None
        p = clamp(p)
        kind = c["kind"]
        cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
        pad = 4 * k
        clip = (bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad)
        e = ease("outQuint", p)
        if kind == "fade":
            return dict(m=ease("inOutSine", p), dy=c.get("dy", 0) * k * (1 - e)), None
        if kind in ("rise", "drop"):
            sgn = 1 if kind == "rise" else -1
            return dict(m=ease("outCubic", p / 0.35), dy=sgn * 0.8 * bh * (1 - e), clip=clip), None
        if kind == "slide":
            return dict(m=ease("outCubic", p / 0.4), dx=-min(0.3 * bw, 220 * k) * (1 - e), clip=clip), None
        if kind in ("pop", "scale"):
            s0 = c.get("s0", 0.6)
            es = ease("outExpo" if kind == "scale" else "outQuint", p)
            return dict(m=ease("outCubic", p / (0.3 if kind == "scale" else 0.4)),
                        s=s0 + (1 - s0) * es, anchor=(cx, cy)), None
        if kind in ("wipe", "wipe_d", "wipe_u"):
            q = ease("inOutCubic", p)
            fe = (0.22 * bw) if kind == "wipe" else 0.45 * bh
            def mask(x0, y0, x1, y1, P, kind=kind, q=q, fe=fe):
                if kind == "wipe":
                    xs = np.arange(x0, x1, dtype=np.float32) + 0.5
                    edge = bb[0] - fe + q * (bw + 2 * fe)
                    m = np.clip((edge - xs) / fe + 0.5, 0, 1)
                    return np.broadcast_to(smooth_arr(m)[None, :], (y1 - y0, x1 - x0))
                ys = np.arange(y0, y1, dtype=np.float32) + 0.5
                if kind == "wipe_d":
                    edge = bb[1] - fe + q * (bh + 2 * fe)
                    m = np.clip((edge - ys) / fe + 0.5, 0, 1)
                else:
                    edge = bb[3] + fe - q * (bh + 2 * fe)
                    m = np.clip((ys - edge) / fe + 0.5, 0, 1)
                return np.broadcast_to(smooth_arr(m)[:, None], (y1 - y0, x1 - x0))
            dx = (14 * k * (1 - ease("outQuint", p))) if kind == "wipe" else 0
            return dict(m=1.0 if q < 1 else 1.0, dx=-dx if kind == "wipe" else 0), (None if p >= 1 else mask)
        if kind == "stroke":
            q = ease("inOutCubic", p)
            if g == "frame":
                total = self.frame1_geom()[5] / 2 + 2
            elif g == "stroke_top":
                total = poly_len(STROKE_TOP) + 2
            else:
                total = poly_len(STROKE_BOT) + 2
            Lc = q * total
            soft = 1.2 / k
            def mask(x0, y0, x1, y1, P, Lc=Lc, soft=soft):
                if P is None:                  # moved (exit): the stroke is complete by then
                    return np.ones((y1 - y0, x1 - x0), np.float32)
                return np.clip((Lc - P) / soft + 0.5, 0, 1)
            return dict(m=1.0, stroke=Lc, p=p), mask
        raise ValueError(kind)

    def render(self, t):
        rgb, hp = self.background(t)
        heads = []
        cache = {}
        for L in self.layers:
            if L.group == "chinoin":
                continue                       # drawn once, fixed, on top of the film
            if L.group not in cache:
                cache[L.group] = self.state(L.group, t)
            st, mask = cache[L.group]
            if mask is not None and "stroke" in st and L.param is None:
                continue
            composite(rgb, L, st, mask)
            if "stroke" in st and st["p"] < 1 and L.group not in [h[0] for h in heads]:
                heads.append((L.group, st["stroke"], st["p"]))
        # a small light leads each frame stroke while it is drawn
        k = self.k
        for g, Lc, p in heads:
            a = 0.85 * math.sin(math.pi * min(1.0, p * 1.05)) ** 0.5
            if g == "frame":
                pts = [self.frame1_point(Lc), self.frame1_point(-Lc)]
            else:
                pts = [poly_point(STROKE_TOP if g == "stroke_top" else STROKE_BOT, Lc)]
            for x, y in pts:
                glow(rgb, x * k, y * k, 7 * k, (200, 240, 255), 0.45 * a * 255 / 255)
                glow(rgb, x * k, y * k, 2.2 * k, (255, 255, 255), 0.9 * a)
        return rgb, hp


def smooth_arr(m):
    return m * m * (3 - 2 * m)


def poly_len(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def walk(segs, u):
    for (a, b) in segs:
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if u <= L:
            f = u / L if L else 0
            return a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
        u -= L
    return segs[-1][1]


def poly_point(pts, u):
    return walk(list(zip(pts, pts[1:])), max(0.0, min(u, poly_len(pts))))


def poly_param(pts, X, Y):
    best = np.full(X.shape, 1e9, np.float32)
    P = np.zeros(X.shape, np.float32)
    acc = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        t = np.clip(((X - x0) * dx + (Y - y0) * dy) / (L * L), 0, 1)
        d = np.hypot(X - (x0 + t * dx), Y - (y0 + t * dy))
        m = d < best
        best[m] = d[m]
        P[m] = (acc + t * L)[m]
        acc += L
    # caps: pixels beyond the start count as the start
    return P


# ------------------------------------------------------------------ film
class Film:
    def __init__(self, layers_dir, scale):
        self.dir, self.scale = layers_dir, scale
        self.man = json.load(open(os.path.join(layers_dir, "manifest.json")))
        self.cache = {}
        self.W, self.H = int(3840 * scale), int(2160 * scale)
        ch = [L for L in self.man["s1"] if L["group"] == "chinoin"][0]
        self.chinoin = Layer(layers_dir, ch, scale)
        s3 = cv2.cvtColor(cv2.imread(os.path.join(layers_dir, "s3_bg.png")), cv2.COLOR_BGR2RGB)
        # the deepest navy of the campaign (page 3 sky) opens the film
        self.navy = s3[60:260, 3300:3700].reshape(-1, 3).mean(0).astype(np.float32)

    def scene(self, name):
        if name not in self.cache:
            keep = {n for n, _, _ in SCENES if n == name}
            for n in list(self.cache):
                if n not in keep and len(self.cache) >= 2:
                    del self.cache[n]
            self.cache[name] = Scene(name, self.dir, self.man[name], self.scale)
        return self.cache[name]

    def frame(self, T):
        idx = [i for i, (n, s, d) in enumerate(SCENES) if s <= T < s + d] or [len(SCENES) - 1]
        i = idx[-1]
        name, start, _ = SCENES[i]
        t = T - start
        sc = self.scene(name)
        rgb, hp = sc.render(t)
        if t < REVEAL:
            if i == 0:
                prev = np.empty_like(rgb)
                prev[:] = self.navy
            else:
                pn, ps, _ = SCENES[i - 1]
                prev, _ = self.scene(pn).render(T - ps)
            q = ease("inOutSine", t / REVEAL)
            fw = 0.16
            tau = q * (1 + fw) - fw / 2
            m = np.clip((tau - sc.arr) / fw + 0.5, 0, 1)
            m = m * m * (3 - 2 * m)
            band = 4 * m * (1 - m)
            out = prev + (rgb - prev) * m[..., None]
            # the front is made of the new scene's own dots and lines, lit up
            out += hp * (band * 3.0)[..., None] + rgb * (band * 0.12)[..., None]
            rgb = out
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
    ap.add_argument("--crf", type=int, default=16)
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
    # frames are rendered in parallel but encoded by one encoder, in order:
    # one continuous GOP structure, no seams between chunks
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-vf", "scale=out_color_matrix=bt709:out_range=tv",
           "-c:v", "libx264", "-preset", a.preset, "-crf", str(a.crf),
           "-profile:v", "high", "-level", "5.2", "-pix_fmt", "yuv420p",
           # keyframes only where a new scene is revealed (motion hides them)
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
