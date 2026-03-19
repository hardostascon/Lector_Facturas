from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship 
from .database import Base 

class RefreshTokens(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    expiracion = Column(Date)
    estado = Column(Boolean, default=True)
    
