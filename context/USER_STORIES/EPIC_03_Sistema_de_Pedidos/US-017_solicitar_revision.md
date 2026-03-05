# US-017 — Solicitar revisión de un pedido

## Historia de Usuario

**Como** cliente,
**quiero** solicitar una revisión si la entrega del freelancer no cumple con lo acordado,
**para** asegurarme de recibir el trabajo según los términos pactados antes de liberar el pago.

## Criterios de Aceptación

- [ ] **CA1:** El cliente solo puede solicitar revisión cuando el pedido está en estado `en_revision` (el freelancer marcó entrega).
- [ ] **CA2:** El cliente debe explicar en un mensaje qué cambios necesita en la revisión.
- [ ] **CA3:** Al solicitar revisión, el pedido regresa al estado `en_progreso` para que el freelancer trabaje en los cambios.
- [ ] **CA4:** El número máximo de revisiones permitidas se define en el paquete contratado (ej. básico: 1, estándar: 2, premium: 3).
- [ ] **CA5:** Si el cliente ha agotado las revisiones, el sistema le informa y le sugiere aceptar la entrega o contactar al soporte.
- [ ] **CA6:** El freelancer recibe una notificación cuando se solicita una revisión.

## Notas Técnicas

- Endpoint: `POST /api/orders/{order_id}/revision`
- Body: `{ "comentario": str }`
- Tabla(s): `orders`
- Campos relevantes: `orders.estado`, `orders.revisiones_usadas`, `orders.revisiones_permitidas`
- Al solicitar: `orders.estado = en_progreso`, `orders.revisiones_usadas += 1`
- Verificar `revisiones_usadas < revisiones_permitidas` antes de permitir la acción

## Prioridad
`Alta`

## Estimación
`3` puntos de historia
