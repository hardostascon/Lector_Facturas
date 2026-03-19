# Lector de Facturas API

API REST para la gestión y lectura automática de facturas mediante técnicas de OCR y LLM.

## Características

- **Extracción de texto**: Uso de EasyOCR para extraer texto de PDFs e imágenes
- **Procesamiento inteligente**: Integración con Ollama (LLM local) para parseo estructurado de datos
- **Gestión de facturas**: CRUD completo de facturas con detalles
- **Autenticación**: Sistema de autenticación JWT con tokens de acceso
- **Control de acceso**: Roles (admin, contador, usuario) con permisos diferenciados
- **Base de datos**: PostgreSQL con SQLAlchemy async

## Tecnologías

- **Backend**: FastAPI
- **Base de datos**: PostgreSQL + SQLAlchemy (async)
- **OCR**: EasyOCR + PyMuPDF
- **LLM**: Ollama (modelo: llama3)
- **Autenticación**: JWT con Python-Jose

## Requisitos

- Python 3.11+
- PostgreSQL
- Ollama instalado localmente

## Instalación

1. Clonar el repositorio:
```bash
git clone <repo-url>
cd Backend
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno en `app/core/config.py`:
```python
# Database
user: str = 'postgres'
password: str = 'tu_password'
host: str = 'localhost'
port: str = '5432'
database: str = 'facturas'

# Security
SECRET_KEY: str = "tu_super_secreto_muy_seguro_aqui_1234567890"
```

5. Crear la base de datos:
```bash
psql -U postgres -c "CREATE DATABASE facturas;"
```

6. Ejecutar migraciones:
```bash
alembic upgrade head
```

7. Iniciar Ollama:
```bash
ollama serve
ollama pull llama3
```

## Uso

Iniciar el servidor:
```bash
uvicorn main:app --reload
```

La API estará disponible en: `http://localhost:8000`

Documentación Swagger: `http://localhost:8000/docs`

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

## Estructura del Proyecto

```
Backend/
├── app/
│   ├── api/v1/endpoints/   # Endpoints de la API
│   ├── core/               # Configuración y seguridad
│   ├── db/                # Configuración de base de datos
│   ├── models/            # Modelos SQLAlchemy
│   ├── schemas/           # Schemas Pydantic
│   ├── services/          # Lógica de negocio
│   └── utils/             # Utilidades
├── alembic/               # Migraciones de base de datos
├── uploads/               # Archivos subidos
└── main.py                # Punto de entrada
```

## Roles y Permisos

| Rol       | Permisos                              |
|-----------|---------------------------------------|
| admin     | CRUD completo, ver todas las facturas |
| contador | CRUD facturas, ver todas las facturas |
| user      | Crear/ver propias facturas           |

## Flujo de Procesamiento de Facturas

1. Usuario sube archivo (PDF/imagen)
2. OCR extrae texto del archivo
3. LLM parsea el texto a formato estructurado
4. Se guarda en la base de datos con detalles

## License

MIT