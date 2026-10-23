# Artilugio Group: sitio web interactivo

Rediseño de una sola página para artilugiogroup.com.mx. Es HTML, CSS y JS estáticos, sin build: basta con subir esta carpeta al hosting. Se debe servir por HTTP (no abriendo el archivo con doble clic), porque los logos de marcas se cargan como máscaras CSS.

## Qué incluye

- **Paleta de marca.** Solo los colores de los backs y del logotipo (azul, cian, naranja, rojo y ámbar sobre blanco y azul marino), usados como colores sólidos.
- **Fondos que cambian al deslizar.** Los dos backs se funden según el tema de cada sección (`data-theme="light|dark"`). El degradado de fondo está en `assets/base-*` y la red de nodos aparece sutil solo en los laterales (`assets/side-*`).
- **Hero con el logo al centro de una red 3D** que reacciona al cursor y se puede arrastrar. Al bajar, la red cambia de forma en cada sección (`data-globe="x y radio dispersión opacidad"`; `data-globe-m` es la versión móvil).
- **Marcas.** Cuadrícula de tarjetas con los logos en gris; al pasar el cursor, el logo se enciende en sus colores originales (en pantallas táctiles se muestran a color).
- **Servicios: de la prescripción al consumo.** Carrusel horizontal que avanza con el scroll vertical, con la barra Prescripción → Consumo y flechas. En móvil se desliza con el dedo.
- **Reseñas.** Carrusel de testimonios con el logo de la marca del cliente.
- **Escena Spline** en «Experiencia 3D». Se carga cuando el visitante se acerca y se activa con «Interactuar», así no atrapa el scroll.
- **Menú siempre visible.** En pantallas angostas los enlaces se desplazan de lado. El logo de la esquina no aparece en la primera pantalla.
- **Todo se queda en la página.** Ningún botón ni enlace lleva a otro sitio.
- Adaptable a móvil y compatible con `prefers-reduced-motion`.

## Logos de marcas

`assets/marcas/<id>.svg` son vectores en los colores originales de cada marca, obtenidos del video del sitio actual (el estado a color al pasar el cursor) y vectorizados por capa de color. Son nítidos a cualquier tamaño; los textos muy pequeños de algunos logos (por ejemplo, el lema de Psicofarma) pierden algo de detalle. Psicofarma nunca aparece a color en el video, así que está en gris oscuro. Si consigues los archivos oficiales, reemplaza el SVG con el mismo nombre.

Para agregar o quitar marcas, edita el arreglo `BRANDS` de `index.html` (`id`, `name` y `ar`, que es ancho entre alto del logo).

## Servicios

Las tarjetas están en el arreglo `SERVICES` de `index.html`. Las 01, 02 y 03 están marcadas `pending: true` porque falta su texto: solo se muestran en la vista previa. Al pegar su título y texto, quita `pending`.

## Reseñas

Agrega cada reseña al arreglo `REVIEWS` de `index.html`:

```js
{ text: 'Texto de la reseña', name: 'Nombre', role: 'Cargo · Empresa', brand: 'novartis' }
```

`brand` es opcional y debe ser un `id` de `BRANDS`. Mientras el arreglo esté vacío, la sección y su enlace en el menú no se muestran.

## Logotipos de Artilugio

Los logos se extrajeron del PDF de backs sin modificarlos:
- `logo-artilugio.svg`: versión vectorial con texto oscuro, para fondos claros.
- `logo-artilugio-dark.webp/.png`: versión con texto blanco, para fondos oscuros.

## Pendientes antes de publicar

1. **Reseñas** y **servicios 01–03.** Pegar los textos reales (ver arriba).
2. **Textos originales.** Revisa contra el sitio en vivo, sobre todo el párrafo de «Quiénes somos» y el del origen griego del nombre (hay un comentario en la sección `#artilugio` que marca dónde va).
3. **Contacto.** Escribe el correo de destino en `data-email` del formulario `#contactForm`. El formulario abre el cliente de correo del visitante. Si prefieres envío directo, conecta el formulario a tu backend o a un servicio de formularios.

## Probar en local

```bash
cd artilugio-web
python3 -m http.server 8080
# abre http://localhost:8080
```
