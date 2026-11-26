#!/usr/bin/env python3
"""Genera las páginas propias de Utopia Tickets en branding/public/:

  legal/index.html                  legal/aviso-legal.html        legal/privacidad.html
  legal/cookies.html                legal/condiciones-de-compra.html
  legal/condiciones-promotores.html legal/reventa-y-transferencia.html
  promotores/index.html             promotores/guia.html
  ayuda/index.html

Todas comparten cabecera, pie y `legal/legal.css`. El contenido vive en `contenido.py` (mismo directorio).
Uso:  python3 -I gen_paginas.py            → regenera en ../public
      REPO_PUBLICO=1 python3 -I gen_paginas.py   → añade el enlace «Código fuente» (AGPL §13) en el pie
      BORRADOR=0 python3 -I gen_paginas.py       → quita la banda de borrador y el noindex (versión publicada)
Sin dependencias. Escribe solo dentro de ../public.
"""
import os, sys, html, json, hashlib
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import contenido as C

PUBLIC = HERE.parent / 'public'
BORRADOR = os.environ.get('BORRADOR', '1') != '0'
REPO_PUBLICO = os.environ.get('REPO_PUBLICO', '0') == '1'
REPO_URL = 'https://github.com/utopia-tickets/utopia-tickets-hievents'
ORG_URL = C.ORG_URL

NAV = [
    ('/utopia/ayuda/', 'Ayuda'),
    ('/utopia/promotores/', 'Para promotores'),
    ('/utopia/legal/', 'Legal'),
]
FOOT = [
    ('/utopia/legal/aviso-legal.html', 'Aviso legal'),
    ('/utopia/legal/condiciones-de-compra.html', 'Condiciones de compra'),
    ('/utopia/legal/reventa-y-transferencia.html', 'Reventa'),
    ('/utopia/legal/condiciones-promotores.html', 'Condiciones para promotores'),
    ('/utopia/legal/privacidad.html', 'Privacidad'),
    ('/utopia/legal/cookies.html', 'Cookies'),
    ('/utopia/legal/condiciones-de-compra.html#reclamaciones', 'Hojas de reclamaciones'),
    ('/utopia/ayuda/', 'Ayuda'),
]


def page(path, title, body, desc, current=None, lead=None, meta=True, toc=None, kind='legal'):
    robots = 'noindex, nofollow' if BORRADOR else 'index, follow'
    nav = '\n'.join(
        f'    <a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for h, t in NAV)
    foot = '\n'.join(f'  <a href="{h}">{t}</a>' for h, t in FOOT)
    if REPO_PUBLICO:
        foot += f'\n  <a href="{REPO_URL}">Código fuente (AGPL)</a>'
    else:
        foot += f'\n  <!-- AGPL §13: al hacer público el repo, regenerar con REPO_PUBLICO=1 para enlazar {REPO_URL} -->'
    draft = ('<p class="draft" role="note">BORRADOR para revisión jurídica. No está publicado ni es vinculante.</p>'
             if BORRADOR and kind == 'legal' else
             '<p class="draft draft-soft" role="note">Versión de prueba: aún no está publicada.</p>' if BORRADOR else '')
    tochtml = ''
    if toc:
        tochtml = ('<nav class="toc" aria-label="Índice">\n<ol>\n' +
                   '\n'.join(f'<li><a href="#{a}">{html.escape(t)}</a></li>' for a, t in toc) + '\n</ol>\n</nav>\n')
    metahtml = f'<p class="meta">Última actualización: {C.FECHA}{" (borrador)" if BORRADOR else ""}</p>\n' if meta else ''
    leadhtml = f'<p class="lead">{lead}</p>\n' if lead else ''
    out = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="{robots}">
<title>{html.escape(title)} · Utopia Tickets</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)} · Utopia Tickets">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="/utopia/logo/utopia-tickets-positivo-1200.png">
<link rel="icon" href="/utopia/favicon/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/utopia/legal/legal.css?v={C.VERSION}">
</head>
<body class="{kind}">
<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="top">
  <a class="brand" href="{ORG_URL}" aria-label="Utopia Tickets, ir a los eventos"><img src="/utopia/logo/utopia-tickets-horizontal-negativo.svg" alt="Utopia Tickets" width="176" height="37"></a>
  <nav class="mainnav" aria-label="Principal">
{nav}
  </nav>
</header>
{draft}
<main id="contenido">
<h1>{title}</h1>
{leadhtml}{metahtml}{tochtml}{body}
</main>
<footer>
{foot}
  <span>UTOPIA BOOKING S.L. · NIF B22863963</span>
  <span class="powered">Powered by Utopia Tickets based on <a href="https://hi.events">Hi.Events</a></span>
</footer>
</body>
</html>
'''
    out = out.replace('<div class="tablewrap">', '<div class="tablewrap" tabindex="0" role="region" aria-label="Tabla; desplázala de lado si no cabe">')
    dest = PUBLIC / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding='utf-8')
    return dest


# Documentos que se aceptan al crear una cuenta de promotor. El backend lee legal/versiones.json y guarda
# en utopia_aceptaciones la versión y la huella sha256 de cada uno; la copia exacta queda en legal/versiones/.
ACEPTABLES = {
    'condiciones-promotores': 'legal/condiciones-promotores.html',
    'privacidad': 'legal/privacidad.html',
    'condiciones-de-compra': 'legal/condiciones-de-compra.html',
    'reventa-y-transferencia': 'legal/reventa-y-transferencia.html',
}


def versiones():
    docs = {}
    arch = PUBLIC / 'legal/versiones'
    arch.mkdir(parents=True, exist_ok=True)
    for doc, rel in ACEPTABLES.items():
        f = PUBLIC / rel
        if not f.exists():
            continue
        data = f.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        copia = arch / f'{doc}-{C.VERSION_LEGAL}-{sha[:12]}.html'
        if not copia.exists():
            copia.write_bytes(data)
        docs[doc] = {
            'version': C.VERSION_LEGAL + ('-borrador' if BORRADOR else ''),
            'sha256': sha,
            'url': '/utopia/' + rel,
            'copia': '/utopia/legal/versiones/' + copia.name,
        }
    out = {'generado': C.FECHA, 'documentos': docs}
    (PUBLIC / 'legal/versiones.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    return docs


def main():
    made = []
    for spec in C.PAGINAS:
        made.append(page(**spec))
    for m in made:
        print('escrita', m.relative_to(PUBLIC))
    for doc, v in versiones().items():
        print('versión', doc, v['version'], v['sha256'][:12])


if __name__ == '__main__':
    main()
