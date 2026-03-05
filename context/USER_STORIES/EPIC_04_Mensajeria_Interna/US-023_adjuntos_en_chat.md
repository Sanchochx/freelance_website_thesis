# US-023 — Enviar archivos adjuntos en el chat

## Historia de Usuario

**Como** usuario (cliente o freelancer),
**quiero** poder enviar archivos adjuntos dentro del chat de un pedido,
**para** compartir referencias, documentos o avances sin salir de la plataforma.

## Criterios de Aceptación

- [ ] **CA1:** El usuario puede adjuntar un archivo junto con (o sin) un mensaje de texto.
- [ ] **CA2:** Se permiten los formatos: PDF, DOC, DOCX, XLS, XLSX, ZIP, PNG, JPG, WEBP.
- [ ] **CA3:** El tamaño máximo por archivo adjunto es de 25 MB.
- [ ] **CA4:** Los archivos se muestran como preview (imágenes) o como enlace con nombre e ícono de tipo de archivo.
- [ ] **CA5:** El receptor puede descargar el archivo haciendo clic en él.
- [ ] **CA6:** Si el archivo supera el tamaño permitido o tiene un formato no soportado, se muestra un error antes de intentar la carga.

## Notas Técnicas

- Endpoint: `POST /api/messages/{order_id}/attachment` (multipart/form-data)
- Tabla(s): `messages`
- El archivo se sube a Cloudinary; la URL se guarda en `messages.archivo_url`
- El mensaje se crea con `contenido` (texto, puede estar vacío) + `archivo_url`
- Validación de MIME type y tamaño en el backend antes de subir a Cloudinary
- Se distribuye en tiempo real por WebSocket como mensaje con tipo `attachment`

## Prioridad
`Media`

## Estimación
`3` puntos de historia
