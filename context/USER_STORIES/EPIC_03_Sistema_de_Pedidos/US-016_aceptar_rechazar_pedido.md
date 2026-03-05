# US-016 — Aceptar o rechazar un pedido

## Historia de Usuario

**Como** freelancer,
**quiero** poder aceptar o rechazar los pedidos que recibo,
**para** gestionar mi carga de trabajo y comprometer mi tiempo solo en proyectos que puedo atender.

## Criterios de Aceptación

- [ ] **CA1:** El freelancer recibe una notificación y puede ver el pedido entrante en su dashboard.
- [ ] **CA2:** El freelancer puede aceptar o rechazar el pedido dentro de las primeras 48 horas.
- [ ] **CA3:** Al aceptar, el pedido cambia de estado `pendiente` a `en_progreso`.
- [ ] **CA4:** Al rechazar, el pedido cambia a `cancelado` y el cliente recibe un reembolso total automático a su wallet.
- [ ] **CA5:** Si el freelancer no responde en 48 horas, el pedido se cancela automáticamente y se reembolsa al cliente.
- [ ] **CA6:** El freelancer puede agregar un mensaje al cliente al aceptar o rechazar.
- [ ] **CA7:** Una vez aceptado, el pedido no puede volver a `pendiente`.

## Notas Técnicas

- Endpoint: `PATCH /api/orders/{order_id}/status`
- Body: `{ "accion": "aceptar|rechazar", "mensaje": str (opcional) }`
- Tabla(s): `orders`, `transactions`, `users`
- Al rechazar: `users.wallet_balance += escrow_retenido` (cliente), `orders.escrow_retenido = 0`, `orders.estado = cancelado`
- Job programado para cancelación automática tras 48h sin respuesta (cron job o Celery Beat)
- Autorización: solo el freelancer del pedido puede ejecutar esta acción

## Prioridad
`Alta`

## Estimación
`5` puntos de historia
