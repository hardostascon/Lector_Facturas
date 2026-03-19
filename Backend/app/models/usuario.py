from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship 
from .database import Base 
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    contraseña = Column(String)
    fecha_nacimiento = Column(Date)
    genero = Column(String)
    telefono = Column(String)
    direccion = Column(String)
    codigo_postal = Column(String)
    ciudad = Column(String)
    provincia = Column(String)
    rol_id = Column(Integer, ForeignKey("roles.id"))
    pais = Column(String)
    fecha_creacion = Column(Date)
    fecha_actualizacion = Column(Date)

    # Relación hacia el rol — permite acceder a usuario.rol.nombre
    rol = relationship("Roles", back_populates="usuarios")

