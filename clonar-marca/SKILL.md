---
name: clonar-marca
description: >-
  Le da nombre y una marca nueva al clon de una app para que sea del propio
  usuario: candidatos de nombre con las verificaciones de marca registrada,
  dominio, tiendas y usuarios en redes que hay que correr, una paleta nueva
  revisada por contraste, un brief de logo, una guía de voz y una herramienta
  de barrido que encuentra cualquier resto del original en el código. Úsala
  cuando el usuario diga "ponle nombre a mi app", "cambia la marca del clon",
  "hazlo mío", "elige un nombre y colores", "brief de logo", "voz de marca",
  "busca restos del original", o después de /clonar-emprendedor. Siempre
  corre antes de /clonar-lanzar.
---

# clonar-marca

Nada se lanza con la identidad del original. Esta skill es la línea entre
"un clon" y "tu app".

Herramienta en esta carpeta:

```bash
python3 sweep.py . --avoid "Original Name,Its Company" --domains original.com --colors "#006bff"
python3 sweep.py . --config clonar/brand.json        # lo mismo, desde el archivo de marca
```

Escribe `clonar/brand.md` y `clonar/brand.json` (`avoid`, `domains`,
`colors`, que usan `sweep.py`, `listing.py` y clonar-publicar).

## Paso 1: el nombre

Lee el ángulo en `clonar/fixes.md`. Genera 20 candidatos de distintos
estilos: descriptivo (Booklink), compuesto (Slotwise), inventado (Calvo),
metáfora (Harbor), verbo (Book). Luego quédate con 5 usando estos filtros:

- **Que no se parezca de forma confusa al original** en sonido, aspecto o
  significado, ni a ninguna otra app de la misma categoría. Esa es la prueba
  que usan las oficinas de marcas, así que es la prueba aquí. Sin juegos de
  palabras con su nombre, sin un gemelo con "-ly".
- Corto, fácil de escribir después de oírlo una vez, sin significados
  incómodos en los idiomas grandes.
- Dice algo sobre el ángulo, o por lo menos no va en su contra.

## Paso 2: las verificaciones, corridas, no supuestas

Para cada uno de los 5, una fila por verificación. Marca cada una como **por
correr**, o con el resultado y la fecha en que se corrió. Nunca escribas
"disponible" en una verificación que nadie corrió.

| verificación | dónde |
| --- | --- |
| marca en EE. UU. | tmsearch.uspto.gov, la clase de la app (por lo general 9 y 42) |
| marca en la UE | eSearch de euipo.europa.eu, o TMview para muchas oficinas |
| Canadá | base de datos de marcas de ised-isde.canada.ca |
| global | WIPO Global Brand Database |
| dominio | `whois name.com`, o la búsqueda del registrador |
| App Store y Play | busca el nombre exacto |
| usuarios en redes | X, Instagram, TikTok, GitHub |
| la web | busca "nombre + categoría" |

Estas son verificaciones preliminares, no una autorización legal. Antes de
gastar dinero en el nombre, un abogado de marcas debería hacer una búsqueda
formal.

## Paso 3: paleta

Una paleta nueva, escrita en los mismos roles de tokens que configuró
clonar-diseno. Elige un tono principal de marca de una familia distinta a la
del original (si el suyo es azul, el tuyo no es un azul parecido). Luego:

```bash
python3 ../clonar-diseno/contrast.py clonar/design/tokens.json
```

Cero fallas AA. Agrega los colores de marca del original a `brand.json` para
que el barrido atrape los que sobrevivan.

## Paso 4: brief de logo

No un logo, sino un brief para quien lo haga (el usuario, un diseñador, un
modelo de imágenes):

- la idea en una línea, ligada al nombre y al ángulo
- tipo de marca: logotipo, símbolo más logotipo, o monograma
- tiene que funcionar a 16px (favicon) y como ícono de app de 1024px
- entregables: SVG, ícono de app de 1024x1024 sin transparencia para iOS,
  set de favicons, imagen para redes de 1200x630
- **no debe parecerse a la marca del original**: ni una forma compartida, ni
  un par de colores, ni un truco con las letras. Pon el logo del original
  junto a los borradores y compáralos.

## Paso 5: voz

Tres palabras para cómo suena, con lo que cada una no significa ("directa,
no brusca"). Cinco pares de lo que sí y lo que no. Luego reescribe con esa voz
los 10 textos más vistos del clon (el registro, los estados vacíos, el botón
principal, la confirmación, el error). Todo desde cero, nada que haga eco de
las frases del original.

## Paso 6: el barrido

Reemplaza cada nombre, color y texto provisional. Luego:

```bash
python3 sweep.py . --config clonar/brand.json
```

Busca en el contenido y en los nombres de los archivos el nombre del original
(también dentro de identificadores como `CalendlyEmbed`), sus dominios y sus
colores, y se salta `node_modules`, los archivos de build y la carpeta de
planeación `clonar/`. Si sale con código 1, todavía queda algo. Arregla hasta
que diga que está limpio (Limpio). Revisa también a ojo: el favicon, los
títulos de las páginas, las plantillas de correo, la imagen OG, el ícono de
la app.

## Resultado

`clonar/brand.md` (el nombre con sus verificaciones, la paleta, el brief de
logo, la voz), `clonar/brand.json`, los tokens actualizados, los textos
reescritos y un barrido limpio. Siguiente: `/clonar-lanzar`.
