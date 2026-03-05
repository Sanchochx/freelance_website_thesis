# US-046 — Email al freelancer cuando llega un nuevo pedido

## Historia de Usuario

**Como** freelancer,
**quiero** recibir un email cuando un cliente crea un nuevo pedido para uno de mis servicios,
**para** ser notificado rápidamente y responder dentro del tiempo límite de 48 horas.

## Criterios de Aceptación

- [ ] **CA1:** Al crear un pedido, el sistema envía automáticamente un email al freelancer correspondiente.
- [ ] **CA2:** El email incluye: nombre del cliente, servicio contratado, paquete seleccionado, monto y mensaje inicial del cliente.
- [ ] **CA3:** El email contiene un enlace directo al detalle del pedido en la plataforma.
- [ ] **CA4:** El email se envía en los primeros 2 minutos tras la creación del pedido.
- [ ] **CA5:** Si el envío del email falla, el sistema lo reintenta hasta 3 veces con intervalo de 5 minutos.
- [ ] **CA6:** El freelancer también recibe una notificación dentro de la plataforma (ver US-048).

## Notas Técnicas

- Disparador: `POST /api/orders` (al completarse la creación del pedido)
- Tabla(s): `notifications`, `users`, `orders`
- Librería: `FastAPI-Mail`
- Plantilla de email HTML con información del pedido
- El envío se realiza de forma asíncrona (background task en FastAPI o tarea Celery)
- Se registra en `notifications` con `tipo = 'nuevo_pedido'` y `user_id = freelancer_id`

## Prioridad
`Alta`

## Estimación
`3` puntos de historia
