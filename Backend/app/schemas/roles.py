from pydantic import BaseModel
from typing import Optional

class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class RolCreate(RolBase):
    pass

class RolUpdate(BaseModel):
    id: int
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class RolOut(RolBase):
    id: int
    estado: bool

    class Config:
        from_attributes = True
