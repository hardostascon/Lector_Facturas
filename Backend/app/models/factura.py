from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, Text, DateTime, func, Numeric
from sqlalchemy.orm import relationship 
from .database import Base 

class Factura(Base):
    __tablename__ = "facturas"
    id = Column(Integer, primary_key=True, index=True)
    archivo = Column(String, index=True)
    facturador = Column(String, index=True)
    factura_numero = Column(String, index=True)
    factura_fecha = Column(Date)
    factura_monto = Column(Numeric(12, 2))
    factura_moneda = Column(String, index=True)
    factura_impuestos = Column(Numeric(12, 2))
    factura_metodoextraccion = Column(String, index=True) 
    factura_textocrudo = Column(Text)
    factura_status = Column(String, index=True)
    factura_fcreacion = Column(DateTime, default=func.now())
    factura_estado = Column(Boolean, default=True)
    
    # Suponiendo que existe un usuario_id para la restricción
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    
    detalle = relationship("DetalleFactura", back_populates="factura")