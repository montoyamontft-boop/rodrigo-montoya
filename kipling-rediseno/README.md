# Kipling School · Campus Satélite y Campus Esmeralda: propuesta de rediseño

Esta es una propuesta visual de los sitios de Kipling School:

- Campus Satélite: [www.kipling.edu.mx](https://www.kipling.edu.mx/)
- Campus Esmeralda: [www.kiplingesmeralda.edu.mx](https://www.kiplingesmeralda.edu.mx/)
- Las secciones de **IB** y **Blog**, que el menú de ambos campus enlaza a [www.kipling.mx](https://www.kipling.mx/)

Mantiene los mismos textos, apartados, enlaces, logotipos e imágenes de los sitios actuales. Solo cambia la interfaz.

## Cómo verlo

**Opción rápida:** abre `kipling-completo.html`. Es un solo archivo con las 132 páginas de los dos campus adentro:

- Al cambiar de página no sales del archivo.
- Desde el menú **Campus** pasas de Satélite a Esmeralda; cambian el logotipo, el menú y el pie de página de cada campus.
- Los videos de YouTube, los mapas y los PDF se abren en una ventana dentro del sitio.
- El buscador busca en el contenido del campus en el que estás.

**Sitio de varias páginas:** Satélite vive en la raíz (`index.html`, `paginas/`) y Esmeralda en `esmeralda/`. Hay que abrirlo con un servidor local, porque si se abre con doble clic los formularios y los mapas incrustados pueden no cargar.

```bash
cd kipling-rediseno
```

```bash
python3 -m http.server 8000
```

Después abre http://localhost:8000 en el navegador.

Para compartir un enlace público, se puede activar GitHub Pages en este repositorio y apuntarlo a la carpeta `kipling-rediseno/`.

## Qué se conserva de los sitios originales

- **Textos.** Se copiaron tal cual:
  - 52 direcciones de Satélite
  - 49 de Esmeralda
  - 36 de IB y Blog

  Una revisión automática comparó 5,154 fragmentos de texto y no encontró ninguno faltante ni modificado.
- **Estructura.** El menú de cada campus es el mismo que en su sitio: ¿Quiénes somos?, Campus, Secciones, IB, Horario Extendido, Blog y HACER UNA CITA, con todos sus submenús. La página principal conserva el mismo orden:
  1. Aviso "Come & Join"
  2. "Confianza y valores que perduran"
  3. Accesos rápidos
  4. Noticias Recientes
  5. Mensaje de bienvenida
  6. Secciones
  7. Galería
  8. Pie de página
- **Páginas interiores.** Conservan sus menús laterales, documentos PDF, formularios de solicitud (Nord Anglia / FormAssembly), mapas, videos de Vimeo, galerías y noticias.
- **Logotipos.** Se usan los archivos oficiales sin modificar:
  - Satélite: `assets/img/header_logo.png`
  - Esmeralda: `assets/img/esmeralda/header_logo.png`
  - Ambos campus: `footer_logo.png` y el logo IB
- **Colores.** La paleta sale del propio logotipo: carmesí `#B40029`, rojo `#F9001C`, azul `#0088D0` y verde `#4FD927`.
- **Imágenes.** Se cargan desde el servidor original del colegio (`3.files.edl.io`) sin recomprimir, recortar ni editar:
  - Los carruseles ofrecen todas las versiones que publica el colegio, hasta 6000 px. El navegador elige la adecuada según la pantalla.
  - La galería ampliada siempre abre el archivo de mayor resolución.
  - Las fotos e infografías se muestran completas, nunca recortadas ni estiradas por encima de su tamaño real.
- **Enlaces externos.** Siguen apuntando a sus direcciones originales:
  - Portales de pago (SSM)
  - Secciones con contraseña (Comunidad Kipling, Colaboradores)
  - WhatsApp
  - Sitios externos citados en los artículos

## Qué cambia en la interfaz

- **Portada.** Ocupa toda la pantalla con un acercamiento lento sobre la foto principal y una animación de entrada en el título. Lleva bandas diagonales inspiradas en la "K" del logotipo.
- **Encabezado.** Es transparente sobre la portada y se vuelve blanco translúcido al bajar. Se oculta al hacer scroll hacia abajo y reaparece al subir.
- **Menús.** En escritorio los submenús se despliegan como tarjetas. En móvil hay un menú lateral con acordeones.
- **Botón de cita.** "HACER UNA CITA" queda fijo abajo en el celular.
- **Accesos rápidos.** Admisiones, Portal de Pagos y Comunidad Kipling aparecen como tarjetas que se encienden al pasar el cursor.
- **Noticias.** Se muestran como tarjetas, y la convocatoria "Come & Join" va destacada.
- **Blog.** Los artículos que el sitio original solo listaba en el menú lateral ahora aparecen también como tarjetas con su foto y sus primeras líneas.
- **Secciones (el espacio dinámico).** Son paneles que se expanden al pasar el cursor y avanzan solos.
- **Galería.** Es una cinta en movimiento continuo. Al hacer clic se abre en grande, con navegación por teclado y gestos táctiles.
- **Carruseles de las páginas interiores.** Usan fondo difuminado de la misma foto para no recortarla, y llevan barra de progreso.
- **Aviso "Come & Join".** "No mostrar de nuevo" sí se recuerda en el navegador.
- **Accesibilidad.** Hay enlace para saltar al contenido, foco visible y la tecla Escape cierra cualquier ventana. Se respeta la opción del sistema de reducir movimiento, y el diseño es responsivo de 320 px a pantallas grandes.

## Errores del sitio original que aquí ya no aparecen

- **Correo de admisiones.** En el artículo "Tecnología educativa en Kipling, preguntas y respuestas", el correo `admisiones@kipling.edu.mx` enlazaba a una dirección rota (`https://n@kipling.edu.mx`). Ahora abre el correo.
- **Menú Campus de Esmeralda.** Apuntaba a una página que da error 404. Aquí abre su submenú (Campus Satélite / Campus Esmeralda).
- **Menú lateral de "Proceso de Admisión".** Usaba direcciones distintas a las del resto del sitio. Aquí todas llevan a la misma página rediseñada.
- **Fotos del artículo EMAT.** Pasaban por una redirección. Ahora apuntan directo a su archivo original.
- **Videos de Vimeo.** Venían con la dirección mal escrita (`&amp;amp;`). Aquí está corregida.

## Cómo se generó

En `_fuente/` está todo lo necesario para regenerar el sitio si el colegio actualiza su contenido:

| Archivo | Función |
|---|---|
| `crawl.py` | Descarga las páginas públicas de un sitio de Kipling |
| `extract.py` | Extrae textos, menús, galerías, documentos y noticias a JSON |
| `content.json`, `content_esmeralda.json`, `content_grupo.json` | Contenido de Satélite, Esmeralda e IB/Blog |
| `build.py` | Genera los dos campus y `kipling-completo.html` |
| `mapa-urls.json` | Relación de cada dirección original con su página rediseñada |
| `redirecciones.json` | Dirección final de las imágenes que el sitio original sirve con redirección |

```bash
python3 _fuente/crawl.py https://www.kipling.edu.mx/ /tmp/sat --depth 3
```

```bash
python3 _fuente/crawl.py https://www.kiplingesmeralda.edu.mx/ /tmp/esm --depth 3
```

```bash
python3 _fuente/crawl.py https://www.kipling.mx/ /tmp/grupo --seeds /apps/pages/bachilleratointernacional /apps/pages/blog --only 'uREC_ID=(1831034|4122469)' --depth 1
```

```bash
python3 _fuente/extract.py /tmp/sat _fuente/content.json https://www.kipling.edu.mx/
```

```bash
python3 _fuente/extract.py /tmp/esm _fuente/content_esmeralda.json https://www.kiplingesmeralda.edu.mx/
```

```bash
python3 _fuente/extract.py /tmp/grupo _fuente/content_grupo.json https://www.kipling.mx/
```

```bash
python3 _fuente/build.py
```

Lo que no se incluyó: el crédito "Powered by Edlio", que pertenece al proveedor de la plataforma y no al colegio, y el traductor de Google del pie de página.
