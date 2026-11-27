/* Portada pública de Utopia Tickets: lista los eventos PUBLICADOS y no terminados de los organizadores
   de data-organizadores (por defecto solo el 1, «Utopia») con el API público de Hi.Events. Nada a mano.
   Defensas: (1) credentials:'omit' para que la sesión de un organizador no cuele sus borradores (el API los devuelve
   si la petición lleva su sesión); (2) solo organizadores con status LIVE; (3) solo eventos status LIVE y no ENDED. */
(function () {
  'use strict';
  var raiz = document.getElementById('eventos');
  if (!raiz) return;
  var lista = document.getElementById('eventos-lista');
  var estado = document.getElementById('eventos-estado');
  var ids = (raiz.getAttribute('data-organizadores') || '1').split(',').map(function (s) { return s.trim(); })
    .filter(function (s) { return /^\d+$/.test(s); });
  var PORTADA_GENERICA = '/utopia/evento/portada-generica.jpg';

  function pedir(url) {
    return fetch(url, { credentials: 'omit', headers: { Accept: 'application/json' }, cache: 'no-store' })
      .then(function (r) { if (!r.ok) { var e = new Error('HTTP ' + r.status); e.status = r.status; throw e; } return r.json(); });
  }

  function organizador(id) {
    return pedir('/api/public/organizers/' + id).then(function (j) {
      var o = j && j.data;
      if (!o || o.status !== 'LIVE') return [];
      return pedir('/api/public/organizers/' + id + '/events?per_page=50').then(function (k) {
        return ((k && k.data) || []).map(function (e) { e.__org = o; return e; });
      });
    }).catch(function (e) { if (e && e.status === 404) return []; throw e; });
  }

  function productos(e) {
    var out = [];
    (e.product_categories || []).forEach(function (c) {
      if (c.is_hidden) return;
      (c.products || []).forEach(function (p) { if (!p.is_hidden && !p.is_hidden_without_promo_code && !p.is_addon_only) out.push(p); });
    });
    return out;
  }

  function situacion(e) {
    var ps = productos(e);
    if (e.products_sold_out || e.upcoming_occurrences_sold_out || (ps.length && ps.every(function (p) { return p.is_sold_out; }))) return 'agotado';
    if (ps.length && ps.every(function (p) { return p.is_before_sale_start_date; })) return 'pronto';
    if (ps.length && ps.every(function (p) { return p.is_after_sale_end_date; })) return 'cerrado';
    if (!ps.length) return 'sin';
    return 'venta';
  }

  function fecha(e) {
    var iso = e.next_occurrence_start_date || e.start_date;
    if (!iso) return '';
    var d = new Date(iso);
    if (isNaN(d)) return '';
    try {
      return new Intl.DateTimeFormat('es-ES', { timeZone: e.timezone || 'Europe/Madrid', weekday: 'short', day: 'numeric',
        month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' }).format(d).replace(',', ' ·');
    } catch (x) { return d.toLocaleString('es-ES'); }
  }

  function lugar(e) {
    var l = e.event_location || {};
    if (l.type === 'ONLINE') return 'En línea';
    var loc = l.location || {};
    var a = loc.structured_address || {};
    var nombre = a.venue_name || loc.name || '';
    var ciudad = a.city || '';
    if (nombre && ciudad && nombre.indexOf(ciudad) === -1) return nombre + ' · ' + ciudad;
    return nombre || ciudad;
  }

  function portada(e) {
    var im = (e.images || []).filter(function (i) { return i.type === 'EVENT_COVER' && i.url; })[0];
    return im ? im.url : PORTADA_GENERICA;
  }

  function el(tag, cls, txt) { var n = document.createElement(tag); if (cls) n.className = cls; if (txt != null) n.textContent = txt; return n; }

  function tarjeta(e) {
    var li = el('li');
    var a = el('a', 'ev');
    a.href = '/event/' + encodeURIComponent(e.id) + '/' + encodeURIComponent(e.slug || 'evento');
    var img = el('div', 'img');
    img.style.backgroundImage = 'url("' + String(portada(e)).replace(/["\\\n\r]/g, '') + '")';
    img.setAttribute('role', 'presentation');
    var t = el('div', 'txt');
    t.appendChild(el('span', 'fecha', fecha(e)));
    t.appendChild(el('span', 'titulo', e.title || ''));
    var lu = lugar(e); if (lu) t.appendChild(el('span', 'lugar', lu));
    var pie = el('span', 'pie');
    var s = situacion(e);
    if (s === 'agotado') pie.appendChild(el('span', 'estado agotado', 'Agotado'));
    else if (s === 'pronto') pie.appendChild(el('span', 'estado', 'Próximamente a la venta'));
    else if (s === 'cerrado' || s === 'sin') pie.appendChild(el('span', 'estado', 'Venta cerrada'));
    pie.appendChild(el('span', 'cta', s === 'venta' ? 'Entradas' : 'Ver evento'));
    t.appendChild(pie);
    a.appendChild(img); a.appendChild(t);
    li.appendChild(a);
    return li;
  }

  function vacio() {
    estado.className = 'vacio';
    estado.innerHTML = '';
    estado.appendChild(el('strong', null, 'Ahora mismo no hay eventos a la venta.'));
    var p = el('p', null, 'Estamos preparando los próximos conciertos: vuelve pronto. Mientras, conoce a Utopia en ');
    var a = el('a', null, 'utopiabooking.com'); a.href = 'https://utopiabooking.com';
    p.appendChild(a); p.appendChild(document.createTextNode('.'));
    estado.appendChild(p);
  }

  function fallo() {
    estado.className = 'vacio';
    estado.innerHTML = '';
    estado.appendChild(el('strong', null, 'No hemos podido cargar los eventos.'));
    var p = el('p', null, 'Vuelve a intentarlo en un momento o ');
    var a = el('a', null, 'mira la página de Utopia'); a.href = '/events/1/utopia';
    p.appendChild(a); p.appendChild(document.createTextNode('.'));
    estado.appendChild(p);
  }

  if (!ids.length || !window.fetch) { fallo(); return; }
  Promise.all(ids.map(organizador)).then(function (grupos) {
    var vistos = {};
    var evs = [].concat.apply([], grupos).filter(function (e) {
      if (!e || e.status !== 'LIVE' || e.lifecycle_status === 'ENDED' || vistos[e.id]) return false;
      vistos[e.id] = true; return true;
    });
    evs.sort(function (a, b) { return String(a.next_occurrence_start_date || a.start_date || '9').localeCompare(String(b.next_occurrence_start_date || b.start_date || '9')); });
    if (!evs.length) { vacio(); raiz.setAttribute('data-total', '0'); return; }
    evs.forEach(function (e) { lista.appendChild(tarjeta(e)); });
    estado.hidden = true;
    lista.hidden = false;
    raiz.setAttribute('data-total', String(evs.length));
  }).catch(function () { fallo(); raiz.setAttribute('data-total', 'error'); });
})();
