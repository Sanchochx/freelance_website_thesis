# US-039 — Ordenar resultados de búsqueda

## Historia de Usuario

**Como** usuario,
**quiero** ordenar los resultados de búsqueda por diferentes criterios,
**para** encontrar el servicio más adecuado según mis prioridades (precio, calidad o popularidad).

## Criterios de Aceptación

- [ ] **CA1:** El usuario puede ordenar los resultados por las siguientes opciones:
  - **Más relevante** (por defecto): combinación de calificación y número de pedidos completados.
  - **Mejor calificado**: de mayor a menor calificación promedio.
  - **Precio: menor a mayor**: por precio del paquete básico.
  - **Precio: mayor a menor**: por precio del paquete básico descendente.
  - **Más vendido**: por número de pedidos completados descendente.
- [ ] **CA2:** El criterio de ordenamiento seleccionado se muestra activo visualmente.
- [ ] **CA3:** Al cambiar el criterio, los resultados se actualizan sin recargar la página.
- [ ] **CA4:** El ordenamiento se mantiene al aplicar filtros adicionales.

## Notas Técnicas

- Endpoint: `GET /api/services?order_by={criterio}&estado=activo`
- Parámetros de `order_by`: `relevancia | calificacion | precio_asc | precio_desc | mas_vendido`
- Tabla(s): `services`, `users`, `orders`
- Relevancia: `ORDER BY (calificacion_promedio * 0.6 + pedidos_completados * 0.4) DESC`
- Calificación: `ORDER BY users.calificacion_promedio DESC`
- Precio ASC/DESC: `ORDER BY services.precio_basico ASC/DESC`
- Más vendido: subconsulta `COUNT(orders[completados]) por service_id`

## Prioridad
`Media`

## Estimación
`3` puntos de historia
