from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PersonaBase(BaseModel):
    nombres: str
    apellidos: str
    numero_documento: str
    rol: Optional[str] = "usuario"

class PersonaCreate(PersonaBase):
    password: str  # contraseña en texto plano (solo para crear)

class PersonaUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None

class PersonaResponse(PersonaBase):
    id_persona: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True
