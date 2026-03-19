import asyncio
from app.models.database import Base
from app.db.base import engine
from app.models.usuario import Usuario
from app.models.roles import Roles
from app.models.permisos import Permisos
from app.models.factura import Factura
from app.models.detalle_factura import DetalleFactura
from app.models.refresh_tokens import RefreshTokens


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas exitosamente")


if __name__ == "__main__":
    asyncio.run(create_tables())
