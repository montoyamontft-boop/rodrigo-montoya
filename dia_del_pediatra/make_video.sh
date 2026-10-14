#!/usr/bin/env bash
# Día del Pediatra: PDF de 3 páginas -> video de motion graphics.
#   ./dia_del_pediatra/make_video.sh RUTA/AL/DIA_DEL_PEDIATRA_-B.pdf            -> salida/dia_del_pediatra_4k.mp4
#   SCALE=0.5 ./dia_del_pediatra/make_video.sh RUTA/AL/DIA_DEL_PEDIATRA_-B.pdf  -> 1920x1080 (vista previa)
# Requiere: python3 (pymupdf, numpy, pillow, opencv-python-headless, scikit-image) y ffmpeg con libx264.
set -euo pipefail
PDF="${1:?uso: ./dia_del_pediatra/make_video.sh RUTA/AL/DIA_DEL_PEDIATRA_-B.pdf}"
SCALE="${SCALE:-1.0}"
WORKERS="${WORKERS:-3}"
CRF="${CRF:-14}"
PRESET="${PRESET:-slow}"
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
BUILD="${BUILD:-$ROOT/build/pediatra}"
mkdir -p "$BUILD" "$ROOT/salida"
if [ ! -f "$BUILD/manifest.json" ]; then
  python3 "$HERE/build.py" "$PDF" "$BUILD"
fi
OUT="${OUT:-$ROOT/salida/dia_del_pediatra_$( [ "$SCALE" = "1.0" ] && echo 4k || echo "${SCALE}x").mp4}"
python3 "$HERE/motion.py" "$BUILD" "$OUT" --scale "$SCALE" --workers "$WORKERS" --crf "$CRF" --preset "$PRESET"
