from pydantic import BaseModel
from datetime import date

class ChildOut(BaseModel):
    id: int
    nombres: str
    apellidos: str
    numero_documento: str
    fecha_nacimiento: date
    sexo: str
    activo: bool

    class Config:
        from_attributes = True
