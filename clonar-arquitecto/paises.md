# Países: pagos, facturación, moneda y atención

**Revisado el 2026-10-22 con fuentes oficiales** (la lista está al final). Los
datos que solo se pudieron confirmar en fuentes secundarias están marcados.

Referencia para lanzar en países hispanohablantes. La leen clonar-arquitecto,
clonar-backend y clonar-lanzar después de preguntar en qué país o países se
va a lanzar la app.

**Esta información cambia con el tiempo.** Es un punto de partida, no asesoría
legal, fiscal ni financiera. Antes de decidir, el usuario debe verificar cada
dato con el proveedor de pagos, la autoridad tributaria del país y un contador
local. Si un dato de aquí no coincide con la fuente oficial, manda la fuente
oficial.

Para actualizarlo, edita solo este archivo y cambia la fecha de revisión de
arriba: las tres skills lo leen desde aquí.

## Cómo se usa

1. Pregunta en qué país o países se va a lanzar la app, y si después se piensa
   abrir a otros.
2. Lee aquí cada país de la respuesta. Si un país no está, busca su autoridad
   tributaria y sus métodos de pago más usados, y dilo.
3. Escribe el resultado en la sección **Países** de `clonar/architecture.md`:
   por país, la moneda, los métodos de pago y la pasarela, la facturación
   electrónica, el impuesto que se muestra en el precio y si WhatsApp será
   canal de atención.
4. Recuérdale al usuario que lo verifique, y que confirme la facturación con un
   contador local antes del lanzamiento.

## Cobrar en uno o en varios países

- **Un país**: usa la pasarela local o Stripe si está disponible ahí, con los
  métodos que la gente de ese país usa de verdad, no solo tarjeta.
- **Varios países a la vez**, con una sola integración:
  - Pasarelas regionales con métodos locales en muchos países. Según sus
    páginas oficiales: dLocal cubre los 14 países latinoamericanos de este
    archivo; EBANX, todos menos El Salvador; PayU, Argentina, Chile, Colombia,
    México, Panamá y Perú (además de Brasil); Kushki, Chile, Colombia,
    Ecuador, México y Perú. La cobertura cambia por método, y algunas piden
    empresa constituida o un volumen mínimo. Pregunta antes.
  - Mercado Pago opera en Argentina, Brasil, Chile, Colombia, México, Perú y
    Uruguay, pero en general cada país usa su propia cuenta y sus propias
    credenciales.
  - Stripe tiene cuentas para empresas en México y España, y en ningún otro de
    los países de este archivo. Acepta tarjetas internacionales de casi
    cualquier país. La lista actual está en stripe.com/global.
  - Merchant of record: vende en tu lugar y se encarga de los impuestos del
    comprador en muchos países. Sirve para software por suscripción vendido a
    varios países. Paddle funciona como merchant of record. Lemon Squeezy le
    está pidiendo a sus usuarios que pasen a Stripe Managed Payments, que por
    ahora tiene lista de espera, así que no lo uses para empezar algo nuevo.
    Igual tienes que facturarle al merchant of record y declarar tus ingresos
    en tu país.
- **Pagos asíncronos**: con efectivo (OXXO, PagoEfectivo, Efecty) y con
  transferencias (SPEI, PSE) el pago queda pendiente hasta que la pasarela
  avisa, a veces horas después, y a veces nunca se paga. Hay que modelarlo.
- **Suscripciones**: casi ningún método local (efectivo, transferencia,
  billeteras) permite cobros recurrentes automáticos. OXXO y Bizum en Stripe,
  por ejemplo, no los permiten. Para planes mensuales, usa tarjeta, o
  domiciliación SEPA en España, y para los demás métodos envía un enlace de
  pago en cada periodo.
- **Apps de iOS y Android**: si vendes contenido o funciones digitales dentro
  de la app, las tiendas exigen su propio sistema de pagos (Apple, guía 3.1.1;
  Google Play, su política de pagos), salvo las excepciones que cada una
  permite en algunos países. Para bienes o servicios que se usan fuera de la
  app (una cita, un pedido de comida), Apple exige otros métodos de pago (guía
  3.1.3(e)), y ahí sirven las pasarelas locales, igual que en la web.

## Países principales

### México

- Moneda: peso mexicano (MXN).
- Pagos: tarjetas de crédito y débito, meses sin intereses con tarjeta de
  crédito, OXXO (el cliente paga en efectivo en tienda con una referencia),
  SPEI (transferencia bancaria), Mercado Pago (que también acepta OXXO y
  SPEI). Stripe está disponible y acepta tarjetas, OXXO, transferencias
  bancarias en pesos y meses sin intereses. Otras pasarelas locales: Conekta,
  Openpay.
- Facturación: CFDI 4.0 ante el SAT, la única versión válida hoy. Se emite
  mediante un PAC (proveedor autorizado de certificación) o con el servicio
  gratuito del SAT. Los clientes suelen pedir factura con sus datos fiscales
  (RFC, nombre o razón social, régimen fiscal, código postal y uso del CFDI).
  Las ventas a quien no pide factura van en una factura global al público en
  general.
- Impuesto: IVA del 16%. En las regiones fronterizas norte y sur hay un
  estímulo fiscal para contribuyentes inscritos (un crédito del 50% del IVA,
  que deja la tasa efectiva en 8%), vigente hasta el 31 de diciembre de 2026.

### Colombia

- Moneda: peso colombiano (COP). En la práctica los precios van sin centavos.
- Pagos: PSE (débito directo desde la cuenta bancaria, muy usado), tarjetas,
  billeteras como Nequi y Daviplata, efectivo en puntos como Efecty. Pasarelas
  locales: Wompi, ePayco, PayU, Mercado Pago (que acepta PSE y Efecty). Stripe
  no ofrece cuentas para empresas en Colombia.
- Facturación: factura electrónica de venta validada por la DIAN, obligatoria
  para la mayoría de quienes venden. Se emite con un proveedor tecnológico
  autorizado, con software propio o con la solución gratuita de la DIAN. El
  cliente puede pedirla con su NIT o su cédula.
- Impuesto: IVA del 19%.

### Perú

- Moneda: sol (PEN).
- Pagos: Yape y Plin (billeteras con QR o número de teléfono, muy usadas),
  tarjetas, transferencias, PagoEfectivo (el cliente paga en efectivo o por
  banca en línea con un código). Pasarelas locales: Niubiz, Izipay, Culqi,
  Mercado Pago (que acepta Yape). Stripe no ofrece cuentas para empresas en
  Perú.
- Facturación: comprobantes de pago electrónicos de la SUNAT (boleta de venta
  para consumidores, factura para empresas con RUC). Se emiten desde los
  sistemas gratuitos de la SUNAT, un OSE (operador de servicios electrónicos)
  o un PSE (proveedor de servicios electrónicos). Ojo: este PSE no tiene nada
  que ver con el PSE de pagos de Colombia.
- Impuesto: IGV del 18%.

### Chile

- Moneda: peso chileno (CLP), sin decimales: guarda los montos como enteros de
  pesos.
- Pagos: Webpay de Transbank (tarjetas de crédito y débito), transferencias
  bancarias (muy usadas), Mercado Pago, Khipu, Flow. Stripe no ofrece cuentas
  para empresas en Chile.
- Facturación: documentos tributarios electrónicos del SII, obligatorios: la
  factura electrónica para empresas con RUT y, desde 2021, la boleta
  electrónica para consumidores. Se emiten desde el sistema del SII o con un
  proveedor de facturación electrónica.
- Impuesto: IVA del 19%.

### Argentina

- Moneda: peso argentino (ARS). Con una inflación alta y cambiante, muchas
  apps actualizan sus precios seguido o los publican en dólares (USD). Decide
  cuál, y cada cuánto ajustas.
- Pagos: Mercado Pago (dinero en cuenta, tarjetas y QR, el más usado), tarjetas
  en cuotas, transferencias. Pasarelas locales: Mercado Pago, Payway. Stripe no
  ofrece cuentas para empresas en Argentina. Los cobros con tarjeta en moneda
  extranjera pueden llevar recargos o percepciones para el comprador: revisa
  la situación vigente.
- Facturación: factura electrónica ante ARCA (la agencia que reemplazó a la
  AFIP), obligatoria para monotributistas y responsables inscriptos. El tipo de
  comprobante (A, B, C o E) depende de tu condición fiscal y la del cliente;
  los monotributistas emiten el tipo C. El cliente se identifica con su CUIT o
  su DNI. Se emite desde el sitio de ARCA o con sus web services.
- Impuesto: IVA del 21%.

### España

- Moneda: euro (EUR).
- Pagos: tarjetas, Bizum (muy usado entre personas y cada vez más en comercios
  en línea), Apple Pay y Google Pay, domiciliación SEPA para suscripciones,
  PayPal. Stripe está disponible y acepta Bizum (sin cobros recurrentes, y
  puede que todavía con acceso limitado) y domiciliación SEPA.
- Facturación:
  - **Verifactu** (el reglamento que exige que el software de facturación
    cumpla requisitos técnicos y pueda enviar los registros a la AEAT): con el
    Real Decreto-ley 15/2025, las fechas vigentes son el 1 de enero de 2027
    para quienes pagan el Impuesto sobre Sociedades y el 1 de julio de 2027
    para el resto. El 5 de octubre de 2026, Hacienda anunció que lo aplaza
    hasta octubre de 2028 para pymes y autónomos (hasta 8 millones de euros de
    facturación), para que coincida con la factura electrónica obligatoria.
    Al revisar este archivo, ese aplazamiento todavía no estaba en el BOE:
    confírmalo.
  - **Factura electrónica obligatoria entre empresas** (Ley Crea y Crece): el
    Real Decreto 238/2026 y la Orden HAC/1028/2026, en vigor desde el 6 de
    octubre de 2026, fijan las fechas. Desde el 6 de octubre de 2027 para
    quienes facturan más de 8 millones de euros, y desde el 6 de octubre de
    2028 para todos los demás, autónomos incluidos.
  - En el País Vasco aplica TicketBAI (Álava, Bizkaia y Gipuzkoa). Navarra
    prepara su propio sistema, NaTicket, sin fechas todavía.
  - El cliente se identifica con su NIF.
- Impuesto: IVA del 21% (en Canarias aplica el IGIC, y en Ceuta y Melilla, el
  IPSI). A consumidores, el precio se muestra con IVA incluido.
- Ventas a consumidores de otros países de la UE: hasta 10.000 euros al año en
  ventas a distancia y servicios digitales a toda la UE, se aplica el IVA
  español (puedes elegir el del país del comprador). Por encima, se aplica el
  IVA del país del comprador y se declara con la ventanilla única (OSS).

## Otros países

| país | moneda | pagos comunes | facturación electrónica | impuesto general |
| --- | --- | --- | --- | --- |
| Ecuador | dólar (USD) | tarjetas, transferencias, Payphone, DeUna, Kushki | comprobantes electrónicos del SRI, obligatorios desde 2022 (salvo negocios populares del RIMPE) | IVA 15% |
| Uruguay | peso uruguayo (UYU) | tarjetas, Mercado Pago, transferencias | CFE (e-Factura y e-Ticket) ante la DGI, obligatorio para contribuyentes de IVA desde 2025 | IVA 22% |
| Costa Rica | colón (CRC) | SINPE Móvil, tarjetas, transferencias | comprobantes electrónicos de Hacienda (versión 4.4 desde septiembre de 2025) | IVA 13% |
| Panamá | balboa y dólar (PAB, USD) | tarjetas, Yappy, transferencias ACH | factura electrónica ante la DGI, con un PAC o con el facturador gratuito | ITBMS 7% |
| Guatemala | quetzal (GTQ) | tarjetas, transferencias, efectivo en agentes | FEL (factura electrónica en línea) ante la SAT | IVA 12% |
| El Salvador | dólar (USD) | tarjetas, transferencias | DTE (documento tributario electrónico) ante el Ministerio de Hacienda, por grupos designados | IVA 13% |
| República Dominicana | peso dominicano (DOP) | tarjetas, transferencias | e-CF ante la DGII (Ley 32-23), por etapas; para pequeños y micro contribuyentes, hasta el 15 de noviembre de 2026 | ITBIS 18% |
| Paraguay | guaraní (PYG), sin decimales | tarjetas, transferencias, billeteras | SIFEN (e-Kuatia) ante la DNIT, por grupos | IVA 10% |
| Bolivia | boliviano (BOB) | pagos con QR, transferencias, tarjetas | facturación en línea del SIN, por grupos | IVA 13% |

Las tasas de impuesto de este archivo se cruzaron con el resumen de impuestos
de PwC (fuente secundaria, revisado en 2026) y, para Ecuador y España, con la
autoridad tributaria.

Para cualquier otro país: busca su autoridad tributaria junto con
"facturación electrónica". Casi toda la región ya la exige o la está
implementando.

## Precios en moneda local

- Muestra los precios en la moneda de cada país, redondeados como se
  acostumbra ahí (por ejemplo 199 MXN, 39.900 COP, 9.990 CLP).
- Formatea los montos con la convención local, que cambia de país a país (por
  ejemplo con `Intl.NumberFormat` y el locale `es-MX`, `es-CO`, `es-AR` o
  `es-ES`).
- No conviertas desde dólares sin más: fija cada precio a mano según el poder
  de compra y la competencia de cada país.
- A consumidores, muestra el precio final con impuestos incluidos. En muchos
  países es obligatorio.
- En App Store Connect y Play Console se pueden fijar precios por país.
- Si cobras en dólares, dilo claro antes del pago, porque el banco del cliente
  puede sumar comisiones o impuestos.

## WhatsApp como canal de atención

- En casi todos los países hispanohablantes, la gente espera soporte,
  confirmaciones y recordatorios por WhatsApp, más que por correo o por SMS.
- Usa la vía oficial: WhatsApp Business Platform (la Cloud API de Meta) o un
  proveedor autorizado como Twilio. El usuario crea la cuenta de Meta Business
  y verifica el número.
- Meta cobra por mensaje entregado desde el 1 de julio de 2025. Las plantillas
  tienen tres categorías: marketing, utilidad y autenticación.
- Fuera de la ventana de 24 horas que se abre cuando el cliente escribe, solo
  se pueden mandar plantillas aprobadas por Meta (recordatorios,
  confirmaciones). Dentro de la ventana se puede responder con texto libre.
- Desde el 1 de octubre de 2026, cada número tiene 1.000 mensajes de servicio
  gratis al mes, y desde el 1.001 se cobran. Las plantillas de utilidad que se
  mandan dentro de la ventana también se cobran. Revisa los precios actuales
  por país antes de calcular costos.
- Pide consentimiento antes de escribirle a alguien, guárdalo, y da una forma
  simple de dejar de recibir mensajes.
- Agrega un botón para escribir por WhatsApp (un enlace `wa.me`) en la landing
  page y dentro de la app.
- Nunca automatices WhatsApp Web ni uses apps no oficiales: Meta bloquea esos
  números.

## Fuentes oficiales para verificar

| tema | dónde |
| --- | --- |
| Stripe por país | stripe.com/global |
| Stripe: OXXO, transferencias, meses sin intereses, Bizum | docs.stripe.com/payments |
| Mercado Pago | mercadopago.com, eligiendo el país, y su documentación para desarrolladores |
| WhatsApp Business Platform y precios | developers.facebook.com/docs/whatsapp/pricing |
| Apple App Review Guidelines | developer.apple.com/app-store/review/guidelines |
| México | www.sat.gob.mx |
| Colombia | www.dian.gov.co |
| Perú | www.sunat.gob.pe |
| Chile | www.sii.cl |
| Argentina | www.arca.gob.ar |
| España | sede.agenciatributaria.gob.es y www.hacienda.gob.es |
| Ecuador | www.sri.gob.ec |
| Uruguay | www.gub.uy/direccion-general-impositiva |
| Costa Rica | www.hacienda.go.cr |
| Panamá | dgi.mef.gob.pa |
| Guatemala | portal.sat.gob.gt |
| El Salvador | www.mh.gob.sv |
| República Dominicana | dgii.gov.do |
| Paraguay | www.dnit.gov.py |
| Bolivia | www.impuestos.gob.bo |
