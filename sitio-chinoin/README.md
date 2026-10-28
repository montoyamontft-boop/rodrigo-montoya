# CHINOIN · rediseño del sitio web

Rediseño de chinoin.com/es: moderno, interactivo y fiel a la marca. **Los textos, imágenes, productos y la
estructura de menús son los del sitio original** (leídos de chinoin.com en octubre de 2026). Las rutas usan las
mismas direcciones que el original (`#/catalogo`, `#/portafolio-respiratorios`, `#/gripe-y-resfriado`, …) para
que sea fácil comparar página por página.

## Ver el sitio

```bash
cd sitio-chinoin
python3 -m http.server 8000      # http://localhost:8000
```

O genera una vista previa en un solo archivo (se abre con doble clic, sin servidor):

```bash
python3 sitio-chinoin/tools/bundle.py chinoin-preview.html
```

## Estructura

| Archivo | Contenido |
|---|---|
| `index.html` | Todas las páginas (navegación por `#/ruta`) |
| `portal-medico.html` | Portal Médico: portada de Conexión Chinoin, acceso y registro (textos de emc.chinoin.com) |
| `js/data.js` | Textos de cada página, menú, portafolios y footer |
| `js/catalogo.js` | Los 32 productos del catálogo (generado con `tools/catalogo.py`) |
| `js/fichas.js` | Fichas completas de producto y aviso de privacidad (generado con `tools/fichas.py`) |
| `js/marcas.js` | Información y tiendas de los sitios de Antiflu-Des, Anara, Feel 360, Gotinal Mar, Scabisan y Topron (generado con `tools/marcas.py`) |
| `js/veterinaria.js` | 74 productos veterinarios, sus fichas, empresa e historia de chinoinveterinaria.com (generado con `tools/veterinaria.py`) |
| `js/app.js` | Vistas, navegación y animaciones |
| `css/styles.css` | Sistema visual |
| `assets/` | Logo oficial (`logo-chinoin.webp` del header original), imágenes de chinoin.com optimizadas a WebP y fotos de Veterinaria |

Para regenerar catálogo y fichas a partir de las páginas descargadas de chinoin.com:

```bash
python3 tools/catalogo.py <carpeta_html> > js/catalogo.js
python3 tools/fichas.py   <carpeta_html> > js/fichas.js
python3 tools/veterinaria.py <carpeta_html_veterinaria> lista_imagenes.txt > js/veterinaria.js
```

## Portada

- **Órbita de productos** en el hero, contadores animados (100 años, 3 plantas, 8 países, productos, 1,700 MWh, 80 %)
  y franja de tiendas tomada de los sitios de marca.
- **Banners recreados en HTML** (Great Place to Work, Conexión Chinoin y 100 años): los originales eran imágenes
  con el texto incrustado y poca resolución; aquí el texto es el mismo, palabra por palabra, pero se dibuja nítido
  a cualquier tamaño. En móvil cambian a formato vertical para que se lean grandes.
- **Círculo dorado** dibujado en HTML con los textos y pilares de la imagen original (que medía 374×340 px y se
  veía borrosa).
- **Línea del tiempo interactiva**: la infografía original (1912–2025) se reconstruyó con sus 20 hitos transcritos
  tal cual y los emblemas recortados a resolución completa; se recorre con el scroll o con los botones de año.

## Imágenes en alta calidad

- `tools/mejorar_imagenes.py` aumenta la resolución con superresolución EDSR (x2/x4) y un afinado ligero. Se usó en
  el anillo de experiencia, el círculo dorado, el mapa de América, las imágenes de "industria limpia", el logo de
  100 años, el logo de Conexión Chinoin, las 8 imágenes de especialidades del Portal Médico y la médica del Portal.
- El médico del inicio del Portal Médico es una foto de stock en alta resolución recortada con `rembg`; los iconos,
  el aro y el círculo naranja que lo acompañan se dibujan en CSS/SVG para que no pierdan nitidez.
- Las fotos de instalaciones de Tecnología medían 390×260 px y no mejoraban lo suficiente; se reemplazaron por
  fotos de stock en alta resolución (la del almacén es la original). También son de stock las fotos de
  laboratorio y médicos de la portada (`assets/img/stock/`).

## Portal Médico

`portal-medico.html` reproduce la portada pública de emc.chinoin.com (Conexión Chinoin): plataforma de
educación médica continua, 8 especialidades, qué encontrará y registro. "Acceso" abre el inicio de sesión y
"Regístrese" abre el registro con los mismos campos y opciones del formulario original (correo, nombre como en la
cédula, cédula profesional, especialidad, hasta 3 portafolios de interés, estado, código postal y ciudad).

## Veterinaria

Antes el menú mandaba a chinoinveterinaria.com en otra pestaña; ahora es una sección del sitio
(`#/veterinaria`) con el contenido de ese sitio:

- **74 productos** de las líneas Pequeñas Especies (Farmacéutica, Oftálmicos, Vacunas) y Grandes Especies
  (Farmacéutica, Biológicos), con filtros por línea, especie y categoría, y buscador por nombre o principio activo.
- **Fichas**: 17 productos tienen ficha completa en texto (descripción, mecanismo, dosis, advertencias,
  presentación); los otros 57 en el original solo tienen una línea y una imagen con la información, que aquí
  se muestra ampliable.
- **Menú anatómico** (Bovinos, Ovinos, Caprinos, Porcinos, Equinos, Caninos, Felinos): en el original esas
  páginas solo tienen una foto; aquí muestran los productos cuya ficha indica uso en esa especie.
- Lanzamientos recientes, historia (1912–2014), empresa (misión, valores, visión, cultura), APP del Dolor y
  contacto de ventas y gerencia médica.
- Detalles del original que se corrigieron al copiar: una tarjeta vacía, Parastin Puppy duplicado (una de sus
  tarjetas enlazaba a `#`) y una categoría marcada como "Audio" en Vacufive 5V.

## Cómo funciona la compra / "Ver más" de cada producto

Cada producto tiene su propia página (`#/producto/<id>`) con foto grande y un solo botón principal, según a
dónde mandaba el botón "Ver más" del catálogo original:

| Caso | Productos | Qué hace |
|---|---|---|
| Dónde comprar | Antiflu-Des, Feel 360, Gotinal Mar, Scabisan Shampoo, Topron, Anara | Lista de farmacias con enlace directo (las que publica cada marca en su sitio), ficha del producto copiada de ese sitio y enlace al sitio oficial |
| Ficha completa | Neoseverin (tabletas y suspensión), Scabisan (crema y emulsión) | Muestra toda la ficha en acordeón, texto íntegro |
| Solo usuarios registrados | Alin, Flexakocs, Gotinal, Mydocalm-A, Trapazyd, Troferit, Ferranina, Venoferrum | Igual que el original: pide iniciar sesión en el Portal Médico |
| Sin enlace en el original | Benebióticos, Koptin, Aytugre, Anara Solución | Solo la página del producto |

## Errores del sitio original que se encontraron

- **Gelan Plus**: su "Ver más" lleva a `chinoin.com/es/gelan-plus`, que da **error 404**. Aquí no se enlaza.
- **Bene Dual, Koptin y Aytugre**: en el catálogo original el título de la tarjeta enlaza a **otro producto**
  (Antiflu-Des, Gotinal y Troferit). Aquí no se copió ese enlace.
- Todas las demás imágenes del sitio original funcionan (138 revisadas).

## Notas sobre los sitios de marca

- Antiflu-Des publica la denominación genérica y las indicaciones como imagen; aquí se transcribieron a texto, tal cual.
- En Gotinal Mar la frase sobre la tecnología Bag-On-Valve termina con los logotipos de Gotinal Mar Soft y Defense;
  aquí se escribieron sus nombres para que la frase se lea completa.

## Pendiente

- **Únete al equipo**: la página `chinoin.com/es/unete-al-equipo` no se pudo leer desde el entorno de trabajo;
  falta su texto (se muestra un aviso).
- **Formularios**: Farmacovigilancia tiene exactamente los campos del formulario de HubSpot original
  (`portalId 48099646`, `formId 2602e084-…`). En esta maqueta no se envía nada; en producción se conecta a ese
  mismo formulario.

## Créditos de fotos

Las fotos de mascotas de la portada de Veterinaria y las de `assets/img/stock/` (laboratorio, médicos, tabletas) son de
[Unsplash](https://unsplash.com) (licencia Unsplash, uso libre). Antes de publicar conviene sustituirlas por fotos
propias de CHINOIN si las hay.
