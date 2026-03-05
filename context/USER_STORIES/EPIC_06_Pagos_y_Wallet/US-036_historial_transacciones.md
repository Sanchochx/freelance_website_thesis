# US-036 — Historial de transacciones descargable

## Historia de Usuario

**Como** usuario,
**quiero** ver y descargar mi historial completo de transacciones,
**para** llevar control de mis ingresos, gastos y movimientos financieros en la plataforma.

## Criterios de Aceptación

- [ ] **CA1:** El historial muestra todas las transacciones del usuario ordenadas por fecha (más reciente primero).
- [ ] **CA2:** Cada transacción muestra: tipo (recarga, pago, cobro, retiro, comisión, reembolso), monto, fecha y estado.
- [ ] **CA3:** El usuario puede filtrar por tipo de transacción y rango de fechas.
- [ ] **CA4:** El historial se puede exportar en formato CSV.
- [ ] **CA5:** El historial es paginado (máximo 20 transacciones por página).
- [ ] **CA6:** Solo el propio usuario puede ver su historial de transacciones.
- [ ] **CA7:** El administrador puede ver el historial de cualquier usuario desde el panel de administración.

## Notas Técnicas

- Endpoint historial: `GET /api/transactions?page={n}&tipo={tipo}&fecha_inicio={date}&fecha_fin={date}`
- Endpoint exportar: `GET /api/transactions/export?formato=csv`
- Tabla(s): `transactions`
- Filtros: `user_id = current_user_id`, `tipo`, `DATE(fecha) BETWEEN fecha_inicio AND fecha_fin`
- Exportación: generación de CSV en el backend con `csv` module de Python
- Autorización: JWT obligatorio; el `user_id` del JWT filtra las transacciones

## Prioridad
`Media`

## Estimación
`3` puntos de historia
