from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_async_session
from app.schemas.roles import RolOut, RolCreate, RolUpdate
from app.services.roles_service import RolService
from app.core.dependencies import get_current_user, require_roles
from app.models.usuario import Usuario

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=List[RolOut])
async def listar_roles(
    db: AsyncSession = Depends(get_async_session),
    usuario_actual: Usuario = Depends(get_current_user),
):
    service = RolService(db)
    return await service.obtener_todosRoles()

@router.post("/", response_model=RolOut, status_code=status.HTTP_201_CREATED)
async def crear_rol(
    rol_data: RolCreate,
    db: AsyncSession = Depends(get_async_session),
    usuario_actual: Usuario = Depends(require_roles(["admin"])),
):
    service = RolService(db)
    return await service.crearRol(rol_data)

@router.get("/{id}", response_model=RolOut)
async def obtener_rol(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    usuario_actual: Usuario = Depends(get_current_user),
):
    service = RolService(db)
    rol = await service.obtenerRol_por_id(id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol
