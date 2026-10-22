# Lista de despliegue: {{tu app}}

Fecha: {{AAAA-MM-DD}}  Commit: {{sha}}  Visto bueno del usuario: {{sí / todavía no}}

## Verificación previa (todo tiene que pasar)

- [ ] suite e2e en verde: {{n pasaron / n}}
- [ ] sin bugs S1 ni S2 abiertos
- [ ] paridad: todas las imprescindibles terminadas ({{n/n}}), puntuación de funciones {{n}}
- [ ] barrido de marca limpio (`sweep.py` sale con código 0)
- [ ] la ficha de la tienda pasa (`listing.py` sale con código 0), si se publica en tiendas
- [ ] el build de producción pasa
- [ ] política de privacidad y términos publicados, con cada proveedor que procesa datos
- [ ] el borrado de cuenta funciona
- [ ] el favicon, los títulos, la imagen OG, los correos y el ícono de la app son tuyos

## Producción

- [ ] base de datos de producción separada, respaldos activados, migraciones en el despliegue
- [ ] variables de entorno configuradas (los nombres coinciden con .env.example)
- [ ] pagos en vivo en cada país: productos, precios, endpoint del webhook + secreto, una compra real reembolsada por método
- [ ] facturación electrónica en producción en cada país que la exige, primer comprobante revisado
- [ ] las URI de redirección y los orígenes de OAuth incluyen el dominio de producción
- [ ] verificación OAuth de Google aprobada (si usas scopes sensibles)
- [ ] dominio de envío de correo verificado

## Dominio

- [ ] A @ -> {{valor}}
- [ ] CNAME www -> {{valor}}
- [ ] SPF, DKIM, DMARC configurados
- [ ] host canónico elegido, el otro redirige
- [ ] HTTPS válido

## Vigilancia

- [ ] seguimiento de errores
- [ ] monitoreo de disponibilidad
- [ ] analíticas
- [ ] flujo principal hecho en el sitio en vivo, en escritorio y en el teléfono
