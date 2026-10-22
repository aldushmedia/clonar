---
name: clonar-diseno
description: >-
  Reconstruye el sistema de diseño de una app para un clon: roles de color,
  escala tipográfica, espaciado, radios, sombras y cada componente con sus
  estados, como design tokens más especificaciones de componentes, con
  recursos propios en lugar de los logos, íconos, ilustraciones o fuentes con
  licencia del original. Incluye un verificador de contraste WCAG. Úsala
  cuando el usuario diga "iguala el diseño", "reconstruye el sistema de
  diseño", "saca los colores y las fuentes", "haz que se vea como X", "design
  tokens para mi clon", o después de /clonar-arquitecto.
---

# clonar-diseno

Lee `clonar/recon.md` y las capturas de `clonar/screens/`. Escribe
`clonar/design/tokens.json` (plantilla en esta carpeta), `tokens.css`, el
mapeo de Tailwind y `clonar/design/components.md`.

```bash
python3 contrast.py clonar/design/tokens.json     # cada par de texto, con su proporción WCAG
```

## Las reglas

Lo que reconstruyes es el **sistema**: los roles, la escala, los patrones, la
forma en que se comporta un formulario o un modal. Eso no le pertenece a
nadie, y los usuarios lo esperan. Lo que nunca tomas:

- **Logos, íconos, ilustraciones, fotos, sonidos.** Usa un set de íconos
  abierto (Lucide, Phosphor, Heroicons, Tabler, todos MIT o similar) y haz o
  encarga tus propias ilustraciones. No calques las suyas.
- **Fuentes con licencia.** Si el original usa una fuente de pago o
  propietaria, elige una abierta que cumpla la misma función: Inter, Geist,
  IBM Plex, Manrope, Source Serif.
- **Sus textos.** Cada etiqueta y cada estado vacío se escribe desde cero.
- **Su color de marca.** Regístralo como un rol (`accent`), usa un marcador
  neutro por ahora, y clonar-marca te da el tuyo. El color característico
  más el diseño característico forman su imagen comercial (trade dress), y
  eso cambia antes del lanzamiento.

## Paso 1: mide, no adivines

A partir de las capturas (haz zoom, usa un selector de color en el equipo
del usuario):

- **Roles de color**, no colores: bg, surface, border, border-input, text,
  text-muted, accent, on-accent, danger, success, warning. Cuenta cuántos
  grises usa realmente la app. Por lo general, de 5 a 7.
- **Escala tipográfica**: tamaños, interlineados, pesos. Ajústala a una
  escala (12, 14, 16, 20, 28, 40 es común). Anota la categoría de la fuente,
  no el archivo de la fuente.
- **Espaciado**: mide la separación entre elementos. Casi siempre tiene base
  4 u 8. Escribe la escala.
- **Radios, sombras, movimiento**: dos o tres de cada uno.
- **Layout**: ancho máximo del contenido, cuadrícula, breakpoints, ancho de la
  barra lateral, alto del encabezado.

## Paso 2: escribe los tokens

Llena `tokens.json`. Conserva los nombres de los roles. clonar-marca solo
cambia los valores. Genera `tokens.css` como custom properties y mapéalas en
el theme de Tailwind para que los componentes usen `bg-surface text-muted`,
nunca hex directo.

Agrega una lista `pairs` con cada combinación de texto y fondo que usa la
app, y luego:

```bash
python3 contrast.py clonar/design/tokens.json
```

AA es el mínimo: 4.5:1 para el texto normal, 3:1 para el texto grande y para
los bordes de los campos y los anillos de foco. Sale con código 1 si algo
falla. Arréglalo en los tokens, no componente por componente.

## Paso 3: especificaciones de componentes

Para cada componente de la lista del reconocimiento, un bloque en
`components.md`:

```
Button
  variantes  primary, secondary, ghost, danger
  tamaños    sm 32px, md 40px, lg 48px
  estados    default, hover, active, focus-visible (anillo de 2px, accent), disabled, loading
  tokens     bg accent, text on-accent, radius md, font sm/600
  a11y       un <button> real, foco visible, al cargar conserva la etiqueta para lectores de pantalla
  se usa en  S02, S07, S09
```

Cada estado que vio el reconocimiento, más los que debería tener: foco,
deshabilitado, cargando, error, vacío. El comportamiento con teclado y con
lector de pantalla es parte de la especificación.

## Paso 4: construye los primitivos

Construye los componentes en código una sola vez, de forma aislada (una ruta
`/design` o Storybook), antes de cualquier pantalla. Usa una base accesible
si el stack tiene una (Radix, shadcn/ui, React Aria). Toma una captura de la
página. Esa es la verificación del sistema de diseño.

## Resultado

`tokens.json`, `tokens.css`, la configuración de Tailwind, `components.md`,
los primitivos construidos y un reporte de contraste con cero fallas AA.
Siguiente: `/clonar-construir`.
