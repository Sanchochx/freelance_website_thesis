# US-013 — Definir paquetes básico, estándar y premium

## Historia de Usuario

**Como** freelancer,
**quiero** definir hasta tres paquetes de precio (básico, estándar y premium) para cada servicio,
**para** ofrecer distintos niveles de alcance y que el cliente elija según su presupuesto.

## Criterios de Aceptación

- [ ] **CA1:** Al crear o editar un servicio, el freelancer puede definir entre 1 y 3 paquetes.
- [ ] **CA2:** Cada paquete incluye: nombre (básico/estándar/premium), descripción del alcance, precio en COP y tiempo de entrega en días.
- [ ] **CA3:** El precio debe ser mayor a COP $0 y hasta COP $5.000.000.
- [ ] **CA4:** El precio del paquete estándar debe ser igual o mayor al básico; el premium igual o mayor al estándar.
- [ ] **CA5:** El tiempo de entrega mínimo es de 1 día y máximo de 90 días.
- [ ] **CA6:** En la vista pública del servicio, los tres paquetes se muestran en columnas comparativas.
- [ ] **CA7:** El cliente selecciona un paquete al momento de crear el pedido.

## Notas Técnicas

- Endpoint: Los paquetes se gestionan como parte de `POST /api/services` y `PUT /api/services/{service_id}`
- Tabla(s): `services`
- Campos: `precio_basico`, `precio_estandar`, `precio_premium`, `tiempo_entrega_basico`, `tiempo_entrega_estandar`, `tiempo_entrega_premium`, `descripcion_basico`, `descripcion_estandar`, `descripcion_premium`
- Validación de precios escalonados en el backend
- Si solo se define un paquete, se toma como paquete único (sin distinción de nivel)

## Prioridad
`Alta`

## Estimación
`3` puntos de historia
