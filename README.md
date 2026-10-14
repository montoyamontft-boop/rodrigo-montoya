> Este repositorio contiene tres piezas: la presentación de Neuropatía/Nevrika (abajo) y los videos
> **Día del Médico** ([`dia_del_medico/README.md`](dia_del_medico/README.md)) y **Día del Pediatra**
> ([`dia_del_pediatra/README.md`](dia_del_pediatra/README.md)), ambos de CHINOIN.

# Neuropatía diabética dolorosa – Nevrika® · video animado

Conversión de la presentación `VIDEO NEUROPATÍA - I.pdf` (12 diapositivas, Adobe Illustrator, 1920 × 1080 pt)
en una pieza de motion graphics de 12 escenas, en el orden original.

| | |
|---|---|
| Salida | `salida/neuropatia_4k.mp4` (se genera con el script; el PDF fuente y el video no se versionan porque este repositorio es público) |
| Resolución | 3840 × 2160 (16:9) |
| Frecuencia | 30 fps constantes |
| Duración | 134,7 s (4041 cuadros) |
| Códec | H.264 High, yuv420p, conversión y etiquetado BT.709 (rango TV), CRF 16, sin audio |

## Cómo se hizo (fidelidad)

* **Nada se redibuja.** Cada escena se obtiene del propio PDF: el flujo de contenido de cada página se
  divide por operador de pintura (trazo, texto, imagen, degradado) y cada grupo se rasteriza por separado
  a 4K con MuPDF, conservando el estado gráfico original (recortes, matrices, transparencias).
  Las tipografías son las incrustadas en el PDF (Bebas Neue, Myriad Pro / Myriad Variable Concept):
  no hay sustitución de fuentes ni texto reconstruido.
* **Modos de fusión.** Varios objetos usan multiplicar/transparencias. El color de cada capa se resuelve
  contra su fondo real del PDF, de modo que al apilar las capas se recompone la página exacta.
* **Verificación automática.** En el momento de lectura de cada escena, el cuadro del video se compara con
  el render directo del PDF a 4K: diferencia máxima ≤ 3/255 por canal en las 12 escenas (redondeo),
  0 píxeles con diferencia > 3.
* Fondos que dependen de modos de fusión (texturas, mapas, swooshes, fotografía de la escena 9) se animan
  como una sola placa para no desalinear lo que está fusionado.

## Lenguaje de movimiento

* Señalética: los letreros colgantes descienden desde arriba; pórticos y postes entran lateralmente.
* Barras y degradados se revelan con barridos de máscara de izquierda a derecha; las gráficas de dosis
  crecen de menor a mayor dosis (150 → 300 → 600 mg) y luego aparecen sus porcentajes.
* Texto: entrada por líneas con máscara (sin escritura letra por letra), escalonada según la jerarquía.
* Pines de ubicación: aparición con escala corta y suave.
* Fondos: asentamiento lento de escala (parallax respecto del contenido) que llega exactamente a 1:1 al
  final de la lectura.
* Transiciones: el contenido sale escalonado, la escena avanza ligeramente (push) y se funde con el fondo de
  la siguiente, que continúa el movimiento. Apertura desde negro, cierre a negro.

Coreografía y tiempos por escena: `pipeline/scenes.py`.

## Regenerar el video

Requisitos: Python 3.10+, `pip install -r pipeline/requirements.txt`, `ffmpeg` con libx264.

```bash
./make_video.sh RUTA/AL/VIDEO_NEUROPATIA_I.pdf            # 4K  -> salida/neuropatia_4k.mp4
SCALE=0.5 ./make_video.sh RUTA/AL/VIDEO_NEUROPATIA_I.pdf  # 1080p
```

Pasos internos:

1. `pipeline/build_layers.py PDF build/layers` – capas RGBA 4K + verificación de recomposición (~11 min).
2. `pipeline/render.py build/layers salida.mp4 --scale 1.0 --workers 3 --crf 16` – animación y codificación.
   `--stills DIR --times 1.0,2.5` exporta cuadros sueltos para revisión.

Herramientas de diagnóstico: `pipeline/analyze.py` (cajas e índices de cada operador por página),
`pipeline/diag.py` (detecta objetos con modos de fusión).

## Limitaciones reales

* Las imágenes incrustadas (fondos, ilustraciones, fotografías) tienen entre ~98 y 220 ppi respecto del
  tamaño de página; a 4K muestran el detalle que contienen, sin interpolación "inventada". Textos y
  vectores son nítidos a 4K.
* La escena 1 (carretera, auto, señales con hormigas) y la fotografía de la escena 9 son imágenes únicas:
  se animan como plano completo, sin capas internas inventadas.
* No se aplica motion blur: los desplazamientos son cortos y con easing, y la lectura queda siempre nítida.
