# US-018 — Entregar archivos dentro del pedido

## Historia de Usuario

**Como** freelancer,
**quiero** poder subir y entregar los archivos finales dentro del pedido,
**para** que el cliente los reciba y pueda revisar y aprobar el trabajo.

## Criterios de Aceptación

- [ ] **CA1:** El freelancer puede subir archivos de entrega solo cuando el pedido está en estado `en_progreso`.
- [ ] **CA2:** Se permiten múltiples archivos por entrega; el tamaño máximo por archivo es de 100 MB.
- [ ] **CA3:** Al enviar la entrega, el pedido cambia al estado `en_revision` y el cliente recibe una notificación.
- [ ] **CA4:** El freelancer puede agregar un mensaje descriptivo junto con los archivos de entrega.
- [ ] **CA5:** El cliente puede descargar los archivos de entrega desde la vista del pedido.
- [ ] **CA6:** Si la entrega llega después del tiempo acordado, el sistema lo registra pero no bloquea la entrega.
- [ ] **CA7:** El cliente puede aceptar la entrega (completando el pedido) o solicitar revisión.

## Notas Técnicas

- Endpoint: `POST /api/orders/{order_id}/delivery` (multipart/form-data)
- Tabla(s): `orders`
- Archivos subidos a Cloudinary (raw upload); URLs guardadas en `orders.archivos_entrega` (array JSON)
- Al enviar: `orders.estado = en_revision`, `orders.fecha_entrega = now()`
- Autorización: solo el freelancer del pedido puede entregar

## Prioridad
`Alta`

## Estimación
`5` puntos de historia
