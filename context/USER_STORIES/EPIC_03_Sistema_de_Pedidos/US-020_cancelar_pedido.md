# US-020 — Cancelar un pedido antes de que inicie

## Historia de Usuario

**Como** cliente,
**quiero** poder cancelar un pedido antes de que el freelancer lo acepte,
**para** recuperar mi dinero si cambio de opinión o encuentro una mejor alternativa.

## Criterios de Aceptación

- [ ] **CA1:** El cliente solo puede cancelar un pedido cuando está en estado `pendiente` (antes de que el freelancer lo acepte).
- [ ] **CA2:** Al cancelar, el cliente recibe un reembolso total del monto retenido en escrow a su wallet.
- [ ] **CA3:** El pedido cambia al estado `cancelado` de forma inmediata.
- [ ] **CA4:** El freelancer recibe una notificación informando que el pedido fue cancelado antes de su respuesta.
- [ ] **CA5:** No es posible cancelar un pedido en estado `en_progreso` o posterior directamente; el cliente debe contactar soporte.
- [ ] **CA6:** El sistema registra el motivo de cancelación si el cliente lo proporciona (campo opcional).

## Notas Técnicas

- Endpoint: `DELETE /api/orders/{order_id}` o `PATCH /api/orders/{order_id}/cancel`
- Tabla(s): `orders`, `transactions`, `users`
- Verificar `orders.estado = 'pendiente'` antes de permitir la cancelación
- Al cancelar: `users.wallet_balance += escrow_retenido` (cliente), `orders.escrow_retenido = 0`, `orders.estado = cancelado`
- Se registra transacción de tipo `reembolso` en `transactions`
- Autorización: solo el `client_id` del pedido puede cancelar

## Prioridad
`Alta`

## Estimación
`3` puntos de historia
