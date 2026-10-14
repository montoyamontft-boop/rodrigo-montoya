"""Día del Pediatra: extract every element of the three PDF pages as exact 4K layers.

Each group of paint operators is rendered twice from the PDF itself, over a
black and over a white backdrop. Every blend mode used in this file (Normal
with opacity, Multiply, Screen) is linear in the backdrop, so

    result = backdrop * F + A

holds per pixel and per channel. F and A are stored as 8-bit images: the layer
then composites exactly over *any* backdrop, also a moving one (parallax,
reveals), with no colour solved against a frozen background.

The background photo of each page is stored as its own opaque 4K plate.
A recomposition check against MuPDF's render of the full page is printed.

usage: python build.py SOURCE.pdf OUT_DIR
"""
import json, os, sys
import numpy as np
import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "pipeline"))
import pdfops  # noqa: E402
from layout import PAGES, GLYPH_OPS  # noqa: E402

ZOOM = 2.0  # 1920 pt -> 3840 px


def parse(spec):
    out = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            out += range(int(a), int(b) + 1)
        else:
            out.append(int(part))
    return out


def render(doc, pno, xref, stream, backdrop=None):
    if backdrop is not None:
        stream = b"q %d %d %d rg 0 0 1920 1080 re f Q\n" % ((backdrop,) * 3) + stream
    doc.update_stream(xref, stream)
    pm = doc[pno].get_pixmap(matrix=pymupdf.Matrix(ZOOM, ZOOM), alpha=False)
    return np.frombuffer(pm.samples, np.uint8).reshape(pm.h, pm.w, 3).astype(np.float32)


def main(src, out):
    os.makedirs(out, exist_ok=True)
    doc = pymupdf.open(src)
    manifest = {}
    glyphs = {}
    for name, spec in PAGES.items():
        pno = spec["page"] - 1
        page = doc[pno]
        # some pages split their drawing over several content streams:
        # merge them into the first so every operator can be switched off
        xrefs = page.get_contents()
        orig = page.read_contents()
        xref = xrefs[0]
        for x in xrefs[1:]:
            doc.update_stream(x, b"")
        po = pdfops.PageOps(orig)
        n = len(po)
        owner = [None] * n
        for g, ops in spec["groups"].items():
            for i in parse(ops):
                assert owner[i] is None, (name, i)
                owner[i] = g
        miss = [i for i in range(n) if owner[i] is None]
        assert not miss, (name, miss)
        # consecutive runs keep the original paint order
        runs = []
        for i in range(n):
            if runs and runs[-1][0] == owner[i]:
                runs[-1][1].append(i)
            else:
                runs.append((owner[i], [i]))
        ref = render(doc, pno, xref, orig)
        comp = None
        layers = []
        for li, (g, ops) in enumerate(runs):
            sub = po.render_subset(set(ops))
            if g == "bg":
                plate = render(doc, pno, xref, sub)
                fn = f"{name}_bg.png"
                Image.fromarray(plate.astype(np.uint8)).save(os.path.join(out, fn), compress_level=1)
                comp = plate.copy()
                layers.append(dict(group=g, file=fn))
                continue
            a = render(doc, pno, xref, sub, backdrop=0)
            w = render(doc, pno, xref, sub, backdrop=1)
            F = (w - a) / 255.0
            m = (np.abs(F - 1).max(-1) > 0.5 / 255) | (a.max(-1) > 0.5)
            ys, xs = np.nonzero(m)
            if len(xs) == 0:
                continue
            x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
            Fq = np.clip(F * 255 + 0.5, 0, 255).astype(np.uint8)
            Aq = np.clip(a + 0.5, 0, 255).astype(np.uint8)
            comp = comp * (Fq / 255.0) + Aq
            fn = f"{name}_{li:03d}_{g}"
            Image.fromarray(Fq[y0:y1, x0:x1]).save(os.path.join(out, fn + "_F.png"), compress_level=1)
            Image.fromarray(Aq[y0:y1, x0:x1]).save(os.path.join(out, fn + "_A.png"), compress_level=1)
            layers.append(dict(group=g, file=fn, x=int(x0), y=int(y0), w=int(x1 - x0), h=int(y1 - y0)))
        for (scn, g), spec_ops in GLYPH_OPS.items():
            if scn != name:
                continue
            boxes = []
            for i in parse(spec_ops):
                a = render(doc, pno, xref, po.render_subset({i}), backdrop=0)
                ys, xs = np.nonzero(a.max(-1) > 8)
                boxes.append([int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)])
            glyphs[f"{name}/{g}"] = boxes
        doc.update_stream(xref, orig)
        diff = np.abs(comp - ref)
        print(f"{name}: {len(layers)} layers, recomposition diff max {diff.max():.1f} "
              f"mean {diff.mean():.4f}, >3: {(diff.max(-1) > 3).mean() * 100:.4f}% px", flush=True)
        Image.fromarray(ref.astype(np.uint8)).save(os.path.join(out, f"{name}_ref.png"), compress_level=1)
        manifest[name] = layers
    json.dump(manifest, open(os.path.join(out, "manifest.json"), "w"), indent=1)
    json.dump(glyphs, open(os.path.join(out, "glyphs.json"), "w"))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
