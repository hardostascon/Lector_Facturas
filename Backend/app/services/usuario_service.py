from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, aliased, contains_eager
from app.models.usuario import Usuario
from app.models.roles import Roles
from app.core.security import verify_password, hash_password
from app.core.exceptions import UnauthorizedException
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from typing import Optional, List
from sqlalchemy import func


class UsuarioService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def autenticar(self, email: str, password: str) -> Optional[Usuario]:
        # Usamos selectinload para cargar el rol junto con el usuario en una sola consulta asíncrona
        result = await self.session.execute(
            select(Usuario)
            .where(Usuario.email == email)
            .options(selectinload(Usuario.rol))
        )
        usuario = result.scalar_one_or_none()
        
        # En tu modelo el campo se llama 'contraseña', no 'password'
        if not usuario or not verify_password(password, usuario.contraseña):
            return None
            
        return usuario
    
    async def crearUsuario(self, user_data: UsuarioCreate) -> Usuario:
        
        db_usuario = Usuario(
            nombre=user_data.nombre,
            apellido=user_data.apellido,
            email=user_data.email,
            fecha_nacimiento=user_data.fecha_nacimiento,
            genero=user_data.genero,
            telefono=user_data.telefono,
            direccion=user_data.direccion,
            codigo_postal=user_data.codigo_postal,
            ciudad=user_data.ciudad,
            provincia=user_data.provincia,
            pais=user_data.pais,
            rol_id=user_data.rol_id,
            fecha_creacion=func.now(),
            fecha_actualizacion=func.now(),
            contraseña=hash_password(user_data.password)
        )
        self.session.add(db_usuario)
        await self.session.commit()
        await self.session.refresh(db_usuario)
        return db_usuario
    
    async def actualizarUsuario(self, id: int, user_data: UsuarioUpdate) -> Optional[Usuario]:
        result = await self.session.execute(
            select(Usuario).where(Usuario.id == id).options(selectinload(Usuario.rol))
        )
        usuario = result.scalar_one_or_none()
        if not usuario:
            return None
        # Convertimos a dict excluyendo los campos que no se enviaron
        update_data = user_data.model_dump(exclude_unset=True)
        
        for campo, valor in update_data.items():
            if campo == "password":
                setattr(usuario, "contraseña", hash_password(valor))
            else:
                setattr(usuario, campo, valor)
                
        # Actualizamos la fecha de modificación automáticamente
        usuario.fecha_actualizacion = func.now()
        
        await self.session.commit()
        await self.session.refresh(usuario)
        return usuario
    
    async def eliminarUsuario(self, id: int) -> bool:
        result = await self.session.execute(
            select(Usuario).where(Usuario.id == id).options(selectinload(Usuario.rol))
        )
        usuario = result.scalar_one_or_none()
        if not usuario:
            return False
        
        try:
            await self.session.delete(usuario)
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            print(f"Error al eliminar usuario: {e}")
            return False

    async def obtenerUsuario_por_id(self, id: int) -> Optional[Usuario]:
        # Creamos un alias 'rol' para la tabla Roles para mayor claridad y evitar el conflicto de llaves 'id'
        rol_alias = aliased(Roles, name="rol")
        
        result = await self.session.execute(
            select(Usuario)
            .join(rol_alias, Usuario.rol_id == rol_alias.id)
            .where(Usuario.id == id)
            .options(contains_eager(Usuario.rol, alias=rol_alias))
        )
        return result.scalar_one_or_none()
    
    async def obtener_usuarios_por_usuario(self, usuario_id: int) -> List[Usuario]:
        # Creamos el alias para roles para el join
        rol_alias = aliased(Roles, name="rol")
        
        result = await self.session.execute(
            select(Usuario)
            .join(rol_alias, Usuario.rol_id == rol_alias.id)
            .where(Usuario.id == usuario_id)
            .options(contains_eager(Usuario.rol, alias=rol_alias))
        )
        return result.scalars().all()
    
    async def obtener_todosUsuarios(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        rol_id: int = None, 
        search: str = None
    ) -> List[Usuario]:
        query = select(Usuario).options(selectinload(Usuario.rol))
        
        if rol_id:
            query = query.where(Usuario.rol_id == rol_id)
            
        if search:
            search_str = f"%{search}%"
            query = query.where(
                (Usuario.nombre.ilike(search_str)) | 
                (Usuario.apellido.ilike(search_str)) | 
                (Usuario.email.ilike(search_str))
            )
            
        query = query.offset(skip).limit(limit)
        
        result = await self.session.execute(query)
        return result.scalars().all()