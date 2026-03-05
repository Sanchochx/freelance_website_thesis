# US-011 — Pausar o eliminar un servicio

## Historia de Usuario

**Como** freelancer,
**quiero** pausar temporalmente o eliminar definitivamente mis servicios,
**para** gestionar mi disponibilidad cuando no puedo atender nuevos pedidos.

## Criterios de Aceptación

- [x] **CA1:** El freelancer puede cambiar el estado de un servicio a `pausado` desde su dashboard.
- [x] **CA2:** Un servicio pausado no aparece en el catálogo público ni en los resultados de búsqueda.
- [x] **CA3:** El freelancer puede volver a activar un servicio pausado en cualquier momento.
- [x] **CA4:** El freelancer puede eliminar permanentemente un servicio solo si no tiene pedidos activos.
- [x] **CA5:** Si el servicio tiene pedidos en progreso, el sistema impide la eliminación y muestra un mensaje explicativo.
- [x] **CA6:** Al eliminar un servicio, se conservan los pedidos históricos asociados para registro.

## Notas Técnicas

- Endpoint pausar/activar: `PATCH /api/services/{service_id}/status` (body: `{ "estado": "pausado" | "activo" }`)
- Endpoint eliminar: `DELETE /api/services/{service_id}`
- Tabla(s): `services`, `orders`
- Verificar ausencia de pedidos activos antes de eliminar: `SELECT COUNT(*) FROM orders WHERE service_id = ? AND estado NOT IN ('completado', 'cancelado')`
- Eliminación lógica: `services.estado = 'eliminado'` (se conserva el registro en BD)

## Prioridad
`Media`

## Estimación
`2` puntos de historia
