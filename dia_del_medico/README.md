# Día del Médico (CHINOIN): video de motion graphics

Conversión de `DIA DEL MEDICO - B.pdf` (3 páginas, Adobe Illustrator, 1920 × 1080 pt) en una pieza animada
de tres escenas unidas por un mismo hilo: **la onda turquesa de puntos**, que recorre cada fondo, lleva
cada mensaje y revela la escena siguiente.

| | |
|---|---|
| Salida | `salida/dia_del_medico_4k.mp4` (generado; el PDF y el video no se versionan porque el repositorio es público) |
| Resolución | 3840 × 2160 (16:9) |
| Frecuencia | 30 fps constantes, 780 cuadros |
| Duración | 26,0 s |
| Códec | H.264 High, yuv420p, BT.709 (rango TV), CRF 14, sin audio |

## Fidelidad: qué se usa y qué no

* **Nada se regenera.** Cada texto, comilla, marco, logotipo y la marca CHINOIN se extrae del propio PDF como
  capa vectorial rasterizada a 4K con MuPDF y sus tipografías incrustadas (Akzidenz-Grotesk BQ Medium,
  Bad Script y Montserrat SemiBold). Las tres fotografías de fondo son las imágenes originales del PDF.
* **Modos de fusión exactos.** Las sombras del texto usan Multiplicar y los paneles usan opacidad. Cada capa
  se renderiza sobre fondo negro y sobre fondo blanco, y así se obtiene `resultado = fondo × F + A`
  por píxel. Esto es exacto para Normal, Multiplicar y Trama, así que las capas se recomponen bien aunque el
  fondo se mueva. Recomposición contra el PDF: diferencia máxima ≤ 3/255 en las tres páginas.
* **Verificación.** En los cuadros de lectura, los píxeles opacos del primer plano coinciden con el render
  directo del PDF a 4K (diferencia máxima 1–2/255). El resto de la diferencia es solo la actividad
  del fondo: la deriva lenta y la luz que recorre la onda.
* **Recursos aplanados.** El instrumental, la onda, el médico, el escudo y la cruz forman parte de la fotografía
  de fondo, no son capas. Por eso no se recortan: la profundidad se crea con un campo de desplazamiento suave
  (plano cercano / plano lejano) cuya transición cae en zonas lisas del degradado. Los objetos se mueven
  rígidos, sin deformarse, y al final de cada escena el fondo llega exactamente a su posición original.
  El escudo y la cruz se revelan con máscaras sobre la misma foto atenuada. Los pulsos de luz solo
  iluminan los nodos y las líneas que ya existen en la imagen: `network.py` detecta 362 nodos y 492
  conexiones reales del escudo.
* **CHINOIN** se compone al final de cada cuadro, fijo y sin transformaciones, durante todo el video.

## Coreografía

Tiempos en segundos del video. Detalle completo en `motion.py` (`CHOREO`, `PULSES`, `DEPTH`).

**Escena 1. Cada historia comienza con una conexión (0–10,4)**
* 0–1,4: desde el azul marino de la campaña, la onda revela el fondo: la luz avanza por la onda y desde ella
  se abre la fotografía. El instrumental (plano cercano) se asienta con escala y desplazamiento contrarios
  a los de la onda (plano lejano): parallax sin deformación.
* 1,15: la comilla de apertura aparece con una escala breve y después entran sus glifos con máscara.
  1,45: el marco blanco se traza **desde la comilla en dos direcciones**, con una pequeña luz en cada punta.
  El punto de encuentro, a la mitad del perímetro, cae exactamente bajo la comilla de cierre.
* Las frases alternan dos entradas: Akzidenz con máscara ascendente o lateral, y Bad Script con un barrido
  suave de izquierda a derecha que deja los glifos intactos. Cada frase lanza un pulso de luz por la onda.
* 6,35: la comilla de cierre sella la historia. Lectura completa hasta 9,0.

**Escena 2. El momento de celebrar (9,0–17,4)**
* La luz continúa por la onda de la página 2 y revela el nuevo fondo y la fotografía del médico, que
  permanece intacta y fija. Solo el fondo izquierdo deriva y la onda ondula muy levemente.
* 10,2: «23» entra con escala breve y firme (1,22 → 1, sin rebote). Las comillas superiores caen con
  máscara y el trazo superior del marco se dibuja desde ellas. Después siguen «de octubre» (barrido)
  y «Día del Médico» (máscara ascendente), escalonados.
* 12,2: el trazo inferior termina, entran las comillas de cierre y un pulso intenso recorre la onda.
  Ese es el momento de celebración. Lectura hasta 16,0.

**Escena 3. El cuidado se convierte en protección (16,0–26,0)**
* La onda de la página 3 llega desde arriba a la izquierda y conecta con la red del escudo, que espera en
  penumbra. Desde el punto de contacto, un frente de luz revela la red y enciende sus líneas al pasar.
* 17,55: los brazos de la cruz se abren desde el centro con un destello breve que se asienta en el
  original. Desde 18,4, pulsos de luz recorren las conexiones existentes de la red.
* «Gracias por hacer» (18,75), «de la salud» (19,6, barrido lento) y «tu propósito.» (20,75) entran con
  una progresión pausada. Después entran los cuatro logotipos de izquierda a derecha y la leyenda.
  Todo queda visible desde 23,8 hasta el final, con el fondo en actividad suave.

Las salidas de cada escena se escalonan en el orden de entrada (fundido y leve deriva en el sentido del flujo),
justo antes de que la onda de la escena siguiente las cubra.

## Regenerar el video

Requisitos: Python 3.10+, `pip install -r pipeline/requirements.txt`, y `ffmpeg` con libx264.

```bash
./dia_del_medico/make_video.sh RUTA/AL/DIA_DEL_MEDICO_-_B.pdf            # 4K    -> salida/dia_del_medico_4k.mp4
SCALE=0.5 ./dia_del_medico/make_video.sh RUTA/AL/DIA_DEL_MEDICO_-_B.pdf  # 1080p -> vista previa rápida
```

Pasos internos:

1. `build.py PDF build/medico`: capas 4K (F/A) y placas de fondo, con verificación de recomposición (~1,5 min).
2. `motion.py build/medico salida.mp4 --scale 1.0 --workers 3 --crf 14 --preset slow`: render en paralelo
   con un único codificador, de modo que no haya costuras entre bloques y los cuadros clave caigan en los
   cambios de escena. En 4 núcleos tarda unos 15–20 min en 4K y menos de 2 min en 1080p.
   `--stills DIR --times 9.5,16.5` exporta cuadros sueltos para revisión.

Archivos: `layout.py` (índices de operadores del PDF por elemento y la geometría medida: ondas, marcos,
escudo, cruz), `build.py` (extracción), `network.py` (red del escudo), `motion.py` (animación y codificación).

## Limitaciones reales

* Las tres fotografías de fondo vienen en el PDF a 1920 × 1080 px. En 4K muestran el detalle que contienen
  (escalado bicúbico), sin detalle inventado. Textos, comillas, marcos y logotipos son vectoriales y
  quedan nítidos a 4K.
* El escudo, la cruz y la onda no existen como capas separadas. Por eso sus revelados son máscaras y luz sobre la
  foto original, nunca recortes.
