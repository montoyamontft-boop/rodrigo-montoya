"""Render every scene into exact 4K RGBA layers straight from the PDF.

For each scene, consecutive paint operators that share a group form one layer,
so stacking the layers reproduces the original paint order. The composite of
all layers is checked against a direct render of the page.

usage: python build_layers.py SOURCE.pdf OUT_DIR
"""
import json, os, sys
import numpy as np
import pymupdf
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdfops
from scenes import SCENES, parse_ops

ZOOM = 2.0  # 1920 pt -> 3840 px


def render_rgba(doc, pno, xref, stream):
    doc.update_stream(xref, stream)
    pm = doc[pno].get_pixmap(matrix=pymupdf.Matrix(ZOOM, ZOOM), alpha=True)
    return np.frombuffer(pm.samples, np.uint8).reshape(pm.h, pm.w, 4).copy()


def render_white(doc, pno, xref, stream):
    """Opaque render on white paper - exactly what a PDF viewer shows."""
    doc.update_stream(xref, stream)
    pm = doc[pno].get_pixmap(matrix=pymupdf.Matrix(ZOOM, ZOOM), alpha=False)
    return np.frombuffer(pm.samples, np.uint8).reshape(pm.h, pm.w, 3).astype(np.float32)


def premul(x):
    return x[..., :3].astype(np.float32) * (x[..., 3:4].astype(np.float32) / 255)


def on_white(x):
    return premul(x) + 255.0 * (1 - x[..., 3:4].astype(np.float32) / 255)


def over(dst, src):
    a = src[..., 3:4].astype(np.float32) / 255
    dst[...] = src[..., :3].astype(np.float32) * a + dst * (1 - a)


def main(src, out, only=None):
    os.makedirs(out, exist_ok=True)
    doc = pymupdf.open(src)
    manifest = []
    old = {}
    if only and os.path.exists(os.path.join(out, "manifest.json")):
        old = {m["scene"]: m for m in json.load(open(os.path.join(out, "manifest.json")))}
    for si, sc in enumerate(SCENES):
        if only and si + 1 not in only:
            manifest.append(old[si + 1])
            continue
        for f in os.listdir(out):
            if f.startswith(f"s{si+1:02d}_"):
                os.remove(os.path.join(out, f))
        pno = sc["page"] - 1
        page = doc[pno]
        xref = page.get_contents()[0]
        orig = page.read_contents()
        po = pdfops.PageOps(orig)
        n = len(po)
        owner = [None] * n
        for g in sc["groups"]:
            for i in parse_ops(g["ops"]):
                if i >= n:
                    raise SystemExit(f"page {sc['page']}: op {i} out of range ({n})")
                if owner[i] is not None:
                    raise SystemExit(f"page {sc['page']}: op {i} in {owner[i]} and {g['name']}")
                owner[i] = g["name"]
        missing = [i for i in range(n) if owner[i] is None]
        if missing:
            print(f"  page {sc['page']}: unassigned ops -> bg: {missing}")
            for i in missing:
                owner[i] = "bg"
        runs = []
        for i in range(n):
            if runs and runs[-1][0] == owner[i]:
                runs[-1][1].append(i)
            else:
                runs.append((owner[i], [i]))
        ref = render_rgba(doc, pno, xref, orig)
        H, W = ref.shape[:2]
        comp = np.full((H, W, 3), 255.0, np.float32)
        layers = []
        bboxes = {}
        # prefix renders are taken on white paper, the way the page is shown
        prev = np.full((H, W, 3), 255.0, np.float32)
        done = []
        for li, (gname, ops) in enumerate(runs):
            iso = render_rgba(doc, pno, xref, po.render_subset(set(ops)))
            done += ops
            after = render_white(doc, pno, xref, po.render_subset(set(done)))
            ys, xs = np.nonzero(iso[..., 3])
            if len(xs) == 0:
                prev = after
                continue
            x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
            # Equivalent normal-blend layer: same coverage as the isolated
            # render, colour solved against the real backdrop so blend modes,
            # soft masks and anti-aliasing seams composite back exactly.
            a = iso[..., 3:4].astype(np.float32) / 255
            with np.errstate(divide="ignore", invalid="ignore"):
                col = np.where(a > 0, (after - prev * (1 - a)) / np.maximum(a, 1e-6), 0)
            rgba = np.concatenate([np.clip(col + 0.5, 0, 255), iso[..., 3:4]], -1).astype(np.uint8)
            prev = after
            over(comp, rgba)
            crop = rgba[y0:y1, x0:x1]
            fn = f"s{si+1:02d}_{li:03d}_{gname}.png"
            Image.fromarray(crop, "RGBA").save(os.path.join(out, fn), compress_level=1)
            layers.append(dict(file=fn, group=gname, x=int(x0), y=int(y0), w=int(x1 - x0), h=int(y1 - y0)))
            b = bboxes.get(gname)
            nb = [int(x0), int(y0), int(x1), int(y1)]
            bboxes[gname] = nb if b is None else [min(b[0], nb[0]), min(b[1], nb[1]), max(b[2], nb[2]), max(b[3], nb[3])]
        doc.update_stream(xref, orig)
        refc = render_white(doc, pno, xref, orig)
        diff = np.abs(comp - refc)
        print(f"scene {si+1:2d} page {sc['page']:2d}: {len(layers)} layers, "
              f"composite diff max {diff.max():.1f} mean {diff.mean():.4f} "
              f">8: {(diff.max(-1) > 8).mean()*100:.3f}% px")
        Image.fromarray(np.clip(refc + 0.5, 0, 255).astype(np.uint8)).save(os.path.join(out, f"ref{si+1:02d}.png"), compress_level=1)
        manifest.append(dict(scene=si + 1, page=sc["page"], size=[W, H], layers=layers, bboxes=bboxes))
    json.dump(manifest, open(os.path.join(out, "manifest.json"), "w"), indent=1)


if __name__ == "__main__":
    only = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else None
    main(sys.argv[1], sys.argv[2], only)
