from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.db.session import get_async_session
from app.services.usuario_service import UsuarioService
from app.core.security import create_access_token
from app.schemas.auth import Token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(get_async_session),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Endpoint de login estándar de OAuth2. 
    Recibe 'username' (que es el email) y 'password'.
    """
    service = UsuarioService(db)
    usuario = await service.autenticar(form_data.username, form_data.password)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Datos que irán dentro del token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": usuario.email, 
            "rol": usuario.rol.nombre if usuario.rol else "usuario",
            "user_id": usuario.id
        }
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": usuario.id,
        "nombre_usuario": f"{usuario.nombre} {usuario.apellido}",
        "rol": usuario.rol.nombre if usuario.rol else "usuario"
    }
