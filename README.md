# Lector de Facturas

Sistema completo para la gestión y lectura automática de facturas mediante técnicas de OCR y LLM.

## Características

- **Extracción de texto**: Uso de EasyOCR para extraer texto de PDFs e imágenes
- **Procesamiento inteligente**: Integración con Ollama (LLM local) para parseo estructurado de datos
- **Gestión de facturas**: CRUD completo de facturas con detalles
- **Autenticación**: Sistema de autenticación JWT con tokens de acceso
- **Control de acceso**: Roles (admin, contador, usuario) con permisos diferenciados
- **Interfaz moderna**: Frontend construido con React, Tailwind CSS y componentes Radix UI

## Tecnologías

### Backend
- **API**: FastAPI
- **Base de datos**: PostgreSQL + SQLAlchemy (async)
- **OCR**: EasyOCR + PyMuPDF
- **LLM**: Ollama (modelo: llama3)
- **Autenticación**: JWT con Python-Jose

### Frontend
- **Framework**: React 18 + Vite
- **Estilos**: Tailwind CSS
- **Componentes**: Radix UI + Material UI
- **Rutas**: React Router
- **Formularios**: React Hook Form

## Requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL
- Ollama instalado localmente

## Estructura del Proyecto

```
Lector_Facturas/
├── Backend/               # API REST con FastAPI
│   ├── app/
│   │   ├── api/v1/endpoints/   # Endpoints de la API
│   │   ├── core/               # Configuración y seguridad
│   │   ├── db/                # Configuración de base de datos
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── schemas/           # Schemas Pydantic
│   │   ├── services/          # Lógica de negocio
│   │   └── utils/             # Utilidades
│   ├── alembic/               # Migraciones de base de datos
│   ├── uploads/               # Archivos subidos
│   └── main.py                # Punto de entrada
│
└── FrontEnd/              # Aplicación React
    ├── src/
    │   └── app/
    │       ├── components/    # Componentes UI
    │       ├── config/       # Configuración API
    │       └── pages/        # Páginas de la app
    ├── index.html
    └── package.json
```

## Instalación

### Backend

1.进入后端目录：
```bash
cd Backend
```

2.创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3.安装依赖：
```bash
pip install -r requirements.txt
```

4.配置数据库连接 `app/core/config.py`

5.创建数据库：
```bash
psql -U postgres -c "CREATE DATABASE facturas;"
```

6.运行迁移：
```bash
alembic upgrade head
```

7.启动 Ollama：
```bash
ollama serve
ollama pull llama3
```

### Frontend

1.进入前端目录：
```bash
cd FrontEnd
```

2.安装依赖：
```bash
npm install
```

## Uso

### Backend

```bash
cd Backend
uvicorn main:app --reload
```

API disponible en: `http://localhost:8000`
Documentación Swagger: `http://localhost:8000/docs`

### Frontend

```bash
cd FrontEnd
npm run dev
```

Aplicación disponible en: `http://localhost:5173`

## Endpoints Principales

### Autenticación
- `POST /api/v1/auth/login` - Iniciar sesión
- `POST /api/v1/auth/register` - Registrar usuario

### Facturas
- `GET /api/v1/facturas/` - Listar facturas
- `POST /api/v1/facturas/upload` - Subir y procesar factura
- `GET /api/v1/facturas/{id}` - Obtener factura por ID
- `PUT /api/v1/facturas/{id}` - Actualizar factura
- `DELETE /api/v1/facturas/{id}` - Eliminar factura

### Usuarios
- `GET /api/v1/usuarios/` - Listar usuarios
- `PUT /api/v1/usuarios/{id}` - Actualizar usuario

### Roles
- `GET /api/v1/roles/` - Listar roles

## Roles y Permisos

| Rol       | Permisos                              |
|-----------|---------------------------------------|
| admin     | CRUD completo, ver todas las facturas |
| contador | CRUD facturas, ver todas las facturas |
| user      | Crear/ver propias facturas           |

## Flujo de Procesamiento de Facturas

1. Usuario sube archivo (PDF/imagen) desde el frontend
2. OCR extrae texto del archivo
3. LLM parsea el texto a formato estructurado
4. Se guarda en la base de datos con detalles

## License

MIT