from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, Numeric, Float
from sqlalchemy.orm import relationship
from .database import Base


class DetalleFactura(Base):
    __tablename__ = "detalle_factura"
    id = Column(Integer, primary_key=True)
    descripcion = Column(String)
    cantidad = Column(Float)
    precio_unitario = Column(Numeric(12, 2))
    impuesto = Column(Numeric(12, 2))
    factura_id = Column(Integer, ForeignKey("facturas.id"))
    factura = relationship("Factura", back_populates="detalle")
