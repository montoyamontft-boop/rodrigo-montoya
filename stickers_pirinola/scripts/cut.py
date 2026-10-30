"""Separa la pirinola + anillos del fondo degradado -> RGBA (foreground desmezclado)."""
import sys, numpy as np, cv2
from PIL import Image

src, msk, out = sys.argv[1:4]
S = 2048
P = np.asarray(Image.open(src).convert('RGB').resize((S, S), Image.LANCZOS), np.float32)
M = np.asarray(Image.open(msk).convert('L').resize((S, S), Image.LANCZOS), np.float32) / 255

# fondo: ajuste polinomial suave con los pixeles claramente de fondo
yy, xx = np.mgrid[0:S, 0:S].astype(np.float32) / S
bgsel = cv2.erode((M < 0.05).astype(np.uint8), np.ones((25, 25)))
if len(sys.argv) > 4:  # zona del texto excluida
    bgsel[:int(float(sys.argv[4]) * S)] = 0
idx = np.nonzero(bgsel[::4, ::4]); X = xx[::4, ::4][idx]; Y = yy[::4, ::4][idx]
def basis(x, y): return np.stack([x**i * y**j for i in range(4) for j in range(4 - i)], -1)
A = basis(X, Y); B = np.zeros_like(P)
for c in range(3):
    coef, *_ = np.linalg.lstsq(A, P[::4, ::4, c][idx], rcond=None)
    B[..., c] = basis(xx, yy) @ coef

D = P - B
d = np.abs(D).max(-1)
alpha = np.clip((d - 14) / 70, 0, 1)
# cuerpo oscuro de la pirinola -> opaco
lum = P.mean(-1)
dark = ((lum < 110) & (M > 0.5)).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(dark)
dark = (lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])).astype(np.uint8)
dark = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (45, 45)))
ff = dark.copy(); cv2.floodFill(ff, np.zeros((S + 2, S + 2), np.uint8), (0, 0), 1)
dark = dark | (1 - ff)
dark = cv2.morphologyEx(dark, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
body = cv2.GaussianBlur(dark.astype(np.float32), (0, 0), 1.5)
gate = cv2.GaussianBlur(cv2.dilate((M > 0.15).astype(np.float32), np.ones((31, 31))), (0, 0), 8)
alpha = np.maximum(alpha * gate, body)
alpha = cv2.GaussianBlur(alpha, (0, 0), 0.8)
F = np.clip(B + D / np.maximum(alpha, 0.05)[..., None], 0, 255)
# anillos: llevar el color hacia una rampa cian luminosa
L = F.mean(-1, keepdims=True) / 255
ramp = np.clip(np.concatenate([L * 1.6 - 0.55, L * 1.25 - 0.05, L * 0.5 + 0.55], -1), 0, 1) * 255
F = F * 0.4 + ramp * 0.6
F = F * (1 - body[..., None]) + P * body[..., None]
rgba = np.dstack([F, alpha * 255]).round().astype(np.uint8)
Image.fromarray(rgba, 'RGBA').save(out)
Image.fromarray(np.clip(B, 0, 255).astype(np.uint8)).save(out.replace('.png', '_bg.png'))
