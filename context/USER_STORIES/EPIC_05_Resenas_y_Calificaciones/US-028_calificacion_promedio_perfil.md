# US-028 — Calificación promedio visible en el perfil

## Historia de Usuario

**Como** usuario (cliente o visitante),
**quiero** ver la calificación promedio del freelancer en su perfil y en las tarjetas de servicio,
**para** evaluar su reputación antes de contratarlo.

## Criterios de Aceptación

- [ ] **CA1:** La calificación promedio se muestra con íconos de estrellas (llenas, medias o vacías) y el valor numérico con un decimal (ej. 4.8).
- [ ] **CA2:** Se muestra el número total de reseñas junto a la calificación (ej. "4.8 ★ (23 reseñas)").
- [ ] **CA3:** Si el freelancer no tiene reseñas, se muestra "Sin calificaciones" en lugar de 0 estrellas.
- [ ] **CA4:** La calificación en las tarjetas de servicio del catálogo coincide con la del perfil del freelancer.
- [ ] **CA5:** La calificación se recalcula automáticamente cada vez que se agrega una nueva reseña.
- [ ] **CA6:** El desglose de calificaciones (cuántas de 5, 4, 3, 2, 1 estrella) es visible en la sección de reseñas del perfil.

## Notas Técnicas

- Endpoint: `GET /api/users/{user_id}/rating`
- Response: `{ "promedio": float, "total_resenas": int, "distribucion": { "5": int, "4": int, ... } }`
- Tabla(s): `reviews`, `users`
- El promedio se almacena en `users.calificacion_promedio` y se actualiza tras cada nueva reseña
- Alternativamente, se calcula en tiempo de consulta con `AVG(rating)` sobre `reviews`

## Prioridad
`Alta`

## Estimación
`2` puntos de historia
