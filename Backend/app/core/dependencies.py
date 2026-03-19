from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_async_session
from app.core.security import verify_token
from app.models.usuario import Usuario
from app.models.roles import Roles

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_session),
) -> Usuario:
    """
    Decodifica el JWT, busca al usuario en la BD y lo retorna con su rol cargado.
    Lanza 401 si el token es inválido o el usuario no existe.
    """
    payload = verify_token(token)
    email: str = payload.get("sub")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no contiene un sujeto válido",
        )

    # Cargamos la relación 'rol' para evitar consultas extras después
    result = await db.execute(
        select(Usuario)
        .where(Usuario.email == email)
        .options(selectinload(Usuario.rol))
    )
    usuario = result.scalar_one_or_none()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )

    return usuario

def require_roles(roles_permitidos: List[str]):
    """
    Retorna una dependencia que verifica que el usuario tenga
    uno de los roles indicados en la lista (comparando por nombre).
    """
    async def verificar_rol(
        usuario: Usuario = Depends(get_current_user),
    ) -> Usuario:
        if not usuario.rol or usuario.rol.nombre not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere uno de los roles: {roles_permitidos}",
            )
        return usuario

    return verificar_rol