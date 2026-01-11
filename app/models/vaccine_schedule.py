from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class VaccineSchedule(Base):
    __tablename__ = "vaccine_schedule"

    id = Column(Integer, primary_key=True, index=True)

    vaccine_id = Column(Integer, ForeignKey("vaccines.id", ondelete="CASCADE"), nullable=False, index=True)
    dosis_numero = Column(Integer, nullable=False)              # 1..N
    edad_objetivo_meses = Column(Integer, nullable=False)       # edad recomendada en meses
    intervalo_min_dias = Column(Integer, nullable=True)         # opcional

    activo = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=False), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("vaccine_id", "dosis_numero", name="uq_vaccine_dose"),
    )
