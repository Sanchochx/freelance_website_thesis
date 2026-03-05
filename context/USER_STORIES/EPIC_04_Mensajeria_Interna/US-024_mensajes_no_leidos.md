# US-024 — Notificaciones de mensajes no leídos

## Historia de Usuario

**Como** usuario,
**quiero** recibir una indicación visual cuando tengo mensajes no leídos,
**para** no perderme comunicaciones importantes de mis pedidos activos.

## Criterios de Aceptación

- [ ] **CA1:** El ícono o enlace de mensajería en la barra de navegación muestra un badge con el número de mensajes no leídos.
- [ ] **CA2:** Al abrir el chat de un pedido, los mensajes se marcan automáticamente como leídos.
- [ ] **CA3:** El conteo de no leídos se actualiza en tiempo real sin necesidad de recargar la página.
- [ ] **CA4:** En el listado de pedidos, se indica visualmente cuáles tienen mensajes no leídos.
- [ ] **CA5:** Si el usuario tiene el chat abierto y llega un nuevo mensaje, este se marca como leído inmediatamente.
- [ ] **CA6:** El badge desaparece cuando no hay mensajes pendientes.

## Notas Técnicas

- Endpoint conteo: `GET /api/messages/unread/count`
- Endpoint marcar leídos: `PATCH /api/messages/{order_id}/read`
- Tabla(s): `messages`
- El campo `messages.leido` se actualiza a `true` cuando el destinatario abre el chat
- El conteo se calcula como `COUNT(*) FROM messages WHERE leido = false AND sender_id != current_user_id AND order_id IN (pedidos del usuario)`
- La actualización en tiempo real se envía por WebSocket al evento `message_read`

## Prioridad
`Media`

## Estimación
`3` puntos de historia
