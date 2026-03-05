# US-038 — Filtros de búsqueda avanzados

## Historia de Usuario

**Como** usuario,
**quiero** filtrar los resultados de búsqueda por categoría, rango de precio, calificación mínima y tiempo de entrega,
**para** encontrar servicios que se ajusten exactamente a mis necesidades y presupuesto.

## Criterios de Aceptación

- [ ] **CA1:** El panel de filtros está disponible en la página de catálogo y resultados de búsqueda.
- [ ] **CA2:** El filtro de **categoría** permite seleccionar una o varias de las 8 categorías disponibles.
- [ ] **CA3:** El filtro de **precio** permite ingresar un rango mínimo y máximo en COP.
- [ ] **CA4:** El filtro de **calificación mínima** ofrece opciones: ≥ 4.5, ≥ 4.0, ≥ 3.5 o cualquier calificación.
- [ ] **CA5:** El filtro de **tiempo de entrega** ofrece opciones: hasta 1 día, hasta 3 días, hasta 7 días, más de 7 días.
- [ ] **CA6:** Los filtros se aplican de forma acumulativa (AND entre filtros).
- [ ] **CA7:** El usuario puede limpiar todos los filtros con un botón "Limpiar filtros".
- [ ] **CA8:** Los filtros activos se muestran como chips/etiquetas para que el usuario sepa cuáles tiene activos.

## Notas Técnicas

- Endpoint: `GET /api/services?categoria_id={id}&precio_min={n}&precio_max={n}&calificacion_min={n}&tiempo_entrega_max={dias}&estado=activo`
- Tabla(s): `services`, `users` (para calificación del freelancer)
- La calificación mínima filtra por `users.calificacion_promedio >= calificacion_min` (JOIN con users)
- El tiempo de entrega filtra por `services.tiempo_entrega <= tiempo_entrega_max`
- Los filtros se combinan dinámicamente en el query de SQLAlchemy

## Prioridad
`Alta`

## Estimación
`5` puntos de historia
