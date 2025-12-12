# app/schemas/centro_salud.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CentroSaludBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    responsable: Optional[str] = None
    nivel: Optional[str] = None
    horario_atencion: Optional[str] = None
    correo: Optional[str] = None
    ciudad: Optional[str] = None
    provincia: Optional[str] = None

class CentroSaludCreate(CentroSaludBase):
    id_usuario_creo: Optional[int] = None

class CentroSaludUpdate(CentroSaludBase):
    activo: Optional[bool] = None

class CentroSaludResponse(CentroSaludBase):
    id_centro: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True
