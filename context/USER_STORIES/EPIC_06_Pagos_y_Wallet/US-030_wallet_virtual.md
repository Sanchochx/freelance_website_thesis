# US-030 — Wallet virtual en COP

## Historia de Usuario

**Como** usuario registrado (cliente o freelancer),
**quiero** tener una wallet virtual dentro de la plataforma con saldo en pesos colombianos,
**para** gestionar mis pagos y cobros sin depender de transferencias externas en cada transacción.

## Criterios de Aceptación

- [ ] **CA1:** Todo usuario tiene una wallet creada automáticamente al registrarse, con saldo inicial de COP $0.
- [ ] **CA2:** El saldo actual de la wallet es visible en el dashboard del usuario.
- [ ] **CA3:** El usuario puede ver el desglose de su saldo: disponible y retenido en escrow (si aplica).
- [ ] **CA4:** El saldo nunca puede ser negativo; el sistema impide operaciones que lo lleven a valores negativos.
- [ ] **CA5:** El saldo se actualiza en tiempo real tras cada transacción (pago, cobro, recarga, retiro).
- [ ] **CA6:** Las transacciones que afectan el saldo quedan registradas en el historial de transacciones.

## Notas Técnicas

- Endpoint saldo: `GET /api/wallet`
- Response: `{ "saldo_disponible": float, "saldo_en_escrow": float, "saldo_total": float }`
- Tabla(s): `users`, `transactions`
- El saldo se almacena en `users.wallet_balance`
- El saldo en escrow se calcula sumando `orders.escrow_retenido` de pedidos activos del usuario
- Todas las operaciones de saldo deben ser atómicas (transacciones de BD) para evitar inconsistencias
- **Contexto Sandbox:** el saldo en la wallet representa dinero de prueba en COP; se alimenta desde MercadoPago Sandbox usando tarjetas y usuarios de prueba. No se opera con dinero real en este proyecto

## Prioridad
`Alta`

## Estimación
`3` puntos de historia
