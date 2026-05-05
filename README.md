# E-commerce API

Aplicación full-stack de e-commerce con **FastAPI** en el backend y **React + Vite** en el frontend. Incluye autenticación JWT, gestión de catálogo (categorías y productos), carrito de compras, órdenes, panel de administración y subida de imágenes a Cloudinary.

---

## Stack Tecnológico

### Backend
- **Python 3.11+**
- **FastAPI** — framework web asíncrono
- **SQLAlchemy 2.0** — ORM
- **Alembic** — migraciones de base de datos
- **PostgreSQL** — base de datos (drivers `asyncpg` y `psycopg2-binary`)
- **Pydantic v2** + **pydantic-settings** — validación y configuración
- **PyJWT** — autenticación con tokens JWT
- **argon2-cffi** + **pwdlib** — hashing de contraseñas
- **Cloudinary** — almacenamiento de imágenes
- **pytest** + **pytest-asyncio** — testing

### Frontend
- **React 18**
- **Vite 6** — bundler y dev server
- **React Router DOM 6** — enrutamiento
- **Axios** — cliente HTTP
- **TailwindCSS 3** — estilos

---

## Estructura del proyecto

```
.
├── alembic/              # Migraciones de la base de datos
├── core/                 # Configuración, excepciones, seguridad
├── models/               # Modelos SQLAlchemy
├── schemas/              # Esquemas Pydantic (request/response)
├── routers/              # Endpoints de la API
├── services/             # Lógica de negocio
├── tests/                # Tests con pytest
├── frontend/             # Aplicación React + Vite
│   └── src/
│       ├── api/          # Cliente axios y módulos por recurso
│       ├── components/   # Componentes reutilizables
│       ├── context/      # Contextos React (auth, carrito, etc.)
│       └── pages/        # Páginas (Home, Cart, Login, admin/, ...)
├── main.py               # Entrypoint de FastAPI
├── alembic.ini
├── pytest.ini
└── requirements.txt
```

---

## Requisitos previos

- **Python 3.11 o superior**
- **Node.js 18 o superior** y **npm**
- **PostgreSQL 14+** corriendo localmente (o accesible por URL)
- Cuenta gratuita de **Cloudinary** (opcional, sólo si vas a usar la subida de imágenes)

---

## Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/raudev-h/E-commerce-API.git
cd "E-commerce API"
```

### 2. Variables de entorno (backend)

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Base de datos principal
DATABASE_URL=postgresql+psycopg2://usuario:password@localhost:5432/ecommerce

# Base de datos de tests (opcional, sólo para correr la suite)
TEST_DATABASE_URL=postgresql+psycopg2://usuario:password@localhost:5432/ecommerce_test

# Clave para firmar JWTs (usa una cadena larga y aleatoria)
SECRET_KEY=cambia-esto-por-una-cadena-segura

# Schema de PostgreSQL (por defecto: ecommerce)
DB_SCHEMA=ecommerce

# Orígenes permitidos por CORS (lista JSON)
CORS_ORIGINS=["http://localhost:5173"]

# Cloudinary (opcional)
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

### 3. Variables de entorno (frontend)

Crea un archivo `frontend/.env` para apuntar el cliente al backend local:

```env
VITE_API_URL=http://localhost:8000
```

Si no defines `VITE_API_URL`, el cliente apuntará a la URL de producción por defecto (`https://api.raudev-h.pro`).

---

## Instalación y ejecución

### Backend

```bash
# 1. Crear y activar entorno virtual
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (Git Bash)
source .venv/Scripts/activate
# macOS / Linux
source .venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear la base de datos en PostgreSQL
#    (desde psql o tu cliente preferido)
#    CREATE DATABASE ecommerce;

# 4. Aplicar migraciones
alembic upgrade head

# 5. Levantar el servidor
uvicorn main:app --reload
```

El backend quedará disponible en `http://localhost:8000`.
Documentación interactiva (Swagger UI): `http://localhost:8000/docs`
Documentación alternativa (ReDoc): `http://localhost:8000/redoc`

### Frontend

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

El frontend quedará disponible en `http://localhost:5173`.

---

## Comandos útiles

### Migraciones (Alembic)

```bash
# Crear una nueva migración a partir de cambios en los modelos
alembic revision --autogenerate -m "descripcion del cambio"

# Aplicar migraciones pendientes
alembic upgrade head

# Revertir la última migración
alembic downgrade -1
```

### Tests

```bash
# Asegúrate de tener TEST_DATABASE_URL configurado en .env
pytest
```

### Frontend

```bash
cd frontend
npm run dev        # servidor de desarrollo
npm run build      # build de producción
npm run preview    # previsualizar el build
```

---

## Funcionalidades

- Registro y login con JWT
- Catálogo público de categorías y productos
- Carrito de compras por usuario
- Creación y consulta de órdenes
- Subida de imágenes de productos a Cloudinary
- Panel de administración (`/admin`) para gestionar categorías, productos y usuarios

---

## Notas

- El backend usa un schema dedicado de PostgreSQL (`ecommerce` por defecto). Asegúrate de que el rol con el que conectas tenga permisos para crearlo o que ya exista.
- Si cambias el puerto del frontend, agrega el nuevo origen a `CORS_ORIGINS` en el `.env`.
- El endpoint de subida de imágenes requiere tener configuradas las credenciales de Cloudinary; el resto de la app funciona sin ellas.
