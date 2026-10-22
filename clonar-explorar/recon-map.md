# Mapa de reconocimiento: {{app}} ({{plataforma}})

Alcance: {{la parte que se clona}}
Para: {{para quién es el clon}}
Fecha: {{AAAA-MM-DD}}

## Fuentes

| # | fuente | URL | notas |
| --- | --- | --- | --- |
| 1 | centro de ayuda | | |

## Ciclo principal

{{una oración: lo que pagan los usuarios}}

## Pantallas

| ID | pantalla | ruta / cómo se llega | propósito | componentes clave | estados vistos |
| --- | --- | --- | --- | --- | --- |
| S01 | | | | | vacío, con datos, error |

## Flujos

```
F01 {{objetivo}}
    S01 -> S02 -> S03
    clics del camino feliz: {{n}}
    límite: {{casos}}
```

## Componentes

| componente | variantes | estados | se usa en |
| --- | --- | --- | --- |
| Botón | primario, secundario, fantasma, peligro | normal, hover, foco, deshabilitado, cargando | todas |

## Modelo de datos inferido

```
{{Entidad}}  {{campos}}
             evidencia: {{ID de pantallas, artículos de ayuda}}
             confianza: alta | media | suposición
```

Relaciones: {{User 1-n EventType, EventType 1-n Booking, ...}}

## Matriz de funciones

Ver `features.csv`. Must: {{n}}, should: {{n}}, could: {{n}}, skip: {{n}}.

## Fuera del alcance (no se puede o no se debe clonar)

- {{contenido con licencia, la red, acuerdos con socios, ...}}

## Tamaño

Pantallas {{n}}, flujos {{n}}, entidades {{n}}. Partes difíciles: {{lista}}. Tamaño: {{S|M|L|XL}}.
