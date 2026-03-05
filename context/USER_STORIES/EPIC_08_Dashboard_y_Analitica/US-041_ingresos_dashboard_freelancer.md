# US-041 — Ingresos del mes y acumulados en el dashboard del freelancer

## Historia de Usuario

**Como** freelancer,
**quiero** ver mis ingresos del mes en curso y mis ingresos acumulados totales en mi dashboard,
**para** controlar mi rendimiento financiero y planificar mejor mi actividad.

## Criterios de Aceptación

- [ ] **CA1:** El dashboard muestra el total de ingresos del mes en curso (del día 1 al día actual).
- [ ] **CA2:** Se muestra también el total acumulado histórico de ingresos (desde el registro).
- [ ] **CA3:** Los ingresos incluyen solo transacciones de tipo `cobro` (después de la comisión del 10%).
- [ ] **CA4:** Se muestra una comparativa de ingresos: mes actual vs mes anterior.
- [ ] **CA5:** Los valores se muestran en pesos colombianos (COP) formateados con separadores de miles.
- [ ] **CA6:** El dashboard se actualiza automáticamente al completarse un pedido.

## Notas Técnicas

- Endpoint: `GET /api/dashboard/freelancer/earnings`
- Response: `{ "mes_actual": float, "mes_anterior": float, "acumulado": float }`
- Tabla(s): `transactions`
- Filtro: `user_id = freelancer_id AND tipo = 'cobro'`
- Mes actual: `DATE_TRUNC('month', fecha) = DATE_TRUNC('month', NOW())`
- Mes anterior: `DATE_TRUNC('month', fecha) = DATE_TRUNC('month', NOW() - INTERVAL '1 month')`

## Prioridad
`Media`

## Estimación
`3` puntos de historia
