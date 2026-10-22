---
name: clonar
description: >-
  Comando maestro del paquete Clonar: guía todo el proceso de clonar una app,
  en orden, desde la exploración hasta la promoción en Instagram. Corre la
  skill de cada etapa, muestra lo que salió y pide la aprobación del usuario
  al final de cada etapa antes de seguir. Lleva el avance en
  clonar/progreso.md para retomar donde quedó. Úsala cuando el usuario diga
  "/clonar", "clona esta app de principio a fin", "quiero clonar X", "guíame
  para clonar una app", "en qué etapa voy", "retoma el clon", o pegue la URL
  de una app que quiere reconstruir sin decir por dónde empezar.
---

# clonar

El comando maestro. No hace el trabajo de cada etapa: eso lo hace la skill de
la etapa. Este comando decide qué etapa sigue, la corre, muestra lo que salió
y espera la aprobación del usuario antes de pasar a la siguiente.

Lee y escribe `clonar/progreso.md` en el proyecto del usuario (plantilla:
`progreso.md` en esta carpeta). Todo lo demás lo escriben las etapas en
`clonar/`.

## Las etapas, en orden

| # | etapa | instrucciones | lo que deja en `clonar/` |
| --- | --- | --- | --- |
| 1 | Explorar | `../clonar-explorar/SKILL.md` | `recon.md`, `features.csv`, `screens/` |
| 2 | Arquitectura | `../clonar-arquitecto/SKILL.md` | `architecture.md` con la sección Países, `schema.sql` |
| 3 | Diseño | `../clonar-diseno/SKILL.md` | `design/` |
| 4 | Construir | `../clonar-construir/SKILL.md` | las pantallas, `build-log.md`, `clone-screens/` |
| 5 | Backend | `../clonar-backend/SKILL.md` | `backend.md` |
| 6 | Probar | `../clonar-probar/SKILL.md` | `test-plan.md`, `bugs.md` |
| 7 | Comparar | `../clonar-comparar/SKILL.md` | `parity.md`, `diffs/` |
| 8 | Emprender | `../clonar-emprendedor/SKILL.md` | `reviews.csv`, `feedback.md`, `fixes.md` |
| 9 | Marca | `../clonar-marca/SKILL.md` | `brand.md`, `brand.json` |
| 10 | Lanzar | `../clonar-lanzar/SKILL.md` | `launch/` |
| 11 | Publicar | `../clonar-publicar/SKILL.md` | `deploy.md` |
| 12 | Redes | `../clonar-redes/SKILL.md` | `redes/reels.md` |

Cada etapa también se puede correr sola con su comando (`/clonar-explorar`,
`/clonar-arquitecto` y así). Este comando las encadena.

## Al empezar

1. Busca `clonar/progreso.md`. Si existe, léelo, di en qué etapa va y qué
   falta, y pregunta si retomar ahí. Si no existe, créalo con la plantilla.
2. Si todavía no hay app elegida, pide la URL de la app y la plataforma (web,
   iOS, Android).
3. Explica en tres líneas cómo va a ser: 12 etapas en orden, cada una termina
   con un resumen y una pregunta de aprobación, y nada se publica sin un visto
   bueno explícito.

## En cada etapa

1. **Anúnciala**: número, nombre, qué va a hacer y qué va a escribir. Marca la
   etapa como "en curso" en `progreso.md`.
2. **Córrela**: lee las instrucciones de la etapa (la ruta de la tabla) y
   síguelas completas, con sus reglas. Si la skill está instalada, también
   puedes invocarla con su comando. Si algo de la etapa contradice este
   archivo, manda la etapa.
3. **Las preguntas de la etapa se hacen dentro de la etapa.** Por ejemplo, la
   etapa 2 pregunta primero en qué país o países se va a lanzar la app. No las
   adivines ni las saltes.
4. **Muestra el resultado**: lo que se escribió (con rutas), las cifras clave
   (pantallas, puntuación de paridad, bugs abiertos, lo que aplique) y los
   riesgos o pendientes.
5. **Pide aprobación**, siempre con esta forma:

   ```
   Etapa N de 12 (nombre) terminada.
   ¿Apruebas para seguir con la etapa N+1 (nombre)?
   Responde: sí / cambios: <qué cambiar> / repetir / saltar / detener
   ```

6. **Espera la respuesta.** No sigas sin un "sí" explícito. El silencio, un
   "ok, veamos" o una pregunta no son aprobación: respóndela y vuelve a
   preguntar.
   - **sí**: anota en `progreso.md` la etapa como aprobada, con la fecha y el
     resumen en una línea, y pasa a la siguiente.
   - **cambios**: haz los cambios dentro de la misma etapa, muestra el
     resultado otra vez y vuelve a pedir aprobación.
   - **repetir**: corre la etapa otra vez desde el principio.
   - **saltar**: solo para las etapas que se pueden saltar (abajo). Di qué se
     pierde, anótala como saltada con el motivo y sigue.
   - **detener**: guarda el avance en `progreso.md` y termina. La próxima vez,
     `/clonar` retoma aquí.

## Lo que no se salta

- **No se pueden saltar**: 1 Explorar, 2 Arquitectura, 4 Construir, 6 Probar,
  9 Marca y 11 Publicar. Las demás se pueden saltar con aprobación.
- **Antes de Publicar**, la verificación previa de clonar-publicar tiene que
  pasar entera (tests, imprescindibles terminados, barrido de marca limpio,
  ficha revisada). Si algo falla, di qué etapa lo arregla y pregunta si volver
  a ella.
- **Si Comparar dice "no se puede publicar"**, propón volver a Construir para
  los faltantes antes de seguir.
- **El "sí" de la etapa 10 no es el visto bueno para publicar.** clonar-publicar
  pide su propio visto bueno antes de poner la app en línea.

## Volver atrás

Si una etapa encuentra un problema de una etapa anterior (por ejemplo, Probar
encuentra una pantalla que falta), dilo así: "Esto es de la etapa 4
(Construir). ¿Vuelvo a esa etapa?". Con un sí, corre la parte de esa etapa que
hace falta, pide su aprobación, y regresa a la etapa en la que ibas. Anota la
vuelta atrás en `progreso.md`.

## Las reglas de todo el paquete

- **Sala limpia**: se reconstruyen funciones y flujos, nunca el código, los
  recursos, los textos ni la marca del original.
- **Solo fuentes públicas y la cuenta del propio usuario.** Nada de scraping
  contra los términos de un sitio ni de saltarse logins o muros de pago.
- **Nada inventado**: ni reseñas, ni cifras, ni testimonios.
- **El usuario crea las cuentas y las claves y compra el dominio.** Claude
  nunca escribe contraseñas, tarjetas ni claves en vivo.
- **Los datos de cada país** (`../clonar-arquitecto/paises.md`) los verifica el
  usuario, y la facturación la confirma un contador local.
- **Nada sale en vivo sin un visto bueno explícito.**

## Resultado

Al aprobar la etapa 12, un resumen final: la app y su URL en vivo, la
puntuación de paridad, los arreglos que la hacen mejor que el original, los
países y sus métodos de pago, los 3 Reels listos para grabar y qué vigilar la
primera semana. `progreso.md` queda con las 12 etapas y sus fechas.
