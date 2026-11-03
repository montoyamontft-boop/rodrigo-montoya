# Carnes del Norte Selecto · propuesta de sitio (concepto)

Página estática de prueba para las skills de diseño (`design-taste-frontend`). **No es el sitio oficial** del negocio.

* `index.html` — la página final, autocontenida (fuentes incrustadas, sin dependencias). Ábrela directo en el navegador.
* `page.html` + `build.py` — fuente. `python3 build.py` regenera `index.html` (dibuja el toro y sus cortes, incrusta las fuentes).
* `trace_logo.py` → `bull.json` — calca el toro del logo (sus facetas) y lo divide en los cortes de res. Requiere `pip install opencv-python-headless shapely`.
* `assets/logo.png` — logotipo del negocio, sin modificar (recortado de una captura; conviene reemplazarlo por el archivo original en alta resolución).
* `vendor/` — GSAP 3.15.0 + ScrollTrigger, Lenis 1.3.26 (desde npm) y el escenario de escenas de la skill (`stage.js`, `stage.css`); `build.py` los incrusta en `index.html`.
* `fonts/` — Libre Franklin y Source Serif 4 (SIL Open Font License, vía Fontsource).

Datos reales tomados de Google (nov. 2026): calificaciones y número de opiniones de las tres sucursales, horarios de apertura,
horarios populares del lunes (sucursal Ruiz Cortines), la publicación de Instagram y la noche del Dueto Rodríguez (30 oct).
Contenido de muestra por confirmar con el negocio: la lista de cortes y sus descripciones, los nombres de las sucursales
(salvo Ruiz Cortines), los enlaces de Maps (son búsquedas) y la página de Facebook.

## Fotos

Fotos libres de Wikimedia Commons (en `assets/`, créditos en `assets/credits.json` y en el pie de la página).
Muestran el mundo del negocio (carne, carbón, música norteña, Atizapán), **no** el local, sus platillos ni su gente.
La terraza sigue dibujada porque no hay foto libre de ella: lo ideal es reemplazarla con fotos propias del negocio.

* `vitrina.jpg` — Meat at the butcher shop.JPG, Revital Salomon, CC BY-SA 4.0 — https://commons.wikimedia.org/wiki/File:Meat_at_the_butcher_shop.JPG
* `ribeye.jpg` — Smoked rib eye - April 2024 - Sarah Stierch.jpg, Missvain, CC BY 4.0 — https://commons.wikimedia.org/wiki/File:Smoked_rib_eye_-_April_2024_-_Sarah_Stierch.jpg
* `parrilla.jpg` — Charcoal grill.jpg, T.Tseng, CC BY 2.0 — https://commons.wikimedia.org/wiki/File:Charcoal_grill.jpg
* `brasa.jpg` — Small piece of meat (5650576076).jpg, Håkan Dahlström from Malmö, Sweden, CC BY 2.0 — https://commons.wikimedia.org/wiki/File:Small_piece_of_meat_(5650576076).jpg
* `bugambilia.jpg` — Bougainvillea 20.jpg, পাপৰি বৰা, CC BY-SA 4.0 — https://commons.wikimedia.org/wiki/File:Bougainvillea_20.jpg
* `norteno.jpg` — Música Norteña Pilo's Bar.jpg, WendyAvilesR, CC BY-SA 4.0 — https://commons.wikimedia.org/wiki/File:M%C3%BAsica_Norte%C3%B1a_Pilo%27s_Bar.jpg
* `bajosexto-pared.jpg` — Bajo sexto ? - I can't read the tagger! 12 String Something - Homestead Pickin' Parlor (2007-08-10 05.51.16 by kc7fys).jpg, kc7fys from Saint Paul, USA, CC BY-SA 2.0 — https://commons.wikimedia.org/wiki/File:Bajo_sexto_%3F_-_I_can%27t_read_the_tagger!_12_String_Something_-_Homestead_Pickin%27_Parlor_(2007-08-10_05.51.16_by_kc7fys).jpg
* `atizapan.jpg` — Calzada San Mateo, Atizapán de Zaragoza, Estado de México.jpg, ProtoplasmaKid, CC BY-SA 4.0 — https://commons.wikimedia.org/wiki/File:Calzada_San_Mateo,_Atizap%C3%A1n_de_Zaragoza,_Estado_de_M%C3%A9xico.jpg

## Interacción

* Portada: el toro se inclina hacia el cursor; cada corte se ilumina, dice su nombre y lleva a la vitrina.
* Escena «Cada corte, en su lugar»: al hacer scroll el toro se desarma en sus cortes, con nombre y enlace.
* Vitrina: «Agregar al asador» conecta cada corte con la calculadora (y el toro de la calculadora también se puede tocar).
* «¿Cómo lo quieres?»: selector de término y grosor con temperatura interna y minutos por lado (valores orientativos).
* Escena «Al carbón»: la foto de la parrilla se abre de una ventana a toda la pantalla.
* Calificaciones que cuentan, gráfica de horas legible al pasar o enfocar, botones magnéticos y scroll suave.
* Con «reducir movimiento» o sin JavaScript todo se muestra en su composición final.
