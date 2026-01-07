# app/schemas/tipos_vacunas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TipoVacunaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    edad_recomendada: Optional[str] = None
    dosis_requeridas: Optional[int] = None

class TipoVacunaCreate(TipoVacunaBase):
    id_usuario_creo: Optional[int] = None

class TipoVacunaUpdate(TipoVacunaBase):
    activo: Optional[bool] = None

class TipoVacunaResponse(TipoVacunaBase):
    id_vacuna: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True
