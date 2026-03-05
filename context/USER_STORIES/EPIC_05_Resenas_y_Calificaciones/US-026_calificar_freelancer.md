# US-026 — Calificar al freelancer al completar un pedido

## Historia de Usuario

**Como** cliente,
**quiero** dejar una calificación y reseña al freelancer al completar un pedido,
**para** ayudar a otros clientes a tomar decisiones informadas y reconocer el buen trabajo.

## Criterios de Aceptación

- [ ] **CA1:** El cliente solo puede calificar al freelancer cuando el pedido está en estado `completado`.
- [ ] **CA2:** La calificación es de 1 a 5 estrellas (obligatorio) y puede incluir un comentario escrito (opcional, máximo 500 caracteres).
- [ ] **CA3:** Solo se puede dejar una reseña por pedido completado; no se permite editar ni eliminar una vez enviada.
- [ ] **CA4:** La reseña aparece en el perfil público del freelancer dentro de los 5 minutos de ser enviada.
- [ ] **CA5:** La calificación promedio del freelancer se actualiza automáticamente.
- [ ] **CA6:** El freelancer recibe una notificación cuando recibe una nueva reseña.
- [ ] **CA7:** Si el cliente no deja reseña en los primeros 7 días tras completarse el pedido, la opción de reseña expira.

## Notas Técnicas

- Endpoint: `POST /api/reviews`
- Body: `{ "order_id": int, "rating": int (1-5), "comentario": str (opcional) }`
- Tabla(s): `reviews`, `users`
- `reviewer_id = client_id`, `reviewed_id = freelancer_id`
- Validación: `orders.estado = 'completado'` y no exista review previa del cliente para ese pedido
- Al insertar: recalcular `users.calificacion_promedio = AVG(rating) WHERE reviewed_id = freelancer_id`

## Prioridad
`Alta`

## Estimación
`3` puntos de historia
