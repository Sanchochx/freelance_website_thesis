# US-032 — Liberación del pago al freelancer al completar el pedido

## Historia de Usuario

**Como** freelancer,
**quiero** recibir automáticamente el pago (descontada la comisión de la plataforma) cuando el pedido se marca como completado,
**para** cobrar por mi trabajo sin necesidad de solicitar el pago manualmente.

## Criterios de Aceptación

- [ ] **CA1:** Al marcar un pedido como completado, el sistema libera el escrow automáticamente.
- [ ] **CA2:** La comisión de la plataforma (10%) se descuenta del monto en escrow antes de acreditar al freelancer.
- [ ] **CA3:** El 90% restante se acredita al wallet del freelancer inmediatamente.
- [ ] **CA4:** Se registran dos transacciones: una de tipo `cobro` (90% al freelancer) y una de tipo `comision` (10% a la plataforma).
- [ ] **CA5:** El freelancer recibe una notificación cuando el pago es liberado (ver US-050).
- [ ] **CA6:** El pedido queda en estado `completado` con `fecha_completado` registrada.
- [ ] **CA7:** El cliente solo puede marcar el pedido como completado cuando está en estado `en_revision`.

## Notas Técnicas

- Endpoint: `PATCH /api/orders/{order_id}/complete`
- Tabla(s): `orders`, `transactions`, `users`
- Operación atómica:
  ```
  comision = escrow_retenido * 0.10
  cobro_freelancer = escrow_retenido * 0.90
  users.wallet_balance += cobro_freelancer (freelancer)
  orders.escrow_retenido = 0
  orders.estado = completado
  INSERT INTO transactions (tipo=cobro, monto=cobro_freelancer, user_id=freelancer)
  INSERT INTO transactions (tipo=comision, monto=comision)
  ```
- Autorización: solo el `client_id` del pedido puede ejecutar la acción de completar

## Prioridad
`Alta`

## Estimación
`5` puntos de historia
