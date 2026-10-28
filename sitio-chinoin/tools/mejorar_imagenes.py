"""Aumenta la resolución de fotos con superresolución (EDSR) y un afinado ligero.

Uso: python3 tools/mejorar_imagenes.py <modelos_dir> <escala 2|4> <entrada> <salida.webp> [lado_max]
Requiere opencv-contrib-python-headless y los modelos EDSR_x2.pb / EDSR_x4.pb
(https://github.com/Saafke/EDSR_Tensorflow).
"""
import sys

import cv2
import numpy as np
from PIL import Image, ImageFilter


def upscale(models, scale, src, tile=360, pad=12):
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(f'{models}/EDSR_x{scale}.pb')
    sr.setModel('edsr', scale)
    im = Image.open(src)
    has_alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
    alpha = im.convert('RGBA').getchannel('A') if has_alpha else None
    rgb = np.asarray(im.convert('RGB'))[:, :, ::-1]
    h, w = rgb.shape[:2]
    out = np.zeros((h * scale, w * scale, 3), np.uint8)
    # por mosaicos para no agotar memoria; con margen para evitar costuras
    for y in range(0, h, tile):
        for x in range(0, w, tile):
            y0, x0 = max(0, y - pad), max(0, x - pad)
            y1, x1 = min(h, y + tile + pad), min(w, x + tile + pad)
            up = sr.upsample(rgb[y0:y1, x0:x1])
            oy, ox = (y - y0) * scale, (x - x0) * scale
            th, tw = min(tile, h - y) * scale, min(tile, w - x) * scale
            out[y * scale:y * scale + th, x * scale:x * scale + tw] = up[oy:oy + th, ox:ox + tw]
    res = Image.fromarray(out[:, :, ::-1])
    res = res.filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=2))
    if alpha is not None:
        res.putalpha(alpha.resize(res.size, Image.LANCZOS))
    return res


if __name__ == '__main__':
    models, scale, src, dst = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    max_side = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    img = upscale(models, scale, src)
    if max_side and max(img.size) > max_side:
        img.thumbnail((max_side, max_side), Image.LANCZOS)
    img.save(dst, 'WEBP', quality=90, method=6)
    print(dst, img.size)
