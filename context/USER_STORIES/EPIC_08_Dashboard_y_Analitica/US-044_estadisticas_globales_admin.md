# US-044 — Estadísticas globales de la plataforma para el administrador

## Historia de Usuario

**Como** administrador,
**quiero** ver estadísticas globales de la plataforma (usuarios, servicios y transacciones),
**para** monitorear el estado general del marketplace y tomar decisiones estratégicas.

## Criterios de Aceptación

- [ ] **CA1:** El panel admin muestra el total de usuarios registrados, desglosado por rol (freelancers y clientes).
- [ ] **CA2:** Se muestra el total de servicios publicados, desglosado por categoría y estado (activo/pausado).
- [ ] **CA3:** Se muestra el volumen total de transacciones del mes en COP y el número de transacciones.
- [ ] **CA4:** Se muestra el número de pedidos activos en la plataforma en tiempo real.
- [ ] **CA5:** Se muestra la comisión total recaudada por la plataforma en el mes.
- [ ] **CA6:** Las estadísticas incluyen una gráfica de crecimiento de usuarios y pedidos por mes (últimos 6 meses).
- [ ] **CA7:** Solo los usuarios con rol `admin` pueden acceder a este panel.

## Notas Técnicas

- Endpoint: `GET /api/admin/stats`
- Response:
  ```json
  {
    "usuarios": { "total": int, "freelancers": int, "clientes": int },
    "servicios": { "total": int, "por_categoria": [...], "activos": int },
    "transacciones_mes": { "volumen_cop": float, "cantidad": int },
    "pedidos_activos": int,
    "comision_mes": float,
    "crecimiento_mensual": [...]
  }
  ```
- Tabla(s): `users`, `services`, `transactions`, `orders`
- Autorización: middleware que verifica `rol = 'admin'` en el JWT

## Prioridad
`Media`

## Estimación
`5` puntos de historia
