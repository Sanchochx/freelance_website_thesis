# US-015 — Crear un pedido

## Historia de Usuario

**Como** cliente,
**quiero** seleccionar un paquete de servicio y crear un pedido,
**para** contratar al freelancer y comenzar el trabajo.

## Criterios de Aceptación

- [ ] **CA1:** Solo usuarios con rol `client` o `freelancer` (actuando como cliente) pueden crear pedidos.
- [ ] **CA2:** El cliente selecciona uno de los paquetes disponibles (básico, estándar o premium) antes de confirmar.
- [ ] **CA3:** El sistema verifica que el cliente tiene saldo suficiente en su wallet antes de confirmar el pedido.
- [ ] **CA4:** Al confirmar, el monto del paquete se descuenta del wallet del cliente y queda retenido en escrow.
- [ ] **CA5:** El pedido se crea en estado `pendiente` y el freelancer recibe una notificación (ver US-046).
- [ ] **CA6:** Un freelancer no puede crear pedidos de sus propios servicios; el sistema muestra error 403.
- [ ] **CA7:** El cliente puede agregar un mensaje inicial al crear el pedido.
- [ ] **CA8:** Si el wallet no tiene saldo suficiente, se redirige al cliente a la pantalla de recarga.

## Notas Técnicas

- Endpoint: `POST /api/orders`
- Tabla(s): `orders`, `transactions`, `users`
- Body: `{ "service_id": int, "paquete": "basico|estandar|premium", "mensaje_inicial": str }`
- Al crear el pedido: `users.wallet_balance -= precio`, `orders.escrow_retenido = precio`, `orders.estado = pendiente`
- Se registra una transacción de tipo `pago` en `transactions`
- Validación: `orders.client_id != orders.freelancer_id`

## Prioridad
`Alta`

## Estimación
`5` puntos de historia
