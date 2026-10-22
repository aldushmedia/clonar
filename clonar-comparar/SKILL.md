---
name: clonar-comparar
description: >-
  Compara el clon de una app con el original: una puntuación de paridad de
  funciones a partir de la matriz de funciones (ponderada por must, should y
  could) con la lista de lo que falta en orden de construcción, más una
  comparación del layout de las capturas que ignora el color, para que un
  cambio de marca no cuente en tu contra. Dos herramientas de Python con la
  biblioteca estándar. Úsala cuando el usuario diga "qué tan cerca está mi
  clon", "compáralo con el original", "qué falta", "revisa la paridad",
  "compara las pantallas", "¿está listo?", o después de /clonar-probar.
---

# clonar-comparar

Dos herramientas en esta carpeta, ambas en Python con la biblioteca
estándar, sin nada que instalar:

```bash
python3 parity.py clonar/features.csv                         # paridad de funciones + lista de faltantes
python3 imgdiff.py clonar/screens/S07.png clonar/clone-screens/S07.png --out diff-S07.png
python3 imgdiff.py a.png b.png --json > clonar/diffs/S07.json # para parity.py --visual
python3 parity.py clonar/features.csv --visual clonar/diffs/*.json --markdown > clonar/parity.md
```

## Qué significa paridad aquí

**Paridad significa que hace el mismo trabajo, no que se ve igual.** La
puntuación de funciones es el número que importa: si un usuario puede hacer
todo lo que podía hacer en el original. La puntuación de layout revisa la
estructura (si la información está en los mismos lugares, con la misma
jerarquía), porque eso es lo que hace que alguien que se cambia se sienta en
casa. Ignora el color a propósito, porque clonar-marca cambia cada color a
propósito. No persigas la paridad de píxeles con el original. Su aspecto
exacto es su imagen comercial (trade dress), y eso cambia antes del
lanzamiento.

## Paso 1: paridad de funciones

Asegúrate de que `clonar/features.csv` esté al día: la columna `clone` de
cada fila es `yes`, `partial` (con una nota), `no` o `skip` (con un motivo).
Luego:

```bash
python3 parity.py clonar/features.csv
```

Pondera must con 3, should con 2 y could con 1, cuenta `partial` como la
mitad, deja fuera las filas `skip` y las filas que agregaste que el original
no tiene, e imprime: la puntuación, las imprescindibles terminadas del total,
cada área de la más débil a la más fuerte y la lista de faltantes en orden de
construcción. Si faltan imprescindibles, no se puede publicar, y lo dice.

## Paso 2: comparación del layout

Para cada pantalla clave, toma dos capturas con el **mismo viewport**
(1440x900 escritorio, 390x844 móvil) en el **mismo estado** (misma forma de
datos, misma pestaña abierta, con la sesión iniciada de la misma manera). Las
del original salen de páginas públicas o de la propia cuenta del usuario y se
guardan en `clonar/screens/`. Las del clon van en `clonar/clone-screens/`.

```bash
python3 imgdiff.py clonar/screens/S07.png clonar/clone-screens/S07.png --out clonar/diffs/S07.png
```

El modo layout (por defecto) convierte ambas en mapas de bordes, las corta en
una cuadrícula y compara dónde están las cosas, puntuando solo las celdas que
tienen algo. Reporta la puntuación con su veredicto (coincide 90+, cerca 75+, parcial
50+, distinto), las regiones que difieren (en las coordenadas en píxeles del
original, de la más grande a la más pequeña) y una diferencia de altura si la
página del clon es mucho más larga o más corta. Las capturas retina y no
retina se comparan bien: ambas se escalan al mismo ancho.

`--mode pixel` es una comparación exacta. Úsala para tus propias regresiones
(el clon de hoy contra el clon de la semana pasada), no contra el original.

## Paso 3: comparación del comportamiento

Recorre cada flujo en ambas apps y compara lo que las puntuaciones no pueden
ver: clics para terminar el flujo principal, qué pasa con los errores, qué se
recuerda entre visitas, qué correos llegan. Menos clics que el original es
una victoria. Escribe cada diferencia así: flujo, lo que hace el original, lo
que hace el clon, arreglar o mantener.

## Paso 4: el reporte

`clonar/parity.md`: puntuación general, puntuación de funciones, puntuación
de layout por pantalla, funciones faltantes en orden de construcción,
diferencias de comportamiento y un veredicto:

- **no se puede publicar**: falta alguna imprescindible, o hay algún bug S1
  abierto
- **se puede publicar**: todas las imprescindibles terminadas, puntuación de
  funciones de 80 o más, sin S1 ni S2 abiertos
- **mejor que el original**: se puede publicar, y además tiene los arreglos
  de clonar-emprendedor. Este es el objetivo. Una copia sin cambios no
  tiene razón para existir.

Da números honestos. Un clon al 62% está al 62%.

## Resultado

`clonar/parity.md`, las imágenes de diferencias y las cinco cosas más
importantes que construir a continuación. Luego `/clonar-construir` para los
huecos, o `/clonar-emprendedor` si ya hay paridad.
