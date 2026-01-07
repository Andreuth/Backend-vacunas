# app/routers/personas.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.persona import PersonaCreate, PersonaResponse, PersonaUpdate
from ..services.persona_service import (
    crear_persona,
    listar_personas,
    obtener_persona,
    actualizar_persona,
    desactivar_persona,
)

from ..models.persona import Persona
from ..security.roles import require_roles

router = APIRouter(prefix="/personas", tags=["Personas"])


# ✅ Crear persona -> admin y medico (con reglas dentro del service)
@router.post("/", response_model=PersonaResponse)
def crear_persona_endpoint(
    data: PersonaCreate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    return crear_persona(db, data, current_user)


# ✅ Listar -> admin y medico
@router.get("/", response_model=List[PersonaResponse])
def listar_personas_endpoint(
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    return listar_personas(db,current_user)



# ✅ Obtener -> admin y medico
@router.get("/{id_persona}", response_model=PersonaResponse)
def obtener_persona_endpoint(
    id_persona: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    persona = obtener_persona(db, id_persona, current_user)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona


# ✅ Actualizar -> admin y medico (con reglas: medico no puede poner rol admin/medico)
@router.put("/{id_persona}", response_model=PersonaResponse)
def actualizar_persona_endpoint(
    id_persona: int,
    data: PersonaUpdate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    persona = actualizar_persona(db, id_persona, data, current_user)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona


# ✅ Eliminar -> admin y medico (si quieres que medico también pueda desactivar)
@router.delete("/{id_persona}")
def eliminar_persona_endpoint(
    id_persona: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    ok = desactivar_persona(db, id_persona ,current_user)
    if not ok:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return {"detail": "Persona desactivada correctamente"}
