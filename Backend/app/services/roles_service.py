from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.roles import Roles
from app.core.exceptions import NotFoundException
from app.schemas.roles import RolCreate, RolUpdate
from typing import List, Optional

class RolService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def crearRol(self, rol_data: RolCreate) -> Roles:
        db_rol = Roles(
            nombre=rol_data.nombre,
            descripcion=rol_data.descripcion
        )
        self.session.add(db_rol)
        await self.session.commit()
        await self.session.refresh(db_rol)
        return db_rol
    
    async def obtenerRol_por_id(self, id: int) -> Optional[Roles]:
        result = await self.session.execute(select(Roles).where(Roles.id == id))
        return result.scalar_one_or_none()
    
    async def obtener_todosRoles(self) -> List[Roles]:
        result = await self.session.execute(select(Roles))
        return result.scalars().all()
    
    async def actualizarRol(self, rol_data: RolUpdate) -> Roles:
        result = await self.session.execute(select(Roles).where(Roles.id == rol_data.id))
        rol = result.scalar_one_or_none()
        if not rol:
            raise NotFoundException("Rol no encontrado")
        
        if rol_data.nombre is not None:
            rol.nombre = rol_data.nombre
        if rol_data.descripcion is not None:
            rol.descripcion = rol_data.descripcion
            
        self.session.add(rol)
        await self.session.commit()
        await self.session.refresh(rol)
        return rol
    
    async def eliminarRol(self, id: int) -> None:
        result = await self.session.execute(select(Roles).where(Roles.id == id))
        rol = result.scalar_one_or_none()
        if not rol:
            raise NotFoundException("Rol no encontrado")
        await self.session.delete(rol)
        await self.session.commit()