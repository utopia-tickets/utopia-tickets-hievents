# branding/ · capa de marca de Utopia Tickets sobre Hi.Events (sin fork)

Va junto al `docker-compose.yml` del servidor. El compose monta:

| Montaje | Para qué |
|---|---|
| `./branding:/branding:ro` | Todo el material (solo lectura). |
| `./branding/99-utopia-branding.sh:/etc/entrypoint.d/99-utopia-branding.sh:ro` | El entrypoint de la imagen (serversideup) ejecuta los `*.sh` de `/etc/entrypoint.d/` antes de `/startup.sh`. Llama a `patch.mjs`. Si falla, la app arranca igual con su aspecto original y deja el aviso en el log. |
| `./branding/public:/app/frontend/dist/client/utopia:ro` | Lo sirve el servidor del frontend (sirv) en `/utopia/…`: `utopia.css`, Chivo, logos, favicon, legales, logo de correo, portada genérica. |

## Qué hace `patch.mjs` en cada arranque (idempotente: siempre parte de la copia `*.utopia-orig` de la imagen)

1. `index.html`: `lang="es"`, quita Google/Bunny Fonts (`fonts.bunny.net`), pone los iconos y el manifest de Utopia, precarga Chivo y añade `/utopia/utopia.css`.
2. Iconos en las rutas fijas de la imagen (`/favicon.ico`, `/manifest-icons/*`, `/site.webmanifest`).
3. Catálogo `es` del frontend (lingui compilado, `dist/{client,server}/assets/es-*.js`): cambia los textos de `i18n/frontend-es.json`. La clave de cada texto es `base64(sha256(msgid + U+001F + contexto))[:6]`. Avisa si un `msgid` ya no existe.
4. `backend/lang/es.json`: fusiona `i18n/backend-es.json` (textos de los correos de tú y en español natural, y las claves que faltaban).
5. Tema de correo: añade `mail/utopia-mail.css` al final de `vendor/mail/html/themes/default.css`.
6. Ficheros PHP y plantillas Blade de `overrides/`: fechas e importes en español, el pie de los correos, el contacto del evento en los correos al comprador, el alta de promotores con aceptación de las condiciones (`CreateAccountRequest.php`, `CreateAccountAction.php`, `UpdateEventStatusHandler.php`), `app/Helper/Currency.php` (los importes siguen `APP_LOCALE`: «59,50 €» en vez de «€59.50») y `app/Validators/Rules/BaseQuestionRule.php` (el aviso de campo obligatorio pasa por la traducción). Cada uno solo se sustituye si el original coincide con el `sha256` de `overrides/manifest.json`; si la imagen cambió, se deja el de la imagen y se avisa. Los ficheros marcados como `nuevo` (la migración `utopia_aceptaciones`) se escriben si no existen o si ya son de la marca; nunca se pisa un fichero de la imagen con el mismo nombre.
7. `config/app.php`: `'locale' => 'en'` pasa a `env('APP_LOCALE', 'en')`; con `APP_LOCALE=es` los correos sin idioma propio (el aviso al organizador) salen en español.
8. Textos fijos del JavaScript compilado que no pasan por el catálogo (`overrides/js-textos.json`): la entrada de ejemplo de la pantalla de acceso, el título por defecto del organizador, el texto emergente del enlace a Hi.Events, el `aria-label` del ojo de la contraseña, el correo de ejemplo de los formularios, la casilla de aceptación del registro y el pie legal (aviso legal, condiciones, privacidad, cookies, hojas de reclamaciones y ayuda) de la página del organizador y del evento, del pago y del acceso y el alta; sus estilos van en `public/utopia.css`. Por fichero: solo si el original coincide con su `sha256` y cada texto aparece las veces exactas; si no, se deja el de la imagen y se avisa. Ojo: quitar un grupo de `js-textos.json` no deshace sus ficheros (`patch.mjs` no toca los que salen de la lista y `docker restart` conserva la capa del contenedor). Para volver atrás, restaura cada `.js` desde su `*.utopia-orig` o recrea el contenedor.
9. Versiones contra la caché: el servidor no manda `Cache-Control` y los `.js` cambiados conservan su nombre. A cada `.js` del cliente con copia `*.utopia-orig` se le añade `?v=<huella>`: en el `<script>` de entrada de `index.html` y con un `<script type="importmap">` para los que se importan desde otros módulos.
10. nginx: `/etc/nginx/nginx.conf` de la imagen, solo si coincide con su `sha256`. Añade `server_tokens off`, incluye `nginx/cabeceras.conf` (`X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`) y `nginx/ubicaciones.conf` (`/assets/` con `Cache-Control: immutable` de un año, `/utopia/` con una hora y los índices de carpeta, y el panel `/manage`, `/admin`, `/auth`… con `X-Frame-Options: DENY` y `no-store`), y quita `X-Powered-By: Express`. HSTS lo pone el proxy TLS que tengas delante.
    - `nginx/estaticas.conf` (desde `ubicaciones.conf`): las páginas propias (`/utopia/*`, `security.txt`, `robots.txt`) con una CSP estricta (`nonce` por petición) y `X-Frame-Options: DENY`. Lo que no existe bajo `/utopia/` sale con `public/404.html` (estado 404 y `noindex`).
    - `ubicaciones.conf` además: «/» (la raíz exacta) sirve la portada `public/inicio/` con `DENY` y `frame-ancestors 'none'`; `/robots.txt` se reescribe a `/utopia/robots.txt` (los dos sitemaps); `/.well-known/security.txt` sale de `public/security.txt` (renuévalo antes de su `Expires`: `test/seguridad.test.mjs` falla 30 días antes); y `noindex` en `legal/versiones/`. La página del evento, el pago y el widget no llevan `DENY`: el widget se enmarca en otras webs a propósito.
    - `nginx/idioma.conf` (opcional): un `map` de nivel `http` para que el HTML del servidor salga en español cuando la petición no trae `Accept-Language` (los rastreadores), y en el idioma pedido cuando lo trae. Si existe, se incluye en `http {}` y `location /` pasa `Accept-Language $utopia_accept_language`. Antes se valida con `nginx -t`; si falla, se deja el `nginx.conf` de siempre y se avisa. Sin el fichero, el `nginx.conf` sale igual que sin él.

    Comprueba la capa con `node --test test/seguridad.test.mjs` (desde `branding/`).

## Páginas propias (`paginas/`)
`paginas/contenido.py` + `paginas/gen_paginas.py` generan en `public/`: `legal/` (índice, aviso legal, condiciones de compra, condiciones para promotores con el anexo del art. 28 RGPD, privacidad, cookies, reventa y transferencia), `promotores/` (tarifa y guía paso a paso) y `ayuda/`. Se editan en `contenido.py` y se regeneran con `python3 -I paginas/gen_paginas.py`; `BORRADOR=0` quita la banda de borrador y el `noindex`, y `REPO_PUBLICO=1` añade al pie el enlace «Código fuente (AGPL)». Escribe también `404.html`, `sitemap.xml` y `robots.txt`, y cada página lleva su canónica absoluta (`SITIO`, por defecto `https://tickets.utopiabooking.com`).

Los documentos que se aceptan al darse de alta como promotor tienen versión y huella en `public/legal/versiones.json`, y la copia exacta de cada versión en `public/legal/versiones/`. No se borra nunca una copia que alguien haya aceptado.

Variables del `.env` que usa la marca: `APP_LOCALE`, `VITE_APP_LOGO_LIGHT/DARK`, `VITE_APP_FAVICON`, `VITE_APP_PRIMARY_COLOR`, `VITE_APP_SECONDARY_COLOR`, `VITE_TOS_URL`, `VITE_PRIVACY_URL`, `VITE_DEFAULT_IMAGE_URL`, `APP_EMAIL_LOGO_URL`, `UTOPIA_AVISO_ALTAS` y `UTOPIA_LEGAL_VERSIONES` (ver `receta/env.template`).

## Al actualizar la imagen de Hi.Events

1. Cambia el digest en el compose y `docker compose up -d all-in-one`.
2. `docker compose logs all-in-one | grep utopia-branding`: tiene que acabar en `fin: 10 OK, 0 con aviso`.
3. Si hay avisos:
   - `msgid que ya no existen`: el texto cambió en inglés; busca el nuevo en `frontend/src/locales/es.po` de la imagen y actualiza `i18n/frontend-es.json`.
   - `el original cambió`: rehaz la plantilla de `overrides/` sobre la nueva (los cambios son pocas líneas marcadas con `$utopiaEs` o con un comentario «Utopia Tickets») y pon el `sha256` nuevo en `manifest.json`.
   - `config/app.php`: comprueba que la línea `'locale' => 'en',` sigue igual.
   - `index.html`: si cambió la cabecera, ajusta las expresiones del paso 1 (y el `<script type="module">` de entrada que busca el paso 9).
   - `textos fijos del JS`: los nombres de los `.js` llevan huella y cambian con cada versión. Busca el texto en inglés en `frontend/dist` (y en `node_modules/@mantine/core` para el `aria-label` de la contraseña), y pon en `overrides/js-textos.json` la ruta, el `sha256` del original y las veces que aparece cada texto.
4. Revisa a ojo la página del evento, la entrada, el check-in y un correo (Mailpit), y pasa un control de accesibilidad (axe).
5. Los selectores de `utopia.css` usan clases estables (`hi-*`, `mantine-*`) y prefijos de módulos CSS (`[class*="_title_"]`). Una versión nueva puede cambiarlos: revísalo con capturas.

## Reglas fijas
- El aviso de Hi.Events se queda visible y legible (AGPL §7(b)). Dice **«Powered by Utopia Tickets based on Hi.Events»**, que es la fórmula que permite el propio aviso del código cuando se modifica Hi.Events. En la web se cambia con el texto `Powered by` de `i18n/frontend-es.json` y en los correos con `overrides/message.blade.php`. El enlace sigue yendo a `https://hi.events` con el mismo tamaño y contraste. Nada de aquí lo oculta, lo encoge ni le baja el contraste. No se usa `APP_EMAIL_FOOTER_TEXT`.
- Logotipo: el apilado es el principal y el de en línea solo va en la cabecera, el panel y la barra del móvil. Detalle en `logo/REGLA-DE-USO.md`.
- Esta carpeta es una modificación de un programa AGPL: su código se ofrece a los usuarios igual que el de Hi.Events (AGPL §13).
- Después de cambiar ficheros de `public/`, reinicia el contenedor: sirv lee la lista de ficheros al arrancar.
- Ejemplos en la marca (entrada de la pantalla de acceso, nombres y correos de los formularios): siempre en español e inventados, nunca un evento real.
