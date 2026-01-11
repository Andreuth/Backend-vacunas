from pydantic import BaseModel
from typing import Optional

class ScheduleFullOut(BaseModel):
    schedule_id: int
    vaccine_id: int
    vaccine_nombre: str
    vaccine_descripcion: Optional[str] = None
    dosis_numero: int
    edad_objetivo_meses: int
    intervalo_min_dias: Optional[int] = None

    class Config:
        from_attributes = True
