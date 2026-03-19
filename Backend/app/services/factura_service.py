from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.factura import Factura
from app.models.detalle_factura import DetalleFactura
from app.schemas.factura import FacturaCreate, FacturaUpdate
from app.core.exceptions import UnauthorizedException
from typing import List, Optional

class FacturaService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def crearFactura(self, factura_data: FacturaCreate, usuario_id: int) -> Factura:
        db_factura = Factura(
            archivo=factura_data.archivo,
            facturador=factura_data.facturador,
            factura_numero=factura_data.factura_numero,
            factura_fecha=factura_data.factura_fecha,
            factura_monto=factura_data.factura_monto,
            factura_moneda=factura_data.factura_moneda,
            factura_impuestos=factura_data.factura_impuestos,
            factura_metodoextraccion=factura_data.factura_metodoextraccion,
            factura_textocrudo=factura_data.factura_textocrudo,
            factura_status=factura_data.factura_status,
            usuario_id=usuario_id
        )
        self.session.add(db_factura)
        
        # Guardar los ítems del detalle si existen
        if factura_data.items:
            # Necesitamos el ID de la factura, flush lo genera sin terminar la transacción
            await self.session.flush()
            for item in factura_data.items:
                if item.precio_unitario == 0:
                    continue
                db_item = DetalleFactura(
                    descripcion=item.descripcion,
                    cantidad=item.cantidad,
                    precio_unitario=item.precio_unitario,
                    impuesto=item.impuesto,
                    factura_id=db_factura.id
                )
                self.session.add(db_item)

        await self.session.commit()
        await self.session.refresh(db_factura)
        
        # Recargar con el detalle para la respuesta
        result = await self.session.execute(
            select(Factura).where(Factura.id == db_factura.id).options(selectinload(Factura.detalle))
        )
        return result.scalar_one()
    
    async def obtenerFactura_por_id(self, id: int) -> Optional[Factura]:
        result = await self.session.execute(
            select(Factura).where(Factura.id == id).options(selectinload(Factura.detalle))
        )
        return result.scalar_one_or_none()
    
    async def obtener_todasFacturas(self, skip: int = 0, limit: int = 100, search: str = None) -> List[Factura]:
        query = select(Factura).options(selectinload(Factura.detalle))
        
        if search:
            search_str = f"%{search}%"
            query = query.where(
                (Factura.facturador.ilike(search_str)) | 
                (Factura.factura_numero.ilike(search_str))
            )
            
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def obtener_facturas_por_usuario(self, usuario_id: int, skip: int = 0, limit: int = 100, search: str = None) -> List[Factura]:
        query = select(Factura).where(Factura.usuario_id == usuario_id).options(selectinload(Factura.detalle))
        
        if search:
            search_str = f"%{search}%"
            query = query.where(
                (Factura.facturador.ilike(search_str)) | 
                (Factura.factura_numero.ilike(search_str))
            )
            
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def actualizarFactura(self, id: int, factura_data: FacturaUpdate) -> Factura:
        factura = await self.obtenerFactura_por_id(id)
        if not factura:
            return None
        
        # Actualizar solo los campos enviados
        update_data = factura_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(factura, key, value)
            
        self.session.add(factura)
        await self.session.commit()
        await self.session.refresh(factura)
        
        # Volver a cargar la factura con su detalle para evitar error 'MissingGreenlet'
        return await self.obtenerFactura_por_id(factura.id)
    
    async def eliminarFactura(self, id: int) -> bool:
        factura = await self.obtenerFactura_por_id(id)
        if not factura:
            return False
        await self.session.delete(factura)
        await self.session.commit()
        return True