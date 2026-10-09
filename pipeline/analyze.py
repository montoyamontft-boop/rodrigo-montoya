"""Measure the on-page bbox of every paint operator (debug aid + input to layering)."""
import json, sys, os
import numpy as np
import pymupdf
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdfops

Z = 0.25


def op_boxes(doc, pno):
    page = doc[pno]
    xref = page.get_contents()[0]
    orig = page.read_contents()
    po = pdfops.PageOps(orig)
    boxes = []
    for i in range(len(po)):
        doc.update_stream(xref, po.render_subset({i}))
        pm = doc[pno].get_pixmap(matrix=pymupdf.Matrix(Z, Z), alpha=True)
        a = np.frombuffer(pm.samples, np.uint8).reshape(pm.h, pm.w, pm.n)[..., 3]
        ys, xs = np.nonzero(a > 4)
        boxes.append(None if len(xs) == 0 else
                     [int(xs.min() / Z), int(ys.min() / Z), int((xs.max() + 1) / Z), int((ys.max() + 1) / Z)])
    doc.update_stream(xref, orig)
    return po, boxes


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    doc = pymupdf.open(src)
    allb = {}
    for pno in range(len(doc)):
        po, boxes = op_boxes(doc, pno)
        allb[pno + 1] = [[i, po.ops[po.paint[i]][0].decode(), b] for i, b in enumerate(boxes)]
        pm = doc[pno].get_pixmap(matrix=pymupdf.Matrix(0.75, 0.75))
        im = Image.frombytes("RGB", (pm.w, pm.h), pm.samples)
        im = Image.blend(im, Image.new("RGB", im.size, "white"), 0.45)
        d = ImageDraw.Draw(im)
        cols = [(255, 0, 0), (0, 140, 0), (0, 0, 255), (200, 0, 200), (0, 130, 130), (160, 90, 0)]
        for i, b in enumerate(boxes):
            if b is None or (b[2] - b[0] > 1800 and b[3] - b[1] > 1000):
                continue
            r = [v * 0.75 for v in b]
            c = cols[i % len(cols)]
            d.rectangle(r, outline=c, width=1)
            d.text((r[0] + 2, r[1] + 1), str(i), fill=c)
        im.save(f"{out}/ops{pno+1:02d}.png")
    json.dump(allb, open(f"{out}/opboxes.json", "w"))
