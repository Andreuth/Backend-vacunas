from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.persona import (
    PersonaCreate,
    PersonaResponse,
    PersonaUpdate
)
from ..services.persona_service import (
    crear_persona,
    listar_personas,
    obtener_persona,
    actualizar_persona,
    desactivar_persona
)
from ..security.jwt import get_current_user
from ..models.persona import Persona

router = APIRouter(prefix="/personas", tags=["Personas"])

# Registro de nueva persona (usuario)
@router.post("/", response_model=PersonaResponse)
def crear_persona_endpoint(
    data: PersonaCreate,
    db: Session = Depends(get_db),
):
    persona = crear_persona(db, data)
    return persona

# Ruta protegida: requiere token
@router.get("/", response_model=List[PersonaResponse])
def listar_personas_endpoint(
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user)
):
    return listar_personas(db)

@router.get("/{id_persona}", response_model=PersonaResponse)
def obtener_persona_endpoint(
    id_persona: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user)
):
    persona = obtener_persona(db, id_persona)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@router.put("/{id_persona}", response_model=PersonaResponse)
def actualizar_persona_endpoint(
    id_persona: int,
    data: PersonaUpdate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user)
):
    persona = actualizar_persona(db, id_persona, data)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@router.delete("/{id_persona}")
def eliminar_persona_endpoint(
    id_persona: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user)
):
    ok = desactivar_persona(db, id_persona)
    if not ok:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return {"detail": "Persona desactivada correctamente"}
