# US-004 — Verificación de correo electrónico

## Historia de Usuario

**Como** usuario recién registrado,
**quiero** verificar mi correo electrónico mediante un enlace enviado a mi bandeja de entrada,
**para** activar mi cuenta y acceder a todas las funcionalidades de la plataforma.

## Criterios de Aceptación

- [x] **CA1:** Tras el registro, el sistema envía automáticamente un email con un enlace de verificación único.
- [x] **CA2:** El enlace de verificación tiene una validez de 24 horas; transcurrido ese tiempo expira.
- [x] **CA3:** Al hacer clic en el enlace, la cuenta cambia a estado `verificado = true`.
- [x] **CA4:** Tras verificar, el usuario es redirigido a la página de login con un mensaje de éxito.
- [x] **CA5:** Si el enlace ya fue usado o expiró, el sistema muestra un mensaje de error y ofrece reenviar el email.
- [x] **CA6:** El usuario puede solicitar el reenvío del email de verificación desde la pantalla de login.
- [x] **CA7:** Un freelancer con cuenta no verificada no puede publicar servicios.

## Notas Técnicas

- Endpoint verificación: `GET /api/auth/verify-email/{token}`
- Endpoint reenvío: `POST /api/auth/resend-verification`
- Tabla(s): `users`
- El token de verificación se almacena hasheado en la base de datos o en un campo temporal con timestamp
- Email enviado con `FastAPI-Mail` usando plantilla HTML
- El token es un UUID v4 generado al momento del registro

## Prioridad
`Alta`

## Estimación
`3` puntos de historia
