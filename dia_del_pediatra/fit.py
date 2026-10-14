"""Measure the flattened geometry of the backgrounds (PDF pt = source px):
centre of each family of concentric white rings, and the circle of each
photo's curved edge. Prints values used in layout.py.

python fit.py BG1.png BG2.png BG3.png
"""
import sys
import numpy as np
import cv2


def ring_center(img, box):
    x0, y0, x1, y1 = box
    im = img[y0:y1, x0:x1].astype(np.float32)
    hsv = cv2.cvtColor(img[y0:y1, x0:x1], cv2.COLOR_RGB2HSV).astype(np.float32)
    L = im.mean(-1)
    white = ((L > 238) & (hsv[..., 1] < 22)).astype(np.float32)
    w = cv2.GaussianBlur(white, (0, 0), 2)
    gx = cv2.Sobel(w, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(w, cv2.CV_32F, 0, 1, ksize=3)
    mag = np.hypot(gx, gy)
    ys, xs = np.nonzero(mag > 0.25 * mag.max())
    nx, ny = gx[ys, xs] / mag[ys, xs], gy[ys, xs] / mag[ys, xs]
    px, py = xs + x0, ys + y0
    # least-squares point closest to all normal lines
    A = np.zeros((2, 2)); b = np.zeros(2)
    for _ in range(3):
        # line through p with direction n: (I - n n^T)(c - p) = 0
        P = np.stack([np.stack([1 - nx * nx, -nx * ny], -1), np.stack([-nx * ny, 1 - ny * ny], -1)], 1)
        A = P.sum(0)
        b = (P @ np.stack([px, py], -1)[..., None])[..., 0].sum(0)
        c = np.linalg.solve(A, b)
        # drop outliers
        r = np.abs((px - c[0]) * ny - (py - c[1]) * nx)
        k = r < np.percentile(r, 70)
        px, py, nx, ny = px[k], py[k], nx[k], ny[k]
    rad = np.hypot(px - c[0], py - c[1])
    return c, (rad.min(), rad.max(), len(px))


def arc_circle(img, rgb, tol, box):
    x0, y0, x1, y1 = box
    sub = img[y0:y1, x0:x1].astype(np.float32)
    m = np.abs(sub - np.array(rgb, np.float32)).max(-1) < tol
    ys, xs = np.nonzero(m)
    xs = xs + x0; ys = ys + y0
    # outermost (rightmost) pixel per row = the edge of the arc
    pts = {}
    for x, y in zip(xs, ys):
        if x > pts.get(y, -1):
            pts[y] = x
    Y = np.array(list(pts)); X = np.array([pts[y] for y in Y])
    A = np.stack([X, Y, np.ones_like(X)], -1).astype(np.float64)
    bb = -(X ** 2 + Y ** 2).astype(np.float64)
    a, b2, c = np.linalg.lstsq(A, bb, rcond=None)[0]
    cx, cy = -a / 2, -b2 / 2
    R = np.sqrt(cx * cx + cy * cy - c)
    res = np.abs(np.hypot(X - cx, Y - cy) - R)
    return (cx, cy, R), res.mean(), len(X)


if __name__ == "__main__":
    bgs = [cv2.cvtColor(cv2.imread(f), cv2.COLOR_BGR2RGB) for f in sys.argv[1:4]]
    print("p1 rings TR", ring_center(bgs[0], (1500, 0, 1920, 330)))
    print("p1 rings BR", ring_center(bgs[0], (1250, 700, 1920, 1080)))
    print("p1 rings L ", ring_center(bgs[0], (0, 100, 260, 1080)))
    print("p2 rings TR", ring_center(bgs[1], (1350, 0, 1920, 480)))
    print("p2 rings L ", ring_center(bgs[1], (0, 0, 330, 1080)))
    print("p3 rings TL", ring_center(bgs[2], (0, 0, 420, 400)))
    print("p3 rings BR", ring_center(bgs[2], (1450, 760, 1920, 1080)))
    print("p1 arc", arc_circle(bgs[0], (10, 10, 140), 45, (900, 0, 1400, 1080)))
    print("p2 arc", arc_circle(bgs[1], (128, 20, 90), 45, (700, 0, 1300, 1080)))
