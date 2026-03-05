# US-043 — Métricas de rendimiento y gráfica histórica del freelancer

## Historia de Usuario

**Como** freelancer,
**quiero** ver mi tasa de completado y una gráfica de mis ingresos o pedidos a lo largo del tiempo,
**para** evaluar mi rendimiento, identificar tendencias y tomar decisiones para mejorar.

## Criterios de Aceptación

- [ ] **CA1:** El dashboard muestra la tasa de completado: porcentaje de pedidos completados sobre el total recibido.
- [ ] **CA2:** Se muestra la tasa de satisfacción del cliente: porcentaje de pedidos sin solicitudes de revisión.
- [ ] **CA3:** Se muestra una gráfica de barras o línea con los ingresos mensuales de los últimos 6 meses.
- [ ] **CA4:** La gráfica es interactiva: al pasar el mouse sobre un punto, se muestra el valor exacto.
- [ ] **CA5:** Se muestra el tiempo de respuesta promedio (tiempo entre recibir un pedido y aceptarlo/rechazarlo).
- [ ] **CA6:** Las métricas se calculan sobre todos los pedidos históricos del freelancer.

## Notas Técnicas

- Endpoint: `GET /api/dashboard/freelancer/metrics`
- Response:
  ```json
  {
    "tasa_completado": float,
    "tasa_satisfaccion": float,
    "tiempo_respuesta_promedio_horas": float,
    "ingresos_mensuales": [{"mes": "2026-01", "total": float}, ...]
  }
  ```
- Tabla(s): `orders`, `transactions`
- Tasa completado: `COUNT(estado=completado) / COUNT(total) * 100`
- Gráfica: `GROUP BY DATE_TRUNC('month', fecha) ORDER BY mes DESC LIMIT 6`
- Frontend: Recharts (LineChart o BarChart)

## Prioridad
`Media`

## Estimación
`5` puntos de historia
