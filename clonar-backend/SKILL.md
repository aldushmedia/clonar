---
name: clonar-backend
description: >-
  Construye el backend del clon de una app: autenticación, migraciones de la
  base de datos y reglas de acceso, pagos con los métodos de cada país (Stripe,
  Mercado Pago o la pasarela local), facturación electrónica, correo,
  WhatsApp, tareas en segundo plano e integraciones con terceros solo mediante
  APIs oficiales, más una lista de verificación de seguridad. Primero pregunta
  en qué país o países se va a lanzar. Úsala cuando el usuario diga "agrega el
  login", "configura la autenticación", "conecta la base de datos", "agrega
  pagos", "conecta Stripe", "conecta Mercado Pago", "agrega la factura
  electrónica", "manda recordatorios por WhatsApp", "agrega Google Calendar",
  "envía correos", "backend para mi clon", o cuando /clonar-construir esté
  corriendo con datos falsos.
---

# clonar-backend

Lee `clonar/architecture.md` y `../clonar-arquitecto/paises.md`. Escribe las
migraciones y el código del servidor, y mantiene al día `clonar/backend.md`
(la lista de verificación de abajo).

## Antes de empezar: países

Pregunta primero en qué país o países se va a lanzar la app. Si
`clonar/architecture.md` ya tiene la sección Países, muéstrala y confírmala
con el usuario en lugar de preguntar desde cero. Si cambió algo, actualiza esa
sección.

Para cada país, lee en `../clonar-arquitecto/paises.md` los métodos de pago,
las pasarelas, la facturación electrónica y si WhatsApp es el canal esperado.
Esa información cambia con el tiempo: dile al usuario que la verifique con
cada proveedor y que confirme la facturación con un contador local.

## Las reglas

- **Solo APIs oficiales y públicas, con las claves del propio usuario.** Nunca
  llames a los endpoints privados de la app original, nunca reutilices su
  cliente OAuth, nunca pases a través de ella como proxy.
- **El usuario crea las cuentas y las claves.** Claude nunca se registra en
  servicios, nunca escribe una contraseña, una tarjeta ni una clave en vivo.
  El usuario crea el proyecto de Stripe, Mercado Pago u otra pasarela,
  Supabase, Resend, Meta Business o Google Cloud, y la cuenta con el proveedor
  de facturación, y pone las claves en `.env.local`. Claude escribe
  `.env.example` con el nombre de cada variable y sin valores.
- **Primero el modo de prueba.** Credenciales y tarjetas de prueba de cada
  pasarela, y el ambiente de pruebas del proveedor de facturación, hasta
  clonar-publicar.

## Autenticación

- Registro con correo y verificación, recuperación de contraseña, enlace
  mágico si el original lo tiene. OAuth (Google, Apple) con las apps de
  desarrollador del propio usuario.
- Sesiones: cookies seguras http-only. Cerrar sesión en todos lados.
- Roles y equipos si el mapa de reconocimiento los tiene: owner, admin,
  member, con una función que responda "puede este usuario hacerle esto a
  este registro".
- Borrado de cuenta que de verdad borre. Apple lo exige para las apps con
  registro.

## Base de datos

- Migraciones a partir de `architecture.md`, versionadas en el repo y
  ejecutadas con un script.
- Reglas de acceso en cada tabla: políticas de row level security en
  Supabase, o la función de autorización llamada en cada consulta. Pruébalo:
  un segundo usuario no debe recibir nada.
- Script de datos de prueba (seed) con datos falsos realistas (sin personas
  reales).
- Respaldos activados (los respaldos diarios del proveedor cuentan, revisa
  que estén activados).

## Pagos

- **La pasarela según el país** (sección Países de `architecture.md`):
  Stripe donde esté disponible, Mercado Pago o la pasarela local, o una
  regional (dLocal, EBANX, PayU, Kushki) para cobrar en varios países con una
  sola integración. Ofrece los métodos que la gente usa en cada país, no solo
  tarjeta: por ejemplo OXXO en México, PSE en Colombia, Yape en Perú, Webpay
  en Chile o Bizum en España.
- Usa el checkout alojado de la pasarela (Stripe Checkout, Checkout Pro de
  Mercado Pago o el equivalente) y su portal o enlace para cambios y
  cancelaciones. No construyas formularios de tarjeta.
- Cobra en la moneda local de cada país, con los montos en la unidad mínima
  de la moneda. Ojo: CLP y PYG no tienen decimales.
- Webhooks: verifica la firma, guarda el id del evento, haz que cada handler
  sea idempotente (todas las pasarelas reintentan). Con Stripe, maneja
  `checkout.session.completed`, `customer.subscription.updated`,
  `customer.subscription.deleted`, `invoice.payment_failed`. Con las demás,
  sus eventos equivalentes de pago aprobado, rechazado, vencido y
  reembolsado.
- **Pagos asíncronos.** Con efectivo (OXXO, PagoEfectivo, Efecty) y
  transferencias (SPEI, PSE), el pago queda pendiente hasta que llega el
  webhook. Guarda el estado (`pending`, `paid`, `expired`, `failed`), no des
  acceso ni confirmes la cita o el pedido hasta que esté pagado, y libera lo
  apartado cuando la referencia venza.
- **Suscripciones.** Casi ningún método local permite cobros recurrentes
  automáticos. Para planes mensuales, usa tarjeta (o domiciliación SEPA en
  España) con las suscripciones de la pasarela, y para los demás métodos envía
  un enlace de pago en cada periodo, con recordatorio.
- El estado de la suscripción vive en tu base de datos, lo actualizan los
  webhooks y lo lee tu app. Nunca confíes en el cliente.
- Cancelar es un solo clic. Los cobros difíciles de cancelar son una de las
  quejas principales sobre la mayoría de las apps, y en muchos lugares son
  ilegales.

## Facturación electrónica

En casi todos los países hispanohablantes, cada cobro necesita un comprobante
electrónico válido ante la autoridad tributaria: CFDI en México, factura
electrónica de la DIAN en Colombia, boleta o factura de la SUNAT en Perú,
boleta o factura del SII en Chile, factura de ARCA en Argentina, software que
cumpla Verifactu en España. El detalle está en `paises.md`.

- Intégrala con un proveedor certificado (en México, un PAC) o con el servicio
  oficial de la autoridad, mediante su API y con el certificado y las claves
  del usuario. Nunca inventes un formato de comprobante propio.
- Guarda los datos fiscales que pide cada país (por ejemplo RFC, NIT, RUC, RUT,
  CUIT o NIF) y deja que el cliente los ingrese al pagar o que pida su factura
  después.
- Emite el comprobante cuando el pago se confirma (por webhook), guarda su
  número o folio, el XML y el PDF, y envíaselo al cliente. Para los reembolsos,
  la nota de crédito o el comprobante que corresponda.
- Si usas un merchant of record (como Paddle), ellos le facturan al
  comprador; tú le facturas al merchant of record según tu país.
- Escribe en `backend.md` qué comprobante emite la app en cada país, y deja
  anotado que el usuario debe confirmarlo con un contador local antes del
  lanzamiento.

## Correo, WhatsApp y tareas

- Correo transaccional mediante Resend o Postmark desde tu propio dominio.
  Plantillas escritas desde cero.
- WhatsApp, donde la sección Países lo marque como canal: confirmaciones,
  recordatorios y atención mediante WhatsApp Business Platform (la Cloud API
  de Meta) o un proveedor autorizado como Twilio, con plantillas aprobadas por
  Meta. Guarda el consentimiento de cada cliente antes de escribirle y da una
  forma simple de dejar de recibir mensajes. Nunca automatices WhatsApp Web ni
  uses apps no oficiales.
- Tareas para todo lo que dependa del tiempo (recordatorios, resúmenes,
  sincronización, limpieza, vencimiento de pagos pendientes) con reintentos y
  un registro de fallos definitivos (dead-letter). Horas en UTC, mostradas en
  la zona del usuario.

## Integraciones

Para cada integración de la matriz de funciones: la API oficial, los scopes
de OAuth necesarios (los menos posibles), el proceso de revisión del
proveedor, los límites de solicitudes. Los scopes de Google como Calendar
necesitan la verificación OAuth de Google antes del lanzamiento público, y
eso tarda semanas. Empiézala pronto y anótalo en `backend.md`. Lo mismo con
la verificación de la cuenta de Meta Business para WhatsApp.

## Lista de verificación de seguridad

- [ ] secretos solo en variables de entorno, `.env*` en `.gitignore`, nada en los bundles del cliente
- [ ] entrada validada en el servidor (zod o similar) en cada ruta
- [ ] autorización verificada en cada lectura y escritura, probada con un segundo usuario
- [ ] límites de solicitudes en la autenticación, el registro y todo lo que envíe correos, SMS o WhatsApp
- [ ] los webhooks verifican las firmas, en cada pasarela
- [ ] los datos fiscales de los clientes se tratan como datos personales
- [ ] consentimiento guardado antes de enviar mensajes por WhatsApp
- [ ] archivos subidos: límites de tamaño y tipo, servidos desde un dominio o bucket separado
- [ ] sin datos de usuarios en las URL ni en los logs
- [ ] dependencias auditadas (`npm audit`)
- [ ] la política de privacidad lista cada proveedor que procesa datos (pasarelas, proveedor de facturación, Resend, Meta, hosting, analíticas)

## Resultado

Autenticación, base de datos, pagos en modo de prueba con los métodos de cada
país, facturación electrónica en el ambiente de pruebas, correo, WhatsApp e
integraciones funcionando, `.env.example`, `clonar/backend.md` con la lista
marcada y los comprobantes por país, y las filas de la matriz de funciones
actualizadas. Recuérdale al usuario que verifique los datos de cada país.
Siguiente: `/clonar-probar`.
