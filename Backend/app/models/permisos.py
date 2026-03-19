from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship 
from .database import Base 

class Permisos(Base):
    __tablename__ = "permisos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    acciones = Column(String)
    estado = Column(Boolean, default=True)
    rol_id = Column(Integer, ForeignKey("roles.id"))
    roles = relationship("Roles", back_populates="roles")
    