// Marca de Utopia sobre Hi.Events sin fork.
// Se ejecuta DENTRO del contenedor all-in-one en cada arranque (desde /etc/entrypoint.d/99-utopia-branding.sh),
// antes de /startup.sh. Cada fichero que toca se restaura primero desde su copia prístina (*.utopia-orig), así que
// es idempotente. Si algo no encaja (otra versión de la imagen), avisa y sigue: nunca impide que arranque la app.
// Uso local de prueba: node patch.mjs --root <copia de /app> --branding <dir branding>
//   --nginx <copia del nginx.conf de la imagen> y --solo '<nombre del paso>' (solo para pruebas).
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';

const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const ROOT = arg('--root', '/app');
const B = arg('--branding', '/branding');
const NGINX = arg('--nginx', '/etc/nginx/nginx.conf');
const SOLO = arg('--solo', null);
const FE = path.join(ROOT, 'frontend/dist');
const BE = path.join(ROOT, 'backend');
const log = (...a) => console.log('[utopia-branding]', ...a);
const warn = (...a) => console.log('[utopia-branding] AVISO:', ...a);
const results = [];

function pristine(file) {
  // Devuelve el contenido original de la imagen (guardando una copia la primera vez).
  const o = file + '.utopia-orig';
  if (!fs.existsSync(o)) fs.copyFileSync(file, o);
  return fs.readFileSync(o, 'utf-8');
}
function step(name, fn) {
  if (SOLO && name !== SOLO) return;
  try { const r = fn(); results.push([name, 'OK', r || '']); log(name, 'OK', r || ''); }
  catch (e) { results.push([name, 'FALLO', String(e.message || e)]); warn(name, String(e.message || e)); }
}

// 1) index.html: sin fuentes de terceros, favicon/manifest/colores propios, CSS de Utopia, lang="es".
step('index.html', () => {
  const f = path.join(FE, 'client/index.html');
  let h = pristine(f);
  const before = h;
  h = h.replace('<html lang="en">', '<html lang="es">');
  h = h.replace(/\s*<link\s+rel="stylesheet"\s+href="https:\/\/fonts\.bunny\.net[^"]*"\s*\/?>/, '');
  h = h.replace(/\s*<!-- Favicon -->[\s\S]*?<meta name="msapplication-TileColor"[^>]*>/, '\n' + fs.readFileSync(path.join(B, 'head-icons.html'), 'utf-8').trim());
  const css = fs.readFileSync(path.join(B, 'public/utopia.css'));
  const v = crypto.createHash('sha1').update(css).digest('hex').slice(0, 10);
  const inject = `    <link rel="preload" href="/utopia/fonts/chivo-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>\n    <link rel="stylesheet" href="/utopia/utopia.css?v=${v}">\n  </head>`;
  h = h.replace(/\s*<\/head>/, '\n' + inject);
  if (h.includes('fonts.bunny.net')) throw new Error('queda fonts.bunny.net en index.html');
  if (!h.includes('/utopia/utopia.css')) throw new Error('no se pudo inyectar utopia.css');
  if (!h.includes('/utopia/favicon/')) throw new Error('no se cambiaron los iconos (¿cambió la cabecera de index.html?)');
  fs.writeFileSync(f, h);
  return `${before.length}→${h.length} bytes, css v=${v}`;
});

// 2) Iconos y manifest en las rutas fijas que usa la imagen (/favicon.ico, /site.webmanifest, /manifest-icons/*).
step('iconos y manifest', () => {
  const pairs = [
    ['public/favicon/favicon.ico', 'client/favicon.ico'],
    ['public/favicon/favicon.ico', 'client/manifest-icons/favicon.ico'],
    ['public/favicon/favicon.svg', 'client/manifest-icons/favicon.svg'],
    ['public/favicon/favicon-32.png', 'client/manifest-icons/favicon-32x32.png'],
    ['public/favicon/favicon-48.png', 'client/manifest-icons/favicon-48x48.png'],
    ['public/favicon/favicon-192.png', 'client/manifest-icons/favicon-192x192.png'],
    ['public/favicon/favicon-512.png', 'client/manifest-icons/favicon-512x512.png'],
    ['public/favicon/apple-touch-icon-180.png', 'client/manifest-icons/apple-touch-icon.png'],
    ['site.webmanifest', 'client/site.webmanifest'],
  ];
  let n = 0;
  for (const [src, dst] of pairs) {
    const s = path.join(B, src), d = path.join(FE, dst);
    if (!fs.existsSync(s)) { warn('falta', src); continue; }
    if (fs.existsSync(d)) pristine(d);
    fs.copyFileSync(s, d); n++;
  }
  return `${n}/${pairs.length} ficheros`;
});

// 3) Catálogo es del frontend (lingui compilado). Clave = sha256(msgid + U+001F + contexto) en base64, 6 caracteres.
const linguiId = (msg, ctx = '') => crypto.createHash('sha256').update(msg + '\u001F' + ctx).digest('base64').slice(0, 6);
step('catálogo es (frontend)', () => {
  const over = JSON.parse(fs.readFileSync(path.join(B, 'i18n/frontend-es.json'), 'utf-8'));
  const files = [];
  for (const dir of ['client/assets', 'server/assets']) {
    const d = path.join(FE, dir);
    if (!fs.existsSync(d)) continue;
    for (const n of fs.readdirSync(d)) if (/^es-[\w-]+\.js$/.test(n) && !n.endsWith('.utopia-orig')) files.push(path.join(d, n));
  }
  let touched = 0, applied = 0, missing = new Set();
  for (const f of files) {
    const src = fs.readFileSync(fs.existsSync(f + '.utopia-orig') ? f + '.utopia-orig' : f, 'utf-8');
    const m = src.match(/JSON\.parse\(`([\s\S]*?)`\)/);
    if (!m) continue; // el otro chunk es/ de fechas
    pristine(f);
    // Valor "cocinado" del template literal: el contenido no lleva ${...} (se comprueba).
    if (m[1].includes('${')) throw new Error('el catálogo contiene ${ : formato inesperado');
    const cooked = m[1].replace(/\\([\\`$])/g, '$1');
    const cat = JSON.parse(cooked);
    let a = 0;
    for (const [msgid, val] of Object.entries(over)) {
      if (msgid.startsWith('_')) continue;
      const id = linguiId(msgid);
      if (!(id in cat)) { missing.add(msgid); continue; }
      cat[id] = val; a++;
    }
    const json = JSON.stringify(cat).replace(/\\/g, '\\\\').replace(/`/g, '\\`').replace(/\$\{/g, '\\${');
    const out = src.slice(0, m.index) + 'JSON.parse(`' + json + '`)' + src.slice(m.index + m[0].length);
    fs.writeFileSync(f, out); touched++; applied = Math.max(applied, a);
  }
  if (!touched) throw new Error('no se encontró ningún catálogo es-*.js');
  if (missing.size) warn('msgid que ya no existen en esta versión:', [...missing].join(' | '));
  return `${touched} ficheros, ${applied} textos`;
});

// 4) Traducciones del backend (correos): se fusionan sobre lang/es.json.
step('lang/es.json (backend)', () => {
  const f = path.join(BE, 'lang/es.json');
  const base = JSON.parse(pristine(f));
  const over = JSON.parse(fs.readFileSync(path.join(B, 'i18n/backend-es.json'), 'utf-8'));
  let n = 0;
  for (const [k, v] of Object.entries(over)) { if (k.startsWith('_')) continue; base[k] = v; n++; }
  fs.writeFileSync(f, JSON.stringify(base, null, 4));
  return `${n} claves`;
});

// 5) Estilo de los correos: se añade la hoja de Utopia al final del tema por defecto (Laravel la incrusta en línea).
step('tema de correo', () => {
  const f = path.join(BE, 'resources/views/vendor/mail/html/themes/default.css');
  const base = pristine(f);
  const add = fs.readFileSync(path.join(B, 'mail/utopia-mail.css'), 'utf-8');
  fs.writeFileSync(f, base + '\n/* === Utopia Tickets === */\n' + add);
  return `${add.length} bytes añadidos`;
});

// 6) Plantillas Blade con fechas en inglés, y el alta libre (CreateAccountRequest/Action,
//    UpdateEventStatusHandler) y ficheros nuevos («nuevo»: true, como la migración de utopia_aceptaciones) (formato fijo 'F j, Y' / 'D, M j, Y · g:i A'): se sustituyen solo si el
//    original coincide con el sha256 esperado; si la imagen cambió, se deja el original y se avisa.
step('plantillas Blade (fechas y pie)', () => {
  const man = JSON.parse(fs.readFileSync(path.join(B, 'overrides/manifest.json'), 'utf-8'));
  const done = [];
  for (const it of man) {
    const dst = path.join(ROOT, it.target);
    if (it.nuevo) {
      // Fichero NUEVO de la marca (p. ej. una migración propia): se escribe si no existe o si ya es
      // nuestro (lleva «Fichero NUEVO que añade la marca»). Nunca se pisa un fichero de la imagen con el mismo nombre.
      const nuestro = fs.readFileSync(path.join(B, 'overrides', it.file), 'utf-8');
      if (fs.existsSync(dst) && !fs.readFileSync(dst, 'utf-8').includes('Fichero NUEVO que añade la marca')) { warn(`${it.target}: ya existe en la imagen, no se toca`); continue; }
      fs.writeFileSync(dst, nuestro);
      done.push(path.basename(it.target) + ' (nuevo)');
      continue;
    }
    if (!fs.existsSync(dst)) { warn('no existe', it.target); continue; }
    const orig = pristine(dst);
    const sha = crypto.createHash('sha256').update(orig).digest('hex');
    if (sha !== it.originalSha256) { warn(`${it.target}: el original cambió (${sha.slice(0, 12)}), se deja el de la imagen`); continue; }
    fs.writeFileSync(dst, fs.readFileSync(path.join(B, 'overrides', it.file), 'utf-8'));
    done.push(path.basename(it.target));
  }
  return done.join(', ');
});

// 7) Idioma por defecto de la app (los correos sin idioma propio, como el aviso al organizador, salían en inglés):
//    config/app.php trae 'locale' => 'en' fijo; se cambia por env('APP_LOCALE', 'en') y el .env pone APP_LOCALE=es.
step('config/app.php (locale)', () => {
  const f = path.join(BE, 'config/app.php');
  if (!fs.existsSync(f)) throw new Error('no existe config/app.php');
  const orig = pristine(f);
  const needle = "'locale' => 'en',";
  if (orig.split(needle).length !== 2) throw new Error("no encuentro una sola línea 'locale' => 'en' (¿cambió la imagen?)");
  fs.writeFileSync(f, orig.replace(needle, "'locale' => env('APP_LOCALE', 'en'),"));
  return 'APP_LOCALE=' + (process.env.APP_LOCALE || '(sin definir: en)');
});

// 8) Textos fijos en el JavaScript compilado (no pasan por lingui): la entrada de ejemplo de la pantalla de acceso, el
//    título por defecto del organizador, etc. Por fichero: solo si el original coincide con su sha256 y
//    cada texto aparece exactamente las veces esperadas; si no, se deja el de la imagen y se avisa.
step('textos fijos del JS', () => {
  const f = path.join(B, 'overrides/js-textos.json');
  if (!fs.existsSync(f)) return 'sin js-textos.json';
  const man = JSON.parse(fs.readFileSync(f, 'utf-8'));
  let ok = 0, total = 0; const avisos = [];
  for (const g of man.grupos || []) {
    for (const it of g.ficheros) {
      total++;
      const dst = path.join(ROOT, it.ruta);
      if (!fs.existsSync(dst)) { avisos.push(`${g.nombre}: no existe ${it.ruta}`); continue; }
      const orig = pristine(dst);
      const sha = crypto.createHash('sha256').update(orig).digest('hex');
      if (sha !== it.sha256) { avisos.push(`${g.nombre}: ${it.ruta} cambió (${sha.slice(0, 12)})`); continue; }
      let out = orig, bien = true;
      for (const [de, a, n] of it.cambios || g.cambios) {
        const c = out.split(de).length - 1;
        if (c !== n) { avisos.push(`${g.nombre}: ${it.ruta} tiene ${c} veces ${de} (esperaba ${n})`); bien = false; break; }
        out = out.split(de).join(a);
      }
      if (!bien) continue;
      fs.writeFileSync(dst, out); ok++;
    }
  }
  if (avisos.length) throw new Error(`${ok}/${total} ficheros; ` + avisos.join(' | '));
  return `${ok}/${total} ficheros`;
});

// 9) Caché de los navegadores: los .js de /assets/ llevan el mismo nombre aunque los cambiemos y el
//    servidor no manda Cache-Control, así que un navegador que ya los tenía seguía usando la versión vieja durante
//    horas (y React avisaba de textos distintos). Para cada .js del cliente que hemos tocado (los que tienen copia
//    *.utopia-orig) se añade ?v=<huella del contenido>: en el <script> de entrada y con un importmap para los que se
//    importan desde otros módulos. Si algo no encaja, index.html se queda como lo dejó el paso 1.
step('versiones contra la caché', () => {
  const f = path.join(FE, 'client/index.html');
  let h = fs.readFileSync(f, 'utf-8');
  if (h.includes('type="importmap"')) throw new Error('index.html ya trae un importmap: no se toca');
  const dir = path.join(FE, 'client/assets');
  const map = {};
  for (const n of fs.readdirSync(dir)) {
    if (!n.endsWith('.js') || !fs.existsSync(path.join(dir, n + '.utopia-orig'))) continue;
    const v = crypto.createHash('sha1').update(fs.readFileSync(path.join(dir, n))).digest('hex').slice(0, 10);
    map['/assets/' + n] = '/assets/' + n + '?v=' + v;
  }
  if (!Object.keys(map).length) return 'nada que versionar';
  const m = h.match(/<script type="module" crossorigin src="(\/assets\/[\w-]+\.js)"><\/script>/);
  if (!m) throw new Error('no encuentro el <script type="module"> de entrada en index.html');
  const im = `<script type="importmap">${JSON.stringify({ imports: map })}</script>\n    `;
  h = h.replace(m[0], im + m[0].replace(m[1], map[m[1]] || m[1]));
  fs.writeFileSync(f, h);
  return `${Object.keys(map).length} módulos versionados`;
});

// 10) nginx: cabeceras de seguridad, sin versión de nginx ni «X-Powered-By: Express», caché larga en
//     /assets/ (con huella) y de una hora en /utopia/, y el panel fuera de marcos ajenos. Solo si el nginx.conf de la
//     imagen coincide con su sha256; si no, se deja el de la imagen y se avisa. nginx arranca después (supervisord),
//     así que lee la versión nueva. Los fragmentos viven en /branding/nginx/.
//     Si existe nginx/idioma.conf (un map de nivel http), se incluye en http {} y «location /» manda al
//     SSR $utopia_accept_language: «es» cuando la petición no trae idioma (los rastreadores) y el suyo cuando lo trae.
//     Antes se pasa «nginx -t» con esa versión; si falla, se escribe la de siempre y se avisa. Sin idioma.conf, el
//     nginx.conf sale byte a byte igual que antes.
function nginxValida(conf) {
  const tmp = NGINX + '.utopia-candidata';
  fs.writeFileSync(tmp, conf);
  // stdout y stderr heredados: nginx.conf abre /dev/stdout y /dev/stderr para sus logs, y con un pipe de Node (un
  // socket) nginx -t falla con ENXIO. Así el detalle del error, si lo hay, queda en el log del contenedor.
  try { execFileSync('nginx', ['-t', '-q', '-c', tmp], { stdio: ['ignore', 'inherit', 'inherit'] }); return true; }
  catch (e) { return String(e.status != null ? `salida ${e.status}` : (e.code || e.message || e)); }
  finally { fs.rmSync(tmp, { force: true }); }
}
step('nginx (cabeceras y caché)', () => {
  const f = NGINX;
  const ESPERADO = '7ed3bfa6ca1880b3962332f4b49cd521fc96fce7e92f9c7d16df7fa85705cbca';
  if (!fs.existsSync(f)) throw new Error('no existe ' + f);
  if (!fs.existsSync(path.join(B, 'nginx/cabeceras.conf'))) throw new Error('faltan los fragmentos de /branding/nginx');
  const orig = pristine(f);
  const sha = crypto.createHash('sha256').update(orig).digest('hex');
  if (sha !== ESPERADO) throw new Error(`nginx.conf cambió (${sha.slice(0, 12)}), se deja el de la imagen`);
  const xss = '       add_header X-XSS-Protection "1; mode=block";';
  const loc = '       location / {\n           proxy_pass http://localhost:5678;';
  if (orig.split(xss).length !== 2 || orig.split(loc).length !== 2 || orig.split('http {').length !== 2) throw new Error('nginx.conf no tiene la forma esperada');
  let n = orig.replace('http {', 'http {\n   server_tokens off;');
  n = n.replace(xss, '       include /branding/nginx/cabeceras.conf;\n       include /branding/nginx/ubicaciones.conf;');
  n = n.replace(loc, loc + '\n           proxy_hide_header X-Powered-By;');
  let idioma = '';
  if (fs.existsSync(path.join(B, 'nginx/idioma.conf'))) {
    const c = n.replace('   server_tokens off;', '   server_tokens off;\n   include /branding/nginx/idioma.conf;')
      .replace(loc + '\n           proxy_hide_header X-Powered-By;',
        loc + '\n           proxy_hide_header X-Powered-By;\n           proxy_set_header Accept-Language $utopia_accept_language;');
    const ok = nginxValida(c);
    if (ok === true) { n = c; idioma = ', SSR en español sin Accept-Language'; }
    else warn('nginx (idioma): nginx -t falla con idioma.conf, se deja sin ella:', ok);
  }
  fs.writeFileSync(f, n);
  return 'server_tokens off, 4 cabeceras, caché de /assets y /utopia, panel con X-Frame-Options' + idioma;
});

const bad = results.filter(r => r[1] !== 'OK').length;
log(`fin: ${results.length - bad} OK, ${bad} con aviso`);
