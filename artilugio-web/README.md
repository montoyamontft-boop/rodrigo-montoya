# Artilugio Group: sitio web interactivo

Rediseño de una sola página para artilugiogroup.com.mx. Es HTML, CSS y JS estáticos, sin build: basta con subir esta carpeta al hosting.

## Qué incluye

- **Fondos que cambian al deslizar.** Los dos backs (`assets/back-light`, `assets/back-dark`) se funden según el tema de cada sección (`data-theme="light|dark"`). Encima, un tinte cambia de tono (azul → cian → naranja → rojo → ámbar) conforme avanza el scroll.
- **Red 3D de nodos.** Un globo de nodos y conexiones con los colores de los backs que reacciona al cursor y se puede arrastrar en el hero. Cambia de posición, tamaño y dispersión en cada sección (`data-globe="x y radio dispersión opacidad"`; `data-globe-m` es la versión móvil).
- **Escena Spline.** Tu escena (`my.spline.design/untitled-C5FXGwdlZSOgdLZIONJ8HOCv`) se embebe en la sección «Experiencia 3D» y se carga cuando el visitante se acerca. Hay que hacer clic en «Interactuar» para controlarla, así no atrapa el scroll. Para cambiar de escena, edita `data-src` en `#xpFrame`.
- Animación del nombre «Artilugio», lectura palabra por palabra en «Quiénes somos», marquesina ligada a la velocidad del scroll, tarjetas con spotlight e inclinación, botones magnéticos, cursor personalizado y carrusel de Progalénica con enlaces a cada producto.
- Adaptable a móvil y compatible con `prefers-reduced-motion`.

## Logotipos

Los logos se extrajeron del PDF de backs sin modificarlos:
- `logo-artilugio.svg`: versión vectorial con texto oscuro, para fondos claros.
- `logo-artilugio-dark.webp/.png`: versión con texto blanco, para fondos oscuros.

## Pendientes antes de publicar

1. **Textos originales.** Los textos se tomaron del sitio actual tal como aparecen en los buscadores. Revisa contra el sitio en vivo, sobre todo:
   - el párrafo de «Quiénes somos»;
   - el párrafo sobre el origen griego del nombre (hay un comentario en la sección `#artilugio` que marca dónde va).
2. **Contacto.** Escribe el correo de destino en `data-email` del formulario `#contactForm`. El formulario abre el cliente de correo del visitante. Si prefieres envío directo, conecta el formulario a tu backend o a un servicio de formularios.
3. **Tienda.** El botón «Ir a la tienda» apunta a `/Progalenica/`. Confirma que esa sea la URL de la tienda.

## Probar en local

```bash
cd artilugio-web
python3 -m http.server 8080
# abre http://localhost:8080
```
