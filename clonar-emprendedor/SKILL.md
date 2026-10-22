---
name: clonar-emprendedor
description: >-
  Investiga la app que se está clonando y lee lo que dicen sus usuarios
  reales en reseñas públicas (App Store, Google Play, G2, Capterra,
  Trustpilot, Reddit, Hacker News, su propio tablero de solicitudes de
  funciones), luego ordena lo que odian, lo que falta y lo que nadie resolvió,
  y lo convierte en un plan de arreglos para el clon y un ángulo de
  posicionamiento que puedas vender. Cada cita es real, textual y enlazada.
  Úsala cuando el usuario diga "qué odia la gente de X", "lee las reseñas",
  "cómo hago que la mía sea mejor", "encuentra el hueco", "qué funciones
  faltan", "cómo lo posiciono", "hazlo vendible", o después de /clonar-comparar.
---

# clonar-emprendedor

Una copia sin cambios de una app no tiene razón para existir. Esta skill
encuentra la razón: lo que los usuarios del original odian, en sus propias
palabras, y lo arregla en la tuya.

Herramienta en esta carpeta:

```bash
python3 reviews.py clonar/reviews.csv --out clonar/feedback.md
```

## Las reglas, que no se negocian

- **Nunca inventes.** Ni reseñas, ni citas, ni calificaciones, ni conteos, ni
  usuarios, ni fuentes inventadas. Si no se puede acceder a una fuente, dilo
  y sigue. Si hay 14 reseñas, di 14.
- **Cada cita es textual y está enlazada.** Copiada exactamente de la
  página, con la URL de la reseña o del hilo. `reviews.py` descarta cualquier
  fila sin enlace.
- **Leer, no extraer datos (scraping).** Lee las páginas de reseñas como lo
  hace una persona, en el navegador, y copia las filas en la hoja. Nada de
  bibliotecas de scraping contra tiendas o sitios de reseñas cuyos términos
  lo prohíben. Los feeds y APIs oficiales y públicos están bien dentro de sus
  términos: el feed RSS de reseñas de clientes de Apple
  (`https://itunes.apple.com/us/rss/customerreviews/id=<APP_ID>/sortBy=mostRecent/json`),
  la API de Algolia de Hacker News (`hn.algolia.com/api/v1/search?query=...`),
  la API oficial de Reddit bajo sus términos.
- **Nunca reseñas falsas.** Ni para tu app, ni en contra de la suya. Es
  ilegal en Estados Unidos (la regla de la FTC de 2024) y en muchos otros
  lugares.
- **Los que escriben reseñas no son tus testimonios.** Sus palabras son
  investigación. No las pongas en tu landing page.

## Paso 1: recolecta

Apunta a más de 100 reseñas de al menos tres fuentes, las más recientes
primero:

| fuente | dónde |
| --- | --- |
| App Store | la página de la app, Calificaciones y reseñas, Ver todo; o el feed RSS de arriba |
| Google Play | la ficha, Ver todas las reseñas, ordenar por más recientes |
| G2, Capterra, Trustpilot | las páginas de reseñas del producto, filtra también de 1 a 3 estrellas |
| Reddit | busca "X alternative", "switched from X", "X sucks", "X vs", y en español "alternativa a X", "me cambié de X", "X no sirve", "X vs" |
| Hacker News | la API de Algolia o la búsqueda del sitio, con las mismas consultas |
| el tablero propio del original | su hoja de ruta pública o tablero de solicitudes (Canny y similares) y los conteos de votos |
| su registro de cambios | lo que ya publicó, para que no "arregles" lo que ya está arreglado |

Cada fila en `clonar/reviews.csv`: `source,url,date,rating,text`, con el
texto copiado exactamente. Lee también las reseñas de 3 y 4 estrellas. "Me
encanta, pero..." es donde se esconden los mejores arreglos.

## Paso 2: ordena

```bash
python3 reviews.py clonar/reviews.csv --out clonar/feedback.md
```

Clasifica las reseñas en temas (`themes.json`, edítalo para la categoría de
la app), le da más peso a las calificaciones bajas y a las reseñas recientes,
marca como débiles los temas con menos de 3 reseñas o una sola
fuente, lista cada solicitud con las propias palabras de los usuarios y
muestra las calificaciones bajas que no coincidieron con ningún tema. Lee esa
última lista a mano. Muchas veces es la mejor parte.

`themes.json` trae patrones en inglés y en español. Los de español cubren
variantes regionales comunes (una app que "se traba", "se cuelga", "se tilda"
o "se queda pegada"; la "clave" o la "contraseña"; la "computadora" o el
"ordenador"), reconocen las palabras con o sin acentos e incluyen un tema de
métodos de pago (efectivo, transferencias, billeteras como Mercado Pago o
Yape). Si tus usuarios usan otras palabras, agrégalas al tema que corresponda
sin quitar las que ya están, y corre `python3 -m unittest discover -s tests`
para confirmar que nada se rompió.

## Paso 3: tres listas

A partir de `feedback.md`, escribe tres listas ordenadas. Cada elemento: el
problema en una línea, cuántas reseñas, cuántas fuentes, una o dos citas
enlazadas.

1. **Lo que odian.** Quejas sobre cosas que hace la app.
2. **Lo que falta.** Funciones que la gente pide por su nombre.
3. **Lo que nadie resolvió.** Trabajos completos o grupos que la app ignora
   ("no está hecha para equipos", "inútil para terapeutas"). Estos se
   convierten en posicionamiento.

Los temas débiles se listan como débiles. No presentes tres comentarios
furiosos de Reddit como una tendencia.

## Paso 4: el plan de arreglos

Elige de 5 a 8, según la evidencia multiplicada por lo barato que sea
arreglarlos. Para cada uno: qué construir o cambiar, el tamaño (S, M, L), qué
skill lo hace y la evidencia. Agrega cada uno a `clonar/features.csv` como
una fila con `original` en `no`. Las quejas de precios y cobros van a
`/clonar-lanzar`.

## Paso 5: el ángulo

Tres opciones de posicionamiento, cada una basada en un tema principal:

```
Para {{quiénes}} que {{odian esto del original, en palabras simples}},
{{tu app}} {{hace esto en su lugar}}.
Evidencia: {{tema}}, {{n}} reseñas en {{n}} fuentes.
```

Recomienda una. Esa define el nombre y la voz de clonar-marca y el hero de
clonar-lanzar. No pongas el nombre del original en el nombre de tu app, en
tus anuncios ni en la ficha de la tienda. Una página de comparación con datos
objetivos es una pregunta legal para un abogado de tu país.

## Resultado

`clonar/reviews.csv`, `clonar/feedback.md`, `clonar/fixes.md` (las tres
listas, el plan de arreglos, el ángulo), filas nuevas en `features.csv` y un
resumen que indique el tamaño de la muestra. Siguiente: `/clonar-marca`.
