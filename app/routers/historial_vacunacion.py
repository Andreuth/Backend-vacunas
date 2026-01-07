<<<<<<< HEAD
# app/routers/historial_vacunacion.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.historial_vacunacion import (
    HistorialVacunacionCreate,
    HistorialVacunacionUpdate,
    HistorialVacunacionResponse,
)
from ..services.historial_vacunacion_service import (
    crear_historial,
    listar_historiales,
    obtener_historial,
    actualizar_historial,
    desactivar_historial,
)

from ..models.persona import Persona
from ..security.roles import require_roles

router = APIRouter(prefix="/historial", tags=["Historial Vacunación"])

# ✅ Crear -> admin y medico
@router.post("/", response_model=HistorialVacunacionResponse)
def crear_historial_endpoint(
    data: HistorialVacunacionCreate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    return crear_historial(db, data)

# ✅ Listar -> admin y medico
@router.get("/", response_model=List[HistorialVacunacionResponse])
def listar_historiales_endpoint(
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    return listar_historiales(db)

# ✅ Obtener -> admin y medico
@router.get("/{id_historial}", response_model=HistorialVacunacionResponse)
def obtener_historial_endpoint(
    id_historial: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    h = obtener_historial(db, id_historial)
    if not h:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return h

# ✅ Actualizar -> admin y medico
@router.put("/{id_historial}", response_model=HistorialVacunacionResponse)
def actualizar_historial_endpoint(
    id_historial: int,
    data: HistorialVacunacionUpdate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    h = actualizar_historial(db, id_historial, data)
    if not h:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return h

# ✅ Eliminar -> admin y medico
@router.delete("/{id_historial}")
def eliminar_historial_endpoint(
    id_historial: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    ok = desactivar_historial(db, id_historial)
    if not ok:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return {"detail": "Historial desactivado correctamente"}
=======
# app/routers/historial_vacunacion.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.historial_vacunacion import (
    HistorialVacunacionCreate,
    HistorialVacunacionUpdate,
    HistorialVacunacionResponse,
)
from ..services.historial_vacunacion_service import (
    crear_historial,
    listar_historiales,
    obtener_historial,
    actualizar_historial,
    desactivar_historial,
)
from ..security.jwt import get_current_user
from ..models.persona import Persona

router = APIRouter(prefix="/historial", tags=["Historial Vacunación"])

@router.post("/", response_model=HistorialVacunacionResponse)
def crear_historial_endpoint(
    data: HistorialVacunacionCreate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    return crear_historial(db, data)

@router.get("/", response_model=List[HistorialVacunacionResponse])
def listar_historiales_endpoint(
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    return listar_historiales(db)

@router.get("/{id_historial}", response_model=HistorialVacunacionResponse)
def obtener_historial_endpoint(
    id_historial: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    h = obtener_historial(db, id_historial)
    if not h:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return h

@router.put("/{id_historial}", response_model=HistorialVacunacionResponse)
def actualizar_historial_endpoint(
    id_historial: int,
    data: HistorialVacunacionUpdate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    h = actualizar_historial(db, id_historial, data)
    if not h:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return h

@router.delete("/{id_historial}")
def eliminar_historial_endpoint(
    id_historial: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    ok = desactivar_historial(db, id_historial)
    if not ok:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return {"detail": "Historial desactivado correctamente"}
>>>>>>> 39b6a8b2c70a058d7af1d83a226d239ece197f4c
