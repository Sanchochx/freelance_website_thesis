# US-031 — Pago en escrow al crear un pedido

## Historia de Usuario

**Como** cliente,
**quiero** que mi pago quede retenido de forma segura en escrow al crear un pedido,
**para** tener la garantía de que el dinero solo se liberará al freelancer cuando el trabajo sea completado satisfactoriamente.

## Criterios de Aceptación

- [ ] **CA1:** Al crear un pedido, el monto del paquete seleccionado se descuenta automáticamente del wallet del cliente.
- [ ] **CA2:** El monto queda retenido en escrow (campo `orders.escrow_retenido`) y no está disponible para el cliente mientras el pedido está activo.
- [ ] **CA3:** El cliente puede ver en su wallet el desglose entre saldo disponible y saldo en escrow.
- [ ] **CA4:** Si el cliente no tiene saldo suficiente, el pedido no se puede crear y se le indica cuánto le falta.
- [ ] **CA5:** El dinero en escrow se libera al freelancer solo cuando el pedido cambia a estado `completado`.
- [ ] **CA6:** Si el pedido es cancelado, el dinero en escrow regresa automáticamente al wallet del cliente.

## Notas Técnicas

- La lógica de escrow es parte del flujo de `POST /api/orders`
- Tabla(s): `orders`, `users`, `transactions`
- Operación atómica: `BEGIN TRANSACTION; users.wallet_balance -= monto; orders.escrow_retenido = monto; INSERT INTO transactions(...); COMMIT;`
- El saldo disponible = `users.wallet_balance` (el escrow se almacena por separado en `orders`)
- No hay una tabla de escrow independiente: el escrow vive en `orders.escrow_retenido`

## Prioridad
`Alta`

## Estimación
`5` puntos de historia
