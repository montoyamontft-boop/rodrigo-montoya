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
| `portal-medico.html` | Inicio de sesión del Portal Médico (textos del original) |
| `js/data.js` | Textos de cada página, menú, portafolios y footer |
| `js/catalogo.js` | Los 32 productos del catálogo (generado con `tools/catalogo.py`) |
| `js/fichas.js` | Fichas completas de producto y aviso de privacidad (generado con `tools/fichas.py`) |
| `js/app.js` | Vistas, navegación y animaciones |
| `css/styles.css` | Sistema visual |
| `assets/` | Logo oficial (`logo-chinoin.webp` del header original), imágenes de chinoin.com optimizadas a WebP y fotos de Veterinaria |

Para regenerar catálogo y fichas a partir de las páginas descargadas de chinoin.com:

```bash
python3 tools/catalogo.py <carpeta_html> > js/catalogo.js
python3 tools/fichas.py   <carpeta_html> > js/fichas.js
```

## Cómo funciona la compra / "Ver más" de cada producto

Cada producto tiene su propia página (`#/producto/<id>`) con foto grande y un solo botón principal, según a
dónde mandaba el botón "Ver más" del catálogo original:

| Caso | Productos | Qué hace |
|---|---|---|
| Sitio de la marca | Antiflu-Des, Feel 360, Gotinal Mar, Scabisan Shampoo, Topron, Anara | Abre el sitio oficial de la marca |
| Ficha completa | Neoseverin (tabletas y suspensión), Scabisan (crema y emulsión) | Muestra toda la ficha en acordeón, texto íntegro |
| Solo usuarios registrados | Alin, Flexakocs, Gotinal, Mydocalm-A, Trapazyd, Troferit, Ferranina, Venoferrum | Igual que el original: pide iniciar sesión en el Portal Médico |
| Sin enlace en el original | Benebióticos, Koptin, Aytugre, Anara Solución | Solo la página del producto |

## Errores del sitio original que se encontraron

- **Gelan Plus**: su "Ver más" lleva a `chinoin.com/es/gelan-plus`, que da **error 404**. Aquí no se enlaza.
- **Bene Dual, Koptin y Aytugre**: en el catálogo original el título de la tarjeta enlaza a **otro producto**
  (Antiflu-Des, Gotinal y Troferit). Aquí no se copió ese enlace.
- Todas las demás imágenes del sitio original funcionan (138 revisadas).

## Pendiente

- **Únete al equipo**: la página `chinoin.com/es/unete-al-equipo` no se pudo leer desde el entorno de trabajo;
  falta su texto (se muestra un aviso).
- **Veterinaria**: el catálogo veterinario vive en `chinoinveterinaria.com` (sin acceso todavía). La página ya
  tiene el diseño nuevo con fotos de mascotas y el enlace al sitio veterinario.
- **Formularios**: Farmacovigilancia tiene exactamente los campos del formulario de HubSpot original
  (`portalId 48099646`, `formId 2602e084-…`). En esta maqueta no se envía nada; en producción se conecta a ese
  mismo formulario.

## Créditos de fotos

Las fotos de mascotas de Veterinaria son de [Unsplash](https://unsplash.com) (licencia Unsplash, uso libre).
