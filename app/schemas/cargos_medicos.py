# app/schemas/cargos_medicos.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CargoMedicoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CargoMedicoCreate(CargoMedicoBase):
    id_usuario_creo: Optional[int] = None

class CargoMedicoUpdate(CargoMedicoBase):
    activo: Optional[bool] = None

class CargoMedicoResponse(CargoMedicoBase):
    id_cargo: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True
