# US-034 — Simular retiro de ganancias con MercadoPago (Sandbox)

## Historia de Usuario

**Como** freelancer,
**quiero** simular el retiro de mis ganancias acumuladas en la wallet a través de MercadoPago Sandbox,
**para** verificar que el flujo de retiro funciona correctamente en el entorno de pruebas, sin mover dinero real.

## Criterios de Aceptación

- [ ] **CA1:** El freelancer puede solicitar un retiro desde su dashboard o sección de wallet.
- [ ] **CA2:** El monto a retirar no puede superar el saldo disponible en la wallet.
- [ ] **CA3:** El monto mínimo de retiro es COP $20.000.
- [ ] **CA4:** El sistema procesa el retiro de forma **simulada** usando las credenciales de prueba de MercadoPago Sandbox; no se transfiere dinero real.
- [ ] **CA5:** El saldo de la wallet se descuenta inmediatamente al solicitar el retiro.
- [ ] **CA6:** El retiro queda en estado `pendiente` hasta que el Sandbox de MercadoPago confirma la transferencia simulada.
- [ ] **CA7:** Se registra una transacción de tipo `retiro` en el historial con el estado del proceso.
- [ ] **CA8:** El freelancer recibe una notificación cuando el retiro simulado es procesado exitosamente.

## Notas Técnicas

- Endpoint: `POST /api/wallet/withdraw`
- Body: `{ "monto": float }`
- Tabla(s): `transactions`, `users`
- Integración: MercadoPago SDK Python en modo **Sandbox**
  - Credenciales: `TEST_ACCESS_TOKEN` del usuario vendedor de prueba
  - El retiro se simula como un pago saliente usando la API de MercadoPago Sandbox
  - No se requiere cuenta bancaria real ni datos financieros reales del freelancer
- Operación: `users.wallet_balance -= monto` + `INSERT INTO transactions (tipo=retiro, estado=pendiente)`
- El estado se actualiza a `completado` o `fallido` mediante respuesta del Sandbox
- En producción real, este flujo usaría la API de Payouts de MercadoPago con `ACCESS_TOKEN` real

## Prioridad
`Alta`

## Estimación
`5` puntos de historia
