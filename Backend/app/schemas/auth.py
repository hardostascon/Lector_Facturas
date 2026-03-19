from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    nombre_usuario: str
    rol: str

class TokenData(BaseModel):
    email: Optional[str] = None
