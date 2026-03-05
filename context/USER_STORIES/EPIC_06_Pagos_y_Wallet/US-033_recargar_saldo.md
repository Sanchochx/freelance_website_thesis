# US-033 — Recargar saldo en la wallet con MercadoPago (Sandbox)

## Historia de Usuario

**Como** usuario (cliente o freelancer),
**quiero** recargar saldo en mi wallet usando el checkout de MercadoPago en modo Sandbox,
**para** simular fondos disponibles con dinero de prueba y poder contratar servicios dentro del entorno de demostración.

## Criterios de Aceptación

- [ ] **CA1:** El usuario puede iniciar una recarga de saldo desde su wallet o desde el flujo de creación de pedido (si no tiene saldo suficiente).
- [ ] **CA2:** Se puede elegir un monto personalizado o uno de los montos predefinidos (ej. $20.000, $50.000, $100.000, $200.000 COP).
- [ ] **CA3:** El sistema redirige al usuario al checkout de MercadoPago **Sandbox** (entorno de pruebas) para completar el pago simulado.
- [ ] **CA4:** El pago se realiza con las **tarjetas de prueba** y **usuarios de prueba** provistos por MercadoPago; no se mueve dinero real.
- [ ] **CA5:** Al completar el pago de prueba exitosamente, el saldo se acredita en la wallet automáticamente mediante webhook del Sandbox.
- [ ] **CA6:** Si el pago de prueba es cancelado o falla (usando tarjeta de rechazo de MP), el saldo no se modifica y se notifica al usuario.
- [ ] **CA7:** Se registra una transacción de tipo `recarga` en el historial.
- [ ] **CA8:** El monto mínimo de recarga es COP $10.000.

## Notas Técnicas

- Endpoint iniciar recarga: `POST /api/wallet/recharge` → retorna URL del checkout Sandbox de MercadoPago
- Endpoint webhook MP: `POST /api/wallet/recharge/webhook`
- Tabla(s): `transactions`, `users`
- Integración: MercadoPago SDK Python en modo **Sandbox**
  - Credenciales: `ACCESS_TOKEN` de prueba (nunca las reales)
  - Instancia: `sdk = mercadopago.SDK(TEST_ACCESS_TOKEN)`
  - Crear preferencia: `sdk.preference().create({ "items": [...] })`
- El sandbox de MercadoPago provee tarjetas y usuarios de prueba para simular aprobaciones, rechazos y cancelaciones
- El webhook del Sandbox funciona igual que el de producción; verificar la firma (`X-Signature`) para seguridad
- El webhook actualiza `users.wallet_balance += monto` solo si `payment.status == 'approved'`

## Prioridad
`Alta`

## Estimación
`5` puntos de historia
