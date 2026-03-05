# US-048 — Alerta en la plataforma al recibir un mensaje nuevo

## Historia de Usuario

**Como** usuario (cliente o freelancer),
**quiero** recibir una alerta visual dentro de la plataforma cuando llega un nuevo mensaje,
**para** estar al tanto de comunicaciones importantes sin tener que revisar manualmente el chat.

## Criterios de Aceptación

- [ ] **CA1:** Cuando llega un nuevo mensaje, aparece una notificación visual en la barra de navegación (badge o toast).
- [ ] **CA2:** La notificación muestra el nombre del remitente y un fragmento del mensaje.
- [ ] **CA3:** Al hacer clic en la notificación, el usuario es redirigido al chat del pedido correspondiente.
- [ ] **CA4:** La alerta aparece en tiempo real sin necesidad de recargar la página (WebSocket o SSE).
- [ ] **CA5:** Las notificaciones no leídas persisten en el ícono de notificaciones hasta que el usuario las revise.
- [ ] **CA6:** El usuario puede marcar todas las notificaciones como leídas con un solo clic.

## Notas Técnicas

- Canal: WebSocket (mismo canal del chat) o Server-Sent Events para notificaciones globales
- Endpoint notificaciones: `GET /api/notifications?leido=false`
- Endpoint marcar leídas: `PATCH /api/notifications/read-all`
- Tabla(s): `notifications`
- Campos: `user_id`, `tipo = 'mensaje_nuevo'`, `mensaje`, `leido`, `fecha`
- Al recibir un mensaje en el WebSocket, se emite un evento `new_notification` al destinatario

## Prioridad
`Alta`

## Estimación
`5` puntos de historia
