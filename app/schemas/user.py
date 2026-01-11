from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    nombres: str = Field(..., max_length=100)
    apellidos: str = Field(..., max_length=100)
    numero_documento: str = Field(..., max_length=20)
    rol: str = Field(..., max_length=20)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)

class UserCreateRepresentative(BaseModel):
    nombres: str = Field(..., max_length=100)
    apellidos: str = Field(..., max_length=100)
    numero_documento: str = Field(..., max_length=20)
    password: str = Field(..., min_length=6, max_length=100)

class UserOut(BaseModel):
    id: int
    nombres: str
    apellidos: str
    numero_documento: str
    rol: str
    activo: bool
    created_by: Optional[int] = None

    class Config:
        from_attributes = True
