---
name: clonar-lanzar
description: >-
  Escribe el lanzamiento del clon de una app: la landing page construida
  sobre el ángulo de posicionamiento, los precios en la moneda local de cada
  país definidos frente a los precios públicos del original y las quejas de
  sus usuarios, los métodos de pago, la factura y el WhatsApp que espera cada
  país, y la ficha de App Store y Google Play revisada contra los límites de
  las tiendas y sus reglas contra copias. Primero pregunta en qué país o
  países se va a lanzar. Úsala cuando el usuario diga "landing page",
  "precios", "cuánto debería cobrar", "precios en pesos", "ficha de App
  Store", "capturas para la tienda", "plan de lanzamiento", "Product Hunt", o
  después de /clonar-marca.
---

# clonar-lanzar

Lee `clonar/fixes.md` (el ángulo y la evidencia), `clonar/brand.md`,
`clonar/brand.json`, la sección Países de `clonar/architecture.md` y
`../clonar-arquitecto/paises.md`. Escribe `clonar/launch/`: `landing.md`,
`pricing.md`, `listing.json`, `launch-plan.md`.

```bash
python3 listing.py clonar/launch/listing.json      # límites, afirmaciones, el nombre del original
```

Empieza a partir de `listing.example.json` en esta carpeta.

## Antes de empezar: países

Pregunta primero en qué país o países se va a lanzar la app. Si
`clonar/architecture.md` ya tiene la sección Países, muéstrala y confírmala
con el usuario en lugar de preguntar desde cero. Si cambió algo, actualiza esa
sección.

Para cada país, lee en `../clonar-arquitecto/paises.md` la moneda, los métodos
de pago, la facturación electrónica, el impuesto que se muestra en el precio y
si WhatsApp es el canal de atención esperado. Esa información cambia con el
tiempo: dile al usuario que la verifique y que confirme la facturación con un
contador local.

## Las reglas

- **Nada de pruebas sociales falsas.** Ni testimonios, ni conteos de
  usuarios, ni calificaciones con estrellas, ni logos de prensa, ni filas de
  "confían en nosotros" inventados. Una sección de pruebas vacía es mejor que
  una falsa. Usuarios beta reales, con su permiso, están bien.
- **Nada de citas de reseñas como testimonios.** Las reseñas del original son
  investigación.
- **El nombre del original queda fuera** del nombre de tu app, de la ficha de
  la tienda, de las palabras clave y de los anuncios. Apple y Google lo
  rechazan, y es una invitación a que te den de baja.

## Paso 1: landing page

`landing.md`, sección por sección, y luego constrúyela en el proyecto:

1. **Hero**: el ángulo como titular (qué haces, para quién), una línea debajo
   y un botón. Una captura del producto real.
2. **El problema**: los dos temas principales de "lo que odian", en palabras
   simples. Parafrasea, no cites a los que escribieron las reseñas.
3. **Cómo funciona**: tres pasos, a partir del flujo principal.
4. **Funciones**: cada una ligada a un arreglo de `fixes.md`. Empieza por los
   arreglos, no por las funciones de paridad. La paridad es el precio de
   entrada.
5. **Precios**: la tabla del paso 2, en la moneda del país de quien visita
   (o con un selector de país), con los métodos de pago de ese país visibles.
6. **Preguntas frecuentes**: las objeciones reales, incluida "¿puedo importar
   desde herramientas de {{categoría}}?" si construiste un importador, "¿con
   qué puedo pagar?" y "¿emiten factura?" en los países que la exigen.
7. **Llamado a la acción final.**

Donde la sección Países marque WhatsApp como canal, agrega un botón para
escribir por WhatsApp (un enlace `wa.me`) y no solo un correo de contacto.

Los textos con la voz de la marca, en español neutro si se lanza en varios
países. Corre la verificación de contraste de clonar-diseno sobre la página.

## Paso 2: precios

`pricing.md`:

- La página pública de precios del original y 2 o 3 alternativas, en una
  tabla, con la URL y la fecha en que se leyó, por país si el original cobra
  distinto en cada uno. Los precios cambian, así que la fecha importa.
- Lo que dijeron los que escribieron reseñas sobre precios y cobros, a partir
  de `feedback.md`, con conteos.
- El modelo: plan gratis o prueba, por usuario o fijo, mensual y anual (el
  anual por lo general con 2 meses gratis).
- Tres niveles como máximo. Nómbralos según para quién son.
- **Precios en moneda local**, fijados a mano para cada país (no convertidos
  desde dólares sin más), redondeados como se acostumbra ahí y, a
  consumidores, con impuestos incluidos. Si algún país se cobra en dólares,
  dilo claro antes del pago.
- **Métodos de pago por país**, los que la gente espera (por ejemplo OXXO en
  México, PSE en Colombia, Yape en Perú, Webpay en Chile, Bizum en España, o
  tarjeta en cuotas donde se use), y cuáles sirven para cobros recurrentes.
- **Factura**: en cada país que la exige, cómo la pide el cliente y qué datos
  fiscales necesita. Que lo confirme un contador local.
- Arregla las quejas de cobros en el producto: cancelar con un clic, correos
  de renovación claros, sin saltos sorpresa de precio por usuario.
- Los productos y precios que hay que crear en la pasarela de cada país (los
  crea el usuario).

## Paso 3: ficha de la tienda

Llena `listing.json`, y luego:

```bash
python3 listing.py clonar/launch/listing.json
```

Revisa los límites de App Store (nombre 30, subtítulo 30, texto promocional
170, palabras clave 100, descripción 4000) y los de Google Play (título 30,
descripción corta 80, completa 4000), cuenta los caracteres como lo hace una
persona, marca las afirmaciones de ranking y de precio en los campos cortos,
los emoji, los caracteres desperdiciados en las palabras clave y **cualquier
nombre de `avoid`** en cualquier parte de la ficha. Sale con código 1 si hay
un error.

La Guía de revisión de apps de Apple 4.1 (Copycats) rechaza las apps que
simplemente copian una app popular o hacen cambios menores al nombre o a la
interfaz de otra app. Tus arreglos y tu propia marca son lo que te hace pasar
la revisión, así que hazlos visibles en las capturas y en las primeras líneas
de la descripción.

Las reglas de afirmaciones de `listing.py` buscan sobre todo palabras en
inglés ("best", "free", "#1"). Si tu ficha está en español, revisa a mano que
los campos cortos no digan "el mejor", "gratis", "número 1" ni algo parecido.

Fija los precios por país en App Store Connect y Play Console. Si la app
vende contenido o funciones digitales dentro de la app, las tiendas suelen
exigir su propio sistema de pagos; las pasarelas locales sirven para la web y
para bienes o servicios que se usan fuera de la app (una cita, un pedido de
comida).

Prepara también: capturas en los tamaños que se exigen hoy (revisa App Store
Connect y Play Console cuando subas, porque cambian), las etiquetas de
privacidad y el formulario de seguridad de datos, las URL de la política de
privacidad y de soporte, la clasificación por edad y las notas para la
revisión con una cuenta de prueba que el revisor pueda usar.

## Paso 4: plan de lanzamiento

`launch-plan.md`: una lista de espera o lista beta antes del lanzamiento,
analíticas y seguimiento de errores activos, dónde conversan los usuarios
descontentos del original en cada país (los hilos de Reddit y las comunidades
de la investigación), una publicación en Product Hunt o Hacker News que
empiece por el arreglo, la atención por WhatsApp lista desde el primer día
donde aplique, y los primeros 10 usuarios con los que hablar uno por uno.

## Resultado

`clonar/launch/` completo, con los precios, los métodos de pago y la factura
de cada país, la landing page construida y `listing.py` pasando. Recuérdale al
usuario que verifique los datos de cada país. Siguiente: `/clonar-publicar`.
