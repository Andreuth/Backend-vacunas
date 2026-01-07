<<<<<<< HEAD
# app/routers/relacion_padre_hijo.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.relacion_padre_hijo import RelacionCreate, RelacionUpdate, RelacionResponse
from ..services.relacion_padre_hijo_service import (
    crear_relacion,
    listar_relaciones,
    obtener_relacion,
    actualizar_relacion,
    desactivar_relacion,
)

from ..models.persona import Persona
from ..security.roles import require_roles

router = APIRouter(prefix="/relaciones", tags=["Relaciones Padre-Hijo"])

# ✅ Crear -> admin y medico (porque registra tutores)
@router.post("/", response_model=RelacionResponse)
def crear_relacion_endpoint(
    data: RelacionCreate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    return crear_relacion(db, data)

# ✅ Listar -> admin y medico
@router.get("/", response_model=List[RelacionResponse])
def listar_relaciones_endpoint(
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    return listar_relaciones(db)

# ✅ Obtener -> admin y medico
@router.get("/{id_relacion}", response_model=RelacionResponse)
def obtener_relacion_endpoint(
    id_relacion: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    r = obtener_relacion(db, id_relacion)
    if not r:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return r

# ✅ Actualizar -> admin y medico
@router.put("/{id_relacion}", response_model=RelacionResponse)
def actualizar_relacion_endpoint(
    id_relacion: int,
    data: RelacionUpdate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    r = actualizar_relacion(db, id_relacion, data)
    if not r:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return r

# ✅ Eliminar -> admin y medico
@router.delete("/{id_relacion}")
def eliminar_relacion_endpoint(
    id_relacion: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    ok = desactivar_relacion(db, id_relacion)
    if not ok:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return {"detail": "Relación desactivada correctamente"}
=======
# app/routers/relacion_padre_hijo.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.relacion_padre_hijo import (
    RelacionCreate,
    RelacionUpdate,
    RelacionResponse,
)
from ..services.relacion_padre_hijo_service import (
    crear_relacion,
    listar_relaciones,
    obtener_relacion,
    actualizar_relacion,
    desactivar_relacion,
)
from ..security.jwt import get_current_user
from ..models.persona import Persona

router = APIRouter(prefix="/relaciones", tags=["Relaciones Padre-Hijo"])

@router.post("/", response_model=RelacionResponse)
def crear_relacion_endpoint(
    data: RelacionCreate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    return crear_relacion(db, data)

@router.get("/", response_model=List[RelacionResponse])
def listar_relaciones_endpoint(
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    return listar_relaciones(db)

@router.get("/{id_relacion}", response_model=RelacionResponse)
def obtener_relacion_endpoint(
    id_relacion: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    r = obtener_relacion(db, id_relacion)
    if not r:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return r

@router.put("/{id_relacion}", response_model=RelacionResponse)
def actualizar_relacion_endpoint(
    id_relacion: int,
    data: RelacionUpdate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    r = actualizar_relacion(db, id_relacion, data)
    if not r:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return r

@router.delete("/{id_relacion}")
def eliminar_relacion_endpoint(
    id_relacion: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    ok = desactivar_relacion(db, id_relacion)
    if not ok:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return {"detail": "Relación desactivada correctamente"}
>>>>>>> 39b6a8b2c70a058d7af1d83a226d239ece197f4c
