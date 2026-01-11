from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)

    child_id = Column(Integer, ForeignKey("children.id", ondelete="RESTRICT"), nullable=False, index=True)
    pediatrician_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)

    fecha_atencion = Column(Date, nullable=False)

    peso_kg = Column(Float, nullable=False)
    talla_cm = Column(Float, nullable=False)

    observaciones = Column(String(500), nullable=True)

    activo = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now(), nullable=False)
