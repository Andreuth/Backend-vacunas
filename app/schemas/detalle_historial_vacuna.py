# app/schemas/detalle_historial_vacuna.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class DetalleHistorialBase(BaseModel):
    id_historial: int
    id_vacuna: int
    lote: Optional[str] = None
    dosis_numero: Optional[int] = None
    fecha_proxima: Optional[date] = None

class DetalleHistorialCreate(DetalleHistorialBase):
    id_usuario_creo: Optional[int] = None

class DetalleHistorialUpdate(DetalleHistorialBase):
    activo: Optional[bool] = None

class DetalleHistorialResponse(DetalleHistorialBase):
    id_detalle: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True
