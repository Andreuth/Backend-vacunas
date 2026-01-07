<<<<<<< HEAD
# app/schemas/historial_vacunacion.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class HistorialVacunacionBase(BaseModel):
    id_persona: int
    id_centro: int
    id_cargo: int
    fecha_aplicacion: date
    observaciones: Optional[str] = None

class HistorialVacunacionCreate(HistorialVacunacionBase):
    id_usuario_creo: Optional[int] = None

class HistorialVacunacionUpdate(HistorialVacunacionBase):
    activo: Optional[bool] = None

class HistorialVacunacionResponse(HistorialVacunacionBase):
    id_historial: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True
=======
# app/schemas/historial_vacunacion.py
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class HistorialVacunacionBase(BaseModel):
    id_persona: int
    id_centro: int
    id_cargo: int
    fecha_aplicacion: date
    observaciones: Optional[str] = None

class HistorialVacunacionCreate(HistorialVacunacionBase):
    id_usuario_creo: Optional[int] = None

class HistorialVacunacionUpdate(HistorialVacunacionBase):
    activo: Optional[bool] = None

class HistorialVacunacionResponse(HistorialVacunacionBase):
    id_historial: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True
>>>>>>> 39b6a8b2c70a058d7af1d83a226d239ece197f4c
