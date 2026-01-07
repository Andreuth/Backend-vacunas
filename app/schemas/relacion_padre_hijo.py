<<<<<<< HEAD
# app/schemas/relacion_padre_hijo.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RelacionBase(BaseModel):
    id_padre: int
    id_hijo: int
    tipo_relacion: Optional[str] = None  # padre, madre, tutor...

class RelacionCreate(RelacionBase):
    id_usuario_creo: Optional[int] = None

class RelacionUpdate(RelacionBase):
    activo: Optional[bool] = None

class RelacionResponse(RelacionBase):
    id_relacion: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True
=======
# app/schemas/relacion_padre_hijo.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RelacionBase(BaseModel):
    id_padre: int
    id_hijo: int
    tipo_relacion: Optional[str] = None  # padre, madre, tutor...

class RelacionCreate(RelacionBase):
    id_usuario_creo: Optional[int] = None

class RelacionUpdate(RelacionBase):
    activo: Optional[bool] = None

class RelacionResponse(RelacionBase):
    id_relacion: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True
>>>>>>> 39b6a8b2c70a058d7af1d83a226d239ece197f4c
