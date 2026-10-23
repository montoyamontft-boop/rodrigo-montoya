"""Prepara las fotos de producto para el sitio.

Uso:
    python3 tools/optimizar_productos.py <carpeta_con_originales>

Cada original debe llamarse como el id del producto (por ejemplo `bilumiv.png`,
`rifosar-pos.tif`). Se generan en assets/productos/:
    <id>.webp       2000 px, para pantallas retina y el zoom de la ficha
    <id>-1000.webp  1000 px, para la cuadrícula
Se conserva la transparencia si el original la tiene.
"""
import sys
from pathlib import Path

from PIL import Image

IDS = {
    "rifosar", "rifosar-pos", "bilumiv", "lezomiv", "fexilev",
    "carenev", "cravicem", "matinev", "tamablan-pf",
}
OUT = Path(__file__).resolve().parent.parent / "assets" / "productos"


def export(img, size, dest):
    copy = img.copy()
    copy.thumbnail((size, size), Image.LANCZOS)
    copy.save(dest, "WEBP", quality=92, method=6)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    OUT.mkdir(parents=True, exist_ok=True)
    done = set()
    for path in sorted(src.iterdir()):
        pid = path.stem.lower()
        if pid not in IDS:
            continue
        img = Image.open(path)
        img = img.convert("RGBA" if "A" in img.getbands() or img.mode == "P" else "RGB")
        if min(img.size) < 1600:
            print(f"aviso: {path.name} mide {img.size[0]}x{img.size[1]}; se recomienda 2000 px o más")
        export(img, 2000, OUT / f"{pid}.webp")
        export(img, 1000, OUT / f"{pid}-1000.webp")
        done.add(pid)
        print(f"listo: {pid}")
    for pid in sorted(IDS - done):
        print(f"falta: {pid}")


if __name__ == "__main__":
    main()
