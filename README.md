# Clonar

Doce skills para Claude que clonan cualquier app y la promocionan, más el
comando /clonar que te lleva por todo el proceso. Gratis, MIT, sin registro,
sin API key, nada que conectar.

Una hace ingeniería inversa de la app que quieres clonar. Otra la reconstruye.
Otra la prueba en busca de bugs. Y una es la Emprendedora: lee lo que los
usuarios de la app odian y lo arregla en la tuya, para que tengas una app que
puedas vender. Al final, otra escribe los Reels para darla a conocer en
Instagram.

En el medio, las demás planean el stack y la base de datos, reconstruyen el
sistema de diseño, conectan la autenticación y los pagos, comparan tu clon con
el original, le dan un nombre y una marca propios, escriben la landing page y
la ficha de la tienda, y lo publican en tu dominio.

Se adapta a cualquier país hispanohablante: pregunta dónde vas a lanzar y
ajusta los pagos, la factura electrónica, la moneda y la atención por WhatsApp.

**Reconstruye lo que una app hace, nunca lo que le pertenece.** Funciones y
flujos, al estilo sala limpia (clean room). No su código, su logo, sus textos
ni su contenido. La letra pequeña está al final, y las skills la hacen cumplir.

## Instalación

Pega esto en Claude:

```
https://github.com/aldushmedia/clonar

instala la skill
```

O como plugin, en Claude Code:

```
/plugin marketplace add aldushmedia/clonar
/plugin install clonar@clonar
```

Claude Code agrupa las skills de un plugin bajo su nombre, así que instaladas
como plugin aparecen como `/clonar:clonar`, `/clonar:clonar-explorar` y así
con las demás. Si prefieres los comandos simples (`/clonar`,
`/clonar-explorar`), copia las carpetas:

```bash
git clone https://github.com/aldushmedia/clonar.git
cp -r clonar/clonar clonar/clonar-* ~/.claude/skills/
```

Para un solo proyecto en lugar de global: copia esas mismas carpetas en el
`.claude/skills/` de tu repo. ¿No usas Claude Code? Pega cualquier `SKILL.md`
al inicio de un chat y funciona como un modo. Pierdes las herramientas de
Python, pero el método funciona.

Las herramientas necesitan Python 3.8 o más reciente. No hay nada que instalar
con pip.

## Empieza con /clonar

`/clonar` es el comando maestro. Te lleva por las 12 etapas en orden: corre la
skill de cada una, te muestra lo que salió y te pide aprobación antes de pasar
a la siguiente. Respondes sí, pides cambios, repites, saltas una etapa
opcional o te detienes. El avance queda en `clonar/progreso.md`, así que la
próxima vez retoma donde quedó. Nada se publica sin tu visto bueno.

## Los comandos

| comando | qué hace |
| --- | --- |
| `/clonar` | El comando maestro: corre todas las etapas en orden y pide tu aprobación al final de cada una. |
| `/clonar-explorar` | Hace ingeniería inversa de cualquier app: pantallas, flujos, componentes, modelo de datos. Desde páginas públicas, capturas, fichas de tienda y tu propia cuenta. |
| `/clonar-arquitecto` | Pregunta en qué países lanzas y planea el stack, el esquema de la base de datos y la API de tu clon. |
| `/clonar-diseno` | Reconstruye el sistema de diseño: colores, tipografía, espaciado, componentes. Como tokens, con tus propios recursos. |
| `/clonar-construir` | Reconstruye la app pantalla por pantalla a partir del mapa de reconocimiento. |
| `/clonar-backend` | Autenticación, base de datos, pagos con los métodos de cada país, facturación electrónica, WhatsApp e integraciones. |
| `/clonar-probar` | Recorre cada flujo y lo prueba en busca de bugs. |
| `/clonar-comparar` | Compara tu clon con el original. Una puntuación de paridad y lo que falta. |
| `/clonar-emprendedor` | Lee lo que los usuarios de la app odian en reseñas reales, en inglés y en español, y lo convierte en arreglos y un ángulo de posicionamiento. |
| `/clonar-marca` | Le da nombre y una marca nueva a tu versión para que sea tuya. |
| `/clonar-lanzar` | Landing page, precios en moneda local y ficha de App Store. |
| `/clonar-publicar` | La publica en tu propio dominio. |
| `/clonar-redes` | Escribe 3 guiones de Reels, sus captions y ganchos para promocionar tu app en Instagram. |

## Cómo usarlo

Con `/clonar` no tienes que recordar el orden. Si prefieres ir a mano, corre
los comandos en este orden. Cada uno lee lo que escribió el anterior, en una
carpeta `clonar/` dentro de tu proyecto.

```
explorar -> arquitecto -> diseno -> construir -> backend -> probar -> comparar -> emprendedor -> marca -> lanzar -> publicar -> redes
```

Un ejemplo: clonar una app de citas para barberías, de esas en las que el
cliente elige barbero, servicio y horario, y la barbería ve su agenda del día.

1. **`/clonar-explorar`** con la URL de la app. Lee el centro de ayuda, la
   página de precios, la ficha de la tienda y los recorridos públicos, y tú
   recorres tu propia cuenta con ella. Resultado: `clonar/recon.md`, con 16
   pantallas, 6 flujos (el cliente reserva un corte, la barbería define los
   horarios de cada barbero, el cliente cambia su cita...), los componentes,
   un modelo de datos inferido (barberías, barberos, servicios, horarios,
   citas) y `features.csv`. El directorio público de barberías de la app
   original queda fuera del alcance: es su red, no una función.
2. **`/clonar-arquitecto`** pregunta primero en qué países vas a lanzar.
   Respondes México, Colombia y España, y con `paises.md` anota la moneda, los
   métodos de pago y la facturación electrónica de cada uno. Elige Next.js,
   Postgres, Mercado Pago para México y Colombia y Stripe para España, escribe
   el esquema (con una restricción para que un barbero nunca tenga dos citas a
   la misma hora) y ordena la construcción: primero el flujo de reserva de
   punta a punta.
3. **`/clonar-diseno`** mide las capturas y las convierte en tokens: roles de
   color, escala tipográfica, espaciado de 8px, las especificaciones del
   selector de barbero y del botón de horario. Íconos abiertos, una fuente
   abierta, tus propias palabras.
4. **`/clonar-construir`** construye la estructura base, luego el flujo de
   reserva y luego cada pantalla con todos sus estados, marcando
   `features.csv` a medida que avanza.
5. **`/clonar-backend`** confirma los países y agrega el registro, el cobro de
   un anticipo con la pasarela de cada país (con pago en efectivo en OXXO para
   México y PSE para Colombia), la factura electrónica mediante un proveedor
   certificado y los recordatorios por WhatsApp con la API oficial.
6. **`/clonar-probar`** escribe un plan de pruebas a partir de los 6 flujos,
   specs de Playwright para los caminos felices y los casos límite (zonas
   horarias, un horario ocupado a mitad de la reserva, doble envío, un pago en
   efectivo que vence sin pagarse), y registra bugs por severidad hasta que no
   quede ningún S1 ni S2 abierto.
7. **`/clonar-comparar`** le pone nota. Funciones 84, todas las imprescindibles
   listas, diseño de la página de reserva 90. Falta: la lista de espera cuando
   no hay horarios, la venta de productos en la barbería.
8. **`/clonar-emprendedor`** lee 140 reseñas reales en App Store, Google
   Play y Reddit, en inglés y en español. Quejas principales: los clientes
   faltan a la cita y no hay recordatorio por WhatsApp, el precio sube con
   cada barbero que agregas, no se puede pagar en efectivo. Cada una con
   conteos y citas enlazadas. Plan de arreglos: recordatorios por WhatsApp,
   precio fijo por barbería, pago en efectivo o con anticipo. Ángulo: una
   agenda para barberías pequeñas que pierden dinero cuando los clientes no
   llegan.
9. **`/clonar-marca`** le pone nombre (con las verificaciones de marca
   registrada y dominio que hay que correr), le da una paleta nueva, un brief
   de logo y una voz, y luego revisa el código hasta que no quede nada del
   original.
10. **`/clonar-lanzar`** confirma los países, escribe la landing page
    alrededor del ángulo, define los precios en pesos mexicanos, pesos
    colombianos y euros frente a la página pública del original, muestra los
    métodos de pago de cada país, agrega un botón de WhatsApp y revisa la
    ficha de la tienda.
11. **`/clonar-publicar`** corre la verificación previa (tests, paridad,
    revisión de marca, ficha), configura producción, te da los registros DNS
    para tu dominio y la publica cuando das el visto bueno.
12. **`/clonar-redes`** escribe 3 Reels: el cliente que no llegó a su cita y el
    recordatorio por WhatsApp que lo evita, la demo de reservar un corte en
    segundos, y la razón para cambiarse con precio fijo por barbería. Cada uno
    con su caption, y 10 ganchos para probar.

También puedes correr cualquiera por separado. Por ejemplo,
`/clonar-emprendedor` sobre una app de pedidos para negocios de comida que
solo estás pensando en clonar: te dice, con cada queja enlazada, si a sus
usuarios les molestan las comisiones por pedido, los pedidos que se pierden o
que no se pueda pagar en efectivo. Es una buena forma de saber si vale la
pena.

## Para lanzar en países hispanohablantes

`/clonar-arquitecto`, `/clonar-backend` y `/clonar-lanzar` preguntan primero
en qué país o países vas a lanzar, y se adaptan a cada uno:

- **Pagos**: los métodos que la gente usa de verdad (por ejemplo Mercado Pago
  en varios países de Latinoamérica, OXXO en México, PSE en Colombia, Yape en
  Perú, Webpay en Chile, Bizum en España, Stripe donde esté disponible) y
  pasarelas regionales para cobrar en varios países a la vez.
- **Facturación electrónica**: una nota por país (CFDI en México, DIAN en
  Colombia, SII en Chile, SUNAT en Perú, ARCA en Argentina, Verifactu en
  España, entre otros).
- **Precios en moneda local** y **WhatsApp** como canal de atención, donde
  aplique.

Todo eso está en un solo archivo, `clonar-arquitecto/paises.md`, para
actualizarlo fácil. Esa información cambia con el tiempo: verifícala con cada
proveedor y con la autoridad tributaria, y confirma la facturación con un
contador local antes de lanzar.

`/clonar-emprendedor` reconoce quejas en inglés y en español, con variantes
regionales comunes de distintos países y con o sin acentos.

## Las herramientas

Son seis, todas en Python con la biblioteca estándar. Ninguna toca la red, y
sus mensajes están en español.

```bash
python3 clonar-comparar/imgdiff.py original.png clone.png --out diff.png   # diferencia de diseño, ignora el color
python3 clonar-comparar/parity.py clonar/features.csv                     # puntuación de paridad + lista de faltantes
python3 clonar-emprendedor/reviews.py clonar/reviews.csv                  # lo que los usuarios odian, ordenado y enlazado
python3 clonar-diseno/contrast.py clonar/design/tokens.json               # contraste WCAG de tus tokens
python3 clonar-marca/sweep.py . --avoid "Original App"                     # ¿queda algo del original?
python3 clonar-lanzar/listing.py clonar/launch/listing.json               # límites de la tienda + revisión de copias
```

**`imgdiff.py`** lee PNG sin bibliotecas, convierte ambas capturas en mapas
de bordes y compara dónde están las cosas, así tus colores nuevos no cuentan
en tu contra. Te dice qué regiones difieren, en los píxeles del original.

**`parity.py`** pondera must, should y could, cuenta lo parcial como la
mitad, y nunca puntúa lo que dejaste fuera a propósito ni lo que agregaste.
Si faltan funciones imprescindibles, no se puede publicar, y lo dice.

**`reviews.py`** descarta cada reseña sin enlace. Cada cita que imprime está
copiada de una fila que le diste, con la URL de esa fila. Los temas con menos
de tres reseñas o una sola fuente se marcan como débiles. Reconoce quejas en
inglés y en español.

**`sweep.py`** encuentra el nombre, el dominio y los colores del original en
cualquier parte de tu código, incluso dentro de identificadores como
`OriginalAppEmbed`, y bloquea el despliegue hasta que todo esté limpio.

**`listing.py`** revisa los límites de App Store y Google Play, las
afirmaciones de ranking en el título, los caracteres desperdiciados en las
palabras clave y el nombre del original en cualquier parte de tu ficha.

```bash
python3 -m unittest discover -s tests -v
```

## Letra pequeña

**Reconstruye funciones y patrones de UX, al estilo sala limpia.** Estudia lo
que la app hace y cómo se mueve la gente por ella, y luego escribe todo desde
cero. Nunca copia el código fuente, los recursos propietarios, los logos, las
marcas registradas, los textos ni las APIs privadas de la app.

**Solo lee lo que tienes permitido leer.** Páginas públicas y tu propia
cuenta. Nunca extrae datos detrás de un login ni en contra de los términos de
un sitio, nunca entra a la cuenta de otra persona y nunca se salta un muro de
pago. Si los términos de tu cuenta prohíben usarla para construir un
competidor, te lo dice y se limita a fuentes públicas.

**Siempre cambia la marca antes del lanzamiento.** Nombre nuevo, paleta
nueva, logo nuevo, palabras nuevas. `/clonar-publicar` no publica hasta que la
revisión esté limpia, y `/clonar-redes` nunca nombra a la app original.

**"Clonar cualquier app" significa las funciones y el flujo.** No el
contenido, la red ni las licencias que una app tiene. Puedes reconstruir el
menú, el carrito y el seguimiento del pedido de una app de pedidos para
negocios de comida. No puedes clonar su red de restaurantes ni de
repartidores.

**No hay garantía de un clon "perfecto".** Los resultados dependen de qué tan
compleja sea la app. Una app de citas para barberías lleva semanas. Un motor
de hojas de cálculo no. `/clonar-explorar` estima el tamaño con honestidad
antes de empezar, y `/clonar-comparar` te da un número real, no una
impresión.

**La Emprendedora nunca inventa nada.** Ni reseñas, ni citas, ni números
inventados. Cada afirmación tiene un enlace, y se indica el tamaño de la
muestra. Los Reels tampoco: sin testimonios ni cifras inventadas.

**Verifica antes de vender.** Corre las verificaciones de marca registrada que
lista `/clonar-marca`, lee los términos de todo lo que usaste y habla con un
abogado antes del lanzamiento si hay dinero de por medio. Esto no es asesoría
legal.

## Archivos

```
clonar/                SKILL.md, progreso.md (el comando maestro)
clonar-explorar/       SKILL.md, recon-map.md, features.csv (la plantilla de la matriz)
clonar-arquitecto/     SKILL.md, architecture.md, paises.md (pagos, facturación, moneda y atención por país)
clonar-diseno/         SKILL.md, tokens.json, contrast.py
clonar-construir/      SKILL.md
clonar-backend/        SKILL.md
clonar-probar/         SKILL.md, test-plan.md, bug-report.md, e2e.example.spec.ts
clonar-comparar/       SKILL.md, imgdiff.py, parity.py
clonar-emprendedor/    SKILL.md, reviews.py, themes.json
clonar-marca/          SKILL.md, sweep.py
clonar-lanzar/         SKILL.md, listing.py, listing.example.json
clonar-publicar/       SKILL.md, preflight.md
clonar-redes/          SKILL.md, reels.md
tests/                 los tests de cada herramienta, incluidos los patrones en español
```

Tus propios archivos viven en `clonar/` dentro de tu proyecto, y las skills
leen los archivos de las otras. No la confundas con la carpeta `clonar/` de
este repo, que es la del comando maestro.

La lógica de las herramientas es la del proyecto original; sus mensajes están
traducidos al español.

## Créditos

Traducción y adaptación al español por Aldush Media. Basada en un proyecto
original con licencia MIT; su aviso de copyright se conserva en `LICENSE`.

## Licencia

MIT. Tómala, cámbiala, publícala. Ver `LICENSE`.
