# Plan de pruebas: {{tu app}}

Build: {{commit}}  Fecha: {{AAAA-MM-DD}}  Entorno: local, datos de prueba

| caso | flujo | tipo | pasos | esperado | auto | resultado |
| --- | --- | --- | --- | --- | --- | --- |
| F01-H1 | el invitado reserva una reunión | feliz | abrir /u/demo/30min, elegir mañana a las 10:00, llenar el formulario, enviar | pantalla de confirmación, reserva en el panel del anfitrión, correo para ambos | e2e | |
| F01-E1 | | límite: el horario se ocupa mientras llena el formulario | | mensaje claro, elegir otro horario, sin reserva doble | e2e | |
| F01-E2 | | límite: invitado en otra zona horaria | | horarios mostrados en la zona del invitado, guardados en UTC | e2e | |
| F01-N1 | | negativo: tarjeta rechazada | | se muestra un error, no se crea la reserva | manual | |
