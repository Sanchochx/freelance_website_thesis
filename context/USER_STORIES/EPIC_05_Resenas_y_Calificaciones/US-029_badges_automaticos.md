# US-029 — Asignación automática de badges al freelancer

## Historia de Usuario

**Como** sistema,
**quiero** asignar badges automáticamente a los freelancers según sus métricas de desempeño,
**para** reconocer públicamente su excelencia y ayudar a los clientes a identificar los mejores proveedores.

## Criterios de Aceptación

- [ ] **CA1:** El badge **"Top Freelancer"** se asigna si el freelancer tiene calificación promedio ≥ 4.8 y al menos 10 pedidos completados.
- [ ] **CA2:** El badge **"Entrega Rápida"** se asigna si el 90% de los pedidos fueron entregados antes o en la fecha límite acordada.
- [ ] **CA3:** El badge **"Alta Calidad"** se asigna si el 95% de los pedidos completados no tuvieron solicitudes de revisión.
- [ ] **CA4:** Los badges se muestran de forma destacada en el perfil del freelancer y en las tarjetas de servicio.
- [ ] **CA5:** Los badges se recalculan automáticamente después de cada pedido completado.
- [ ] **CA6:** Si el freelancer deja de cumplir las condiciones (por nuevas reseñas negativas), el badge se retira automáticamente.
- [ ] **CA7:** El freelancer recibe una notificación cuando obtiene un nuevo badge.

## Notas Técnicas

- Tabla(s): `users`, `orders`, `reviews`
- El campo `users.badges` almacena un array JSON con los badges activos
- La lógica de evaluación se ejecuta como tarea programada (cron) tras cada pedido completado o al recibir una reseña
- Criterios de cálculo:
  - Top Freelancer: `AVG(reviews.rating) >= 4.8 AND COUNT(orders[completados]) >= 10`
  - Entrega Rápida: `COUNT(orders[fecha_entrega <= fecha_limite]) / COUNT(orders[completados]) >= 0.9`
  - Alta Calidad: `COUNT(orders[revisiones_usadas = 0]) / COUNT(orders[completados]) >= 0.95`

## Prioridad
`Media`

## Estimación
`5` puntos de historia
