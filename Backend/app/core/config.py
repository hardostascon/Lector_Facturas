from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    user: str = 'postgres'
    password: str = '123456'
    host: str = 'localhost'
    port: str = '5432'
    database: str = 'facturas'
    DATABASE_URL: str = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
    
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    
    # Seguridad
    SECRET_KEY: str = "tu_super_secreto_muy_seguro_aqui_1234567890" # CAMBIAR EN PRODUCCIÓN
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
