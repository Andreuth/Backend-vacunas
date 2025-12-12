# app/routers/cargos_medicos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.cargos_medicos import (
    CargoMedicoCreate,
    CargoMedicoUpdate,
    CargoMedicoResponse,
)
from ..services.cargos_medicos_service import (
    crear_cargo,
    listar_cargos,
    obtener_cargo,
    actualizar_cargo,
    desactivar_cargo,
)
from ..security.jwt import get_current_user
from ..models.persona import Persona

router = APIRouter(prefix="/cargos", tags=["Cargos Médicos"])

@router.post("/", response_model=CargoMedicoResponse)
def crear_cargo_endpoint(
    data: CargoMedicoCreate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    return crear_cargo(db, data)

@router.get("/", response_model=List[CargoMedicoResponse])
def listar_cargos_endpoint(
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    return listar_cargos(db)

@router.get("/{id_cargo}", response_model=CargoMedicoResponse)
def obtener_cargo_endpoint(
    id_cargo: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    cargo = obtener_cargo(db, id_cargo)
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    return cargo

@router.put("/{id_cargo}", response_model=CargoMedicoResponse)
def actualizar_cargo_endpoint(
    id_cargo: int,
    data: CargoMedicoUpdate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    cargo = actualizar_cargo(db, id_cargo, data)
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    return cargo

@router.delete("/{id_cargo}")
def eliminar_cargo_endpoint(
    id_cargo: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    ok = desactivar_cargo(db, id_cargo)
    if not ok:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    return {"detail": "Cargo desactivado correctamente"}
