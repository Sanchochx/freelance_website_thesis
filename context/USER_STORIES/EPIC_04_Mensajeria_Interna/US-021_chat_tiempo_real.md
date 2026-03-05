# US-021 — Chat en tiempo real por pedido

## Historia de Usuario

**Como** usuario (cliente o freelancer),
**quiero** chatear en tiempo real con la contraparte de un pedido activo,
**para** coordinar detalles, aclarar dudas y comunicarme durante el desarrollo del trabajo.

## Criterios de Aceptación

- [ ] **CA1:** Cada pedido tiene un canal de chat propio, accesible desde la vista de detalle del pedido.
- [ ] **CA2:** Los mensajes se entregan en tiempo real sin necesidad de recargar la página.
- [ ] **CA3:** Solo el cliente y el freelancer del pedido pueden acceder al chat de ese pedido.
- [ ] **CA4:** Los mensajes se muestran con el nombre del remitente, avatar y timestamp (hora y fecha).
- [ ] **CA5:** El chat está disponible durante todo el ciclo de vida del pedido (incluso en estado `en_revision`).
- [ ] **CA6:** Si la conexión WebSocket se pierde, el sistema intenta reconectar automáticamente.
- [ ] **CA7:** Al enviar un mensaje, el input se limpia y el scroll baja automáticamente al último mensaje.

## Notas Técnicas

- Protocolo: WebSocket — `WS /ws/chat/{order_id}?token={jwt}`
- Tabla(s): `messages`
- Campos: `order_id`, `sender_id`, `contenido`, `timestamp`, `leido = false`
- Autenticación del WebSocket: JWT en query param o header `Authorization`
- Librería: FastAPI WebSocket o Socket.io
- Los mensajes también se persisten en BD para el historial (ver US-022)

## Prioridad
`Alta`

## Estimación
`8` puntos de historia
