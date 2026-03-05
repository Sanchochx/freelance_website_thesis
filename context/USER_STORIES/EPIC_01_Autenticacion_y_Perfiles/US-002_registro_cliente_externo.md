# US-002 — Registro de cliente externo

## Historia de Usuario

**Como** cliente externo (empresa o persona natural),
**quiero** registrarme en la plataforma con mi correo personal o empresarial,
**para** poder contratar servicios de los estudiantes freelancers.

## Criterios de Aceptación

- [ ] **CA1:** El formulario de registro solicita: nombre completo, correo (personal o empresarial), contraseña y —opcionalmente— nombre de empresa.
- [ ] **CA2:** El sistema acepta cualquier dominio de correo válido (no institucional).
- [ ] **CA3:** La contraseña debe tener mínimo 8 caracteres, al menos una mayúscula y un número.
- [ ] **CA4:** Al completar el registro, el sistema envía un correo de verificación.
- [ ] **CA5:** La cuenta queda en estado `no verificado` hasta que el usuario confirme su correo.
- [ ] **CA6:** El rol asignado automáticamente es `client`.
- [ ] **CA7:** Un cliente externo no puede publicar servicios; si intenta hacerlo, recibe un error 403.
- [ ] **CA8:** No se permite registrar el mismo correo dos veces.

## Notas Técnicas

- Endpoint: `POST /api/auth/register/client`
- Tabla(s): `users`
- Campos relevantes: `nombre`, `email`, `password_hash` (bcrypt), `rol = client`, `empresa` (opcional), `verificado = false`
- Validación de formato de email estándar (RFC 5322)
- No se valida dominio institucional
- Se genera un token de verificación y se envía por email (ver US-004)

## Prioridad
`Alta`

## Estimación
`3` puntos de historia
