# US-019 — Historial completo de pedidos

## Historia de Usuario

**Como** usuario (cliente o freelancer),
**quiero** ver el historial completo de todos mis pedidos con su estado actual,
**para** hacer seguimiento a mis contrataciones o proyectos en cualquier momento.

## Criterios de Aceptación

- [ ] **CA1:** El cliente ve todos los pedidos que ha realizado, ordenados por fecha (más reciente primero).
- [ ] **CA2:** El freelancer ve todos los pedidos recibidos, ordenados por fecha (más reciente primero).
- [ ] **CA3:** Cada entrada del historial muestra: nombre del servicio, paquete contratado, estado, monto y fechas de creación y completado (si aplica).
- [ ] **CA4:** El usuario puede filtrar el historial por estado: pendiente, en progreso, en revisión, completado, cancelado.
- [ ] **CA5:** Al hacer clic en un pedido del historial, se accede al detalle completo del pedido.
- [ ] **CA6:** El historial es paginado (máximo 20 pedidos por página).

## Notas Técnicas

- Endpoint (cliente): `GET /api/orders?rol=client&page={n}&estado={estado}`
- Endpoint (freelancer): `GET /api/orders?rol=freelancer&page={n}&estado={estado}`
- Tabla(s): `orders`, `services`, `users`
- El rol se determina desde el JWT; el endpoint filtra por `client_id` o `freelancer_id` según corresponda
- Paginación: `LIMIT 20 OFFSET (page-1)*20`
- Response incluye `total_count` para calcular páginas en el frontend

## Prioridad
`Media`

## Estimación
`3` puntos de historia
