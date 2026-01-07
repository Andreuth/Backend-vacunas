from sqlalchemy import Column, Integer, Date, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from ..database import Base

class HistorialVacunacion(Base):
    __tablename__ = "historial_vacunacion"

    id_historial = Column(Integer, primary_key=True, index=True)
    id_persona = Column(Integer, ForeignKey("personas.id_persona"), nullable=False)
    id_centro = Column(Integer, ForeignKey("centro_salud.id_centro"), nullable=False)
    id_cargo = Column(Integer, ForeignKey("cargos_medicos.id_cargo"), nullable=False)

    fecha_aplicacion = Column(Date, nullable=False)
    observaciones = Column(String(500))

    id_usuario_creo = Column(Integer)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    activo = Column(Boolean, default=True)
