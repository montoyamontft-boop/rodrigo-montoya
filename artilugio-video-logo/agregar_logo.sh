#!/usr/bin/env bash
# Pone el logo de Artilugio arriba a la izquierda de un video, sin perder calidad.
# Uso: ./agregar_logo.sh video.mp4 [alto_de_salida]
#   alto_de_salida: vacío = resolución original; 1080 = reescala a 1080p.
# El logo mide 16 % del alto del video y queda a 3.8 % del borde.
set -euo pipefail
in="$1"; out_h="${2:-}"
dir="$(cd "$(dirname "$0")" && pwd)"
h=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$in")
base=""
if [ -n "$out_h" ]; then base="scale=-2:${out_h}:flags=lanczos,"; h="$out_h"; fi
logo_h=$(( h * 16 / 100 )); margin=$(( h * 38 / 1000 ))
out="${in%.*}-artilugio${out_h:+-${out_h}p}.mp4"
ffmpeg -y -i "$in" -i "$dir/logo-artilugio-1190.png" -filter_complex \
  "[0:v]${base}format=yuv444p[b];[1:v]scale=-1:${logo_h}:flags=lanczos,format=rgba,scale=out_color_matrix=bt709:out_range=tv,format=yuva444p[l];[b][l]overlay=${margin}:${margin}:format=yuv444,format=yuv420p[v]" \
  -map "[v]" -map 0:a? -c:v libx264 -preset slow -crf 12 -profile:v high -tune film \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a copy -movflags +faststart "$out"
echo "$out"
