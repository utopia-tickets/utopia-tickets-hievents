# Utopia Tickets · capa de marca sobre Hi.Events

**Utopia Tickets** es la tiquetera de Utopia Booking. Usa **[Hi.Events](https://hi.events)** (AGPL-3.0) **sin fork**: la imagen oficial no se toca, y en cada arranque se le superponen el logotipo, los colores, la tipografía Chivo, los textos en español, las plantillas de correo y de entrada, el alta de promotores con aceptación de las condiciones, y las páginas legales, de ayuda y para promotores.

Este repositorio tiene **todo lo que se modifica de Hi.Events**, es decir, el «código fuente correspondiente» que la AGPL §13 obliga a ofrecer a quien use la tiquetera, además de una receta de instalación sin secretos.

## Base

| | |
|---|---|
| Imagen | `daveearley/hi.events-all-in-one:v2.2.0` |
| Digest | `sha256:435728539250541d69f4161804056aeb52e5b9d99ecd44960f7a1a2fb44e3b74` |
| Código de Hi.Events | https://github.com/HiEventsDev/hi.events (etiqueta `v2.2.0`) |

## Contenido

| Carpeta | Qué es |
|---|---|
| `branding/` | La capa de marca. `patch.mjs` se ejecuta en cada arranque desde `/etc/entrypoint.d/` y siempre parte de las copias originales de la imagen. Hace 10 pasos idempotentes: `index.html`, iconos, catálogo `es` del frontend, `lang/es.json`, tema de correo, plantillas Blade y PHP (con guarda `sha256`), `APP_LOCALE`, textos fijos del JavaScript, versiones contra la caché y cabeceras de nginx. `public/` se sirve en `/utopia/…` (CSS, Chivo, logotipos, favicon, logo del correo, legales, ayuda y promotores). Detalle y mantenimiento en `branding/README.md` |
| `branding/overrides/` | Ficheros de Hi.Events modificados: fechas e importes en español, el pie de los correos, el contacto del evento en los correos al comprador, el alta de promotores con aceptación de las condiciones y una migración propia (`utopia_aceptaciones`). Solo se aplican si el original coincide con el `sha256` de `manifest.json` |
| `branding/i18n/` | Traducciones corregidas del frontend (por `msgid`) y del backend (`es.json`) |
| `branding/paginas/` | Generador de las páginas legales, de ayuda y para promotores de `branding/public/` |
| `logo/` | Logotipo «Utopia Tickets» apilado (principal) y en línea, en positivo, negativo y monocromo (SVG y PNG), favicon, logo del correo, hoja de medidas y **regla de uso** (`logo/REGLA-DE-USO.md`) |
| `receta/` | `docker-compose.yml` con los tres montajes de la marca, `env.template` (solo marcadores, **ninguna clave**) y `setup.sh`, que genera los secretos y arranca |

## Cómo se instala

1. En una carpeta del servidor pon `receta/docker-compose.yml`, `receta/env.template`, `receta/setup.sh` y la carpeta `branding/`.
2. En `env.template`, cambia `tickets.example.com` por tu dominio público y revisa el correo, Stripe y `UTOPIA_AVISO_ALTAS`.
3. Ejecuta `sh setup.sh`: crea `.env` con secretos nuevos y arranca con `docker compose up -d`. La app escucha en `127.0.0.1:8080`; delante va tu proxy TLS o tu túnel.
4. Comprueba `docker compose logs all-in-one | grep utopia-branding`. Tiene que acabar en `fin: 10 OK, 0 con aviso`.
5. Al actualizar la imagen, sigue `branding/README.md`, «Al actualizar la imagen de Hi.Events».

El compose monta:
- `./branding:/branding:ro`
- `./branding/99-utopia-branding.sh:/etc/entrypoint.d/99-utopia-branding.sh:ro`
- `./branding/public:/app/frontend/dist/client/utopia:ro`

Las variables de la marca son `APP_LOCALE`, `VITE_APP_LOGO_LIGHT/DARK`, `VITE_APP_FAVICON`, `VITE_APP_PRIMARY_COLOR`, `VITE_APP_SECONDARY_COLOR`, `VITE_TOS_URL`, `VITE_PRIVACY_URL`, `VITE_DEFAULT_IMAGE_URL`, `APP_EMAIL_LOGO_URL`, `UTOPIA_AVISO_ALTAS` y `UTOPIA_LEGAL_VERSIONES`.

## Logotipo: regla de uso (resumen)

- **Apilado («utopia» y debajo «TICKETS») = principal**: página del evento, entrada, correos, portadas, carteles y redes. Copia las proporciones del original de Utopia Booking: mayúscula al 0,5015 de la altura x, interlineado de base a base al 0,8237 de la altura x y centrado óptico de −7,4 u.
- **En línea**: solo en la cabecera estrecha de la app, el panel del organizador y la barra del móvil.
- Un solo nombre, «Utopia Tickets». Positivo sobre claro y negativo sobre oscuro. La estrella siempre va en #68C3B7.

## Aviso de Hi.Events

El aviso exigido por Hi.Events (AGPL §7(b)) sigue visible y legible en la web, la entrada y los correos: **«Powered by Utopia Tickets based on Hi.Events»**, con el enlace a https://hi.events. Esta es la fórmula que permite el propio aviso del código para versiones modificadas. Quitarlo requiere licencia comercial (https://hi.events/licensing).

## Avisos

- Los legales de `branding/public/legal/` son los publicados (versión de `legal/versiones.json`). Se editan en `branding/paginas/contenido.py` y se regeneran con `gen_paginas.py`; no se borra nunca una copia de `legal/versiones/` que alguien haya aceptado.
- Ni secretos ni datos de compradores: las claves van en el `.env` del servidor, que no está en este repositorio.

## Modificaciones (AGPL §5)

Este repositorio es una **versión modificada de Hi.Events** (`v2.2.0`). Las modificaciones son de **UTOPIA BOOKING S.L.**, desde noviembre de 2026, y se publican con la misma licencia AGPL-3.0. Cada fichero de Hi.Events cambiado está en `branding/overrides/` con un comentario «Utopia Tickets (nov-2026)» que explica qué cambia, y el historial de git da la fecha de cada cambio. Los ficheros nuevos (`branding/`, `receta/`, `logo/`) son obra de Utopia Booking.

La rama `main` es el código que usa la tiquetera de `tickets.utopiabooking.com`. Puede ir algo por delante de lo desplegado mientras se prueba un cambio.

## Licencia

AGPL-3.0, la misma que Hi.Events (`LICENSE`). Hi.Events es © Hi.Events Ltd. Las modificaciones son © 2026 UTOPIA BOOKING S.L. La tipografía Chivo va con su licencia OFL (`branding/public/fonts/OFL-Chivo.txt`).
