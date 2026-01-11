from pydantic import BaseModel, Field
from datetime import date

class RepresentativeInput(BaseModel):
    nombres: str = Field(..., max_length=100)
    apellidos: str = Field(..., max_length=100)
    numero_documento: str = Field(..., max_length=20)
    password: str = Field(..., min_length=6, max_length=100)

class ChildInput(BaseModel):
    nombres: str = Field(..., max_length=100)
    apellidos: str = Field(..., max_length=100)
    numero_documento: str = Field(..., max_length=20)
    fecha_nacimiento: date
    sexo: str = Field(..., max_length=10)  # "M" / "F" / "OTRO"

class RegisterChildRequest(BaseModel):
    representante: RepresentativeInput
    nino: ChildInput
    parentesco: str = Field(..., max_length=30)  # madre/padre/tutor
    es_principal: bool = True

class RegisterChildResponse(BaseModel):
    representante_id: int
    nino_id: int
    relacion_id: int
