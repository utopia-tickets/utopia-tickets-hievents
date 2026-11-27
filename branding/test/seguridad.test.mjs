// Seguridad y SEO de la capa de marca de Utopia Tickets.
// - security.txt (RFC 9116): solo campos del RFC, Contact no personal y que ya sale en el aviso legal, Expires único y
//   vigente (falla 30 días antes de caducar y si pasa de un año), Canonical, texto UTF-8 y fuera de los sitemaps.
// - robots.txt declara los dos sitemaps; cada página propia lleva su canónica absoluta y el sitemap propio lista justo las
//   indexables; la 404 es noindex, sin canónica y fuera del sitemap.
// - nginx: sin X-XSS-Protection; «/» con DENY y frame-ancestors 'none'; /utopia/ con la CSP estricta; la página del
//   evento, el pago y el widget siguen fuera de las rutas con DENY (el widget los enmarca a propósito).
// Ejecutar desde branding/: node --test test/seguridad.test.mjs   (o BRANDING=<dir> node --test <ruta>/seguridad.test.mjs)
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { isUtf8 } from 'node:buffer';
import { join, dirname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const B = process.env.BRANDING || join(dirname(fileURLToPath(import.meta.url)), '..');
const PUB = join(B, 'public');
const SITIO = 'https://tickets.utopiabooking.com';
const DIA = 24 * 60 * 60 * 1000;   // un día en ms
const leer = (p) => readFileSync(join(B, p), 'utf8');

const secBytes = readFileSync(join(PUB, 'security.txt'));
const secTxt = secBytes.toString('utf8');
const campos = secTxt.split(/\r?\n/).filter((l) => l.trim() && !l.startsWith('#')).map((l) => {
  const i = l.indexOf(':');
  return [l.slice(0, i).trim().toLowerCase(), l.slice(i + 1).trim()];
});
const valores = (k) => campos.filter(([n]) => n === k).map(([, v]) => v);

function htmls(dir) {
  const out = [];
  for (const n of readdirSync(dir)) {
    const p = join(dir, n);
    if (statSync(p).isDirectory()) { if (n !== 'versiones') out.push(...htmls(p)); }
    else if (n.endsWith('.html')) out.push(p);
  }
  return out;
}
const PAGINAS = ['legal', 'ayuda', 'promotores'].flatMap((d) => htmls(join(PUB, d)));
const urlDe = (f) => `${SITIO}/utopia/${relative(PUB, f).replace(/index\.html$/, '')}`;
const meta = (html, re) => (html.match(re) || [])[1];

test('security.txt: campos de RFC 9116, contacto de Utopia publicado en el aviso legal y Expires vigente', () => {
  const conocidos = new Set(['contact', 'expires', 'encryption', 'acknowledgments', 'preferred-languages', 'canonical', 'policy', 'hiring', 'csaf']);
  for (const [n] of campos) assert.ok(conocidos.has(n), `campo desconocido en security.txt: ${n}`);
  const contactos = valores('contact');
  assert.ok(contactos.length >= 1, 'falta Contact');
  const aviso = readFileSync(join(PUB, 'legal/aviso-legal.html'), 'utf8');
  for (const c of contactos) {
    assert.match(c, /^(mailto:[^@\s]+@utopiabooking\.com|https:\/\/tickets\.utopiabooking\.com\/\S*)$/, `Contact inválido o fuera del dominio: ${c}`);
    // Contact de un buzón de rol, nunca el de una persona.
    if (c.startsWith('mailto:')) assert.match(c, /^mailto:(tickets|soporte|seguridad|security|hola|info|contacto)@/, `Contact personal: ${c}`);
    if (c.startsWith('mailto:')) assert.ok(aviso.includes(c.slice(7)), `${c} no sale en el aviso legal`);
  }
  const exp = valores('expires');
  assert.equal(exp.length, 1, 'Expires tiene que aparecer exactamente una vez');
  assert.match(exp[0], /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$/, 'Expires en formato RFC 3339');
  const t = Date.parse(exp[0]);
  assert.ok(t - Date.now() > 30 * DIA, `security.txt caduca el ${exp[0]}: renovar Expires en public/security.txt (≤ 1 año)`);
  assert.ok(t - Date.now() <= 366 * DIA, 'Expires a más de un año: el RFC recomienda menos');
  assert.deepEqual(valores('canonical'), [`${SITIO}/.well-known/security.txt`]);
  const langs = valores('preferred-languages');
  assert.ok(langs.length <= 1, 'Preferred-Languages, como mucho una vez');
  assert.ok(secTxt.endsWith('\n'), 'acaba en salto de línea');
  assert.ok(isUtf8(secBytes), 'security.txt tiene que ser UTF-8 válido');
});

test('robots.txt declara los dos sitemaps con URL absoluta y no bloquea nada', () => {
  const r = readFileSync(join(PUB, 'robots.txt'), 'utf8');
  const maps = [...r.matchAll(/^Sitemap:\s*(\S+)$/gm)].map((m) => m[1]);
  assert.deepEqual(maps.sort(), [`${SITIO}/sitemap.xml`, `${SITIO}/utopia/sitemap.xml`].sort());
  assert.match(r, /^User-agent: \*$/m);
  assert.doesNotMatch(r, /^Disallow:\s*\/\s*$/m, 'robots.txt no puede bloquear todo el sitio');
});

test('páginas propias: canónica absoluta propia, y el sitemap lista justo las indexables', () => {
  assert.ok(PAGINAS.length >= 10, `pocas páginas propias: ${PAGINAS.length}`);
  const xml = readFileSync(join(PUB, 'sitemap.xml'), 'utf8');
  const locs = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
  assert.equal(new Set(locs).size, locs.length, 'URL repetidas en el sitemap');
  const indexables = [];
  for (const f of PAGINAS) {
    const h = readFileSync(f, 'utf8');
    const canon = meta(h, /<link rel="canonical" href="([^"]+)">/);
    assert.equal(canon, urlDe(f), `canónica de ${relative(PUB, f)}`);
    assert.equal(meta(h, /<meta property="og:url" content="([^"]+)">/), canon, `og:url de ${relative(PUB, f)}`);
    assert.match(meta(h, /<meta property="og:image" content="([^"]+)">/) || '', /^https:\/\//, `og:image absoluta en ${relative(PUB, f)}`);
    if ((meta(h, /<meta name="robots" content="([^"]+)">/) || '').startsWith('index')) indexables.push(canon);
  }
  assert.deepEqual([...locs].sort(), indexables.sort(), 'el sitemap tiene que listar justo las páginas indexables');
  for (const s of ['sitemap.xml', 'robots.txt']) assert.doesNotMatch(readFileSync(join(PUB, s), 'utf8'), /security\.txt|404\.html|\/versiones\//, `${s} no lista security.txt, la 404 ni las copias`);
});

test('404 de la marca: en español, noindex, sin canónica', () => {
  const h = readFileSync(join(PUB, '404.html'), 'utf8');
  assert.match(h, /<html lang="es">/);
  assert.match(h, /<meta name="robots" content="noindex">/);
  assert.doesNotMatch(h, /rel="canonical"/);
  assert.match(h, /<title>Página no encontrada · Utopia Tickets<\/title>/);
  assert.match(h, /Powered by Utopia Tickets based on <a href="https:\/\/hi\.events">Hi\.Events<\/a>/, 'el aviso de Hi.Events sigue visible (AGPL §7(b))');
});

test('nginx: sin X-XSS-Protection, «/» con DENY y frame-ancestors, /utopia/ con CSP estricta y el widget enmarcable', () => {
  const cab = leer('nginx/cabeceras.conf');
  assert.doesNotMatch(cab.replace(/^#.*$/gm, ''), /X-XSS-Protection/i, 'X-XSS-Protection está obsoleta');
  assert.doesNotMatch(cab, /Strict-Transport-Security/i, 'HSTS lo pone el proxy público, no la marca');
  const est = leer('nginx/estaticas.conf');
  const csp = meta(est, /add_header Content-Security-Policy "([^"]+)" always;/) || '';
  for (const d of ["default-src 'self'", "frame-ancestors 'none'", "base-uri 'self'", "form-action 'self'", "object-src 'none'"]) assert.ok(csp.includes(d), `falta ${d} en la CSP de /utopia/`);
  assert.doesNotMatch(csp, /unsafe-inline|unsafe-eval|\*/, 'CSP de /utopia/ sin comodines ni unsafe-*');
  const ubi = leer('nginx/ubicaciones.conf');
  const bloque = (re) => { const m = ubi.match(re); assert.ok(m, `falta el bloque ${re}`); return m[0]; };
  const raiz = bloque(/location = \/ \{[\s\S]*?\n\}/);
  assert.match(raiz, /add_header X-Frame-Options "DENY" always;/);
  assert.match(raiz, /add_header Content-Security-Policy "frame-ancestors 'none'" always;/);
  assert.match(bloque(/location \^~ \/utopia\/ \{[\s\S]*?\n\}/), /include \/branding\/nginx\/estaticas\.conf;/);
  assert.match(bloque(/location = \/\.well-known\/security\.txt \{[\s\S]*?\n\}/), /rewrite \^ \/utopia\/security\.txt break;/);
  assert.match(ubi, /^rewrite \^\/robots\\\.txt\$ \/utopia\/robots\.txt last;$/m);
  const panel = new RegExp(meta(ubi, /location ~ (\^\/\([^)]*\)\(\/\|\$\)) \{/));
  for (const p of ['/events/1/utopia', '/event/1/x', '/checkout/1/abc/details', '/widget/1']) assert.ok(!panel.test(p), `${p} tiene que poder enmarcarse (widget)`);
  for (const p of ['/manage/events', '/auth/login']) assert.ok(panel.test(p), `${p} tiene que llevar DENY`);
  assert.ok(existsSync(join(PUB, '404.html')), 'falta public/404.html');
});
