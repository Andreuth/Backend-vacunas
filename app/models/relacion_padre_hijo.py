from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from ..database import Base

class RelacionPadreHijo(Base):
    __tablename__ = "relacion_padre_hijo"

    id_relacion = Column(Integer, primary_key=True, index=True)
    id_padre = Column(Integer, ForeignKey("personas.id_persona"), nullable=False)
    id_hijo = Column(Integer, ForeignKey("personas.id_persona"), nullable=False)
    tipo_relacion = Column(String(50))  # padre, madre, tutor, etc.

    id_usuario_creo = Column(Integer)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    activo = Column(Boolean, default=True)
