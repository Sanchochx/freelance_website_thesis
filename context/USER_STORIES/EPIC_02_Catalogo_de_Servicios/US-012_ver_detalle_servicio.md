# US-012 — Ver el detalle completo de un servicio

## Historia de Usuario

**Como** usuario (autenticado o visitante),
**quiero** ver el detalle completo de un servicio antes de decidir contratarlo,
**para** evaluar si el freelancer y la oferta se ajustan a mis necesidades.

## Criterios de Aceptación

- [ ] **CA1:** La página de detalle muestra: título, descripción, categoría, imágenes de ejemplo, los tres paquetes con precios y tiempos de entrega, y el perfil resumido del freelancer.
- [ ] **CA2:** Se muestra la calificación promedio del freelancer y el número de pedidos completados.
- [ ] **CA3:** Se listan las reseñas de pedidos anteriores asociados a ese servicio.
- [ ] **CA4:** Si el servicio está pausado o eliminado, se muestra un mensaje de "servicio no disponible" en lugar del detalle.
- [ ] **CA5:** El botón de contratar es visible solo para usuarios autenticados con rol `client`; los freelancers ven un indicador de que no pueden contratar sus propios servicios.
- [ ] **CA6:** La URL del servicio es única y compartible (ej. `/servicios/{service_id}`).

## Notas Técnicas

- Endpoint: `GET /api/services/{service_id}`
- Tabla(s): `services`, `users`, `reviews`, `orders`
- La respuesta incluye datos del freelancer (`nombre`, `avatar_url`, `calificacion_promedio`) desde `users`
- Las reseñas se obtienen de `reviews` filtrando por `order_id` de pedidos del servicio
- Servicios con `estado != 'activo'` retornan 404 o 410 Gone para visitantes

## Prioridad
`Alta`

## Estimación
`3` puntos de historia
