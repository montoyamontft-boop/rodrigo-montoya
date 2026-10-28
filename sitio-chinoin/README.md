# CHINOIN · rediseño del sitio web

Propuesta de rediseño de chinoin.com/es: moderna, interactiva y fiel a la marca.
Se conserva tal cual la arquitectura de información del sitio original.

## Ver el sitio

```bash
cd sitio-chinoin
python3 -m http.server 8000
# http://localhost:8000
```

No necesita compilación: HTML, CSS y JavaScript sin dependencias (solo Google Fonts).

## Estructura

| Archivo | Contenido |
|---|---|
| `index.html` | Portada y todas las páginas internas (navegación por `#/ruta`) |
| `portal-medico.html` | Inicio de sesión del Portal Médico (textos idénticos al original) |
| `js/data.js` | **Todo el contenido**: menú, categorías, productos y textos de cada página |
| `js/app.js` | Navegación, mega menú, vistas y animaciones |
| `css/styles.css` | Sistema visual |
| `assets/chinoin-logo.png` | Logo original sin modificar (solo se le quitó el fondo blanco) |

### Rutas

- `#/nosotros/calidad`, `#/nosotros/responsabilidad-social`, `#/nosotros/tecnologia`
- `#/productos`, `#/productos/<grupo>` (areas-terapeuticas, cuidado-de-la-salud, benebioticos, odontologia, veterinaria)
- `#/productos/<categoría>` (respiratorio, gripe-y-resfriado, …) y `#/producto/<id>` con botón **Comprar**
- `#/unidades/mercado-privado`, `venta-a-gobierno`, `exportaciones`, `maquilas`, `huespedes`
- `#/contacto/unete-al-equipo`, `#/contacto/farmacovigilancia`
- `portal-medico.html`

## Identidad

| Token | Valor | Origen |
|---|---|---|
| Naranja logo | `#EF5422` | medido del logo |
| Naranja menú | `#EC5E2A` | medido del menú original |
| Morado | `#321D70` | medido del menú original |
| Durazno | `#FDEFE9` | círculos de íconos del menú original |

## Pendiente

`www.chinoin.com` estaba bloqueado por la red del entorno donde se construyó esta versión, así que
**faltan las fotos de producto, el catálogo y los textos de las páginas internas**. En el sitio se ven como
avisos de "Contenido pendiente" y tarjetas en gris. Para completarlos solo hay que llenar `products` y
`pages` en `js/data.js`. El formato viene comentado ahí.

Los formularios (Farmacovigilancia, Únete al equipo, Portal Médico) son de muestra: hay que conectarlos al
mismo destino que usa el sitio original.
