# Contenido de las páginas propias de Utopia Tickets. Lo usa gen_paginas.py.
# Datos de la empresa: los públicos del aviso legal (Registro Mercantil).
# Tarifa: 0,50 € + IVA por entrada de pago; los gastos de gestión los decide el promotor. Devoluciones: las pide el
# comprador al promotor; son obligatorias si se cancela; la comisión de Utopia no se devuelve nunca.

FECHA = '25 de noviembre de 2026'
VERSION = '20261125b'
VERSION_LEGAL = '2026-11-26'
ORG_URL = '/events/1/utopia'
MAIL = 'tickets@utopiabooking.com'
MAIL_PRIV = 'privacidad@utopiabooking.com'
TEL = '640 05 87 78'

EMPRESA = f'''<ul class="datos">
<li><strong>Titular:</strong> UTOPIA BOOKING S.L.</li>
<li><strong>NIF:</strong> B22863963</li>
<li><strong>Domicilio social:</strong> Ctra. de Alomartes 27, 1.º B, 18260 Íllora (Granada), España</li>
<li><strong>Registro:</strong> Registro Mercantil de Granada, hoja GR-63674 (folio electrónico), inscripción 1.ª · EUID ES18020.000451995</li>
<li><strong>Correo:</strong> <a href="mailto:{MAIL}">{MAIL}</a> · <strong>Teléfono:</strong> {TEL}</li>
</ul>'''

R = lambda t: f' <span class="rev">[{t}]</span>'

def secciones(items):
    """items: [(ancla, título, html)] → (toc, body) con numeración."""
    toc, body = [], []
    for i, (a, t, h) in enumerate(items, 1):
        toc.append((a, f'{i}. {t}'))
        body.append(f'<h2 id="{a}">{i}. {t}</h2>\n{h}')
    return toc, '\n\n'.join(body)

# ---------------------------------------------------------------- aviso legal
import os as _os
REPO_PUBLICO = _os.environ.get('REPO_PUBLICO', '0') == '1'
REPO_URL = 'https://github.com/utopia-tickets/utopia-tickets-hievents'
_CODIGO = (f'Puedes descargarlo en <a href="{REPO_URL}">{REPO_URL}</a>.' if REPO_PUBLICO else
           f'Si lo quieres, escríbenos a <a href="mailto:{MAIL}">{MAIL}</a> y te lo mandamos gratis.')

AVISO = [
    ('titular', 'Quién somos', f'''<p>Este sitio, Utopia Tickets, es un servicio de UTOPIA BOOKING S.L. (en adelante, «Utopia»). Estos son sus datos (artículo 10 de la Ley 34/2002 de servicios de la sociedad de la información, LSSI):</p>
{EMPRESA}'''),
    ('servicio', 'Qué es Utopia Tickets', '''<p>Utopia Tickets es una plataforma de venta de entradas. Los organizadores de cada evento («promotores») se dan de alta, aceptan sus condiciones y la usan para vender sus entradas y cobrarlas en su propia cuenta de Stripe. Todos actúan como empresarios o profesionales. En la página de cada evento se indica quién lo organiza y vende: es con esa persona o empresa con quien contratas la entrada. Utopia presta la plataforma y no es parte de ese contrato, salvo cuando el organizador es la propia Utopia.</p>
<p>La compra de entradas se rige por las <a href="/utopia/legal/condiciones-de-compra.html">condiciones de compra</a> y la <a href="/utopia/legal/reventa-y-transferencia.html">política de reventa y transferencia</a>; el uso de la plataforma por los promotores, por las <a href="/utopia/legal/condiciones-promotores.html">condiciones para promotores</a>.</p>'''),
    ('uso', 'Uso del sitio', '''<p>Puedes navegar por el sitio sin registrarte. Al usarlo te comprometes a hacerlo de buena fe, sin dañar el servicio, sin intentar acceder a datos o cuentas que no son tuyas, sin automatizar compras (bots) y sin usar las entradas ni el sitio para fines ilícitos. Utopia puede bloquear el acceso a quien lo incumpla.</p>'''),
    ('contenidos', 'Avisos de contenidos ilícitos y puntos de contacto', f'''<p>Utopia Tickets aloja información de terceros: los eventos que publican los promotores. Por eso aplica el Reglamento (UE) 2022/2065 de servicios digitales.</p>
<ul>
<li><strong>Punto de contacto único</strong>, para las autoridades y para cualquier usuario: <a href="mailto:{MAIL}">{MAIL}</a>. Te atiende una persona, en español o en inglés.</li>
<li><strong>Cómo avisar de un contenido ilícito</strong> (por ejemplo, un evento falso, una estafa, un contenido que vulnera tus derechos o que incita al odio): escríbenos a ese correo con la dirección exacta (URL) del contenido, por qué crees que es ilícito, tu nombre y tu correo (no hace falta si se trata de ciertos delitos contra menores) y una declaración de que lo que dices es cierto y lo haces de buena fe.</li>
<li><strong>Qué hacemos:</strong> te confirmamos que lo hemos recibido, lo revisa una persona con diligencia y objetividad, y te decimos qué hemos decidido y cómo puedes impugnarlo. Si retiramos un contenido o suspendemos una cuenta, le explicamos al promotor el motivo, como dicen las <a href="/utopia/legal/condiciones-promotores.html#moderacion">condiciones para promotores</a>.</li>
<li>Si sabemos de algo que haga sospechar un delito que amenace la vida o la seguridad de las personas, lo comunicamos enseguida a las autoridades.</li>
</ul>'''),
    ('propiedad', 'Propiedad intelectual y software libre', f'''<p>La marca, el logotipo y los textos propios de Utopia Tickets son de Utopia. Los carteles, imágenes, nombres y textos de cada evento son de su organizador o de sus titulares, que los publican bajo su responsabilidad.</p>
<p>La plataforma funciona con <a href="https://hi.events">Hi.Events</a>, software libre con licencia AGPL-3.0, al que Utopia ha añadido su marca y sus textos. Por esa licencia, el código fuente de la versión que usamos, con nuestros cambios, está a disposición de quien use el servicio. {_CODIGO}</p>'''),
    ('responsabilidad', 'Responsabilidad', '''<p>Utopia procura que la información del sitio sea correcta y que el servicio esté disponible. No responde del contenido que publica cada organizador sobre su evento ni de la celebración del evento, que son responsabilidad del organizador, pero retira con prontitud lo que sea ilícito en cuanto lo conoce. Los enlaces a sitios de terceros se ofrecen solo como ayuda. Nada de este aviso limita los derechos que te da la ley como consumidor.</p>'''),
    ('ley', 'Ley aplicable', '''<p>Este aviso se rige por la ley española. Si eres consumidor, puedes reclamar ante los tribunales de tu domicilio.</p>'''),
]

# ---------------------------------------------------------------- privacidad
PRIV = [
    ('quien', 'Quién trata tus datos', f'''<p>En Utopia Tickets hay papeles distintos según quién seas y para qué se usen tus datos:</p>
<div class="tablewrap"><table>
<thead><tr><th>Si eres…</th><th>Responsable de tus datos</th><th>Papel de Utopia</th></tr></thead>
<tbody>
<tr><td><strong>Comprador o asistente</strong> de un evento</td><td>El <strong>organizador del evento</strong>, que aparece en su página y en tus correos, para todo lo que tiene que ver con tu compra y tu entrada</td><td>Encargada del tratamiento: presta la plataforma al organizador y trata tus datos solo para lo que él necesita (artículo 28 del RGPD)</td></tr>
<tr><td>Comprador de un evento <strong>organizado por Utopia</strong></td><td>Utopia</td><td>Responsable</td></tr>
<tr><td><strong>Promotor</strong> con cuenta en la plataforma, o quien se da de alta</td><td>Utopia</td><td>Responsable</td></tr>
<tr><td><strong>Cualquier persona</strong>, para la seguridad de la plataforma y la prevención del fraude, y cuando nos escribes una reclamación, una queja o un aviso de contenido ilícito</td><td>Utopia</td><td>Responsable, solo para esas finalidades</td></tr>
</tbody></table></div>
<p>Datos de Utopia:</p>
{EMPRESA}
<p>Para cualquier asunto de privacidad: <a href="mailto:{MAIL_PRIV}">{MAIL_PRIV}</a>. Utopia no está obligada a tener delegado de protección de datos; este correo cumple esa función de contacto.</p>'''),
    ('compradores', 'Compradores y asistentes', f'''<h3>Qué datos y de dónde salen</h3>
<ul>
<li>Nombre, apellidos y correo de quien compra y de cada asistente, y las respuestas a las preguntas que añada el organizador (por ejemplo, la talla de una camiseta). Si otra persona compró tu entrada, tus datos nos los dio ella.</li>
<li>El pedido: entradas, importes, fecha, estado del pago y de las devoluciones, y el uso de la entrada en la puerta (hora del escaneo).</li>
<li>Datos técnicos de la conexión (dirección IP y navegador) para la seguridad del servicio.</li>
<li>Los datos de tu tarjeta los recoge directamente Stripe. Ni Utopia ni el organizador los ven ni los guardan.</li>
</ul>
<p>Los datos marcados como obligatorios en la compra son necesarios para venderte la entrada y mandártela: sin ellos no se puede comprar.</p>
<h3>Para qué y con qué base</h3>
<div class="tablewrap"><table>
<thead><tr><th>Finalidad</th><th>Quién decide</th><th>Base legal</th></tr></thead>
<tbody>
<tr><td>Gestionar tu compra, mandarte las entradas, controlar el acceso y atender tus dudas y devoluciones</td><td>El organizador</td><td>Contrato (art. 6.1.b RGPD)</td></tr>
<tr><td>Guardar los pedidos para la contabilidad y los impuestos del organizador</td><td>El organizador</td><td>Obligación legal (art. 6.1.c)</td></tr>
<tr><td>Mandarte novedades del organizador, solo si marcas la casilla al comprar</td><td>El organizador</td><td>Consentimiento (art. 6.1.a), que puedes retirar en cualquier momento con el enlace de cada correo</td></tr>
<tr><td>Proteger la plataforma: frenar bots, compras fraudulentas, reventa abusiva y ataques</td><td>Utopia</td><td>Interés legítimo de Utopia, de los organizadores y de los compradores en un servicio seguro (art. 6.1.f)</td></tr>
<tr><td>Atender las reclamaciones, hojas de quejas y avisos de contenidos ilícitos que nos mandes</td><td>Utopia</td><td>Obligación legal (art. 6.1.c: ley de consumidores y Reglamento de servicios digitales)</td></tr>
</tbody></table></div>
<p>Utopia no te manda publicidad propia por haber comprado una entrada de otro organizador. Los correos de tu pedido y de cambios o cancelaciones del evento no son publicidad: te llegan aunque no marques la casilla.</p>
<p><strong>Decisiones automáticas.</strong> Utopia no toma decisiones automatizadas que te afecten de forma significativa. Stripe puede rechazar de forma automática un pago que su sistema considere fraudulento, y Cloudflare puede pedirte una comprobación de que no eres un robot. Si te pasa y crees que es un error, escríbenos y lo revisa una persona.</p>
<h3>Cuánto tiempo</h3>
<p>Mientras dure el evento y las posibles reclamaciones, y después el tiempo que exige la ley para la contabilidad y los impuestos (hasta 6 años). Si das de baja las novedades, se dejan de usar tus datos para eso en el momento. Los datos de seguridad de la conexión se borran en pocas semanas, salvo que hagan falta para un caso concreto de fraude.</p>
<h3>Tus derechos</h3>
<p>Puedes pedir el acceso, la rectificación, la supresión, la oposición, la limitación y la portabilidad de tus datos. Para lo que hace el organizador, pídeselo a él; si escribes a Utopia, le pasamos tu petición en un máximo de 5 días y te ayudamos a que se atienda. Para lo que decide Utopia (seguridad, fraude y reclamaciones), escríbenos a <a href="mailto:{MAIL_PRIV}">{MAIL_PRIV}</a>.</p>'''),
    ('promotores', 'Promotores y altas', '''<ul>
<li><strong>Datos:</strong> los de tu cuenta (nombre, correo y contraseña cifrada), los de tu empresa para la factura, el identificador de tu cuenta de Stripe, la constancia de que aceptaste las condiciones (qué versión, cuándo, desde qué IP y navegador) y el registro de uso de la plataforma.</li>
<li><strong>Para qué:</strong> darte el servicio, cobrarte la comisión y emitir su factura, avisarte de cambios del servicio y de las condiciones, <strong>revisar las altas nuevas y los eventos</strong> para prevenir el fraude y proteger a los compradores, atender los avisos de contenidos ilícitos y mantener la seguridad.</li>
<li><strong>Base:</strong> el contrato (condiciones para promotores), las obligaciones fiscales, mercantiles y del Reglamento de servicios digitales, y el interés legítimo en prevenir el fraude. Si marcas la casilla de novedades, tu consentimiento.</li>
<li><strong>Obligatorios:</strong> los datos marcados como obligatorios en el alta y en la facturación; sin ellos no podemos darte el servicio ni facturarte.</li>
<li><strong>Cuánto tiempo:</strong> mientras tengas la cuenta; después, la constancia de la aceptación y las facturas durante el plazo legal (6 años, Código de Comercio), y los datos de una cuenta suspendida por fraude, lo necesario para defender reclamaciones.</li>
<li><strong>Stripe</strong> verifica tu identidad y la de tu empresa cuando conectas tu cuenta. Lo hace según tu contrato con Stripe y, para la prevención del fraude y sus obligaciones legales, como responsable propio. Utopia solo recibe el identificador de la cuenta y si está verificada.</li>
</ul>'''),
    ('destinatarios', 'Con quién se comparten', '''<div class="tablewrap"><table>
<thead><tr><th>Quién</th><th>Para qué</th><th>Dónde</th></tr></thead>
<tbody>
<tr><td>El organizador del evento</td><td>Es el responsable de los datos de sus compradores</td><td>Según el organizador</td></tr>
<tr><td>Stripe Payments Europe, Ltd.</td><td>Cobro con tarjeta en la cuenta del organizador, verificación de los promotores y prevención del fraude</td><td>Irlanda (UE), con transferencias a EE. UU. cubiertas por el Marco de Privacidad de Datos UE-EE. UU. y cláusulas tipo</td></tr>
<tr><td>Cloudflare, Inc.</td><td>Conexión segura entre tu navegador y el servidor de Utopia (túnel cifrado), cortafuegos y protección frente a bots y ataques</td><td>EE. UU. y su red de centros de datos, con transferencias cubiertas por el Marco de Privacidad de Datos UE-EE. UU. y cláusulas tipo</td></tr>
<tr><td>Brevo SAS</td><td>Envío de los correos de la plataforma (pedidos, entradas, avisos)</td><td>Francia (UE), con servidores en la UE. Algunos de sus proveedores están en EE. UU., con el Marco de Privacidad de Datos y cláusulas tipo</td></tr>
<tr><td>Autoridades, juzgados y fuerzas de seguridad</td><td>Solo cuando lo exija la ley o para denunciar un fraude</td><td>España</td></tr>
</tbody></table></div>
<p>La plataforma funciona en un servidor propio de Utopia en España, y sus copias de seguridad se guardan cifradas, también en España. No vendemos datos ni los cedemos a nadie más.</p>'''),
    ('correos', 'Los correos que te mandamos', '''<p>Los correos de la plataforma (pedido, entradas, cambios del evento, acceso a la cuenta) salen con Brevo. Brevo añade a cada correo una imagen invisible y redirige los enlaces para contar las aperturas y los clics y detectar problemas de entrega; Utopia usa esos datos solo de forma agregada, para saber si los correos llegan. Si no quieres que se cuente la apertura, configura tu programa de correo para no cargar imágenes: tus entradas funcionan igual.</p>
<p>Si en un correo pulsas «darse de baja», Brevo puede dejar de entregarte también los correos de tus pedidos. Si te pasa y no te llegan tus entradas, escríbenos y lo solucionamos.</p>'''),
    ('seguridad', 'Seguridad', '''<p>La plataforma va cifrada (HTTPS y un túnel cifrado hasta el servidor), las contraseñas se guardan cifradas, el panel de administración no es accesible desde internet, el acceso del equipo de Utopia está limitado a lo imprescindible y las copias de seguridad diarias se guardan cifradas. Si hay una brecha de seguridad, Utopia avisa al organizador responsable sin demora y, cuando el riesgo lo exija, a las personas afectadas y a la Agencia Española de Protección de Datos, como manda el RGPD.</p>'''),
    ('menores', 'Menores', '''<p>Para comprar hay que ser mayor de edad o tener al menos 14 años y el permiso de tu madre, tu padre o tu tutor (artículo 7 de la Ley Orgánica 3/2018). Si un menor de 14 años va a un evento, la entrada la compra un adulto responsable. Para darse de alta como promotor hay que ser mayor de edad.</p>
<p>Utopia no pide por su cuenta la edad de los asistentes ni documentos de los menores. Si un organizador o un recinto pide una autorización firmada o un documento de identidad para que entre un menor, se le entrega a él en el acceso al evento: lo trata el organizador o el recinto como responsable, según su propia política de privacidad, y Utopia no lo recibe.</p>'''),
    ('cambios', 'Cambios de esta política', '''<p>Si cambiamos esta política, publicaremos la versión nueva con su fecha y, si el cambio es importante, avisaremos por correo a los promotores. Las versiones aceptadas en cada alta se guardan.</p>'''),
    ('reclamar', 'Reclamar', '''<p>Si crees que no hemos tratado bien tus datos, puedes reclamar ante la Agencia Española de Protección de Datos (<a href="https://www.aepd.es">aepd.es</a>). Antes, si quieres, escríbenos y lo intentamos resolver.</p>
<p>Las cookies se explican en su propia página: <a href="/utopia/legal/cookies.html">cookies</a>.</p>'''),
]

# ---------------------------------------------------------------- cookies
# Medición en el dominio público (25-nov-2026) y en una compra de prueba con Stripe. Se repite si cambia la plataforma.
COOKIES = [
    ('resumen', 'En corto', '''<p>Utopia Tickets solo usa las cookies y el almacenamiento imprescindibles para que funcionen la compra, el pago y el panel, y para proteger la plataforma frente a bots y ataques. No usamos cookies de análisis ni de publicidad, así que no te pedimos permiso con un aviso: estas cookies no lo necesitan (artículo 22.2 de la LSSI y guía de cookies de la Agencia Española de Protección de Datos). Si algún organizador activa un píxel de seguimiento en su página, te lo pedirá antes de cargarlo.</p>'''),
    ('lista', 'Qué guardamos en tu navegador', '''<div class="tablewrap"><table>
<thead><tr><th>Nombre</th><th>De quién</th><th>Para qué</th><th>Cuánto dura</th></tr></thead>
<tbody>
<tr><td><code>cf_clearance</code></td><td>Cloudflare (para Utopia Tickets)</td><td>Recordar que tu navegador ya pasó la comprobación de seguridad frente a bots. Puede aparecer en cualquier página</td><td>6 meses</td></tr>
<tr><td><code>previous_url</code> (almacenamiento local)</td><td>Utopia Tickets</td><td>Recordar a qué página volver después de iniciar sesión</td><td>Hasta que lo borres</td></tr>
<tr><td><code>session_identifier</code></td><td>Utopia Tickets</td><td>Recordar tu compra mientras rellenas los datos</td><td>La sesión</td></tr>
<tr><td><code>hievents.checkout.session.*</code> (almacenamiento de sesión)</td><td>Utopia Tickets</td><td>Mantener tus entradas reservadas durante el pago</td><td>Hasta cerrar la pestaña</td></tr>
<tr><td><code>token</code> (solo en el panel de promotores)</td><td>Utopia Tickets</td><td>Mantener abierta tu sesión de promotor (no accesible desde JavaScript)</td><td>La sesión</td></tr>
<tr><td><code>__stripe_mid</code></td><td>Stripe (solo en la página de pago)</td><td>Prevenir el fraude en el pago</td><td>6 meses</td></tr>
<tr><td><code>__stripe_sid</code></td><td>Stripe (solo en la página de pago)</td><td>Prevenir el fraude en el pago</td><td>30 minutos</td></tr>
</tbody></table></div>
<p>En el alta, el inicio de sesión y la recuperación de la contraseña se carga además Cloudflare Turnstile, una comprobación de que no eres un robot que no guarda cookies en este sitio. Stripe solo se carga en la página de pago. La letra y los iconos se sirven desde nuestro propio servidor, sin terceros.</p>
<p>Medido en tickets.utopiabooking.com el 25 de noviembre de 2026 (páginas públicas, alta y acceso) y en una compra de prueba de noviembre de 2026 (pago). Si esta lista cambia, actualizaremos esta página y su fecha.</p>'''),
    ('correos', 'En los correos', '''<p>Los correos de la plataforma llevan una imagen invisible de Brevo que cuenta si se abren, y sus enlaces pasan por Brevo para contar los clics. Se usa solo de forma agregada, para saber si los correos llegan. Si no lo quieres, configura tu programa de correo para no cargar imágenes. Más detalle en <a href="/utopia/legal/privacidad.html#correos">privacidad</a>.</p>'''),
    ('borrar', 'Cómo borrarlas', '''<p>Puedes borrarlas desde los ajustes de tu navegador. Si las bloqueas, puede que tengas que repetir la comprobación de seguridad y no podrás terminar una compra ni entrar en el panel.</p>'''),
]

# ---------------------------------------------------------------- condiciones de compra
COMPRA = [
    ('vende', 'Quién te vende la entrada', f'''<p>Cada evento lo organiza y vende su <strong>organizador</strong> (el «promotor»), que aparece en la página del evento, en el resumen de compra y en tus correos. El contrato de la entrada es con él, y él responde de que el evento se celebre como se anunció. Todos los organizadores de Utopia Tickets han declarado actuar como empresarios o profesionales, así que en tu compra se aplican todos tus derechos como consumidor.</p>
<p>Todos los organizadores venden con estas condiciones. Cada uno puede añadir en la página de su evento condiciones propias (por ejemplo, de admisión o una política de devoluciones más generosa), pero nunca empeorar las de aquí ni tus derechos legales.</p>
<p>Utopia Tickets es la plataforma de venta de UTOPIA BOOKING S.L., que presta el servicio al organizador como intermediaria y no es parte del contrato de la entrada. <strong>El dinero de tu entrada va directamente a la cuenta del organizador</strong>, no a Utopia. Cuando el organizador es Utopia, Utopia es quien te vende.</p>
{EMPRESA}'''),
    ('reparto', 'Quién responde de qué', f'''<div class="tablewrap"><table>
<thead><tr><th>Asunto</th><th>Responde</th></tr></thead>
<tbody>
<tr><td>Que el evento se celebre como se anunció, el recinto, la seguridad y el acceso</td><td>El organizador</td></tr>
<tr><td>Las devoluciones (cancelación, aplazamiento, cambios) y la factura de tu entrada</td><td>El organizador, que es quien cobró</td></tr>
<tr><td>Que la web, el pago y el envío de las entradas funcionen, y tus datos en la plataforma</td><td>Utopia</td></tr>
<tr><td>Ayudarte si el organizador no te contesta</td><td>Utopia (ver <a href="#devoluciones">cómo pedir una devolución</a>)</td></tr>
</tbody></table></div>
<p>Utopia no da garantías ni seguros propios sobre el evento. Tampoco hay un buscador que ordene eventos de varios organizadores: cada organizador tiene su página, con sus eventos por fecha, y nadie paga por salir antes. Las dudas y reclamaciones se resuelven como se explica en <a href="#reclamaciones">dudas y reclamaciones</a>.</p>'''),
    ('compra', 'Cómo se compra', '''<ol>
<li>Eliges el evento, el tipo de entrada y cuántas quieres.</li>
<li>Escribes tu nombre y tu correo, y los de cada asistente si el evento lo pide.</li>
<li>Antes de pagar ves el resumen con el precio final de cada entrada, gastos incluidos, y el total. Si algo está mal, vuelve atrás y corrígelo antes de pulsar «Pagar».</li>
<li>Pagas. En cuanto se confirma el pago, te llega un correo con el pedido y otro con cada entrada.</li>
</ol>
<p>Las entradas quedan reservadas unos minutos mientras terminas la compra; si se acaba el tiempo, vuelven a la venta. El contrato queda cerrado cuando se confirma el pago. El organizador puede limitar cuántas entradas compra cada persona. La compra se hace en español. Tu pedido queda archivado en la plataforma y puedes verlo siempre desde el enlace «Ver pedido» de tu correo. Si después ves un error en el nombre de un asistente, puedes corregirlo como se explica en <a href="/utopia/legal/reventa-y-transferencia.html#titular">cambiar el nombre de una entrada</a> o pidiéndoselo al organizador, sin coste.</p>'''),
    ('precio', 'Precio y gastos de gestión', '''<p>Los precios van en euros y con el IVA incluido. El precio que ves anunciado es el que pagas. Si el organizador cobra <strong>gastos de gestión</strong>, van siempre incluidos en el precio anunciado, desglosados, y son un importe fijo por entrada, igual para todo el evento; el organizador explica qué incluyen. Si en algún caso no estaban incluidos en el precio anunciado, no tienes que pagarlos. No hay ningún otro cargo: ni por imprimir la entrada, ni por guardarla en el móvil, ni por corregir una errata en el nombre.</p>'''),
    ('pago', 'Pago', '''<p>El pago con tarjeta lo procesa Stripe en la cuenta del organizador. Ni Utopia ni el organizador ven los datos de tu tarjeta. Algunas tarjetas piden una comprobación de tu banco (3D Secure), y Stripe puede rechazar un pago si su sistema antifraude lo considera sospechoso; si te pasa, prueba otro medio de pago o escríbenos.</p>
<p>Si el organizador lo permite, puedes «pagar más tarde» (por ejemplo, en la taquilla o por transferencia). Las entradas no valen hasta que el organizador recibe el pago. La factura de tu entrada, si la necesitas, te la hace el organizador.</p>'''),
    ('entrada', 'Tu entrada y el código QR', '''<p>Cada entrada lleva un código QR único. Puedes enseñarlo en el móvil o imprimirlo. El QR solo vale una vez: al escanearlo en la puerta queda registrado y cualquier copia se rechaza. No publiques fotos de tu entrada: si alguien la copia y entra antes, no se puede comprobar quién es el titular.</p>
<p>Si pierdes el correo, recupéralo en <a href="/utopia/ayuda/#perdi">«¿Dónde están mis entradas?»</a>.</p>'''),
    ('acceso', 'Acceso al recinto y derecho de admisión', '''<p>En la página del evento están la hora de apertura de puertas y las condiciones de acceso. En la puerta pueden pedirte un documento de identidad y, si la entrada es nominativa, que coincida con el nombre. El organizador y el recinto solo pueden negar la entrada por motivos objetivos: aforo completo, no tener la edad mínima, no llevar entrada válida, poner en riesgo la seguridad o alterar el orden, llevar objetos prohibidos o no cumplir las condiciones específicas de admisión del recinto, que tienen que estar a la vista en la entrada (en Andalucía, aprobadas por el ayuntamiento). Nunca por motivos discriminatorios. Si te niegan la entrada o te expulsan por algo que es responsabilidad tuya, no se devuelve el precio. Los horarios y el orden de actuación pueden variar algo; si el cambio es importante, tienes derecho a la devolución (ver <a href="#cambios">cambios del evento</a>).</p>
<p>Si el organizador va a grabar o fotografiar al público para difundirlo, lo indica en la página del evento y en su información de privacidad.</p>'''),
    ('menores', 'Menores de edad', '''<p>Para comprar hay que ser mayor de edad o tener al menos 14 años y el permiso de tu madre, tu padre o tu tutor; las entradas de los menores de 14 las compra un adulto responsable. Todos los menores necesitan su propia entrada, salvo que el organizador indique otra cosa en la página del evento (por ejemplo, que los bebés no la necesitan).</p>
<p>La edad mínima y las condiciones para menores (por ejemplo, ir con su madre, padre o tutor) las fija cada organizador según la normativa de su comunidad autónoma, y tiene que indicarlas en la página del evento antes de la compra. Por ejemplo, en Andalucía los menores de 16 años no pueden entrar en pubs, bares con música, salas de fiesta ni discotecas, salvo las de juventud; pero, si el organizador lo permite, sí pueden ir a un concierto u otra actuación en directo en esos locales, solo mientras dure y siempre acompañados de su madre, su padre, su tutor o un adulto autorizado expresamente por ellos (artículo 3.2 del reglamento andaluz de admisión, en la redacción del Decreto 211/2018). Los papeles que pida el organizador para eso (por ejemplo, una autorización firmada) se entregan en el acceso al evento. Si un menor no cumple unas condiciones que estaban indicadas, se le puede negar la entrada sin devolución; si no estaban indicadas antes de comprar, el organizador te devuelve lo que pagaste.</p>'''),
    ('desistimiento', 'Sin derecho de desistimiento', '''<p>Las entradas son un servicio de ocio con fecha concreta, así que no tienen derecho de desistimiento (artículo 103.l del texto refundido de la Ley General para la Defensa de los Consumidores y Usuarios). No se devuelven por cambiar de planes; sí en los casos de <a href="#cancelacion">cancelación</a> y de <a href="#cambios">cambios del evento</a>.</p>'''),
    ('cancelacion', 'Si se cancela o se suspende el evento', '''<p>Si el evento se cancela, <strong>el organizador te devuelve todo lo que pagaste</strong>, gastos de gestión incluidos, en el mismo medio de pago y en un máximo de 14 días. No tienes que pedirlo: te llegará un correo cuando se haga.</p>
<p>Lo mismo si el evento se suspende cuando ya ha empezado por un fallo de las instalaciones o por una causa que dependa del organizador. Si se suspende ya empezado por una causa ajena a él (por ejemplo, una orden de la autoridad o un temporal), se aplica lo que diga la normativa de espectáculos de la comunidad donde se celebra.</p>'''),
    ('cambios', 'Si cambia la fecha, el lugar o el artista', '''<p>Si el evento se aplaza, cambia de recinto, <strong>cambia el artista principal</strong> anunciado o cambia en algo esencial de lo que compraste (por ejemplo, la hora de comienzo en más de dos horas), tu entrada vale para el evento modificado sin hacer nada. Si no te interesa, pide la devolución completa al organizador, gastos incluidos: puedes pedirla desde que se anuncia el cambio hasta 4 días después de la fecha prevista del evento (la nueva, si se aplaza), y siempre durante al menos 15 días desde el aviso. Si se aplaza sin nueva fecha y en 90 días no se ha anunciado, se trata como una cancelación. Un cambio menor del horario, del orden de actuación o de los teloneros no da derecho a devolución.</p>'''),
    ('fuerza', 'Fuerza mayor', '''<p>Ni el organizador ni Utopia responden de daños por causas que no pueden controlar ni evitar (catástrofes, órdenes de la autoridad, epidemias, cortes generales de suministro o de internet). Aun así, si el evento no se celebra, se aplica lo dicho en <a href="#cancelacion">cancelación</a> y te devuelven lo que pagaste.</p>'''),
    ('devoluciones', 'Cómo pedir una devolución', f'''<ul>
<li><strong>Las devoluciones las pides al organizador</strong> y las hace él, porque es quien recibió el dinero. Su correo está en la página del evento y en el correo de tu pedido. Tiene que contestarte en un máximo de 5 días hábiles.</li>
<li>Fuera de los casos de <a href="#cancelacion">cancelación</a> y de <a href="#cambios">cambios del evento</a>, el organizador no está obligado a devolver, aunque puede hacerlo si quiere.</li>
<li>La devolución llega al mismo medio de pago. Según tu banco, puede tardar unos días en verse. Las entradas devueltas quedan anuladas.</li>
<li>Si el organizador no te contesta, escríbenos a <a href="mailto:{MAIL}">{MAIL}</a>: le reclamamos nosotros y, si no atiende sus obligaciones, podemos suspender sus ventas. Utopia no cobra el precio de tu entrada, así que no puede devolvértelo ni garantiza la devolución, pero te daremos sus datos (nombre, NIF y domicilio) para que puedas reclamarle.</li>
<li>Las entradas no incluyen un seguro de cancelación para el comprador.</li>
<li>Te recomendamos pedir la devolución al organizador antes de abrir un contracargo en tu banco, porque suele ser más rápido. Si tu banco te devuelve el dinero por un contracargo, las entradas de ese pedido dejan de valer.</li>
</ul>'''),
    ('reventa', 'Reventa y cambio de titular', '''<p>Las entradas son para uso personal. No se pueden revender por encima del precio pagado ni usar con fines comerciales sin permiso del organizador. Las compradas con datos falsos, con programas automáticos, con tarjetas ajenas o para revenderlas pueden anularse. Si el organizador lo permite, puedes cambiar el nombre del asistente. El detalle está en la <a href="/utopia/legal/reventa-y-transferencia.html">política de reventa y transferencia</a>.</p>'''),
    ('accesibilidad', 'Accesibilidad', '''<p>La compra se puede hacer con teclado, lector de pantalla y zoom. El organizador indica en la página del evento si el recinto es accesible y cómo pedir plaza adaptada o entrada de acompañante. Si encuentras una barrera, escribe al organizador o a nosotros y te ayudamos.</p>'''),
    ('responsabilidad', 'Responsabilidad de Utopia', '''<p>Utopia responde de que la plataforma funcione con la diligencia debida y de tratar tus datos según la ley. No responde de la organización ni de la celebración del evento, que son del organizador. Nada de estas condiciones limita los derechos que te reconoce la ley como consumidor.</p>'''),
    ('reclamaciones', 'Dudas, reclamaciones y hojas de quejas', f'''<ul>
<li><strong>Sobre el evento</strong> (horarios, accesos, devoluciones), escribe al organizador.</li>
<li><strong>Sobre la plataforma</strong>, a Utopia: por correo a <a href="mailto:{MAIL}">{MAIL}</a>, por teléfono al {TEL} o por carta a UTOPIA BOOKING S.L., Ctra. de Alomartes 27, 1.º B, 18260 Íllora (Granada). Te contestamos lo antes posible y, como máximo, en 10 días.</li>
<li><strong>Hojas de quejas y reclamaciones:</strong> existen hojas de quejas y reclamaciones a tu disposición. Puedes pedírnoslas, en papel o en formato electrónico, en ese correo o en esa dirección, y también al organizador. En Andalucía tienes además la hoja electrónica oficial en <a href="https://www.consumoresponde.es">consumoresponde.es</a>.</li>
<li><strong>Si no quedas conforme:</strong> Utopia no está adherida a ningún sistema de arbitraje de consumo. Puedes acudir a los servicios de consumo de tu ayuntamiento o de tu comunidad autónoma, o a la Junta Arbitral de Consumo de tu comunidad; en nuestra respuesta te diremos si aceptamos la mediación o el arbitraje en tu caso. Y siempre puedes acudir a los tribunales de tu domicilio.</li>
</ul>'''),
    ('version', 'Cambios de estas condiciones', '''<p>A cada compra se le aplican las condiciones vigentes cuando la hiciste. Si las cambiamos, publicaremos la versión nueva con su fecha.</p>'''),
    ('ley', 'Ley aplicable', '''<p>Estas condiciones se rigen por la ley española. Si eres consumidor, puedes reclamar ante los tribunales de tu domicilio.</p>'''),
]

# ---------------------------------------------------------------- reventa y transferencia
REVENTA = [
    ('resumen', 'En corto', '''<p>Las entradas de Utopia Tickets son para ir al evento, no para hacer negocio con ellas. Puedes pasarle tu entrada a otra persona si el organizador lo permite, pero no revenderla por más de lo que pagaste.</p>'''),
    ('titular', 'Cambiar el nombre de una entrada', '''<ul>
<li>Si el organizador lo permite, desde el enlace «Ver pedido» de tu correo puedes cambiar el nombre y el correo de cada asistente, gratis, hasta el inicio del evento.</li>
<li>Si no ves esa opción, escribe al organizador: es él quien decide si sus entradas son nominativas y si se pueden cambiar. Corregir una errata en el nombre es siempre gratis.</li>
<li>Quien compró sigue siendo el titular del pedido: las devoluciones, si proceden, van a su medio de pago.</li>
</ul>'''),
    ('reventa', 'Reventa', '''<ul>
<li>No se permite revender entradas por encima del precio que pagaste (entrada más gastos de gestión), ni anunciarlas en webs de reventa, ni comprarlas para revenderlas. En Andalucía, la reventa no autorizada es además una infracción administrativa (Ley 13/1999 de espectáculos públicos de Andalucía).</li>
<li>Tampoco se permite comprar con programas automáticos (bots), con varias identidades para saltarse el límite de entradas por persona, ni con tarjetas que no son tuyas. Revender entradas compradas así es una práctica desleal (artículo 27.6 de la Ley 3/1991 de competencia desleal).</li>
<li>Si el organizador o Utopia detectan una reventa prohibida o una compra hecha con bots o con varias identidades, la entrada puede anularse: el organizador devuelve a quien la compró lo que pagó, en su medio de pago, y la entrada deja de valer. Si el pago fue fraudulento (por ejemplo, con una tarjeta robada), la entrada se anula y no hay nada que devolver.</li>
<li>Si compraste una entrada de reventa, no tienes garantía de que valga ni derecho a que el organizador te devuelva lo que pagaste de más: compra siempre en la página oficial del evento.</li>
</ul>'''),
    ('copias', 'Entradas duplicadas o robadas', '''<p>Cada QR solo entra una vez. Si alguien entra antes con una copia de tu entrada, la puerta no puede saber quién es el titular. Por eso no publiques tu entrada y desconfía de quien te la venda fuera de la página oficial.</p>'''),
    ('promotores', 'Para los promotores', '''<p>Las condiciones para promotores prohíben usar Utopia Tickets para revender entradas de otras plataformas por encima de su precio. Cada organizador puede limitar las entradas por pedido y hacerlas nominativas.</p>'''),
]

# ---------------------------------------------------------------- condiciones para promotores
PROMO = [
    ('partes', 'Partes y objeto', f'''<p>Estas condiciones regulan el uso de Utopia Tickets por las personas y empresas que organizan eventos y venden sus entradas en la plataforma («el promotor»). La plataforma la presta UTOPIA BOOKING S.L. («Utopia»):</p>
{EMPRESA}
<p>Utopia presta la plataforma. <strong>El promotor organiza el evento y vende las entradas en su nombre y por su cuenta</strong>; Utopia no es parte del contrato entre el promotor y sus compradores. El promotor declara que contrata y vende como empresario o profesional, no como consumidor: Utopia lo dice así a los compradores.</p>'''),
    ('alta', 'Alta, aceptación y cuenta', '''<ul>
<li><strong>Alta libre:</strong> cualquier persona mayor de edad con capacidad para contratar, o cualquier empresa a través de quien la represente, puede crear una cuenta en la plataforma. Para crearla hay que marcar la casilla de aceptación de estas condiciones y de la política de privacidad. Utopia guarda la constancia de esa aceptación: la versión aceptada, su huella, la fecha, la dirección IP y el navegador, y una copia exacta de cada versión.</li>
<li>El promotor da datos verdaderos y completos, también los de facturación, y los mantiene al día. Quien crea la cuenta en nombre de una empresa declara que puede obligarla.</li>
<li>Es responsable de las personas a las que da acceso a su cuenta y de guardar sus contraseñas. Recomendamos activar el doble factor.</li>
<li><strong>Stripe antes de vender:</strong> para publicar un evento, el promotor tiene que conectar su cuenta de Stripe, que verifica su identidad y la de su empresa. Sin ella la plataforma no deja publicar.</li>
</ul>'''),
    ('revision', 'Revisión de las altas y de los eventos', '''<ul>
<li>Utopia revisa cada alta nueva y los eventos que se publican, para proteger a los compradores y a la plataforma.</li>
<li>Puede pedir al promotor, en cualquier momento, la documentación que acredite quién es y que puede organizar el evento: NIF, escritura o poderes, contrato con el recinto o con el artista, licencias, autorización de las condiciones de admisión o seguro. Si no la entrega en el plazo que se le indique, puede pausarse la venta o suspenderse la cuenta.</li>
<li>La revisión no significa que Utopia garantice el evento ni al promotor ante los compradores.</li>
</ul>'''),
    ('suspension', 'Suspensión y cierre de cuentas', f'''<p>Utopia puede suspender una cuenta, pausar las ventas o retirar un evento concreto si hay indicios razonables de:</p>
<ul>
<li>fraude, suplantación o datos falsos;</li>
<li>un evento ilegal, inexistente, engañoso o sin los permisos necesarios;</li>
<li>que el promotor no hace las devoluciones a las que está obligado, o acumula quejas o contracargos;</li>
<li>riesgo para los compradores o para la plataforma, o el incumplimiento de estas condiciones o de la ley;</li>
<li>una orden de una autoridad.</li>
</ul>
<p>Al suspender: los eventos y la página del organizador dejan de estar publicados, se paran las ventas y se cierra el acceso a la cuenta. Utopia manda al promotor, por correo y <strong>como tarde en el momento en que la suspensión surte efecto</strong>, los motivos concretos: los hechos, la regla de estas condiciones o la norma en que se basa, y cómo puede impugnarla. Solo se omiten los hechos que la ley o una autoridad prohíban contar. El promotor puede dar sus explicaciones escribiendo a <a href="mailto:{MAIL}">{MAIL}</a>; una persona de Utopia que no tomó la decisión las revisa y le contesta en un máximo de 10 días. Si se aclara, se reactiva la cuenta sin demora, con sus datos.</p>
<p>Para cerrar del todo la cuenta, Utopia avisa con <strong>30 días</strong> de antelación y con los motivos, salvo que una obligación legal le impida esperar, que haya una razón imperiosa según la ley (por ejemplo, un fraude) o que el promotor haya incumplido estas condiciones de forma reiterada; en esos casos, le da los motivos sin demora.</p>
<p>La suspensión o el cierre no liberan al promotor de sus obligaciones con los compradores, y Utopia puede avisar a los compradores afectados y darles los datos del promotor para que le reclamen.</p>'''),
    ('evento', 'Qué hace el promotor', '''<p>El promotor es el responsable del evento y de su venta. En particular:</p>
<ul>
<li>Las licencias, permisos, comunicaciones a la autoridad, aforo y normas del recinto, y el <strong>seguro de responsabilidad civil</strong> que exija la normativa de espectáculos de su comunidad.</li>
<li>Los derechos de los artistas y de autor (SGAE u otras entidades), y los de las imágenes, logotipos y textos que publica.</li>
<li>El control de la edad mínima, el acceso de menores y la venta de alcohol en el evento, según la normativa de su comunidad.</li>
<li>La información del evento, verdadera y en la página antes de la compra: qué es, fecha, hora y lugar, precios y gastos de gestión, edad mínima y condiciones para menores (también si alguno no necesita entrada, como los bebés), accesibilidad del recinto, condiciones de admisión, si se grabará al público, y cómo, dónde y en qué plazo pedir la devolución si el evento se suspende o cambia.</li>
<li><strong>Sus datos como vendedor</strong>, a la vista del comprador antes de comprar (en la página del evento o del organizador): nombre o razón social, NIF, domicilio y un correo de atención que conteste.</li>
<li>Vender con las <a href="/utopia/legal/condiciones-de-compra.html">condiciones de compra</a> de la plataforma. Puede añadir en la página del evento condiciones propias, siempre que no empeoren esas condiciones ni los derechos legales del comprador.</li>
<li>El IVA y los demás impuestos de sus entradas, y la factura al comprador que la pida.</li>
<li>Atender a sus compradores: sus dudas, sus reclamaciones y hojas de quejas, sus <a href="#devoluciones">devoluciones</a> y sus <a href="#datos">datos personales</a>.</li>
</ul>'''),
    ('andalucia', 'Eventos en Andalucía', '''<p>Si el evento se celebra en Andalucía, el promotor cumple además la Ley 13/1999 de espectáculos públicos de Andalucía y el Decreto 10/2003 (reglamento de admisión). Lo más importante para vender entradas:</p>
<ul>
<li>La publicidad y la página del evento dicen la denominación y el domicilio del promotor, el plazo y el lugar para pedir la devolución y, si las hay, las condiciones específicas de admisión, que tienen que estar aprobadas por el ayuntamiento y expuestas en un cartel en la entrada.</li>
<li>Se devuelve el precio si el evento se suspende, se aplaza o cambia en algo sustancial, y también si se suspende ya empezado por un fallo de las instalaciones. El plazo para pedirlo va desde el anuncio hasta 4 días después de la fecha del evento, y se alarga mientras haya gente esperando su devolución.</li>
<li>Al menos el 70 % de cada clase de entrada se vende directamente al público, sin recargo ni sobreprecio. Si cobra gastos de gestión, el promotor se asegura de cumplirlo (por ejemplo, con venta en taquilla sin gastos o sin cobrar gastos).</li>
<li>Los menores de 16 años no pueden entrar en pubs, bares con música, salas de fiesta ni discotecas, salvo las de juventud. Excepción: en una actuación en directo concreta, el titular del local o el promotor puede permitirles la entrada solo mientras dure la actuación, siempre acompañados de su madre, padre o tutor o de un adulto autorizado expresamente por ellos, con el trámite que pida el ayuntamiento y anunciándolo en la página del evento (artículo 3.2 del Decreto 10/2003, en la redacción del Decreto 211/2018). Las autorizaciones y los documentos de los menores los recogen el promotor o el recinto en el acceso, como responsables de esos datos; no se piden a través de la plataforma.</li>
<li>Los menores de 3 años solo pueden estar en el evento con su madre, padre o tutor o con un adulto autorizado por ellos, que no puede ser personal del recinto, y a los menores de 18 no se les vende alcohol ni tabaco (artículos 3.4 y 3.3 del mismo reglamento).</li>
</ul>'''),
    ('cobros', 'Cobros: el dinero va a tu Stripe', '''<ul>
<li>Los cobros con tarjeta se hacen en la <strong>cuenta de Stripe del propio promotor</strong> (Stripe Connect estándar, con cargos directos). El dinero llega a su cuenta en cada venta y Stripe se lo transfiere a su banco según el calendario de pagos de su cuenta de Stripe; Utopia no lo retiene ni lo controla.</li>
<li>Las comisiones de Stripe y sus cargos por disputas las paga el promotor en su cuenta, según su contrato con Stripe.</li>
<li>Utopia no recibe ni guarda el dinero de las entradas, ni lo retiene al suspender una cuenta. Stripe puede aplicar retenciones o reservas en la cuenta del promotor según su contrato; Utopia no las controla.</li>
<li>Si el promotor permite «pagar más tarde» (taquilla o transferencia), cobra él directamente y marca el pedido como pagado.</li>
</ul>'''),
    ('tarifa', 'Tarifa de Utopia', '''<div class="price"><p class="big">0,50 € <small>+ IVA</small></p><p>por cada entrada de pago vendida.</p></div>
<ul>
<li>Las entradas gratuitas e invitaciones no pagan nada. No hay cuotas, altas ni permanencia.</li>
<li>En las ventas con tarjeta, la comisión se cobra automáticamente en cada venta: Stripe la descuenta del cobro y la ingresa a Utopia (<em>application fee</em>). Con el IVA del 21 %, son 0,61 € por entrada.</li>
<li>En las ventas de pago que el promotor cobra fuera de Stripe («pagar más tarde», taquilla o transferencia) la comisión es la misma. Utopia la factura a mes vencido y el promotor la paga por transferencia en 15 días.</li>
<li>La comisión la paga el promotor. <strong>No puede cobrársela al comprador como un recargo aparte</strong>: si quiere, la tiene en cuenta al fijar su precio.</li>
<li>Utopia puede acordar por escrito una tarifa distinta con un promotor. Cualquier cambio de la tarifa general se avisa con 30 días de antelación y el promotor puede darse de baja sin coste.</li>
</ul>'''),
    ('gastos', 'Gastos de gestión al comprador', '''<p>Si el promotor quiere cobrar gastos de gestión al comprador, los fija él y <strong>son suyos</strong>; Utopia no cobra nada de ellos. Tienen que cumplir lo que pide la Dirección General de Consumo (nota de 11 de julio de 2024):</p>
<ul>
<li>Corresponden a un servicio que recibe el comprador, no a costes del promotor, y el promotor explica en la página del evento qué incluyen.</li>
<li>Van <strong>siempre incluidos en el precio anunciado</strong>, desglosados. La plataforma lo muestra así por defecto y el promotor no lo cambia.</li>
<li>Son un importe fijo por entrada, <strong>igual para todas las entradas del evento</strong>: ni un porcentaje ni más caros en las entradas más caras, salvo que la entrada incluya un servicio adicional que lo justifique.</li>
<li>No son más caros que los que pague quien compra en persona, salvo servicio adicional.</li>
<li>No se cobra nada por imprimir la entrada, por guardarla en el móvil ni por corregir una errata en el nombre.</li>
</ul>
<p>Utopia puede pedir que se corrijan y, si no se corrigen, pausar la venta del evento.</p>'''),
    ('devoluciones', 'Devoluciones y contracargos', '''<ul>
<li>El comprador pide las devoluciones <strong>al promotor</strong>, que las hace desde el panel. El reembolso sale de su cuenta de Stripe.</li>
<li>Si el evento se cancela, o se suspende ya empezado por un fallo de las instalaciones o por una causa que dependa del promotor, el promotor devuelve a cada comprador todo lo que pagó, gastos de gestión incluidos, en un máximo de 14 días y sin que se lo pidan.</li>
<li>Si se aplaza, cambia de recinto, cambia el artista principal o cambia en algo esencial (por ejemplo, la hora de comienzo en más de dos horas), devuelve todo a quien lo pida desde el anuncio hasta 4 días después de la fecha del evento (la nueva, si se aplaza) y, en todo caso, durante al menos 15 días desde el aviso. Si se aplaza sin nueva fecha y en 90 días no la ha anunciado, se trata como una cancelación.</li>
<li>Avisa de cualquier cambio a los compradores en cuanto lo sepa, con el correo de la plataforma.</li>
<li>Si un comprador no pudo entrar por una condición de edad o de admisión que no estaba en la página antes de la compra, le devuelve lo que pagó.</li>
<li>Fuera de esos casos, las devoluciones son voluntarias del promotor. Si tiene una política de devoluciones más generosa, la publica en la página del evento y no la empeora para quien ya compró. Contesta a las peticiones de los compradores en un máximo de 5 días hábiles, y a las hojas de quejas y reclamaciones en el plazo que fije su comunidad (en Andalucía, 10 días hábiles).</li>
<li><strong>La comisión de Utopia no se devuelve nunca</strong>, tampoco si el evento se cancela o el promotor devuelve una entrada: el servicio de venta ya se prestó. Stripe tampoco devuelve su comisión.</li>
<li>Los contracargos y disputas de los compradores son del promotor y se gestionan en su cuenta de Stripe. Utopia le facilita los datos de la venta y del acceso para defenderlos.</li>
<li>Si el promotor no atiende las devoluciones a las que está obligado, Utopia puede suspender sus ventas y avisar a los compradores (ver <a href="#suspension">suspensión</a>). Utopia no garantiza ni adelanta devoluciones; si aun así paga o asume algún importe por cuenta del promotor, este se lo devuelve en 15 días desde que se le pida.</li>
</ul>'''),
    ('factura', 'Factura mensual de la comisión', '''<p>El día 1 de cada mes, Utopia emite al promotor una factura con las comisiones de las entradas vendidas el mes anterior, con su IVA, y se la envía por correo. La parte de las ventas con tarjeta sale ya <strong>cobrada</strong>, porque la comisión se descontó en cada venta; la de las ventas cobradas fuera de Stripe sale pendiente de pago. Los datos de facturación son los de la cuenta del promotor. Si el promotor no está de acuerdo con una factura, lo dice en los 15 días siguientes a recibirla.</p>
<p>Impuestos: la comisión lleva el IVA español del 21 %. Si el promotor es una empresa de otro país de la UE con NIF-IVA válido, se factura sin IVA por inversión del sujeto pasivo. El IVA y los impuestos de las entradas son del promotor.</p>'''),
    ('comunicaciones', 'Comunicaciones con los compradores', '''<ul>
<li>El promotor puede escribir a sus compradores desde el panel sobre su pedido y su evento (cambios, horarios, accesos).</li>
<li>Solo puede mandarles publicidad si el comprador marcó la casilla de novedades al comprar o en los demás casos que permite el artículo 21 de la LSSI, identificándose y siempre con una forma sencilla de darse de baja que respete. Es el responsable de esos envíos.</li>
<li>Utopia puede limitar o revisar los envíos masivos para evitar el spam y proteger la entrega de los correos de todos.</li>
</ul>'''),
    ('datos', 'Datos personales de los compradores', '''<p>El promotor es el <strong>responsable</strong> de los datos de sus compradores y asistentes, y Utopia es su <strong>encargada del tratamiento</strong>. El encargo se rige por el <a href="#anexo">anexo</a> de estas condiciones (artículo 28 del RGPD), que el promotor acepta al aceptar estas condiciones; aceptado por medios electrónicos, vale como contrato escrito (artículo 28.9 del RGPD). Si el promotor prefiere firmarlo aparte, Utopia se lo manda con el mismo contenido.</p>
<p>Utopia es responsable propia, y no encargada, solo de tres cosas: la seguridad y la prevención del fraude de la plataforma, atender las reclamaciones y los avisos de contenidos ilícitos que reciba, y sus propias obligaciones legales. Lo explica su <a href="/utopia/legal/privacidad.html">política de privacidad</a>.</p>'''),
    ('uso', 'Uso aceptable y prohibiciones', '''<p>No se puede usar Utopia Tickets para:</p>
<ul>
<li>eventos ilegales, inexistentes o engañosos, o sin los permisos necesarios;</li>
<li>revender entradas de otras plataformas o de otros organizadores por encima de su precio;</li>
<li>vender algo que no sea una entrada o un servicio ligado al evento;</li>
<li>contenidos que inciten al odio o la violencia, discriminen, vulneren derechos de terceros o sean sexualmente explícitos;</li>
<li>recoger datos de los compradores con otros fines o enviar comunicaciones comerciales sin consentimiento;</li>
<li>suplantar a otra persona o empresa, blanquear dinero o cualquier otro fraude;</li>
<li>atacar, sobrecargar o intentar saltarse la seguridad de la plataforma.</li>
</ul>
<p>Utopia puede comunicar los indicios de fraude a las autoridades, con los datos del promotor, cuando la ley lo permita o lo exija.</p>'''),
    ('moderacion', 'Cómo revisamos los contenidos', f'''<ul>
<li>Revisamos los eventos y atendemos los avisos de contenidos ilícitos que recibimos en <a href="mailto:{MAIL}">{MAIL}</a>. Lo decide siempre una persona. Las únicas herramientas automáticas son las de seguridad: la protección frente a bots de Cloudflare y el antifraude de los pagos de Stripe.</li>
<li>Podemos retirar o despublicar un evento o un contenido que incumpla la ley o estas condiciones, pausar sus ventas o <a href="#suspension">suspender la cuenta</a>. Lo hacemos con proporción: primero lo menos grave que resuelva el problema.</li>
<li>Cada vez, le mandamos al promotor una explicación con lo que hemos decidido, los hechos, si vino de un aviso de un tercero, la regla o la norma en que nos basamos, si se usaron medios automáticos, y cómo puede impugnarlo: pidiéndonos que lo revisemos, respondiendo a ese correo, o ante los tribunales.</li>
</ul>'''),
    ('trato', 'Igualdad de trato, orden de los eventos y datos', '''<ul>
<li><strong>Orden:</strong> no hay un buscador ni un listado común de eventos de varios promotores. Cada promotor tiene su página, con sus eventos ordenados por fecha. Nadie paga por salir antes.</li>
<li><strong>Igualdad de trato:</strong> Utopia también vende entradas de sus propios eventos, sin pagarse la tarifa a sí misma, y puede acordar tarifas distintas con algunos promotores (ver <a href="#tarifa">tarifa</a>). Fuera de eso, todos los promotores tienen las mismas funciones y la misma visibilidad, y Utopia no usa los datos de ventas de un promotor para sus propios eventos ni para los de otro.</li>
<li><strong>Datos:</strong> el promotor ve y puede exportar en cualquier momento los datos de sus pedidos, compradores y asistentes. Utopia accede a ellos solo como encargada (ver <a href="#datos">datos</a>) y, para su propia gestión, a datos agregados de uso de la plataforma, que no comparte con otros promotores. Los datos de los cobros están en la cuenta de Stripe del promotor.</li>
<li><strong>Otros canales:</strong> el promotor puede vender sus entradas también por otros canales y con otras condiciones. Utopia no difunde sus eventos en otros sitios ni programas de socios, salvo lo dicho en <a href="#marca">marca</a>.</li>
</ul>'''),
    ('marca', 'Marca, contenidos e imagen', '''<ul>
<li>Las páginas, entradas y correos llevan la marca Utopia Tickets y el aviso «Powered by Utopia Tickets based on Hi.Events», que el promotor no puede quitar. El promotor puede poner su logotipo, sus colores y sus textos en sus eventos.</li>
<li>El promotor sigue siendo el dueño de sus contenidos. Da a Utopia permiso gratuito y no exclusivo para mostrar sus logotipos, carteles, imágenes, nombres de artistas y textos en la plataforma y en la difusión de sus eventos, mientras el evento esté publicado y hasta 12 meses después. Garantiza que tiene los derechos de todo lo que publica, también los de imagen de los artistas. Utopia puede retirar un contenido si alguien alega de forma creíble que infringe sus derechos (ver <a href="#moderacion">revisión de contenidos</a>).</li>
<li>Utopia puede citar al promotor como cliente, con su nombre y su logotipo, salvo que el promotor le pida que no lo haga.</li>
</ul>'''),
    ('responsabilidad', 'Disponibilidad, responsabilidad e indemnidad', '''<ul>
<li>Utopia pone los medios razonables para que la plataforma funcione sin cortes, y avisa con antelación de las paradas previstas.</li>
<li>Utopia no responde de la celebración del evento, de las decisiones del promotor ni de las de Stripe, ni del lucro cesante o la pérdida de ventas por una caída del servicio.</li>
<li>Ninguna de las partes responde de los incumplimientos causados por fuerza mayor (catástrofes, órdenes de la autoridad, epidemias, fallos generales de suministro, de internet o de los proveedores de pago). La fuerza mayor no exime al promotor de devolver las entradas de un evento que no se celebra.</li>
<li>La responsabilidad total de Utopia frente al promotor se limita a las comisiones que le haya cobrado en los 12 meses anteriores al hecho. Este límite y la exclusión del lucro cesante no se aplican en caso de dolo o culpa grave, a los daños a las personas ni a lo que la ley no permita limitar.</li>
<li>El promotor mantendrá a Utopia indemne de cualquier reclamación, sanción, daño o gasto (incluidos los honorarios razonables de abogado) de terceros, como compradores, artistas, recintos, entidades de gestión o autoridades, que nazca de sus eventos, de sus contenidos, de su trato con los compradores o del incumplimiento de estas condiciones o de la ley, salvo dolo o culpa grave de Utopia. Utopia le avisará de la reclamación en cuanto la conozca, le dejará participar en su defensa y no pagará nada a su cargo sin consultarle, salvo resolución firme o requerimiento de una autoridad.</li>
</ul>'''),
    ('baja', 'Duración y baja', '''<p>El contrato no tiene plazo. El promotor puede darse de baja cuando quiera, después de celebrar o cancelar (con sus devoluciones) los eventos que tenga a la venta. Utopia puede terminarlo como se explica en <a href="#suspension">suspensión y cierre</a>. Al terminar, el promotor puede exportar sus datos durante 90 días y después Utopia devuelve o borra los datos de los compradores según el <a href="#anexo">anexo</a>, y conserva lo que exija la ley.</p>'''),
    ('cambios', 'Cambios de estas condiciones', '''<p>Utopia avisará por correo de cualquier cambio con 30 días de antelación y guardará cada versión con su fecha. Si el promotor no está de acuerdo, puede darse de baja sin coste antes de que entre en vigor; si sigue usando la plataforma después, se entiende que acepta la versión nueva. Ningún cambio se aplica hacia atrás. Los cambios exigidos por la ley pueden aplicarse antes.</p>'''),
    ('varios', 'Avisos y otras reglas', '''<ul>
<li>Los avisos entre las partes se hacen por correo electrónico: al correo de la cuenta del promotor y a la dirección de Utopia de estas condiciones.</li>
<li>Si una cláusula fuera nula, el resto sigue valiendo. Que Utopia no exija una obligación en un momento dado no significa que renuncie a ella.</li>
<li>Si hay una traducción de estas condiciones, manda la versión en español.</li>
<li>El promotor no puede ceder este contrato sin el permiso de Utopia. Utopia puede cederlo a otra empresa que continúe el servicio, avisando al promotor con 30 días; si no está de acuerdo, puede darse de baja sin coste.</li>
</ul>'''),
    ('ley', 'Ley y tribunales', '''<p>Estas condiciones se rigen por la ley española. Los conflictos se resolverán en los juzgados y tribunales que correspondan según la ley.</p>'''),
    ('anexo', 'Anexo: encargo del tratamiento (art. 28 RGPD)', '''<p>Este anexo forma parte de las condiciones y lo acepta el promotor («responsable») al aceptarlas. UTOPIA BOOKING S.L. es la «encargada».</p>
<ul>
<li><strong>Objeto:</strong> Utopia trata los datos de los compradores y asistentes del promotor solo para prestarle la plataforma: venta, envío de entradas y correos, control de acceso, devoluciones, soporte y prevención del fraude en sus ventas.</li>
<li><strong>Duración:</strong> la del contrato.</li>
<li><strong>Datos y personas:</strong> identificativos y de contacto, pedidos, respuestas a preguntas del evento y registros de acceso de compradores y asistentes. No se tratan categorías especiales de datos salvo que el promotor las pida en sus preguntas, cosa que debe evitar.</li>
<li><strong>Instrucciones:</strong> Utopia solo trata los datos según las instrucciones documentadas del promotor, que son estas condiciones y la configuración de sus eventos. Si una instrucción le parece contraria al RGPD, se lo dice al promotor.</li>
<li><strong>Confidencialidad y seguridad:</strong> quien accede a los datos está obligado a guardar secreto. Medidas: cifrado en tránsito (HTTPS y túnel cifrado), contraseñas cifradas, panel de administración no accesible desde internet, acceso mínimo, cortafuegos, copias diarias cifradas y registros de acceso. La plataforma funciona en un servidor propio de Utopia en España.</li>
<li><strong>Subencargados autorizados:</strong> Cloudflare, Inc. (túnel, cortafuegos y protección frente a bots; EE. UU., con el Marco de Privacidad de Datos UE-EE. UU. y cláusulas tipo) y Brevo SAS (envío de los correos; Francia, con servidores en la UE). Utopia les impone las mismas obligaciones y avisará de cualquier cambio con 30 días para que el promotor pueda oponerse. Stripe trata los datos de pago según su propio contrato con el promotor.</li>
<li><strong>Transferencias internacionales:</strong> solo las de los subencargados citados, con las garantías indicadas. Al aceptar estas condiciones, el promotor da la instrucción documentada de hacerlas.</li>
<li><strong>Derechos de los interesados:</strong> Utopia pasa al promotor, en un máximo de 5 días, cualquier petición que reciba y le ayuda a atenderla.</li>
<li><strong>Brechas:</strong> Utopia avisa al promotor sin dilación indebida, y como muy tarde en 48 horas desde que la conozca, con la información que tenga, y le ayuda a notificarla.</li>
<li><strong>Ayuda al responsable:</strong> Utopia le ayuda, con la información de que disponga, en las evaluaciones de impacto y consultas previas que necesite, y lleva el registro de las actividades que trata por cuenta de los promotores.</li>
<li><strong>Fin del encargo:</strong> el promotor puede exportar sus datos desde el panel. Después, Utopia los borra en 90 días, salvo lo que deba guardar por ley, bloqueado.</li>
<li><strong>Auditoría:</strong> Utopia pone a disposición del promotor la información necesaria para demostrar que cumple este anexo y permite las auditorías razonables que pida, con aviso previo y a su cargo.</li>
</ul>'''),
]

# ---------------------------------------------------------------- índice legal
LEGAL_INDEX = '''<ul class="cards">
<li><a href="/utopia/legal/aviso-legal.html"><strong>Aviso legal</strong><span>Quién somos y cómo funciona el sitio.</span></a></li>
<li><a href="/utopia/legal/condiciones-de-compra.html"><strong>Condiciones de compra</strong><span>Para quien compra entradas: precio, entrada, cancelaciones y devoluciones.</span></a></li>
<li><a href="/utopia/legal/reventa-y-transferencia.html"><strong>Reventa y transferencia</strong><span>Cambiar el nombre de una entrada y qué no se permite.</span></a></li>
<li><a href="/utopia/legal/condiciones-promotores.html"><strong>Condiciones para promotores</strong><span>Alta, tarifa, cobros, devoluciones, suspensión y datos (con el anexo de encargo del tratamiento).</span></a></li>
<li><a href="/utopia/legal/privacidad.html"><strong>Privacidad</strong><span>Qué datos se tratan, quién y para qué.</span></a></li>
<li><a href="/utopia/legal/cookies.html"><strong>Cookies</strong><span>Solo las imprescindibles.</span></a></li>
<li><a href="/utopia/legal/condiciones-de-compra.html#reclamaciones"><strong>Reclamaciones</strong><span>Hojas de quejas y reclamaciones, y cómo reclamar.</span></a></li>
<li><a href="/utopia/legal/aviso-legal.html#contenidos"><strong>Avisar de un contenido ilícito</strong><span>Un evento falso, una estafa o algo que vulnera tus derechos.</span></a></li>
</ul>'''


# ---------------------------------------------------------------- ayuda
AYUDA = [
    ('perdi', '¿Dónde están mis entradas?', '''<p>Te llegaron por correo justo después de pagar, en un mensaje con el asunto «🎟️ Tu entrada para…» o «Tus entradas para…». Si no lo encuentras:</p>
<ol>
<li>Busca en spam o en «Promociones» el remitente <strong>Utopia Tickets</strong>.</li>
<li>Pide que te las reenviemos: entra en <a href="/auth/login">«¿Solo buscas tus entradas?»</a>, escribe el correo con el que compraste y te mandamos un enlace a todas tus entradas.</li>
<li>Si aun así no aparecen, escribe al organizador del evento.</li>
</ol>'''),
    ('imprimir', '¿Tengo que imprimirla?', '''<p>No. Enseña el QR en el móvil, con el brillo alto. Si prefieres papel, abre la entrada y pulsa «Imprimir». Cada QR vale una sola vez.</p>'''),
    ('nombre', '¿Puedo cambiar el nombre de una entrada?', '''<p>Si el organizador lo permite, desde el enlace «Ver pedido» de tu correo puedes cambiar el nombre y el correo de cada asistente. Si no ves esa opción, escribe al organizador. Revender por encima del precio no está permitido: mira la <a href="/utopia/legal/reventa-y-transferencia.html">política de reventa y transferencia</a>.</p>'''),
    ('devolucion', '¿Me devuelven el dinero si no puedo ir?', '''<p>Las entradas no tienen derecho de desistimiento, así que no se devuelven por cambiar de planes. Si el evento se <strong>cancela</strong>, el organizador te devuelve todo, gastos incluidos, sin que lo pidas. Si se <strong>aplaza, cambia de lugar o cambia el artista principal</strong> y no te interesa, pide la devolución al organizador: tienes hasta 4 días después de la fecha del evento (y al menos 15 días desde el aviso). Detalle en las <a href="/utopia/legal/condiciones-de-compra.html#cambios">condiciones de compra</a>.</p>'''),
    ('quien', '¿Quién me vende la entrada?', '''<p>El organizador del evento, que aparece en su página y en tu correo. Utopia Tickets es la plataforma de venta: el dinero va directamente al organizador.</p>'''),
    ('pago', 'Problemas con el pago', '''<ul>
<li>Si tu banco pide una comprobación (3D Secure), termina el paso en la app del banco y vuelve a la página.</li>
<li>Si el pago falla, no se cobra nada y puedes volver a intentarlo. Si ves un cargo sin correo de confirmación, espera unos minutos: si no llega, escríbenos con la hora y el importe.</li>
<li>Para la factura de tu entrada, pídela al organizador.</li>
</ul>'''),
    ('puerta', 'En la puerta', '''<p>Lleva la entrada a mano y el documento de identidad. Si tu QR sale como «ya usado», díselo al personal de la puerta: comprobarán a qué hora se escaneó.</p>'''),
    ('accesible', 'Accesibilidad', '''<p>Si necesitas plaza adaptada, acompañante o ayuda para comprar, escribe al organizador antes del evento. Si encuentras una barrera en la web, cuéntanoslo.</p>'''),
    ('contacto', 'Contacto', f'''<ul>
<li><strong>Sobre un evento</strong> (horarios, accesos, devoluciones): el organizador. Su correo está en la página del evento y en tus correos.</li>
<li><strong>Sobre la web o el pago:</strong> <a href="mailto:{MAIL}">{MAIL}</a> · {TEL} · UTOPIA BOOKING S.L., Ctra. de Alomartes 27, 1.º B, 18260 Íllora (Granada). Contestamos como máximo en 10 días.</li>
<li><strong>Hojas de quejas y reclamaciones:</strong> existen hojas de quejas y reclamaciones a tu disposición. Pídenoslas en ese correo o en esa dirección, en papel o en formato electrónico, o al organizador. Más en <a href="/utopia/legal/condiciones-de-compra.html#reclamaciones">reclamaciones</a>.</li>
<li><strong>Para avisar de un evento falso o de un contenido ilícito:</strong> mira <a href="/utopia/legal/aviso-legal.html#contenidos">cómo avisarnos</a>.</li>
</ul>'''),
]

# ---------------------------------------------------------------- promotores (captación)
# Coste de Stripe por entrada de ejemplo (con 2,17 entradas por pedido) y comisión con IVA medida en una compra de prueba.
EJ = [(10, 0.27), (18, 0.39), (30, 0.57)]
COM_IVA = 0.61
def fila(p, stripe):
    rec = p - stripe - COM_IVA
    f = lambda x: f'{x:,.2f} €'.replace('.', ',')
    return f'<tr><td>{f(p)}</td><td>{f(stripe)}</td><td>{f(COM_IVA)}</td><td><strong>{f(rec)}</strong></td></tr>'

PROMO_HOME = f'''<section class="hero">
<p class="kicker">Para promotores, salas y artistas</p>
<p class="claim">Vende tus entradas con tu marca. <span>Cobra al momento.</span></p>
<p>El dinero de cada entrada llega a tu propia cuenta de Stripe en el momento de la venta. Nosotros solo cobramos 0,50 € + IVA por entrada de pago.</p>
<p class="ctas"><a class="btn" href="/auth/register">Crear mi cuenta gratis</a> <a class="btn btn-ghost" href="/utopia/promotores/guia.html">Ver la guía</a></p>
</section>

<h2 id="tarifa">Una tarifa, sin letra pequeña</h2>
<div class="price"><p class="big">0,50 € <small>+ IVA</small></p><p>por entrada de pago. Entradas gratis e invitaciones: 0 €. Sin cuotas ni permanencia.</p></div>
<ul class="ticks">
<li><strong>Tus gastos de gestión son tuyos.</strong> Si quieres cobrar gastos al comprador, los pones tú (fijos e incluidos en el precio, como pide Consumo) y te los quedas enteros.</li>
<li><strong>Cobras en cada venta,</strong> no días después del evento: el dinero va a tu Stripe.</li>
<li><strong>Tus datos son tuyos:</strong> compradores, asistentes y ventas, exportables cuando quieras.</li>
<li><strong>Software libre</strong> (Hi.Events), sin cajas negras.</li>
</ul>

<h2 id="ejemplo">Cuánto te queda de cada entrada</h2>
<p>Ejemplo sin gastos de gestión al comprador, pagando con tarjeta europea (Stripe: 1,5 % + 0,25 € por pedido, repartido entre una media de 2,17 entradas por pedido, la de nuestra última gira).</p>
<div class="tablewrap"><table>
<thead><tr><th>Precio</th><th>Stripe</th><th>Utopia con IVA</th><th>Te queda</th></tr></thead>
<tbody>
{''.join(fila(p, s) for p, s in EJ)}
</tbody></table></div>
<p>Stripe es aproximado. Si tu empresa recupera el IVA, el IVA de la comisión (0,11 €) lo deduces, así que en realidad te cuesta 0,50 €.</p>
<p class="note">Lo habitual en las salas de Granada es que la tiquetera cobre un 10 % al comprador: 1 € en una entrada de 10 € y 3 € en una de 30 €. Con Utopia Tickets puedes no cobrar nada al comprador, o poner tus propios gastos.</p>

<h2 id="incluye">Qué incluye</h2>
<ul class="cards">
<li><div><strong>Página del evento y widget</strong><span>Con tu logo y tus colores, y un botón para tu web.</span></div></li>
<li><div><strong>Entradas con QR por correo</strong><span>En español, con tu evento y, si quieres, tu logo.</span></div></li>
<li><div><strong>Control de acceso con el móvil</strong><span>Listas por puerta, sin instalar nada.</span></div></li>
<li><div><strong>Invitaciones y RR. PP.</strong><span>Entradas ocultas, códigos y enlaces de afiliado.</span></div></li>
<li><div><strong>Varias entradas y cupos</strong><span>General, Meet&amp;Greet, aforos compartidos.</span></div></li>
<li><div><strong>Lista de espera y mensajes</strong><span>Escribe a tus asistentes desde el panel.</span></div></li>
</ul>

<h2 id="como">Cómo empezar</h2>
<ol class="steps">
<li><a href="/auth/register">Crea tu cuenta</a> en dos minutos y acepta las condiciones. Confirma tu correo.</li>
<li>Conecta tu cuenta de Stripe (o crea una) desde el panel. Sin Stripe no se puede publicar.</li>
<li>Crea tu evento, tus entradas y tus gastos de gestión.</li>
<li>Publícalo y comparte el enlace o el widget.</li>
</ol>
<p>Revisamos cada alta nueva para proteger a los compradores; si necesitamos algo, te escribimos. Lee la <a href="/utopia/promotores/guia.html">guía paso a paso</a> y las <a href="/utopia/legal/condiciones-promotores.html">condiciones para promotores</a>. ¿Dudas antes de empezar? Escríbenos a <a href="mailto:{MAIL}">{MAIL}</a>.</p>'''

# ---------------------------------------------------------------- guía del promotor
GUIA = [
    ('cuenta', 'Tu cuenta', '''<ol>
<li>Entra en <a href="/auth/register">Crear cuenta</a>, rellena tus datos y marca la casilla de aceptación de las <a href="/utopia/legal/condiciones-promotores.html">condiciones para promotores</a> y la privacidad: sin ella no se crea la cuenta.</li>
<li>Te llega un correo para confirmar tu dirección: ábrelo, porque sin confirmar no puedes publicar eventos.</li>
<li>Utopia revisa cada alta nueva. Si necesitamos algún dato o documento (NIF, contrato con la sala…), te escribimos.</li>
<li>Entra en <a href="/auth/login">el panel</a> y activa el doble factor en tu perfil.</li>
<li>En <em>Organizador</em> pon tu nombre comercial, tu logotipo, tus colores y tu correo de atención: es lo que verán tus compradores.</li>
</ol>'''),
    ('stripe', 'Conecta tu Stripe', '''<ol>
<li>En el panel, <em>Organizador → Pagos → Conectar con Stripe</em>.</li>
<li>Inicia sesión en tu Stripe o crea una cuenta con los datos de tu empresa (NIF, administrador, IBAN). Stripe te pedirá verificar tu identidad.</li>
<li>Al volver, la tiquetera muestra la cuenta conectada. Desde ese momento, lo que vendas cae en tu Stripe. <strong>Sin Stripe conectado no puedes publicar ningún evento</strong>, tampoco uno gratuito o con «pagar más tarde».</li>
<li>En <em>IVA</em>, indica que eres empresa española: la comisión de Utopia lleva el 21 % y te sale en la factura mensual.</li>
</ol>'''),
    ('evento', 'Tu primer evento', '''<ol>
<li><em>Crear evento</em>: título, fecha y hora, recinto y descripción. Sube una portada horizontal (por ejemplo, 1600 × 900).</li>
<li><em>Entradas</em>: crea cada tipo (General, Meet&amp;Greet…), su precio con IVA incluido y su cupo. Para invitaciones, crea una entrada gratuita y márcala como oculta.</li>
<li><em>Capacidad</em>: si todas las entradas comparten el aforo, crea una asignación de capacidad con el total.</li>
<li><em>Ajustes → Pago</em>: deja activo Stripe. Si vas a vender en taquilla, activa también «pagar más tarde» con instrucciones.</li>
<li><em>Ajustes → Página</em>: preguntas frecuentes (hora de puertas, edad mínima y menores, condiciones de admisión, accesibilidad, si se grabará al público, cómo pedir la devolución si el evento cambia) y tus datos como vendedor: nombre o razón social, NIF, domicilio y correo de atención. Son obligatorios: lo dicen las <a href="/utopia/legal/condiciones-promotores.html#evento">condiciones</a>.</li>
<li>Revisa la vista previa en el móvil y publícalo.</li>
</ol>'''),
    ('gastos', 'Gastos de gestión', '''<p>Son tuyos. Créalos en <em>Cuenta → Impuestos y tarifas</em> como «Tarifa» de importe fijo (por ejemplo, 1 €) y asígnalos a todas las entradas del evento. Reglas (nota de Consumo de julio de 2024, recogidas en las <a href="/utopia/legal/condiciones-promotores.html#gastos">condiciones</a>):</p>
<ul>
<li>El mismo importe fijo para todas las entradas del evento, nunca un porcentaje.</li>
<li>Siempre incluidos en el precio que se anuncia: deja la opción de mostrar el precio con los gastos incluidos.</li>
<li>Explica en la página del evento qué incluyen, y que no sean más caros que comprar en persona.</li>
<li>Si el evento es en Andalucía, al menos el 70 % de cada clase de entrada se tiene que vender sin recargo (por ejemplo, en taquilla sin gastos).</li>
</ul>
<p>La comisión de Utopia no se cobra al comprador como recargo aparte: la pagas tú y te sale en la factura mensual.</p>'''),
    ('vender', 'Vender y difundir', '''<ul>
<li>Comparte el enlace del evento o pega el <em>widget</em> en tu web.</li>
<li>Para RR. PP., crea un afiliado por persona: cada uno tiene su enlace y ves cuánto vende.</li>
<li>Para descuentos, crea códigos promocionales.</li>
<li>Si se agota, activa la lista de espera.</li>
</ul>'''),
    ('taquilla', 'Taquilla el día del evento', '''<p>La versión gratuita no trae el módulo de taquilla, pero puedes vender en la puerta así (las entradas de pago que vendas así también llevan la comisión de 0,50 € + IVA, que te facturamos a mes vencido):</p>
<ul>
<li>Con el móvil, compra desde la página del evento eligiendo «pagar más tarde», cobra en efectivo o con tu datáfono y marca el pedido como pagado en el panel.</li>
<li>O, desde <em>Asistentes → Añadir</em>, crea la entrada a nombre del comprador y márcala como pagada.</li>
</ul>'''),
    ('puerta', 'Control de acceso en la puerta', '''<ol>
<li>En <em>Check-in</em>, crea una lista por puerta (por ejemplo, «Puerta principal» y «Meet&amp;Greet»).</li>
<li>Comparte el enlace de cada lista con quien esté en la puerta: se abre en el móvil, sin cuenta ni app.</li>
<li>Escanea con la cámara. Si un QR ya se usó, sale el aviso «ya está registrado»; en la lista de recientes ves cuándo entró.</li>
<li>Hace falta conexión: lleva un router 4G o usa el wifi del recinto. Prueba la lista antes de abrir puertas.</li>
</ol>'''),
    ('devoluciones', 'Devoluciones', '''<ul>
<li>Desde <em>Pedidos</em>, abre el pedido y pulsa <em>Reembolsar</em>. Puedes devolver todo o una parte.</li>
<li>Si cancelas el evento, devuelve todos los pedidos, gastos incluidos, en 14 días como máximo.</li>
<li>Si lo aplazas, cambias de recinto o de artista principal, devuelve todo a quien lo pida hasta 4 días después de la fecha del evento (y al menos durante 15 días desde tu aviso). Avisa a tus compradores desde el panel en cuanto lo sepas.</li>
<li>La comisión de Utopia no se devuelve, ni Stripe devuelve la suya.</li>
<li>Los contracargos te llegan a tu Stripe; responde allí con la prueba (correo de la entrada y escaneo en la puerta).</li>
</ul>'''),
    ('factura', 'Tu factura mensual', '''<p>El día 1 te llega por correo la factura de Utopia con las comisiones del mes anterior: entradas vendidas, base, IVA y total. Tiene dos partes:</p>
<ul>
<li><strong>Ventas con tarjeta</strong>: sale cobrada, porque ya se descontó en cada venta; en tu Stripe ves cada comisión como <em>application fee</em>.</li>
<li><strong>Entradas de pago que cobraste fuera de Stripe</strong> («pagar más tarde» que marcaste como pagado, o «Añadir asistente» con importe): sale pendiente de pago. La pagas por transferencia en los 15 días siguientes (antes del día 16), con el número de la factura como referencia. Cuentan en el mes en que marcas el pedido como pagado.</li>
</ul>
<p>Las entradas gratuitas y las invitaciones no pagan nada.</p>
<p>Si algo no encaja con las condiciones, Utopia puede suspender la cuenta: se despublican los eventos y se cierra el acceso, y te escribimos con el motivo para que puedas explicarte.</p>'''),
    ('ayuda', '¿Dudas?', f'''<p>Escríbenos a <a href="mailto:{MAIL}">{MAIL}</a> o llama al {TEL}.</p>'''),
]

def _sec(path, title, desc, items, lead, current='/utopia/legal/', kind='legal'):
    toc, body = secciones(items)
    return dict(path=path, title=title, desc=desc, body=body, toc=toc, lead=lead, current=current, kind=kind)

PAGINAS = [
    dict(path='legal/index.html', title='Información legal', desc='Aviso legal, condiciones, privacidad y cookies de Utopia Tickets.',
         body=LEGAL_INDEX, lead='Todo lo legal de Utopia Tickets, en lenguaje claro.', current='/utopia/legal/'),
    _sec('legal/aviso-legal.html', 'Aviso legal', 'Datos de UTOPIA BOOKING S.L. y condiciones de uso de Utopia Tickets.', AVISO,
         'Quién está detrás de Utopia Tickets y qué reglas tiene el sitio.'),
    _sec('legal/privacidad.html', 'Privacidad', 'Cómo trata Utopia Tickets los datos de compradores y promotores.', PRIV,
         'Qué datos se tratan, quién los trata y para qué.'),
    _sec('legal/cookies.html', 'Cookies', 'Las cookies de Utopia Tickets: solo las imprescindibles.', COOKIES,
         'Solo usamos las imprescindibles.'),
    _sec('legal/condiciones-de-compra.html', 'Condiciones de compra', 'Condiciones de compra de entradas en Utopia Tickets.', COMPRA,
         'Qué compras, quién te lo vende y qué pasa si algo cambia. Cómo se tratan tus datos: <a href="/utopia/legal/privacidad.html">privacidad</a>.'),
    _sec('legal/reventa-y-transferencia.html', 'Reventa y transferencia', 'Política de reventa y cambio de titular de las entradas de Utopia Tickets.', REVENTA,
         'Cómo pasar tu entrada a otra persona y qué no se permite.'),
    _sec('legal/condiciones-promotores.html', 'Condiciones para promotores', 'Tarifa, cobros, devoluciones y datos para promotores de Utopia Tickets.', PROMO,
         'Para quien organiza eventos y vende sus entradas en Utopia Tickets. Se aceptan al crear la cuenta.'),
    dict(path='promotores/index.html', title='Vende tus entradas con Utopia Tickets', desc='Tiquetera para promotores: 0,50 € + IVA por entrada y el dinero en tu Stripe al momento.',
         body=PROMO_HOME, lead=None, meta=False, current='/utopia/promotores/', kind='promo'),
    _sec('promotores/guia.html', 'Guía del promotor', 'Paso a paso para vender entradas con Utopia Tickets.', GUIA,
         'De la cuenta a la puerta, paso a paso.', current='/utopia/promotores/', kind='promo'),
    _sec('ayuda/index.html', 'Ayuda', 'Ayuda para compradores de Utopia Tickets: entradas, devoluciones y contacto.', AYUDA,
         'Respuestas rápidas para quien compra entradas.', current='/utopia/ayuda/', kind='promo'),
]
