# US-049 — Recordatorio de pedido sin respuesta por más de 3 días

## Historia de Usuario

**Como** usuario (cliente o freelancer),
**quiero** recibir un recordatorio si un pedido activo lleva más de 3 días sin actividad o respuesta,
**para** que ningún pedido quede abandonado y se puedan tomar acciones a tiempo.

## Criterios de Aceptación

- [ ] **CA1:** Si un pedido en estado `pendiente` no ha sido aceptado o rechazado por el freelancer en 3 días, ambas partes reciben un recordatorio por email.
- [ ] **CA2:** Si un pedido en estado `en_progreso` no ha recibido ningún mensaje ni entrega en 3 días, el cliente recibe un recordatorio para contactar al freelancer.
- [ ] **CA3:** Si un pedido en estado `en_revision` no ha sido aprobado ni se ha solicitado revisión en 3 días, el freelancer recibe un recordatorio.
- [ ] **CA4:** El email de recordatorio incluye: estado del pedido, días sin actividad y un enlace directo al pedido.
- [ ] **CA5:** Los recordatorios se envían una sola vez por pedido (no se repiten diariamente).
- [ ] **CA6:** Si el pedido tiene actividad después del recordatorio, el temporizador se reinicia.

## Notas Técnicas

- Mecanismo: tarea programada (cron job) que se ejecuta diariamente
- Librería: Celery Beat con Redis como broker, o APScheduler en FastAPI
- Tabla(s): `orders`, `notifications`, `messages`
- Lógica:
  - `SELECT * FROM orders WHERE estado IN ('pendiente', 'en_progreso', 'en_revision') AND (ultima_actividad IS NULL OR ultima_actividad < NOW() - INTERVAL '3 days') AND recordatorio_enviado = false`
- Al enviar: `orders.recordatorio_enviado = true`; se reinicia cuando hay nueva actividad

## Prioridad
`Baja`

## Estimación
`5` puntos de historia
