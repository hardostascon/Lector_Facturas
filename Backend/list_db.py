import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, desc
from app.models.factura import Factura
from app.core.config import settings

async def show_crudo():
    engine = create_async_engine(settings.DATABASE_URL, future=True)
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with Session() as session:
        result = await session.execute(select(Factura).order_by(desc(Factura.id)).limit(1))
        f = result.scalar_one_or_none()
        if f:
            print(f.factura_textocrudo)

if __name__ == "__main__":
    asyncio.run(show_crudo())
