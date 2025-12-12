# app/routers/centro_salud.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.centro_salud import (
    CentroSaludCreate,
    CentroSaludUpdate,
    CentroSaludResponse,
)
from ..services.centro_salud_service import (
    crear_centro,
    listar_centros,
    obtener_centro,
    actualizar_centro,
    desactivar_centro,
)
from ..security.jwt import get_current_user
from ..models.persona import Persona

router = APIRouter(prefix="/centros", tags=["Centros de Salud"])

@router.post("/", response_model=CentroSaludResponse)
def crear_centro_endpoint(
    data: CentroSaludCreate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    return crear_centro(db, data)

@router.get("/", response_model=List[CentroSaludResponse])
def listar_centros_endpoint(
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    return listar_centros(db)

@router.get("/{id_centro}", response_model=CentroSaludResponse)
def obtener_centro_endpoint(
    id_centro: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    centro = obtener_centro(db, id_centro)
    if not centro:
        raise HTTPException(status_code=404, detail="Centro no encontrado")
    return centro

@router.put("/{id_centro}", response_model=CentroSaludResponse)
def actualizar_centro_endpoint(
    id_centro: int,
    data: CentroSaludUpdate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    centro = actualizar_centro(db, id_centro, data)
    if not centro:
        raise HTTPException(status_code=404, detail="Centro no encontrado")
    return centro

@router.delete("/{id_centro}")
def eliminar_centro_endpoint(
    id_centro: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    ok = desactivar_centro(db, id_centro)
    if not ok:
        raise HTTPException(status_code=404, detail="Centro no encontrado")
    return {"detail": "Centro desactivado correctamente"}
