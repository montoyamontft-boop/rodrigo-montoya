"""Animación en loop de la pirinola girando. Genera cuadros RGBA (transparentes) y sobre fondo."""
import os, sys, numpy as np, cv2
from PIL import Image

OUT = sys.argv[1]; os.makedirs(OUT + '/t', exist_ok=True); os.makedirs(OUT + '/f', exist_ok=True)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 72      # cuadros por loop (30 fps)
C = 1080                                               # lienzo
fg = np.asarray(Image.open('fg1.png'), np.float32) / 255
S = fg.shape[0]
A = fg[..., 3]; RGB = fg[..., :3]

# --- máscara del cuerpo (misma lógica que cut.py) ---
P = RGB * 255; lum = P.mean(-1)
dark = ((lum < 110) & (A > 0.95)).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(dark)
dark = (lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])).astype(np.uint8)
dark = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (45, 45)))
ff = dark.copy(); cv2.floodFill(ff, np.zeros((S + 2, S + 2), np.uint8), (0, 0), 1)
dark = dark | (1 - ff)
dark = cv2.morphologyEx(dark, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
body = cv2.GaussianBlur(dark.astype(np.float32), (0, 0), 1.2)
hide = cv2.dilate(dark, np.ones((7, 7))).astype(np.float32)

# --- anillos: premultiplicado, sin el cuerpo ---
ra = A * (1 - hide)
ring = np.dstack([RGB * ra[..., None], ra])

# elipse por momentos ponderados
ys, xs = np.nonzero(ra > 0.25); w = ra[ys, xs]
cx, cy = np.average(xs, weights=w), np.average(ys, weights=w)
cov = np.cov(np.stack([xs - cx, ys - cy]), aweights=w)
ev, evec = np.linalg.eigh(cov)
ang = np.arctan2(evec[1, 1], evec[0, 1])               # eje mayor
ratio = np.sqrt(ev[0] / ev[1])                          # menor/mayor
R = int(np.percentile(np.hypot(xs - cx, ys - cy) * 1.0, 99.5) / ratio * 1.05) if False else None
ca, sa = np.cos(ang), np.sin(ang)
# imagen -> espacio círculo: rotar -ang, estirar eje menor
def to_circle(x, y):
    u = (x - cx) * ca + (y - cy) * sa; v = (-(x - cx) * sa + (y - cy) * ca) / ratio
    return u, v
u, v = to_circle(xs, ys); R = int(np.percentile(np.hypot(u, v), 99.8) * 1.04)
K = 2 * R
# matriz afín imagen->círculo (centrada en R,R)
Mc = np.array([[ca, sa, 0], [-sa / ratio, ca / ratio, 0]], np.float64)
Mc[:, 2] = -Mc[:, :2] @ [cx, cy] + R
circ = cv2.warpAffine(ring, Mc, (K, K), flags=cv2.INTER_LINEAR)
hid_c = cv2.warpAffine(hide, Mc, (K, K), flags=cv2.INTER_LINEAR)
# polar: filas = ángulo (720), columnas = radio
NA = 1440
pol = cv2.warpPolar(circ, (R, NA), (R, R), R, cv2.WARP_POLAR_LINEAR)
hp = cv2.warpPolar(hid_c, (R, NA), (R, R), R, cv2.WARP_POLAR_LINEAR)[..., None]
opp = np.roll(pol, NA // 2, 0); hop = np.roll(hp, NA // 2, 0)
pol = pol * (1 - hp) + opp * hp * (1 - hop)             # rellenar lo oculto con el lado opuesto
pol *= np.clip((0.97 - np.arange(R) / R) / 0.15, 0, 1)[None, :, None]
# frente / fondo en espacio círculo
yy, xx = np.mgrid[0:K, 0:K].astype(np.float32)
front_c = np.clip((yy - R) / (0.12 * R) + 0.5, 0, 1)
Mi = cv2.invertAffineTransform(Mc)

# --- encuadre de salida ---
th = np.linspace(0, 2 * np.pi, 360)
eu, ev_ = 0.8 * R * np.cos(th), 0.8 * R * np.sin(th)
ex = cx + eu * ca - ev_ * ratio * sa; ey = cy + eu * sa + ev_ * ratio * ca
yb, xb = np.nonzero(dark)
x0, x1 = min(xb.min(), ex.min()), max(xb.max(), ex.max()); y0, y1 = min(yb.min(), ey.min()), max(yb.max(), ey.max())
sc = 0.92 * C / max(x1 - x0, y1 - y0)
ox = C / 2 - sc * (x0 + x1) / 2; oy = C / 2 - sc * (y0 + y1) / 2 + 10
Mo = np.array([[sc, 0, ox], [0, sc, oy]])
def place(img, M=None):
    M2 = Mo if M is None else np.vstack([Mo, [0, 0, 1]])[:2] @ np.vstack([M, [0, 0, 1]])
    return cv2.warpAffine(img, M2, (C, C), flags=cv2.INTER_AREA if M is None else cv2.INTER_LINEAR)
def compose(M):  # matriz de imagen fuente -> salida
    return (np.vstack([Mo, [0, 0, 1]]) @ np.vstack([M, [0, 0, 1]]))[:2]

# cuerpo premultiplicado + geometría para brillos
bodyimg = np.dstack([RGB * body[..., None], body])
by, bx = np.nonzero(dark)
tip = np.array([bx[by == by.max()].mean(), by.max()])   # punta inferior (pivote)
rows = np.arange(by.min(), by.max() + 1)
lft = np.full(S, np.nan); rgt = np.full(S, np.nan)
for r in rows:
    xr = bx[by == r]
    if len(xr): lft[r], rgt[r] = xr.min(), xr.max()
ok = ~np.isnan(lft)
from scipy.ndimage import gaussian_filter1d
for arr in (lft, rgt):
    arr[ok] = gaussian_filter1d(arr[ok], 6)
mid = (lft + rgt) / 2; hw = (rgt - lft) / 2
xxS = np.arange(S)[None, :].astype(np.float32)

# sombra / resplandor de piso
ring_sc = cv2.warpAffine(ra, Mo, (C, C), flags=cv2.INTER_AREA)
rng = np.random.default_rng(7)
NS = 46
sp_r = rng.uniform(0.45, 1.08, NS); sp_a = rng.uniform(0, 2 * np.pi, NS)
sp_k = rng.choice([1, 2, 2, 3], NS); sp_s = rng.uniform(1.5, 4.5, NS); sp_ph = rng.uniform(0, 2 * np.pi, NS)
sp_tw = rng.choice([1, 2, 3], NS)

def over(dst, src):  # premultiplicado
    return src + dst * (1 - src[..., 3:4])

def bg_frame(t):
    # fondo: degradado radial verde azulado profundo + halo cian que respira
    g = np.hypot((xx_o - C / 2) / C, (yy_o - C * 0.55) / C)
    base = np.stack([np.interp(g, [0, .75], [18, 4]), np.interp(g, [0, .75], [62, 14]), np.interp(g, [0, .75], [74, 24])], -1)
    return base / 255
yy_o, xx_o = np.mgrid[0:C, 0:C].astype(np.float32)
BG = bg_frame(0)

def dot_layer(pts, sizes, inten):
    L = np.zeros((C, C), np.float32)
    for (x, y), s_, i in zip(pts, sizes, inten):
        if i <= 0.01: continue
        x0_, y0_ = int(max(0, x - 6 * s_)), int(max(0, y - 6 * s_)); x1_, y1_ = int(min(C, x + 6 * s_)), int(min(C, y + 6 * s_))
        if x1_ <= x0_ or y1_ <= y0_: continue
        gx, gy = np.meshgrid(np.arange(x0_, x1_), np.arange(y0_, y1_))
        d2 = ((gx - x) ** 2 + (gy - y) ** 2) / s_ ** 2
        star = np.exp(-d2) + 0.35 * np.exp(-((gx - x) ** 2) / (0.15 * s_) ** 2 - ((gy - y) ** 2) / (3 * s_) ** 2) \
               + 0.35 * np.exp(-((gy - y) ** 2) / (0.15 * s_) ** 2 - ((gx - x) ** 2) / (3 * s_) ** 2)
        L[y0_:y1_, x0_:x1_] += i * star
    return np.clip(L, 0, 1)

Mring = compose(Mi)
disc_y = (Mo @ [0, cy + 0.0, 1])[1]
FRONT_O = cv2.warpAffine(front_c, Mring, (C, C), flags=cv2.INTER_LINEAR) * np.clip((yy_o - disc_y + 10) / 40, 0, 1)
REV = 2           # vueltas de los anillos por loop
SWEEP = 6         # pasadas de brillo sobre el cuerpo por loop
for f in range(N):
    t = f / N
    # anillos girados con desenfoque de movimiento
    acc = np.zeros_like(pol)
    for k in range(5):
        sh = int(round((t + k * 0.0022) * REV * NA)) % NA
        acc += np.roll(pol, sh, 0)
    acc /= 5
    cc = cv2.warpPolar(acc, (K, K), (R, R), R, cv2.WARP_POLAR_LINEAR + cv2.WARP_INVERSE_MAP)
    pulse = 1 + 0.12 * np.sin(2 * np.pi * t * 2)
    Mring = compose(Mi)
    full_o = cv2.warpAffine(cc, Mring, (C, C), flags=cv2.INTER_LINEAR)
    fm = FRONT_O[..., None]
    back_o = full_o * (1 - fm); front_o = full_o * fm
    ringsum = back_o[..., 3] + front_o[..., 3]

    # cuerpo: bamboleo de precesión alrededor de la punta + brillos que lo recorren
    wob = 2.2 * np.sin(2 * np.pi * t * 2); dx = 6 * np.sin(2 * np.pi * t * 2 + 1.2)
    Mw = cv2.getRotationMatrix2D((float(tip[0]), float(tip[1])), wob, 1.0); Mw[0, 2] += dx
    hl = np.zeros((S, S), np.float32)
    for j in range(3):
        p = 2 * np.pi * (t * SWEEP + j / 3)
        vis = np.cos(p)
        if vis <= 0: continue
        cxr = mid + hw * np.sin(p); wid = 0.10 * hw + 4
        band = np.exp(-((xxS - np.nan_to_num(cxr, nan=-1e4)[:, None]) / np.nan_to_num(wid, nan=1)[:, None]) ** 2)
        hl += vis ** 1.5 * band
    hl = np.clip(hl * dark, 0, 1) * 0.36
    bimg = bodyimg.copy(); bimg[..., :3] = np.clip(bimg[..., :3] + hl[..., None] * np.array([0.75, 0.95, 1.0]) * body[..., None], 0, None)
    body_o = cv2.warpAffine(bimg, compose(Mw), (C, C), flags=cv2.INTER_AREA)

    # resplandor y destellos
    glow = cv2.GaussianBlur(ringsum, (0, 0), 22) * 0.85 * pulse
    glow2 = cv2.GaussianBlur(ringsum, (0, 0), 6) * 0.35 * pulse
    tipo = Mo @ [*tip, 1]
    floor = np.exp(-(((xx_o - tipo[0]) / 70) ** 2 + ((yy_o - tipo[1] - 6) / 14) ** 2))
    pts, sz, it = [], [], []
    for i in range(NS):
        a = sp_a[i] + 2 * np.pi * sp_k[i] * t
        u_, v_ = sp_r[i] * R * np.cos(a), sp_r[i] * R * np.sin(a)
        X = Mring @ [u_ + R, v_ + R, 1]
        pts.append(X); sz.append(sp_s[i]); it.append(max(0, np.sin(2 * np.pi * sp_tw[i] * t + sp_ph[i])) ** 2 * (0.5 + 0.5 * (np.sin(a) > -0.2)))
    dots = dot_layer(pts, sz, it)

    cyan = np.array([0.25, 0.85, 1.0], np.float32)
    add = glow[..., None] * cyan + glow2[..., None] * cyan + dots[..., None] * np.array([0.8, 0.97, 1.0]) + floor[..., None] * cyan * 0.6

    # capa transparente (premultiplicada)
    L = np.zeros((C, C, 4), np.float32)
    L = over(L, back_o); L = over(L, body_o); L = over(L, front_o)
    addA = np.clip(add.max(-1), 0, 1)
    T = L.copy(); T[..., :3] += add * (1 - L[..., 3:4]) ; T[..., 3] = np.clip(L[..., 3] + addA * (1 - L[..., 3]), 0, 1)
    T[..., :3] = np.minimum(T[..., :3], T[..., 3:4])
    alpha = np.maximum(T[..., 3:4], 1e-4)
    Image.fromarray((np.dstack([np.clip(T[..., :3] / alpha, 0, 1), T[..., 3:4]]) * 255 + .5).astype(np.uint8), 'RGBA').save(f'{OUT}/t/{f:03d}.png')
    # sobre fondo: luz aditiva (screen) + capas
    B = BG + add * 0.9
    B = B * (1 - L[..., 3:4]) + L[..., :3]
    B = 1 - (1 - B) * (1 - np.clip(dots[..., None] * 0.6 * np.array([0.8, 0.97, 1.0]), 0, 1))
    Image.fromarray((np.clip(B, 0, 1) * 255 + .5).astype(np.uint8)).save(f'{OUT}/f/{f:03d}.png')
    print(f, end=' ', flush=True)
