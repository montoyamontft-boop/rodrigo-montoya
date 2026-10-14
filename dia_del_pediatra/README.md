# Día del Pediatra (CHINOIN): video de motion graphics

Conversión de `DIA DEL PEDIATRA -B.pdf` (3 páginas, Adobe Illustrator, 1920 × 1080 pt) en una pieza animada
de tres escenas. Concepto: **pequeños gestos, grandes cuidados**. Los arcos de las fotografías, los
círculos concéntricos, las tarjetas y los contornos forman un mismo lenguaje que conduce cada revelado
y cada transición.

| | |
|---|---|
| Salida | `salida/dia_del_pediatra_4k.mp4` (generado; el PDF y el video no se versionan porque el repositorio es público) |
| Resolución | 3840 × 2160 (16:9) |
| Frecuencia | 30 fps constantes, 780 cuadros |
| Duración | 26,0 s; la composición final queda completa durante 5,8 s |
| Códec | H.264 High, yuv420p, BT.709 (rango TV), CRF 14, sin audio |

## Fidelidad

* **Nada se regenera.** Textos (Baloo Chettan y Montserrat), tarjeta, plecas, globo, contornos, logotipos,
  leyenda y CHINOIN se extraen del PDF como capas vectoriales a 4K. Cada capa se renderiza sobre fondo negro
  y blanco (`resultado = fondo × F + A`), así que se recompone exacta aunque el fondo se mueva.
  Recomposición contra el PDF: diferencia máxima ≤ 2,1/255 en las tres páginas.
* **Composición final verificada.** En las pausas de lectura y en el último cuadro, la imagen coincide con
  el render directo del PDF a 4K (diferencia máxima 2/255). La única excepción es la esquina de CHINOIN,
  por lo que se explica abajo.
* **Recursos aplanados.** Los arcos de color, los círculos blancos y las diagonales translúcidas forman
  parte de las fotografías de fondo. No se recortan ni se dibujan de nuevo:
  * Las fotos se mueven rígidas, con un acercamiento de cámara sutil que termina en el encuadre original.
    Rostros, manos y cuerpos no se deforman.
  * El arco de cada foto se desplaza radialmente desde el centro de su propia circunferencia: se usan los
    píxeles del propio trazo, sin estirar su grosor.
  * Los círculos se expanden con una escala radial alrededor de su centro (medido en la imagen con
    `fit.py`) y respiran con una onda suave de presencia que los atenúa y los devuelve.
  * Las diagonales se desplazan en su propia dirección, con el plano pastel.
  * Ninguna deformación toca las fotografías.
* **Contornos dibujados.** La tarjeta azul, el contorno negro de la pleca y el contorno morado del globo se trazan
  siguiendo su propia forma: el esqueleto de cada contorno se recorre desde un punto de inicio.
* **«Grandes desafíos.»** entra letra por letra. Cada letra es la porción exacta de la capa original (relleno
  turquesa y contorno blanco), separada con las cajas de sus propios contornos.
* **Globo sin costuras.** El globo se compone de un cuerpo y dos tiras que se tocan. Mientras aparece, se
  dibujan como una sola forma, de modo que no se ve la costura que en el PDF tapa el contorno morado. En
  cuanto el contorno termina de dibujarse, vuelven a usarse las piezas originales del PDF.
* **CHINOIN** se compone al final de cada cuadro, fijo y nítido durante todo el video. Su posición en el
  PDF varía hasta 3 pt entre páginas (1680 / 1679 / 1677 pt). Se mantiene la de la página 1, de modo que en
  las páginas 2 y 3 esa esquina difiere apenas 1,5 pt del original.

## Coreografía

Tiempos en segundos del video. Detalle completo en `motion.py` (`CHOREO`, `DEPTH`, `RIPPLES`, `REVEAL`).

**Escena 1. Pequeños pacientes. Grandes desafíos. (0–9,3)**
* 0–2,2: sobre el pastel de la propia página, la fotografía de la doctora con el bebé se abre en un círculo
  concéntrico a su arco. El arco cian y azul viaja con el borde de la máscara, se posa exactamente en su
  sitio (≈1,1 s) y el frente continúa desplegando el fondo. Los círculos blancos se expanden lentamente.
* 1,9: el contorno azul de la tarjeta se traza desde la esquina superior izquierda en dos direcciones, y la
  línea superior avanza hasta sus guiones. 2,55: la superficie turquesa llega con un desplazamiento corto
  desde el contorno. «Pequeños pacientes.» viaja con ella y se revela con un barrido.
* 3,85: «Grandes desafíos.» entra con más presencia: letra por letra, desde su línea base, con una llegada
  suave (≈3 % de sobrepaso, sin rebote).
* Lectura completa hasta 7,5. Las salidas se escalonan con un desplazamiento suave.

**Escena 2. Celebrar a quienes cuidan (7,9–15,4)**
* La curva conduce la transición: el arco magenta sale desde el centro de su circunferencia, revela al pediatra
  con el bebé, se posa en su sitio y el frente sigue hasta mostrar el fondo rosa. Los círculos del fondo
  siguen en movimiento suave.
* 9,55: «20 de octubre» entra con una máscara ascendente limpia. 10,15: la pleca magenta se despliega
  con una máscara horizontal de borde inclinado, como sus extremos, y «Día del Pediatra» aparece con el
  mismo borde. 10,55: el contorno negro se dibuja por separado alrededor de la pleca mientras se asienta
  en su posición original.

**Escena 3. Un reconocimiento con calidez (14,0–26,0)**
* Los círculos de la escena 2 se abren en ondas concéntricas que dan paso al fondo turquesa y rosa. La
  fotografía del osito y el estetoscopio llega con un acercamiento muy sutil que termina en el encuadre
  original.
* 15,25: el globo turquesa se expande desde la punta de su cola, con llegada suave. 15,55: el contorno
  morado se dibuja con un desfase respecto al globo.
* 16,35–17,55: el mensaje se revela línea por línea («Nuestro reconocimiento» / «a quienes hacen» /
  «de la salud infantil» / «su vocación.»).
* 18,6: los cuatro logotipos aparecen escalonados, sin perder detalles ni registros. 19,5: la leyenda.
  Composición final completa desde 20,2 hasta 26,0, con los círculos todavía vivos.

## Regenerar el video

Requisitos: Python 3.10+, `pip install -r pipeline/requirements.txt`, y `ffmpeg` con libx264.

```bash
./dia_del_pediatra/make_video.sh RUTA/AL/DIA_DEL_PEDIATRA_-B.pdf            # 4K    -> salida/dia_del_pediatra_4k.mp4
SCALE=0.5 ./dia_del_pediatra/make_video.sh RUTA/AL/DIA_DEL_PEDIATRA_-B.pdf  # 1080p -> vista previa (~1 min)
```

Pasos internos:

1. `build.py PDF build/pediatra`: capas 4K (F/A), placas de fondo y cajas de cada letra, con verificación
   de recomposición. La página 1 reparte su dibujo en 8 flujos de contenido, que se unen antes de separar
   las capas.
2. `motion.py build/pediatra salida.mp4 --scale 1.0 --workers 3 --crf 14 --preset slow`: render en paralelo
   con un único codificador (sin costuras entre bloques y con cuadros clave en los cambios de escena).
   `--stills DIR --times 8.5,15.9` exporta cuadros sueltos.

Archivos: `layout.py` (operadores del PDF por elemento y geometría medida), `fit.py` (mide centros de los
círculos y arcos de las fotos), `build.py` (extracción) y `motion.py` (animación y codificación).

## Limitaciones reales

* Las tres fotografías vienen en el PDF a 1920 × 1080 px. En 4K muestran el detalle que contienen, sin detalle
  inventado; los textos, la tarjeta, la pleca, el globo y los logotipos son vectoriales y quedan nítidos a 4K.
* Los círculos que caen sobre las propias fotografías (a la izquierda en las páginas 1 y 2) no se deforman,
  para no tocar a las personas.
