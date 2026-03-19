import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import AsyncSessionLocal
from app.models.roles import Roles
from app.models.usuario import Usuario
from app.core.security import hash_password

async def crear_primer_admin():
    async with AsyncSessionLocal() as session:
        # Crear los roles básicos si no existen
        roles_basicos = ["admin", "contador", "usuario"]
        roles_ids = {}

        for rol_nombre in roles_basicos:
            # Buscar el rol
            query_rol = await session.execute(select(Roles).where(Roles.nombre == rol_nombre))
            rol_existente = query_rol.scalar_one_or_none()
            
            if not rol_existente:
                print(f"Creando rol '{rol_nombre}'...")
                nuevo_rol = Roles(nombre=rol_nombre, estado=True)
                session.add(nuevo_rol)
                await session.flush()
                roles_ids[rol_nombre] = nuevo_rol.id
            else:
                roles_ids[rol_nombre] = rol_existente.id

        # Crear un usuario administrador inicial
        email_admin = "admin@admin.com"
        query_usuario = await session.execute(select(Usuario).where(Usuario.email == email_admin))
        usuario_existente = query_usuario.scalar_one_or_none()

        if not usuario_existente:
            print("Creando el primer usuario administrador...")
            nuevo_admin = Usuario(
                nombre="Administrador",
                apellido="Principal",
                email=email_admin,
                contraseña=hash_password("admin"),
                rol_id=roles_ids["admin"],
            )
            session.add(nuevo_admin)
            await session.commit()
            print("\n¡Usuario administrador creado con éxito!")
            print("Email: admin@admin.com")
            print("Contraseña: admin")
            print("Usar estas credenciales en el endpoint POST /api/v1/auth/login")
        else:
            print(f"\nEl usuario {email_admin} ya existe en la base de datos.")

if __name__ == "__main__":
    asyncio.run(crear_primer_admin())
