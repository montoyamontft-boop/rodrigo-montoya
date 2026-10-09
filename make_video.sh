#!/usr/bin/env bash
# Produce the animated video from the original PDF.
#   ./make_video.sh RUTA/AL/VIDEO_NEUROPATIA_I.pdf            -> salida/neuropatia_4k.mp4 (3840x2160)
#   SCALE=0.5 ./make_video.sh RUTA/AL/VIDEO_NEUROPATIA_I.pdf  -> 1920x1080
# Requires: python3 (pymupdf, numpy, pillow) and ffmpeg with libx264.
set -euo pipefail
PDF="${1:?uso: ./make_video.sh RUTA/AL/VIDEO_NEUROPATIA_I.pdf}"
SCALE="${SCALE:-1.0}"
WORKERS="${WORKERS:-3}"
CRF="${CRF:-16}"
HERE="$(cd "$(dirname "$0")" && pwd)"
BUILD="${BUILD:-$HERE/build/layers}"
mkdir -p "$BUILD" "$HERE/salida"
if [ ! -f "$BUILD/manifest.json" ]; then
  python3 "$HERE/pipeline/build_layers.py" "$PDF" "$BUILD"
fi
OUT="${OUT:-$HERE/salida/neuropatia_$( [ "$SCALE" = "1.0" ] && echo 4k || echo "${SCALE}x").mp4}"
python3 "$HERE/pipeline/render.py" "$BUILD" "$OUT" --scale "$SCALE" --workers "$WORKERS" --crf "$CRF"
