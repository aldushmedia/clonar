---
name: clonar-explorar
description: >-
  Hace ingeniería inversa de cualquier app y la convierte en un mapa de
  reconocimiento: inventario de pantallas, flujos de usuario, lista de
  componentes, modelo de datos inferido y una matriz de funciones, a partir de
  páginas públicas, capturas, fichas de tiendas de apps, documentación de
  ayuda y la propia cuenta del usuario. Es el primer paso del paquete Clonar.
  Úsala cuando el usuario diga "clona esta app", "haz ingeniería inversa de
  X", "cómo funciona X", "mapea X", "qué pantallas tiene X", "quiero construir
  mi propia versión de X", "copia esta app", o pegue la URL de una app o su
  enlace de App Store y quiera reconstruirla.
---

# clonar-explorar

Todo lo demás del paquete se construye a partir de lo que escribe esta skill.
Un mal mapa de reconocimiento da un mal clon, así que tómate tu tiempo aquí.

El resultado va en el proyecto del usuario:

```
clonar/recon.md        el mapa de reconocimiento (plantilla: recon-map.md en esta carpeta)
clonar/features.csv    la matriz de funciones (plantilla: features.csv en esta carpeta)
clonar/screens/        capturas de referencia del original. Nunca se publican.
```

## Las reglas, antes que nada

Esta skill reconstruye **funciones y patrones de UX**, al estilo sala limpia
(clean room). Estudia lo que hace la app y cómo se mueve un usuario por ella.
No toma nada que le pertenezca a la app.

- **Solo fuentes públicas y la propia cuenta del usuario.** Nunca entres a una
  cuenta que no sea del usuario, nunca pidas una contraseña, nunca te saltes
  un muro de pago o un login con ningún truco.
- **Leer, no extraer datos (scraping).** Sin crawlers, sin descargas masivas,
  sin bucles. Si hay una herramienta de navegador conectada al navegador del
  propio usuario, lee las páginas a velocidad humana con el usuario presente.
- **Sin código fuente, sin APIs privadas.** No leas ni guardes los bundles de
  JavaScript de la app, no descompiles su binario ni registres sus llamadas
  de red para copiar endpoints. Leer la documentación pública de su API está
  bien.
- **Revisa los términos.** Los términos de algunos productos prohíben usar una
  cuenta para construir un producto competidor. Si la cuenta del usuario está
  bajo términos así, dilo y trabaja solo con fuentes públicas.
- **Las capturas son de referencia.** Viven en `clonar/screens/`, se usan
  para comparar diseños y nunca entran al clon.

## Paso 1: alcance

Pregunta tres cosas, o propón respuestas y consigue un sí:

1. **Qué app y qué plataforma.** Web, iOS, Android, escritorio.
2. **Qué parte.** "Todo Notion" no es un proyecto. "Las páginas, los bloques
   y la opción de compartir de Notion" sí lo es. Por defecto, el ciclo
   principal: el flujo por el que pagan los usuarios.
3. **Para quién es.** El negocio del propio usuario, un nicho, un producto
   para vender.

## Paso 2: lista las fuentes

Primero arma una tabla de fuentes, con una URL en cada fila. En orden de
valor:

| fuente | qué te da |
| --- | --- |
| centro de ayuda / documentación | la lista de funciones más completa que existe, y la configuración |
| página de precios | qué funciones importan (las ponen detrás del pago) |
| registro de cambios (changelog) | qué se agregó hace poco, qué cree importante el equipo |
| ficha de la tienda de apps | capturas de cada pantalla clave, el discurso, las calificaciones |
| videos públicos de recorrido | flujos reales, clic por clic |
| sitio de marketing | posicionamiento, el ciclo principal en sus palabras |
| la propia cuenta del usuario | lo real, cada estado, manejado por el usuario |
| documentación pública de la API | el modelo de datos, casi gratis |

## Paso 3: inventario de pantallas

Una fila por pantalla. Los ID son estables: S01, S02... Todos los demás
archivos se refieren a ellos.

`ID | pantalla | ruta o cómo se llega | propósito | componentes clave | estados vistos`

Los estados importan: vacío, cargando, con datos, error, permiso denegado,
móvil. Un estado vacío que no registraste es un estado vacío que no vas a
construir.

## Paso 4: flujos de usuario

F01, F02... Cada uno es un objetivo y las pantallas por las que pasa:

```
F01 El invitado reserva una reunión
    S07 página de reserva -> S08 elegir horario -> S09 formulario de datos -> S10 confirmado
    límite: no hay horarios esta semana, la zona horaria es distinta, el horario se ocupa mientras llena el formulario
```

Cuenta los clics del camino feliz. Ese es el número a superar.

## Paso 5: componentes

Cada parte de la interfaz que se repite: botones, campos, selectores de fecha,
modales, tablas, avisos (toasts), navegación. Nombre, variantes, estados, qué
pantallas lo usan. Esto se convierte en la lista de componentes de
clonar-diseno.

## Paso 6: modelo de datos inferido

Entidades, campos y relaciones, cada uno con su evidencia y un nivel de
confianza:

```
Booking  id, event_type_id, start_at, end_at, guest_name, guest_email,
         status (confirmed | cancelled | rescheduled), answers (json)
         evidencia: campos del formulario S09, confirmación S10, artículo de ayuda "Cancelar una reserva"
         confianza: alta
```

Marca las suposiciones como suposiciones. clonar-arquitecto convierte esto en
un esquema real.

## Paso 7: matriz de funciones

Escribe `clonar/features.csv` (columnas: feature, area, priority, original,
clone, notes). La prioridad es must / should / could (imprescindible,
deseable, opcional). `clone` empieza en `no` en cada fila y se va llenando
durante la construcción. clonar-comparar le pone la puntuación.

## Paso 8: lo que no se puede clonar

Haz la lista con honestidad, como filas `skip` con un motivo: contenido con
licencia (un catálogo de música, un banco de imágenes), la red y sus
usuarios, los datos que le pertenecen a la app, acuerdos con socios,
hardware, licencias reguladas (banca, salud). "Clonar cualquier app"
significa las funciones y el flujo, no lo que la app tiene.

## Paso 9: estima el tamaño

Pantallas, flujos, entidades y las partes difíciles (tiempo real,
sincronización, pagos, integraciones de calendario o correo, modo sin
conexión). Da un tamaño: S (un fin de semana), M (unas semanas), L (un
trimestre), XL (redefine el alcance). Sin promesas de un clon perfecto.

## Resultado

`clonar/recon.md` y `clonar/features.csv`, y luego un resumen de cinco
líneas: el ciclo principal, la cantidad de pantallas y flujos, las tres
partes más difíciles, lo que queda fuera del alcance y el siguiente paso:
`/clonar-arquitecto`.
