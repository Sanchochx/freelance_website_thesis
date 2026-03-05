# US-042 — Estado de pedidos en el dashboard del freelancer

## Historia de Usuario

**Como** freelancer,
**quiero** ver en mi dashboard el estado de todos mis pedidos (activos, completados y cancelados),
**para** gestionar mi carga de trabajo y saber cuántos pedidos tengo en cada etapa.

## Criterios de Aceptación

- [ ] **CA1:** El dashboard muestra contadores separados para: pedidos pendientes, en progreso, en revisión, completados (histórico) y cancelados (histórico).
- [ ] **CA2:** Los pedidos activos (pendiente + en progreso + en revisión) se listan con nombre del cliente, servicio y fecha límite.
- [ ] **CA3:** Al hacer clic en un pedido del dashboard, se navega directamente al detalle del pedido.
- [ ] **CA4:** Los pedidos próximos a vencer (menos de 24 horas para la fecha de entrega) se resaltan visualmente.
- [ ] **CA5:** Los contadores se actualizan en tiempo real o al recargar la página.

## Notas Técnicas

- Endpoint: `GET /api/dashboard/freelancer/orders`
- Response: `{ "pendientes": int, "en_progreso": int, "en_revision": int, "completados": int, "cancelados": int, "pedidos_activos": [...] }`
- Tabla(s): `orders`, `users`, `services`
- Filtro: `orders.freelancer_id = current_user_id`
- Lista de activos: `orders WHERE estado IN ('pendiente', 'en_progreso', 'en_revision') ORDER BY fecha_limite ASC`

## Prioridad
`Media`

## Estimación
`3` puntos de historia
