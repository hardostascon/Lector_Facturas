from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime
from app.db.session import get_async_session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioDelete, UsuarioResponse
from app.services.usuario_service import UsuarioService

from app.core.dependencies import get_current_user, require_roles

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/", response_model=List[UsuarioResponse])
async def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    rol_id: int = None,
    search: str = None,
    db: AsyncSession = Depends(get_async_session),
    usuario_actual: Usuario = Depends(get_current_user),
):
    service = UsuarioService(db)
    
    # Restricción: Los usuarios normales solo ven sus propias facturas.
    # Los admin y contador ven TODO.
    if usuario_actual.rol and usuario_actual.rol.nombre in ["admin", "contador"]:
        return await service.obtener_todosUsuarios(skip=skip, limit=limit, rol_id=rol_id, search=search)
    
    # Los usuarios normales solo se ven a sí mismos
    return await service.obtener_usuarios_por_usuario(usuario_actual.id)

@router.get("/{id}", response_model=UsuarioResponse)
async def obtener_usuario(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    usuario_actual: Usuario = Depends(get_current_user),
):
    service = UsuarioService(db)
    usuario = await service.obtenerUsuario_por_id(id)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificación de propiedad (si no es admin/contador)
    es_admin_o_contador = usuario_actual.rol and usuario_actual.rol.nombre in ["admin", "contador"]
    if not es_admin_o_contador and usuario.id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este usuario")
        
    return usuario


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(
    usuario_data: UsuarioCreate,
    db: AsyncSession = Depends(get_async_session),
    usuario_actual: Usuario = Depends(require_roles(["admin", "contador"])), 
):
    service = UsuarioService(db)
    return await service.crearUsuario(usuario_data)
    
@router.put("/{id}", response_model=UsuarioResponse)
async def actualizar_usuario(
    id: int,
    usuario_data: UsuarioUpdate,
    db: AsyncSession = Depends(get_async_session),
    usuario_actual: Usuario = Depends(require_roles(["admin", "contador"])),
):
    service = UsuarioService(db)
    usuario = await service.actualizarUsuario(id, usuario_data)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario  

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    usuario_actual: Usuario = Depends(require_roles(["admin"])),
):
    service = UsuarioService(db)
    success = await service.eliminarUsuario(id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return None
