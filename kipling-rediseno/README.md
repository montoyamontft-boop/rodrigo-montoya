# Kipling School · Campus Satélite: propuesta de rediseño

Esta es una propuesta visual del sitio [www.kipling.edu.mx](https://www.kipling.edu.mx/).
Mantiene los mismos textos, apartados, enlaces, logotipos e imágenes del sitio actual.
Solo cambia la interfaz.

## Cómo verlo

Hay que abrirlo con un servidor local. Si se abre el archivo con doble clic, los formularios y los mapas incrustados pueden no cargar.

```bash
cd kipling-rediseno
```

```bash
python3 -m http.server 8000
```

Después abre http://localhost:8000 en el navegador.

Para compartir un enlace público, se puede activar GitHub Pages en este repositorio y apuntarlo a la carpeta `kipling-rediseno/`.

## Qué se conserva del sitio original

- **Textos.** Se copiaron tal cual de las 47 direcciones públicas del sitio. Una revisión automática comparó 592 fragmentos de texto y no encontró ninguno faltante ni modificado.
- **Estructura.** El menú es el mismo: ¿Quiénes somos?, Campus, Secciones, IB, Horario Extendido, Blog y HACER UNA CITA, con todos sus submenús. La página principal conserva el mismo orden:
  1. Aviso "Come & Join"
  2. "Confianza y valores que perduran"
  3. Accesos rápidos
  4. Noticias Recientes
  5. Mensaje de bienvenida
  6. Secciones
  7. Galería
  8. Pie de página
- **Páginas interiores.** Conservan sus menús laterales, documentos PDF, formularios de solicitud (Nord Anglia / FormAssembly), mapas, videos de Vimeo, galerías y noticias.
- **Logotipos.** Se usan los archivos oficiales sin modificar: `header_logo.png`, `footer_logo.png` y el logo IB.
- **Colores.** La paleta sale del propio logotipo: carmesí `#B40029`, rojo `#F9001C`, azul `#0088D0` y verde `#4FD927`.
- **Imágenes.** Se cargan desde el servidor original del colegio (`3.files.edl.io`) sin recomprimir, recortar ni editar:
  - Los carruseles ofrecen todas las versiones que publica el colegio, hasta 6000 px. El navegador elige la adecuada según la pantalla.
  - La galería ampliada siempre abre el archivo de mayor resolución.
  - Las fotos dentro del contenido se muestran completas, sin recortes.
- **Enlaces externos.** Los portales de pagos (SSM), las secciones con contraseña (Comunidad Kipling, Colaboradores), IB y Blog en kipling.mx, Campus Esmeralda, YouTube y el buscador del sitio siguen apuntando a sus direcciones originales.

## Qué cambia en la interfaz

- **Portada.** Ocupa toda la pantalla con un acercamiento lento sobre la foto principal y una animación de entrada en el título. Lleva bandas diagonales inspiradas en la "K" del logotipo.
- **Encabezado.** Es transparente sobre la portada y se vuelve blanco translúcido al bajar. Se oculta al hacer scroll hacia abajo y reaparece al subir.
- **Menús.** En escritorio los submenús se despliegan como tarjetas. En móvil hay un menú lateral con acordeones.
- **Botón de cita.** "HACER UNA CITA" queda fijo abajo en el celular.
- **Accesos rápidos.** Admisiones, Portal de Pagos y Comunidad Kipling aparecen como tarjetas que se encienden al pasar el cursor.
- **Noticias.** Se muestran como tarjetas, y la convocatoria "Come & Join" va destacada.
- **Secciones (el espacio dinámico).** Son paneles que se expanden al pasar el cursor y avanzan solos.
- **Galería.** Es una cinta en movimiento continuo. Al hacer clic se abre en grande, con navegación por teclado y gestos táctiles.
- **Carruseles de las páginas interiores.** Usan fondo difuminado de la misma foto para no recortarla, y llevan barra de progreso.
- **Aviso "Come & Join".** "No mostrar de nuevo" sí se recuerda en el navegador.
- **Accesibilidad.** Hay enlace para saltar al contenido, foco visible y la tecla Escape cierra cualquier ventana. Se respeta la opción del sistema de reducir movimiento, y el diseño es responsivo de 320 px a pantallas grandes.

## Cómo se generó

En `_fuente/` está todo lo necesario para regenerar el sitio si el colegio actualiza su contenido:

| Archivo | Función |
|---|---|
| `crawl.py` | Descarga las páginas públicas de kipling.edu.mx |
| `extract.py` | Extrae textos, menús, galerías, documentos y noticias a `content.json` |
| `build.py` | Genera `index.html` y `paginas/*.html` a partir de `content.json` |
| `mapa-urls.json` | Relación de cada dirección original con su página rediseñada |

```bash
python3 _fuente/crawl.py /ruta/temporal
```

```bash
python3 _fuente/extract.py /ruta/temporal _fuente/content.json
```

```bash
python3 _fuente/build.py
```

Lo que no se incluyó: el crédito "Powered by Edlio", que pertenece al proveedor de la plataforma y no al colegio, y el traductor de Google del pie de página.
