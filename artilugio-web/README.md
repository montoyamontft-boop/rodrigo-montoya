# Artilugio Group: sitio web interactivo

Rediseño de una sola página para artilugiogroup.com.mx. Es HTML, CSS y JS estáticos, sin build: basta con subir esta carpeta al hosting.

## Qué incluye

- **Paleta de marca.** Solo los colores de los backs y del logotipo (azul, cian, naranja, rojo y ámbar sobre blanco y azul marino), usados como colores sólidos, sin degradados entre ellos.
- **Fondos que cambian al deslizar.** Los dos backs (`assets/back-light`, `assets/back-dark`) se funden según el tema de cada sección (`data-theme="light|dark"`).
- **Hero con el logo al centro de una red 3D.** La red de nodos rodea al logotipo, reacciona al cursor y se puede arrastrar. Al bajar, la red se mueve y cambia de forma en cada sección (`data-globe="x y radio dispersión opacidad"`; `data-globe-m` es la versión móvil).
- **Escena Spline.** Tu escena (`my.spline.design/untitled-C5FXGwdlZSOgdLZIONJ8HOCv`) se embebe en «Experiencia 3D» y se carga cuando el visitante se acerca. Hay que hacer clic en «Interactuar» para controlarla, así no atrapa el scroll.
- **Productos integrados.** Los productos de Progalénica viven dentro de la página: cuadrícula con filtros por área y una ficha que se abre en la misma página, con zoom sobre la foto y anterior/siguiente. «Solicitar información» lleva al formulario de contacto con el producto ya escrito.
- **Todo se queda en la página.** Ningún botón ni enlace lleva a otro sitio.
- Adaptable a móvil y compatible con `prefers-reduced-motion`.

## Fotos de producto (alta calidad)

Las fichas usan `assets/productos/<id>.webp` (2000 px) y `<id>-1000.webp` (1000 px). Mientras no existan, cada tarjeta muestra el nombre del producto sobre el fondo de estudio.

1. Junta las fotos originales en una carpeta, nombradas con el id: `rifosar`, `rifosar-pos`, `bilumiv`, `lezomiv`, `fexilev`, `carenev`, `cravicem`, `matinev`, `tamablan-pf`. Lo ideal es PNG con fondo transparente, de 2000 px o más por lado.
2. Ejecuta `python3 tools/optimizar_productos.py <carpeta>`. Requiere Pillow.

Los datos de cada producto (nombre, sustancia, concentración, presentación y área) están en el arreglo `PRODUCTS` de `index.html`.

## Logotipos

Los logos se extrajeron del PDF de backs sin modificarlos:
- `logo-artilugio.svg`: versión vectorial con texto oscuro, para fondos claros.
- `logo-artilugio-dark.webp/.png`: versión con texto blanco, para fondos oscuros.

## Pendientes antes de publicar

1. **Textos originales.** Los textos se tomaron del sitio actual tal como aparecen en los buscadores. Revisa contra el sitio en vivo, sobre todo el párrafo de «Quiénes somos» y el del origen griego del nombre (hay un comentario en la sección `#artilugio` que marca dónde va).
2. **Fotos de producto.** Ver la sección anterior.
3. **Contacto.** Escribe el correo de destino en `data-email` del formulario `#contactForm`. El formulario abre el cliente de correo del visitante. Si prefieres envío directo, conecta el formulario a tu backend o a un servicio de formularios.

## Probar en local

```bash
cd artilugio-web
python3 -m http.server 8080
# abre http://localhost:8080
```
