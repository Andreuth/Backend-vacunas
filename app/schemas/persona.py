<<<<<<< HEAD
from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime

# Roles válidos según tu diseño
RolPersona = Literal["admin", "medico", "padre", "hijo"]


class PersonaBase(BaseModel):
    nombres: str
    apellidos: str
    numero_documento: str
    rol: RolPersona


class PersonaCreate(PersonaBase):
    # ✅ ahora es opcional para permitir HIJO sin password
    password: Optional[str] = None


class PersonaUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    numero_documento: Optional[str] = None
    rol: Optional[RolPersona] = None
    activo: Optional[bool] = None

    # ✅ si quieres permitir cambiar password desde update
    password: Optional[str] = None


class PersonaResponse(PersonaBase):
    model_config = ConfigDict(from_attributes=True)  # ✅ Pydantic v2

    id_persona: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    # ✅ auditoría (si tu tabla tiene estos campos)
    id_usuario_creo: Optional[int] = None
=======
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
>>>>>>> 39b6a8b2c70a058d7af1d83a226d239ece197f4c
