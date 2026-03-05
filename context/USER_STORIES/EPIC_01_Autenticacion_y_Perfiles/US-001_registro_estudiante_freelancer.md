# US-001 — Registro de estudiante freelancer

## Historia de Usuario

**Como** estudiante universitario de la USTA Tunja,
**quiero** registrarme en la plataforma usando mi correo institucional,
**para** poder ofrecer mis servicios como freelancer a clientes externos y a otros estudiantes.

## Criterios de Aceptación

- [x] **CA1:** El formulario de registro solicita: nombre completo, correo institucional (`@usantoto.edu.co`), contraseña, carrera y semestre.
- [x] **CA2:** El sistema valida que el correo pertenece al dominio institucional; de lo contrario, muestra un error claro.
- [x] **CA3:** La contraseña debe tener mínimo 8 caracteres, al menos una mayúscula y un número.
- [x] **CA4:** Al completar el registro, el sistema envía un correo de verificación al email ingresado.
- [x] **CA5:** La cuenta queda en estado `no verificado` hasta que el usuario confirme su correo.
- [x] **CA6:** No se permite registrar el mismo correo dos veces; el sistema muestra un mensaje de error si ya existe.
- [x] **CA7:** El rol asignado automáticamente es `freelancer`.

## Notas Técnicas

- Endpoint: `POST /api/auth/register/freelancer`
- Tabla(s): `users`
- Campos relevantes: `nombre`, `email`, `password_hash` (bcrypt), `rol = freelancer`, `carrera`, `semestre`, `verificado = false`
- Validación de dominio: regex `^[a-zA-Z0-9._%+-]+@usantoto\.edu\.co$`
- Se genera un token de verificación y se envía por email (ver US-004)
- Contraseña hasheada con `passlib[bcrypt]`

## Prioridad
`Alta`

## Estimación
`5` puntos de historia
