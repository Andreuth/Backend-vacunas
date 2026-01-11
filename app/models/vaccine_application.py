from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class VaccineApplication(Base):
    __tablename__ = "vaccine_applications"

    id = Column(Integer, primary_key=True, index=True)

    visit_id = Column(Integer, ForeignKey("visits.id", ondelete="CASCADE"), nullable=False, index=True)
    child_id = Column(Integer, ForeignKey("children.id", ondelete="RESTRICT"), nullable=False, index=True)

    schedule_id = Column(Integer, ForeignKey("vaccine_schedule.id", ondelete="RESTRICT"), nullable=False, index=True)

    fecha_aplicacion = Column(Date, nullable=False)
    lote = Column(String(50), nullable=True)
    proxima_fecha = Column(Date, nullable=True)

    activo = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("child_id", "schedule_id", name="uq_child_schedule_once"),
    )
