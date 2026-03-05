# US-008 — Recuperación de contraseña

## Historia de Usuario

**Como** usuario registrado,
**quiero** recuperar el acceso a mi cuenta si olvidé mi contraseña,
**para** no perder permanentemente el acceso a mi perfil y datos.

## Criterios de Aceptación

- [ ] **CA1:** Desde la pantalla de login, el usuario puede acceder a "¿Olvidaste tu contraseña?".
- [ ] **CA2:** El usuario ingresa su correo registrado y el sistema envía un email con un enlace de restablecimiento.
- [ ] **CA3:** El sistema no confirma ni niega si el correo existe (por seguridad), siempre muestra el mismo mensaje de éxito.
- [ ] **CA4:** El enlace de restablecimiento tiene validez de 1 hora.
- [ ] **CA5:** Al acceder al enlace, el usuario puede ingresar y confirmar su nueva contraseña.
- [ ] **CA6:** La nueva contraseña debe cumplir los mismos criterios de complejidad del registro (mínimo 8 caracteres, una mayúscula, un número).
- [ ] **CA7:** Una vez usada, el enlace queda invalidado y no puede reutilizarse.
- [ ] **CA8:** Tras restablecer la contraseña, el usuario es redirigido al login con un mensaje de éxito.

## Notas Técnicas

- Endpoint solicitud: `POST /api/auth/forgot-password` (body: `{ "email": "..." }`)
- Endpoint restablecimiento: `POST /api/auth/reset-password` (body: `{ "token": "...", "new_password": "..." }`)
- Tabla(s): `users`
- El token de restablecimiento es un UUID v4 con timestamp de expiración almacenado en la BD
- Email enviado con `FastAPI-Mail`
- La nueva contraseña se hashea con `passlib[bcrypt]` antes de guardar

## Prioridad
`Alta`

## Estimación
`3` puntos de historia
