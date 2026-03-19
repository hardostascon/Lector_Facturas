from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from app.api.v1.endpoints import auth, facturas, usuario, roles
from app.core.config import settings

app = FastAPI(
    title="Lector de Facturas API",
    description="API para la gestión y lectura de facturas mediante OCR",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración de CORS
# Para evitar problemas de puerto o hostname en desarrollo usamos "*"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos (facturas PDF/JPG)
# Nos aseguramos de que la carpeta uploads exista
if not os.path.exists("uploads"):
    os.makedirs("uploads")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Registro de Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(facturas.router, prefix=settings.API_V1_STR)
app.include_router(usuario.router, prefix=settings.API_V1_STR)
app.include_router(roles.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "mensaje": "Bienvenido a la API de Lector de Facturas",
        "docs": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
