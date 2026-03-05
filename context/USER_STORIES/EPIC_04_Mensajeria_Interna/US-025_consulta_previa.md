# US-025 — Consulta previa al freelancer antes del pedido

## Historia de Usuario

**Como** cliente potencial,
**quiero** poder enviar un mensaje al freelancer antes de realizar un pedido,
**para** aclarar dudas sobre el servicio, el alcance o los tiempos antes de comprometerme.

## Criterios de Aceptación

- [ ] **CA1:** En la página de detalle de un servicio, existe un botón "Contactar al freelancer" visible para usuarios autenticados con rol `client`.
- [ ] **CA2:** Al hacer clic, se abre un formulario o modal para escribir un mensaje de consulta.
- [ ] **CA3:** El freelancer recibe la consulta en su bandeja de mensajes y puede responder.
- [ ] **CA4:** La conversación de consulta previa queda separada de los chats de pedidos activos.
- [ ] **CA5:** Si el cliente decide crear un pedido después de la consulta, se le ofrece enlace directo al servicio.
- [ ] **CA6:** Un freelancer no puede enviar consultas sobre sus propios servicios.

## Notas Técnicas

- Endpoint: `POST /api/messages/inquiry`
- Body: `{ "service_id": int, "mensaje": str }`
- Tabla(s): `messages`
- Se crea un hilo de consulta con `order_id = null` e identificado por `service_id` + `client_id` + `freelancer_id`
- Alternativa: crear un `pre_order` o `inquiry` entity separada para mayor claridad
- El freelancer recibe notificación en la plataforma (ver US-048)

## Prioridad
`Baja`

## Estimación
`3` puntos de historia
