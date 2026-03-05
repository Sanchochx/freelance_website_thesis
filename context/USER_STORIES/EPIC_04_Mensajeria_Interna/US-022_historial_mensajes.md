# US-022 — Historial persistente de mensajes

## Historia de Usuario

**Como** usuario (cliente o freelancer),
**quiero** ver el historial completo de mensajes de un pedido aunque haya cerrado sesión,
**para** revisar conversaciones anteriores y tener un registro de lo acordado.

## Criterios de Aceptación

- [ ] **CA1:** Al abrir el chat de un pedido, se cargan todos los mensajes previos ordenados cronológicamente.
- [ ] **CA2:** El historial se carga con paginación inversa (los más recientes al fondo, scroll para ver más antiguos).
- [ ] **CA3:** Los mensajes se conservan indefinidamente mientras el pedido exista en la plataforma.
- [ ] **CA4:** El historial incluye los archivos adjuntos enviados (con vista previa o enlace de descarga).
- [ ] **CA5:** Se indica visualmente qué mensajes fueron enviados por cada parte (alineación diferente, color diferente).
- [ ] **CA6:** Solo el cliente y el freelancer del pedido pueden ver el historial de ese pedido.

## Notas Técnicas

- Endpoint: `GET /api/messages/{order_id}?page={n}`
- Tabla(s): `messages`
- Filtro: `messages.order_id = order_id`, ordenado por `timestamp ASC`
- Paginación: `LIMIT 50 OFFSET (page-1)*50`
- Autorización: verificar que `sender_id` pertenece al `client_id` o `freelancer_id` del pedido
- Los archivos adjuntos se sirven desde Cloudinary (URL pública)

## Prioridad
`Alta`

## Estimación
`3` puntos de historia
