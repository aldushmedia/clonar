---
name: clonar-probar
description: >-
  Recorre cada flujo del clon de una app y lo prueba en busca de bugs: un
  plan de pruebas generado a partir de los flujos del reconocimiento con
  caminos felices y casos límite, tests end-to-end con Playwright donde se
  pueda, un recorrido en el navegador donde no, y reportes de bugs con un
  formato fijo con severidad, pasos y evidencia. Úsala cuando el usuario diga
  "prueba mi clon", "encuentra bugs", "haz QA de esto", "recorre todo",
  "escribe tests e2e", "¿funciona?", o después de /clonar-construir o
  /clonar-backend.
---

# clonar-probar

Lee los flujos de `clonar/recon.md`. Escribe `clonar/test-plan.md`,
`clonar/bugs.md` y tests end-to-end en el proyecto (`e2e/`). Plantillas en
esta carpeta: `test-plan.md`, `bug-report.md`, `e2e.example.spec.ts`.

## La regla

**Prueba tu clon, no el original.** Nunca hagas pruebas de carga, fuzzing,
scripts ni bombardeos contra los servidores de la app original. Usar el
original a mano, como un usuario normal, para ver cómo se comporta está bien.

## Paso 1: el plan

Para cada flujo F01, F02... del mapa de reconocimiento, escribe:

- **Camino feliz**: los pasos, y lo que el usuario debería ver al final.
- **Casos límite** que apliquen. Recorre esta lista en cada flujo:
  entrada vacía, entrada muy larga, emoji y acentos, dos pestañas a la vez,
  doble clic en enviar, botón atrás a mitad del flujo, recargar a mitad del
  flujo, red lenta, sin conexión, sesión expirada, datos de un segundo
  usuario (deben ser invisibles), zonas horarias y horario de verano, ancho
  de móvil, solo teclado, etiquetas para lectores de pantalla.
- **Casos negativos**: contraseña incorrecta, tarjeta rechazada (tarjeta de
  prueba de Stripe `4000 0000 0000 0002`), permiso denegado, registro
  borrado.

Numera cada caso: F01-H1, F01-E3, F01-N2.

## Paso 2: automatiza lo que puedas

Playwright, un spec por flujo, contra el servidor de desarrollo local con
datos de prueba. Usa roles y etiquetas como selectores
(`getByRole('button', { name: 'Book' })`), nunca clases CSS. Mira
`e2e.example.spec.ts`.

```bash
npm i -D @playwright/test && npx playwright install chromium
npx playwright test
```

Agrega a cada spec: que falle con errores en la consola, que falle con
cualquier respuesta 5xx, y un análisis de accesibilidad con axe
(`@axe-core/playwright`) en cada pantalla.

## Paso 3: recorre el resto a mano

Lo que no se puede automatizar (que lleguen los correos, OAuth con
proveedores reales, pagos de punta a punta, fallas visuales) recibe una
pasada manual. Si hay una herramienta de navegador disponible, maneja con
ella el clon local y toma una captura en cada paso. Si no, dale al usuario la
lista de verificación y espera sus respuestas.

## Paso 4: reporta los bugs

Cada bug va en `clonar/bugs.md` con el formato de `bug-report.md`: un ID,
una severidad, pasos exactos, lo esperado, lo que pasó y la evidencia.
Severidad:

| | significa |
| --- | --- |
| S1 | pérdida de datos, hueco de seguridad, pagos incorrectos, flujo principal bloqueado |
| S2 | una función rota, sin alternativa |
| S3 | rota pero con alternativa, o visiblemente mal |
| S4 | cosmético |

Reporta solo lo que reprodujiste. Lo que "podría ser un problema" va en una
lista aparte de "por revisar".

## Paso 5: ciclo de arreglos

Arregla primero S1 y S2. Para cada arreglo: escribe primero el test que
falla, arregla, mira cómo pasa y conserva el test. Vuelve a correr toda la
suite después de cada tanda. Actualiza `bugs.md` con el commit que arregló
cada uno.

## Resultado

`test-plan.md`, los specs, `bugs.md` y un resumen: casos ejecutados, los que
pasaron, los que fallaron, bugs por severidad y los arreglados hasta ahora.
No publiques nada con un S1 abierto. Siguiente: `/clonar-comparar`.
