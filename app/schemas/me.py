from pydantic import BaseModel

class MeOut(BaseModel):
    id: int
    nombres: str
    apellidos: str
    numero_documento: str
    rol: str

    class Config:
        from_attributes = True
