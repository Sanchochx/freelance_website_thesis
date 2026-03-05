# US-005 — Perfil completo de freelancer

## Historia de Usuario

**Como** estudiante freelancer,
**quiero** tener un perfil público completo con mi foto, carrera, habilidades y portafolio,
**para** generar confianza en los clientes y aumentar mis posibilidades de ser contratado.

## Criterios de Aceptación

- [x] **CA1:** El perfil muestra: foto de perfil, nombre, carrera, semestre, bio, habilidades (lista de tags), portafolio (imágenes/links) y calificación promedio con número de reseñas.
- [x] **CA2:** El perfil es visible públicamente para cualquier usuario (autenticado o no).
- [x] **CA3:** Los servicios activos del freelancer se listan en su perfil.
- [x] **CA4:** Las reseñas recibidas se muestran en el perfil con nombre del cliente, calificación y comentario.
- [x] **CA5:** Los badges obtenidos (Top Freelancer, Entrega Rápida, Alta Calidad) se muestran destacados.
- [x] **CA6:** Si el freelancer no tiene reseñas aún, se muestra "Sin calificaciones todavía".
- [x] **CA7:** La calificación promedio se actualiza automáticamente al recibir nuevas reseñas.

## Notas Técnicas

- Endpoint: `GET /api/users/{user_id}/profile`
- Tabla(s): `users`, `services`, `reviews`
- La calificación promedio se calcula como `AVG(rating)` de `reviews` donde `reviewed_id = user_id`
- Las habilidades se almacenan como array JSON en `users.habilidades`
- El portafolio se almacena como array de URLs (Cloudinary) en `users.portafolio`
- Los badges se almacenan en `users.badges` (array JSON)

## Prioridad
`Alta`

## Estimación
`5` puntos de historia
