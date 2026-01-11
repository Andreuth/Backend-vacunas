from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from app.schemas.visit import VisitOut

class AppliedVaccineFull(BaseModel):
    application_id: int
    fecha_aplicacion: date
    lote: Optional[str] = None
    proxima_fecha: Optional[date] = None

    schedule_id: int
    dosis_numero: int
    edad_objetivo_meses: int

    vaccine_id: int
    vaccine_nombre: str
    vaccine_descripcion: Optional[str] = None

class HistoryFullItem(BaseModel):
    visit: VisitOut
    applications: List[AppliedVaccineFull]
