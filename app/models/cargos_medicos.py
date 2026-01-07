from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from ..database import Base

class CargoMedico(Base):
    __tablename__ = "cargos_medicos"

    id_cargo = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(300))
    id_usuario_creo = Column(Integer)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    activo = Column(Boolean, default=True)
