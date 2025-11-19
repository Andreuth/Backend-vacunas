from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from ..database import Base

class CentroSalud(Base):
    __tablename__ = "centro_salud"

    id_centro = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200))
    telefono = Column(String(20))
    responsable = Column(String(100))
    nivel = Column(String(50))
    horario_atencion = Column(String(100))
    correo = Column(String(100))
    ciudad = Column(String(100))
    provincia = Column(String(100))
    id_usuario_creo = Column(Integer)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    activo = Column(Boolean, default=True)
