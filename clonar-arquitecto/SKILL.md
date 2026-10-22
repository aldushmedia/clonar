---
name: clonar-arquitecto
description: >-
  Planea el stack, el esquema de la base de datos y la API del clon de una
  app, a partir del mapa de reconocimiento que escribió clonar-explorar. Elige
  tecnología aburrida y administrada, convierte el modelo de datos inferido en
  SQL real con índices y reglas de acceso, lista cada ruta por flujo y ordena
  la construcción empezando por un corte vertical delgado. Primero pregunta en
  qué país o países se va a lanzar y adapta los pagos, la facturación
  electrónica, la moneda y el canal de atención. Úsala cuando el usuario diga
  "planea el clon", "qué stack debería usar", "diseña la base de
  datos", "escribe el esquema", "planea la API", "arquitectura para mi
  versión de X", o después de que termine /clonar-explorar.
---

# clonar-arquitecto

Lee `clonar/recon.md` y `clonar/features.csv`. Escribe
`clonar/architecture.md` (plantilla: architecture.md en esta carpeta).

Si no hay mapa de reconocimiento, detente y corre `/clonar-explorar` primero.
Planear un clon de memoria, con lo que recuerdas que hace una app, es la
forma de olvidarte de la mitad.

## Paso 0: países

Antes que nada, pregunta en qué país o países se va a lanzar la app, y si
después se piensa abrir a otros. La respuesta cambia los pagos, la
facturación, la moneda y el canal de atención, así que va primero.

Con la respuesta, lee cada país en `paises.md` (en esta carpeta) y escribe en
`clonar/architecture.md` la sección **Países**: por país, la moneda, los
métodos de pago y la pasarela, la facturación electrónica que aplica, el
impuesto que se muestra en el precio y si WhatsApp será canal de atención.
clonar-backend y clonar-lanzar leen esa sección.

`paises.md` es un punto de partida y cambia con el tiempo. Dile al usuario que
verifique cada dato con el proveedor, la autoridad tributaria y un contador
local antes de decidir.

## Paso 1: el stack

Usa lo que el usuario ya conoce si tiene un stack. Si no, el que viene por
defecto, porque cada parte es administrada, está documentada y es barata con
cero usuarios:

| capa | por defecto | alternativa |
| --- | --- | --- |
| app web | Next.js (App Router) + TypeScript | Remix, SvelteKit, Rails |
| estilos | Tailwind, tokens de clonar-diseno | CSS modules |
| móvil | Expo (React Native) | SwiftUI, Kotlin |
| base de datos | Postgres en Supabase o Neon | PlanetScale, SQLite (Turso) |
| ORM | Drizzle o Prisma | SQL directo |
| autenticación | Supabase Auth o Auth.js | Clerk |
| pagos | según los países (`paises.md`): Stripe donde esté disponible, Mercado Pago o la pasarela local | dLocal, EBANX, PayU o Kushki para varios países; Paddle como merchant of record |
| facturación electrónica | un proveedor certificado en cada país que la exija | el servicio gratuito de la autoridad tributaria, con poco volumen |
| correo | Resend o Postmark | SES |
| WhatsApp | WhatsApp Business Platform (Cloud API de Meta) | un proveedor autorizado como Twilio |
| tareas | Vercel Cron, Inngest o Trigger.dev | un worker en Fly |
| archivos | Supabase Storage o Cloudflare R2 | S3 |
| hosting | Vercel | Netlify, Fly, Render |

Escribe cada elección con una línea que explique por qué. Una sola base de
datos. Sin microservicios. El clon no necesita la arquitectura del original,
necesita las funciones del original.

## Paso 2: el esquema

Convierte el modelo de datos inferido en SQL. Para cada tabla:

- `id uuid primary key default gen_random_uuid()`, `created_at`, `updated_at`
- una columna de dueño (`user_id` u `org_id`) en todo lo que le pertenece a
  un usuario
- claves foráneas con una regla `on delete` decidida, no la que viene por
  defecto
- índices en cada clave foránea y en cada columna por la que filtras u
  ordenas
- enums o restricciones check para los campos de estado
- las fechas y horas como `timestamptz`, siempre, guardadas en UTC
- el dinero como entero en la unidad mínima de la moneda (centavos) más una
  columna de moneda. Ojo con las monedas sin decimales, como CLP o PYG
- los pagos con su estado (`pending`, `paid`, `expired`, `failed`), porque el
  efectivo y las transferencias se confirman después
- los datos fiscales del cliente si algún país exige factura con ellos (por
  ejemplo RFC, NIT, RUC, RUT, CUIT o NIF), y el comprobante emitido por cada
  cobro
- reglas de acceso: row level security de Postgres en Supabase, o una
  verificación de autorización por consulta en la capa de datos. Escribe
  cuál.

Ejemplo, para una app de reservas:

```sql
create table bookings (
  id uuid primary key default gen_random_uuid(),
  event_type_id uuid not null references event_types(id) on delete cascade,
  host_id uuid not null references users(id) on delete cascade,
  start_at timestamptz not null,
  end_at timestamptz not null,
  guest_name text not null,
  guest_email text not null,
  guest_timezone text not null,
  status text not null default 'confirmed'
    check (status in ('confirmed','cancelled','rescheduled')),
  answers jsonb not null default '{}',
  created_at timestamptz not null default now(),
  constraint no_zero_length check (end_at > start_at)
);
create index on bookings (host_id, start_at);
```

Luego, las restricciones duras que encontró el reconocimiento. Que dos
invitados reserven el mismo horario es un problema de base de datos (una
restricción de exclusión o un índice único), no un problema de interfaz.

## Paso 3: la API

Una tabla por flujo del mapa de reconocimiento. Para cada ruta o server
action:

`método ruta | qué hace | quién puede llamarla | entrada | salida | flujo`

Además, los webhooks de entrada (Stripe, proveedores de calendario) y de
salida, y las tareas en segundo plano (recordatorios, sincronización,
limpieza) con su horario.

Solo APIs oficiales y públicas, con las claves del propio usuario. Nunca los
endpoints privados de la app original, aunque se vean en el navegador.

## Paso 4: las partes que muerden

Escribe una línea sobre cada una que aplique: zonas horarias y horario de
verano, idempotencia (los webhooks llegan dos veces), condiciones de carrera,
límites de solicitudes, límites de tamaño de archivo, búsqueda, tiempo real,
modo sin conexión, entregabilidad del correo, multi-tenancy, borrado según
el RGPD, pagos que se confirman horas después, facturación electrónica por
país, precios y montos en varias monedas.

## Paso 5: orden de construcción

1. **Corte vertical.** El ciclo principal de punta a punta, feo: registrarse,
   hacer lo único importante, ver el resultado. Prueba que el stack funciona.
2. **Imprescindibles (must)** de `features.csv`, por área.
3. **Deseables (should)**, luego las opcionales (could).
4. **Los arreglos** que encuentre clonar-emprendedor, una vez que haya
   corrido.

Cada hito lista sus pantallas (ID S), tablas y rutas.

## Resultado

`clonar/architecture.md` (con la sección Países), el SQL en
`clonar/schema.sql` o como la primera migración, y un resumen: los países con
su pasarela, el stack en una línea, la cantidad de tablas, la cantidad de
rutas, las tres partes más riesgosas, el recordatorio de verificar los datos de
cada país y el siguiente paso: `/clonar-diseno`.
