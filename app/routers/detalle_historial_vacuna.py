# app/routers/detalle_historial_vacuna.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.detalle_historial_vacuna import (
    DetalleHistorialCreate,
    DetalleHistorialUpdate,
    DetalleHistorialResponse,
)
from ..services.detalle_historial_vacuna_service import (
    crear_detalle,
    listar_detalles,
    obtener_detalle,
    actualizar_detalle,
    desactivar_detalle,
)

from ..models.persona import Persona
from ..security.roles import require_roles

router = APIRouter(prefix="/detalle", tags=["Detalle Historial Vacuna"])

# ✅ Crear -> admin y medico
@router.post("/", response_model=DetalleHistorialResponse)
def crear_detalle_endpoint(
    data: DetalleHistorialCreate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    return crear_detalle(db, data)

# ✅ Listar -> admin y medico
@router.get("/", response_model=List[DetalleHistorialResponse])
def listar_detalles_endpoint(
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    return listar_detalles(db)

# ✅ Obtener -> admin y medico
@router.get("/{id_detalle}", response_model=DetalleHistorialResponse)
def obtener_detalle_endpoint(
    id_detalle: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    d = obtener_detalle(db, id_detalle)
    if not d:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return d

# ✅ Actualizar -> admin y medico
@router.put("/{id_detalle}", response_model=DetalleHistorialResponse)
def actualizar_detalle_endpoint(
    id_detalle: int,
    data: DetalleHistorialUpdate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    d = actualizar_detalle(db, id_detalle, data)
    if not d:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return d

# ✅ Eliminar -> admin y medico
@router.delete("/{id_detalle}")
def eliminar_detalle_endpoint(
    id_detalle: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    ok = desactivar_detalle(db, id_detalle)
    if not ok:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return {"detail": "Detalle desactivado correctamente"}
