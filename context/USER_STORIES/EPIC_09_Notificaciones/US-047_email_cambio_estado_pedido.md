# US-047 — Email al cliente cuando cambia el estado de su pedido

## Historia de Usuario

**Como** cliente,
**quiero** recibir un email cada vez que el estado de mi pedido cambia,
**para** estar informado del progreso de mi contratación sin tener que revisar la plataforma constantemente.

## Criterios de Aceptación

- [ ] **CA1:** El cliente recibe un email en cada cambio de estado: pendiente → en progreso, en progreso → en revisión, en revisión → completado, cualquier estado → cancelado.
- [ ] **CA2:** El email indica claramente: el nuevo estado, el nombre del servicio y del freelancer, y qué acción (si alguna) debe tomar el cliente.
- [ ] **CA3:** Para el estado `en_revision` (entrega disponible), el email incluye un enlace directo para revisar la entrega.
- [ ] **CA4:** Para el estado `completado`, el email incluye un enlace para dejar reseña al freelancer.
- [ ] **CA5:** El email se envía de forma asíncrona dentro de los 2 minutos del cambio de estado.
- [ ] **CA6:** El cliente puede desactivar las notificaciones por email desde la configuración de su perfil.

## Notas Técnicas

- Disparador: `PATCH /api/orders/{order_id}/status` (en cada cambio de estado)
- Tabla(s): `notifications`, `users`, `orders`
- Librería: `FastAPI-Mail`
- Se envía email diferente según el nuevo estado (plantillas distintas)
- Se registra en `notifications` con `tipo = 'cambio_estado_pedido'` y `user_id = client_id`
- La preferencia de emails se almacena en `users.notificaciones_email` (boolean)

## Prioridad
`Alta`

## Estimación
`3` puntos de historia
