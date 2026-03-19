import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.models.factura import Factura
from app.core.config import settings

async def list_all():
    engine = create_async_engine(settings.DATABASE_URL, future=True)
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with Session() as session:
        result = await session.execute(select(Factura).order_by(Factura.id.desc()).limit(10))
        facturas = result.scalars().all()
        for f in facturas:
            print(f"--- ID: {f.id} ---")
            print(f"Número: {f.factura_numero}")
            print(f"Texto Crudo: {f.factura_textocrudo}")
            print("-" * 20)

if __name__ == "__main__":
    asyncio.run(list_all())
