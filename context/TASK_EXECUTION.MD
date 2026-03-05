# 📋 TASK EXECUTION WORKFLOW

**Versión:** 2.0
**Última actualización:** 2026-03-04

---

## 📁 Context Files

Antes de comenzar cualquier tarea, revisar estos archivos clave:

- **`@context/IMPLEMENTATION_PLAN.md`** - Plan maestro con historias de usuario y progreso por fases
- **`@context/USER_STORIES`** - Todas las historias de usuario
- **`@CLAUDE.md`** - Detalles del proyecto, stack tecnológico y estándares de código
- **`@context/technical_spec.txt`** - Reglas de negocio, módulos y stack técnico del sistema

---

## 🔄 Execution Process

### 1. Find Next User Story

- Localiza la **primera historia de usuario no marcada** (con `[ ]`) en `IMPLEMENTATION_PLAN.md`
- Lee el archivo completo de la historia de usuario para entender TODOS los criterios de aceptación
- Verifica las dependencias antes de comenzar

**Ejemplo:**
```markdown
[ ] US-AUTH-001: Registro de Usuario
```

---

### 2. Implement Each Acceptance Criterion

**Regla de oro:** Trabaja los criterios **UNO A LA VEZ** (no te adelantes)

Para cada criterio de aceptación:

1. **Explica qué vas a construir y por qué**
   - Describe el objetivo del criterio
   - Menciona cómo se relaciona con la arquitectura general

2. **Crea/modifica archivos en los directorios correctos**
   - Sigue la estructura del proyecto definida en `CLAUDE.md`
   - Respeta la organización de carpetas existente

3. **Aplica estándares y convenciones**
   - Sigue las convenciones de código de `CLAUDE.md`
   - Mantén consistencia con el código existente

4. **Marca el criterio como completado**
   - En el archivo de la historia de usuario, marca: `[x]` cuando termines

**Ejemplo de progreso en archivo de US:**
```markdown

## Criterios de Aceptación

- [x] El sistema debe permitir registro con email y contraseña
- [x] Las contraseñas deben estar hasheadas
- [ ] Debe validar formato de email
- [ ] Debe enviar email de confirmación
```

---

### 3. Complete the User Story

- **Después de que TODOS los criterios estén marcados `[x]`:**
  - Marca la historia de usuario como completa `[x]` en `IMPLEMENTATION_PLAN.md`
  - Actualiza las métricas del dashboard (contadores y barras de progreso)

**Ejemplo en IMPLEMENTATION_PLAN.md:**
```markdown
[x] US-AUTH-001:
```

---

### 4. Checkpoint

Después de completar cada historia de usuario:

1. **Muestra un resumen de lo implementado:**
   - Archivos creados/modificados
   - Funcionalidades implementadas
   - Decisiones técnicas tomadas

2. **Solicita confirmación antes de continuar:**
   - Espera aprobación del usuario
   - No avances automáticamente a la siguiente US

**Ejemplo de resumen:**
```
✅ US-AUTH-001 Completada

Archivos creados:
- backend/app/models/user.py - Modelo de usuario con hash de contraseña
- backend/app/routes/auth.py - Endpoints de registro
- backend/app/schemas/user.py - Validación con Pydantic

Funcionalidades:
- Registro con validación de email
- Hash de contraseñas con bcrypt
- Validación de campos requeridos

¿Proceder con US-AUTH-002?
```

---

### 5. Create Phase Summary

**Cuándo:** Al completar TODAS las historias de usuario de una fase completa

**Qué crear:** Un documento resumen con nombre: `user-story-[EPIC-NAME]-resume.md`

**Contenido del resumen:**

#### 📝 Changes Made
Descripción de alto nivel de lo implementado en la fase:
- Módulos principales creados
- Funcionalidades core implementadas
- Integraciones realizadas

#### 📂 Files Modified/Created
Lista detallada de cada archivo con:
- Ruta del archivo
- Propósito del archivo
- Cambios principales realizados

#### 🎯 Rationale
Explicación clara para contexto de LLM:
- Qué se completó y por qué
- Cómo encaja en la arquitectura general
- Decisiones de diseño importantes
- Patrones utilizados

#### 🚀 Next Steps
- Qué fase viene después
- Dependencias o prerrequisitos
- Consideraciones para la siguiente fase

**Propósito:** Ayudar a futuras sesiones de LLM a entender el estado del proyecto sin releer todo el código

---

### 6. Check User Story in Implementation Plan

Después de completar una historia:
- ✅ Marca la US como `[x]` en `IMPLEMENTATION_PLAN.md`
- 📊 Actualiza métricas del dashboard
- 🔄 Actualiza barras de progreso de épica y fase

---

### 7. Wait for Instruction and Review

⚠️ **IMPORTANTE:**
- **Espera instrucciones del usuario** antes de continuar
- **No hagas nada adicional** que no esté incluido en el workflow
- **No te adelantes** a la siguiente historia sin autorización

---

### 8. Wait for Instruction and Review

⚠️ **CRÍTICO:**
- **Solicita revisión** después de cada historia completada
- **No asumas** que debes continuar automáticamente
- **Pregunta explícitamente** si proceder con la siguiente US

---

## ⚠️ Important Guidelines

### 🏗️ Architecture
- **Sigue CLAUDE.md** para todas las decisiones técnicas:
  - Arquitectura del proyecto
  - Estándares de código
  - Organización de archivos
  - Convenciones de nombres

### 📈 Incremental Work
- **Completa un criterio antes de comenzar el siguiente**
- No intentes hacer múltiples criterios simultáneamente
- Mantén commits pequeños y atómicos

### 📝 Documentation
- **Actualiza documentación conforme avanzas**, no al final
- Documenta decisiones técnicas importantes
- Mantén comentarios en el código cuando sea necesario

### 🧪 Testing
- **Implementación solamente** - no escribas tests a menos que la US lo requiera explícitamente
- Si la US incluye criterios de testing, impleméntalos

### ❓ Questions
- **Pregunta si algo no está claro**
- Si los criterios de aceptación son ambiguos, solicita aclaración
- Si hay conflictos con la arquitectura existente, discútelo antes de implementar

---

## 🎯 Best Practices

### ✅ DO:
- Leer toda la historia de usuario antes de comenzar
- Seguir el orden establecido en IMPLEMENTATION_PLAN.md
- Marcar progreso en tiempo real
- Solicitar confirmación después de cada US
- Explicar decisiones técnicas

### ❌ DON'T:
- Saltarte historias de usuario
- Trabajar en múltiples US simultáneamente
- Asumir implementaciones sin revisar criterios
- Avanzar sin autorización del usuario
- Modificar archivos fuera del alcance de la US actual

---

## 🔍 Verification Checklist

Antes de marcar una US como completa, verificar:

- [ ] Todos los criterios de aceptación están marcados `[x]`
- [ ] Los archivos están en los directorios correctos
- [ ] El código sigue los estándares de `CLAUDE.md`
- [ ] La documentación está actualizada
- [ ] No hay código comentado sin razón
- [ ] Las funcionalidades funcionan según los criterios

---

## 📌 Quick Reference

| Archivo | Propósito |
|---------|-----------|
| `IMPLEMENTATION_PLAN.md` | Plan maestro con todas las US y progreso |
| `CLAUDE.md` | Detalles técnicos y estándares del proyecto |
| `context/USER_STORIES/` | Archivos individuales de historias de usuario |

---

## 🚀 Getting Started

Para comenzar la implementación:

1. Abre `IMPLEMENTATION_PLAN.md`
2. Busca la primera US con `[ ]` en Fase 1
3. Lee el archivo completo de esa US
4. Sigue este workflow paso a paso
5. Solicita confirmación antes de avanzar

---

**¡Importante!** Este workflow está diseñado para trabajo incremental y colaborativo. Siempre espera confirmación del usuario antes de proceder a la siguiente historia.
