# Karnes del Norte Prime · propuesta de sitio (concepto)

Página estática de prueba, con personalidad propia frente a Carnes del Norte Selecto (`../site`). **No es el sitio oficial.**

* `index.html` — la página final, autocontenida (fuentes, three.js y datos incrustados). Las fotos viven en `assets/`.
* `page.html` + `build.py` — fuente. `python3 build.py` regenera `index.html`.
* `src/bull3d.js` — el toro del logo como escultura 3D facetada (three.js 0.169). `npm install && npm run bundle` genera `vendor/bull3d.js`.
* `bull.json` — las facetas del toro, calcadas del logo con `../site/trace_logo.py`.
* `fonts/` — Newsreader (SIL Open Font License, vía Fontsource).

Dirección de diseño (skill design-taste-frontend): «The dark room», seed 1358615903. Un solo fondo carbón; el toro y las fotos
aparecen como piezas iluminadas. Acento latón (el sorteo daba salvia; se cambió porque choca con la carne).

## Interacción

* Portada: el toro 3D gira hacia el cursor; cada corte se adelanta, se ilumina y dice su nombre; al tocarlo lleva a su explicación.
* «Un toro, corte por corte»: escena fija; al hacer scroll el toro gira y enciende cada corte con cómo cocinarlo.
* «Todos los cortes»: tabla a un solo tamaño de letra; el botón + agrega cada corte para asar a la báscula.
* «La báscula»: calcula kilos, tortillas, cebollitas y carbón; copia la lista y abre el chat de Instagram.
* Sin WebGL, sin JavaScript o con «reducir movimiento»: se ve el toro plano y todo el contenido completo.

## Pendiente de confirmar con el negocio

* Dirección, horario y teléfono de la sucursal (la tarjeta dice que se pidan por Instagram).
* Lista de cortes, tiempos de cocción (orientativos) y si manejan tomahawk.
* Las fotos son libres de Wikimedia Commons (créditos en el pie y en `assets/credits.json`); no son del local.
