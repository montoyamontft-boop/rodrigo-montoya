"""Animate the scene layers and encode the video.

usage:
  python render.py LAYERS_DIR OUT.mp4 [--scale 1.0] [--workers 3] [--crf 16]
  python render.py LAYERS_DIR --stills DIR --times 1.0,2.5   (debug frames)

scale 1.0 -> 3840x2160, 0.5 -> 1920x1080. Constant 30 fps.
"""
import argparse, json, math, os, subprocess, sys, tempfile
from functools import lru_cache
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenes import SCENES, FPS, OVERLAP

PT = 2.0  # output px per pt at scale 1.0

# ---------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x

EASE = {
    "linear": lambda p: p,
    "outQuad": lambda p: 1 - (1 - p) ** 2,
    "outCubic": lambda p: 1 - (1 - p) ** 3,
    "outQuart": lambda p: 1 - (1 - p) ** 4,
    "outQuint": lambda p: 1 - (1 - p) ** 5,
    "outExpo": lambda p: 1.0 if p >= 1 else 1 - 2 ** (-10 * p),
    "inOutExpo": lambda p: 0.0 if p <= 0 else 1.0 if p >= 1 else
        (2 ** (20 * p - 10) / 2 if p < 0.5 else (2 - 2 ** (-20 * p + 10)) / 2),
    "inOutQuart": lambda p: 8 * p ** 4 if p < 0.5 else 1 - (-2 * p + 2) ** 4 / 2,
    "inQuart": lambda p: p ** 4,
    "inCubic": lambda p: p ** 3,
    "inOutCubic": lambda p: 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2,
    "inOutSine": lambda p: -(math.cos(math.pi * p) - 1) / 2,
    # gentle overshoot (~3%), no bounce
    "outBack": lambda p: 1 + 2.2 * (p - 1) ** 3 + 1.2 * (p - 1) ** 2,
}

# ---------------------------------------------------------------- timeline
def timeline():
    starts, t = [], 0.0
    for sc in SCENES:
        starts.append(t)
        t += sc["dur"] - OVERLAP
    total = starts[-1] + SCENES[-1]["dur"]
    return starts, total


FADE_IN = 0.8      # first scene from black
FADE_OUT = 1.4     # last scene to black

# Energy of the entries: offsets are amplified, durations shortened, and
# entries start once the incoming transition has mostly landed.
OFFSET_GAIN = 1.8
SCALE_GAIN = 1.6
DUR_GAIN = 0.78
ENTRY_DELAY = 0.15
BG_GAIN = 2.0          # background settle amplitude (start scale - 1) x gain
CAM_IN = 1.07          # whole-scene camera settle at the start of each scene
CAM_IN_DUR = 1.8

# Transition between scene i and i+1 (len = scenes - 1)
TRANSITIONS = ["bar", "push_l", "zoom", "push_l", "push_d", "zoom",
               "bar", "push_l", "push_d", "zoom", "push_l"]
SHUTTER_SAMPLES = 12   # motion-blur sub-samples during transitions (180 deg shutter)


class Scene:
    def __init__(self, idx, spec, man, layers_dir, scale):
        self.idx, self.spec, self.scale = idx, spec, scale
        self.dur = spec["dur"]
        self.last = idx == len(SCENES) - 1
        self.first = idx == 0
        self.k = scale  # layer px -> output px
        self.W = int(round(man["size"][0] * scale))
        self.H = int(round(man["size"][1] * scale))
        self.groups = {g["name"]: g for g in spec["groups"]}
        self.bboxes = {k: [v * scale for v in b] for k, b in man["bboxes"].items()}
        self.layers = []
        for L in man["layers"]:
            im = Image.open(os.path.join(layers_dir, L["file"])).convert("RGBA")
            x, y = L["x"] * scale, L["y"] * scale
            if scale != 1.0:
                # resample onto the scaled grid, keeping sub-pixel origin exact
                fx, fy = math.floor(x), math.floor(y)
                w = int(math.ceil(x + L["w"] * scale)) - fx + 1
                h = int(math.ceil(y + L["h"] * scale)) - fy + 1
                im = im.convert("RGBa").transform(
                    (w, h), Image.AFFINE,
                    (1 / scale, 0, (fx - x) / scale, 0, 1 / scale, (fy - y) / scale),
                    resample=Image.BICUBIC)
                x, y = fx, fy
            else:
                im = im.convert("RGBa")
            self.layers.append(dict(group=L["group"], im=im, x=int(x), y=int(y)))
        # exit ordering: same order as entry
        fg = sorted([g for g in spec["groups"] if "bg" not in g], key=lambda g: g.get("t", 0))
        self.exit_rank = {g["name"]: i / max(1, len(fg) - 1) for i, g in enumerate(fg)}
        self.hold_end = self.dur - OVERLAP if not self.last else self.dur - FADE_OUT

    # state of a group at scene-local time t -> (opacity, scale, anchor, dx, dy, wipe)
    def group_state(self, name, t):
        g = self.groups.get(name, {"name": name, "bg": 1.0})
        bb = self.bboxes.get(name, [0, 0, self.W, self.H])
        if "bg" in g:
            p = clamp(t / self.hold_end)
            s = 1 + (g["bg"] - 1) * BG_GAIN * (1 - EASE["outCubic"](p))
            return dict(op=1.0, s=s, ax=self.W / 2, ay=self.H / 2, dx=0, dy=0, wipe=None, clip=None)
        t0 = g.get("t", 0) * DUR_GAIN + ENTRY_DELAY
        d = g.get("d", 0.8) * DUR_GAIN
        p = clamp((t - t0) / d)
        ease = g.get("ease", "outExpo")
        if ease in ("outCubic", "outQuart"):
            ease = "outExpo"
        e = EASE[ease](p)
        if g.get("wipe"):
            op = 1.0 if p > 0 else 0.0
        elif g.get("mask"):
            op = EASE["outQuad"](clamp(p / 0.35))
        else:
            op = EASE["outQuad"](clamp(p / 0.45))
        k = PT * self.scale * OFFSET_GAIN
        dx = g.get("dx", 0) * k * (1 - e)
        dy = g.get("dy", 0) * k * (1 - e)
        s0 = g.get("s0", 1.0)
        s0 = max(0.2, 1 + (s0 - 1) * SCALE_GAIN)
        s = 1 + (s0 - 1) * (1 - e)
        ax, ay = anchor(bb, g.get("anchor", "c"))
        wipe = (g["wipe"], EASE[g.get("ease", "inOutCubic")](p), bb) if g.get("wipe") else None
        clip = bb if g.get("mask") else None
        return dict(op=op, s=s, ax=ax, ay=ay, dx=dx, dy=dy, wipe=wipe, clip=clip)

    def camera(self, t):
        """Whole-scene settle: starts slightly pushed in, lands on exactly 1.0."""
        return 1 + (CAM_IN - 1) * (1 - EASE["outExpo"](clamp(t / CAM_IN_DUR)))

    def scene_alpha(self, t):
        a = 1.0
        if self.first:
            a *= EASE["inOutSine"](clamp(t / FADE_IN))
        if self.last:
            a *= 1 - EASE["inOutSine"](clamp((t - (self.dur - FADE_OUT)) / FADE_OUT))
        return a

    def render(self, t):
        """Premultiplied float32 RGB + alpha buffer of this scene at local time t."""
        W, H = self.W, self.H
        # white paper, as the PDF is displayed
        rgb = np.full((H, W, 3), 255.0, np.float32)
        alpha = np.ones((H, W), np.float32)
        cam = self.camera(t)
        cx, cy = W / 2, H / 2
        cache = {}
        for L in self.layers:
            gname = L["group"]
            st = cache.get(gname) or cache.setdefault(gname, self.group_state(gname, t))
            if st["op"] <= 0.002:
                continue
            if st["wipe"] and st["wipe"][1] <= 0:
                continue
            k = cam * st["s"]
            bx = cam * (st["s"] * -st["ax"] + st["ax"] + st["dx"] - cx) + cx
            by = cam * (st["s"] * -st["ay"] + st["ay"] + st["dy"] - cy) + cy
            im, x0, y0 = L["im"], L["x"], L["y"]
            w, h = im.size
            ident = abs(k - 1) < 1e-9 and abs(bx - round(bx)) < 1e-6 and abs(by - round(by)) < 1e-6
            if ident:
                ox, oy = x0 + int(round(bx)), y0 + int(round(by))
                src = im
            else:
                fx0 = k * x0 + bx
                fy0 = k * y0 + by
                ox, oy = math.floor(fx0), math.floor(fy0)
                ow = int(math.ceil(fx0 + k * w)) - ox + 1
                oh = int(math.ceil(fy0 + k * h)) - oy + 1
                src = im.transform((ow, oh), Image.AFFINE,
                                   (1 / k, 0, (ox - fx0) / k, 0, 1 / k, (oy - fy0) / k),
                                   resample=Image.BICUBIC)
            sw, sh = src.size
            # visible region
            rx0, ry0 = max(ox, 0), max(oy, 0)
            rx1, ry1 = min(ox + sw, W), min(oy + sh, H)
            if st["clip"]:
                cb = st["clip"]
                pad = 2
                c0x = cam * (cb[0] - pad - cx) + cx
                c0y = cam * (cb[1] - pad - cy) + cy
                c1x = cam * (cb[2] + pad - cx) + cx
                c1y = cam * (cb[3] + pad - cy) + cy
                rx0, ry0 = max(rx0, int(math.floor(c0x))), max(ry0, int(math.floor(c0y)))
                rx1, ry1 = min(rx1, int(math.ceil(c1x))), min(ry1, int(math.ceil(c1y)))
            if rx1 <= rx0 or ry1 <= ry0:
                continue
            # src is premultiplied (RGBa): colour in 0..255 already scaled by alpha
            a = np.asarray(src, dtype=np.float32)[ry0 - oy:ry1 - oy, rx0 - ox:rx1 - ox]
            f = st["op"]
            if st["wipe"]:
                f = f * wipe_mask(st["wipe"], rx0, ry0, rx1, ry1, cam, cx, cy, self.scale)[..., None]
            a = a * f
            sa = a[..., 3] / 255.0
            inv = 1 - sa
            rgb[ry0:ry1, rx0:rx1] = a[..., :3] + rgb[ry0:ry1, rx0:rx1] * inv[..., None]
            alpha[ry0:ry1, rx0:rx1] = sa + alpha[ry0:ry1, rx0:rx1] * inv
        return rgb, alpha


def shift(img, dx, dy):
    """Integer translation of a full frame, uncovered area left black (never visible)."""
    H, W = img.shape[:2]
    out = np.zeros_like(img)
    xs0, xs1 = max(0, -dx), min(W, W - dx)
    ys0, ys1 = max(0, -dy), min(H, H - dy)
    if xs1 > xs0 and ys1 > ys0:
        out[ys0 + dy:ys1 + dy, xs0 + dx:xs1 + dx] = img[ys0:ys1, xs0:xs1]
    return out


def zoom(img, k):
    """Scale a full frame about its centre (k >= 1 keeps the frame covered)."""
    if abs(k - 1) < 1e-4:
        return img
    H, W = img.shape[:2]
    im = Image.fromarray(np.clip(img + 0.5, 0, 255).astype(np.uint8))
    cx, cy = W / 2, H / 2
    im = im.transform((W, H), Image.AFFINE, (1 / k, 0, cx - cx / k, 0, 1 / k, cy - cy / k),
                      resample=Image.BILINEAR)
    return np.asarray(im, np.float32)


def transition(kind, a, b, p, bar):
    """Combine outgoing frame a and incoming frame b at progress p in [0, 1]."""
    H, W = a.shape[:2]
    if p <= 0:
        return a
    if p >= 1:
        return b
    if kind == "push_l":          # camera travels right: a exits left, b enters from right
        e = EASE["inOutQuart"](p)
        off = int(round(e * W))
        out = shift(a, -off, 0)
        out[:, W - off:] = b[:, :off] if off else out[:, W:]
        return out
    if kind == "push_d":          # hanging signs: b drops in from above, a falls out below
        e = EASE["inOutQuart"](p)
        off = int(round(e * H))
        out = shift(a, 0, off)
        if off:
            out[:off] = b[H - off:]
        return out
    if kind == "zoom":            # zoom through: a rushes forward and dissolves into b
        ea = EASE["inQuart"](p)
        eb = EASE["outExpo"](clamp((p - 0.25) / 0.75))
        A = zoom(a, 1 + 0.6 * ea)
        B = zoom(b, 1.18 - 0.18 * eb)
        f = EASE["inOutSine"](clamp((p - 0.2) / 0.6))
        return A * (1 - f) + B * f
    if kind == "bar":             # the deck's gradient bar sweeps across, revealing b
        band, tail = bar
        e = EASE["inOutQuart"](p)
        bw, tw = int(W * 0.42), int(W * 0.10)
        slant = 0.45
        lead = -tw - int(H * slant) + e * (W + bw + tw + 2 * int(H * slant))
        xs = np.arange(W, dtype=np.float32)[None, :]
        ys = np.arange(H, dtype=np.float32)[:, None]
        edge = lead + (H - ys) * slant        # leading edge leans like the deck's bar ends
        u = edge - xs                          # distance behind the leading edge
        out = np.where((u < 0)[..., None], zoom(a, 1 + 0.05 * e), 0)
        m_tail = (u >= 0) & (u < tw)
        m_band = (u >= tw) & (u < tw + bw)
        m_in = u >= tw + bw
        out = out + m_tail[..., None] * tail[None, None, :]
        idx = np.clip(((u - tw) / bw * (len(band) - 1)).astype(np.int32), 0, len(band) - 1)
        # gradient runs red (trailing) -> magenta (towards the tail), as on slide 1
        idx = len(band) - 1 - idx
        out = np.where(m_band[..., None], band[idx], out)
        out = np.where(m_in[..., None], b, out)
        return out.astype(np.float32)
    raise ValueError(kind)


def anchor(bb, a):
    x0, y0, x1, y1 = bb
    xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
    return {"c": (xm, ym), "b": (xm, y1), "t": (xm, y0), "l": (x0, ym), "r": (x1, ym),
            "tl": (x0, y0), "tr": (x1, y0), "bl": (x0, y1), "br": (x1, y1)}[a]


def wipe_mask(wipe, rx0, ry0, rx1, ry1, cam, cx, cy, scale):
    d, p, bb = wipe
    x0, y0, x1, y1 = [cam * (v - c) + c for v, c in zip(bb, (cx, cy, cx, cy))]
    feather = 48 * scale
    if d in ("l", "r"):
        xs = np.arange(rx0, rx1, dtype=np.float32) + 0.5
        span = (x1 - x0) + feather
        if d == "l":
            edge = x0 - feather + p * span
            m = np.clip((edge - xs) / feather + 1, 0, 1) if p < 1 else np.ones_like(xs)
        else:
            edge = x1 + feather - p * span
            m = np.clip((xs - edge) / feather + 1, 0, 1) if p < 1 else np.ones_like(xs)
        return np.broadcast_to(m[None, :], (ry1 - ry0, rx1 - rx0))
    ys = np.arange(ry0, ry1, dtype=np.float32) + 0.5
    span = (y1 - y0) + feather
    if d == "u":   # reveal from bottom upwards
        edge = y1 + feather - p * span
        m = np.clip((ys - edge) / feather + 1, 0, 1) if p < 1 else np.ones_like(ys)
    else:          # from top downwards
        edge = y0 - feather + p * span
        m = np.clip((edge - ys) / feather + 1, 0, 1) if p < 1 else np.ones_like(ys)
    return np.broadcast_to(m[:, None], (ry1 - ry0, rx1 - rx0))


class Film:
    def __init__(self, layers_dir, scale):
        self.man = json.load(open(os.path.join(layers_dir, "manifest.json")))
        self.dir, self.scale = layers_dir, scale
        self.starts, self.total = timeline()
        self.cache = {}

    def scene(self, i):
        if i not in self.cache:
            # keep at most 2 scenes in memory
            for k in list(self.cache):
                if abs(k - i) > 1:
                    del self.cache[k]
            self.cache[i] = Scene(i, SCENES[i], self.man[i], self.dir, self.scale)
        return self.cache[i]

    def scene_rgb(self, i, T):
        sc = self.scene(i)
        t = T - self.starts[i]
        rgb, _ = sc.render(t)
        return rgb * sc.scene_alpha(t)

    def frame(self, T):
        active = [i for i, s in enumerate(self.starts) if s <= T < s + SCENES[i]["dur"]]
        if not active:
            active = [len(SCENES) - 1]
        if len(active) == 1:
            out = self.scene_rgb(active[0], T)
        else:
            i = active[0]
            t0 = self.starts[i + 1]
            a = self.scene_rgb(i, T)
            b = self.scene_rgb(i + 1, T)
            kind = TRANSITIONS[i]
            # motion blur: average the transition geometry over a 180 deg shutter
            acc = np.zeros_like(a)
            n = SHUTTER_SAMPLES
            for k in range(n):
                ts = T + ((k + 0.5) / n - 0.5) * 0.5 / FPS
                p = clamp((ts - t0) / OVERLAP)
                acc += transition(kind, a, b, p, self.bar_colors())
            out = acc / n
        return np.clip(out + 0.5, 0, 255).astype(np.uint8)

    def bar_colors(self):
        """Gradient band + navy tail sampled from the deck's own title bar (slide 1)."""
        if not hasattr(self, "_bar"):
            man = self.man[0]
            band = tail = None
            for L in man["layers"]:
                im = np.asarray(Image.open(os.path.join(self.dir, L["file"])).convert("RGB"), np.float32)
                if L["group"] == "bar":
                    row = im[im.shape[0] // 2]
                    a = np.asarray(Image.open(os.path.join(self.dir, L["file"])))[im.shape[0] // 2, :, 3]
                    band = row[a > 250]
                elif L["group"] == "bartail":
                    a = np.asarray(Image.open(os.path.join(self.dir, L["file"])))[..., 3]
                    tail = im[a > 250].mean(0)
            self._bar = (band, tail)
        return self._bar

    def nframes(self):
        return int(round(self.total * FPS))


def encode_segment(args):
    layers_dir, scale, f0, f1, path, crf = args
    film = Film(layers_dir, scale)
    W, H = int(3840 * scale), int(2160 * scale)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           # convert RGB -> YUV with the BT.709 matrix the file is tagged with
           "-vf", "scale=out_color_matrix=bt709:out_range=tv",
           "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-tune", "animation",
           "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
           "-color_trc", "bt709", "-color_range", "tv", "-threads", "2", path]
    if os.path.exists(path):
        return path  # finished in an earlier (interrupted) run
    part = path[:-4] + ".part.mp4"
    cmd[-1] = part
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(f0, f1):
        p.stdin.write(film.frame(f / FPS).tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError("ffmpeg failed")
    os.replace(part, path)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("layers")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--crf", type=int, default=16)
    ap.add_argument("--stills")
    ap.add_argument("--times")
    ap.add_argument("--range")
    a = ap.parse_args()
    if a.stills:
        os.makedirs(a.stills, exist_ok=True)
        film = Film(a.layers, a.scale)
        for ts in a.times.split(","):
            T = float(ts)
            Image.fromarray(film.frame(T)).save(os.path.join(a.stills, f"t{T:07.3f}.png"))
        return
    starts, total = timeline()
    n = int(round(total * FPS))
    f0, f1 = 0, n
    if a.range:
        s, e = a.range.split(":")
        f0, f1 = int(float(s) * FPS), min(n, int(float(e) * FPS))
    # split on scene boundaries-ish: equal chunks
    chunks = max(a.workers * 8, 1)
    step = math.ceil((f1 - f0) / chunks)
    # fixed segment folder so an interrupted render resumes where it stopped
    tmp = os.path.abspath(a.out) + f".segments709_{f0}_{f1}_{a.scale}_{a.crf}"
    os.makedirs(tmp, exist_ok=True)
    jobs = [(a.layers, a.scale, s, min(s + step, f1), os.path.join(tmp, f"seg{j:03d}.mp4"), a.crf)
            for j, s in enumerate(range(f0, f1, step))]
    print(f"{f1-f0} frames, {(f1-f0)/FPS:.2f}s, {len(jobs)} segments", flush=True)
    from multiprocessing import Pool
    with Pool(a.workers) as pool:
        for k, path in enumerate(pool.imap(encode_segment, jobs)):
            print(f"  segment {k+1}/{len(jobs)} done", flush=True)
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as fh:
        for j in jobs:
            fh.write(f"file '{j[4]}'\n")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                           "-i", lst, "-c", "copy", "-movflags", "+faststart", a.out])
    for j in jobs:
        os.remove(j[4])
    os.remove(lst)
    os.rmdir(tmp)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
