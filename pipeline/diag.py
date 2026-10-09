"""Find operators whose isolated rendering does not composite back exactly
(blend modes, knockout groups, backdrop-dependent soft masks)."""
import sys, os
import numpy as np, pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdfops

Z = 0.5


def rr(doc, pno, xref, s):
    doc.update_stream(xref, s)
    pm = doc[pno].get_pixmap(matrix=pymupdf.Matrix(Z, Z), alpha=True)
    a = np.frombuffer(pm.samples, np.uint8).reshape(pm.h, pm.w, 4).astype(np.float32)
    return a[..., :3] * a[..., 3:4] / 255, a[..., 3] / 255


def main(src, pages):
    doc = pymupdf.open(src)
    for pg in pages:
        pno = pg - 1
        xref = doc[pno].get_contents()[0]
        orig = doc[pno].read_contents()
        po = pdfops.PageOps(orig)
        comp = None
        bad = []
        for k in range(len(po)):
            c, a = rr(doc, pno, xref, po.render_subset({k}))
            if comp is None:
                comp, ca = c.copy(), a.copy()
            else:
                comp = c + comp * (1 - a[..., None])
                ca = a + ca * (1 - a)
            ref, _ = rr(doc, pno, xref, po.render_subset(set(range(k + 1))))
            d = np.abs(comp - ref)
            m = d.mean()
            if m > 0.3:
                bad.append((k, po.ops[po.paint[k]][0].decode(), round(float(m), 2), round(float(d.max()), 1)))
                comp = ref.copy()  # resync
                ca = rr(doc, pno, xref, po.render_subset(set(range(k + 1))))[1]
        doc.update_stream(xref, orig)
        print(pg, bad)


main(sys.argv[1], [int(x) for x in sys.argv[2].split(",")])
