from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)

    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)

    numero_documento = Column(String(20), nullable=False, unique=True, index=True)

    fecha_nacimiento = Column(Date, nullable=False)
    sexo = Column(String(10), nullable=False)  # M/F/OTRO (lo controlamos a nivel API)

    activo = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now(), nullable=False)
