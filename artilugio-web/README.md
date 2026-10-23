# Artilugio Group: sitio web interactivo

Rediseño de una sola página para artilugiogroup.com.mx. Es HTML, CSS y JS estáticos, sin build: basta con subir esta carpeta al hosting.

## Qué incluye

- **Tipografía Montserrat** en toda la página, incluida en `assets/fonts/` (licencia SIL Open Font License), así que no depende de Google Fonts.
- **Paleta de marca.** Solo los colores de los backs y del logotipo (azul, cian, naranja, rojo y ámbar sobre blanco y azul marino), usados como colores sólidos.
- **Fondos que cambian al deslizar.** Los dos backs se funden según el tema de cada sección (`data-theme="light|dark"`). El degradado de fondo está en `assets/base-*` y la red de nodos aparece sutil solo en los laterales (`assets/side-*`).
- **Contenido del sitio actual**, seccionado igual: Inicio (¿Quiénes somos?), Acerca de (áreas comerciales y de Marketing; Compromiso social), Servicios (Pilares estratégicos; Especialización de la prescripción al consumo; Experiencia 3D; Nuestro equipo; Artilugio; Clientes) y Contacto.
- **Franja de valores** bajo el inicio (Profesionales de la salud · Pacientes · Terapias de alto valor) y franja en movimiento con los conceptos del sitio (Adopción, Retención, Estrategia médica, Programas de pacientes y los pilares).
- **Nuestro equipo como rueda de rompecabezas:** los 10 puestos son piezas de colores alrededor del logo (el diseño de la imagen del equipo). La rueda gira lentamente (los textos se mantienen derechos). Al llegar a la sección, las piezas se arman una por una con el scroll; después un foco recorre la rueda y el puesto activo se muestra junto al título. Al pasar el cursor o tocar una pieza, esta se levanta y las demás se atenúan. El arreglo `TEAM` de `index.html` tiene el nombre, los saltos de línea y el color de cada pieza.
- **Encabezado como el del sitio actual:** logo a la izquierda y Inicio · Acerca de · Servicios · Contacto a la derecha; el enlace de la parte donde estás se marca en azul.
- **Inicio con el logo al centro de una red 3D** que reacciona al cursor y se puede arrastrar. Al bajar, la red cambia de forma en cada sección (`data-globe="x y radio dispersión opacidad"`; `data-globe-m` es la versión móvil).
- **Marcas.** Cuadrícula de tarjetas con los logos en gris; al pasar el cursor, el logo se enciende en sus colores originales (en pantallas táctiles se muestran a color).
- **Servicios: de la prescripción al consumo.** Carrusel horizontal que avanza con el scroll vertical, con la barra Prescripción → Consumo y flechas. En móvil se desliza con el dedo.
- **Escena Spline** en «Experiencia 3D», después de «Especialización de la prescripción al consumo». Se carga cuando el visitante se acerca y se activa con «Interactuar», así no atrapa el scroll.
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

Los mensajes del formulario se dirigen a raquel@artilugiogroup.com.mx y myrnar@artilugiogroup.com.mx (atributo `data-email` de `#contactForm`, separados por coma); en la sección de contacto se muestra myrnar@artilugiogroup.com.mx, como en el sitio actual. Al enviar, el formulario abre la aplicación de correo del visitante con el mensaje listo. Si prefieres que se envíe directo sin abrir el correo, hay que conectarlo a un backend o a un servicio de formularios.

## Probar en local

```bash
cd artilugio-web
python3 -m http.server 8080
# abre http://localhost:8080
```
