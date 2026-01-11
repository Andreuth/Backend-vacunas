from pydantic import BaseModel, Field
from typing import Optional

class VaccineCreate(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: Optional[str] = Field(None, max_length=300)

class VaccineOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    activo: bool

    class Config:
        from_attributes = True

class ScheduleCreate(BaseModel):
    vaccine_id: int
    dosis_numero: int = Field(..., ge=1)
    edad_objetivo_meses: int = Field(..., ge=0)
    intervalo_min_dias: Optional[int] = Field(None, ge=0)

class ScheduleOut(BaseModel):
    id: int
    vaccine_id: int
    dosis_numero: int
    edad_objetivo_meses: int
    intervalo_min_dias: Optional[int] = None
    activo: bool

    class Config:
        from_attributes = True
