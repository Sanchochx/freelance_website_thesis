# US-045 — Gestión de reportes pendientes para el administrador

## Historia de Usuario

**Como** administrador,
**quiero** ver y gestionar los usuarios y servicios reportados por la comunidad,
**para** mantener la calidad y seguridad del marketplace.

## Criterios de Aceptación

- [ ] **CA1:** El panel admin muestra una lista de reportes pendientes de revisión, con: objeto reportado (usuario o servicio), motivo del reporte, fecha y quién reportó.
- [ ] **CA2:** El administrador puede filtrar los reportes por tipo (usuario o servicio) y por estado (pendiente, resuelto, desestimado).
- [ ] **CA3:** Al revisar un reporte de usuario, el admin puede: suspender al usuario, enviarle una advertencia o desestimar el reporte.
- [ ] **CA4:** Al revisar un reporte de servicio, el admin puede: pausar o eliminar el servicio, o desestimar el reporte.
- [ ] **CA5:** El usuario reportado recibe una notificación cuando se toma una acción sobre su cuenta o servicio.
- [ ] **CA6:** Todos los reportes y acciones quedan registrados para auditoría.
- [ ] **CA7:** Solo los usuarios con rol `admin` pueden acceder a esta sección.

## Notas Técnicas

- Endpoint listar reportes: `GET /api/admin/reports?tipo={tipo}&estado={estado}`
- Endpoint accionar reporte: `PATCH /api/admin/reports/{report_id}/action`
- Body: `{ "accion": "suspender|advertencia|desestimar|pausar_servicio|eliminar_servicio", "motivo": str }`
- Tabla(s): tabla adicional `reports` (id, reporter_id, reported_user_id, reported_service_id, motivo, estado, fecha)
- Autorización: JWT con `rol = 'admin'`

## Prioridad
`Media`

## Estimación
`5` puntos de historia
