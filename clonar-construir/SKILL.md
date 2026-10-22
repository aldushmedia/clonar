---
name: clonar-construir
description: >-
  Reconstruye una app pantalla por pantalla a partir del mapa de
  reconocimiento: primero la estructura base de la app, luego el flujo
  principal como un corte vertical, y después cada pantalla con todos sus
  estados, marcando la matriz de funciones a medida que avanza. Escribe cada
  línea desde cero, nunca el código, los recursos ni los textos del original.
  Úsala cuando el usuario diga "construye el clon", "construye la pantalla
  S07", "empieza a construir", "reconstruye esta pantalla", "implementa la
  página de reserva", o después de /clonar-diseno.
---

# clonar-construir

Lee `clonar/recon.md`, `clonar/architecture.md` y `clonar/design/`.
Actualiza `clonar/features.csv` (la columna `clone`) y lleva
`clonar/build-log.md`.

## Las reglas

- **Sala limpia.** Cada línea de código se escribe aquí, a partir del mapa de
  reconocimiento y las especificaciones. Nunca pegues el HTML, el CSS, el
  JavaScript, los SVG ni las imágenes del original, nunca cargues nada desde
  su dominio o su CDN, nunca hagas "ver código fuente y adaptar".
- **Tus palabras.** Escribe desde cero cada etiqueta, botón, estado vacío y
  correo. Igualar lo que hace un botón es paridad. Igualar su frase es copiar.
- **Solo tokens.** Nada de hex ni de valores en píxeles directos en los
  componentes. Si falta un valor, agrégalo a los tokens.

## Paso 1: la estructura base

Rutas para cada pantalla del inventario (las páginas provisionales están
bien), el layout (navegación, encabezado, barra lateral), los tokens
conectados, los primitivos de clonar-diseno y datos de prueba (seed) para
que las pantallas tengan algo real que mostrar. Haz commit.

## Paso 2: el corte vertical

El ciclo principal del mapa de reconocimiento, de punta a punta, antes que
cualquier otra cosa. Para una app de reservas: crear un tipo de evento, abrir
la página pública, reservar un horario, verlo en el panel. Que sea feo está
bien. Lo que importa es que funcione. Si clonar-backend todavía no corrió,
usa los datos de prueba y una capa de datos falsa con las mismas firmas de
funciones, para que cambiarla por la real no modifique el código de ninguna
pantalla.

## Paso 3: pantalla por pantalla

Trabaja en el orden de `architecture.md`. Para cada pantalla:

1. Lee su fila en el mapa de reconocimiento: propósito, componentes, estados,
   qué flujos pasan por ella.
2. Mira la captura de referencia para el layout y la jerarquía. No para los
   píxeles.
3. Constrúyela con los primitivos. Datos reales de la capa de datos.
4. **Cada estado**: vacío, cargando (skeletons, no spinners, si el original
   los usa), con datos, error, sin permiso, contenido largo (un nombre de 60
   caracteres), ancho de móvil.
5. Lo básico, siempre: HTML semántico, etiquetas en los campos, accesible con
   teclado, foco visible, imágenes con texto alternativo.
6. Cambia las filas correspondientes de `features.csv` a `yes` o `partial`
   (con una nota).
7. Toma una captura con el mismo viewport que la referencia y guárdala en
   `clonar/clone-screens/S07.png` para clonar-comparar.
8. Un commit por pantalla: `build: S07 página de reserva`.

## Definición de terminado, por pantalla

- [ ] cada estado del mapa de reconocimiento, más vacío, error y cargando
- [ ] funciona a 390px y a 1440px de ancho
- [ ] solo con teclado: se puede completar el flujo
- [ ] sin errores en la consola
- [ ] sin textos fijos tomados del original
- [ ] features.csv actualizado
- [ ] captura guardada para el diff

## Paso 4: el registro de construcción

`clonar/build-log.md`, una línea por pantalla: ID, fecha, terminada o
parcial, qué falta, qué fue más difícil de lo esperado. Cuando una función
resulte más grande de lo que parecía, dilo en el registro y en el chat. No
publiques la mitad en silencio.

## Cuando no sabes cómo funciona algo

Vuelve al original como usuario: lee su artículo de ayuda, mira su recorrido
público, usa la propia cuenta del usuario. No escarbes en su código ni en sus
llamadas de red. Luego construye tu propia versión de ese comportamiento.

## Resultado

Pantallas construidas, la matriz de funciones actualizada, capturas guardadas
y un resumen: pantallas terminadas del total, imprescindibles terminadas del
total, qué sigue. Luego `/clonar-backend` si la capa de datos todavía es
falsa, o si no `/clonar-probar`.
