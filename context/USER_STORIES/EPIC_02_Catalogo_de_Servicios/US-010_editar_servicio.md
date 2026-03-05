# US-010 — Editar un servicio existente

## Historia de Usuario

**Como** freelancer,
**quiero** editar cualquier campo de mis servicios publicados,
**para** mantener la información actualizada y mejorar mi oferta.

## Criterios de Aceptación

- [x] **CA1:** Solo el freelancer propietario del servicio puede editarlo.
- [x] **CA2:** Se pueden editar todos los campos: título, descripción, categoría, imágenes, paquetes y tiempo de entrega.
- [x] **CA3:** Los cambios se reflejan inmediatamente en el catálogo público.
- [x] **CA4:** No se puede editar un servicio que tiene pedidos en estado `en progreso`; se muestra un mensaje informativo.
- [x] **CA5:** Al agregar nuevas imágenes, las anteriores pueden mantenerse o eliminarse individualmente.
- [x] **CA6:** Al editar los precios de los paquetes, los pedidos existentes no se ven afectados (conservan el precio al momento de la contratación).

## Notas Técnicas

- Endpoint: `PUT /api/services/{service_id}`
- Tabla(s): `services`
- Autorización: `user_id` del JWT debe coincidir con `services.user_id`
- Verificar que no exista `orders` con `service_id` y `estado IN ('en_progreso')` antes de permitir edición de precios
- Imágenes: eliminar URLs antiguas de Cloudinary al reemplazarlas

## Prioridad
`Media`

## Estimación
`3` puntos de historia
