# US-050 — Notificación al freelancer cuando se libera su pago

## Historia de Usuario

**Como** freelancer,
**quiero** recibir una notificación (en la plataforma y por email) cuando el cliente aprueba mi entrega y se libera mi pago,
**para** saber cuándo el dinero está disponible en mi wallet y confirmar que el pedido fue exitoso.

## Criterios de Aceptación

- [ ] **CA1:** Al completarse un pedido, el freelancer recibe una notificación inmediata dentro de la plataforma.
- [ ] **CA2:** Simultáneamente, el freelancer recibe un email de confirmación de pago liberado.
- [ ] **CA3:** La notificación y el email muestran: nombre del cliente, servicio, monto bruto, comisión descontada y monto neto recibido.
- [ ] **CA4:** La notificación incluye un enlace al historial de transacciones para ver el cobro.
- [ ] **CA5:** El email llega en los primeros 2 minutos tras la liberación del pago.
- [ ] **CA6:** La notificación en plataforma persiste en el centro de notificaciones hasta ser marcada como leída.

## Notas Técnicas

- Disparador: `PATCH /api/orders/{order_id}/complete` (cuando el cliente aprueba)
- Tabla(s): `notifications`, `users`, `transactions`
- Notificación en plataforma: INSERT en `notifications (user_id=freelancer_id, tipo='pago_liberado', mensaje=...)`
- Email: enviado de forma asíncrona con `FastAPI-Mail`
- Se envía vía WebSocket al freelancer si está conectado (evento `payment_released`)
- El mensaje de la notificación: `"¡Pago liberado! Has recibido COP $X por el pedido '{nombre_servicio}'."`

## Prioridad
`Alta`

## Estimación
`3` puntos de historia
