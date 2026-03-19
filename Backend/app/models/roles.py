from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship 
from .database import Base 

class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    estado = Column(Boolean, default=True)
    usuarios = relationship("Usuario", back_populates="rol")
    roles = relationship("Permisos", back_populates="roles")
