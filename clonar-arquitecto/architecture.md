# Arquitectura: {{tu app}} (una reconstrucción de las funciones principales de {{app}})

## Países

Lanzamiento en: {{países}}  Después: {{países, o ninguno}}
Datos tomados de `paises.md` el {{AAAA-MM-DD}}. Verificados por el usuario: {{sí / todavía no}}

| país | moneda | métodos de pago | pasarela | facturación electrónica | impuesto en el precio | WhatsApp |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

## Stack

| capa | elección | por qué |
| --- | --- | --- |
| web | | |
| base de datos | | |
| autenticación | | |
| pagos | | |
| facturación electrónica | | |
| correo | | |
| WhatsApp | | |
| tareas | | |
| hosting | | |

## Esquema

Tablas: {{n}}. Reglas de acceso: {{RLS | verificaciones en la capa de datos}}.

```sql
-- o ver clonar/schema.sql
```

## API

| método ruta | hace | quién | entrada | salida | flujo |
| --- | --- | --- | --- | --- | --- |

Webhooks de entrada: {{...}}  Webhooks de salida: {{...}}
Tareas: {{nombre, horario, qué hace}}

## Las partes que muerden

- zonas horarias:
- idempotencia:
- condiciones de carrera:
- pagos asíncronos:
- facturación por país:

## Orden de construcción

1. Corte vertical: {{pantallas, tablas, rutas}}
2. Imprescindibles:
3. Deseables:
4. Arreglos de clonar-emprendedor:
