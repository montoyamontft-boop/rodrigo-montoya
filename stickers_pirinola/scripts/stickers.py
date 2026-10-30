"""Stickers estáticos (borde blanco troquelado) + versiones HD con fondo."""
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

fg = Image.open('fg1.png')                      # 2048 RGBA
bg = Image.open('fg1_bg.png').convert('RGBA')   # degradado original
BLUE = (60, 108, 170, 255)
font = ImageFont.truetype('BebasNeue.ttf', 400)

def crop_alpha(im, thr=8):
    a = np.asarray(im)[..., 3]; ys, xs = np.nonzero(a > thr)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

def text_img(txt, width):
    tmp = Image.new('RGBA', (4000, 700), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((50, 50), txt, font=font, fill=BLUE)
    t = crop_alpha(tmp)
    return t.resize((width, round(t.height * width / t.width)), Image.LANCZOS)

def die_cut(im, border, pad):
    W, H = im.size; c = Image.new('RGBA', (W + 2 * pad, H + 2 * pad), (0, 0, 0, 0)); c.alpha_composite(im, (pad, pad))
    a = (np.asarray(c)[..., 3] > 40).astype(np.uint8)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * border + 1, 2 * border + 1))
    sil = cv2.dilate(cv2.morphologyEx(a, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (border * 3, border * 3))), k)
    ff = sil.copy(); cv2.floodFill(ff, np.zeros((sil.shape[0] + 2, sil.shape[1] + 2), np.uint8), (0, 0), 1); sil = sil | (1 - ff)
    sil = cv2.GaussianBlur(sil.astype(np.float32), (0, 0), 1.2)
    out = Image.new('RGBA', c.size, (0, 0, 0, 0))
    sh = Image.fromarray((sil * 70).astype(np.uint8)).filter(ImageFilter.GaussianBlur(border * 0.5))
    out.paste((0, 30, 40, 255), (0, int(border * 0.35)), sh)          # sombra suave
    out.alpha_composite(Image.merge('RGBA', [Image.new('L', c.size, 255)] * 3 + [Image.fromarray((sil * 255).astype(np.uint8))]))
    out.alpha_composite(c)
    return crop_alpha(out, 2)

def square(im, S, margin=0.04):
    s = S * (1 - 2 * margin) / max(im.size); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    c = Image.new('RGBA', (S, S), (0, 0, 0, 0)); c.alpha_composite(im, ((S - im.width) // 2, (S - im.height) // 2)); return c

top = crop_alpha(fg, 20)
# --- sticker 1: pirinola ---
s1 = square(die_cut(top, 34, 60), 2048)
# --- sticker 2: texto + pirinola ---
txt = text_img('TEN UN GRAN DÍA', round(top.width * 0.98))
comb = Image.new('RGBA', (max(top.width, txt.width), txt.height + 70 + top.height), (0, 0, 0, 0))
comb.alpha_composite(txt, ((comb.width - txt.width) // 2, 0)); comb.alpha_composite(top, ((comb.width - top.width) // 2, txt.height + 70))
s2 = square(die_cut(comb, 34, 60), 2048)
for name, im in [('sticker_pirinola', s1), ('sticker_ten_un_gran_dia', s2)]:
    im.save(f'out/{name}_HD.png')
    im.resize((512, 512), Image.LANCZOS).save(f'out/{name}_whatsapp.webp', quality=92, method=6)

# --- versiones HD con fondo ---
up1 = Image.open('up1.png').convert('RGB').resize((2048, 2048), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
up1.save('out/pirinola_HD.png')
hd2 = bg.copy()
txt2 = text_img('TEN UN GRAN DÍA', 1800)
hd2.alpha_composite(txt2, ((2048 - txt2.width) // 2, 150))
y0 = 150 + txt2.height + 90
sc = min((2048 - y0 - 70) / top.height, 1900 / top.width); t2 = top.resize((round(top.width * sc), round(top.height * sc)), Image.LANCZOS)
hd2.alpha_composite(t2, ((2048 - t2.width) // 2, y0))
hd2.convert('RGB').save('out/ten_un_gran_dia_HD.png')
