from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio_basico = Column(Numeric(10, 2), nullable=True)
    precio_estandar = Column(Numeric(10, 2), nullable=True)
    precio_premium = Column(Numeric(10, 2), nullable=True)
    tiempo_entrega = Column(Integer, nullable=True)  # days
    imagenes = Column(ARRAY(String), nullable=True)
    categoria_id = Column(Integer, nullable=True)  # no FK — categories table doesn't exist yet
    estado = Column(String(20), nullable=False, default="activo")  # 'activo' | 'inactivo'
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    freelancer = relationship("User", back_populates="services")
