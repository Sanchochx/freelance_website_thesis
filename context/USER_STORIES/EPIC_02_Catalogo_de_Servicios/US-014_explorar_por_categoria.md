# US-014 — Explorar servicios por categoría

## Historia de Usuario

**Como** usuario (visitante o autenticado),
**quiero** explorar los servicios disponibles agrupados por categoría,
**para** encontrar rápidamente el tipo de servicio que necesito.

## Criterios de Aceptación

- [ ] **CA1:** La página principal muestra las 8 categorías disponibles con iconos descriptivos.
- [ ] **CA2:** Al seleccionar una categoría, se despliega el listado de servicios activos de esa categoría.
- [ ] **CA3:** Cada tarjeta de servicio en el listado muestra: imagen principal, título, nombre del freelancer, calificación promedio y precio base.
- [ ] **CA4:** Los servicios se ordenan por defecto por relevancia (combinación de calificación y número de pedidos).
- [ ] **CA5:** Si una categoría no tiene servicios activos, se muestra un mensaje amigable de "sin resultados".
- [ ] **CA6:** La URL de cada categoría es navegable y compartible (ej. `/categorias/{categoria_id}`).

## Notas Técnicas

- Endpoint listado de categorías: `GET /api/categories`
- Endpoint servicios por categoría: `GET /api/services?categoria_id={id}&estado=activo`
- Tabla(s): `categories`, `services`, `users`
- El campo `icono` de `categories` almacena el nombre del ícono (ej. nombre de Heroicons o similar)
- La relevancia se calcula como score compuesto: `(calificacion_promedio * 0.6) + (pedidos_completados * 0.4)`

## Prioridad
`Alta`

## Estimación
`3` puntos de historia
