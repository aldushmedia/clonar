---
name: clonar-publicar
description: >-
  Publica el clon de una app en el propio dominio del usuario: una
  verificación previa obligatoria (tests en verde, imprescindibles de paridad
  terminadas, barrido de marca limpio, ficha revisada, páginas legales
  publicadas), base de datos y variables de entorno de producción, el
  hosting, los registros DNS del dominio y del correo, Stripe en modo en
  vivo, redirecciones de OAuth, monitoreo y builds móviles para TestFlight y
  Play. Úsala cuando el usuario diga "despliégalo", "publícalo", "ponlo en
  línea", "conecta mi dominio", "pasa a producción", "publica la app", o
  después de /clonar-lanzar.
---

# clonar-publicar

Lee todo lo que hay en `clonar/`. Escribe `clonar/deploy.md` (la lista de
verificación de `preflight.md` en esta carpeta, completada).

## Las reglas

- **Nada sale en vivo sin el visto bueno del usuario.** Muestra los
  resultados de la verificación previa y pregunta.
- **El usuario compra e inicia sesión.** Claude nunca compra un dominio,
  ingresa una tarjeta, escribe una contraseña ni pega una clave en vivo.
  Claude escribe los registros DNS exactos, los nombres de las variables de
  entorno y los comandos; el usuario hace los pasos de las cuentas.
- **No hasta que tenga marca propia.** El barrido tiene que estar limpio. Sin
  excepciones.

## Paso 1: verificación previa

Corre cada verificación y pega los resultados en `deploy.md`:

```bash
npx playwright test                                                  # clonar-probar
python3 ../clonar-comparar/parity.py clonar/features.csv               # imprescindibles terminadas
python3 ../clonar-marca/sweep.py . --config clonar/brand.json      # código 0: limpio
python3 ../clonar-lanzar/listing.py clonar/launch/listing.json     # si se publica en tiendas
npm run build                                                        # el build de producción pasa
```

(Las rutas son relativas a donde esté instalado el paquete. En
`~/.claude/skills/` eso es `~/.claude/skills/clonar-comparar/parity.py`, y así
con las demás.)

Además, a mano: sin bugs S1 ni S2 abiertos, las páginas de política de
privacidad y de términos publicadas (con cada proveedor que procesa datos),
banner de cookies si usas cookies no esenciales en la UE o el Reino Unido, el
borrado de cuenta funciona, y el favicon, los títulos y la imagen OG son
tuyos.

Cualquier falla detiene el despliegue. Di cuál y por qué.

## Paso 2: servicios de producción

- Un **proyecto de producción separado** para la base de datos (nunca el de
  desarrollo), con respaldos activados y migraciones que corre el despliegue,
  no a mano.
- Las variables de entorno de producción configuradas en el hosting, iguales
  a `.env.example`. Las claves en vivo, solo aquí.
- **Pagos** (Stripe, Mercado Pago o la pasarela de cada país): cambia al
  modo en vivo, vuelve a crear los productos y los precios en cada moneda,
  agrega el endpoint del webhook de producción y su secreto de firma, prueba
  una compra real con cada método de pago y reembólsala.
- **Facturación electrónica**: pasa el proveedor del ambiente de pruebas a
  producción en cada país que la exige, y revisa el primer comprobante real.
- **OAuth**: agrega el dominio de producción a las URI de redirección y a
  los orígenes autorizados de cada proveedor. Los scopes de Google que
  necesitan verificación tienen que estar aprobados, o solo los usuarios de
  prueba podrán iniciar sesión.
- **Correo**: el dominio de envío verificado con el proveedor.

## Paso 3: hosting y dominio

Por defecto: Vercel para Next.js (si no, Netlify, Cloudflare Pages, Fly o
Render). Conecta el repo para que `main` se despliegue y los pull requests
tengan URL de vista previa.

El dominio, después de que el usuario lo compre en cualquier registrador:

| registro | nombre | valor |
| --- | --- | --- |
| A | @ | la IP raíz del hosting (Vercel: aparece en la configuración del dominio) |
| CNAME | www | el destino del hosting (Vercel: `cname.vercel-dns.com`) |
| TXT | @ o un subdominio | el valor de verificación del hosting, si lo pide |

El DNS del correo, del proveedor de correo: SPF (TXT), DKIM (CNAME o TXT) y
un registro DMARC que empiece en `v=DMARC1; p=none; rua=mailto:you@yourdomain`
y que luego se endurezca a `quarantine` cuando los reportes estén limpios.
Sin esto, tus correos de confirmación van a spam.

Elige un host canónico (el dominio raíz o www) y redirige el otro. HTTPS es
automático en los hostings de arriba; revísalo.

## Paso 4: vigílalo

Seguimiento de errores (Sentry o el del hosting), monitoreo de disponibilidad
en la página de inicio y en la API del flujo principal, logs guardados,
analíticas (una que respete la privacidad evita el banner de cookies) y una
alerta al correo o al teléfono del usuario. Luego haz tú mismo el flujo
principal en el sitio en vivo, y pídele al usuario que lo haga en su
teléfono.

## Paso 5: móvil, si hay una app

Expo: `eas build` y luego `eas submit` a TestFlight y a las pruebas internas
de Play. Nativa: archiva en Xcode y sube a App Store Connect; bundle de
Gradle a Play Console. El usuario es dueño de las cuentas de desarrollador
(99 USD al año para Apple, 25 USD una sola vez para Google). Primero la beta,
luego la revisión con la ficha de clonar-lanzar.

## Resultado

`clonar/deploy.md` con cada verificación y su resultado, la URL en vivo, los
registros DNS configurados y qué vigilar durante la primera semana. El clon
ahora es una app con tu nombre. Siguiente: `/clonar-redes`, para darla a
conocer en Instagram.
