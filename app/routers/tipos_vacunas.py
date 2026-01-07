<<<<<<< HEAD
# app/routers/tipos_vacunas.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.tipos_vacunas import TipoVacunaCreate, TipoVacunaUpdate, TipoVacunaResponse
from ..services.tipos_vacunas_service import (
    crear_vacuna,
    listar_vacunas,
    obtener_vacuna,
    actualizar_vacuna,
    desactivar_vacuna,
)

from ..models.persona import Persona
from ..security.roles import require_roles

router = APIRouter(prefix="/vacunas", tags=["Tipos de Vacunas"])

# ✅ Crear -> admin y medico
@router.post("/", response_model=TipoVacunaResponse)
def crear_vacuna_endpoint(
    data: TipoVacunaCreate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
   return crear_vacuna(db, data, current_user)


# ✅ Listar -> admin, medico, padre
@router.get("/", response_model=List[TipoVacunaResponse])
def listar_vacunas_endpoint(
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico", "padre"])),
):
    return listar_vacunas(db)

# ✅ Obtener -> admin, medico, padre
@router.get("/{id_vacuna}", response_model=TipoVacunaResponse)
def obtener_vacuna_endpoint(
    id_vacuna: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico", "padre"])),
):
    vacuna = obtener_vacuna(db, id_vacuna)
    if not vacuna:
        raise HTTPException(status_code=404, detail="Vacuna no encontrada")
    return vacuna

# ✅ Actualizar -> admin y medico
@router.put("/{id_vacuna}", response_model=TipoVacunaResponse)
def actualizar_vacuna_endpoint(
    id_vacuna: int,
    data: TipoVacunaUpdate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    vacuna = actualizar_vacuna(db, id_vacuna, data, current_user)

    if not vacuna:
        raise HTTPException(status_code=404, detail="Vacuna no encontrada")
    return vacuna

# ✅ Eliminar -> admin y medico
@router.delete("/{id_vacuna}")
def eliminar_vacuna_endpoint(
    id_vacuna: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(require_roles(["admin", "medico"])),
):
    ok = desactivar_vacuna(db, id_vacuna)
    if not ok:
        raise HTTPException(status_code=404, detail="Vacuna no encontrada")
    return {"detail": "Vacuna desactivada correctamente"}
=======
# app/routers/tipos_vacunas.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.tipos_vacunas import (
    TipoVacunaCreate,
    TipoVacunaUpdate,
    TipoVacunaResponse,
)
from ..services.tipos_vacunas_service import (
    crear_vacuna,
    listar_vacunas,
    obtener_vacuna,
    actualizar_vacuna,
    desactivar_vacuna,
)
from ..security.jwt import get_current_user
from ..models.persona import Persona

router = APIRouter(prefix="/vacunas", tags=["Tipos de Vacunas"])

@router.post("/", response_model=TipoVacunaResponse)
def crear_vacuna_endpoint(
    data: TipoVacunaCreate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    return crear_vacuna(db, data)

@router.get("/", response_model=List[TipoVacunaResponse])
def listar_vacunas_endpoint(
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    return listar_vacunas(db)

@router.get("/{id_vacuna}", response_model=TipoVacunaResponse)
def obtener_vacuna_endpoint(
    id_vacuna: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    vacuna = obtener_vacuna(db, id_vacuna)
    if not vacuna:
        raise HTTPException(status_code=404, detail="Vacuna no encontrada")
    return vacuna

@router.put("/{id_vacuna}", response_model=TipoVacunaResponse)
def actualizar_vacuna_endpoint(
    id_vacuna: int,
    data: TipoVacunaUpdate,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    vacuna = actualizar_vacuna(db, id_vacuna, data)
    if not vacuna:
        raise HTTPException(status_code=404, detail="Vacuna no encontrada")
    return vacuna

@router.delete("/{id_vacuna}")
def eliminar_vacuna_endpoint(
    id_vacuna: int,
    db: Session = Depends(get_db),
    current_user: Persona = Depends(get_current_user),
):
    ok = desactivar_vacuna(db, id_vacuna)
    if not ok:
        raise HTTPException(status_code=404, detail="Vacuna no encontrada")
    return {"detail": "Vacuna desactivada correctamente"}
>>>>>>> 39b6a8b2c70a058d7af1d83a226d239ece197f4c
