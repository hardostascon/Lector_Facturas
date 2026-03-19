
# 🧾 Lector de Facturas

Sistema completo para la gestión y lectura automática de facturas mediante OCR y modelos de lenguaje (LLM) locales.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-latest-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## ✨ Características

| Módulo | Descripción |
|---|---|
| 📄 **Extracción OCR** | Lectura automática de texto desde PDFs e imágenes con EasyOCR |
| 🤖 **Procesamiento LLM** | Parseo estructurado de datos con Ollama (llama3) ejecutado localmente |
| 🗂️ **Gestión de facturas** | CRUD completo con historial y detalles por factura |
| 🔐 **Autenticación JWT** | Tokens de acceso seguros con Python-Jose |
| 👥 **Control de acceso** | Sistema de roles diferenciados (admin, contador, usuario) |
| 🎨 **Interfaz moderna** | Frontend en React 18 con Tailwind CSS y componentes Radix UI |

---

## 🛠️ Tecnologías

### Backend
- **API**: [FastAPI](https://fastapi.tiangolo.com/)
- **Base de datos**: PostgreSQL + SQLAlchemy (async)
- **OCR**: EasyOCR + PyMuPDF
- **LLM**: [Ollama](https://ollama.com/) — modelo `llama3`
- **Autenticación**: JWT con Python-Jose
- **Migraciones**: Alembic

### Frontend
- **Framework**: React 18 + Vite
- **Estilos**: Tailwind CSS
- **Componentes**: Radix UI + Material UI
- **Rutas**: React Router
- **Formularios**: React Hook Form

---

## 📋 Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

- [Python 3.11+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Ollama](https://ollama.com/) — para ejecutar el modelo LLM localmente

---

## 📁 Estructura del proyecto

```
Lector_Facturas/
├── Backend/
│   ├── app/
│   │   ├── api/v1/endpoints/   # Endpoints de la API
│   │   ├── core/               # Configuración y seguridad
│   │   ├── db/                 # Configuración de base de datos
│   │   ├── models/             # Modelos SQLAlchemy
│   │   ├── schemas/            # Schemas Pydantic
│   │   ├── services/           # Lógica de negocio (OCR, LLM)
│   │   └── utils/              # Utilidades generales
│   ├── alembic/                # Migraciones de base de datos
│   ├── uploads/                # Archivos subidos por los usuarios
│   ├── requirements.txt
│   └── main.py                 # Punto de entrada de la API
│
└── FrontEnd/
    ├── src/
    │   └── app/
    │       ├── components/     # Componentes reutilizables de UI
    │       ├── config/         # Configuración de la API
    │       └── pages/          # Páginas de la aplicación
    ├── index.html
    ├── package.json
    └── vite.config.js
```

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/lector-facturas.git
cd lector-facturas
```

### 2. Configurar el Backend

```bash
# Entrar al directorio del backend
cd Backend

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate      # Linux / macOS
# venv\Scripts\activate       # Windows

# Instalar dependencias
pip install -r requirements.txt
```

Crea el archivo de configuración copiando el ejemplo:

```bash
cp app/core/config.example.py app/core/config.py
```

Edita `app/core/config.py` con tus valores:

```python
DATABASE_URL = "postgresql+asyncpg://usuario:contraseña@localhost/facturas"
SECRET_KEY = "tu_clave_secreta_aqui"
OLLAMA_BASE_URL = "http://localhost:11434"
```

Crea la base de datos y ejecuta las migraciones:

```bash
psql -U postgres -c "CREATE DATABASE facturas;"
alembic upgrade head
```

Inicia el servidor de Ollama y descarga el modelo:

```bash
ollama serve
ollama pull llama3
```

### 3. Configurar el Frontend

```bash
cd FrontEnd
npm install
```

Crea el archivo de entorno:

```bash
cp .env.example .env
```

Edita `.env`:

```
VITE_API_URL=http://localhost:8000
```

---

## ▶️ Uso

### Iniciar el Backend

```bash
cd Backend
source venv/bin/activate      # Si no está activo
uvicorn main:app --reload
```

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Iniciar el Frontend

```bash
cd FrontEnd
npm run dev
```

- **Aplicación**: http://localhost:5173

> 💡 Asegúrate de que `ollama serve` esté corriendo antes de procesar facturas.

---

## 📡 Endpoints

### Autenticación
| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/v1/auth/login` | Iniciar sesión |
| `POST` | `/api/v1/auth/register` | Registrar nuevo usuario |

### Facturas
| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/v1/facturas/` | Listar todas las facturas |
| `POST` | `/api/v1/facturas/upload` | Subir y procesar una factura |
| `GET` | `/api/v1/facturas/{id}` | Obtener factura por ID |
| `PUT` | `/api/v1/facturas/{id}` | Actualizar factura |
| `DELETE` | `/api/v1/facturas/{id}` | Eliminar factura |

### Usuarios
| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/v1/usuarios/` | Listar usuarios (solo admin) |
| `PUT` | `/api/v1/usuarios/{id}` | Actualizar datos de usuario |

### Roles
| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/v1/roles/` | Listar roles disponibles |

---

## 🔒 Roles y Permisos

| Rol | Ver propias facturas | Ver todas las facturas | Crear / Editar | Eliminar | Gestión de usuarios |
|---|:---:|:---:|:---:|:---:|:---:|
| `admin` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `contador` | ✅ | ✅ | ✅ | ✅ | ❌ |
| `usuario` | ✅ | ❌ | ✅ | ❌ | ❌ |

---

## 🔄 Flujo de procesamiento de una factura

```
Usuario sube PDF/Imagen
        │
        ▼
   EasyOCR extrae
   el texto del archivo
        │
        ▼
   Ollama (llama3) parsea
   el texto a JSON estructurado
        │
        ▼
   Se valida con
   schemas Pydantic
        │
        ▼
   Se guarda en PostgreSQL
   con todos sus detalles
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Haz un fork del repositorio
2. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. Haz commit de tus cambios: `git commit -m 'feat: agrega nueva funcionalidad'`
4. Sube tu rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).
