from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from datetime import datetime
from ..database import Base

class DetalleHistorialVacuna(Base):
    __tablename__ = "detalle_historial_vacuna"

    id_detalle = Column(Integer, primary_key=True, index=True)
    id_historial = Column(Integer, ForeignKey("historial_vacunacion.id_historial"), nullable=False)
    id_vacuna = Column(Integer, ForeignKey("tipos_vacunas.id_vacuna"), nullable=False)

    lote = Column(String(50))
    dosis_numero = Column(Integer)
    fecha_proxima = Column(Date)

    id_usuario_creo = Column(Integer)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    activo = Column(Boolean, default=True)
