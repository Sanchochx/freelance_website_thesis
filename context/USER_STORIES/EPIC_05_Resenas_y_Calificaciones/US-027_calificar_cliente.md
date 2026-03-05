# US-027 — Calificar al cliente al completar un pedido

## Historia de Usuario

**Como** freelancer,
**quiero** poder calificar al cliente al finalizar un pedido completado,
**para** que otros freelancers tengan información sobre la calidad del cliente como contratante.

## Criterios de Aceptación

- [ ] **CA1:** El freelancer solo puede calificar al cliente cuando el pedido está en estado `completado`.
- [ ] **CA2:** La calificación es de 1 a 5 estrellas (obligatorio) y puede incluir un comentario escrito (opcional, máximo 500 caracteres).
- [ ] **CA3:** Solo se puede dejar una reseña por pedido completado; no es editable ni eliminable.
- [ ] **CA4:** La reseña del cliente aparece en el perfil del cliente.
- [ ] **CA5:** La calificación del cliente se muestra cuando un freelancer recibe un pedido de ese cliente, para tomar la decisión de aceptar o rechazar.
- [ ] **CA6:** Si el freelancer no deja reseña en los primeros 7 días tras completarse el pedido, la opción expira.

## Notas Técnicas

- Endpoint: `POST /api/reviews`
- Body: `{ "order_id": int, "rating": int (1-5), "comentario": str (opcional) }`
- Tabla(s): `reviews`, `users`
- `reviewer_id = freelancer_id`, `reviewed_id = client_id`
- Misma tabla `reviews` con roles invertidos; diferenciar por roles de `reviewer_id` y `reviewed_id`
- Validación: `orders.estado = 'completado'` y no exista review previa del freelancer para ese pedido

## Prioridad
`Media`

## Estimación
`2` puntos de historia
