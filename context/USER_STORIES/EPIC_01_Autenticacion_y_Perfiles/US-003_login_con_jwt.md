# US-003 — Inicio de sesión con JWT

## Historia de Usuario

**Como** usuario registrado (freelancer, cliente o administrador),
**quiero** iniciar sesión con mi correo y contraseña de forma segura,
**para** acceder a las funcionalidades de la plataforma según mi rol.

## Criterios de Aceptación

- [x] **CA1:** El formulario de login solicita correo electrónico y contraseña.
- [x] **CA2:** Si las credenciales son correctas, el sistema devuelve un JWT válido.
- [x] **CA3:** El JWT contiene el `user_id`, `rol` y tiempo de expiración (24 horas).
- [x] **CA4:** Si el correo o la contraseña son incorrectos, el sistema devuelve un error genérico sin especificar cuál campo es incorrecto.
- [x] **CA5:** Si la cuenta no está verificada, el sistema informa al usuario y le ofrece reenviar el correo de verificación.
- [x] **CA6:** El token se almacena en el cliente de forma segura (httpOnly cookie o localStorage según configuración).
- [x] **CA7:** Las rutas protegidas rechazan requests sin token válido con error 401.
- [x] **CA8:** El sistema soporta cierre de sesión invalidando el token en el cliente.

## Notas Técnicas

- Endpoint: `POST /api/auth/login`
- Tabla(s): `users`
- Librería: `PyJWT` + `passlib[bcrypt]`
- Payload del JWT: `{ "sub": user_id, "rol": rol, "exp": timestamp }`
- Tiempo de expiración: 24 horas (configurable por variable de entorno)
- En rutas protegidas: middleware de autenticación valida el token en cada request

## Prioridad
`Alta`

## Estimación
`3` puntos de historia
