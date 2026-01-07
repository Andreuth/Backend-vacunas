# app/routers/centro_salud.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.centro_salud import CentroSaludCreate, CentroSaludUpdate, CentroSaludResponse
from ..services.centro_salud_service import (
    crear_centro,
    listar_centros,
    obtener_centro,
    actualizar_centro,
    desactivar_centro,
)

from ..models.persona import Persona
from ..security.roles import require_roles

router = APIRouter(prefix="/centros", tags=["Centros de Salud"])

# ✅ Crear -> SOLO admin
@router.post("/", response_model=CentroSaludResponse)
def crear_centro_endpoint(
    data: CentroSaludCreate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin"])),
):
    return crear_centro(db, data,current_user)

# ✅ Listar -> admin, medico, padre
@router.get("/", response_model=List[CentroSaludResponse])
def listar_centros_endpoint(
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico", "padre"])),
):
    return listar_centros(db)

# ✅ Obtener -> admin, medico, padre
@router.get("/{id_centro}", response_model=CentroSaludResponse)
def obtener_centro_endpoint(
    id_centro: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico", "padre"])),
):
    centro = obtener_centro(db, id_centro)
    if not centro:
        raise HTTPException(status_code=404, detail="Centro no encontrado")
    return centro

# ✅ Actualizar -> SOLO admin
@router.put("/{id_centro}", response_model=CentroSaludResponse)
def actualizar_centro_endpoint(
    id_centro: int,
    data: CentroSaludUpdate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin"])),
):
    centro = actualizar_centro(db, id_centro, data,current_user)
    if not centro:
        raise HTTPException(status_code=404, detail="Centro no encontrado")
    return centro

# ✅ Eliminar -> SOLO admin
@router.delete("/{id_centro}")
def eliminar_centro_endpoint(
    id_centro: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin"])),
):
    ok = desactivar_centro(db, id_centro)
    if not ok:
        raise HTTPException(status_code=404, detail="Centro no encontrado")
    return {"detail": "Centro desactivado correctamente"}
