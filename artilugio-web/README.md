# Artilugio Group: sitio web interactivo

Rediseño de una sola página para artilugiogroup.com.mx. Es HTML, CSS y JS estáticos, sin build: basta con subir esta carpeta al hosting.

## Qué incluye

- **Paleta de marca.** Solo los colores de los backs y del logotipo (azul, cian, naranja, rojo y ámbar sobre blanco y azul marino), usados como colores sólidos.
- **Fondos que cambian al deslizar.** Los dos backs se funden según el tema de cada sección (`data-theme="light|dark"`). El degradado de fondo está en `assets/base-*` y la red de nodos aparece sutil solo en los laterales (`assets/side-*`).
- **Hero con el logo al centro de una red 3D** que reacciona al cursor y se puede arrastrar. Al bajar, la red cambia de forma en cada sección (`data-globe="x y radio dispersión opacidad"`; `data-globe-m` es la versión móvil).
- **Marcas.** Cuadrícula de tarjetas con los logos en gris; al pasar el cursor, el logo se enciende en sus colores originales (en pantallas táctiles se muestran a color).
- **Servicios: de la prescripción al consumo.** Carrusel horizontal que avanza con el scroll vertical, con la barra Prescripción → Consumo y flechas. En móvil se desliza con el dedo.
- **Escena Spline** en «Experiencia 3D». Se carga cuando el visitante se acerca y se activa con «Interactuar», así no atrapa el scroll.
- **Menú siempre visible.** En pantallas angostas los enlaces se desplazan de lado. El logo de la esquina no aparece en la primera pantalla.
- **Todo se queda en la página.** Ningún botón ni enlace lleva a otro sitio.
- Adaptable a móvil y compatible con `prefers-reduced-motion`.

## Logos de marcas

`assets/marcas/<id>.svg` son vectores en los colores originales de cada marca, obtenidos del video del sitio actual (el estado a color al pasar el cursor) y vectorizados por capa de color. Son nítidos a cualquier tamaño; los textos muy pequeños de algunos logos (por ejemplo, el lema de Psicofarma) pierden algo de detalle. Psicofarma va en negro. Si consigues los archivos oficiales, reemplaza el SVG con el mismo nombre.

Para agregar o quitar marcas, edita el arreglo `BRANDS` de `index.html` (`id`, `name` y `ar`, que es ancho entre alto del logo).

## Servicios

Las seis tarjetas (Rx & Éticos, Genéricos de Marca & OTX, OTC & Consumo, Dispositivos Médicos, Suplementos & Nutracéuticos y Enfermedades Raras) están en el arreglo `SERVICES` de `index.html`, con el color de su número en `c`.

## Logotipos de Artilugio

Los logos se extrajeron del PDF de backs sin modificarlos:
- `logo-artilugio.svg`: versión vectorial con texto oscuro, para fondos claros.
- `logo-artilugio-dark.webp/.png`: versión con texto blanco, para fondos oscuros.

## Contacto

Los mensajes del formulario se dirigen a raquel@artilugiogroup.com.mx y myrnar@artilugiogroup.com.mx (atributo `data-email` de `#contactForm`, separados por coma); ambos correos también aparecen visibles en la sección de contacto. Al enviar, el formulario abre la aplicación de correo del visitante con el mensaje listo. Si prefieres que se envíe directo sin abrir el correo, hay que conectarlo a un backend o a un servicio de formularios.

## Pendientes antes de publicar

1. **Textos originales.** Revisa contra el sitio en vivo, sobre todo el párrafo de «Quiénes somos» y el del origen griego del nombre (hay un comentario en la sección `#artilugio` que marca dónde va).

## Probar en local

```bash
cd artilugio-web
python3 -m http.server 8080
# abre http://localhost:8080
```
