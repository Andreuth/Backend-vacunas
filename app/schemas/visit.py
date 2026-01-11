from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

class VisitCreate(BaseModel):
    child_id: int
    fecha_atencion: date
    peso_kg: float = Field(..., gt=0)
    talla_cm: float = Field(..., gt=0)
    observaciones: Optional[str] = Field(None, max_length=500)

class VisitOut(BaseModel):
    id: int
    child_id: int
    pediatrician_id: int
    fecha_atencion: date
    peso_kg: float
    talla_cm: float
    observaciones: Optional[str] = None
    activo: bool

    class Config:
        from_attributes = True

class VaccineApplicationCreate(BaseModel):
    schedule_id: int
    fecha_aplicacion: date
    lote: Optional[str] = Field(None, max_length=50)
    proxima_fecha: Optional[date] = None

class VaccineApplicationOut(BaseModel):
    id: int
    visit_id: int
    child_id: int
    schedule_id: int
    fecha_aplicacion: date
    lote: Optional[str] = None
    proxima_fecha: Optional[date] = None
    activo: bool

    class Config:
        from_attributes = True

# Para historial (representante)
class HistoryItem(BaseModel):
    visit: VisitOut
    applications: List[VaccineApplicationOut]
