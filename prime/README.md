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

## Datos del negocio (de su perfil de Instagram @karnesprime)

* «Carnicería boutique con cortes premium y productos de alta calidad». Res, pollo, cerdo y mariscos.
* Calzada de los Jinetes 79B · 8:00 a 19:00 h · tel. 55 8926 0375.
* Frases suyas usadas en la página: «Única sucursal, única calidad, única Karne Prime» y «¿No sabes qué corte pedir? Nosotros te ayudamos».
* Logo, rib eye y fachada recortados de sus publicaciones (`assets/logo-prime*.png`, `ribeye-prime.jpg`, `fachada.jpg`), en baja resolución:
  conviene pedir los originales.

## Pendiente de confirmar con el negocio

* Días de apertura (el perfil solo dice 8:00 a 19:00 h), lista de cortes, tiempos de cocción (orientativos) y si manejan tomahawk.
* El resto de las fotos son libres de Wikimedia Commons (créditos en el pie y en `assets/credits.json`); no son del local.
