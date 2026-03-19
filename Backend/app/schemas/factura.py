from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal

# Detalle de Factura
class DetalleFacturaBase(BaseModel):
    descripcion: str
    cantidad: float = 1.0
    precio_unitario: float = 0.0
    impuesto: float = 0.0

class DetalleFacturaCreate(DetalleFacturaBase):
    pass

class DetalleFacturaResponse(DetalleFacturaBase):
    id: int
    factura_id: int
    
    class Config:
        from_attributes = True

# Factura
class FacturaBase(BaseModel):
    archivo: Optional[str] = None
    facturador: Optional[str] = None
    factura_numero: str
    factura_fecha: date
    factura_monto: float = 0.0
    factura_moneda: str = "COP"
    factura_impuestos: float = 0.0
    factura_metodoextraccion: Optional[str] = None
    factura_textocrudo: Optional[str] = None
    factura_status: str = "pendiente"

class FacturaCreate(FacturaBase):
    items: List[DetalleFacturaCreate] = []

class FacturaUpdate(BaseModel):
    archivo: Optional[str] = None
    facturador: Optional[str] = None
    factura_numero: Optional[str] = None
    factura_fecha: Optional[date] = None
    factura_monto: Optional[int] = None
    factura_status: Optional[str] = None
    factura_estado: Optional[bool] = None

class FacturaResponse(FacturaBase):
    id: int
    factura_fcreacion: datetime
    factura_estado: bool
    usuario_id: Optional[int]
    detalle: List[DetalleFacturaResponse] = []

    class Config:
        from_attributes = True
