# Logo de Artilugio sobre video

Pone el logotipo de Artilugio en pequeño, abajo a la derecha, sin perder calidad del video.

```bash
./agregar_logo.sh video.mp4         # misma resolución del original
./agregar_logo.sh video.mp4 1080    # reescalado a 1080p (el logo se dibuja nítido a ese tamaño)
```

- `logo-artilugio-1190.png`: el logo vectorial del PDF de backs renderizado a 1190 px con fondo transparente, sin modificarlo.
- El video se recodifica en H.264 High con CRF 12 (prácticamente sin pérdida) y espacio de color BT.709; el audio se copia tal cual.
- Requiere `ffmpeg`.
