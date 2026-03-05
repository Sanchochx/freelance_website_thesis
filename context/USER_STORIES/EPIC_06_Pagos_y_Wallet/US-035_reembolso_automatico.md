# US-035 — Reembolso automático al cancelar un pedido antes de iniciarse

## Historia de Usuario

**Como** cliente,
**quiero** recibir un reembolso automático y total si el pedido es cancelado antes de que el freelancer lo acepte e inicie,
**para** no perder mi dinero por pedidos que no prosperaron.

## Criterios de Aceptación

- [ ] **CA1:** El reembolso se activa automáticamente cuando un pedido en estado `pendiente` es cancelado (por el cliente o por timeout de 48h).
- [ ] **CA2:** El monto completo retenido en escrow se devuelve al wallet del cliente sin descuentos.
- [ ] **CA3:** El reembolso se refleja en el wallet del cliente de forma inmediata.
- [ ] **CA4:** Se registra una transacción de tipo `reembolso` en el historial de ambas partes.
- [ ] **CA5:** El cliente recibe una notificación confirmando el reembolso con el monto devuelto.
- [ ] **CA6:** Si el pedido ya está en estado `en_progreso` o posterior, no aplica reembolso automático (debe gestionarse por soporte).

## Notas Técnicas

- La lógica de reembolso se ejecuta dentro de `PATCH /api/orders/{order_id}/cancel` o `DELETE /api/orders/{order_id}`
- Tabla(s): `orders`, `transactions`, `users`
- Operación atómica:
  ```
  users.wallet_balance += orders.escrow_retenido (cliente)
  orders.escrow_retenido = 0
  orders.estado = cancelado
  INSERT INTO transactions (tipo=reembolso, monto=monto_reembolso, user_id=client_id)
  ```
- Verificar `orders.estado IN ('pendiente')` antes de aplicar reembolso total

## Prioridad
`Alta`

## Estimación
`3` puntos de historia
