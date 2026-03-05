# US-040 — Servicios destacados en la página principal

## Historia de Usuario

**Como** usuario (visitante o autenticado),
**quiero** ver una sección de servicios destacados en la página principal del marketplace,
**para** descubrir los mejores servicios disponibles sin tener que buscar.

## Criterios de Aceptación

- [ ] **CA1:** La página principal muestra una sección "Servicios Destacados" con al menos 8 servicios.
- [ ] **CA2:** Los servicios destacados se seleccionan automáticamente basándose en: calificación promedio alta y número de pedidos completados.
- [ ] **CA3:** Cada tarjeta de servicio destacado muestra: imagen, título, nombre del freelancer, calificación y precio base.
- [ ] **CA4:** Los servicios destacados rotan periódicamente o se refrescan al cargar la página.
- [ ] **CA5:** Solo se muestran servicios en estado `activo`.
- [ ] **CA6:** Al hacer clic en un servicio destacado, se navega a la página de detalle del servicio.
- [ ] **CA7:** El administrador puede marcar servicios manualmente como destacados desde el panel admin.

## Notas Técnicas

- Endpoint: `GET /api/services/featured`
- Tabla(s): `services`, `users`
- Selección automática: `ORDER BY (calificacion_promedio * 0.7 + pedidos_completados * 0.3) DESC LIMIT 12`
- Campo adicional en `services`: `destacado` (boolean) para marcado manual por admin
- La query prioriza servicios con `destacado = true` primero, luego los automáticos
- Respuesta cacheada por 15 minutos para mejorar rendimiento

## Prioridad
`Media`

## Estimación
`3` puntos de historia
