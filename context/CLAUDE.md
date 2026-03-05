# CLAUDE.md — FreelanceUSTA

Archivo de contexto técnico para Claude Code. Leer este archivo completo antes de escribir cualquier línea de código.

---

## 🎯 Descripción del Proyecto

**FreelanceUSTA** es un marketplace web fullstack donde estudiantes universitarios verificados ofrecen servicios freelance y clientes externos (empresas y personas naturales) los contratan. Funciona como un Fiverr/Workana pero con verificación institucional y enfoque en el ecosistema universitario colombiano.

---

## 🏗️ Arquitectura General

```
freelanceusta/
├── backend/                  # FastAPI + PostgreSQL
│   ├── app/
│   │   ├── main.py           # Entry point de la aplicación
│   │   ├── config.py         # Variables de entorno y configuración
│   │   ├── database.py       # Conexión a PostgreSQL con SQLAlchemy
│   │   ├── models/           # Modelos SQLAlchemy (tablas de BD)
│   │   ├── schemas/          # Schemas Pydantic (validación y serialización)
│   │   ├── routes/           # Endpoints FastAPI organizados por módulo
│   │   ├── services/         # Lógica de negocio separada de los endpoints
│   │   ├── middleware/       # CORS, autenticación, logging
│   │   └── utils/            # Helpers: email, cloudinary, mercadopago, jwt
│   ├── alembic/              # Migraciones de base de datos
│   ├── requirements.txt
│   └── .env
│
├── frontend/                 # React 19 + Tailwind CSS
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── components/       # Componentes reutilizables
│   │   │   ├── common/       # Button, Input, Modal, Badge, Avatar, etc.
│   │   │   ├── layout/       # Navbar, Sidebar, Footer
│   │   │   └── features/     # Componentes específicos por módulo
│   │   ├── pages/            # Páginas completas por ruta
│   │   ├── store/            # Estado global con Zustand
│   │   ├── services/         # Llamadas a la API con Axios
│   │   ├── hooks/            # Custom hooks
│   │   ├── utils/            # Helpers y constantes
│   │   └── assets/           # Imágenes, iconos, fuentes
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── .env
│
└── context/                  # Archivos de contexto del proyecto
    ├── IMPLEMENTATION_PLAN.md
    ├── TASK_EXECUTION.md
    ├── technical_spec.txt
    └── USER_STORIES/
        ├── EPIC_01_Autenticacion_y_Perfiles/
        ├── EPIC_02_Catalogo_de_Servicios/
        ├── EPIC_03_Sistema_de_Pedidos/
        ├── EPIC_04_Mensajeria_Interna/
        ├── EPIC_05_Resenas_y_Calificaciones/
        ├── EPIC_06_Pagos_y_Wallet/
        ├── EPIC_07_Busqueda_y_Filtros/
        ├── EPIC_08_Dashboard_y_Analitica/
        └── EPIC_09_Notificaciones/
```

---

## 🛠️ Stack Tecnológico

### Backend
| Tecnología | Versión | Uso |
|-----------|---------|-----|
| Python | 3.11+ | Lenguaje principal |
| FastAPI | Latest | Framework web |
| SQLAlchemy | 2.x | ORM |
| Alembic | Latest | Migraciones de BD |
| PostgreSQL | 15+ | Base de datos |
| PyJWT | Latest | Tokens JWT |
| passlib + bcrypt | Latest | Hash de contraseñas |
| python-dotenv | Latest | Variables de entorno |
| FastAPI-Mail | Latest | Envío de emails |
| cloudinary | Latest | Storage de imágenes y archivos |
| mercadopago | Latest | SDK de pagos (Sandbox) |
| websockets | Latest | Chat en tiempo real |
| uvicorn | Latest | Servidor ASGI |

### Frontend
| Tecnología | Versión | Uso |
|-----------|---------|-----|
| React | 19 | Framework UI |
| Vite | Latest | Build tool |
| Tailwind CSS | 3.x | Estilos |
| React Router | v6 | Routing |
| Zustand | Latest | Estado global |
| Axios | Latest | HTTP client |
| Socket.io-client | Latest | WebSockets (chat) |
| Recharts | Latest | Gráficas del dashboard |

---

## 🗄️ Modelo de Base de Datos

### Tabla: users
```sql
id              SERIAL PRIMARY KEY
nombre          VARCHAR(100) NOT NULL
email           VARCHAR(150) UNIQUE NOT NULL
password_hash   VARCHAR(255) NOT NULL
rol             VARCHAR(20) NOT NULL  -- 'freelancer' | 'client' | 'admin'
carrera         VARCHAR(100)          -- solo freelancers
semestre        INTEGER               -- solo freelancers
avatar_url      VARCHAR(255)
bio             TEXT
habilidades     TEXT[]                -- array de habilidades
wallet_balance  DECIMAL(12,2) DEFAULT 0
verificado      BOOLEAN DEFAULT FALSE
fecha_registro  TIMESTAMP DEFAULT NOW()
```

### Tabla: categories
```sql
id      SERIAL PRIMARY KEY
nombre  VARCHAR(100) NOT NULL
icono   VARCHAR(50)
```

### Tabla: services
```sql
id              SERIAL PRIMARY KEY
user_id         INTEGER FK → users
categoria_id    INTEGER FK → categories
titulo          VARCHAR(150) NOT NULL
descripcion     TEXT NOT NULL
precio_basico   DECIMAL(10,2) NOT NULL
precio_estandar DECIMAL(10,2)
precio_premium  DECIMAL(10,2)
tiempo_entrega  INTEGER               -- días
imagenes        TEXT[]                -- urls de Cloudinary
estado          VARCHAR(20) DEFAULT 'activo'  -- 'activo' | 'pausado' | 'agotado'
fecha_creacion  TIMESTAMP DEFAULT NOW()
```

### Tabla: orders
```sql
id               SERIAL PRIMARY KEY
service_id       INTEGER FK → services
client_id        INTEGER FK → users
freelancer_id    INTEGER FK → users
paquete          VARCHAR(20)   -- 'basico' | 'estandar' | 'premium'
estado           VARCHAR(30)   -- 'pendiente' | 'en_progreso' | 'en_revision' | 'completado' | 'cancelado'
precio           DECIMAL(10,2) NOT NULL
escrow_retenido  DECIMAL(10,2) NOT NULL
fecha_creacion   TIMESTAMP DEFAULT NOW()
fecha_completado TIMESTAMP
```

### Tabla: messages
```sql
id          SERIAL PRIMARY KEY
order_id    INTEGER FK → orders
sender_id   INTEGER FK → users
contenido   TEXT
archivo_url VARCHAR(255)
leido       BOOLEAN DEFAULT FALSE
timestamp   TIMESTAMP DEFAULT NOW()
```

### Tabla: reviews
```sql
id           SERIAL PRIMARY KEY
order_id     INTEGER FK → orders
reviewer_id  INTEGER FK → users
reviewed_id  INTEGER FK → users
rating       INTEGER NOT NULL  -- 1 a 5
comentario   TEXT
fecha        TIMESTAMP DEFAULT NOW()
```

### Tabla: transactions
```sql
id        SERIAL PRIMARY KEY
user_id   INTEGER FK → users
order_id  INTEGER FK → orders  -- nullable
tipo      VARCHAR(30)  -- 'recarga' | 'pago' | 'cobro' | 'retiro' | 'comision' | 'reembolso'
monto     DECIMAL(10,2) NOT NULL
estado    VARCHAR(20)  -- 'pendiente' | 'completado' | 'fallido'
fecha     TIMESTAMP DEFAULT NOW()
```

### Tabla: notifications
```sql
id       SERIAL PRIMARY KEY
user_id  INTEGER FK → users
tipo     VARCHAR(50)
mensaje  TEXT
leido    BOOLEAN DEFAULT FALSE
fecha    TIMESTAMP DEFAULT NOW()
```

---

## 🔐 Autenticación y Roles

- Autenticación con **JWT Bearer Token**
- Token expira en **24 horas**
- Roles disponibles: `freelancer`, `client`, `admin`
- Los **freelancers** se registran con correo institucional (se valida dominio)
- Los **clientes externos** se registran con cualquier correo
- Rutas protegidas por rol usando dependency injection de FastAPI

### Reglas por rol
| Acción | Freelancer | Client | Admin |
|--------|-----------|--------|-------|
| Publicar servicios | ✅ | ❌ | ✅ |
| Contratar servicios | ✅ | ✅ | ❌ |
| Ver dashboard propio | ✅ | ❌ | ❌ |
| Panel administración | ❌ | ❌ | ✅ |
| Moderar usuarios | ❌ | ❌ | ✅ |

---

## 💰 Reglas de Negocio — Pagos

- Todos los pagos son en **pesos colombianos (COP)**
- MercadoPago se usa en modo **Sandbox** (entorno de pruebas, sin dinero real)
- Credenciales de prueba: `ACCESS_TOKEN` de test de MercadoPago
- Se usan tarjetas y usuarios de prueba para simular transacciones
- **Flujo de escrow:**
  1. Cliente crea pedido → monto se descuenta de su wallet y queda retenido
  2. Pedido completado → sistema descuenta 10% de comisión y acredita al freelancer
  3. Pedido cancelado antes de iniciar → reembolso total al wallet del cliente
- La comisión del 10% va a la cuenta de la plataforma (admin)
- Un freelancer no puede contratarse a sí mismo

---

## 📡 Convenciones de API

### Estructura de endpoints
```
GET     /api/v1/{recurso}           → Listar
POST    /api/v1/{recurso}           → Crear
GET     /api/v1/{recurso}/{id}      → Detalle
PUT     /api/v1/{recurso}/{id}      → Actualizar
DELETE  /api/v1/{recurso}/{id}      → Eliminar
```

### Respuesta estándar exitosa
```json
{
  "success": true,
  "data": { ... },
  "message": "Operación exitosa"
}
```

### Respuesta estándar de error
```json
{
  "success": false,
  "error": "Descripción del error",
  "detail": "Detalle técnico opcional"
}
```

### Códigos HTTP usados
| Código | Uso |
|--------|-----|
| 200 | Éxito general |
| 201 | Recurso creado |
| 400 | Error de validación |
| 401 | No autenticado |
| 403 | Sin permisos |
| 404 | No encontrado |
| 422 | Error de schema Pydantic |
| 500 | Error interno |

---

## 📁 Convenciones de Código

### Backend (Python)
- `snake_case` para variables, funciones y archivos
- `PascalCase` para clases (modelos, schemas)
- Un archivo por modelo en `models/`
- Un archivo por recurso en `routes/`
- La lógica de negocio va en `services/`, no en `routes/`
- Usar `Depends()` de FastAPI para inyección de dependencias
- Todos los endpoints deben tener docstring

### Frontend (JavaScript/React)
- `PascalCase` para componentes y archivos de componentes
- `camelCase` para variables, funciones y hooks
- `kebab-case` para archivos que no son componentes
- Un componente por archivo
- Los custom hooks comienzan con `use` (ej: `useAuth`, `useOrders`)
- Los servicios de API van en `src/services/` con un archivo por módulo
- El estado global en Zustand se organiza por store (`useAuthStore`, `useOrderStore`)

---

## 🌐 Variables de Entorno

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/freelanceusta
SECRET_KEY=tu_secret_key_muy_seguro
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24

MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_app_password
MAIL_FROM=noreply@freelanceusta.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com

CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret

MP_ACCESS_TOKEN=TEST-xxxxxxxxxxxx  # Sandbox token de MercadoPago

FRONTEND_URL=http://localhost:5173
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
```

---

## 🚀 Comandos de Desarrollo

### Backend
```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor de desarrollo
uvicorn app.main:app --reload --port 8000

# Crear migración
alembic revision --autogenerate -m "descripcion"

# Aplicar migraciones
alembic upgrade head
```

### Frontend
```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Build de producción
npm run build
```

---

## ⚠️ Reglas Importantes

1. **Nunca** hardcodear credenciales en el código — siempre usar `.env`
2. **Nunca** saltar una historia de usuario del plan de implementación
3. **Siempre** crear la migración de Alembic al agregar o modificar un modelo
4. **Siempre** validar el rol del usuario antes de ejecutar operaciones sensibles
5. **Nunca** exponer el `password_hash` en ninguna respuesta de la API
6. **Siempre** usar el `wallet_balance` con transacciones atómicas para evitar inconsistencias
7. Los WebSockets del chat van en `backend/app/routes/ws.py`
8. Las imágenes y archivos **siempre** se suben a Cloudinary, nunca al servidor local

---

## 📌 Orden de Implementación

Seguir estrictamente el orden del `IMPLEMENTATION_PLAN.md`:

1. EPIC_01 — Autenticación y Perfiles
2. EPIC_02 — Catálogo de Servicios
3. EPIC_03 — Sistema de Pedidos
4. EPIC_04 — Mensajería Interna
5. EPIC_05 — Reseñas y Calificaciones
6. EPIC_06 — Pagos y Wallet
7. EPIC_07 — Búsqueda y Filtros
8. EPIC_08 — Dashboard y Analítica
9. EPIC_09 — Notificaciones
