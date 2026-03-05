# US-009 — Crear un servicio (gig)

## Historia de Usuario

**Como** estudiante freelancer verificado,
**quiero** crear un servicio en la plataforma describiendo qué ofrezco, mis precios y tiempos de entrega,
**para** que los clientes puedan encontrarme y contratarme.

## Criterios de Aceptación

- [x] **CA1:** Solo usuarios con rol `freelancer` y cuenta verificada pueden crear servicios.
- [x] **CA2:** El formulario solicita: título, descripción, categoría, imágenes de ejemplo (mínimo 1, máximo 5), tiempo de entrega y al menos un paquete de precio.
- [x] **CA3:** El título tiene un máximo de 100 caracteres; la descripción un máximo de 1200 caracteres.
- [x] **CA4:** El servicio se crea en estado `activo` por defecto.
- [x] **CA5:** Las imágenes se suben a Cloudinary y se almacenan sus URLs.
- [x] **CA6:** La categoría debe pertenecer a las 8 categorías disponibles del sistema.
- [x] **CA7:** El servicio recién creado aparece en el catálogo público inmediatamente.
- [x] **CA8:** Un freelancer no puede crear más de 10 servicios activos simultáneamente.

## Notas Técnicas

- Endpoint: `POST /api/services`
- Tabla(s): `services`, `categories`
- Campos: `user_id` (del JWT), `titulo`, `descripcion`, `categoria_id`, `precio_basico`, `precio_estandar`, `precio_premium`, `tiempo_entrega`, `estado = activo`
- Imágenes: upload a Cloudinary, URLs guardadas en `services.imagenes` (array JSON)
- Autorización: JWT requerido con rol `freelancer` y `verificado = true`

## Prioridad
`Alta`

## Estimación
`5` puntos de historia
