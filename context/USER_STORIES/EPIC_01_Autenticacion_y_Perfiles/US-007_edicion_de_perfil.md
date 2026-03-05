# US-007 — Edición de perfil

## Historia de Usuario

**Como** usuario autenticado (freelancer o cliente),
**quiero** editar la información de mi perfil,
**para** mantener mis datos actualizados y mejorar mi presentación en la plataforma.

## Criterios de Aceptación

- [x] **CA1:** El freelancer puede editar: foto de perfil, bio, habilidades, portafolio (agregar/quitar imágenes o links).
- [x] **CA2:** El cliente puede editar: foto de perfil, nombre y empresa.
- [x] **CA3:** El correo electrónico no se puede cambiar directamente; requiere un flujo separado de cambio de correo con verificación.
- [x] **CA4:** La foto de perfil se sube a Cloudinary y se almacena la URL resultante.
- [x] **CA5:** Los cambios se guardan inmediatamente y se reflejan en el perfil público.
- [x] **CA6:** Si la foto sube falla (tamaño > 5 MB o formato no soportado), se muestra un error descriptivo.
- [x] **CA7:** Solo el propio usuario puede editar su perfil (verificación por JWT).

## Notas Técnicas

- Endpoint: `PUT /api/users/{user_id}/profile`
- Endpoint foto: `POST /api/users/{user_id}/avatar` (multipart/form-data)
- Tabla(s): `users`
- Cloudinary: upload con preset configurado; retorna `secure_url`
- Formatos de imagen aceptados: JPG, PNG, WEBP; tamaño máximo 5 MB
- Autorización: el `user_id` del JWT debe coincidir con el `user_id` de la ruta

## Prioridad
`Media`

## Estimación
`3` puntos de historia
