from pydantic import BaseModel
from datetime import date
from typing import Optional

class NextVaccineItem(BaseModel):
    vaccine_id: int
    vaccine_nombre: str
    schedule_id: int
    dosis_numero: int
    edad_objetivo_meses: int

    fecha_recomendada: date
    estado: str  # PENDIENTE | ATRASADA

    # si quieres mostrar por qué:
    dias_diferencia: int

class NextVaccinesResponse(BaseModel):
    child_id: int
    items: list[NextVaccineItem]
