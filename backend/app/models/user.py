from sqlalchemy import ARRAY, Boolean, Column, DateTime, Integer, Numeric, String, Text
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False)  # 'freelancer' | 'client' | 'admin'
    carrera = Column(String(100), nullable=True)
    semestre = Column(Integer, nullable=True)
    empresa = Column(String(150), nullable=True)  # solo clientes externos
    avatar_url = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    habilidades = Column(ARRAY(String), nullable=True)
    wallet_balance = Column(Numeric(12, 2), default=0)
    verificado = Column(Boolean, default=False)
    verification_token = Column(String(255), nullable=True)
    verification_token_expires = Column(DateTime(timezone=True), nullable=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
