# US-006 — Perfil de cliente

## Historia de Usuario

**Como** cliente (externo o estudiante),
**quiero** tener un perfil con mi información básica e historial de contrataciones,
**para** que los freelancers puedan conocer mi historial y confiar en mí como cliente.

## Criterios de Aceptación

- [ ] **CA1:** El perfil muestra: foto de perfil, nombre, empresa (si aplica), fecha de registro y calificación promedio como cliente.
- [ ] **CA2:** El historial de contrataciones muestra los pedidos completados (sin revelar montos pagados).
- [ ] **CA3:** Las reseñas recibidas de freelancers se muestran en el perfil.
- [ ] **CA4:** El número total de servicios contratados y completados es visible en el perfil.
- [ ] **CA5:** El perfil del cliente es visible para los freelancers cuando reciben un pedido de ese cliente.
- [ ] **CA6:** Los datos sensibles (correo, wallet balance) no se exponen en el perfil público.

## Notas Técnicas

- Endpoint: `GET /api/users/{user_id}/profile`
- Tabla(s): `users`, `orders`, `reviews`
- La respuesta filtra campos según el rol del usuario consultante
- El historial de pedidos se filtra por `orders.client_id = user_id` y `estado = completado`
- La calificación promedio como cliente se calcula de `reviews` donde `reviewed_id = user_id` y el reviewer es freelancer

## Prioridad
`Media`

## Estimación
`3` puntos de historia
