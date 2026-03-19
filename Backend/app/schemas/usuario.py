import re
from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional
from datetime import date
from app.schemas.roles import RolOut

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    fecha_nacimiento: Optional[date] = None
    genero: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    codigo_postal: Optional[str] = None
    ciudad: Optional[str] = None
    provincia: Optional[str] = None
    pais: Optional[str] = None
    rol_id: int
    fecha_creacion: Optional[date] = None
    fecha_actualizacion: Optional[date] = None

class UsuarioCreate(UsuarioBase):
    password: str
    confirmar_password: str
    @field_validator('password')
    @classmethod
    def password_minimo(cls, v):
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return v
    @model_validator(mode="after")
    def password_coincide(self) -> "UsuarioCreate":
        if self.password != self.confirmar_password:
            raise ValueError("Las contraseñas no coinciden")
        return self
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise ValueError("Email inválido")
        return v

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    fecha_nacimiento: Optional[date] = None
    genero: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    codigo_postal: Optional[str] = None
    ciudad: Optional[str] = None
    provincia: Optional[str] = None
    pais: Optional[str] = None
    rol_id: Optional[int] = None
    password: Optional[str] = None
    fecha_creacion: Optional[date] = None
    fecha_actualizacion: Optional[date] = None

class UsuarioDelete(BaseModel):
    id: int

class UsuarioResponse(UsuarioBase):
    id: int
    nombre: str
    apellido: str
    email: EmailStr
    fecha_nacimiento: Optional[date] = None
    genero: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    codigo_postal: Optional[str] = None
    ciudad: Optional[str] = None
    provincia: Optional[str] = None
    pais: Optional[str] = None
    rol_id: int
    fecha_creacion: Optional[date] = None
    fecha_actualizacion: Optional[date] = None
    rol: RolOut

    class Config:
        from_attributes = True


class UsuarioOut(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
