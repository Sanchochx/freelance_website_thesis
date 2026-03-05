# US-037 — Búsqueda de servicios por palabra clave

## Historia de Usuario

**Como** usuario (visitante o autenticado),
**quiero** buscar servicios usando palabras clave en una barra de búsqueda,
**para** encontrar rápidamente los servicios que necesito sin tener que navegar por categorías.

## Criterios de Aceptación

- [ ] **CA1:** La barra de búsqueda está disponible en la página principal y en el catálogo de servicios.
- [ ] **CA2:** La búsqueda se realiza sobre los campos: título del servicio y descripción.
- [ ] **CA3:** Los resultados se muestran en tiempo real o tras presionar Enter / clic en el botón de búsqueda.
- [ ] **CA4:** La búsqueda es insensible a mayúsculas/minúsculas y a acentos.
- [ ] **CA5:** Si no hay resultados, se muestra un mensaje amigable con sugerencias alternativas.
- [ ] **CA6:** Solo se muestran servicios en estado `activo`.
- [ ] **CA7:** La URL se actualiza con el término de búsqueda para permitir compartir o navegar con el botón "atrás" del navegador.

## Notas Técnicas

- Endpoint: `GET /api/services?search={keyword}&estado=activo`
- Tabla(s): `services`
- Búsqueda: `ILIKE '%keyword%'` en `titulo` y `descripcion` (PostgreSQL)
- Alternativa de mayor rendimiento: PostgreSQL Full Text Search (`to_tsvector` + `to_tsquery`)
- Normalización de acentos: `unaccent` extension de PostgreSQL
- Los resultados se paginan (20 por página)

## Prioridad
`Alta`

## Estimación
`3` puntos de historia
